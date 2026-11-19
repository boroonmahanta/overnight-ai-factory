#!/usr/bin/env python3
"""Spike 0.14 part 3 (plan 5.11, 5.14): a stdio shim in front of the Dataverse CLI's MCP proxy.

Published as probe/mcp_shim.py in GetAI-IP/export-probe (private, scratch). A probe for
the Stage 3 driver, not a gate script.

    python3 -I mcp_shim.py --cap N --log FILE [options] -- dataverse mcp <url>

It sits between an MCP client (on the shim's own stdin and stdout) and the proxy it
starts (the command after --), and passes newline-delimited JSON-RPC both ways. For
each tools/call request it:

  - counts the call, and every attempt it sends to the proxy under its own ID
    ("shim-<n>"), so a late answer can never be taken for a retry's answer. Each
    attempt that reaches Dataverse is billed 0.1 Copilot Credit; initialize,
    tools/list and refused calls are not (spike 0.3);
  - refuses an attempt past --cap with a JSON-RPC error and sends nothing to the
    proxy; retries count against the cap. That is a stop, PARK type budget;
  - retries a failed attempt up to --retries times, waiting --backoff seconds and
    doubling. Failed means: a JSON-RPC error, a result with isError, no answer
    within --timeout, or an answer dropped by --fault. A call that still fails goes
    back to the client with its last error, and is a stop, PARK type
    --park-on-failure;
  - after the first stop, refuses every later tools/call, unless --keep-going
    (probe only, so one session can show several failures);
  - logs every call, attempt, answer, retry, refusal, late answer and stop as JSON
    lines (--log), keeps the proxy's stderr (--proxy-log), and copies the proxy's
    stderr lines from each failed attempt into that attempt's record: the proxy
    hides an upstream cause behind -32603 (spike 0.3 finding 3);
  - keeps running counts in --summary and the first stop in --stop-file, for the
    driver to read.

Everything else (initialize, tools/list, notifications, the server's own requests
and the client's answers to them) passes through unchanged.

Probe only: --fault drop-answer:<tool>:<n> throws away the proxy's answer to the
first attempt of the n-th call of <tool>, and treats it as no answer, so a retry
follows. Used to see whether a retried create writes twice.

Not handled: notifications/cancelled for a tools/call (it passes through with the
client's ID, which the proxy does not know); restarting a proxy that exits.

Standard library only (python3 -I). Never writes a token: every log line goes
through a filter that removes token-shaped strings.
"""

import argparse
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time

JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]*")
STATUS = re.compile(r"\b([45]\d\d)\b")
PROXY_GONE = object()

CAP_CODE = -32010        # refused: the cap is used
STOPPED_CODE = -32011    # refused: the session stopped earlier
NO_ANSWER_CODE = -32012  # no usable answer after every attempt, or the proxy exited


def redact(text):
    return JWT.sub("[token removed]", text or "")


def clip(text, limit=1200):
    text = " ".join(redact(str(text)).split())
    return text if len(text) <= limit else text[:limit] + " ...[cut]"


def now():
    stamp = time.time()
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(stamp)) + f".{int(stamp * 1000) % 1000:03d}Z"


def answer_text(answer):
    """The words of an answer, for the log: the error, or the result's text parts."""
    if not isinstance(answer, dict):
        return ""
    if "error" in answer:
        return json.dumps(answer["error"])
    result = answer.get("result") or {}
    parts = [part.get("text", "") for part in result.get("content") or [] if isinstance(part, dict)]
    if result.get("structuredContent") is not None:
        parts.append(json.dumps(result["structuredContent"]))
    return "\n".join(parts)


def kind_of(answer):
    if answer is None:
        return "no_answer"
    if answer is PROXY_GONE:
        return "proxy_exit"
    if "error" in answer:
        return "rpc_error"
    if (answer.get("result") or {}).get("isError"):
        return "tool_error"
    return "ok"


def parse_fault(text):
    parts = text.split(":")
    if len(parts) != 3 or parts[0] != "drop-answer" or not parts[2].isdigit() or int(parts[2]) < 1:
        raise SystemExit(f"--fault must be drop-answer:<tool>:<n>, not {text!r}")
    return parts[1], int(parts[2])


class Shim:
    def __init__(self, args, command):
        self.args = args
        self.faults = [parse_fault(f) for f in args.fault]
        self.lock = threading.Lock()         # counts, pending, stops
        self.log_lock = threading.Lock()
        self.summary_lock = threading.Lock()
        self.client_lock = threading.Lock()  # our stdout
        self.proxy_lock = threading.Lock()   # the proxy's stdin
        self.pending = {}
        self.handlers = []
        self.stderr_lines = []
        self.stops = []
        self.proxy_gone = False
        self.seen = {}
        self.counts = {"calls": 0, "attempts": 0, "refused": 0, "retries": 0, "late_answers": 0,
                       "outcomes": {}, "tools": {}}
        self.started = now()
        self.log_handle = open(args.log, "a", encoding="utf-8")
        self.proxy_log = open(args.proxy_log, "a", encoding="utf-8") if args.proxy_log else None
        self.proxy = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, encoding="utf-8", errors="replace", bufsize=1)
        self.log("start", command=" ".join(command), cap=args.cap, retries=args.retries, timeout=args.timeout,
                 backoff=args.backoff, keep_going=args.keep_going, faults=args.fault,
                 park_on_failure=args.park_on_failure, proxy_pid=self.proxy.pid)
        threading.Thread(target=self.read_proxy, daemon=True).start()
        threading.Thread(target=self.read_proxy_stderr, daemon=True).start()

    # ---------- plumbing ----------

    def log(self, event, **fields):
        record = {"at": now(), "event": event}
        record.update(fields)
        line = redact(json.dumps(record, default=str))
        with self.log_lock:
            self.log_handle.write(line + "\n")
            self.log_handle.flush()

    def to_client(self, message):
        with self.client_lock:
            sys.stdout.write(json.dumps(message) + "\n")
            sys.stdout.flush()

    def to_proxy(self, message):
        with self.proxy_lock:
            try:
                self.proxy.stdin.write(json.dumps(message) + "\n")
                self.proxy.stdin.flush()
                return True
            except (BrokenPipeError, OSError, ValueError):
                return False

    def read_proxy(self):
        for line in self.proxy.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except ValueError:
                self.log("proxy-stdout-not-json", text=clip(line, 400))
                continue
            if isinstance(message, dict) and "method" not in message and "id" in message:
                with self.lock:
                    waiting = self.pending.get(message["id"])
                if waiting is not None:
                    waiting.put(message)
                    continue
                if isinstance(message["id"], str) and message["id"].startswith("shim-"):
                    # An answer to an attempt the shim gave up on. For a write, it means the write landed.
                    with self.lock:
                        self.counts["late_answers"] += 1
                    self.log("late-answer", upstream_id=message["id"], kind=kind_of(message),
                             text=clip(answer_text(message), 1500))
                    continue
            self.to_client(message)
        with self.lock:
            self.proxy_gone = True
            waiting = list(self.pending.values())
        for each in waiting:
            each.put(PROXY_GONE)
        self.log("proxy-exit", code=self.proxy.poll())

    def read_proxy_stderr(self):
        for line in self.proxy.stderr:
            line = redact(line.rstrip("\n"))
            with self.lock:
                self.stderr_lines.append((time.time(), line))
                if len(self.stderr_lines) > 5000:
                    del self.stderr_lines[:1000]
            if self.proxy_log:
                self.proxy_log.write(f"{now()} {line}\n")
                self.proxy_log.flush()

    def stderr_since(self, started):
        with self.lock:
            return [line for stamp, line in self.stderr_lines if stamp >= started]

    def write_summary(self, final=False):
        if not self.args.summary:
            return
        with self.lock:
            data = json.loads(json.dumps(self.counts))
            data.update(cap=self.args.cap, retries_allowed=self.args.retries, timeout=self.args.timeout,
                        stops=list(self.stops), started=self.started, updated=now(), final=final,
                        proxy_exit_code=self.proxy.poll())
        with self.summary_lock:   # calls can end at the same moment
            temporary = self.args.summary + ".tmp"
            with open(temporary, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
            os.replace(temporary, self.args.summary)

    def record_stop(self, reason, park, tool, call_no, detail):
        stop = {"reason": reason, "park": park, "tool": tool, "call": call_no, "detail": detail, "at": now()}
        with self.lock:
            first = not self.stops
            self.stops.append(stop)
        self.log("stop" if first else "stop-again", **stop)
        if first and self.args.stop_file:
            with open(self.args.stop_file, "w", encoding="utf-8") as handle:
                json.dump(stop, handle, indent=2)
        return stop

    def refuse(self, client_id, call_no, tool, code, text, stop):
        with self.lock:
            self.counts["refused"] += 1
            self.counts["tools"][tool]["refused"] += 1
            used = self.counts["attempts"]
        data = {"source": "spike-0.14 mcp shim", "reason": stop["reason"], "park": stop["park"],
                "cap": self.args.cap, "used": used}
        self.to_client({"jsonrpc": "2.0", "id": client_id, "error": {"code": code, "message": text, "data": data}})
        self.log("refused", call=call_no, tool=tool, code=code, message=text)

    def fault_hits(self, tool, nth):
        return any(tool == want and nth == n for want, n in self.faults)

    # ---------- one tools/call ----------

    def handle_call(self, message):
        client_id = message.get("id")
        params = message.get("params") or {}
        tool = params.get("name")
        with self.lock:
            self.counts["calls"] += 1
            call_no = self.counts["calls"]
            self.seen[tool] = nth = self.seen.get(tool, 0) + 1
            per = self.counts["tools"].setdefault(tool, {"calls": 0, "attempts": 0, "ok": 0, "failed": 0, "refused": 0})
            per["calls"] += 1
            stopped = self.stops[0] if self.stops else None
        self.log("call", call=call_no, client_id=client_id, tool=tool, nth_of_tool=nth,
                 arguments=clip(json.dumps(params.get("arguments")), 800))
        if stopped and not self.args.keep_going:
            return self.refuse(client_id, call_no, tool, STOPPED_CODE,
                               f"Refused: this session stopped earlier ({stopped['reason']}, PARK {stopped['park']}). "
                               f"Not sent to Dataverse.", stopped)
        attempt, last_kind = 0, None
        while True:
            with self.lock:
                gone = self.proxy_gone
                over = self.counts["attempts"] >= self.args.cap
                if not (gone or over):
                    self.counts["attempts"] += 1
                    per["attempts"] += 1
                    upstream_id = f"shim-{self.counts['attempts']}"
                    waiting = queue.Queue()
                    self.pending[upstream_id] = waiting
            if over:
                stop = self.record_stop("cap", "budget", tool, call_no,
                                        f"all {self.args.cap} MCP calls of this session are used"
                                        + (f"; {attempt} attempt(s) of this call failed before" if attempt else ""))
                return self.refuse(client_id, call_no, tool, CAP_CODE,
                                   f"Refused: the MCP call cap is reached ({self.args.cap} calls this session). "
                                   f"Not sent to Dataverse. The session stops here (PARK budget).", stop)
            if gone:
                stop = self.record_stop("proxy-exit", self.args.park_on_failure, tool, call_no,
                                        f"the Dataverse proxy exited (code {self.proxy.poll()})")
                with self.lock:
                    per["failed"] += 1
                self.to_client({"jsonrpc": "2.0", "id": client_id, "error": {
                    "code": NO_ANSWER_CODE, "message": "The Dataverse proxy has exited. Not sent.",
                    "data": {"source": "spike-0.14 mcp shim", "reason": stop["reason"], "park": stop["park"]}}})
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind="proxy_exit")
                return
            attempt += 1
            if attempt > 1:
                with self.lock:
                    self.counts["retries"] += 1
                self.log("retry", call=call_no, tool=tool, attempt=attempt, after=last_kind)
            started = time.time()
            self.log("attempt", call=call_no, tool=tool, attempt=attempt, upstream_id=upstream_id)
            answer = None
            if self.to_proxy(dict(message, id=upstream_id)):
                try:
                    answer = waiting.get(timeout=self.args.timeout)
                except queue.Empty:
                    answer = None
            else:
                answer = PROXY_GONE
                with self.lock:          # never sent, so not an attempt
                    self.counts["attempts"] -= 1
                    per["attempts"] -= 1
            with self.lock:
                self.pending.pop(upstream_id, None)
            seconds = round(time.time() - started, 2)
            kind = kind_of(answer)
            if attempt == 1 and isinstance(answer, dict) and self.fault_hits(tool, nth):
                self.log("fault-dropped-answer", call=call_no, tool=tool, upstream_id=upstream_id,
                         kind_dropped=kind, text=clip(answer_text(answer), 1500))
                answer, kind = None, "dropped"
            stderr = []
            if kind != "ok":
                time.sleep(0.3)   # let the proxy's stderr for this attempt arrive
                stderr = self.stderr_since(started)
            with self.lock:
                self.counts["outcomes"][kind] = self.counts["outcomes"].get(kind, 0) + 1
                if kind == "ok":
                    per["ok"] += 1
            self.log("answer", call=call_no, tool=tool, attempt=attempt, upstream_id=upstream_id, kind=kind,
                     seconds=seconds, text=clip(answer_text(answer), 2000),
                     proxy_stderr=[clip(line, 500) for line in stderr[-20:]],
                     status_hint=sorted(set(STATUS.findall(" ".join(stderr)))))
            if kind == "ok":
                self.to_client(dict(answer, id=client_id))
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind="ok")
                return
            last_kind = kind
            if kind == "proxy_exit":
                continue   # the next pass sees the proxy gone and stops
            if attempt > self.args.retries:
                stop = self.record_stop("failed-after-retries", self.args.park_on_failure, tool, call_no,
                                        f"{tool} failed {attempt} times; the last was {kind}")
                with self.lock:
                    per["failed"] += 1
                if isinstance(answer, dict):
                    self.to_client(dict(answer, id=client_id))
                else:
                    self.to_client({"jsonrpc": "2.0", "id": client_id, "error": {
                        "code": NO_ANSWER_CODE,
                        "message": f"No usable answer from the Dataverse proxy to {tool} after {attempt} attempts.",
                        "data": {"source": "spike-0.14 mcp shim", "reason": stop["reason"], "park": stop["park"],
                                 "last": kind}}})
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind=kind)
                return
            time.sleep(self.args.backoff * (2 ** (attempt - 1)))

    def guarded_call(self, message):
        try:
            self.handle_call(message)
        except Exception as error:   # never leave the client waiting
            self.log("shim-error", error=f"{type(error).__name__}: {error}")
            self.to_client({"jsonrpc": "2.0", "id": message.get("id"),
                            "error": {"code": -32603, "message": f"shim error: {type(error).__name__}"}})
        finally:
            self.write_summary()

    # ---------- main loop ----------

    def run(self):
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except ValueError:
                self.log("client-stdin-not-json", text=clip(line, 400))
                continue
            if isinstance(message, dict) and message.get("method") == "tools/call" and "id" in message:
                thread = threading.Thread(target=self.guarded_call, args=(message,), daemon=True)
                self.handlers.append(thread)
                thread.start()
                continue
            if not self.to_proxy(message):
                method = message.get("method") if isinstance(message, dict) else None
                self.log("pass-through-failed", method=method)
                if isinstance(message, dict) and method and "id" in message:
                    self.to_client({"jsonrpc": "2.0", "id": message["id"],
                                    "error": {"code": NO_ANSWER_CODE, "message": "The Dataverse proxy has exited."}})
        self.log("client-closed")
        limit = self.args.timeout * (self.args.retries + 1) + self.args.backoff * (2 ** self.args.retries) + 30
        for thread in self.handlers:
            thread.join(timeout=limit)
        try:
            self.proxy.stdin.close()
        except OSError:
            pass
        try:
            self.proxy.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.proxy.terminate()
            try:
                self.proxy.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proxy.kill()
                self.proxy.wait()
        time.sleep(0.2)
        self.write_summary(final=True)
        with self.lock:
            totals = {k: self.counts[k] for k in ("calls", "attempts", "refused", "retries", "late_answers")}
        self.log("end", proxy_exit_code=self.proxy.poll(), stops=len(self.stops), **totals)
        return 0


def main(argv):
    if "--" not in argv:
        print("usage: mcp_shim.py --cap N --log FILE [options] -- <proxy command>", file=sys.stderr)
        return 2
    split = argv.index("--")
    parser = argparse.ArgumentParser(prog="mcp_shim.py")
    parser.add_argument("--cap", type=int, required=True, help="MCP calls (attempts sent) allowed this session")
    parser.add_argument("--retries", type=int, default=3, help="retries after a failed attempt")
    parser.add_argument("--timeout", type=float, default=120.0, help="seconds to wait for each answer")
    parser.add_argument("--backoff", type=float, default=1.0, help="first wait before a retry, doubled each time")
    parser.add_argument("--log", required=True, help="JSON lines: every call, attempt, answer and stop")
    parser.add_argument("--proxy-log", help="the proxy's stderr, time-stamped")
    parser.add_argument("--summary", help="running counts, rewritten after every call")
    parser.add_argument("--stop-file", help="the first stop, written when it happens")
    parser.add_argument("--park-on-failure", default="tool_failure", help="PARK type for a call that still fails")
    parser.add_argument("--keep-going", action="store_true", help="probe only: keep passing calls after a stop")
    parser.add_argument("--fault", action="append", default=[], help="probe only: drop-answer:<tool>:<n>")
    args = parser.parse_args(argv[:split])
    command = argv[split + 1:]
    if not command or args.cap < 0 or args.retries < 0:
        parser.error("a proxy command after --, a cap of 0 or more and retries of 0 or more are needed")
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    return Shim(args, command).run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
