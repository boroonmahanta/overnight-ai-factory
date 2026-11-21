#!/usr/bin/env python3
"""Spike 0.14 parts 3 and 4 (plan 5.11, 5.14): a stdio shim in front of the Dataverse CLI's MCP proxy.

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
  - follows the retry rule Boroon accepted on 20 November 2026 (spike 0.14 part 3):
      * a tool result with isError is the tool saying no (a bad query, a missing
        table, a duplicate key): it goes back to the client at once, with no retry
        and no stop, unless its text says the call was throttled (429, 503, "too
        many requests"), which is retried up to --retries times, waiting as long as
        the answer asks (at most --max-wait seconds);
      * no answer within --timeout, a JSON-RPC error from the proxy, or the proxy
        exiting is retried up to --retries times with back-off (--backoff, doubled),
        starting the proxy again first if it exited, but only for a call that is
        safe to repeat: a read, an update or delete by row ID, or a create whose
        every record carries a row ID. Any other call (a table change, a file
        upload, invoke_api, a tool the shim does not know) is not retried;
      * every create gets a row ID before its first attempt: for each record with
        none, the shim adds the table's primary key (its name from the Web API's
        EntityDefinitions, through --keys-file or --webapi) with a new GUID;
      * on a retry, "duplicate key" for a single create, or "does not exist" for a
        single delete, means the earlier attempt landed: the shim answers success.
        For a batch it cannot tell which records landed, so that is a failure;
      * a call that still fails, or one that is not safe to retry, goes back to the
        client with its last error and is a stop, PARK type --park-on-failure
        (tool_failure);
  - after the first stop, refuses every later tools/call, unless --keep-going
    (probe only, so one session can show several failures);
  - logs every call, attempt, answer (its text and correlation ID), retry, refusal,
    late answer, row ID added, proxy restart and stop as JSON lines (--log), keeps
    the proxy's stderr (--proxy-log), and copies the proxy's stderr lines from each
    failed attempt into that attempt's record;
  - keeps running counts in --summary and the first stop in --stop-file, for the
    driver to read; logs the tool names from tools/list as they pass.

Everything else (initialize, tools/list, notifications, the server's own requests
and the client's answers to them) passes through unchanged, except that a client's
notifications/cancelled for a call is sent on under that call's current attempt ID.

Probe only: --fault drop-answer:<tool>:<n> throws away the proxy's answer to the
first attempt of the n-th call of <tool>, and treats it as no answer, so a retry
follows.

Standard library only (python3 -I). Never writes a token: every log line goes
through a filter that removes token-shaped strings, and the Web API token is never
logged.
"""

import argparse
import json
import os
import queue
import re
import shlex
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]*")
STATUS = re.compile(r"\b([45]\d\d)\b")
CORRELATION = re.compile(r"correlation ID:\s*([0-9a-fA-F-]{36})")
THROTTLED = re.compile(r"(?<![\w-])(429|503)(?![\w-])|too many requests|throttl|rate limit|"
                       r"exceeded the limit|service unavailable|server is busy", re.I)
RETRY_AFTER = re.compile(r"retry[- ]after[:\s]+(\d+(?:\.\d+)?)", re.I)
DUPLICATE = re.compile(r"duplicate key", re.I)
NOT_FOUND = re.compile(r"does not exist|was not found|\bnot found\b", re.I)
MISSING_TABLE = re.compile(r"entity with name \S+ and id 0{8}-", re.I)
PROXY_GONE = object()

CAP_CODE = -32010        # refused: the cap is used
STOPPED_CODE = -32011    # refused: the session stopped earlier
NO_ANSWER_CODE = -32012  # no usable answer after every attempt, or the proxy exited

# The Dataverse MCP server's tools (16 in spike 0.14 part 3), by how safe a repeat is.
READ_TOOLS = {"read_query", "search", "search_data", "describe", "file_download"}
ROW_WRITE_TOOLS = {"update_record", "delete_record"}   # by row ID: a repeat changes nothing more
CREATE_TOOL = "create_record"
RECORD_ID_ARGS = ("recordid", "record_id", "id", "rowid", "row_id")


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
        return "throttled" if THROTTLED.search(answer_text(answer)) else "tool_error"
    return "ok"


def parse_fault(text):
    parts = text.split(":")
    if len(parts) != 3 or parts[0] != "drop-answer" or not parts[2].isdigit() or int(parts[2]) < 1:
        raise SystemExit(f"--fault must be drop-answer:<tool>:<n>, not {text!r}")
    return parts[1], int(parts[2])


def find_arg(arguments, names):
    """The first argument whose name matches one of `names`, ignoring case."""
    for key in arguments:
        if key.lower() in names:
            return key
    return None


class Keys:
    """Each table's primary key name, from --keys-file and then the Web API's EntityDefinitions."""

    def __init__(self, args):
        self.args = args
        self.known = {}
        self.token, self.token_at = None, 0.0
        self.lock = threading.Lock()
        if args.keys_file:
            with open(args.keys_file, encoding="utf-8") as handle:
                self.known.update({k.lower(): v for k, v in json.load(handle).items()})

    def _token(self):
        if self.token and time.time() - self.token_at < 1800:
            return self.token
        argv = [part.replace("{url}", self.args.webapi.rstrip("/")) for part in shlex.split(self.args.token_command)]
        process = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
        if process.returncode != 0 or not process.stdout.strip():
            raise RuntimeError(f"the token command failed (exit {process.returncode}): {clip(process.stderr, 300)}")
        self.token, self.token_at = process.stdout.strip(), time.time()
        return self.token

    def primary_key(self, table):
        table = (table or "").lower()
        with self.lock:
            if table in self.known:
                return self.known[table], "cache"
            if not (self.args.webapi and table and re.fullmatch(r"[a-z0-9_]+", table)):
                return None, "no Web API to ask"
            url = (f"{self.args.webapi.rstrip('/')}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')"
                   "?$select=PrimaryIdAttribute")
            try:
                request = urllib.request.Request(url, headers={
                    "Authorization": "Bearer " + self._token(), "Accept": "application/json",
                    "OData-MaxVersion": "4.0", "OData-Version": "4.0"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    key = json.load(response).get("PrimaryIdAttribute")
            except urllib.error.HTTPError as error:
                return None, f"EntityDefinitions answered HTTP {error.code}"
            except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
                return None, f"EntityDefinitions not read: {clip(error, 300)}"
            if key:
                self.known[table] = key
                return key, "web api"
            return None, "EntityDefinitions gave no PrimaryIdAttribute"


class Shim:
    def __init__(self, args, command):
        self.args = args
        self.command = command
        self.faults = [parse_fault(f) for f in args.fault]
        self.lock = threading.Lock()         # counts, pending, stops, the proxy
        self.log_lock = threading.Lock()
        self.summary_lock = threading.Lock()
        self.client_lock = threading.Lock()  # our stdout
        self.proxy_lock = threading.Lock()   # the proxy's stdin
        self.restart_lock = threading.Lock()
        self.pending = {}
        self.in_flight = {}                  # the client's call ID -> the attempt ID now at the proxy
        self.handlers = []
        self.stderr_lines = []
        self.stops = []
        self.proxy_gone = False
        self.initialize = None               # the client's initialize request, for a restart
        self.list_ids = set()                # tools/list requests whose answers to log
        self.seen = {}
        self.counts = {"calls": 0, "attempts": 0, "refused": 0, "retries": 0, "late_answers": 0,
                       "ids_added": 0, "resolved_on_retry": 0, "tool_errors_returned": 0,
                       "not_retried_unsafe": 0, "restarts": 0, "outcomes": {}, "tools": {}}
        self.started = now()
        self.log_handle = open(args.log, "a", encoding="utf-8")
        self.proxy_log = open(args.proxy_log, "a", encoding="utf-8") if args.proxy_log else None
        self.keys = Keys(args)
        self.proxy = None
        self.start_proxy()
        self.log("start", command=" ".join(command), cap=args.cap, retries=args.retries, timeout=args.timeout,
                 backoff=args.backoff, keep_going=args.keep_going, faults=args.fault,
                 park_on_failure=args.park_on_failure, proxy_pid=self.proxy.pid,
                 keys_known=len(self.keys.known), webapi=bool(args.webapi))

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

    def start_proxy(self):
        process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", bufsize=1)
        with self.lock:
            self.proxy = process
            self.proxy_gone = False
        threading.Thread(target=self.read_proxy, args=(process,), daemon=True).start()
        threading.Thread(target=self.read_proxy_stderr, args=(process,), daemon=True).start()
        return process

    def restart_proxy(self, why):
        """Start the proxy again and replay the client's initialize, so a retry can follow."""
        with self.restart_lock:
            with self.lock:
                if not self.proxy_gone:
                    return True   # another call restarted it already
                if self.counts["restarts"] >= self.args.max_restarts or self.initialize is None:
                    return False
                self.counts["restarts"] += 1
                number = self.counts["restarts"]
            old_code = self.proxy.poll()
            process = self.start_proxy()
            waiting = queue.Queue()
            init_id = f"shim-init-{number}"
            with self.lock:
                self.pending[init_id] = waiting
            ok = self.to_proxy(dict(self.initialize, id=init_id))
            try:
                answer = waiting.get(timeout=self.args.timeout) if ok else None
            except queue.Empty:
                answer = None
            with self.lock:
                self.pending.pop(init_id, None)
            ok = isinstance(answer, dict) and "result" in answer
            if ok:
                self.to_proxy({"jsonrpc": "2.0", "method": "notifications/initialized"})
            self.log("proxy-restart", number=number, why=why, old_exit_code=old_code, new_pid=process.pid, ok=ok)
            return ok

    def read_proxy(self, process):
        for line in process.stdout:
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
                    listed = message["id"] in self.list_ids
                    self.list_ids.discard(message["id"])
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
                if listed:
                    tools = ((message.get("result") or {}).get("tools")) or []
                    self.log("tools-list", count=len(tools), names=sorted(t.get("name", "") for t in tools))
            self.to_client(message)
        with self.lock:
            if process is not self.proxy:
                return
            self.proxy_gone = True
            waiting = list(self.pending.values())
        for each in waiting:
            each.put(PROXY_GONE)
        self.log("proxy-exit", code=process.wait())

    def read_proxy_stderr(self, process):
        for line in process.stderr:
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

    def record_stop(self, reason, park, tool, call_no, detail, last_text=""):
        stop = {"reason": reason, "park": park, "tool": tool, "call": call_no, "detail": detail, "at": now()}
        if last_text:
            stop["last_answer"] = clip(last_text, 1500)
            found = CORRELATION.search(last_text)
            if found:
                stop["correlation_id"] = found.group(1)
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

    # ---------- what a call is ----------

    def prepare(self, tool, message, call_no):
        """Add a row ID to every record of a create that has none. Returns (message, plan)."""
        arguments = dict(((message.get("params") or {}).get("arguments")) or {})
        plan = {"safe": False, "single": True, "record_id": None, "write": None}
        if tool in READ_TOOLS:
            plan["safe"] = True
            return message, plan
        if tool in ROW_WRITE_TOOLS:
            plan["write"] = "delete" if tool == "delete_record" else "update"
            id_arg = find_arg(arguments, RECORD_ID_ARGS)
            plan["record_id"] = arguments.get(id_arg) if id_arg else None
            batch = any(isinstance(arguments.get(k), list) for k in arguments if k.lower() in ("items", "records", "ids"))
            plan["single"] = not batch
            plan["safe"] = bool(plan["record_id"]) or batch
            return message, plan
        if tool != CREATE_TOOL:
            return message, plan   # a table change, a file upload, invoke_api or an unknown tool: never repeated
        plan["write"] = "create"
        table_arg = find_arg(arguments, ("tablename", "table", "entityname", "logicalname"))
        table = arguments.get(table_arg) if table_arg else None
        key, source = self.keys.primary_key(table)
        records, as_text = [], {}
        for arg in ("item", "items"):
            value = arguments.get(arg)
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                    as_text[arg] = True
                except ValueError:
                    continue
            if isinstance(value, dict):
                value = dict(value)
                records.append(value)
                arguments[arg] = value
            elif isinstance(value, list):
                plan["single"] = False
                value = [dict(each) if isinstance(each, dict) else each for each in value]
                records.extend(each for each in value if isinstance(each, dict))
                arguments[arg] = value
        if not records or not key:
            self.log("id-not-added", call=call_no, tool=tool, table=table,
                     why="no record in the call" if not records else source)
            return message, plan
        added = []
        for record in records:
            have = next((k for k in record if k.lower() == key.lower()), None)
            if have and record[have]:
                plan["record_id"] = plan["record_id"] or str(record[have])
                continue
            record[key] = str(uuid.uuid4())
            plan["record_id"] = plan["record_id"] or record[key]
            added.append(record[key])
        for arg in as_text:
            arguments[arg] = json.dumps(arguments[arg])
        plan["safe"] = True
        if added:
            with self.lock:
                self.counts["ids_added"] += len(added)
            self.log("id-added", call=call_no, tool=tool, table=table, key=key, key_from=source, ids=added)
        params = dict(message.get("params") or {}, arguments=arguments)
        return dict(message, params=params), plan

    @staticmethod
    def landed_already(plan, kind, text, earlier_unknown):
        """After an attempt whose fate is unknown, is this tool error the earlier attempt's success?"""
        if not earlier_unknown or kind != "tool_error" or not plan["single"]:
            return False
        if plan["write"] == "create":
            return bool(DUPLICATE.search(text))
        if plan["write"] == "delete":
            return bool(NOT_FOUND.search(text)) and not MISSING_TABLE.search(text)
        return False

    # ---------- one tools/call ----------

    def handle_call(self, message):
        client_id = message.get("id")
        params = message.get("params") or {}
        tool = params.get("name")
        with self.lock:
            self.counts["calls"] += 1
            call_no = self.counts["calls"]
            self.seen[tool] = nth = self.seen.get(tool, 0) + 1
            per = self.counts["tools"].setdefault(tool, {"calls": 0, "attempts": 0, "ok": 0, "failed": 0, "refused": 0,
                                                         "tool_errors": 0})
            per["calls"] += 1
            stopped = self.stops[0] if self.stops else None
        self.log("call", call=call_no, client_id=client_id, tool=tool, nth_of_tool=nth,
                 arguments=clip(json.dumps(params.get("arguments")), 800))
        if stopped and not self.args.keep_going:
            return self.refuse(client_id, call_no, tool, STOPPED_CODE,
                               f"Refused: this session stopped earlier ({stopped['reason']}, PARK {stopped['park']}). "
                               f"Not sent to Dataverse.", stopped)
        message, plan = self.prepare(tool, message, call_no)
        attempt, last_kind, earlier_unknown = 0, None, False
        while True:
            with self.lock:
                gone = self.proxy_gone
            if gone:
                gone = not self.restart_proxy(f"before attempt {attempt + 1} of call {call_no} ({tool})")
            with self.lock:
                over = self.counts["attempts"] >= self.args.cap
                if not (gone or over):
                    self.counts["attempts"] += 1
                    per["attempts"] += 1
                    upstream_id = f"shim-{self.counts['attempts']}"
                    waiting = queue.Queue()
                    self.pending[upstream_id] = waiting
                    self.in_flight[client_id] = upstream_id
            if over:
                stop = self.record_stop("cap", "budget", tool, call_no,
                                        f"all {self.args.cap} MCP calls of this session are used"
                                        + (f"; {attempt} attempt(s) of this call failed before" if attempt else ""))
                return self.refuse(client_id, call_no, tool, CAP_CODE,
                                   f"Refused: the MCP call cap is reached ({self.args.cap} calls this session). "
                                   f"Not sent to Dataverse. The session stops here (PARK budget).", stop)
            if gone:
                stop = self.record_stop("proxy-exit", self.args.park_on_failure, tool, call_no,
                                        f"the Dataverse proxy exited (code {self.proxy.poll()}) and could not be "
                                        f"started again")
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
                    self.proxy_gone = True
            with self.lock:
                self.pending.pop(upstream_id, None)
                self.in_flight.pop(client_id, None)
            seconds = round(time.time() - started, 2)
            kind = kind_of(answer)
            if attempt == 1 and isinstance(answer, dict) and self.fault_hits(tool, nth):
                self.log("fault-dropped-answer", call=call_no, tool=tool, upstream_id=upstream_id,
                         kind_dropped=kind, text=clip(answer_text(answer), 1500))
                answer, kind = None, "dropped"
            text = answer_text(answer)
            stderr = []
            if kind != "ok":
                time.sleep(0.3)   # let the proxy's stderr for this attempt arrive
                stderr = self.stderr_since(started)
            found = CORRELATION.search(text)
            with self.lock:
                self.counts["outcomes"][kind] = self.counts["outcomes"].get(kind, 0) + 1
                if kind == "ok":
                    per["ok"] += 1
            self.log("answer", call=call_no, tool=tool, attempt=attempt, upstream_id=upstream_id, kind=kind,
                     seconds=seconds, text=clip(text, 2000), correlation_id=found.group(1) if found else None,
                     proxy_stderr=[clip(line, 500) for line in stderr[-20:]],
                     status_hint=sorted(set(STATUS.findall(" ".join(stderr)))))
            if kind == "ok":
                self.to_client(dict(answer, id=client_id))
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind="ok")
                return
            if self.landed_already(plan, kind, text, earlier_unknown):
                with self.lock:
                    self.counts["resolved_on_retry"] += 1
                    per["ok"] += 1
                verb = "Created" if plan["write"] == "create" else "Deleted"
                words = (f"{verb} record with ID {plan['record_id']}. (Spike 0.14 shim: an earlier attempt of this call "
                         f"got no usable answer; the retry found it had landed: {clip(text, 300)})")
                self.to_client({"jsonrpc": "2.0", "id": client_id,
                                "result": {"content": [{"type": "text", "text": words}], "isError": False}})
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind="landed-already",
                         record_id=plan["record_id"])
                return
            if kind == "tool_error" and not (earlier_unknown and plan["write"] and not plan["single"]):
                # The tool said no: the client's call to fix. No retry, no stop.
                with self.lock:
                    self.counts["tool_errors_returned"] += 1
                    per["tool_errors"] += 1
                self.to_client(dict(answer, id=client_id))
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind="tool_error")
                return
            last_kind = kind
            if kind in ("no_answer", "dropped", "rpc_error", "proxy_exit"):
                earlier_unknown = True
            batch_unknown = kind == "tool_error"   # a batch write whose earlier attempt may have landed in part
            retryable = not batch_unknown and (kind == "throttled" or plan["safe"])
            if not retryable or attempt > self.args.retries:
                if not retryable:
                    with self.lock:
                        self.counts["not_retried_unsafe"] += 1
                if batch_unknown:
                    reason, why = "batch-unconfirmed", (f"{tool} is a batch; an earlier attempt got no usable answer "
                                                        f"and the retry says no, so which records landed is unknown")
                elif not retryable:
                    reason, why = "not-safe-to-retry", f"{tool} is not safe to repeat, and its attempt was {kind}"
                else:
                    reason, why = "failed-after-retries", f"{tool} failed {attempt} times; the last was {kind}"
                stop = self.record_stop(reason, self.args.park_on_failure, tool, call_no, why, text)
                with self.lock:
                    per["failed"] += 1
                if isinstance(answer, dict):
                    self.to_client(dict(answer, id=client_id))
                else:
                    self.to_client({"jsonrpc": "2.0", "id": client_id, "error": {
                        "code": NO_ANSWER_CODE,
                        "message": f"No usable answer from the Dataverse proxy to {tool} after {attempt} attempt(s).",
                        "data": {"source": "spike-0.14 mcp shim", "reason": stop["reason"], "park": stop["park"],
                                 "last": kind}}})
                self.log("final", call=call_no, tool=tool, attempts=attempt, kind=kind)
                return
            wait = self.args.backoff * (2 ** (attempt - 1))
            if kind == "throttled":
                asked = RETRY_AFTER.search(text)
                wait = min(float(asked.group(1)), self.args.max_wait) if asked else wait
            time.sleep(wait)

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

    def pass_through(self, message):
        method = message.get("method") if isinstance(message, dict) else None
        if method == "initialize":
            self.initialize = message
        elif method == "tools/list" and "id" in message:
            with self.lock:
                self.list_ids.add(message["id"])
        elif method == "notifications/cancelled":
            wanted = (message.get("params") or {}).get("requestId")
            with self.lock:
                upstream = self.in_flight.get(wanted)
            if upstream:
                self.log("cancelled", client_id=wanted, upstream_id=upstream)
                message = dict(message, params=dict(message.get("params") or {}, requestId=upstream))
        with self.lock:
            gone = self.proxy_gone
        if gone and method not in ("initialize", "notifications/cancelled"):
            self.restart_proxy(f"before {method or 'a message'}")
        if not self.to_proxy(message):
            self.log("pass-through-failed", method=method)
            if isinstance(message, dict) and method and "id" in message:
                self.to_client({"jsonrpc": "2.0", "id": message["id"],
                                "error": {"code": NO_ANSWER_CODE, "message": "The Dataverse proxy has exited."}})

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
            self.pass_through(message)
        self.log("client-closed")
        limit = (self.args.timeout * (self.args.retries + 1) + self.args.backoff * (2 ** self.args.retries)
                 + self.args.max_wait + 30)
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
            totals = {k: self.counts[k] for k in ("calls", "attempts", "refused", "retries", "late_answers",
                                                  "ids_added", "resolved_on_retry", "tool_errors_returned",
                                                  "not_retried_unsafe", "restarts")}
        self.log("end", proxy_exit_code=self.proxy.poll(), stops=len(self.stops), **totals)
        return 0


def main(argv):
    if "--" not in argv:
        print("usage: mcp_shim.py --cap N --log FILE [options] -- <proxy command>", file=sys.stderr)
        return 2
    split = argv.index("--")
    parser = argparse.ArgumentParser(prog="mcp_shim.py")
    parser.add_argument("--cap", type=int, required=True, help="MCP calls (attempts sent) allowed this session")
    parser.add_argument("--retries", type=int, default=3, help="retries after a failed attempt, where safe")
    parser.add_argument("--timeout", type=float, default=120.0, help="seconds to wait for each answer")
    parser.add_argument("--backoff", type=float, default=1.0, help="first wait before a retry, doubled each time")
    parser.add_argument("--max-wait", type=float, default=300.0, help="longest wait a throttled answer may ask for")
    parser.add_argument("--max-restarts", type=int, default=3, help="times the proxy may be started again")
    parser.add_argument("--keys-file", help="JSON {table logical name: primary key name}, read at start")
    parser.add_argument("--webapi", help="the Dataverse URL, to read a table's primary key from EntityDefinitions")
    parser.add_argument("--token-command",
                        default="az account get-access-token --resource {url} --query accessToken --output tsv",
                        help="prints a token for --webapi; {url} is replaced. Never logged")
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
