# Stage 1 build plan: the gate, offline parts

Written 3 November 2026 (Session 5, planning only). Approved in outline by Boroon the same day: pull in slice 1, fix the rename gap in the plan too, and do the build in separate sessions to save context.

This covers the parts of Stage 1 (plan section 11.2) that need no tenant and no real GitHub org. Everything here lives in `factory-gates/`, staged in this repo until `getai/factory-gates` exists.

## Where things stand

- Slice 1 is done: `lane_map.py`, `check_protected_paths.py`, `manifest.py`, `scripts.sha256`, 23 tests. Merged to `main` by PR 10.
- **Build 1 is done** (Session 6, 3 November 2026, branch `claude/brave-davinci-0d5ssc`): the workflow file, `map` and `locks` on the tested scripts, `pending-scripts.txt`, PyYAML pinned for tests, 24 new tests (47 in all), the plan's `map` and `locks` jobs fixed. Also decided by Boroon the same day: actions pinned to full commit IDs with Dependabot to keep them fresh, and the hash manifest widened from scripts to every file a gate job reads. Details in `docs/progress.md` and `factory-gates/README.md`.
- **Build 1 merged** by PR 11 on 3 November 2026.
- **Build 2 is done** (Session 7, 3 November 2026, branch `claude/eager-goldberg-gj0iqg`): the four rulesets as JSON, `templates/CODEOWNERS`, `make_rulesets.py`, `audit_bypass.py`, 65 new tests (112 in all), manifest regenerated. Nothing applied. Choices to confirm are listed in `factory-gates/README.md` under "Rulesets and CODEOWNERS".
- **Build 2 merged** by PR 12 on 3 November 2026.
- **Build 3 is done** (Session 8, 3 November 2026, branch `claude/elegant-wozniak-316hdv`): `check_builders.py`, `pack_offline.py` (the `pac` wrapper, untested against the real `pac`), the fixture project, the `build` job on the scripts, 29 new tests (141 in all), manifest regenerated, and a fix to `manifest.py` for git worktrees. `map` hands the two scripts to `build` as an artifact, because `build` holds no credentials and cannot check out the private gate repo. Choices to confirm and the steps to move `factory-gates/` to GHE.com are in `factory-gates/README.md`.
- **Layout change in Build 1:** the scripts moved from `factory-gates/gate/lcp/` to `factory-gates/lcp/`. The workflow checks the gate repo out at `gate/`, so it calls them as `gate/lcp/<name>.py`. Below, `gate/lcp/x.py` means the workflow path; the file lives at `factory-gates/lcp/x.py`.
- Tests run with `cd factory-gates && python3 -m pip install --require-hashes -r requirements-test.txt` (once), then `python3 -B -m unittest discover -s tests`.

## How to start each build session

1. Start from the branch that holds this plan, or from `main` once Boroon has merged it. Check `factory-gates/` exists first.
2. Read `CLAUDE.md`, `docs/progress.md`, this file and `factory-gates/README.md`.
3. Read only the plan lines named for that session. Do not load whole sources.
4. Run the tests before changing anything (141 after Build 3).
5. End as usual: progress entry, commit, push, no pull request unless asked.

## Decisions before Build 1

D1, D2 and D3 decided by Boroon on 3 November 2026: the recommended options in each case. Build 1 can start.

**D1. How `map` and `locks` get our scripts.** Plan lines 1618 to 1671. Both jobs hold no credentials, and the gate repo is private, so they cannot check out `gate/lcp/*.py`. Options:

| Option | What | Trade-off |
|---|---|---|
| A (**chosen**, Boroon, 3 November 2026) | Give `map` and `locks` the same read-only gate App token that `static` uses, check out the gate repo, verify `scripts.sha256`, then run the scripts | Uses the tested scripts. Safe under rule 5 because neither job runs PR code (`locks` only runs `git diff`). Two more jobs hold the reader key |
| B | Keep the inline bash, add `--no-renames` to `locks`. The Python scripts become the reference and their tests check the bash matches | No new credentials. Two copies of the logic that can drift |

**D2. The ~20 scripts the workflow calls that do not exist yet** (for example `check_manifest.py`, `lint_logic_apps.py`, `merge_danger_floor.py`). **Decided (Boroon, 3 November 2026):** a `pending-scripts.txt` list in `factory-gates/`. A test fails if the workflow calls a script that is neither in `gate/` nor on that list. Writing a script removes it from the list. No stub files, so nothing fake is hashed.

**D3. A YAML parser for the tests.** Python's standard library has none. **Decided (Boroon, 3 November 2026):** PyYAML, pinned with a hash, for tests only, in `factory-gates/requirements-test.txt`. The gate scripts themselves stay free of packages.

## Build 1: the workflow file, and the plan fix (done 3 November 2026)

Read: plan lines 1563 to 2058 (Appendix A), 622 to 665 (section 5.7). (Line numbers as they were before Build 1.)

1. Copy the Appendix A YAML verbatim to `factory-gates/.github/workflows/lcp-gate.yml`. First commit is the plain copy, so later diffs show every change.
2. `map`: give it the read-only gate App token, check out the gate repo, verify hashes, call `lane_map.py` (D1 option A). Keep its outputs `lane` and `story`.
3. `locks`: same pattern, call `check_protected_paths.py` (D1 option A). This closes the rename gap.
4. Make the hash check run before the first trusted script in every job that runs one. Use `manifest.py` or keep `sha256sum --check --strict`, whichever matches `scripts.sha256`'s format. Check both agree.
5. Leave `verify-in-test` and `danger` as written, with a header comment saying they are untested and wait for the Stage 0 spikes.
6. Tests in `factory-gates/tests/test_workflow.py`:
   - The file parses.
   - Top-level `permissions` is empty.
   - Only `verify-in-test` has `id-token: write`.
   - `build` has `contents: read` only, no secrets, no App token.
   - Every job that runs a `gate/lcp/` script verifies hashes first.
   - Every script called is in `gate/` or `pending-scripts.txt` (D2).
   - Every action is pinned to a version. Note: the plan pins to tags such as `@v5`, not commit SHAs. Flag this as a finding and do not change it without Boroon.
7. Regenerate `scripts.sha256`.
8. **Plan fix (approved 3 November 2026):** edit the `locks` job in `docs/sources/plan-v3.1.md` Appendix A to match. Replace the inline check with the script call and the gate checkout (D1 option A). Add one line to the decision log (section 14) and note it in `factory-gates/README.md`.

Done when: all tests pass, including the new ones. The test with `--no-renames` removed still fails. The plan's `locks` job no longer misses renames.

## Build 2: rulesets and CODEOWNERS as files (done 3 November 2026)

Read: plan lines 641 to 650 (rulesets, section 5.7 part 3), 2108 to 2245 (Appendix B, for `trust.yml` and CODEOWNERS by floor, skim only). Line numbers as at the end of Build 1.

1. Four JSON files in `factory-gates/rulesets/`, in GitHub's REST ruleset format: `main-gate.json`, `integration-gate.json`, `protected-paths.json`, `factory-required-workflows.json`. Settings as plan section 5.7.
2. `factory-gates/templates/CODEOWNERS` for project repos. Protected paths go to `@acceptance-owners` or the platform team.
3. One source for protected paths. `protected-paths.json` is generated from the list in `check_protected_paths.py` by a small `gate/lcp/make_rulesets.py`. A test fails if the committed JSON is stale, the same way the manifest test works.
4. `gate/lcp/audit_bypass.py`: reads a ruleset JSON and fails if a bypass list names an App, an integration, a machine account, the write role or Copilot (rule 6). `main-gate` must have an empty bypass list. This is the offline half of the plan's nightly bypass audit.
5. Tests for both scripts. Regenerate `scripts.sha256`.
6. Not applied anywhere. Applying needs the real org on GHE.com.

Done when: all tests pass. Seeded bad files fail as expected: a stale ruleset, Copilot in a bypass list, and a protected path missing from CODEOWNERS.

## Build 3: the offline `build` job checks (done 3 November 2026)

Read: plan lines 1718 to 1762 (the `build` job, as at the end of Build 1), section 5.6 only if needed (`grep -n '^### 5.6' docs/sources/plan-v3.1.md`).

1. `gate/lcp/check_builders.py`: runs every `workflows/build/*.py`, then fails on `git diff --exit-code`. It runs PR code, so it has no credentials (the job stays as it is). It is a gate-repo script so the logic is tested, but it is only as trusted as the job it runs in.
2. A small fixture project under `factory-gates/tests/fixtures/` with one builder and its output. Tests: matching output passes, hand-edited output fails, a builder that crashes fails.
3. `pac solution pack` and `pac copilot pack`: wrap the calls in a script with clear errors. Do not install `pac` here. The call itself stays `[untested]` until a Stage 0 spike runs it.
4. Update the workflow's `build` job to call the script. Regenerate `scripts.sha256`.

Done when: all tests pass. The `build` job still has no credentials (the Build 1 test proves it).

How it went: all three done. One gap in this plan: a job with no credentials cannot check out the private gate repo, so `map` (which already holds the reader token and checks the hashes) uploads `check_builders.py` and `pack_offline.py` as a one-day artifact for `build`. The drift check also fails on an uncommitted new output file, which `git diff --exit-code` alone misses. Both are listed in `factory-gates/README.md` for Boroon to confirm.

## Not in these three sessions

- Anything needing a tenant or the real org: OIDC with `pac` (spike 0.2), import to Test, Playwright, verifiers, `factory-test` setup, applying rulesets.
- The rest of Stage 1: Spec Kit 1.2 presets (`getai-lcp`), `glossary.md` and `docs/adr/` templates, the Playwright kit v0, locked scenario conventions, mining 20 human sessions. **Plan these in a separate planning session.**
- Stage 1's exit test ("a seeded edit to `tests/acceptance/` is blocked by the push ruleset and, with the ruleset off, by the `locks` job") can only be half met offline. The `locks` half is covered by tests. The ruleset half waits for the org.

## Risks

- The YAML is the plan's untested starting point. Our tests prove its shape, not that it runs on GHE.com.
- Required workflows ignore `branches`, `paths` and `types` filters (plan section 5.7). Do not add any.
- Action tags, not SHAs (Build 1 step 6). Raised as a finding and settled the same day: `factory-gates` pins to full commit IDs; the plan's YAML keeps the tags for readability.
- `rulesets/` and `templates/` are hashed into `scripts.sha256` (done in Build 2). Regenerate the manifest after any change to them.
