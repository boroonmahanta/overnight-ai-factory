#!/usr/bin/env python3
"""Map a pull request branch to a lane and a story.

Agent branches are agent/<lane>/<ado-id>-<attempt>, for example agent/fl2/48213-1.
Anything else (human PR, release PR, merge queue) maps to lane "none".
An agent branch naming a lane that is not in the allowed list fails.

This replaces the inline bash in the `map` job of lcp-gate.yml (plan Appendix A)
so the rule can be tested. It runs in a job with no credentials.

Environment (as set by the workflow):
  HEAD_REF       the PR head branch, or the merge group head ref
  ALLOWED        space-separated lane codes, from vars.LCP_LANES, e.g. "fl1 fl2 fl3"
  GITHUB_OUTPUT  file to append lane= and story= lines to
"""
import os
import re
import sys

AGENT_BRANCH = re.compile(r"^agent/(fl[0-9]+)/([0-9]+)-([0-9]+)$")


class LaneError(Exception):
    pass


def map_branch(head_ref: str, allowed: str) -> tuple[str, str]:
    """Return (lane, story). Raise LaneError for an agent branch on an unknown lane."""
    match = AGENT_BRANCH.fullmatch(head_ref)
    if not match:
        return "none", "none"
    lane, story = match.group(1), match.group(2)
    if lane not in allowed.split():
        raise LaneError(f"Unknown lane: {lane}")
    return lane, story


def main() -> int:
    head_ref = os.environ.get("HEAD_REF", "")
    allowed = os.environ.get("ALLOWED", "")
    try:
        lane, story = map_branch(head_ref, allowed)
    except LaneError as err:
        print(err, file=sys.stderr)
        return 1
    out = os.environ.get("GITHUB_OUTPUT")
    line = f"lane={lane}\nstory={story}\n"
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(line)
    else:
        sys.stdout.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
