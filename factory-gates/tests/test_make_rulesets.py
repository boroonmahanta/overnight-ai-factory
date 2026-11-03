import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lcp"))
import audit_bypass  # noqa: E402
import check_protected_paths as cpp  # noqa: E402
import make_rulesets as mr  # noqa: E402

RULESETS = ROOT / "rulesets"
CODEOWNERS = ROOT / "templates/CODEOWNERS"


def load(name: str) -> dict:
    return json.loads((RULESETS / f"{name}.json").read_text(encoding="utf-8"))


def rules_by_type(ruleset: dict) -> dict:
    return {rule["type"]: rule.get("parameters", {}) for rule in ruleset["rules"]}


class CommittedFilesTests(unittest.TestCase):
    """The committed JSON and CODEOWNERS match the one list in check_protected_paths.py."""

    def test_committed_ruleset_and_codeowners_are_current(self):
        # If this fails: python3 lcp/make_rulesets.py make . (then regenerate scripts.sha256),
        # or fix templates/CODEOWNERS. Both are gate changes: reviewed daytime PR only (rule 17).
        self.assertEqual(mr.check(ROOT), [])

    def test_protected_paths_ruleset_lists_every_protected_path(self):
        ruleset = load("protected-paths")
        self.assertEqual(ruleset["target"], "push")
        self.assertEqual(ruleset["enforcement"], "active")
        self.assertEqual(rules_by_type(ruleset)["file_path_restriction"]["restricted_file_paths"], cpp.PROTECTED_PATHS)

    def test_ruleset_bypass_is_the_two_teams_only(self):
        actors = load("protected-paths")["bypass_actors"]
        self.assertEqual(len(actors), 2)
        self.assertEqual({a["actor_type"] for a in actors}, {"Team"})

    def test_ruleset_and_locks_job_block_the_same_paths(self):
        # Every pattern the ruleset restricts is a pattern the locks job also blocks.
        samples = [p for glob in load("protected-paths")["rules"][0]["parameters"]["restricted_file_paths"]
                   for p in mr.sample_paths(glob)]
        self.assertEqual(cpp.find_protected(samples), sorted(set(samples)))

    def test_all_four_rulesets_parse_and_are_named_after_their_file(self):
        names = sorted(p.stem for p in RULESETS.glob("*.json"))
        self.assertEqual(names, ["factory-required-workflows", "integration-gate", "main-gate", "protected-paths"])
        for name in names:
            ruleset = load(name)
            self.assertEqual(ruleset["name"], name)
            self.assertIn(ruleset["target"], {"branch", "push"})
            self.assertIn(ruleset["enforcement"], {"active", "evaluate"})
            self.assertTrue(ruleset["rules"])

    def test_all_four_rulesets_pass_the_bypass_audit(self):
        for path in RULESETS.glob("*.json"):
            self.assertEqual(audit_bypass.audit_file(path), [], path.name)

    def test_every_ruleset_applies_only_to_factory_repos(self):
        for path in RULESETS.glob("*.json"):
            prop = load(path.stem)["conditions"]["repository_property"]["include"]
            self.assertEqual(prop, [{"name": "factory", "property_values": ["enabled"], "source": "custom"}], path.name)


class PlanSettingsTests(unittest.TestCase):
    """Settings as plan section 5.7, part 3."""

    def test_main_gate(self):
        ruleset = load("main-gate")
        self.assertEqual(ruleset["bypass_actors"], [])
        self.assertEqual(ruleset["conditions"]["ref_name"]["include"], ["refs/heads/main"])
        rules = rules_by_type(ruleset)
        for required in ("deletion", "non_fast_forward", "required_linear_history", "merge_queue"):
            self.assertIn(required, rules)
        pr = rules["pull_request"]
        self.assertEqual(pr["required_approving_review_count"], 1)
        self.assertTrue(pr["dismiss_stale_reviews_on_push"])
        self.assertTrue(pr["require_code_owner_review"])
        self.assertTrue(pr["require_last_push_approval"])
        checks = rules["required_status_checks"]
        self.assertTrue(checks["strict_required_status_checks_policy"])
        self.assertEqual([c["context"] for c in checks["required_status_checks"]], ["lcp-gate"])
        for check in checks["required_status_checks"]:
            self.assertIn("integration_id", check, "pin every check to its source app")

    def test_integration_gate(self):
        ruleset = load("integration-gate")
        self.assertEqual(ruleset["bypass_actors"], [])
        self.assertEqual(ruleset["conditions"]["ref_name"]["include"], ["refs/heads/integration"])
        rules = rules_by_type(ruleset)
        self.assertEqual(rules["pull_request"]["required_approving_review_count"], 1)
        self.assertIn("merge_queue", rules)
        contexts = [c["context"] for c in rules["required_status_checks"]["required_status_checks"]]
        self.assertEqual(contexts, ["lcp-gate", "lane/drift"])

    def test_required_workflows(self):
        ruleset = load("factory-required-workflows")
        self.assertEqual(ruleset["enforcement"], "evaluate", "stage 1 starts in Evaluate mode (plan 11.2)")
        self.assertEqual(ruleset["bypass_actors"], [])
        workflows = rules_by_type(ruleset)["workflows"]["workflows"]
        self.assertEqual(len(workflows), 1)
        self.assertEqual(workflows[0]["path"], ".github/workflows/lcp-gate.yml")
        self.assertEqual(workflows[0]["ref"], "refs/heads/release")


class SeededFailureTests(unittest.TestCase):
    """Copies of the committed files, broken on purpose, must fail the check."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(RULESETS, self.root / "rulesets")
        shutil.copytree(ROOT / "templates", self.root / "templates")

    def tearDown(self):
        self.tmp.cleanup()

    def run_check(self):
        return subprocess.run(
            [sys.executable, str(Path(mr.__file__)), "check", str(self.root)],
            capture_output=True, text=True,
        )

    def test_fresh_copy_passes(self):
        self.assertEqual(self.run_check().returncode, 0)

    def test_stale_ruleset_fails(self):
        path = self.root / mr.RULESET_FILE
        ruleset = json.loads(path.read_text())
        ruleset["rules"][0]["parameters"]["restricted_file_paths"].remove("scripts/**")
        path.write_text(json.dumps(ruleset, indent=2) + "\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("stale: rulesets/protected-paths.json", result.stderr)

    def test_missing_ruleset_fails(self):
        (self.root / mr.RULESET_FILE).unlink()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing: rulesets/protected-paths.json", result.stderr)

    def test_protected_path_missing_from_codeowners_fails(self):
        path = self.root / mr.CODEOWNERS_FILE
        lines = [line for line in path.read_text().splitlines() if not line.startswith("/tests/acceptance/")]
        path.write_text("\n".join(lines) + "\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("protected path tests/acceptance/** (tests/acceptance/sample.txt) is not owned by", result.stderr)
        self.assertIn("no owner", result.stderr)

    def test_protected_path_owned_by_the_wrong_team_fails(self):
        path = self.root / mr.CODEOWNERS_FILE
        path.write_text(path.read_text() + "\n/deploy/   @getai/factory-reviewers\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("protected path deploy/** (deploy/sample.txt) is not owned by", result.stderr)
        self.assertIn("@getai/factory-reviewers", result.stderr)

    def test_make_repairs_a_stale_ruleset(self):
        (self.root / mr.RULESET_FILE).write_text("{}\n")
        subprocess.run([sys.executable, str(Path(mr.__file__)), "make", str(self.root)], check=True)
        self.assertEqual(self.run_check().returncode, 0)


class CodeownersMatchingTests(unittest.TestCase):
    """The matcher follows GitHub's CODEOWNERS rules for the patterns we use."""

    def owners(self, text, path):
        return mr.owners_of(path, mr.parse_codeowners(text))

    def test_anchored_folder_covers_everything_below_it(self):
        text = "/tests/acceptance/  @t/a\n"
        self.assertEqual(self.owners(text, "tests/acceptance/x.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "tests/acceptance/deep/x.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "other/tests/acceptance/x.md"), [])
        self.assertEqual(self.owners(text, "tests/acceptance-old/x.md"), [])

    def test_anchored_file_matches_only_at_the_root(self):
        text = "/glossary.md  @t/a\n"
        self.assertEqual(self.owners(text, "glossary.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "docs/glossary.md"), [])
        self.assertEqual(self.owners(text, "glossary.md.bak"), [])

    def test_unanchored_pattern_matches_at_any_depth(self):
        text = "*.md  @t/a\n"
        self.assertEqual(self.owners(text, "a/b/c.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "c.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "c.mdx"), [])

    def test_single_star_stays_within_one_folder(self):
        text = "/specs/*/spec.md  @t/a\n"
        self.assertEqual(self.owners(text, "specs/001/spec.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "specs/001/sub/spec.md"), [])

    def test_trailing_star_does_not_reach_subfolders(self):
        text = "/docs/*  @t/a\n"
        self.assertEqual(self.owners(text, "docs/x.md"), ["@t/a"])
        self.assertEqual(self.owners(text, "docs/sub/x.md"), [])

    def test_last_matching_line_wins_and_comments_are_ignored(self):
        text = "# comment\n/deploy/  @t/a  # trailing\n/deploy/prod/  @t/b @t/c\n"
        self.assertEqual(self.owners(text, "deploy/x.json"), ["@t/a"])
        self.assertEqual(self.owners(text, "deploy/prod/x.json"), ["@t/b", "@t/c"])

    def test_check_accepts_either_allowed_team(self):
        text = "/glossary.md  @getai/platform-team\n"
        self.assertEqual(mr.check_codeowners(text, ["glossary.md"]), [])

    def test_sample_paths(self):
        self.assertEqual(mr.sample_paths("deploy/**"), ["deploy/sample.txt", "deploy/sub/sample.txt"])
        self.assertEqual(mr.sample_paths("specs/*/spec.md"), ["specs/x/spec.md"])
        self.assertEqual(mr.sample_paths("CLAUDE.md"), ["CLAUDE.md"])


if __name__ == "__main__":
    unittest.main()
