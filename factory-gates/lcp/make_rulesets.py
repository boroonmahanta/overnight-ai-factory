#!/usr/bin/env python3
"""Generate the protected-paths push ruleset and check CODEOWNERS against it.

One source for protected paths: PROTECTED_PATHS in check_protected_paths.py
(plan section 5.7, part 3). This script turns it into
rulesets/protected-paths.json, in GitHub's REST ruleset format, so the push
ruleset and the `locks` job can never disagree. A test fails if the committed
JSON is stale, the same way the manifest test works.

It also checks templates/CODEOWNERS: every protected path must be owned by
@<org>/acceptance-owners or @<org>/platform-team, the two teams allowed in the
push ruleset's bypass list (plan 5.7). A protected path nobody owns, or one
owned by another team, is a problem.

  make_rulesets.py make  <root>   # writes rulesets/protected-paths.json
  make_rulesets.py check <root>   # fails if the JSON is stale or CODEOWNERS is short

The other three rulesets (main-gate, integration-gate, factory-required-
workflows) are written by hand; they carry no path list. Team and repository
IDs are 0 until the real organisation exists on GHE.com. The API rejects id 0,
so a file applied before the IDs are filled in fails loudly.

Nothing here applies anything. Applying needs the real organisation.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_protected_paths import PROTECTED_PATHS, glob_to_regex  # noqa: E402

RULESET_FILE = "rulesets/protected-paths.json"
CODEOWNERS_FILE = "templates/CODEOWNERS"
ORG = "getai"
# The only two teams the push ruleset lets through (plan 5.7). Team IDs are
# filled in at apply time, by a reviewed PR, then the JSON is regenerated.
BYPASS_TEAMS = [("acceptance-owners", 0), ("platform-team", 0)]
PROTECTED_OWNERS = {f"@{ORG}/{team}" for team, _ in BYPASS_TEAMS}


def protected_paths_ruleset() -> dict:
    return {
        "name": "protected-paths",
        "target": "push",
        "enforcement": "active",
        "bypass_actors": [
            {"actor_id": team_id, "actor_type": "Team", "bypass_mode": "always"}
            for _, team_id in BYPASS_TEAMS
        ],
        "conditions": {
            "repository_property": {
                "include": [{"name": "factory", "property_values": ["enabled"], "source": "custom"}],
                "exclude": [],
            }
        },
        "rules": [
            {"type": "file_path_restriction", "parameters": {"restricted_file_paths": list(PROTECTED_PATHS)}},
        ],
    }


def render(ruleset: dict) -> str:
    return json.dumps(ruleset, indent=2) + "\n"


# --- CODEOWNERS -------------------------------------------------------------
# GitHub's CODEOWNERS rules: a pattern with a slash anywhere but the end is
# anchored to the repo root; one without matches at any depth. A trailing slash
# means the folder and everything in it. `*` stays within one folder, `**`
# crosses folders. A pattern ending in `*` does not reach into subfolders
# ("docs/*"). The last matching line wins.


def codeowners_regex(pattern: str) -> re.Pattern:
    dir_only = pattern.endswith("/")
    anchored = "/" in pattern.rstrip("/")
    body = pattern.strip("/")
    inner = glob_to_regex(body)[1:-1]  # drop the ^ and $
    if dir_only:
        inner += "/.*"
    elif not body.endswith("*"):
        inner += "(/.*)?"
    prefix = "^" if anchored else "^(.*/)?"
    return re.compile(f"{prefix}{inner}$")


def parse_codeowners(text: str) -> list[tuple[str, list[str]]]:
    rules = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        pattern, *owners = line.split()
        rules.append((pattern, owners))
    return rules


def owners_of(path: str, rules: list[tuple[str, list[str]]]) -> list[str]:
    found: list[str] = []
    for pattern, owners in rules:
        if codeowners_regex(pattern).match(path):
            found = owners
    return found


def sample_paths(glob: str) -> list[str]:
    """Concrete paths a protected glob covers: a file, and a file one folder deeper."""
    shallow = glob.replace("**", "sample.txt").replace("*", "x")
    deep = glob.replace("**", "sub/sample.txt").replace("*", "x")
    return [shallow] if shallow == deep else [shallow, deep]


def check_codeowners(text: str, protected: list[str] = PROTECTED_PATHS, allowed=PROTECTED_OWNERS) -> list[str]:
    rules = parse_codeowners(text)
    problems = []
    for glob in protected:
        for path in sample_paths(glob):
            owners = owners_of(path, rules)
            if not set(owners) & allowed:
                held = " ".join(owners) if owners else "no owner"
                problems.append(
                    f"protected path {glob} ({path}) is not owned by {' or '.join(sorted(allowed))} "
                    f"in CODEOWNERS: {held}"
                )
    return problems


# --- make and check ---------------------------------------------------------


def make(root: Path) -> None:
    path = root / RULESET_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(protected_paths_ruleset()), encoding="utf-8")


def check(root: Path) -> list[str]:
    problems = []
    ruleset = root / RULESET_FILE
    if not ruleset.is_file():
        problems.append(f"missing: {RULESET_FILE} (run make_rulesets.py make)")
    elif ruleset.read_text(encoding="utf-8") != render(protected_paths_ruleset()):
        problems.append(f"stale: {RULESET_FILE} does not match check_protected_paths.py (run make_rulesets.py make)")
    codeowners = root / CODEOWNERS_FILE
    if not codeowners.is_file():
        problems.append(f"missing: {CODEOWNERS_FILE}")
    else:
        problems.extend(check_codeowners(codeowners.read_text(encoding="utf-8")))
    return problems


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "make":
        make(Path(argv[2]))
        return 0
    if len(argv) == 3 and argv[1] == "check":
        problems = check(Path(argv[2]))
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1 if problems else 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
