# factory-gates (staging copy)

This folder is the first build of the gate repo, `getai/factory-gates` in the plan. It is staged inside the planning repo until that repo exists. Move the contents there as they are: this folder's root becomes the repo root (`lcp/`, `scripts.sha256`, `.github/`, `tests/` and the rest), on the protected `release` branch.

Status: **slice 1 and Build 1 done, tested locally only.** Nothing here has run on GHE.com or a Power Platform tenant. The workflow's shape is tested. Whether it runs is not.

## What is here

| File | What it does | Plan |
|---|---|---|
| `.github/workflows/lcp-gate.yml` | The gate workflow. Plan Appendix A, with `map` and `locks` changed to run the tested scripts (Build 1). Every action is pinned to a full commit ID, with the version as a comment | Appendix A |
| `.github/dependabot.yml` | Asks Dependabot to open a weekly pull request when an action pin has a newer release. It rewrites the ID and the version comment together. A human merges by day (rule 17). Untested on GHE.com | |
| `lcp/lane_map.py` | Maps `agent/<lane>/<ado-id>-<attempt>` to a lane and a story. Anything else maps to `none`. An unknown lane fails. Run by `map` | Appendix A, job `map` |
| `lcp/check_protected_paths.py` | Fails an agent PR that changes a protected path (tests, locked scenarios, specs, glossary, ADRs, standards, `.github/`, `.claude/`, scripts, deploy). One list. Run by `locks` | Appendix A, job `locks`; rule 17 |
| `lcp/manifest.py` | Makes and checks `scripts.sha256`. Fails on a changed, missing or unlisted file | Appendix A header rules; stage 1 "trusted scripts with a hash manifest" |
| `scripts.sha256` | The manifest, in `sha256sum` format, of every file a gate job reads. Today that is the three scripts. Prompts, rubrics, agents, rules and project settings join it as they are written | |
| `pending-scripts.txt` | The 20 scripts the workflow calls that are not written yet (decision D2). Delete a line when you write the script | |
| `requirements-test.txt` | PyYAML 6.0.3, pinned by hash, for tests only (decision D3). The scripts in `lcp/` use the standard library only | |
| `tests/` | 47 tests. Real git repos for the protected-path check. `test_workflow.py` checks the workflow's shape | |

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

After any change to a hashed file, regenerate the manifest: `python3 lcp/manifest.py make . > scripts.sha256`. A test fails if you forget. Changing a gate script, a prompt, the workflow, `pending-scripts.txt` or `requirements-test.txt` is a reviewed daytime PR (rule 17).

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

## Findings

1. **Renames (fixed).** The plan's inline `locks` check, `git diff --name-only BASE...HEAD`, listed only the new path of a rename, so moving `tests/acceptance/trip.md` to `src/moved.md` passed. `check_protected_paths.py` uses `--no-renames`, and `test_moving_a_protected_file_out_of_its_folder_is_blocked` fails if that is removed. The workflow now runs the script. The plan's Appendix A `locks` job was edited to match (approved 3 November 2026), with a row in decision log 14.4.
2. **Tag pins (fixed).** The plan pinned actions to tags such as `@v5`, which can be moved to other code. Boroon decided on 3 November 2026 to pin to full commit IDs. Each ID is the commit its major tag pointed to on that day, read with `git ls-remote`, and the comment names the matching release (for example `actions/checkout` `v5.1.0`). The plan's YAML keeps the tags for readability and says so in its header.
3. **actionlint 1.7.12 flags three lines, all in the untested jobs:** `queue: max` under `concurrency` in `verify-in-test` (the plan already says "confirm syntax in stage 1"), and `copilot-requests: write` in `verify-in-test` and `danger` ("unknown permission scope"). actionlint's list may lag GitHub. Left as written. Check in spike 0.6 and stage 1. actionlint is not a dependency here. It was run from scratch space.
4. **`sha256sum` does not catch an unlisted file.** See "What is hashed" above. A test pins this gap down.

## Next slices

1. Build 2: the four rulesets and CODEOWNERS as files, with the protected path list derived from `check_protected_paths.py`, and the offline bypass audit. See `docs/plans/stage-1-gate-build-plan.md`.
2. Build 3: the `build` job's offline checks (builders, `git diff --exit-code`, `pac solution pack`).
3. Everything that needs a tenant (OIDC, import to Test, Playwright, verifiers) waits for the stage 0 spikes. `verify-in-test` and `danger` carry a header comment saying so.
