#!/usr/bin/env python3
"""Generate the four rulesets from one config, and check CODEOWNERS against them.

One source for protected paths: PROTECTED_PATHS in check_protected_paths.py
(plan section 5.7, part 3). One source for names and IDs: rulesets/org.json
(the org, the gate repo, team IDs, App IDs). This script turns both into the
four files in rulesets/, in GitHub's REST ruleset format, so the push ruleset
and the `locks` job can never disagree, and an ID is typed once. A test fails
if any committed ruleset is stale, the same way the manifest test works.

It also checks templates/CODEOWNERS: every protected path must be owned by
@<org>/acceptance-owners or @<org>/platform-team, the two teams allowed in the
push ruleset's bypass list (plan 5.7). A protected path nobody owns, or one
owned by another team, is a problem.

  make_rulesets.py make  <root>   # writes rulesets/*.json from org.json
  make_rulesets.py check <root>   # fails if a ruleset is stale or CODEOWNERS is short

IDs in org.json are 0 until apply_rulesets.py resolve fills them from the real
organisation. The API rejects id 0, so a file applied before that fails loudly.
Nothing here applies anything; apply_rulesets.py does, and only with --yes.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_protected_paths import PROTECTED_PATHS, glob_to_regex  # noqa: E402

RULESETS_DIR = "rulesets"
ORG_FILE = "rulesets/org.json"
CODEOWNERS_FILE = "templates/CODEOWNERS"
RULESET_NAMES = ["main-gate", "integration-gate", "protected-paths", "factory-required-workflows"]
# The only two teams the push ruleset lets through (plan 5.7).
BYPASS_TEAMS = ["acceptance-owners", "platform-team"]
GATE_WORKFLOW = ".github/workflows/lcp-gate.yml"

FACTORY_REPOS = {
    "repository_property": {
        "include": [{"name": "factory", "property_values": ["enabled"], "source": "custom"}],
        "exclude": [],
    }
}
MERGE_QUEUE = {
    "type": "merge_queue",
    "parameters": {
        "check_response_timeout_minutes": 60,
        "grouping_strategy": "ALLGREEN",
        "max_entries_to_build": 5,
        "max_entries_to_merge": 5,
        "merge_method": "SQUASH",
        "min_entries_to_merge": 1,
        "min_entries_to_merge_wait_minutes": 5,
    },
}


def load_org(root: Path) -> dict:
    return json.loads((root / ORG_FILE).read_text(encoding="utf-8"))


def protected_owners(org: dict) -> set[str]:
    return {f"@{org['org']}/{team}" for team in BYPASS_TEAMS}


def status_checks(*checks: tuple[str, int]) -> dict:
    return {
        "type": "required_status_checks",
        "parameters": {
            "strict_required_status_checks_policy": True,
            "do_not_enforce_on_create": False,
            "required_status_checks": [{"context": context, "integration_id": app_id} for context, app_id in checks],
        },
    }


def branch_ruleset(name: str, branches: list[str], rules: list[dict], enforcement: str = "active") -> dict:
    return {
        "name": name,
        "target": "branch",
        "enforcement": enforcement,
        "bypass_actors": [],
        "conditions": {**FACTORY_REPOS, "ref_name": {"include": branches, "exclude": []}},
        "rules": rules,
    }


def main_gate(org: dict) -> dict:
    return branch_ruleset("main-gate", ["refs/heads/main"], [
        {"type": "deletion"},
        {"type": "non_fast_forward"},
        {"type": "required_linear_history"},
        {"type": "pull_request", "parameters": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews_on_push": True,
            "require_code_owner_review": True,
            "require_last_push_approval": True,
            "required_review_thread_resolution": True,
        }},
        status_checks(("lcp-gate", org["apps"]["github-actions"])),
        MERGE_QUEUE,
    ])


def integration_gate(org: dict) -> dict:
    # Force pushes stay allowed: V2.1 resets `integration` each evening without a bypass entry.
    # The `lane/drift` check is left out for stage 1 (Boroon, 3 November 2026): the App that
    # posts it is built in stage 3. Add it then, with a passing tick for human PRs (plan gap,
    # see docs/progress.md). Setting apps.lane-drift in org.json to a non-zero ID adds it.
    checks = [("lcp-gate", org["apps"]["github-actions"])]
    if org["apps"].get("lane-drift"):
        checks.append(("lane/drift", org["apps"]["lane-drift"]))
    return branch_ruleset("integration-gate", ["refs/heads/integration"], [
        {"type": "deletion"},
        {"type": "pull_request", "parameters": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews_on_push": True,
            "require_code_owner_review": True,
            "require_last_push_approval": False,
            "required_review_thread_resolution": True,
        }},
        status_checks(*checks),
        MERGE_QUEUE,
    ])


def protected_paths(org: dict) -> dict:
    return {
        "name": "protected-paths",
        "target": "push",
        "enforcement": "active",
        "bypass_actors": [
            {"actor_id": org["teams"][team], "actor_type": "Team", "bypass_mode": "always"}
            for team in BYPASS_TEAMS
        ],
        "conditions": FACTORY_REPOS,
        "rules": [
            {"type": "file_path_restriction", "parameters": {"restricted_file_paths": list(PROTECTED_PATHS)}},
        ],
    }


def required_workflows(org: dict) -> dict:
    # Stage 1 starts in Evaluate mode (plan 11.2); org.json switches it to active.
    return branch_ruleset(
        "factory-required-workflows", ["refs/heads/main", "refs/heads/integration"],
        [{"type": "workflows", "parameters": {
            "do_not_enforce_on_create": False,
            "workflows": [{
                "path": GATE_WORKFLOW,
                "ref": org["gate_workflow_ref"],
                "repository_id": org["gate_repository_id"],
            }],
        }}],
        enforcement=org["required_workflows_enforcement"],
    )


BUILDERS = {
    "main-gate": main_gate,
    "integration-gate": integration_gate,
    "protected-paths": protected_paths,
    "factory-required-workflows": required_workflows,
}


def rulesets(org: dict) -> dict[str, dict]:
    return {name: BUILDERS[name](org) for name in RULESET_NAMES}


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


def check_codeowners(text: str, allowed: set[str], protected: list[str] = PROTECTED_PATHS) -> list[str]:
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
    org = load_org(root)
    (root / RULESETS_DIR).mkdir(parents=True, exist_ok=True)
    for name, ruleset in rulesets(org).items():
        (root / RULESETS_DIR / f"{name}.json").write_text(render(ruleset), encoding="utf-8")


def check(root: Path) -> list[str]:
    problems = []
    org = load_org(root)
    for name, ruleset in rulesets(org).items():
        rel = f"{RULESETS_DIR}/{name}.json"
        path = root / rel
        if not path.is_file():
            problems.append(f"missing: {rel} (run make_rulesets.py make)")
        elif path.read_text(encoding="utf-8") != render(ruleset):
            problems.append(f"stale: {rel} does not match org.json and check_protected_paths.py (run make_rulesets.py make)")
    codeowners = root / CODEOWNERS_FILE
    if not codeowners.is_file():
        problems.append(f"missing: {CODEOWNERS_FILE}")
    else:
        problems.extend(check_codeowners(codeowners.read_text(encoding="utf-8"), protected_owners(org)))
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
