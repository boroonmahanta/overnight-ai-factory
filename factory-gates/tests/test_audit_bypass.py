import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lcp"))
import audit_bypass  # noqa: E402
import make_rulesets as mr  # noqa: E402

RULESETS = ROOT / "rulesets"


def ruleset(name, *actors):
    return {"name": name, "target": "push", "enforcement": "active", "bypass_actors": list(actors), "rules": []}


def actor(kind, actor_id=1):
    return {"actor_id": actor_id, "actor_type": kind, "bypass_mode": "always"}


class AuditTests(unittest.TestCase):
    def test_empty_bypass_passes(self):
        self.assertEqual(audit_bypass.audit(ruleset("main-gate")), [])
        self.assertEqual(audit_bypass.audit({"name": "x", "bypass_actors": None}), [])

    def test_a_team_passes_outside_main_gate(self):
        self.assertEqual(audit_bypass.audit(ruleset("protected-paths", actor("Team", 42))), [])

    def test_main_gate_must_have_an_empty_bypass_list(self):
        problems = audit_bypass.audit(ruleset("main-gate", actor("Team", 42)))
        self.assertEqual(problems, ["main-gate: the bypass list must be empty, it has 1 entries"])

    def test_copilot_is_an_app_and_fails(self):
        # GitHub's docs suggest adding Copilot as a bypass actor when a ruleset blocks it.
        # Copilot is a GitHub App, so it arrives as an Integration. That is the trap (plan 5.7).
        problems = audit_bypass.audit(ruleset("protected-paths", actor("Integration", 1143301)))
        self.assertEqual(len(problems), 1)
        self.assertIn("GitHub App or integration", problems[0])
        self.assertIn("Copilot is one", problems[0])
        self.assertIn("rule 6", problems[0])

    def test_write_role_fails(self):
        problems = audit_bypass.audit(ruleset("protected-paths", actor("RepositoryRole", 4)))
        self.assertEqual(len(problems), 1)
        self.assertIn("repository role write (id 4)", problems[0])

    def test_every_repository_role_fails_not_only_write(self):
        for role_id in (1, 2, 3, 5, 99):
            self.assertEqual(len(audit_bypass.audit(ruleset("integration-gate", actor("RepositoryRole", role_id)))), 1)

    def test_deploy_key_and_org_admin_and_unknown_fail(self):
        for kind in ("DeployKey", "OrganizationAdmin", "Mystery"):
            problems = audit_bypass.audit(ruleset("protected-paths", actor(kind)))
            self.assertEqual(len(problems), 1, kind)

    def test_one_problem_per_bad_actor(self):
        problems = audit_bypass.audit(ruleset("protected-paths", actor("Team", 1), actor("Integration", 2), actor("DeployKey", None)))
        self.assertEqual(len(problems), 2)


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_audit(self, *paths):
        return subprocess.run(
            [sys.executable, str(Path(audit_bypass.__file__)), *map(str, paths)],
            capture_output=True, text=True,
        )

    def write(self, name, data):
        path = self.dir / f"{name}.json"
        path.write_text(json.dumps(data) if not isinstance(data, str) else data)
        return path

    def test_committed_rulesets_pass(self):
        result = self.run_audit(*(RULESETS / f"{name}.json" for name in mr.RULESET_NAMES))
        self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_seeded_copilot_in_protected_paths_fails(self):
        # The committed ruleset, with Copilot added to its bypass list.
        data = json.loads((RULESETS / "protected-paths.json").read_text())
        data["bypass_actors"].append(actor("Integration", 1143301))
        result = self.run_audit(self.write("bad", data))
        self.assertEqual(result.returncode, 1)
        self.assertIn("protected-paths: a GitHub App or integration (app id 1143301; Copilot is one)", result.stderr)

    def test_seeded_team_in_main_gate_fails(self):
        data = json.loads((RULESETS / "main-gate.json").read_text())
        data["bypass_actors"].append(actor("Team", 7))
        result = self.run_audit(self.write("bad", data))
        self.assertEqual(result.returncode, 1)
        self.assertIn("main-gate: the bypass list must be empty", result.stderr)

    def test_unreadable_or_odd_files_fail(self):
        self.assertEqual(self.run_audit(self.write("broken", "{not json")).returncode, 1)
        self.assertEqual(self.run_audit(self.write("list", [])).returncode, 1)
        self.assertEqual(self.run_audit(self.dir / "absent.json").returncode, 1)

    def test_no_arguments_prints_usage(self):
        result = self.run_audit()
        self.assertEqual(result.returncode, 2)
        self.assertIn("audit_bypass.py <ruleset.json>", result.stderr)


if __name__ == "__main__":
    unittest.main()
