"""Tests for lcp/check_builders.py (Build 3, 3 November 2026).

Each test copies tests/fixtures/builder-project/ into a fresh git repo, commits
it as a PR would arrive, and runs the script the way the build job does. The
fixture holds one builder and its committed output.
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "lcp/check_builders.py"
FIXTURE = ROOT / "tests/fixtures/builder-project"
OUTPUT = "src/generated/status_choices.yml"
BUILDER = "workflows/build/build_status_choices.py"


def git(cwd, *args) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


class CheckBuildersTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "project"
        shutil.copytree(FIXTURE, self.repo)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "user.email", "t@example.com")
        git(self.repo, "config", "user.name", "t")
        self.commit("fixture project")

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, message):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "--allow-empty", "-m", message)

    def write(self, rel, text):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def check(self, *extra, root=None):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(root or self.repo), *extra],
            capture_output=True, text=True,
        )

    # The cases the build plan names.

    def test_matching_output_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"running {BUILDER}", result.stdout)
        self.assertIn("1 builder(s) ran, generated files match the commit", result.stdout)
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_hand_edited_output_fails(self):
        out = self.repo / OUTPUT
        out.write_text(out.read_text().replace("label: Approved", "label: Approved by hand"))
        self.commit("agent edits generated output")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Generated files do not match builders", result.stderr)
        self.assertIn(f"changed: {OUTPUT}", result.stderr)
        self.assertIn("-    label: Approved by hand", result.stderr)  # the diff is shown
        self.assertIn("+    label: Approved", result.stderr)

    def test_builder_that_crashes_fails_and_the_others_still_run(self):
        self.write("workflows/build/build_broken.py", 'raise RuntimeError("input file is missing")\n')
        self.commit("add a broken builder")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("builder workflows/build/build_broken.py failed with exit code 1", result.stderr)
        self.assertIn("RuntimeError: input file is missing", result.stderr)
        # build_broken sorts first; the good builder still ran and its output still matches.
        self.assertLess(result.stdout.index("build_broken.py"), result.stdout.index(BUILDER))
        self.assertNotIn("do not match", result.stderr)

    # Drift the plan's inline `git diff --exit-code` would miss.

    def test_output_left_out_of_the_commit_fails(self):
        git(self.repo, "rm", "-q", OUTPUT)
        self.commit("agent forgets to commit generated output")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"not in the commit: {OUTPUT}", result.stderr)
        # The plan's check passes here, and pack would ship a file nobody reviewed.
        plain = subprocess.run(["git", "diff", "--exit-code"], cwd=self.repo, capture_output=True)
        self.assertEqual(plain.returncode, 0)

    def test_a_builder_that_stages_its_change_still_fails(self):
        self.write("workflows/build/build_zz_stage.py",
                   "import subprocess\n"
                   f"with open('{OUTPUT}', 'a') as fh:\n"
                   "    fh.write('# extra\\n')\n"
                   f"subprocess.run(['git', 'add', '{OUTPUT}'], check=True)\n")
        self.commit("add a builder that stages")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"changed: {OUTPUT}", result.stderr)

    def test_a_deleted_output_fails(self):
        self.write("workflows/build/build_zz_delete.py", f"import os\nos.remove('{OUTPUT}')\n")
        self.commit("add a builder that deletes output")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"deleted: {OUTPUT}", result.stderr)

    # Edges.

    def test_builder_past_the_timeout_fails(self):
        self.write("workflows/build/build_slow.py", "import time\ntime.sleep(30)\n")
        self.commit("add a slow builder")
        result = self.check("--timeout", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("builder workflows/build/build_slow.py ran past the 1 second timeout", result.stderr)

    def test_no_builders_passes(self):
        shutil.rmtree(self.repo / "workflows")
        self.commit("no builders")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no builders match workflows/build/*.py", result.stdout)

    def test_ignored_files_written_by_a_builder_pass(self):
        self.write(".gitignore", "out/\n")
        self.write("workflows/build/build_zz_scratch.py",
                   "from pathlib import Path\nPath('out').mkdir(exist_ok=True)\n"
                   "Path('out/scratch.txt').write_text('x')\n")
        self.commit("builder writes to an ignored folder")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_a_builder_importing_a_helper_leaves_no_bytecode_behind(self):
        # Builders run with -B, so an imported helper writes no __pycache__ into the tree.
        self.write("workflows/build/helpers/fmt.py", "def upper(s):\n    return s.upper()\n")
        self.write("workflows/build/build_zz_import.py", "from helpers import fmt\nfmt.upper('x')\n")
        self.commit("builder with a helper module")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(list(self.repo.rglob("__pycache__")))

    def test_only_python_files_directly_in_the_build_folder_run(self):
        self.write("workflows/build/README.md", "not a builder\n")
        self.write("workflows/build/helpers/never_run.py", "raise SystemExit(9)\n")
        self.commit("non-builders beside the builders")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 builder(s) ran", result.stdout)

    def test_usage_errors_exit_2(self):
        missing = self.check(root=Path(self.tmp.name) / "nowhere")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("is not a folder", missing.stderr)
        plain = Path(self.tmp.name) / "plain"
        plain.mkdir()
        not_git = self.check(root=plain)
        self.assertEqual(not_git.returncode, 2)
        self.assertIn("is not a git work tree", not_git.stderr)
        subfolder = self.check(root=self.repo / "src")
        self.assertEqual(subfolder.returncode, 2)
        self.assertIn("must be the top of the work tree", subfolder.stderr)


class FixtureTests(unittest.TestCase):
    def test_the_fixture_holds_one_builder_and_its_output(self):
        builders = sorted(p.name for p in (FIXTURE / "workflows/build").glob("*.py"))
        self.assertEqual(builders, ["build_status_choices.py"])
        text = (FIXTURE / OUTPUT).read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Generated by workflows/build/build_status_choices.py"))
        self.assertIn("  - value: 100000002\n    label: Approved\n", text)


if __name__ == "__main__":
    unittest.main()
