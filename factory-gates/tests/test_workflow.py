"""Shape tests for .github/workflows/lcp-gate.yml (Build 1, 3 November 2026).

These prove the file's shape against the plan's rules: credentials, hash checks,
script calls and pins. They do not prove it runs on GHE.com. Nothing does yet.

Needs PyYAML, test only (decision D3):
  python3 -m pip install --require-hashes -r requirements-test.txt
"""
import json
import posixpath
import re
import unittest
from pathlib import Path

try:
    import yaml
except ImportError as err:  # fail loudly, never skip: a skipped gate test hides a gap
    raise ImportError(
        "tests/test_workflow.py needs PyYAML (test only, decision D3). Run: "
        "python3 -m pip install --require-hashes -r requirements-test.txt"
    ) from err

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/lcp-gate.yml"
PENDING = ROOT / "pending-scripts.txt"

GATE_PATH = "gate"  # where every job checks out the gate repo
VERIFY_CMD = "sha256sum --check --strict scripts.sha256"
# build runs PR code, so it holds no gate token and cannot check out the gate repo.
# map uploads the scripts build needs, after its hash check, under this name (Build 3).
BUILD_ARTIFACT = "gate-build-scripts"
FED_BY_ARTIFACT = {"build"}

# A gate script call: lcp/x.py from inside gate/, gate/lcp/x.py from the workspace,
# ../gate/lcp/x.py from inside pr/. Anchored so pr/lcp/x.py or $PWD/lcp/... do not match.
SCRIPT_REF = re.compile(r"(?:^|[\s\"'=(])((?:\.\./)*(?:gate/)?lcp/[\w./-]+\.(?:py|mjs|sh))")
ACTION_REF = re.compile(r"^[\w.-]+/[\w.-]+(?:/[\w./-]+)?@([\w.-]+)$")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
MOVING_REFS = {"main", "master", "latest", "head", "dev", "develop", "trunk"}


def load_workflow() -> dict:
    with WORKFLOW.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def pending_scripts() -> list[str]:
    lines = PENDING.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.lstrip().startswith("#")]


def script_refs(step: dict) -> list[str]:
    """Resolve each gate script a step calls to a path inside the gate checkout."""
    run = step.get("run") or ""
    workdir = step.get("working-directory") or "."
    return [posixpath.normpath(posixpath.join(workdir, m.group(1))) for m in SCRIPT_REF.finditer(run)]


def is_gate_checkout(step: dict) -> bool:
    w = step.get("with") or {}
    return (
        str(step.get("uses", "")).startswith("actions/checkout@")
        and w.get("repository") == "${{ env.GATE_REPO }}"
        and w.get("ref") == "release"
        and w.get("path") == GATE_PATH
    )


def is_hash_verify(step: dict) -> bool:
    return step.get("working-directory") == GATE_PATH and (step.get("run") or "").strip() == VERIFY_CMD


def is_app_token(step: dict) -> bool:
    return str(step.get("uses", "")).startswith("actions/create-github-app-token@")


def is_build_scripts_download(step: dict) -> bool:
    return (
        str(step.get("uses", "")).startswith("actions/download-artifact@")
        and (step.get("with") or {}).get("name") == BUILD_ARTIFACT
    )


def is_build_scripts_upload(step: dict) -> bool:
    return (
        str(step.get("uses", "")).startswith("actions/upload-artifact@")
        and (step.get("with") or {}).get("name") == BUILD_ARTIFACT
    )


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wf = load_workflow()
        cls.jobs = cls.wf["jobs"]

    def all_steps(self):
        for job_name, job in self.jobs.items():
            for index, step in enumerate(job.get("steps", [])):
                yield job_name, index, step

    def test_file_parses_and_has_the_six_jobs(self):
        self.assertEqual(
            list(self.jobs), ["map", "locks", "build", "static", "verify-in-test", "danger"]
        )
        self.assertEqual(self.wf["env"]["GATE_REPO"], "getai/factory-gates")

    def test_triggers_have_no_filters(self):
        # Required workflows ignore branches, paths and types filters (plan 5.7). Do not add any.
        on = self.wf.get("on", self.wf.get(True))  # PyYAML reads a bare `on` key as True
        self.assertEqual(set(on), {"pull_request", "merge_group"})
        for trigger, config in on.items():
            self.assertFalse(config, f"{trigger} has filters: {config}")

    def test_top_level_permissions_are_empty(self):
        self.assertEqual(self.wf["permissions"], {})

    def test_only_verify_in_test_can_request_an_oidc_token(self):
        with_oidc = {
            name for name, job in self.jobs.items()
            if (job.get("permissions") or {}).get("id-token") not in (None, "none")
        }
        self.assertEqual(with_oidc, {"verify-in-test"})
        self.assertEqual(self.jobs["verify-in-test"]["permissions"]["id-token"], "write")

    def test_build_runs_pr_code_with_no_credentials(self):
        # Rule 5: build runs the PR's builders, so it holds nothing.
        build = self.jobs["build"]
        self.assertEqual(build["permissions"], {"contents": "read"})
        self.assertNotIn("environment", build)
        text = json.dumps(build)
        for banned in ("secrets.", "github.token", "id-token", "create-github-app-token", "azure/login"):
            self.assertNotIn(banned, text, f"build mentions {banned}")

    def test_secrets_only_feed_the_gate_app_token_steps(self):
        for name, job in self.jobs.items():
            self.assertNotIn("secrets.", json.dumps(job.get("env", {})), f"{name} job env")
        for name, index, step in self.all_steps():
            if "secrets." not in json.dumps(step):
                continue
            self.assertTrue(is_app_token(step), f"{name} step {index} uses a secret outside a token step")
            others = {k: v for k, v in step["with"].items() if k != "private-key"}
            self.assertNotIn("secrets.", json.dumps(others), f"{name} step {index}")
            self.assertNotIn("secrets.", json.dumps(step.get("env", {})), f"{name} step {index}")

    def test_every_checkout_drops_its_credentials(self):
        for name, index, step in self.all_steps():
            if str(step.get("uses", "")).startswith("actions/checkout@"):
                self.assertIs(step["with"].get("persist-credentials"), False, f"{name} step {index}")

    def test_every_job_that_runs_a_gate_script_verifies_hashes_first(self):
        jobs_with_scripts = set()
        for name, job in self.jobs.items():
            steps = job.get("steps", [])
            script_steps = [i for i, s in enumerate(steps) if script_refs(s)]
            if not script_steps:
                continue
            jobs_with_scripts.add(name)
            if name in FED_BY_ARTIFACT:
                # No gate checkout here: the scripts arrive from map, which checked them.
                # test_build_gets_its_scripts_from_map_after_the_hash_check covers map's side.
                downloads = [i for i, s in enumerate(steps) if is_build_scripts_download(s)]
                self.assertTrue(downloads, f"{name}: runs gate scripts but never downloads them")
                self.assertLess(downloads[0], script_steps[0], f"{name}: a script runs before the download")
                self.assertFalse([s for s in steps if is_gate_checkout(s)], f"{name}: gate checkout")
                continue
            checkouts = [i for i, s in enumerate(steps) if is_gate_checkout(s)]
            verifies = [i for i, s in enumerate(steps) if is_hash_verify(s)]
            self.assertTrue(checkouts, f"{name}: no gate checkout at {GATE_PATH}/")
            self.assertTrue(verifies, f"{name}: no hash check")
            self.assertLess(checkouts[0], verifies[0], f"{name}: hash check before the gate checkout")
            self.assertLess(verifies[0], script_steps[0], f"{name}: a gate script runs before the hash check")
        # Guard against the check passing by finding nothing.
        self.assertEqual(jobs_with_scripts, {"map", "locks", "build", "static", "verify-in-test", "danger"})

    def test_build_gets_its_scripts_from_map_after_the_hash_check(self):
        build_steps = self.jobs["build"]["steps"]
        called = sorted({ref for s in build_steps for ref in script_refs(s)})
        self.assertEqual(called, ["gate/lcp/check_builders.py", "gate/lcp/pack_offline.py"])
        self.assertIn("map", self.jobs["build"]["needs"])

        # map uploads exactly those scripts, after its hash check, and nothing else.
        map_steps = self.jobs["map"]["steps"]
        uploads = [i for i, s in enumerate(map_steps) if is_build_scripts_upload(s)]
        verifies = [i for i, s in enumerate(map_steps) if is_hash_verify(s)]
        self.assertEqual(len(uploads), 1)
        self.assertLess(verifies[0], uploads[0], "map uploads the scripts before checking their hashes")
        upload = map_steps[uploads[0]]["with"]
        self.assertEqual(sorted(upload["path"].split()), called)
        self.assertEqual(upload["if-no-files-found"], "error")
        self.assertEqual(upload["retention-days"], 1)
        other_uploads = [s for s in map_steps if str(s.get("uses", "")).startswith("actions/upload-artifact@")]
        self.assertEqual(len(other_uploads), 1, "map uploads something besides the build scripts")

        # build downloads them from this run only, into gate/lcp/, outside the PR tree at pr/.
        downloads = [s for s in build_steps if is_build_scripts_download(s)]
        self.assertEqual(len(downloads), 1)
        self.assertEqual(downloads[0]["with"], {"name": BUILD_ARTIFACT, "path": f"{GATE_PATH}/lcp"})
        pr_checkout = build_steps[0]
        self.assertTrue(str(pr_checkout.get("uses", "")).startswith("actions/checkout@"))
        self.assertEqual(pr_checkout["with"].get("path"), "pr")

        # No other job takes the build scripts.
        for name, job in self.jobs.items():
            if name != "build":
                self.assertFalse([s for s in job.get("steps", []) if is_build_scripts_download(s)], name)

    def test_build_runs_the_tested_scripts_not_inline_commands(self):
        runs = {s.get("name"): s.get("run") or "" for s in self.jobs["build"]["steps"] if s.get("run")}
        self.assertEqual(
            runs["Run every builder, then fail on any diff"],
            "python3 -I gate/lcp/check_builders.py --root pr",
        )
        self.assertEqual(
            runs["Pack the solution offline (YAML source format)"],
            "python3 -I gate/lcp/pack_offline.py solution --source pr/src --out out",
        )
        self.assertEqual(
            runs["Pack Copilot Studio workspaces offline"],
            "python3 -I gate/lcp/pack_offline.py agents --root pr/agents",
        )
        inline = "\n".join(runs.values())
        for banned in ("git diff", "pac solution", "pac copilot", "workflows/build"):
            self.assertNotIn(banned, inline, f"build runs {banned} inline")
        # The zips land in out/ at the workspace root, where static downloads them.
        upload = next(s for s in self.jobs["build"]["steps"]
                      if str(s.get("uses", "")).startswith("actions/upload-artifact@"))
        self.assertEqual(upload["with"]["name"], "packed")
        self.assertEqual(upload["with"]["path"], "out/")

    def test_every_script_call_resolves_into_the_gate_checkout(self):
        for name, index, step in self.all_steps():
            for ref in script_refs(step):
                self.assertTrue(ref.startswith(GATE_PATH + "/lcp/"), f"{name} step {index}: {ref}")

    def test_every_script_called_exists_or_is_pending(self):
        pending = set(pending_scripts())
        for name, index, step in self.all_steps():
            for ref in script_refs(step):
                rel = ref[len(GATE_PATH) + 1:]
                self.assertTrue(
                    (ROOT / rel).is_file() or rel in pending,
                    f"{name} step {index} calls {rel}: not in lcp/ and not in pending-scripts.txt",
                )

    def test_pending_list_holds_only_unwritten_scripts_still_called(self):
        listed = pending_scripts()
        self.assertEqual(len(listed), len(set(listed)), "duplicate line in pending-scripts.txt")
        called = {ref[len(GATE_PATH) + 1:] for _, _, step in self.all_steps() for ref in script_refs(step)}
        for rel in listed:
            self.assertFalse((ROOT / rel).exists(), f"{rel} is written: delete it from pending-scripts.txt")
            self.assertIn(rel, called, f"{rel} is no longer called: delete it from pending-scripts.txt")

    def test_map_uses_the_tested_lane_script_and_keeps_its_outputs(self):
        job = self.jobs["map"]
        self.assertEqual(job["outputs"], {
            "lane": "${{ steps.lane.outputs.lane }}",
            "story": "${{ steps.lane.outputs.story }}",
        })
        lane_step = next(s for s in job["steps"] if s.get("id") == "lane")
        self.assertEqual(script_refs(lane_step), ["gate/lcp/lane_map.py"])
        self.assertNotIn("BASH_REMATCH", lane_step["run"])
        self.assertEqual(set(lane_step["env"]), {"HEAD_REF", "ALLOWED"})

    def test_locks_uses_the_tested_script_not_inline_git_diff(self):
        job = self.jobs["locks"]
        pr_checkout = job["steps"][0]
        self.assertEqual(pr_checkout["with"].get("path"), "pr")
        self.assertEqual(pr_checkout["with"].get("fetch-depth"), 0)  # BASE...HEAD needs history
        check = job["steps"][-1]
        self.assertEqual(script_refs(check), ["gate/lcp/check_protected_paths.py"])
        self.assertEqual(check["working-directory"], "pr")
        self.assertIn('--lane "$LANE"', check["run"])
        self.assertIn('--base "$BASE_SHA"', check["run"])
        self.assertNotIn("git diff", json.dumps(job))

    def test_every_action_is_pinned_to_a_version(self):
        for name, index, step in self.all_steps():
            uses = step.get("uses")
            if uses is None:
                continue
            match = ACTION_REF.match(uses)
            self.assertIsNotNone(match, f"{name} step {index}: {uses} has no version")
            self.assertNotIn(match.group(1).lower(), MOVING_REFS, f"{name} step {index}: {uses}")

    def test_every_action_is_pinned_to_a_commit_sha_with_its_version_beside_it(self):
        # A tag such as @v5 can be moved to other code; a full commit SHA cannot
        # (decided by Boroon, 3 November 2026). The "# vX.Y.Z" comment is what Dependabot
        # reads and rewrites, so it must sit on the same line as the pin.
        for name, index, step in self.all_steps():
            uses = step.get("uses")
            if uses is not None:
                self.assertRegex(ACTION_REF.match(uses).group(1), FULL_SHA, f"{name} step {index}")
        uses_lines = [ln for ln in WORKFLOW.read_text(encoding="utf-8").splitlines() if "uses:" in ln]
        self.assertTrue(uses_lines)
        for line in uses_lines:
            self.assertRegex(line, r"@[0-9a-f]{40} # v\d+\.\d+\.\d+\b", f"no version comment: {line.strip()}")


if __name__ == "__main__":
    unittest.main()
