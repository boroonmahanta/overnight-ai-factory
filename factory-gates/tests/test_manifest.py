import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gate" / "lcp"))
import manifest  # noqa: E402


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "gate/lcp").mkdir(parents=True)
        (self.root / "gate/lcp/a.py").write_text("print('a')\n")
        (self.root / "gate/lcp/b.py").write_text("print('b')\n")

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
        self.assertEqual(rel, "gate/lcp/a.py")

    def test_changed_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "gate/lcp/a.py").write_text("print('tampered')\n")
        self.assertEqual(manifest.verify(self.root, text), ["changed: gate/lcp/a.py"])

    def test_missing_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "gate/lcp/b.py").unlink()
        self.assertEqual(manifest.verify(self.root, text), ["missing: gate/lcp/b.py"])

    def test_unlisted_file_is_reported(self):
        text = manifest.make(self.root)
        (self.root / "gate/lcp/c.py").write_text("print('new')\n")
        self.assertEqual(manifest.verify(self.root, text), ["unlisted: gate/lcp/c.py"])

    def test_bytecode_cache_is_ignored(self):
        text = manifest.make(self.root)
        (self.root / "gate/lcp/__pycache__").mkdir()
        (self.root / "gate/lcp/__pycache__/a.cpython-313.pyc").write_bytes(b"x")
        self.assertEqual(manifest.verify(self.root, text), [])

    def test_bad_manifest_line_raises(self):
        with self.assertRaises(ValueError):
            manifest.verify(self.root, "not-a-hash gate/lcp/a.py\n")


if __name__ == "__main__":
    unittest.main()


class CommittedManifestTests(unittest.TestCase):
    def test_committed_manifest_matches_the_scripts(self):
        # If this fails, regenerate: python3 gate/lcp/manifest.py make . > scripts.sha256
        # Regenerating is a gate-script change: reviewed daytime PR only (rule 17).
        root = Path(__file__).resolve().parents[1]
        text = (root / "scripts.sha256").read_text(encoding="utf-8")
        self.assertEqual(manifest.verify(root, text), [])
