# factory-gates (staging copy)

This folder is the first build of the gate repo, `getai/factory-gates` in the plan. It is staged inside the planning repo until that repo exists. Move the contents there as they are: this folder's root becomes the repo root (`lcp/`, `scripts.sha256`, `.github/`, `tests/` and the rest), on the protected `release` branch.

Status: **slice 1, Build 1 and Build 2 done, tested locally only.** Nothing here has run on GHE.com or a Power Platform tenant. The workflow's shape is tested. Whether it runs is not. The rulesets are files, not applied anywhere.

## What is here

| File | What it does | Plan |
|---|---|---|
| `.github/workflows/lcp-gate.yml` | The gate workflow. Plan Appendix A, with `map` and `locks` changed to run the tested scripts (Build 1). Every action is pinned to a full commit ID, with the version as a comment | Appendix A |
| `.github/dependabot.yml` | Asks Dependabot to open a weekly pull request when an action pin has a newer release. It rewrites the ID and the version comment together. A human merges by day (rule 17). Untested on GHE.com | |
| `lcp/lane_map.py` | Maps `agent/<lane>/<ado-id>-<attempt>` to a lane and a story. Anything else maps to `none`. An unknown lane fails. Run by `map` | Appendix A, job `map` |
| `lcp/check_protected_paths.py` | Fails an agent PR that changes a protected path (tests, locked scenarios, specs, glossary, ADRs, standards, `.github/`, `.claude/`, scripts, deploy). One list. Run by `locks` | Appendix A, job `locks`; rule 17 |
| `lcp/manifest.py` | Makes and checks `scripts.sha256`. Fails on a changed, missing or unlisted file | Appendix A header rules; stage 1 "trusted scripts with a hash manifest" |
| `lcp/make_rulesets.py` | Generates `rulesets/protected-paths.json` from the one path list in `check_protected_paths.py`, and checks `templates/CODEOWNERS` owns every protected path. `check` fails if either is behind (Build 2) | Section 5.7 part 3 |
| `lcp/audit_bypass.py` | Reads ruleset JSON and fails if a bypass list names anything but a team: an App (Copilot is one), a deploy key, a repository role or the org admin role. `main-gate` must have an empty list. The offline half of the nightly bypass audit (Build 2) | Section 5.7 part 3; rule 6 |
| `rulesets/` | The four rulesets in GitHub's REST format: `main-gate.json`, `integration-gate.json`, `protected-paths.json` (generated), `factory-required-workflows.json`. Not applied anywhere | Section 5.7 part 3 |
| `templates/CODEOWNERS` | CODEOWNERS for a project repo. Protected paths go to `@getai/acceptance-owners` or `@getai/platform-team` | Section 5.7; 5.10 for rung L2 |
| `scripts.sha256` | The manifest, in `sha256sum` format, of every file a gate job reads. Today: the five scripts, the four rulesets and the CODEOWNERS template. Prompts, rubrics, agents, rules and project settings join it as they are written | |
| `pending-scripts.txt` | The 20 scripts the workflow calls that are not written yet (decision D2). Delete a line when you write the script | |
| `requirements-test.txt` | PyYAML 6.0.3, pinned by hash, for tests only (decision D3). The scripts in `lcp/` use the standard library only | |
| `tests/` | 84 tests. Real git repos for the protected-path check. `test_workflow.py` checks the workflow's shape. `test_make_rulesets.py` and `test_audit_bypass.py` check the rulesets and CODEOWNERS, with seeded bad copies | |

## Layout: why `lcp/` is at the root

Every job checks this repo out at `gate/` and calls `gate/lcp/<name>.py`. It runs `sha256sum --check --strict scripts.sha256` inside `gate/`. Plan C.5 also names `factory-gates/lcp/verify/`. So `lcp/` sits at the repo root. Slice 1 had the scripts at `gate/lcp/`, which would have made the calls resolve to `gate/gate/lcp/`. Build 1 moved them. A pro-code gate would sit beside it as `pcp/` with its own `pcp-gate.yml` (a proposal, not decided).

## What is hashed

Everything a gate job reads from this repo (decided by Boroon, 3 November 2026): scripts, prompts, rubrics, `.github/agents/*.agent.md`, `danger-rules.yml`, `projects/*/trust.yml` and settings, the Playwright kit's lockfile. A new folder is hashed unless `manifest.py` lists it as not hashed. Not hashed, because no job reads them: `tests/`, `README.md`, `pending-scripts.txt`, `requirements-test.txt`, the manifest itself, and `.github/` apart from `.github/agents/` (the workflow is the root of trust and is pinned by the required-workflow ruleset; Dependabot edits its pins by PR).

The workflow checks hashes with `sha256sum --check --strict`, which catches a changed or missing file but not an unlisted one. `manifest.py verify` catches all three, and `test_committed_manifest_matches_the_scripts` runs it, so an unlisted file fails this repo's tests before it reaches `release`. A job only ever runs files the workflow names, and all of those are listed. Tests prove the two tools agree on changed and missing files.

## Running the tests

```bash
cd factory-gates
python3 -m pip install --require-hashes -r requirements-test.txt
python3 -B -m unittest discover -s tests
```

Python 3.11 or later. Expect `OK`. Without PyYAML, `test_workflow.py` fails to import on purpose (it does not skip), and the other tests still run.

After any change to a hashed file, regenerate the manifest: `python3 lcp/manifest.py make . > scripts.sha256`. A test fails if you forget. After any change to the protected path list, regenerate the ruleset too: `python3 lcp/make_rulesets.py make .`, then the manifest. Changing a gate script, a prompt, the workflow, a ruleset, the CODEOWNERS template, `pending-scripts.txt` or `requirements-test.txt` is a reviewed daytime PR (rule 17).

## Rulesets and CODEOWNERS (Build 2)

The four rulesets are organisation rulesets. Each has a `repository_property` condition, `factory = enabled`, so one copy covers every factory repo (plan 5.7 part 1 does this for the required workflow; here it is applied to all four). To apply one per repo instead, drop that condition.

What the files say, and what is still a placeholder:

- **`main-gate`**: empty bypass list, no deletions, no force pushes, linear history, one approval, stale approvals dismissed, code owner review, approval of the most recent push, conversation resolution, pinned `lcp-gate` check, merge queue (squash). As plan 5.7.
- **`integration-gate`**: one approval (rungs L0 and L1), code owner review, pinned checks `lcp-gate` and `lane/drift`, merge queue, no deletions. Force pushes are left allowed, as V2.1 did so the App can reset `integration` each evening without a bypass entry. **Confirm with Boroon that the evening reset is still wanted.** Rung L2 drops approvals to zero (plan 5.10); that is a stage 7 edit.
- **`protected-paths`** (push ruleset, generated): the 16 patterns from `check_protected_paths.py`, bypass `acceptance-owners` and `platform-team` only.
- **`factory-required-workflows`**: `lcp-gate.yml` from `factory-gates` at `refs/heads/release`, on `main` and `integration`. Enforcement is `evaluate`, because stage 1 starts in Evaluate mode (plan 11.2). Switch to `active` at the stage 1 exit test.
- **Placeholders, filled at apply time by a reviewed PR:** the two team IDs in `make_rulesets.py` (`BYPASS_TEAMS`, then regenerate), the gate repository ID in `factory-required-workflows.json`, and the integration ID of the `lane/drift` check (the App that posts it does not exist yet). All are `0` today. The API rejects `0`, so a file applied too early fails loudly rather than silently. `15368` is the GitHub Actions App ID on github.com; confirm it on GHE.com. The check context name `lcp-gate` is the workflow name; confirm the name a required workflow reports on GHE.com.
- **CODEOWNERS team handles** are `@getai/<team>`, because CODEOWNERS needs the org prefix. The plan writes `@acceptance-owners` and so on. Change `ORG` in `make_rulesets.py` and the template together if the org is named differently.
- **No `*` line in CODEOWNERS.** Both branch rulesets require a code owner review, so a catch-all owner would make every PR wait for that team, and at rung L2 would block auto-merge. Ordinary paths rely on the one-approval rule. The floor-3-and-above paths for L2 are listed as comments, ready for stage 7.
- **Who owns what in CODEOWNERS** (a proposal): tests and specs to `acceptance-owners`; the harness, scripts and deploy settings to `platform-team`; `glossary.md`, `docs/adr/` and `coding-standards.md` to either.
- **Glob meaning.** In the script, `*` stays within one folder and `**` crosses folders, anchored at the repo root. GitHub's fnmatch may read `*` more loosely. If so the ruleset blocks a little more than the script, never less. The `locks` job is the second lock, so the narrower reading is the safe one.

`audit_bypass.py` sees only the JSON. What it cannot see offline is a machine account inside an allowed team. The online half of the audit (list each bypass team's members and check them against the identity register) waits for the real organisation, as does applying anything.

## What `test_workflow.py` checks

- The file parses and has the six jobs. Triggers are only `pull_request` and `merge_group`, with no filters.
- Top-level `permissions` is empty. Only `verify-in-test` has `id-token: write`.
- `build` has `contents: read` only, and no secrets, job token, App token, OIDC or Azure login.
- Secrets appear only as the private key of a GitHub App token step. Every checkout sets `persist-credentials: false`.
- Every job that runs a gate script checks out the gate repo and verifies hashes first. The check confirms it found scripts in `map`, `locks`, `static`, `verify-in-test` and `danger`, so it cannot pass by finding nothing.
- Every script called resolves into the gate checkout, and is in `lcp/` or `pending-scripts.txt`. Every line in `pending-scripts.txt` is unwritten and still called.
- `map` runs `lane_map.py` and keeps its `lane` and `story` outputs. `locks` runs `check_protected_paths.py` with no inline `git diff`.
- Every action is pinned to a full commit ID, never a tag or a branch, with a `# vX.Y.Z` comment on the same line (Dependabot reads and rewrites that comment).

Each check was proved by breaking a copy on purpose: removing `--no-renames`, moving the hash check after a script, a secret in `build`, `id-token` in `static`, an unknown script, a written pending script, a branch filter, a checkout that keeps credentials, an action on `@main`, and the plan's original `locks` job. Each one failed.

## What the Build 2 tests check

- The committed `protected-paths.json` matches the list in `check_protected_paths.py`, and every path the ruleset restricts is a path the `locks` job blocks (sample paths through both).
- Every protected path is owned in `templates/CODEOWNERS` by one of the two bypass teams. The matcher follows GitHub's CODEOWNERS rules (anchoring, trailing slash, `*` within a folder, `docs/*` not reaching subfolders, last line wins), each rule tested.
- All four rulesets parse, are named after their file, apply only to `factory = enabled` repos, and pass the bypass audit. The settings in plan 5.7 are asserted one by one.
- Seeded bad copies fail with the right message: a stale ruleset (a path removed), a missing ruleset, a protected path with no owner, a protected path owned by the wrong team, Copilot (an Integration) in the push ruleset's bypass list, a team in `main-gate`'s bypass list, every repository role, a deploy key, the org admin role, broken JSON.
- Also proved on the real files, then restored: adding a path to the list fails the ruleset and CODEOWNERS checks until both are updated; a hand edit to the generated JSON fails as stale.

## Findings

1. **Renames (fixed).** The plan's inline `locks` check, `git diff --name-only BASE...HEAD`, listed only the new path of a rename, so moving `tests/acceptance/trip.md` to `src/moved.md` passed. `check_protected_paths.py` uses `--no-renames`, and `test_moving_a_protected_file_out_of_its_folder_is_blocked` fails if that is removed. The workflow now runs the script. The plan's Appendix A `locks` job was edited to match (approved 3 November 2026), with a row in decision log 14.4.
2. **Tag pins (fixed).** The plan pinned actions to tags such as `@v5`, which can be moved to other code. Boroon decided on 3 November 2026 to pin to full commit IDs. Each ID is the commit its major tag pointed to on that day, read with `git ls-remote`, and the comment names the matching release (for example `actions/checkout` `v5.1.0`). The plan's YAML keeps the tags for readability and says so in its header.
3. **actionlint 1.7.12 flags three lines, all in the untested jobs:** `queue: max` under `concurrency` in `verify-in-test` (the plan already says "confirm syntax in stage 1"), and `copilot-requests: write` in `verify-in-test` and `danger` ("unknown permission scope"). actionlint's list may lag GitHub. Left as written. Check in spike 0.6 and stage 1. actionlint is not a dependency here. It was run from scratch space.
4. **`sha256sum` does not catch an unlisted file.** See "What is hashed" above. A test pins this gap down.

## Next slices

1. Build 3: the `build` job's offline checks (builders, `git diff --exit-code`, `pac solution pack`). See `docs/plans/stage-1-gate-build-plan.md`.
2. Applying the rulesets, filling the placeholder IDs, and the online half of the bypass audit need the real organisation on GHE.com.
3. Everything that needs a tenant (OIDC, import to Test, Playwright, verifiers) waits for the stage 0 spikes. `verify-in-test` and `danger` carry a header comment saying so.
