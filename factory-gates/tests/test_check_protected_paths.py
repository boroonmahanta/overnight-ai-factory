import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gate" / "lcp"))
import check_protected_paths as cpp  # noqa: E402


class FindProtectedTests(unittest.TestCase):
    def test_every_protected_area_is_caught(self):
        paths = [
            "tests/acceptance/trip.spec.ts", "tests/scenarios/a.md",
            "specs/001/spec.md", "specs/001/checklists/ux.md",
            "glossary.md", "docs/adr/0007-x.md", "coding-standards.md",
            ".specify/preset.yml", ".github/workflows/x.yml", ".claude/skills/a/SKILL.md",
            ".mcp/config.json", "AGENTS.md", "CLAUDE.md",
            "scripts/run.sh", "builders/lib/helpers.py", "deploy/settings.json",
        ]
        self.assertEqual(cpp.find_protected(paths), sorted(paths))

    def test_ordinary_files_pass(self):
        paths = [
            "src/Other/Entities/trip.yml", "workflows/build/flows.py", "handoff/48213/state.md",
            "tests/dev/48213/check.md", "specs/001/plan.md", "specs/001/tasks.md",
            "docs/lessons-learned.md", "README.md",
        ]
        self.assertEqual(cpp.find_protected(paths), [])

    def test_lookalikes_pass(self):
        # Near misses must not trip the check: it is anchored at the repo root.
        paths = ["src/scripts/x.py", "docs/glossary.md.bak", "mytests/acceptance/x", "docs/CLAUDE.md"]
        self.assertEqual(cpp.find_protected(paths), [])


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class GitDiffTests(unittest.TestCase):
    """Real git repos: the check must see what git actually reports."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "tests/acceptance").mkdir(parents=True)
        (self.repo / "tests/acceptance/trip.md").write_text("locked scenario\n" * 20)
        (self.repo / "src").mkdir()
        (self.repo / "src/a.txt").write_text("a\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "base")
        self.base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, check=True,
                                   capture_output=True, text=True).stdout.strip()
        git(self.repo, "checkout", "-q", "-b", "agent/fl1/1-1")

    def tearDown(self):
        self.tmp.cleanup()

    def commit_all(self):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "change")

    def run_check(self, lane="fl1"):
        return subprocess.run(
            [sys.executable, str(Path(cpp.__file__)), "--lane", lane, "--base", self.base],
            cwd=self.repo, capture_output=True, text=True,
        )

    def test_edit_to_locked_scenario_is_blocked(self):
        (self.repo / "tests/acceptance/trip.md").write_text("weakened\n")
        self.commit_all()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("tests/acceptance/trip.md", result.stderr)

    def test_clean_change_passes(self):
        (self.repo / "src/a.txt").write_text("b\n")
        self.commit_all()
        self.assertEqual(self.run_check().returncode, 0)

    def test_moving_a_protected_file_out_of_its_folder_is_blocked(self):
        # With rename detection on, git would show only src/moved.md and this would pass.
        (self.repo / "tests/acceptance/trip.md").rename(self.repo / "src/moved.md")
        self.commit_all()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("tests/acceptance/trip.md", result.stderr)

    def test_filename_with_spaces_and_unicode(self):
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts/my script é.sh").write_text("x\n")
        self.commit_all()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("scripts/my script é.sh", result.stderr)

    def test_human_pr_is_not_checked(self):
        (self.repo / "tests/acceptance/trip.md").write_text("humans may change this\n")
        self.commit_all()
        self.assertEqual(self.run_check(lane="none").returncode, 0)


if __name__ == "__main__":
    unittest.main()
