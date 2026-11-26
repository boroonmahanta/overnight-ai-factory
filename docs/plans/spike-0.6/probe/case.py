#!/usr/bin/env python3
"""Run one Copilot CLI case for spike 0.6 (ADO 2451) and keep everything it wrote.

Each case gets a fresh COPILOT_HOME (no saved trust, agents, settings or
sessions from another case), its own log folder and its own usage file, and
runs the pinned CLI from $COPILOT_BIN. Output goes to <out>/<name>/:

  events.jsonl  stdout (JSON lines with --output-format json)
  stderr.txt    stderr
  usage.json    --usage-output-file
  logs/         --log-dir (process logs)
  home/         the case's COPILOT_HOME, left for reading
  case.json     the command line (no values from the environment), exit code,
                duration, and a summary read from the files above

Only counts, names and the last answer's first 400 characters are summarised.

  python3 -I probe/case.py --name m1 --cwd work --out out \
      [--env K=V ...] [--home-agent file.agent.md ...] [--no-json] -- -p "..." ...
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path


def read_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            rows.append({"_unparsed": line[:200]})
    return rows


def attrs_to_dict(attrs):
    """OTLP-style [{key, value:{stringValue|intValue|doubleValue|...}}] or a plain dict."""
    if isinstance(attrs, dict):
        return attrs
    out = {}
    for a in attrs or []:
        if not isinstance(a, dict) or "key" not in a:
            continue
        v = a.get("value")
        if isinstance(v, dict):
            v = next(iter(v.values()), None) if v else None
        out[a["key"]] = v
    return out


def walk(obj):
    """Yield every dict inside obj."""
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def summarise_events(rows):
    s = {"event_types": dict(Counter(r.get("type", "?") for r in rows))}
    models, tools, agents, limit_events = Counter(), [], set(), []
    last_answer = None
    for r in rows:
        t, d = r.get("type", ""), r.get("data") or {}
        if t == "session.start":
            s["selected_model"] = d.get("selectedModel")
            s["session_limits"] = d.get("sessionLimits")
            s["copilot_version"] = d.get("copilotVersion")
            for k in d:
                if "agent" in k.lower():
                    agents.add(f"session.start.{k}={json.dumps(d[k])[:120]}")
        if t == "session.auto_mode_resolved":
            s["auto_mode_resolved"] = d
        if "model" in d and isinstance(d.get("model"), str):
            models[d["model"]] += 1
        if t == "tool.execution_start":
            tools.append({"tool": d.get("toolName"), "args": json.dumps(d.get("arguments"))[:160]})
        if t == "tool.execution_complete":
            tools.append({"done": d.get("success"), "result": json.dumps(d.get("result"))[:200]})
        if t == "assistant.message" and d.get("content"):
            last_answer = d["content"]
        if "limit" in t or "credit" in t or "quota" in t:
            limit_events.append({"type": t, "data": json.dumps(d)[:300]})
        for k, v in d.items():
            if "agent" in k.lower() and t != "session.start":
                agents.add(f"{t}.{k}={json.dumps(v)[:120]}")
        if t == "result":
            s["result_exit"] = r.get("exitCode")
            s["result_usage"] = r.get("usage")
    s["models_seen"] = dict(models)
    s["tools"] = tools[:60]
    s["agent_fields"] = sorted(agents)[:40]
    s["limit_events"] = limit_events[:20]
    s["last_answer"] = (last_answer or "")[:400]
    return s


def summarise_otel(rows):
    """Read either the file exporter's lines or the sink's OTLP/HTTP JSON bodies."""
    spans, nano, resources, metrics = Counter(), defaultdict(float), [], Counter()
    span_attrs = defaultdict(set)
    for r in rows:
        body = r.get("json", r)
        for d in walk(body):
            if "resource" in d and isinstance(d["resource"], dict):
                res = attrs_to_dict(d["resource"].get("attributes"))
                if res and res not in resources:
                    resources.append(res)
            name = d.get("name")
            if isinstance(name, str) and ("spanId" in d or "span_id" in d or "traceId" in d or "kind" in d and "startTimeUnixNano" in d):
                spans[name.split(" ")[0]] += 1
                a = attrs_to_dict(d.get("attributes"))
                for k in a:
                    span_attrs[name.split(" ")[0]].add(k)
                n = a.get("github.copilot.nano_aiu")
                if n is not None:
                    try:
                        nano[name.split(" ")[0]] += float(n)
                    except (TypeError, ValueError):
                        pass
            elif isinstance(name, str) and any(k in d for k in ("sum", "histogram", "gauge", "dataPoints")):
                metrics[name] += 1
    return {
        "spans": dict(spans),
        "nano_aiu_by_span": dict(nano),
        "span_attribute_keys": {k: sorted(v)[:60] for k, v in span_attrs.items()},
        "resources": resources[:5],
        "metrics": dict(metrics),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--cwd", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--env", action="append", default=[], help="K=V for this case only")
    ap.add_argument("--home-agent", action="append", default=[], help="copy into COPILOT_HOME/agents/")
    ap.add_argument("--otel-file", action="store_true", help="file exporter into <case>/otel.jsonl")
    ap.add_argument("--sink", help="the OTLP sink's file: keep what it got during this case")
    ap.add_argument("--no-json", action="store_true")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("rest", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    args = a.rest[1:] if a.rest[:1] == ["--"] else a.rest

    out = Path(a.out).resolve() / a.name
    if out.exists():
        shutil.rmtree(out)
    (out / "logs").mkdir(parents=True)
    home = out / "home"
    home.mkdir()
    for f in a.home_agent:
        (home / "agents").mkdir(exist_ok=True)
        shutil.copy(f, home / "agents" / Path(f).name)

    env = dict(os.environ)
    env["COPILOT_HOME"] = str(home)
    env["COPILOT_AUTO_UPDATE"] = "false"
    for kv in a.env:
        k, _, v = kv.partition("=")
        env[k] = v.replace("{case}", str(out))
    if a.otel_file:
        env["COPILOT_OTEL_FILE_EXPORTER_PATH"] = str(out / "otel.jsonl")

    cmd = [os.environ["COPILOT_BIN"], *args, "--usage-output-file", str(out / "usage.json"),
           "--log-dir", str(out / "logs"), "--no-auto-update"]
    if not a.no_json:
        cmd += ["--output-format", "json"]
    sink = Path(a.sink) if a.sink else None
    sink_start = sink.stat().st_size if sink and sink.exists() else 0
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=a.cwd, env=env, capture_output=True, text=True, timeout=a.timeout)
        code, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, so, se = "timeout", e.stdout or "", e.stderr or ""
        so = so.decode() if isinstance(so, bytes) else so
        se = se.decode() if isinstance(se, bytes) else se
    dur = round(time.time() - t0, 1)
    (out / "events.jsonl").write_text(so, encoding="utf-8")
    (out / "stderr.txt").write_text(se, encoding="utf-8")

    summary = {"name": a.name, "cwd": a.cwd, "args": args,
               "env_keys": sorted(kv.partition("=")[0] for kv in a.env),
               "exit": code, "seconds": dur}
    summary["events"] = summarise_events(read_jsonl(out / "events.jsonl")) if not a.no_json else {}
    summary["stdout_head"] = so[:600] if a.no_json or not summary["events"].get("event_types") else ""
    summary["stderr_head"] = se[:1200]
    up = out / "usage.json"
    if up.exists():
        try:
            u = json.loads(up.read_text())
            summary["usage"] = {k: u[k] for k in u if k in (
                "totalNanoAiu", "totalPremiumRequestCost", "modelMetrics", "agentMetrics")}
        except ValueError:
            summary["usage"] = "unreadable"
    if (out / "otel.jsonl").exists():
        summary["otel_file"] = summarise_otel(read_jsonl(out / "otel.jsonl"))
    if sink:
        time.sleep(3)  # let a last export land
        got = b""
        if sink.exists():
            with sink.open("rb") as f:
                f.seek(sink_start)
                got = f.read()
        (out / "sink.jsonl").write_bytes(got)
        rows = read_jsonl(out / "sink.jsonl")
        summary["otel_sink"] = {"posts": dict(Counter(r.get("path") for r in rows)),
                                "content_types": dict(Counter(r.get("content_type") for r in rows)),
                                **summarise_otel(rows)}
    (out / "case.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    ev = summary["events"]
    print(f"case {a.name}: exit {code}, {dur}s, model {ev.get('selected_model')} "
          f"seen {ev.get('models_seen')}, nano {summary.get('usage', {}).get('totalNanoAiu') if isinstance(summary.get('usage'), dict) else None}")
    print("  answer:", (ev.get("last_answer") or summary["stdout_head"] or "")[:200].replace("\n", " | "))
    if se.strip():
        print("  stderr:", se.strip()[:300].replace("\n", " | "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
