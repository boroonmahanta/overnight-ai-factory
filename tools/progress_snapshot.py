#!/usr/bin/env python3
"""A snapshot of the factory build's progress, for the progress dashboard.

Boroon asked on 9 November 2026 for a page that shows how the factory build
is going, with a button to sync it. Claude.ai has no connector to this ADO
project, so the page cannot query the board itself. This script builds the
data on the laptop instead, and a Claude Code session uploads it to the page.

It writes two JSON files of rows to --out:
- stories.json: every User Story in the ADO project getai-overnight-ai-factory
  (read with the Azure CLI, as the signed-in user), with its stage from its
  Epic, its Start and Finish dates, the date it was closed, and its track
  (laptop or documents) from docs/plans/schedule.md.
- sessions.json: time and tokens per local Claude Code session, from
  tools/session_usage.py --json.

Only counts, titles, states and dates are written. No message text is read.

Usage:
  python3 -I tools/progress_snapshot.py --out <folder>
Options: --az <path to az>, --org, --project, --schedule <schedule.md>,
--no-sessions (skip sessions.json), --transcripts <folder> (where the
Claude Code transcripts are, when the script runs from a copy of the repo at
another path, as the daily sync does).
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
SYDNEY = ZoneInfo("Australia/Sydney")
FIELDS = [
    "System.Id", "System.Title", "System.State", "System.WorkItemType",
    "System.Parent", "System.Tags", "Microsoft.VSTS.Scheduling.StartDate",
    "Microsoft.VSTS.Scheduling.FinishDate", "Microsoft.VSTS.Common.ClosedDate",
]


def ado_items(az, org, project):
    wiql = (
        "SELECT " + ",".join(f"[{f}]" for f in FIELDS) + " FROM WorkItems "
        f"WHERE [System.TeamProject] = '{project}' "
        "AND [System.WorkItemType] IN ('Epic','Feature','User Story')"
    )
    out = subprocess.run(
        [az, "boards", "query", "--org", org, "--project", project, "--wiql", wiql, "-o", "json"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        sys.exit("progress_snapshot: az boards query failed. Is the Azure CLI signed in "
                 "(az login) with the azure-devops extension?\n" + out.stderr.strip()[-500:])
    return {x["id"]: x["fields"] for x in json.loads(out.stdout)}


def local_date(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(SYDNEY).date().isoformat()


def stage_of(title):
    m = re.match(r"Stage (\d+)", title or "")
    if m:
        return f"Stage {m.group(1)}", int(m.group(1))
    return "Planning", 10


def category(state):
    if state in ("Done", "Closed"):
        return "done"
    if state == "Proposed":
        return "proposed"
    return "active"


def tracks(schedule_path):
    """ADO id to track, from the schedule's table. A story listed twice keeps both."""
    found = {}
    try:
        text = schedule_path.read_text(encoding="utf-8")
    except OSError:
        return found
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[2].isdigit():
            continue
        raw = cells[4].lower()
        if raw.startswith("documents") and "laptop" in raw:
            track = "Documents, then laptop"
        elif raw.startswith("documents"):
            track = "Documents"
        elif raw.startswith("laptop"):
            track = "Laptop"
        elif raw.startswith("boroon"):
            track = "Boroon"
        else:
            track = cells[4]
        seen = found.setdefault(int(cells[2]), [])
        if track not in seen:
            seen.append(track)
    return {k: " and ".join(v) for k, v in found.items()}


def stories(items, track_of):
    rows = []
    for wid, f in items.items():
        if f.get("System.WorkItemType") != "User Story" or f.get("System.State") == "Removed":
            continue
        feature = items.get(f.get("System.Parent")) or {}
        epic = items.get(feature.get("System.Parent")) or {}
        if epic.get("System.WorkItemType") != "Epic":
            epic = feature if feature.get("System.WorkItemType") == "Epic" else {}
        stage, order = stage_of(epic.get("System.Title"))
        tags = [t.strip() for t in (f.get("System.Tags") or "").split(";") if t.strip()]
        start = local_date(f.get("Microsoft.VSTS.Scheduling.StartDate"))
        finish = local_date(f.get("Microsoft.VSTS.Scheduling.FinishDate"))
        cat = category(f.get("System.State"))
        rows.append({
            "id": wid,
            "title": f.get("System.Title"),
            "state": f.get("System.State"),
            "category": cat,
            "stage": stage,
            "stage_order": order,
            "epic": epic.get("System.Title"),
            "feature": feature.get("System.Title"),
            "spike": "spike" in tags,
            "scheduled": bool(finish),
            "start": start,
            "finish": finish,
            "closed": local_date(f.get("Microsoft.VSTS.Common.ClosedDate")) if cat == "done" else None,
            "track": track_of.get(wid),
        })
    return sorted(rows, key=lambda r: (r["start"] or "9999", r["id"]))


def sessions(transcripts=None):
    cmd = [sys.executable, "-I", str(REPO / "tools" / "session_usage.py"), "--json"]
    if transcripts:
        cmd += ["--root", str(transcripts)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        print("progress_snapshot: no sessions written: " + out.stderr.strip()[-300:], file=sys.stderr)
        return None
    return json.loads(out.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=Path(tempfile.gettempdir()) / "factory-progress")
    ap.add_argument("--az", default=shutil.which("az") or "/opt/homebrew/bin/az")
    ap.add_argument("--org", default="https://dev.azure.com/getai")
    ap.add_argument("--project", default="getai-overnight-ai-factory")
    ap.add_argument("--schedule", type=Path, default=REPO / "docs" / "plans" / "schedule.md")
    ap.add_argument("--no-sessions", action="store_true")
    ap.add_argument("--transcripts", type=Path, default=None,
                    help="the transcript folder, when running from a copy of the repo at another path")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    taken = datetime.now(SYDNEY).replace(microsecond=0).isoformat()
    rows = stories(ado_items(a.az, a.org, a.project), tracks(a.schedule))
    for r in rows:
        r["snapshot_at"] = taken  # when the board was read, so the page can show it
    (a.out / "stories.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    msg = f"stories.json: {len(rows)} stories, {sum(r['scheduled'] for r in rows)} scheduled"
    if not a.no_sessions:
        s = sessions(a.transcripts)
        if s is not None:
            (a.out / "sessions.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
            msg += f"; sessions.json: {len(s)} sessions"
    print(f"{msg}. Written to {a.out}")


if __name__ == "__main__":
    main()
