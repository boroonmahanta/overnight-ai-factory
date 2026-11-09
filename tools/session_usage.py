#!/usr/bin/env python3
"""Time and tokens per Claude Code session, from the local transcripts.

Boroon asked on 7 November 2026 for each story's time and tokens in its ADO
body (project getai-overnight-ai-factory). This totals them from the
transcripts Claude Code keeps on this laptop. Cloud sessions are not there.

How it counts:
- Every *.jsonl under the project's transcript folder, subagents included.
  Forked sessions copy their parent's messages, so entries are de-duplicated
  by uuid, and model responses by message id, before counting. Entries are
  grouped by their own sessionId, so a fork's copied history stays with the
  session it came from.
- Active time: the sum of gaps between consecutive entries, with any gap over
  --idle-cap minutes (default 10) counted as zero. A single tool call that
  ran longer than that is counted as idle too.
- Tokens: from each response's usage block: input, cache write, cache read
  and output. "Processed" is all four added up; cache reads dominate it.

Only counts are printed. No message text is read out.

Usage:
  python3 -I tools/session_usage.py                 # every session, oldest first
  python3 -I tools/session_usage.py --latest        # the most recent session only
  python3 -I tools/session_usage.py --session ee02cc9a 45b27b0d
                                                    # these sessions, plus one line
                                                    # for their total, ready for ADO
  python3 -I tools/session_usage.py --json          # every session as JSON rows, for
                                                    # tools/progress_snapshot.py
Options: --root <transcript folder>, --idle-cap <minutes>, --utc-offset <hours>
(default 11, Sydney daylight time).
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


def default_root():
    here = str(Path(__file__).resolve().parent.parent)
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9-]", "-", here)


def collect(root, idle_cap):
    seen_uuid, seen_msg = set(), set()
    stamps = defaultdict(list)
    tokens = defaultdict(Counter)
    branches = defaultdict(Counter)
    for path in sorted(root.rglob("*.jsonl")):
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                sid = e.get("sessionId")
                if not sid:
                    continue
                uid, ts = e.get("uuid"), e.get("timestamp")
                if uid and ts and uid not in seen_uuid:
                    seen_uuid.add(uid)
                    stamps[sid].append(datetime.fromisoformat(ts.replace("Z", "+00:00")))
                    branches[sid][e.get("gitBranch") or "-"] += 1
                msg = e.get("message")
                if e.get("type") != "assistant" or not isinstance(msg, dict) or not msg.get("usage"):
                    continue
                mid = msg.get("id")
                if not mid or mid in seen_msg:
                    continue
                seen_msg.add(mid)
                u = msg["usage"]
                t = tokens[sid]
                t["input"] += u.get("input_tokens") or 0
                t["cache_write"] += u.get("cache_creation_input_tokens") or 0
                t["cache_read"] += u.get("cache_read_input_tokens") or 0
                t["output"] += u.get("output_tokens") or 0
    rows = []
    for sid, ts in stamps.items():
        ts.sort()
        active = sum(g for g in ((b - a).total_seconds() / 60 for a, b in zip(ts, ts[1:])) if g <= idle_cap)
        t = tokens[sid]
        rows.append({
            "session": sid, "first": ts[0], "last": ts[-1], "active_min": round(active),
            "output": t["output"], "cache_read": t["cache_read"],
            "processed": t["input"] + t["cache_write"] + t["cache_read"] + t["output"],
            "branch": branches[sid].most_common(1)[0][0],
        })
    return sorted(rows, key=lambda r: r["first"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=default_root())
    ap.add_argument("--session", nargs="+", default=[], help="session ID prefixes")
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--idle-cap", type=float, default=10)
    ap.add_argument("--utc-offset", type=float, default=11)
    ap.add_argument("--json", action="store_true", help="print every session as JSON rows")
    a = ap.parse_args()
    if not a.root.is_dir():
        sys.exit(f"session_usage: no transcript folder at {a.root}")
    rows = collect(a.root, a.idle_cap)
    if a.json:
        print(json.dumps([{
            "session": r["session"][:8], "first": r["first"].isoformat(), "last": r["last"].isoformat(),
            "active_min": r["active_min"], "output": r["output"], "cache_read": r["cache_read"],
            "processed": r["processed"], "branch": r["branch"],
        } for r in rows], indent=1))
        return
    if a.latest:
        rows = [max(rows, key=lambda r: r["last"])]
    elif a.session:
        rows = [r for r in rows if any(r["session"].startswith(p) for p in a.session)]
    if not rows:
        sys.exit("session_usage: no matching sessions")
    off = timedelta(hours=a.utc_offset)
    for r in rows:
        print(f"{r['session'][:8]}  {r['first'] + off:%d %b %H:%M} to {r['last'] + off:%d %b %H:%M}  "
              f"active {r['active_min']:4} min  output {r['output']:>9,}  processed {r['processed']:>12,}  {r['branch']}")
    if a.session or a.latest:
        active = sum(r["active_min"] for r in rows)
        h, m = divmod(active, 60)
        print()
        print(f"Time and tokens, whole session: active time {h} h {m:02d} min (gaps over "
              f"{a.idle_cap:g} minutes not counted), from {min(r['first'] for r in rows) + off:%d %b %H:%M} "
              f"to {max(r['last'] for r in rows) + off:%d %b %H:%M} (UTC{a.utc_offset:+g}). "
              f"Tokens: {sum(r['output'] for r in rows):,} output; "
              f"{sum(r['processed'] for r in rows):,} processed in all, of which "
              f"{sum(r['cache_read'] for r in rows):,} were cache reads. "
              f"From {len(rows)} local transcript(s).")


if __name__ == "__main__":
    main()
