import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lcp"))
import manifest  # noqa: E402


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "lcp").mkdir(parents=True)
        (self.root / "lcp/a.py").write_text("print('a')\n")
        (self.root / "lcp/b.py").write_text("print('b')\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_fresh_manifest_verifies(self):
        text = manifest.make(self.root)
        self.assertEqual(manifest.verify(self.root, text), [])

    def test_format_matches_sha256sum(self):
        line = manifest.make(self.root).splitlines()[0]
        digest, sep, rel = line.partition("  ")
        self.assertEqual(len(digest), 64)
        self.assertEqual(sep, "  ")
        self.assertEqual(rel, "lcp/a.py")

    def test_changed_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "lcp/a.py").write_text("print('tampered')\n")
        self.assertEqual(manifest.verify(self.root, text), ["changed: lcp/a.py"])

    def test_missing_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "lcp/b.py").unlink()
        self.assertEqual(manifest.verify(self.root, text), ["missing: lcp/b.py"])

    def test_unlisted_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "lcp/c.py").write_text("print('new')\n")
        self.assertEqual(manifest.verify(self.root, text), ["unlisted: lcp/c.py"])

    def test_bytecode_cache_is_ignored(self):
        text = manifest.make(self.root)
        (self.root / "lcp/__pycache__").mkdir()
        (self.root / "lcp/__pycache__/a.cpython-313.pyc").write_bytes(b"x")
        self.assertEqual(manifest.verify(self.root, text), [])

    def test_a_git_worktree_link_file_is_ignored(self):
        # In a git worktree (or a submodule) .git is a file, not a folder. It must never be
        # hashed: a manifest made in a worktree would list it, and sha256sum would then fail
        # in every gate job, where .git is a folder (found rehearsing the move, Build 3).
        text = manifest.make(self.root)
        (self.root / ".git").write_text("gitdir: /elsewhere/.git/worktrees/x\n")
        self.assertEqual(manifest.make(self.root), text)
        self.assertEqual(manifest.verify(self.root, text), [])

    def test_bad_manifest_line_raises(self):
        with self.assertRaises(ValueError):
            manifest.verify(self.root, "not-a-hash lcp/a.py\n")


class ScopeTests(unittest.TestCase):
    """Every file a gate job reads is hashed; tests, docs and the workflow folder are not."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel in self.hashed + self.not_hashed:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{rel}\n")

    def tearDown(self):
        self.tmp.cleanup()

    hashed = [
        "lcp/a.py", "lcp/cs-runner/run.mjs", "lcp/danger-rules.yml", "lcp/verify/bin/lcp-verify",
        "prompts/lcp-evaluate.md", "rubrics/copilot-agent.md",
        "projects/p1/trust.yml", "projects/p1/test.settings.json",
        "playwright/package-lock.json", "rulesets/main-gate.json", "templates/CODEOWNERS",
        ".github/agents/lcp-evaluator.agent.md",
    ]
    not_hashed = [
        "tests/test_a.py", "tests/fixtures/x.yml", "README.md", "pending-scripts.txt",
        "requirements-test.txt", "scripts.sha256", ".gitignore",
        ".github/workflows/lcp-gate.yml", ".github/dependabot.yml", ".github/CODEOWNERS",
        "lcp/__pycache__/a.cpython-313.pyc", ".git/HEAD",
    ]

    def test_scope(self):
        self.assertEqual(manifest.trusted_files(self.root), sorted(self.hashed))

    def test_an_unlisted_prompt_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "prompts/focus-regression.md").write_text("new focus\n")
        self.assertEqual(manifest.verify(self.root, text), ["unlisted: prompts/focus-regression.md"])

    def test_a_changed_rules_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "lcp/danger-rules.yml").write_text("floor: 0\n")
        self.assertEqual(manifest.verify(self.root, text), ["changed: lcp/danger-rules.yml"])

    def test_editing_a_test_or_the_readme_needs_no_regeneration(self):
        text = manifest.make(self.root)
        (self.root / "tests/test_a.py").write_text("changed\n")
        (self.root / "README.md").write_text("changed\n")
        (self.root / ".github/workflows/lcp-gate.yml").write_text("changed\n")
        self.assertEqual(manifest.verify(self.root, text), [])


class CommittedManifestTests(unittest.TestCase):
    def test_committed_manifest_matches_the_scripts(self):
        # If this fails, regenerate: python3 lcp/manifest.py make . > scripts.sha256
        # Regenerating is a gate-script change: reviewed daytime PR only (rule 17).
        root = Path(__file__).resolve().parents[1]
        text = (root / "scripts.sha256").read_text(encoding="utf-8")
        self.assertEqual(manifest.verify(root, text), [])


@unittest.skipUnless(shutil.which("sha256sum"), "sha256sum not on PATH (it is on the ubuntu runners)")
class Sha256sumAgreementTests(unittest.TestCase):
    """The workflow checks hashes with `sha256sum --check --strict scripts.sha256`.
    manifest.py must write a file sha256sum reads the same way (Build 1, step 4)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "lcp/sub").mkdir(parents=True)
        (self.root / "lcp/a.py").write_text("print('a')\n")
        (self.root / "lcp/sub/b.mjs").write_text("console.log('b')\n")
        (self.root / "scripts.sha256").write_text(manifest.make(self.root))

    def tearDown(self):
        self.tmp.cleanup()

    def both(self, root):
        """Return (sha256sum passes, manifest.py passes) for root."""
        result = subprocess.run(
            ["sha256sum", "--check", "--strict", "scripts.sha256"],
            cwd=root, capture_output=True, text=True,
        )
        text = (root / "scripts.sha256").read_text(encoding="utf-8")
        return result.returncode == 0, manifest.verify(root, text) == []

    def test_committed_manifest_passes_sha256sum(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(self.both(root), (True, True))

    def test_both_accept_a_fresh_manifest(self):
        self.assertEqual(self.both(self.root), (True, True))

    def test_both_reject_a_changed_script(self):
        (self.root / "lcp/a.py").write_text("print('tampered')\n")
        self.assertEqual(self.both(self.root), (False, False))

    def test_both_reject_a_missing_script(self):
        (self.root / "lcp/sub/b.mjs").unlink()
        self.assertEqual(self.both(self.root), (False, False))

    def test_only_manifest_py_catches_an_unlisted_script(self):
        # Known gap: sha256sum checks only what is listed. The committed-manifest test
        # catches an unlisted script before it reaches the release branch.
        (self.root / "lcp/c.py").write_text("print('unreviewed')\n")
        self.assertEqual(self.both(self.root), (True, False))


if __name__ == "__main__":
    unittest.main()
