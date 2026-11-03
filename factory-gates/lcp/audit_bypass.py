#!/usr/bin/env python3
"""Fail if a ruleset's bypass list names anything but a team (rule 6).

The offline half of the plan's nightly bypass audit (plan 5.7, part 3): "a
nightly audit fails the kickoff if any App, machine account, the write role or
Copilot appears in a bypass list". GitHub's own docs suggest adding Copilot as a
bypass actor when a ruleset blocks it. That is the trap this script is for.

Reads ruleset JSON in GitHub's REST format. Bypass actors there are typed:
Team, Integration (a GitHub App, which is what Copilot is), RepositoryRole,
OrganizationAdmin or DeployKey. Only Team is allowed, and only in rulesets
other than main-gate, whose bypass list must be empty (plan 5.7).

What this cannot see offline: a machine account inside an allowed team. The
online half of the audit lists the members of each bypass team and checks them
against the identity register. That half waits for the real organisation.

  audit_bypass.py <ruleset.json> [<ruleset.json> ...]
"""
import json
import sys
from pathlib import Path

ALLOWED_ACTOR_TYPES = {"Team"}
MUST_BE_EMPTY = {"main-gate"}
# Repository role IDs as the rulesets UI exports them on github.com. Confirm on
# GHE.com. The audit fails on every role whatever its ID; the name is for the message.
ROLE_NAMES = {1: "read", 2: "maintain", 3: "triage", 4: "write", 5: "admin"}


def audit(ruleset: dict) -> list[str]:
    name = ruleset.get("name", "<unnamed>")
    actors = ruleset.get("bypass_actors") or []
    problems = []
    if name in MUST_BE_EMPTY and actors:
        problems.append(f"{name}: the bypass list must be empty, it has {len(actors)} entries")
    for actor in actors:
        kind = actor.get("actor_type")
        actor_id = actor.get("actor_id")
        if kind == "Team":
            continue
        if kind == "Integration":
            what = f"a GitHub App or integration (app id {actor_id}; Copilot is one)"
        elif kind == "DeployKey":
            what = "a deploy key, a machine credential"
        elif kind == "RepositoryRole":
            role = ROLE_NAMES.get(actor_id, "unknown")
            what = f"the repository role {role} (id {actor_id})"
        elif kind == "OrganizationAdmin":
            what = "the organisation admin role"
        else:
            what = f"an unknown actor type {kind!r}"
        problems.append(f"{name}: {what} is in the bypass list. Only named teams may bypass (rule 6)")
    return problems


def audit_file(path: Path) -> list[str]:
    try:
        ruleset = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"{path}: cannot read ruleset: {exc}"]
    if not isinstance(ruleset, dict):
        return [f"{path}: not a ruleset object"]
    return audit(ruleset)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    problems = []
    for arg in argv[1:]:
        problems.extend(audit_file(Path(arg)))
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
