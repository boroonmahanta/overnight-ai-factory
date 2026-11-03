"""Tests for lcp/pack_offline.py (Build 3, 3 November 2026).

pac is not installed here (the build plan says not to). A fake `pac` on PATH
records every call and behaves as FAKE_PAC_MODE says. So these tests prove the
wrapper's calls and its error handling, not that the real pac accepts the flags.
That waits for a stage 0 spike.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "lcp/pack_offline.py"

FAKE_PAC = f"""#!{sys.executable}
import json, os, sys, time, zipfile
from pathlib import Path
args = sys.argv[1:]
with open(os.environ["FAKE_PAC_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps({{"args": args, "cwd": os.getcwd()}}) + "\\n")
mode = os.environ.get("FAKE_PAC_MODE", "ok")
if mode == "hang":
    time.sleep(30)
if mode == "fail" or mode == "fail-in:" + Path.cwd().name:
    print("Error: the folder does not hold a solution", file=sys.stderr)
    sys.exit(3)
if args[:2] == ["solution", "pack"]:
    target = Path(args[args.index("--zipfile") + 1])
    if mode == "no-zip":
        sys.exit(0)
    if mode == "not-a-zip":
        target.write_text("not a zip")
        sys.exit(0)
    with zipfile.ZipFile(target, "w") as z:
        z.writestr("solution.xml", "<ImportExportXml/>")
"""


class PackOfflineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name)
        self.bin = self.work / "bin"
        self.bin.mkdir()
        pac = self.bin / "pac"
        pac.write_text(FAKE_PAC, encoding="utf-8")
        pac.chmod(0o755)
        self.empty_bin = self.work / "empty-bin"
        self.empty_bin.mkdir()
        self.log = self.work / "pac-calls.jsonl"
        (self.work / "pr/src/Other").mkdir(parents=True)
        (self.work / "pr/src/Other/Solution.yml").write_text("SolutionManifest: {}\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_pack(self, *args, mode="ok", pac_on_path=True):
        env = dict(os.environ, FAKE_PAC_LOG=str(self.log), FAKE_PAC_MODE=mode,
                   PATH=str(self.bin if pac_on_path else self.empty_bin))
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *args],
                              cwd=self.work, env=env, capture_output=True, text=True)

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def solution(self, mode="ok", **kw):
        return self.run_pack("solution", "--source", "pr/src", "--out", "out", mode=mode, **kw)

    def agents(self, mode="ok", **kw):
        return self.run_pack("agents", "--root", "pr/agents", mode=mode, **kw)

    def make_workspaces(self, *names):
        for name in names:
            (self.work / "pr/agents" / name).mkdir(parents=True)

    # pac solution pack

    def test_solution_packs_unmanaged_then_managed_with_the_plans_flags(self):
        result = self.solution()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([c["args"] for c in self.calls()], [
            ["solution", "pack", "--zipfile", "out/solution_unmanaged.zip", "--folder", "pr/src",
             "--packagetype", "Unmanaged"],
            ["solution", "pack", "--zipfile", "out/solution_managed.zip", "--folder", "pr/src",
             "--packagetype", "Managed"],
        ])
        for name in ("solution_unmanaged.zip", "solution_managed.zip"):
            self.assertTrue(zipfile.is_zipfile(self.work / "out" / name), name)
        self.assertIn("packed pr/src into out/solution_unmanaged.zip and solution_managed.zip",
                      result.stdout)

    def test_pac_missing_is_a_clear_error(self):
        result = self.solution(pac_on_path=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pac was not found on PATH", result.stderr)
        self.assertIn("dotnet tool install --global Microsoft.PowerApps.CLI.Tool", result.stderr)

    def test_pac_failure_names_the_package_and_shows_pacs_output(self):
        result = self.solution(mode="fail")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unmanaged solution: `pac solution pack --zipfile out/solution_unmanaged.zip",
                      result.stderr)
        self.assertIn("failed with exit code 3", result.stderr)
        self.assertIn("Error: the folder does not hold a solution", result.stderr)
        self.assertIn("Managed solution:", result.stderr)  # both calls tried, both reported

    def test_zero_exit_without_a_zip_fails(self):
        result = self.solution(mode="no-zip")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unmanaged solution: pac exited 0 but wrote no zip at out/solution_unmanaged.zip",
                      result.stderr)

    def test_a_stale_zip_cannot_pass_for_a_new_one(self):
        (self.work / "out").mkdir()
        with zipfile.ZipFile(self.work / "out/solution_managed.zip", "w") as z:
            z.writestr("old.xml", "from an earlier run")
        result = self.solution(mode="no-zip")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Managed solution: pac exited 0 but wrote no zip", result.stderr)
        self.assertFalse((self.work / "out/solution_managed.zip").exists())

    def test_zero_exit_with_a_file_that_is_not_a_zip_fails(self):
        result = self.solution(mode="not-a-zip")
        self.assertEqual(result.returncode, 1)
        self.assertIn("out/solution_unmanaged.zip is not a zip file", result.stderr)

    def test_missing_or_empty_source_fails_before_pac_runs(self):
        (self.work / "pr/src/Other/Solution.yml").unlink()
        (self.work / "pr/src/Other").rmdir()
        empty = self.solution()
        self.assertEqual(empty.returncode, 1)
        self.assertIn("no solution source to pack: pr/src is missing or empty", empty.stderr)
        (self.work / "pr/src").rmdir()
        missing = self.solution()
        self.assertEqual(missing.returncode, 1)
        self.assertIn("pr/src is missing or empty", missing.stderr)
        self.assertEqual(self.calls(), [])

    def test_a_hung_pac_is_stopped_at_the_timeout(self):
        result = self.run_pack("solution", "--source", "pr/src", "--out", "out", "--timeout", "1",
                               mode="hang")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ran past the 1 second timeout", result.stderr)

    # pac copilot pack

    def test_agents_packs_each_workspace_in_name_order_from_inside_it(self):
        self.make_workspaces("b-helpdesk", "a-intake", ".hidden")
        (self.work / "pr/agents/README.md").write_text("not a workspace\n")
        result = self.agents()
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = self.calls()
        self.assertEqual([c["args"] for c in calls], [["copilot", "pack"], ["copilot", "pack"]])
        self.assertEqual([Path(c["cwd"]).name for c in calls], ["a-intake", "b-helpdesk"])
        self.assertIn("packed 2 workspace(s) under pr/agents", result.stdout)

    def test_no_agents_folder_passes_without_needing_pac(self):
        result = self.agents(pac_on_path=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no Copilot Studio workspaces under pr/agents; nothing to pack", result.stdout)
        (self.work / "pr/agents").mkdir()
        self.assertEqual(self.agents(pac_on_path=False).returncode, 0)

    def test_a_failing_workspace_is_named_and_the_others_still_pack(self):
        self.make_workspaces("a-intake", "b-helpdesk")
        result = self.agents(mode="fail-in:a-intake")
        self.assertEqual(result.returncode, 1)
        self.assertIn("workspace pr/agents/a-intake: `pac copilot pack` failed with exit code 3",
                      result.stderr)
        self.assertNotIn("b-helpdesk", result.stderr)
        self.assertEqual([Path(c["cwd"]).name for c in self.calls()], ["a-intake", "b-helpdesk"])

    def test_agents_with_pac_missing_is_a_clear_error(self):
        self.make_workspaces("a-intake")
        result = self.agents(pac_on_path=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pac was not found on PATH", result.stderr)

    def test_usage_errors_exit_2(self):
        self.assertEqual(self.run_pack().returncode, 2)
        self.assertEqual(self.run_pack("solution", "--out", "out").returncode, 2)


if __name__ == "__main__":
    unittest.main()
