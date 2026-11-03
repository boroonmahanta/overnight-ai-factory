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

# The one list of protected paths (plan section 5.7, part 3), in the fnmatch
# form the push ruleset uses. make_rulesets.py generates
# rulesets/protected-paths.json from it, and a test fails if that file or
# templates/CODEOWNERS falls behind. A change here is a gate-script change:
# reviewed PR only.
PROTECTED_PATHS = [
    "tests/acceptance/**",
    "tests/scenarios/**",
    "specs/*/spec.md",
    "specs/*/checklists/**",
    "glossary.md",
    "docs/adr/**",
    "coding-standards.md",
    ".specify/**",
    ".github/**",
    "AGENTS.md",
    "CLAUDE.md",
    ".claude/**",
    ".mcp/**",
    "scripts/**",
    "builders/lib/**",
    "deploy/**",
]


def glob_to_regex(pattern: str) -> str:
    """`**` matches across folders, `*` within one. Anchored to the repo root."""
    out = ""
    i = 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
        elif pattern[i] == "*":
            out += "[^/]*"
            i += 1
        else:
            out += re.escape(pattern[i])
            i += 1
    return f"^{out}$"


PROTECTED = re.compile("|".join(glob_to_regex(p) for p in PROTECTED_PATHS))


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
