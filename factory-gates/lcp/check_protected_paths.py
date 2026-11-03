#!/usr/bin/env python3
"""Fail an agent pull request that changes a protected path.

This is the second lock behind the push ruleset (plan section 5.x, Appendix A,
job `locks`). Agents never change tests, locked scenarios, specs, standards, the
glossary, decision records, hooks, workflows, skills, agent instructions, scripts
or deploy settings (rule 17). Humans change them by reviewed daytime PR.

Renames are listed as a delete plus an add (--no-renames). Without that, moving
a protected file out of a protected folder would show only the new path and
slip through.

Usage:
  check_protected_paths.py --lane <lane> --base <sha>   # reads git diff BASE...HEAD
  check_protected_paths.py --lane none ...              # human PR: nothing to check
"""
import argparse
import re
import subprocess
import sys

# One list. Keep it in step with the push ruleset path restrictions
# (plan section 5.x). A change here is a gate-script change: reviewed PR only.
PROTECTED = re.compile(
    r"^("
    r"tests/acceptance/|tests/scenarios/"
    r"|specs/[^/]+/spec\.md|specs/[^/]+/checklists/"
    r"|glossary\.md|docs/adr/|coding-standards\.md"
    r"|\.specify/|\.github/|\.claude/|\.mcp/"
    r"|AGENTS\.md|CLAUDE\.md"
    r"|scripts/|builders/lib/|deploy/"
    r")"
)


def find_protected(paths: list[str]) -> list[str]:
    return sorted({p for p in paths if PROTECTED.match(p)})


def changed_paths(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "--no-renames", "-z", f"{base}...HEAD"],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8", errors="surrogateescape")
    return [p for p in out.split("\0") if p]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True)
    parser.add_argument("--base", required=True)
    args = parser.parse_args(argv)
    if args.lane == "none":
        return 0
    hits = find_protected(changed_paths(args.base))
    if hits:
        print("An agent PR changed a protected path. Failing.", file=sys.stderr)
        for path in hits:
            print(f"  {path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
