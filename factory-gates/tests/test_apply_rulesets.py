import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lcp"))
import apply_rulesets as ar  # noqa: E402
import make_rulesets as mr  # noqa: E402

ORG = mr.load_org(ROOT)["org"]


class FakeGitHub:
    """Answers the handful of endpoints the tool uses. Records every write."""

    def __init__(self, org=ORG, teams=None, repos=None, apps=None, rulesets=None, members=None, property_exists=False):
        self.org = org
        self.teams = teams or {}          # slug -> id
        self.repos = repos or {}          # name -> id
        self.apps = apps or {}            # slug -> id
        self.rulesets = rulesets or []    # list of dicts with id
        self.members = members or {}      # slug -> list of {login, type}
        self.property_exists = property_exists
        self.next_id = 900
        self.writes = []

    def __call__(self, method, url, headers, body):
        assert headers["Authorization"] == "Bearer t0k", headers
        assert url.startswith("https://api.")
        path = url.split("/", 3)[3]
        path = "/" + path.split("?")[0]
        if method in ("POST", "PUT"):
            self.writes.append((method, path, body))
        o = self.org
        if path == f"/orgs/{o}/properties/schema/factory":
            if method == "PUT":
                self.property_exists = True
                return 200, json.dumps({"property_name": "factory"})
            return (200, json.dumps({"property_name": "factory"})) if self.property_exists else (404, "{}")
        if path.startswith(f"/orgs/{o}/teams/") and path.endswith("/members"):
            slug = path.split("/")[4]
            return 200, json.dumps(self.members.get(slug, []))
        if path.startswith(f"/orgs/{o}/teams/"):
            slug = path.split("/")[4]
            return (200, json.dumps({"id": self.teams[slug], "slug": slug})) if slug in self.teams else (404, "{}")
        if path == f"/orgs/{o}/teams":
            return 200, json.dumps([{"id": i, "slug": s} for s, i in self.teams.items()])
        if path.startswith(f"/repos/{o}/"):
            name = path.split("/")[3]
            return (200, json.dumps({"id": self.repos[name]})) if name in self.repos else (404, "{}")
        if path.startswith("/apps/"):
            slug = path.split("/")[2]
            return (200, json.dumps({"id": self.apps[slug]})) if slug in self.apps else (404, "{}")
        if path == f"/orgs/{o}/rulesets":
            if method == "POST":
                self.next_id += 1
                stored = {**body, "id": self.next_id}
                self.rulesets.append(stored)
                return 201, json.dumps(stored)
            return 200, json.dumps([{"id": r["id"], "name": r["name"]} for r in self.rulesets])
        if path.startswith(f"/orgs/{o}/rulesets/"):
            rid = int(path.rsplit("/", 1)[1])
            for index, r in enumerate(self.rulesets):
                if r["id"] == rid:
                    if method == "PUT":
                        self.rulesets[index] = {**body, "id": rid}
                        return 200, json.dumps(self.rulesets[index])
                    return 200, json.dumps({**r, "source": o, "_links": {}})
            return 404, "{}"
        raise AssertionError(f"unexpected {method} {path}")


def resolved_org(**overrides):
    org = mr.load_org(ROOT)
    org["teams"] = {"acceptance-owners": 11, "platform-team": 12, "factory-reviewers": 13}
    org["gate_repository_id"] = 501
    org["apps"] = {"github-actions": 15368, "lane-drift": 77}
    org.update(overrides)
    return org


class ApiTests(unittest.TestCase):
    def test_hosts(self):
        self.assertEqual(ar.api_base("github.com"), "https://api.github.com")
        self.assertEqual(ar.api_base("getai.ghe.com"), "https://api.getai.ghe.com")

    def test_token_must_be_set(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                ar.token_from_env()


class ResolveTests(unittest.TestCase):
    def test_fills_ids_and_reports_what_is_missing(self):
        gh = FakeGitHub(teams={"acceptance-owners": 11, "platform-team": 12}, repos={"factory-gates": 501}, apps={"github-actions": 15368})
        org = mr.load_org(ROOT)
        out, notes = ar.resolve(ar.Api("github.com", "t0k", gh), org)
        self.assertEqual(out["teams"], {"acceptance-owners": 11, "platform-team": 12, "factory-reviewers": 0})
        self.assertEqual(out["gate_repository_id"], 501)
        self.assertEqual(out["apps"], {"github-actions": 15368, "lane-drift": 0})
        self.assertEqual(len(notes), 2)
        self.assertIn("team factory-reviewers does not exist", notes[0])
        self.assertIn("app lane-drift", notes[1])
        self.assertEqual(gh.writes, [], "resolve only reads")
        self.assertEqual(org["teams"]["acceptance-owners"], 0, "the input is not changed in place")


class PlanAndApplyTests(unittest.TestCase):
    def setUp(self):
        self.org = resolved_org()
        self.local = mr.rulesets(self.org)

    def test_unresolved_ids_are_found_wherever_they_sit(self):
        local = mr.rulesets(mr.load_org(ROOT))
        self.assertEqual(ar.unresolved_ids(local["protected-paths"]), ["bypass_actors[0].actor_id", "bypass_actors[1].actor_id"])
        self.assertEqual(ar.unresolved_ids(local["factory-required-workflows"]), ["rules[0].parameters.workflows[0].repository_id"])
        self.assertEqual(ar.unresolved_ids(local["integration-gate"]), [], "lane/drift is out for stage 1, so nothing is unresolved")
        self.assertEqual(ar.unresolved_ids(local["main-gate"]), [])
        self.assertEqual(ar.unresolved_ids(self.local["integration-gate"]), [])

    def test_plan_on_an_empty_org_creates_everything_and_sends_nothing(self):
        gh = FakeGitHub()
        rows = ar.plan(ar.Api("github.com", "t0k", gh), self.org, self.local)
        self.assertEqual([(t, a) for t, a, _ in rows], [
            ("property factory", "create"),
            ("ruleset main-gate", "create"),
            ("ruleset integration-gate", "create"),
            ("ruleset protected-paths", "create"),
            ("ruleset factory-required-workflows", "create"),
        ])
        self.assertEqual(gh.writes, [])

    def test_plan_blocks_a_ruleset_with_an_unresolved_id(self):
        local = mr.rulesets(mr.load_org(ROOT))
        rows = ar.plan(ar.Api("github.com", "t0k", FakeGitHub()), self.org, local)
        actions = {t: (a, d) for t, a, d in rows}
        self.assertEqual(actions["ruleset protected-paths"][0], "blocked")
        self.assertIn("actor_id", actions["ruleset protected-paths"][1])
        self.assertEqual(actions["ruleset main-gate"][0], "create")

    def test_apply_creates_then_a_second_apply_changes_nothing(self):
        gh = FakeGitHub()
        api = ar.Api("github.com", "t0k", gh)
        done = ar.apply(api, self.org, self.local)
        self.assertEqual([a for _, a, _ in done], ["created"] * 5)
        self.assertEqual([m for m, _, _ in gh.writes], ["PUT", "POST", "POST", "POST", "POST"])
        self.assertEqual(gh.writes[0][1], f"/orgs/{ORG}/properties/schema/factory")
        self.assertEqual(gh.writes[0][2]["allowed_values"], ["enabled", "disabled"])
        self.assertEqual(gh.writes[1][2], self.local["main-gate"])
        gh.writes.clear()
        done = ar.apply(api, self.org, self.local)
        self.assertEqual([a for _, a, _ in done], ["unchanged"] * 5)
        self.assertEqual(gh.writes, [])

    def test_a_drifted_live_ruleset_is_updated_in_place(self):
        drifted = {**self.local["main-gate"], "id": 42, "bypass_actors": [{"actor_id": 9, "actor_type": "Team", "bypass_mode": "always"}]}
        gh = FakeGitHub(rulesets=[drifted], property_exists=True)
        api = ar.Api("github.com", "t0k", gh)
        rows = ar.plan(api, self.org, self.local)
        self.assertEqual(rows[1], ("ruleset main-gate", "update", "id 42"))
        ar.apply(api, self.org, self.local)
        self.assertEqual(gh.writes[0][:2], ("PUT", f"/orgs/{ORG}/rulesets/42"))
        self.assertEqual(gh.rulesets[0]["bypass_actors"], [])

    def test_api_errors_are_raised_with_the_status(self):
        gh = FakeGitHub()
        api = ar.Api("github.com", "t0k", lambda m, u, h, b: (403, '{"message":"Resource not accessible"}'))
        with self.assertRaises(ar.ApiError) as raised:
            ar.plan(api, self.org, self.local)
        self.assertEqual(raised.exception.status, 403)


class AuditLiveTests(unittest.TestCase):
    def setUp(self):
        self.org = resolved_org()
        self.local = mr.rulesets(self.org)
        self.gh = FakeGitHub(teams={"acceptance-owners": 11, "platform-team": 12, "factory-reviewers": 13, "everyone": 14},
                             members={"acceptance-owners": [{"login": "ana", "type": "User"}],
                                      "platform-team": [{"login": "ben", "type": "User"}]})
        self.gh.rulesets = [{**r, "id": 100 + i} for i, r in enumerate(self.local.values())]
        self.api = ar.Api("github.com", "t0k", self.gh)

    def test_clean_org_passes(self):
        self.assertEqual(ar.audit_live(self.api, self.org), [])
        self.assertEqual(self.gh.writes, [])

    def test_copilot_added_in_the_ui_is_caught(self):
        self.gh.rulesets[2]["bypass_actors"].append({"actor_id": 1143301, "actor_type": "Integration", "bypass_mode": "always"})
        problems = ar.audit_live(self.api, self.org)
        self.assertEqual(len(problems), 1)
        self.assertIn("protected-paths: a GitHub App or integration", problems[0])

    def test_a_team_in_main_gate_is_caught(self):
        self.gh.rulesets[0]["bypass_actors"].append({"actor_id": 12, "actor_type": "Team", "bypass_mode": "always"})
        problems = ar.audit_live(self.api, self.org)
        self.assertIn("main-gate: the bypass list must be empty, it has 1 entries", problems)

    def test_a_third_team_in_the_push_ruleset_is_caught(self):
        self.gh.rulesets[2]["bypass_actors"].append({"actor_id": 14, "actor_type": "Team", "bypass_mode": "always"})
        problems = ar.audit_live(self.api, self.org)
        self.assertEqual(len(problems), 1)
        self.assertIn("protected-paths: team everyone is in the bypass list", problems[0])

    def test_a_bot_in_a_bypass_team_is_caught(self):
        self.gh.members["platform-team"].append({"login": "factory-merger[bot]", "type": "Bot"})
        self.gh.members["acceptance-owners"].append({"login": "svc-deploy", "type": "Bot"})
        problems = ar.audit_live(self.api, self.org)
        self.assertEqual(len(problems), 2)
        self.assertTrue(any("factory-merger[bot]" in p for p in problems))
        self.assertTrue(any("svc-deploy" in p for p in problems))

    def test_an_unknown_team_id_is_reported_by_id(self):
        self.gh.rulesets[2]["bypass_actors"].append({"actor_id": 999, "actor_type": "Team", "bypass_mode": "always"})
        problems = ar.audit_live(self.api, self.org)
        self.assertIn("team id 999 is in the bypass list", problems[0])


class CommandLineTests(unittest.TestCase):
    """main() with a fake transport: the command surface, never the network."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / "rulesets", self.root / "rulesets")
        shutil.copytree(ROOT / "templates", self.root / "templates")
        self.env = mock.patch.dict(os.environ, {"GH_TOKEN": "t0k"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_usage(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(ar.main(["x"]), 2)
            self.assertEqual(ar.main(["x", "nuke", "."]), 2)

    def test_resolve_rewrites_org_json_and_regenerates(self):
        gh = FakeGitHub(teams={"acceptance-owners": 11, "platform-team": 12, "factory-reviewers": 13},
                        repos={"factory-gates": 501}, apps={"github-actions": 15368, "lane-drift": 77})
        self.assertEqual(ar.main(["x", "resolve", str(self.root)], transport=gh), 0)
        org = mr.load_org(self.root)
        self.assertEqual(org["teams"]["platform-team"], 12)
        self.assertEqual(mr.check(self.root), [], "rulesets were regenerated to match")
        protected = json.loads((self.root / "rulesets/protected-paths.json").read_text())
        self.assertEqual([a["actor_id"] for a in protected["bypass_actors"]], [11, 12])

    def test_resolve_with_a_missing_team_still_writes_and_returns_1(self):
        gh = FakeGitHub(teams={"acceptance-owners": 11}, repos={"factory-gates": 501}, apps={"github-actions": 15368})
        self.assertEqual(ar.main(["x", "resolve", str(self.root)], transport=gh), 1)
        self.assertEqual(mr.load_org(self.root)["teams"]["acceptance-owners"], 11)

    def test_apply_without_yes_sends_nothing(self):
        gh = FakeGitHub()
        self.assertEqual(ar.main(["x", "apply", str(self.root)], transport=gh), 2)
        self.assertEqual(gh.writes, [])

    def test_plan_sends_nothing(self):
        gh = FakeGitHub()
        self.assertEqual(ar.main(["x", "plan", str(self.root)], transport=gh), 0)
        self.assertEqual(gh.writes, [])

    def test_apply_with_yes_on_unresolved_ids_sends_only_what_is_resolved(self):
        # The committed org.json has team and repo IDs of 0: only the property, main-gate
        # and integration-gate (no lane/drift in stage 1) can go.
        gh = FakeGitHub()
        self.assertEqual(ar.main(["x", "apply", str(self.root), "--yes"], transport=gh), 0)
        self.assertEqual([(m, p) for m, p, _ in gh.writes],
                         [("PUT", f"/orgs/{ORG}/properties/schema/factory"), ("POST", f"/orgs/{ORG}/rulesets"), ("POST", f"/orgs/{ORG}/rulesets")])
        self.assertEqual([w[2]["name"] for w in gh.writes[1:]], ["main-gate", "integration-gate"])

    def test_audit_exit_codes(self):
        gh = FakeGitHub(teams={"acceptance-owners": 11, "platform-team": 12})
        self.assertEqual(ar.main(["x", "audit", str(self.root)], transport=gh), 0)
        gh.rulesets = [{"id": 1, "name": "main-gate", "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]}]
        self.assertEqual(ar.main(["x", "audit", str(self.root)], transport=gh), 1)

    def test_api_error_is_reported_not_raised(self):
        self.assertEqual(ar.main(["x", "plan", str(self.root)], transport=lambda m, u, h, b: (401, '{"message":"Bad credentials"}')), 1)


if __name__ == "__main__":
    unittest.main()
