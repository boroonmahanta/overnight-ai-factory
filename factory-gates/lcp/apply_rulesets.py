#!/usr/bin/env python3
"""Look up IDs, show what applying the rulesets would change, apply them, audit them.

Runs by a human, by day, against the real organisation (plan 5.7 part 3;
stage 1 "the four rulesets and CODEOWNERS"). Standard library only. The token
comes from the GH_TOKEN or GITHUB_TOKEN environment variable and is never
written anywhere. It needs organisation admin, because rulesets and custom
properties are organisation settings.

  apply_rulesets.py resolve <root>        # fill the IDs in rulesets/org.json from the org, then regenerate
  apply_rulesets.py plan    <root>        # dry run: what apply would create, update or leave alone
  apply_rulesets.py apply   <root> --yes  # create or update the custom property and the four rulesets
  apply_rulesets.py audit   <root>        # the online half of the nightly bypass audit

Nothing is sent without --yes. plan and apply refuse any ruleset that still
holds an unresolved ID (a 0 in actor_id, integration_id or repository_id),
because the API would reject it or, worse, accept it with the wrong meaning.

audit reads the live organisation rulesets and runs audit_bypass on each. Then,
for every team in a bypass list, it checks the team is one of the two allowed
(acceptance-owners, platform-team) and lists its members, failing on a bot or
machine account. Rule 6: no App, integration or machine account in any bypass
list. The nightly kickoff runs this before any lane starts.

Hosts: github.com uses https://api.github.com. A GHE.com organisation at
<sub>.ghe.com uses https://api.<sub>.ghe.com.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_bypass  # noqa: E402
import make_rulesets as mr  # noqa: E402

PROPERTY = {
    "value_type": "single_select",
    "required": False,
    "allowed_values": ["enabled", "disabled"],
    "description": "Repos the factory gate applies to (plan 5.7). Set by the platform team only.",
}
COMPARED_KEYS = ("name", "target", "enforcement", "bypass_actors", "conditions", "rules")
ID_KEYS = {"actor_id", "integration_id", "repository_id"}
API_VERSION = "2022-11-28"


class ApiError(Exception):
    def __init__(self, status: int, method: str, path: str, body: str):
        super().__init__(f"{method} {path} -> {status}: {body[:300]}")
        self.status = status


def api_base(host: str) -> str:
    return "https://api.github.com" if host == "github.com" else f"https://api.{host}"


class Api:
    """A thin client. `transport(method, url, headers, body) -> (status, text)` is swapped in tests."""

    def __init__(self, host: str, token: str, transport=None):
        self.base = api_base(host)
        self.token = token
        self.transport = transport or self._urllib
        self.sent: list[tuple[str, str, dict | None]] = []

    @staticmethod
    def _urllib(method, url, headers, body):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status, response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode("utf-8", errors="replace")

    def call(self, method: str, path: str, body: dict | None = None, ok=(200, 201)):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "factory-gates apply_rulesets",
        }
        if body is not None:
            headers["Content-Type"] = "application/json"
        if method in ("POST", "PUT", "PATCH", "DELETE"):
            self.sent.append((method, path, body))
        status, text = self.transport(method, self.base + path, headers, body)
        if status not in ok:
            raise ApiError(status, method, path, text)
        return json.loads(text) if text else None

    def get(self, path: str):
        return self.call("GET", path)

    def get_or_none(self, path: str):
        try:
            return self.get(path)
        except ApiError as error:
            if error.status == 404:
                return None
            raise


def token_from_env() -> str:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Set GH_TOKEN or GITHUB_TOKEN to a token with organisation admin.")
    return token


# --- resolve ----------------------------------------------------------------


def resolve(api: Api, org: dict) -> tuple[dict, list[str]]:
    """Return org.json with IDs filled from the organisation, and notes about what stayed 0."""
    name = org["org"]
    notes = []
    out = json.loads(json.dumps(org))
    for slug in out["teams"]:
        team = api.get_or_none(f"/orgs/{name}/teams/{slug}")
        if team is None:
            notes.append(f"team {slug} does not exist in {name}: create it, then resolve again")
        else:
            out["teams"][slug] = team["id"]
    repo = api.get_or_none(f"/repos/{name}/{out['gate_repository']}")
    if repo is None:
        notes.append(f"repository {name}/{out['gate_repository']} does not exist: create it, then resolve again")
    else:
        out["gate_repository_id"] = repo["id"]
    for slug in out["apps"]:
        app = api.get_or_none(f"/apps/{slug}")
        if app is None:
            notes.append(f"app {slug} is not installed or does not exist: its ID stays as it is")
        else:
            out["apps"][slug] = app["id"]
    return out, notes


# --- plan and apply ---------------------------------------------------------


def unresolved_ids(ruleset: dict) -> list[str]:
    found = []

    def walk(node, trail):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ID_KEYS and value == 0:
                    found.append(f"{trail}.{key}" if trail else key)
                walk(value, f"{trail}.{key}" if trail else key)
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{trail}[{index}]")

    walk(ruleset, "")
    return found


def subset(ruleset: dict) -> dict:
    return {key: ruleset.get(key) for key in COMPARED_KEYS}


def plan(api: Api, org: dict, local: dict[str, dict]) -> list[tuple[str, str, str]]:
    """Return (thing, action, detail) rows. Actions: create, update, unchanged, blocked."""
    name = org["org"]
    rows = []
    prop = api.get_or_none(f"/orgs/{name}/properties/schema/factory")
    rows.append(("property factory", "unchanged" if prop else "create", "single_select enabled/disabled"))
    live = {r["name"]: r for r in api.get(f"/orgs/{name}/rulesets?per_page=100")}
    for ruleset_name, ruleset in local.items():
        missing = unresolved_ids(ruleset)
        if missing:
            rows.append((f"ruleset {ruleset_name}", "blocked", f"unresolved IDs: {', '.join(missing)}"))
            continue
        if ruleset_name not in live:
            rows.append((f"ruleset {ruleset_name}", "create", ""))
            continue
        current = api.get(f"/orgs/{name}/rulesets/{live[ruleset_name]['id']}")
        if subset(current) == subset(ruleset):
            rows.append((f"ruleset {ruleset_name}", "unchanged", f"id {current['id']}"))
        else:
            rows.append((f"ruleset {ruleset_name}", "update", f"id {current['id']}"))
    return rows


def apply(api: Api, org: dict, local: dict[str, dict]) -> list[tuple[str, str, str]]:
    name = org["org"]
    rows = plan(api, org, local)
    live = {r["name"]: r for r in api.get(f"/orgs/{name}/rulesets?per_page=100")}
    done = []
    for thing, action, detail in rows:
        if action in ("unchanged", "blocked"):
            done.append((thing, action, detail))
        elif thing == "property factory":
            api.call("PUT", f"/orgs/{name}/properties/schema/factory", PROPERTY, ok=(200, 201))
            done.append((thing, "created", ""))
        elif action == "create":
            created = api.call("POST", f"/orgs/{name}/rulesets", local[thing.split(" ", 1)[1]])
            done.append((thing, "created", f"id {created['id']}"))
        elif action == "update":
            ruleset_name = thing.split(" ", 1)[1]
            updated = api.call("PUT", f"/orgs/{name}/rulesets/{live[ruleset_name]['id']}", local[ruleset_name])
            done.append((thing, "updated", f"id {updated['id']}"))
    return done


# --- audit ------------------------------------------------------------------


def audit_live(api: Api, org: dict) -> list[str]:
    """The online half of the bypass audit. Empty means clean."""
    name = org["org"]
    allowed = {org["teams"][team]: team for team in mr.BYPASS_TEAMS}
    problems = []
    teams_seen = set()
    for summary in api.get(f"/orgs/{name}/rulesets?per_page=100"):
        ruleset = api.get(f"/orgs/{name}/rulesets/{summary['id']}")
        problems.extend(audit_bypass.audit(ruleset))
        for actor in ruleset.get("bypass_actors") or []:
            if actor.get("actor_type") == "Team":
                teams_seen.add((ruleset["name"], actor.get("actor_id")))
    teams = {team["id"]: team["slug"] for team in api.get(f"/orgs/{name}/teams?per_page=100")}
    for ruleset_name, team_id in sorted(teams_seen, key=str):
        slug = teams.get(team_id, f"id {team_id}")
        if team_id not in allowed or allowed[team_id] == 0:
            problems.append(f"{ruleset_name}: team {slug} is in the bypass list. Only {' and '.join(mr.BYPASS_TEAMS)} may bypass (plan 5.7)")
        if team_id in teams:
            for member in api.get(f"/orgs/{name}/teams/{teams[team_id]}/members?per_page=100"):
                login = member.get("login", "?")
                if member.get("type") != "User" or login.endswith("[bot]"):
                    problems.append(f"{ruleset_name}: bypass team {slug} has a non-human member {login} (rule 6)")
    return problems


# --- command line -----------------------------------------------------------


def print_rows(rows):
    for thing, action, detail in rows:
        print(f"{action:<10} {thing}{'  ' + detail if detail else ''}")


def main(argv: list[str], transport=None) -> int:
    if len(argv) < 3 or argv[1] not in ("resolve", "plan", "apply", "audit"):
        print(__doc__, file=sys.stderr)
        return 2
    command, root = argv[1], Path(argv[2])
    org = mr.load_org(root)
    api = Api(org["host"], token_from_env(), transport)
    try:
        if command == "resolve":
            resolved, notes = resolve(api, org)
            (root / mr.ORG_FILE).write_text(json.dumps(resolved, indent=2) + "\n", encoding="utf-8")
            mr.make(root)
            print(f"rulesets/org.json updated and rulesets regenerated. Regenerate scripts.sha256 next.")
            for note in notes:
                print(f"note: {note}")
            return 1 if notes else 0
        local = mr.rulesets(org)
        if command == "plan":
            print_rows(plan(api, org, local))
            return 0
        if command == "apply":
            if "--yes" not in argv[3:]:
                print_rows(plan(api, org, local))
                print("Nothing sent. Add --yes to apply.", file=sys.stderr)
                return 2
            print_rows(apply(api, org, local))
            return 0
        problems = audit_live(api, org)
        for problem in problems:
            print(problem, file=sys.stderr)
        print("bypass audit: " + ("clean" if not problems else f"{len(problems)} problems"))
        return 1 if problems else 0
    except ApiError as error:
        print(f"GitHub API: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
