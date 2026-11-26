#!/usr/bin/env python3
"""Time and tokens per story from OpenTelemetry, every engine, in one place (spike 0.20, ADO 2738).

A probe, not a ledger loader. It reads OTLP/HTTP JSON as `docs/plans/spike-0.6/probe/otlp_sink.py`
stores it (one POST per line: {"path", "content_type", "json"}) and Copilot CLI's file exporter
lines ({"type": "span" | "metric", ...}), from any number of files: the laptop's collector and
the night runner's, merged. It totals model calls and tokens per story, engine and session.

Where the story comes from, in order:
  1. `story_id` in the resource attributes (OTEL_RESOURCE_ATTRIBUTES), or on the data point;
  2. for Claude Code, the session's git branch in its local transcript (--transcripts), with the
     ADO ID taken from the branch name (the first run of 4 to 6 digits, as in
     claude/session-55-2738-time-tokens): the desktop app drops OTEL_RESOURCE_ATTRIBUTES;
  3. otherwise "unattributed".

Counting, so the engines add up the same way:
  - Copilot (CLI, SDK, VS Code): one model call per `chat` span; its gen_ai.usage.input_tokens
    includes cache reads and writes, so uncached input = input - cache_read - cache_write.
    AI credits from github.copilot.nano_aiu on the root invoke_agent span only (it is the sum
    of its chat spans; never add both).
  - Claude Code: one model call per claude_code.api_request event; input_tokens excludes the
    cache. Cost is the engine's own estimate (cost_usd), not a price.
  - "processed" = uncached input + cache read + cache write + output, as tools/session_usage.py
    counts it.

Only counts and names are printed: no prompt text, and no user.email or account IDs.

  python3 -I story_report.py store.jsonl [more.jsonl ...] [--transcripts ~/.claude/projects]
         [--json out.json]
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ADO_ID = re.compile(r"(?<![0-9])([0-9]{4,6})(?![0-9])")


def val(v):
    if isinstance(v, dict) and v:
        return next(iter(v.values()))
    return v


def attrs(a):
    if isinstance(a, dict):
        return a
    return {x["key"]: val(x.get("value")) for x in (a or []) if isinstance(x, dict) and "key" in x}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def branch_map(roots):
    """session.id -> the branch most of its transcript entries carry."""
    out = {}
    for root in roots:
        for p in Path(root).expanduser().rglob("*.jsonl"):
            counts = defaultdict(int)
            sid = None
            try:
                with p.open(encoding="utf-8") as f:
                    for line in f:
                        try:
                            e = json.loads(line)
                        except ValueError:
                            continue
                        sid = sid or e.get("sessionId")
                        b = e.get("gitBranch")
                        if b:
                            counts[b] += 1
            except OSError:
                continue
            if sid and counts and sid not in out:
                out[sid] = max(counts, key=counts.get)
    return out


def story_from_branch(branch):
    m = ADO_ID.search(branch or "")
    return m.group(1) if m else None


class Totals:
    def __init__(self):
        self.calls = 0
        self.input = 0.0
        self.cache_read = 0.0
        self.cache_write = 0.0
        self.output = 0.0
        self.credits = 0.0
        self.cost_usd = 0.0
        self.models = defaultdict(int)

    def processed(self):
        return self.input + self.cache_read + self.cache_write + self.output

    def as_dict(self):
        return {"model_calls": self.calls, "input_uncached": int(self.input), "cache_read": int(self.cache_read),
                "cache_write": int(self.cache_write), "output": int(self.output),
                "processed": int(self.processed()), "copilot_ai_credits": round(self.credits, 6),
                "claude_cost_usd_estimate": round(self.cost_usd, 6), "models": dict(self.models)}


def lines(paths):
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        yield json.loads(line)
                    except ValueError:
                        continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--transcripts", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    branches = branch_map(a.transcripts)
    # (story, engine, session) -> Totals
    t = defaultdict(Totals)

    def key(res, dp, session):
        story = dp.get("story_id") or res.get("story_id")
        how = "attribute"
        if not story and session in branches:
            story, how = story_from_branch(branches[session]), "branch"
        engine = res.get("service.name", "?")
        ep = dp.get("app.entrypoint") or res.get("app.entrypoint")
        if ep:
            engine += f" ({ep})"
        return (story or "unattributed", how if story else "-", engine, session or "?")

    for r in lines(a.files):
        if r.get("type") == "span":  # Copilot's file exporter
            bodies = [{"resourceSpans": [{"resource": r.get("resource", {}),
                                          "scopeSpans": [{"spans": [r]}]}]}]
        elif r.get("type") == "metric":
            continue
        else:
            bodies = [r.get("json") or {}]
        for b in bodies:
            for rs in b.get("resourceSpans", []):
                res = attrs((rs.get("resource") or {}).get("attributes"))
                for ss in rs.get("scopeSpans", []):
                    for sp in ss.get("spans", []):
                        sa = attrs(sp.get("attributes"))
                        name = sp.get("name", "")
                        sess = sa.get("gen_ai.conversation.id")
                        if name.startswith("chat"):
                            k = t[key(res, sa, sess)]
                            k.calls += 1
                            cr = num(sa.get("gen_ai.usage.cache_read.input_tokens"))
                            cw = num(sa.get("gen_ai.usage.cache_write.input_tokens"))
                            k.cache_read += cr
                            k.cache_write += cw
                            k.input += max(num(sa.get("gen_ai.usage.input_tokens")) - cr - cw, 0)
                            k.output += num(sa.get("gen_ai.usage.output_tokens"))
                            k.models[sa.get("gen_ai.request.model") or name[5:]] += 1
                        elif name.startswith("invoke_agent") and not sp.get("parentSpanId"):
                            t[key(res, sa, sess)].credits += num(sa.get("github.copilot.nano_aiu")) / 1e9
            for rl in b.get("resourceLogs", []):
                res = attrs((rl.get("resource") or {}).get("attributes"))
                for sl in rl.get("scopeLogs", []):
                    for lr in sl.get("logRecords", []):
                        la = attrs(lr.get("attributes"))
                        if la.get("event.name") != "api_request":
                            continue
                        k = t[key(res, la, la.get("session.id"))]
                        k.calls += 1
                        k.input += num(la.get("input_tokens"))
                        k.cache_read += num(la.get("cache_read_tokens"))
                        k.cache_write += num(la.get("cache_creation_tokens"))
                        k.output += num(la.get("output_tokens"))
                        k.cost_usd += num(la.get("cost_usd"))
                        k.models[la.get("model")] += 1

    rows = [{"story": s, "story_from": how, "engine": e, "session": sid, **v.as_dict()}
            for (s, how, e, sid), v in sorted(t.items())]
    by_story = defaultdict(Totals)
    for (s, _, _, _), v in t.items():
        agg = by_story[s]
        for f in ("calls", "input", "cache_read", "cache_write", "output", "credits", "cost_usd"):
            setattr(agg, f, getattr(agg, f) + getattr(v, f))
    print(f"{'story':<13} {'from':<9} {'engine':<38} {'session':<10} {'calls':>5} {'processed':>11} {'output':>7} {'credits':>8} {'usd est':>8}")
    for r in rows:
        print(f"{r['story']:<13} {r['story_from']:<9} {r['engine'][:38]:<38} {r['session'][:8]:<10} {r['model_calls']:>5} "
              f"{r['processed']:>11,} {r['output']:>7,} {r['copilot_ai_credits']:>8.3f} {r['claude_cost_usd_estimate']:>8.4f}")
    print()
    for s, v in sorted(by_story.items()):
        d = v.as_dict()
        print(f"story {s}: {d['model_calls']} model calls, {d['processed']:,} tokens processed "
              f"({d['output']:,} output), {d['copilot_ai_credits']:.3f} Copilot AI credits, "
              f"USD {d['claude_cost_usd_estimate']:.4f} Claude Code estimate")
    if a.json:
        Path(a.json).write_text(json.dumps({"rows": rows}, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
