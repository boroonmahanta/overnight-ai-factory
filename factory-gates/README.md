# factory-gates (staging copy)

This folder is the first build of the gate repo, `getai/factory-gates` in the plan. It is staged inside the planning repo until that repo exists. Move the contents there, with `gate/` and `scripts.sha256` at the root of the repo, on the protected `release` branch.

Status: **first slice, tested locally, not run against GHE.com or a Power Platform tenant.** The workflow YAML (plan Appendix A) is not in here yet.

## What is here

| File | What it does | Plan |
|---|---|---|
| `gate/lcp/lane_map.py` | Maps `agent/<lane>/<ado-id>-<attempt>` to a lane and a story. Anything else maps to `none`. An unknown lane fails | Appendix A, job `map` |
| `gate/lcp/check_protected_paths.py` | Fails an agent PR that changes a protected path (tests, locked scenarios, specs, glossary, ADRs, standards, `.github/`, `.claude/`, scripts, deploy). One list | Appendix A, job `locks`; rule 17 |
| `gate/lcp/manifest.py` | Makes and checks `scripts.sha256`. Fails on a changed, missing or unlisted script | Appendix A header rules; stage 1 "trusted scripts with a hash manifest" |
| `scripts.sha256` | The manifest of everything under `gate/` | |
| `tests/` | 23 unit tests. Real git repos are used for the protected-path check | |

Run the tests: `python3 -B -m unittest discover -s tests` (Python 3.11 or later, no packages).

After any change under `gate/`, regenerate the manifest: `python3 gate/lcp/manifest.py make . > scripts.sha256`. A test fails if you forget. Changing a gate script is a reviewed daytime PR (rule 17).

## Finding: the plan's inline `locks` check misses renames

Appendix A's `locks` job runs `git diff --name-only "$BASE_SHA"...HEAD`. By default git detects renames and lists only the new path, so moving `tests/acceptance/trip.md` to `src/moved.md` shows `src/moved.md` alone and passes. `check_protected_paths.py` uses `--no-renames`, so the old path is listed as a deletion and fails. `test_moving_a_protected_file_out_of_its_folder_is_blocked` proves it, and fails if `--no-renames` is removed. The push ruleset on the same paths is the first lock and should stop this too, but the second lock is meant to hold on its own.

## Next slices

1. Wire the three scripts into `lcp-gate.yml` (extract Appendix A, replace the inline bash in `map` and `locks`, add a manifest verify step to every job that holds credentials).
2. The four rulesets and CODEOWNERS as files, with the protected path list derived from `check_protected_paths.py`, not copied by hand.
3. The `build` job's offline checks (builders, `git diff --exit-code`, `pac solution pack`).
4. Everything that needs a tenant (OIDC, import to Test, Playwright, verifiers) waits for the stage 0 spikes.
