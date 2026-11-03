# Progress log

Read this second, after `CLAUDE.md`. Add a new entry at the top of the log at the end of every session.
Keep entries short. Write for a reader who has no memory of the chat.

Entry template:

```
## Session N, <date>, branch <name>
Done:
Decisions:
Files changed:
Open items:
Next steps:
```

## Current state

- Mostly documents. First code: `factory-gates/` (stage 1 slice 1 and Builds 1 to 3, 141 tests passing locally). No pipelines or environments exist yet. Nothing has run on GHE.com or a tenant. The rulesets are files, not applied.
- **Build 1 is done** (Session 6). PR 11 merged into `main` on 3 November 2026.
- **Build 2 is done** (Session 7). PR 12 merged into `main` on 3 November 2026.
- **Build 3 is done** (Session 8). PR 13 merged into `main` on 3 November 2026.
- **The move of `factory-gates/` to `GetAI-IP/factory-gates` on `getai.ghe.com` is under way** (Session 9, 3 November 2026). `GetAI-IP` is the central org; four other orgs will use the gate. The split is checked (tree ID `2651ffba…`), step 8 is ready as `docs/plans/factory-gates-move-step-8.patch` (points at `GetAI-IP`), and **the rest runs from Boroon's laptop**. The cloud route is closed: connecting `getai.ghe.com` as a Git provider needs a Claude Team or Enterprise plan, and he is on an individual plan (checked 3 November 2026). `factory-gates/` is still here, untouched.
- PR 9 (Session 4) and PR 10 (Session 5) are merged.
- The main plan is V3.1, dated 1 November 2026: `docs/sources/plan-v3.1.md`.
- Nothing from the plan has been built or tested. Every item marked `[untested]` in the plan is still untested.
- Boroon said more context will be added in later sessions.
- Work is sized with T-shirt sizes (XS to XL), approved on 1 November 2026. See `CLAUDE.md`.

## Open items

- **The move is laptop work (decided 3 November 2026).** The Git providers route needs a Claude Team or Enterprise plan and Boroon is on an individual plan, so it is closed. A local Claude Code session on his laptop, or a cloud session attached to a laptop folder by Remote Control, runs README steps 2 to 12. The step 8 patch applies with `git am`. The steps below are kept only in case a Team plan comes later (the docs cover GitHub Enterprise Server and say nothing about `*.ghe.com`).
  - **The steps** (from https://code.claude.com/docs/en/github-enterprise-server, read 3 November 2026; the page covers GitHub Enterprise Server and is silent on `*.ghe.com`). Needs the Owner or Primary Owner role in the Claude org (Team or Enterprise plan) and permission to create GitHub Apps on `getai.ghe.com`. (1) Create the empty private repo `GetAI-IP/factory-gates` (move step 2). (2) claude.ai, Organization settings, Git providers (https://claude.ai/admin-settings/source-control#github-enterprise), GitHub Enterprise section, Connect, "Set up automatically": display name up to 20 characters, hostname `getai.ghe.com`, leave the CA field empty. (3) Continue to GitHub Enterprise, review the pre-filled app, Create GitHub App. (4) Install the app on `factory-gates` only. (5) On claude.ai/code connect your own GitHub Enterprise account from the repository picker, then start a new session with the repo. If the guided redirect is blocked, use "Add manually" (needs app ID, client ID, client secret, webhook secret, private key; copy the webhook URL Claude generates into the app).
  - **Likely trip points, my inference, untested:** the GHE.com API is at `api.getai.ghe.com`, not `/api/v3` as on Server (see `lcp/apply_rulesets.py`), and the page does not say Claude handles that; the app manifest has no Workflows permission, so a push touching `.github/workflows/` (the first push of the split, the step 8 patch) is refused until Workflows read and write is added in the app's settings and approved; an enterprise IP allow list needs Anthropic's outbound IPs; the cloud environment may need `getai.ghe.com` and `api.getai.ghe.com` under Allowed domains.
- **Five orgs, one central gate (Boroon, 3 November 2026).** The enterprise on `getai.ghe.com` is `GetAI`. The central org `GetAI-IP` holds `factory-gates` and the held-out tests (`factory-holdout`). Four orgs will use the gate: `AI-Business-Solutions`, `AI-Managed-Services`, `Cloud-AI-Platforms`, `GetAI-Knowledge`. Org logins have no `_tqa7h098` suffix (checked for `GetAI-IP` by its URL; assumed for the others, check `AI-Business-Solutions` before step 12). The gate is a repo, a workflow file and rulesets, not a GitHub App; its only Apps are the two read-only token Apps. **Design, proposed, not built:** `lcp-gate.yml` becomes a reusable workflow; each of the four orgs gets a small private caller repo that its own `factory-required-workflows` ruleset points at; one `org.json` per org. Until then `rulesets/org.json` and `templates/CODEOWNERS` describe `AI-Business-Solutions`. **Checked:** (b) below is true. `factory-gates` Settings, Actions, Access offers "Accessible from repositories in the 'GetAI' enterprise", now set. Access is allowed only from private repos, so the callers must be private. Still to check: (a), (c), (d) below.
  - History of the question. Asked 3 November 2026 how many GitHub orgs would hold factory repos; the plan and `factory-gates` assumed one. **Boroon's answer and proposal (3 November 2026): three or four orgs will use the method.** One central org, "Get AI IP", holds the single `factory-gates` repo. Each of the three or four orgs gets a thin caller of it. **Proposed, not yet built.** My reading of how it would work: a reusable workflow (`on: workflow_call`) in the central repo; in each org a small protected repo holding a short caller `lcp-gate.yml` (`uses: <central>/factory-gates/.github/workflows/lcp-gate.yml@release`) that the org ruleset `factory-required-workflows` points at; teams, CODEOWNERS and bypass lists stay per org (one `org.json` per org); the two token Apps and their secrets per org. **To check on `getai.ghe.com` first (all beliefs, none tested):** (a) a ruleset can only require a workflow from a repo in its own org, hence the caller; (b) a private reusable workflow can be shared to other orgs in the same enterprise through the repo's Actions access setting; (c) `job_workflow_ref` in the OIDC token then names the central workflow, so the federated credential pin to `release` still works (spike 0.2); (d) a token App owned by one org can be installed on others, or each org needs its own pair. **Answered by Boroon (3 November 2026):** the central org is `GetAI-IP`. He is Owner of five orgs on `getai.ghe.com`, all listed with the suffix `_tqa7h098`: `AI-Business-Solutions`, `AI-Managed-Services`, `Cloud-AI-Platforms`, `GetAI-IP`, `GetAI-Knowledge`. My reading, not confirmed: the four consumers are the other four, and the shared suffix means one enterprise. **Still open:** (1) the real login of each org. The list shows `AI-Business-Solutions_tqa7h098` beside `AI-Business-Solutions`; the org's URL on `getai.ghe.com` says which one the API, CODEOWNERS and the workflow need. (2) Where `factory-holdout` lives, central or per org. (3) The four checks above. **Effect on the move:** the target is `GetAI-IP/factory-gates`, not `AI-Business-Solutions/factory-gates`. The step 8 patch names `AI-Business-Solutions` and must be redone: `GATE_REPO` and the gate-reader token `owner` fields to `GetAI-IP` (holdout `owner` waits on question 2). Leave `rulesets/org.json` and `templates/CODEOWNERS` alone for now: both are hashed, and they describe a consumer org (`AI-Business-Solutions`, as the first, proposed). A later build adds the caller repo and one `org.json` per org.
- **Sources are complete.** Boroon uploaded the whole research folder as a zip. Every file was checked by checksum against the repo, duplicates were skipped, and the rest were added. The other session ("Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`) is no longer needed for sources and can be deleted.
- **Not read in full.** The files added from the zip were saved but not read in this session: the reports V1 and V2, the runtime and costs note, the eight GitHub and Azure notes, the five Power Platform notes and the one-pager. The five workshop slide images were saved but not viewed. The plan condenses most of them. Read one only when a task needs its detail.
- **Decisions still waiting on Boroon** (from `docs/analysis/tshirt-sizing.md`): approve the shortlist of skills to read in full before any are adopted (plan section 8.3); decide whether to add a work-size field to ADO (Appendix D); decide whether to write a GET AI router skill that routes by size. The sizes themselves are approved.
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The zip copy is the same, so the source itself is cut off.
- **Credit funding: accepted (Boroon, 2 November 2026).** Builds for customers can be made on credits. Settled.
- Spike 0.9 has a hard date. Audit for unmanaged developer environments before 15 November 2026.

## Log

## Session 9, 2026-11-03, branch `claude/wonderful-lamport-vbdypu`

The move of `factory-gates/` to GHE.com, from `main` (PR 13, Build 3, merged 3 November 2026). The 141 tests passed before any change. Boroon expected this session to run on his laptop. It ran in a cloud container that cannot reach `getai.ghe.com`: the network policy denies the host, there is no login for it, and SSO cannot run in a cloud session. So the move got as far as a cloud session can take it, then paused.

Done:
- `docs/progress.md`: Current state says PR 13 merged on 3 November 2026.
- Move steps 1, 3 and 4, in a fresh clone of `main`: `git subtree split --prefix=factory-gates` gave 13 commits (first: slice 1; head: `f91750e`). The two tree IDs match: `git rev-parse main:factory-gates` and the split's tree are both `2651ffba434dcd658540a4a261cf47b51db0e024`. A plain clone of the split passes the 141 tests, `manifest.py verify` and `make_rulesets.py check`.
- Step 8 prepared and tested, saved as `docs/plans/factory-gates-move-step-8.patch` (one commit on top of the split). First made for `AI-Business-Solutions`, then redone for `GetAI-IP` once that became the central org. `GATE_REPO`, all six token `owner:` fields (each reads only `factory-gates` or `factory-holdout`), the holdout checkout and the header comment say `GetAI-IP`; the `GATE_REPO` assertion in `tests/test_workflow.py` matches; the README is no longer a "staging copy" and names the central org, the four orgs and the callers as next slice 6. On a fresh clone of the split, `git am` applies it cleanly and 141 tests, manifest and rulesets check all pass. No hashed file changed, so `scripts.sha256` is unchanged. `factory-gates/` here is frozen, so the patch cannot go stale.
- `factory-gates/` itself is untouched, so a fresh split from `main` gives the same tree ID.
- This session pushed nothing to `getai.ghe.com`.
- **Done by Boroon on `getai.ghe.com`, 3 November 2026:** step 2, created `GetAI-IP/factory-gates` (private, empty). Step 6, a `release` ruleset with **0 required approvals for now** (see Decisions). Step 7, Access set to "Accessible from repositories in the 'GetAI' enterprise". Actions permissions: I advised "Allow enterprise, and select non-enterprise" with "Allow actions created by GitHub" ticked, Marketplace verified creators unticked, `azure/login@*` listed, and the full-SHA pin rule ticked (all nine actions in the workflow are already pinned; checked). Steps 3 to 5 from his Mac (git 2.56.0), in a fresh clone of `main`: the split head `f91750ec6a4d9982cb2d55b117ddbdf6003f2d90` and both tree IDs (`2651ffba…`) matched this session's exactly, and the push created `release` in `GetAI-IP/factory-gates` (144 objects, no sign-in prompt: credentials already stored).

Decisions (Boroon, 3 November 2026):
- A stand-in repo `github.com/boroonmahanta/factory-gates` was proposed, chosen, then dropped before anything was created. Reason: a personal github.com account cannot do any of stage 1's org-level work (the required-workflow ruleset, the `factory=enabled` property, teams, the two Apps, Australian runners, the federated credential, Copilot on GHE.com). It would serve one or two slices of file work and add a second host and a second set of identities. Do not reopen unless the Git providers check fails and the laptop is out of reach for long.
- The cloud route (Git providers) is closed: it needs a Claude Team or Enterprise plan, and Boroon is on an individual plan. The move runs from his laptop.
- **Central org `GetAI-IP`** holds the gate repo and the held-out tests; four orgs will use the gate (see Open items). Supersedes `AI-Business-Solutions` as the gate's home.
- **Step 6 with 0 required approvals for now.** Boroon has no second approver yet; he will raise it before the gate is released to the rest of the enterprise. Pull requests are still required, and force pushes and deletion are still blocked. My note: until then "reviewed" in rule 17 means self-review, so keep write access to `factory-gates` to Boroon alone, and raise the approvals before step 12 makes the gate required on any org.
- One gate repo serves many teams and both profiles (`profile:lcp` now; `profile:pcp` with its own `pcp-gate.yml` at stage 5).

Findings:
- A token route for the cloud exists in principle (a new environment with `getai.ghe.com` under Allowed domains and a token stored as an environment secret) but the docs route GitHub through their own proxy and say nothing about this for GitHub hosts. Untested. Steps 2, 6 and 7 are web settings by hand either way.
- Local Claude Code on the laptop needs nothing special for GHE.com. It uses the laptop's own git and `gh`.
- The new repo's README said "(staging copy)" and named the wrong org. Fixed in the step 8 patch.
- **Dependabot runs on `getai.ghe.com`** (open since Build 1; the comment in `.github/dependabot.yml` still says untested). Within 15 minutes of the push it opened five pull requests in `GetAI-IP/factory-gates`, all major bumps: `azure/login` 2.3.1 to 3.1.0 (#1), `actions/create-github-app-token` 2.2.2 to 3.3.0 (#2), `actions/setup-node` 4.4.0 to 7.1.0 (#3), `actions/checkout` 5.1.0 to 7.0.1 (#4), `actions/upload-artifact` 4.6.2 to 7.0.2 (#5). Five is Dependabot's default limit (no `open-pull-requests-limit` set), so `download-artifact`, `setup-python`, `setup-dotnet` and `codeql-action` will follow as these close. My advice: merge none yet and close none (closing makes Dependabot skip that version). Take them after step 9 passes and the gate's self-test workflow (next slice 2) exists, one at a time, each after reading its release notes; move `upload-artifact` and `download-artifact` together, since the `map` to `build` hand-off uses both. Possible `dependabot.yml` change in that slice (by reviewed PR): group the two artifact actions, set the limit. The Dependabot PRs show "Review required" although step 6 was set to 0 approvals; watch whether the step 8 PR can be merged.
- On GHE.com a private repo's workflows can be shared with the whole enterprise, but only to private repos.
- If step 6 had 1 required approval and an empty bypass list, a lone owner could never merge step 8 (no one can approve their own pull request).
- **The step 8 pull request would not merge** (3 November 2026). Most likely cause, my mistake: I advised ticking "Require approval of the most recent reviewable push" in the step 6 ruleset. That needs someone other than the pusher to approve, even with 0 required approvals, so a lone owner is blocked. Advised: untick it, and check that code-owner review and required status checks are off, until a second approver exists; re-tick it when approvals go to 1. Do not use the bypass list. **Real cause found:** the merge box said "At least 1 approving review is required … New changes require approval from someone other than the last pusher", and the repo's rules page shows an **org ruleset `protect-main` in `GetAI-IP`** (3 branch rules, targeting 1 branch) besides `release-protection`. It most likely targets the default branch, which is now `release`. That org rule is also why the Dependabot pull requests said "Review required". Options given to Boroon: a colleague with write access approves (best, a real review), or exclude `factory-gates` from `protect-main` until a second approver exists. **He excluded `factory-gates` from `protect-main`** (org settings; the repo's rules page is read-only for org rulesets) **and merged the step 8 pull request**, 3 November 2026. Remove the exclusion once there is a second approver. `release` should now have tree `1e7ece8621aafa27a22798d61c5b997c2340560b` (the split plus the patch, computed here).
- **The scripts need Python 3.10 or later** (`Path | None` in signatures, no `from __future__ import annotations`); the README does not say so. macOS's built-in `python3` is 3.9 and would fail on import. The workflow uses 3.11. Homebrew's Python refuses a plain `pip install` (externally managed), so step 9 on a Mac needs a virtual environment.
- The red `lcp-gate` run on the step 8 pull request fails at the first `create-github-app-token` step: `appId option is required`, because `vars.GATE_READER_APP_ID` is not set (the gate reader App does not exist yet). Expected (step 10). The same log shows the Actions permissions allow GitHub's actions, and the token step already targets `GetAI-IP/factory-gates`, the step 8 change.

Files changed: `docs/progress.md`, `docs/plans/factory-gates-move-step-8.patch` (new), `CLAUDE.md`.

Open items:
- None left on the Git providers check: closed, individual plan (see Open items).
- Step 10 (what the gate workflow does on the gate repo's own pull requests) needs Boroon's choice at the time. The two options are in the README.
- Step 12 (rulesets) and spike 0.9 (before 15 November 2026) unchanged.

Next steps:
1. A session on Boroon's laptop (local Claude Code, or Remote Control to a laptop folder) starts from this branch or from `main` once it is merged (the patch and notes are only on this branch until then). It does a fresh split and checks the tree ID is still `2651ffba…` (it is, unless `factory-gates/` has changed).
2. Then README steps 2 to 12 in order: he creates the empty repo (step 2), the split is pushed as `release` (step 5), steps 6 and 7 are settings he does by hand, then `git am docs/plans/factory-gates-move-step-8.patch` on a branch off `release`, opened as the new repo's first pull request (he merges), then step 9 in a fresh clone of the new repo.
3. Step 11 (delete `factory-gates/` here, by pull request) only after step 9 passes in a fresh clone of the new repo.
4. Then the rulesets, from his laptop, once the three teams exist. `apply --yes` only when he says so.

## Session 8, 2026-11-03, branch `claude/elegant-wozniak-316hdv`

Build 3 of `docs/plans/stage-1-gate-build-plan.md`, started from `main` (PR 12, Build 2, merged 3 November 2026). The 112 tests passed before any change.

Done:
- `lcp/check_builders.py`: runs every `workflows/build/*.py` in name order from the project root (`python -B`, 600 second timeout each, all run even after one fails), then fails on any drift from the starting commit: a changed, deleted or staged tracked file, or a new file git does not ignore. Prints the builder's traceback, the files and the first lines of the diff. Exit 1 on failure, 2 for usage.
- `lcp/pack_offline.py`: `solution` runs the plan's two `pac solution pack` calls (unmanaged, then managed) and fails on `pac` missing, `pac` failing, a zero exit with no zip or a broken zip, or no source; it deletes old zips first. `agents` runs `pac copilot pack` in each `agents/<name>/`. The plan's flags, unchanged. `pac` was not installed; the call stays `[untested]`.
- `tests/fixtures/builder-project/`: one builder, its input and its committed output.
- The workflow's `build` job now checks the PR out at `pr/` and runs the two scripts; no inline `git diff` or `pac`. `map` uploads the two scripts, after its hash check, as a one-day artifact `gate-build-scripts`, which `build` downloads. `build` still holds no credentials: the Build 1 test passes unchanged.
- Tests: `test_check_builders.py` (13), `test_pack_offline.py` (13, with a fake `pac` on `PATH`), two new tests in `test_workflow.py` and the hash-order test taught about the artifact. 140 in all, `OK` (141 after the fix below). The two cases the plan named fail as expected: a hand-edited output, a builder that crashes. Broke a copy eleven ways; each failed (list in the README).
- `scripts.sha256` regenerated (eight scripts now). The manifest tests failed until then, as they should. `pending-scripts.txt` did not list either script, so nothing was removed (still 20).
- actionlint 1.7.12: still only the three known warnings, none in `map` or `build`.
- `factory-gates/README.md`: Build 3 section, test list, findings 5 to 9, and **"Moving to GHE.com"**, twelve steps for the move. Not moved.
- **Rehearsed the move** on a scratch clone: `git subtree split` gave 11 commits, starting with slice 1 and Build 1's plain copy of Appendix A; the split tree ID equals the folder's (step 4); a plain clone of the split passes all tests, the manifest and the rulesets check (step 9).
- **Bug found in that rehearsal, fixed:** in a git worktree `.git` is a file, and `manifest.py` hashed it. A manifest made in a worktree would list `.git`, and `sha256sum --check` would then fail in every gate job. Claude Code on a laptop often works in worktrees. `.git` is now never hashed; one new test (failed before the fix). `scripts.sha256` regenerated. 141 tests, `OK`.

Choices of mine (the first two confirmed by Boroon later the same day, see below):
- **How `build` gets a gate script.** The build plan did not say. `build` cannot check out the private gate repo without the reader token, which it must not hold (rule 5). Chosen: `map` hands the two checked scripts over as an artifact. The alternative is an inline copy in the YAML, which brings back two copies of the logic (the D1 trade-off).
- **The drift check is stricter than the plan.** `git diff --exit-code` misses a generated file that was never committed, which pack would then ship unreviewed. A test shows the plan's command passing in that case.
- No `pac` version check in the wrapper; the install step pins it.

Findings (README, Findings 5 to 9): the gap above; the uncommitted-output gap; the plan's bash loop fails a project with no builders (no `nullglob`); the plan never collects `pac copilot pack` output; the worktree bug above.

Files changed: `factory-gates/lcp/check_builders.py` (new), `factory-gates/lcp/pack_offline.py` (new), `factory-gates/tests/fixtures/builder-project/` (new, three files), `factory-gates/tests/test_check_builders.py` (new), `factory-gates/tests/test_pack_offline.py` (new), `factory-gates/tests/test_workflow.py`, `factory-gates/tests/test_manifest.py`, `factory-gates/lcp/manifest.py`, `factory-gates/.github/workflows/lcp-gate.yml`, `factory-gates/scripts.sha256`, `factory-gates/README.md`, `docs/plans/stage-1-gate-build-plan.md`, `CLAUDE.md`, `docs/progress.md`.

Open items:
- Whether `pac solution pack` takes these flags for the YAML source format, and what `pac copilot pack` writes: stage 0 spike.
- At the move: `lcp-gate.yml` will also run on `factory-gates`' own pull requests and fail there (README move step 10).
- Still open: the check context name on GHE.com, actionlint warnings in the untested jobs, Dependabot on GHE.com, spike 0.9 before 15 November 2026.

Second request (same day, same branch). Decisions by Boroon, 3 November 2026:
- **`build` gets its two scripts from `map` as an artifact.** Confirmed.
- **Keep the stricter drift check** (a new uncommitted file fails too). Confirmed.
- **Edit the plan to match the `build` and `map` YAML.** Done: Appendix A `map` and `build` jobs copied from `factory-gates` by script, with the commit pins read back as tags; both job tables; the gate order in 5.6; the trusted-script list in 5.7; the YAML header rule; a new row in decision log 14.4. A parse of both files shows all six jobs and the top level match. `CLAUDE.md`'s line-number map updated (the plan is now 2,604 lines).
- Open the pull request (he said "pull"; read as open the pull request). Opened. He merges it by hand.

Files changed in the second request: `docs/sources/plan-v3.1.md`, `factory-gates/README.md`, `docs/plans/stage-1-gate-build-plan.md`, `CLAUDE.md`, `docs/progress.md`.

Next steps:
1. Boroon reviews and merges the Build 3 pull request.
2. Move `factory-gates/` to `AI-Business-Solutions/factory-gates`, from his laptop: the twelve steps in `factory-gates/README.md`, "Moving to GHE.com".
3. Then the rulesets, from his laptop, once the three teams exist. `apply --yes` only when he says so.
4. A workflow in the gate repo that runs its own tests on every pull request.
5. The separate planning session for the rest of Stage 1 (presets, templates, Playwright kit v0, mining sessions).

## Session 7, 2026-11-03, branch `claude/eager-goldberg-gj0iqg`

Build 2 of `docs/plans/stage-1-gate-build-plan.md`, started from `main` (PR 11, Build 1, merged 3 November 2026). The 47 tests passed before any change.

Done:
- **One source for protected paths.** `check_protected_paths.py` now holds the list as 16 fnmatch globs (`PROTECTED_PATHS`, the ruleset's own form) and builds its regex from them. Same behaviour; the eight existing tests still pass. `glob_to_regex` reads `*` as within one folder and `**` as across folders, anchored at the root.
- `lcp/make_rulesets.py`: `make` writes `rulesets/protected-paths.json` from that list; `check` fails if the JSON is stale or missing, or if `templates/CODEOWNERS` leaves a protected path unowned by `@getai/acceptance-owners` or `@getai/platform-team`. It carries a small CODEOWNERS matcher (GitHub's rules: anchoring, trailing slash, `*` in one folder, `docs/*` not reaching subfolders, last line wins).
- `lcp/audit_bypass.py`: reads ruleset JSON; fails on any bypass actor that is not a team (Integration, which is what Copilot is; DeployKey; every RepositoryRole, the write role named; OrganizationAdmin; unknown). `main-gate` must have an empty list. Exit 1 with one line per problem, 2 for usage.
- `rulesets/`: `main-gate.json`, `integration-gate.json`, `factory-required-workflows.json` by hand, `protected-paths.json` generated. All four are organisation rulesets with the `factory = enabled` property condition. Settings as plan 5.7 part 3; `factory-required-workflows` is in `evaluate` mode (plan 11.2, stage 1 starts in Evaluate).
- `templates/CODEOWNERS`: tests and specs to acceptance owners; harness, scripts and deploy to the platform team; glossary, ADRs and coding standards to either; no `*` catch-all; the L2 floor-3 paths as comments for stage 7.
- Tests: `test_make_rulesets.py` (24) and `test_audit_bypass.py` (13). 84 in all, `OK`. The three seeded bad files from the plan's done-when fail as expected (stale ruleset, Copilot in a bypass list, protected path missing from CODEOWNERS), plus a wrong-team owner, a team in `main-gate`, every role, a deploy key, broken JSON. Also broke the real files on purpose and restored them: a new path in the list fails both checks; a hand edit to the generated JSON fails as stale.
- `scripts.sha256` regenerated: five scripts, four rulesets, the CODEOWNERS template. The manifest test failed until then, as the plan said it would.
- Nothing applied. Applying needs the real org on GHE.com.

Second request ("I have the real org, do the rest"), same day, same branch:
- **All four rulesets are now generated** from `rulesets/org.json` (host, org, gate repo, team IDs, App IDs, enforcement mode) plus the protected path list. The hand-written three were regenerated byte for byte first, so nothing changed in them. Filling an ID is now a data change in one file.
- **`lcp/apply_rulesets.py`** (standard library, token from `GH_TOKEN`): `resolve` looks up team, repo and App IDs and rewrites `org.json`; `plan` is a dry run; `apply --yes` creates or updates the `factory` custom property and the four rulesets by name, never deletes; `audit` is the online half of the nightly bypass audit (live rulesets through `audit_bypass`, only the two allowed teams, no bot or machine member). `plan` and `apply` refuse any ruleset still holding a `0` ID. Tested only against a fake GitHub in `tests/test_apply_rulesets.py` (27 tests). 111 tests in all, `OK`.
- The README has the seven steps to apply once the org details are in `org.json`. Boroon said he will give the real org. Nothing has been sent anywhere.
- Open: `integration-gate` pins the `lane/drift` check to an App that does not exist yet, so `plan` will report it blocked until that App exists or Boroon decides to pin the check without one. **Decided (Boroon, 3 November 2026): `lane/drift` is left out of `integration-gate` for stage 1, back at stage 3.** `make_rulesets.py` adds it again once `apps.lane-drift` in `org.json` is a real ID. A test proves that. 112 tests.
- **Plan gap found 3 November 2026:** `lane/drift` is a required check on every PR into `integration`, human or agent, and the bypass list is empty. The plan says only the lane-close job posts it, for agent branches. A human PR into `integration` would have no tick and could never merge. Fix at stage 3, one of: the drift App posts a passing `lane/drift` on any branch that is not `agent/*` ("not a lane branch"), or the gate's `map` job posts it for lane `none`. Not in the plan yet. Does not affect `main`, this repo or `factory-gates`.
- **The real org (Boroon, 3 November 2026): `https://getai.ghe.com/AI-Business-Solutions`.** Host `getai.ghe.com`, org `AI-Business-Solutions`, now in `rulesets/org.json` and the CODEOWNERS handles (`@AI-Business-Solutions/<team>`). Rulesets regenerated, manifest regenerated, tests read the org from `org.json`. The plan's name `getai/factory-gates` becomes `AI-Business-Solutions/factory-gates` on that host; the plan text is not edited yet.
- Boroon is building the factory in his personal github.com repo and will move it to the GHE.com org when complete. That is fine for the planning repo. Two limits: rulesets are org settings, not repo content, so they are applied to `AI-Business-Solutions` by the tool, never forked; and a required workflow must live in a repo in the same org, so `factory-gates` must be pushed as a new repo there (GHE.com cannot fork from github.com; push `factory-gates/` as its own repo).
- **This container cannot reach `api.getai.ghe.com`** (the environment's network policy denied it). So `resolve`, `plan` and `apply` run from Boroon's machine, or the environment's network access is widened to that host.

Decisions by Boroon, 3 November 2026:
- **`lane/drift` out of `integration-gate` for stage 1**, back at stage 3 together with a passing tick for human PRs into `integration`.
- Confirmed in chat: every merge stays human until trust matures. The ticks sit in front of the human approval, never instead of it. Only rung L2, per class, drops the approval on `integration`, never on `main`.
- **Split the repos.** The planning repo (documents, plans, skills) stays on github.com, where these cloud sessions work. `factory-gates` moves to `AI-Business-Solutions/factory-gates` on `getai.ghe.com` after Build 3, pushed as a new repo with the folder root as the repo root and a protected `release` branch. The staged copy here is then deleted, so there is one copy. From then on gate code changes happen in the org repo, by reviewed PR, with Claude Code on his laptop. The rulesets are applied from his laptop once the three teams exist.
- Also agreed: allow `getai.ghe.com` and `api.getai.ghe.com` in the cloud environment's network access, so a cloud session can run `plan` and `audit` against the org with a token held as an environment secret.

Choices of mine, all listed in `factory-gates/README.md` under "Rulesets and CODEOWNERS" for him to confirm or change:
- All four rulesets at organisation level with the `factory = enabled` condition, not one copy per repo.
- Placeholder IDs are `0` in `org.json` (three team IDs, the gate repo ID; the `lane/drift` App ID stays `0` until stage 3, which keeps that check out). `plan` and `apply` refuse a ruleset with a `0`, so nothing half-filled reaches the API. `15368` is the GitHub Actions App ID on github.com; `resolve` replaces it with the host's own.
- `integration-gate` leaves force pushes allowed (V2.1's evening reset of `integration` without a bypass entry). Confirm the reset is still wanted.
- No `*` line in CODEOWNERS, so code owner review bites only on protected paths and will not block L2 auto-merge later.
- Team handles carry the org prefix, now `@AI-Business-Solutions/<team>`, because CODEOWNERS needs it. The check reads the org from `org.json`.
- The audit fails every repository role, not only write: the plan allows only the two teams.

Files changed: `factory-gates/lcp/check_protected_paths.py`, `factory-gates/lcp/make_rulesets.py` (new), `factory-gates/lcp/audit_bypass.py` (new), `factory-gates/lcp/apply_rulesets.py` (new), `factory-gates/rulesets/` (`org.json` and four generated rulesets, all new), `factory-gates/templates/CODEOWNERS` (new), `factory-gates/tests/test_make_rulesets.py` (new), `factory-gates/tests/test_audit_bypass.py` (new), `factory-gates/tests/test_apply_rulesets.py` (new), `factory-gates/scripts.sha256`, `factory-gates/README.md`, `docs/plans/stage-1-gate-build-plan.md`, `CLAUDE.md`, `docs/progress.md`.

Open items:
- The check context a required workflow reports on GHE.com (`lcp-gate` assumed). Confirm in stage 1.
- GitHub's fnmatch may read `*` more loosely than the script. If so the ruleset blocks a little more, never less. Check when the push ruleset is first applied.
- The online half of the bypass audit is written (`apply_rulesets.py audit`) but has only run against a fake GitHub. Checking team members against an identity register is not built; it lists members and fails on bots only.
- Still open from Session 6: actionlint warnings in the untested jobs; Dependabot on GHE.com; spike 0.9 before 15 November 2026.

Next steps:
1. Boroon reviews and merges Build 2 (pull request opened at his request, 3 November 2026).
2. Build 3, from `main`: the offline `build` job checks (`check_builders.py`, a fixture project, the `pac` pack wrapper). Regenerate the manifest.
3. Then move `factory-gates/` to `AI-Business-Solutions/factory-gates` on GHE.com (decision above), create the three teams, run `resolve` and `plan` from Boroon's laptop, and only `apply --yes` when he says so. The seven steps are in the README.
4. A separate planning session for the rest of Stage 1 (presets, templates, Playwright kit v0, mining sessions).
5. Boroon: create the three teams in `AI-Business-Solutions`, and allow `getai.ghe.com` and `api.getai.ghe.com` in the cloud environment's network access.
6. Stage 3: put `lane/drift` back with a passing tick for human PRs, and edit the plan to close that gap.

## Session 6, 2026-11-03, branch `claude/brave-davinci-0d5ssc`

Build 1 of `docs/plans/stage-1-gate-build-plan.md`, started from `main` (PR 10 merged). D1 to D3 settled before the session.

Done:
- Copied plan Appendix A verbatim to `factory-gates/.github/workflows/lcp-gate.yml` as its own commit (`806c3b2`), so later diffs show every change.
- **Layout fix:** moved the scripts from `factory-gates/gate/lcp/` to `factory-gates/lcp/`. The workflow checks the gate repo out at `gate/` and calls `gate/lcp/<name>.py`, and plan C.5 names `factory-gates/lcp/verify/`. With the old layout every call would have resolved to `gate/gate/lcp/`. `manifest.py` now scans `lcp/`.
- `map` and `locks` now get the read-only gate token, check out the gate repo, verify `scripts.sha256`, then run `lane_map.py` and `check_protected_paths.py` (D1). `locks` checks out the PR at `pr/` like the other jobs and passes the lane to the script, which already lets lane `none` through (tested), so the step-level `if` was dropped.
- Hash check: kept `sha256sum --check --strict scripts.sha256` in every job. New tests prove `manifest.py` and `sha256sum` agree on changed and missing files. Only `manifest.py` catches an unlisted file; the committed-manifest test covers that before release.
- `verify-in-test` and `danger` left as written, each with a header comment naming the stage 0 spikes they wait for.
- `pending-scripts.txt` (D2): the 20 scripts the workflow calls that do not exist. `requirements-test.txt` (D3): PyYAML 6.0.3 with 48 hashes (source archive plus every CPython 3.11 to 3.14 wheel) from PyPI. pip accepted it with `--require-hashes`, and the source archive hash was checked by hand.
- `tests/test_workflow.py`: 15 tests, covering every check in the build plan plus no trigger filters, secrets only in token steps, `persist-credentials: false` everywhere. Five agreement tests in `test_manifest.py`. 43 tests at this point (47 by the end of the session, see below).
- Proved the tests by breaking a copy 10 ways (including removing `--no-renames` and putting back the plan's original `locks` job). Each failed as it should.
- **Plan fix (approved 3 November 2026):** Appendix A `locks` job replaced with the factory-gates version. Consistency edits: both credential tables, "Four jobs hold" the gate key, the 5.7 trusted-script list, and a row in decision log 14.4. The plan's `locks` job is now identical to the one in factory-gates.

Decisions in the first request: none new from Boroon. Three choices of mine were put to him afterwards and all approved in the second request (below): the layout move (forced by the plan's own paths); dropping the `if` on the `locks` step; keeping `sha256sum` rather than calling `manifest.py` in the workflow.

Files changed, whole session: `factory-gates/` (`.github/workflows/lcp-gate.yml` new, `.github/dependabot.yml` new, `lcp/` moved from `gate/lcp/`, `lcp/manifest.py` rewritten, `scripts.sha256`, `pending-scripts.txt` new, `requirements-test.txt` new, `tests/test_workflow.py` new, `tests/test_manifest.py`, other tests' import paths, `README.md`), `docs/sources/plan-v3.1.md`, `docs/plans/stage-1-gate-build-plan.md`, `CLAUDE.md`, `docs/progress.md`.

On the branch, in order: `806c3b2` (Appendix A copied verbatim), `2ecaa3c` (layout move), `9980c9d` (`map` and `locks` wired, workflow tests), `eb1ce7a` (plan `locks` fix), `b1cd152` (log), `440d3f1` (commit pins, Dependabot), `8860c2a` (manifest scope), `c88fe31` (plan `map` fix, decision rows). All pushed. No pull request opened. Boroon merges by hand.

Then (Session 6, second request), decisions by Boroon, 3 November 2026, all done on this branch:
- **Keep `locks` running on every PR** with the human-PR exemption inside the script (one tested place, not two).
- **Keep `sha256sum` as the hash check** in the workflow. A job only runs files the workflow names, and all are listed. The committed-manifest test catches an unlisted file before `release`.
- **Pin every action to a full commit ID.** Nine actions. Each ID is what its major tag pointed to on 3 November 2026 (`git ls-remote`), with the matching release as a comment: checkout v5.1.0, setup-python v5.6.0, setup-dotnet v5.4.0, upload-artifact v4.6.2, create-github-app-token v2.2.2, download-artifact v4.3.0, setup-node v4.4.0, azure/login v2.3.1, codeql-action v3.39.1. `.github/dependabot.yml` added (weekly, Mondays, Sydney time) so pin updates arrive as reviewed PRs. The expected-failure test is now a normal test and also checks the version comment is on the same line. The plan's YAML keeps the tags for readability and says so in its header.
- **The plan's `map` job now matches factory-gates** (gate token, hash check, `lane_map.py`). Both credential tables, "Five jobs hold" the gate key, and the 14.4 row updated.
- **The hash manifest now covers every file a gate job reads**, not only `lcp/`: prompts, rubrics, `.github/agents/`, rules, `projects/`, the Playwright lockfile, and whatever is added later. Not hashed: `tests/`, docs, test-only files, the manifest itself, and `.github/` apart from `agents/`. `manifest.py` rewritten around an `is_hashed` rule; four scope tests added; plan 5.7 and the Appendix A header say so; a 14.4 row records it. Today the manifest still lists only the three scripts, because nothing else exists yet.
- 47 tests, `OK`. actionlint still shows only the three known warnings. Checked the plan's six jobs against factory-gates with the pins mapped back to tags: all six match.

Also answered in chat: a pro-code gate would most likely sit beside `lcp/` as `pcp/` with its own `pcp-gate.yml` in the same repo (V2.1 used one `factory-gates` repo for both lanes). Not decided. Three things to settle then: shared scripts between the two gates, the manifest covering both, and the custom-property value that routes code repos to `pcp-gate.yml`. Noted in the README.

Open items:
- **Finding: actionlint 1.7.12 flags `queue: max` and `copilot-requests: write` (twice)**, all in the untested jobs. Left as written. Check in spike 0.6 and stage 1.
- Dependabot on GHE.com for this org: untested. If it is not available, the pins go stale until someone re-runs the lookup by hand.
- Spike 0.9, the environment audit, is still due before 15 November 2026.

Next steps:
1. Boroon reviews and merges Build 1 (pull request when he asks for one).
2. Build 2, from `main`: rulesets and CODEOWNERS as files, `make_rulesets.py`, `audit_bypass.py`. Regenerate the manifest after adding `rulesets/` and `templates/`.
3. Build 3: the offline `build` job checks.

## Session 5, 2026-11-03, branch `claude/nice-brahmagupta-5641pb`

Planning only. No build work, by Boroon's choice, to save context.

Done:
- Fast-forwarded this branch onto `claude/wizardly-planck-8i7543`, so it now holds slice 1 (`86e257a`, `7ea4ad0`, `183216d`). Re-ran the 23 tests: all pass.
- Wrote `docs/plans/stage-1-gate-build-plan.md`: three build sessions (workflow file and plan fix; rulesets and CODEOWNERS; offline `build` job checks), with what to read, steps, tests and done tests for each.

Decisions (Boroon, 3 November 2026):
- Pull slice 1 into this branch: yes.
- Fix the rename gap in the plan's Appendix A `locks` job too, not only in `factory-gates/`: yes. Done in Build 1, not yet.
- Build in separate sessions, one per slice. This session is planning only.

Files changed: `docs/plans/stage-1-gate-build-plan.md` (new), `docs/progress.md`, `CLAUDE.md`.

Open items:
- **Three decisions before Build 1, all decided 3 November 2026** (detail in the plan): D1, `map` and `locks` get the read-only gate token; D2, a pending-scripts list checked by a test; D3, PyYAML pinned for tests only.
- Finding to raise in Build 1: the plan pins actions to tags such as `@v5`, not commit SHAs.
- Slice 1 and this plan go to `main` by the Session 5 pull request, opened 3 November 2026 at Boroon's request.
- The rest of Stage 1 (Spec Kit presets, glossary and ADR templates, Playwright kit, session mining) needs its own planning session.
- Spike 0.9, the environment audit, is still due before 15 November 2026.

Later in Session 5, Boroon decided: D1, option A (`map` and `locks` get the read-only gate App token); D2, the pending-scripts list. D3, PyYAML pinned with a hash, for tests only.

Next steps:
1. Boroon merges the Session 5 pull request (slice 1 plus this plan) into `main`.
2. Build 1, from `main`.

## Session 4, 2026-11-02, branch `claude/wizardly-planck-8i7543`

Build started (Boroon, 2 November 2026: "get on with the actual build"). **Stage 1 slice 1 is `factory-gates/`**, staged in this repo until the `getai/factory-gates` repo exists. Three trusted gate scripts with 23 unit tests, all passing locally with Python 3.13 and no packages:
- `lane_map.py`: branch `agent/<lane>/<ado-id>-<attempt>` to lane and story; unknown lane fails (replaces the inline bash in the `map` job).
- `check_protected_paths.py`: fails an agent PR that touches a protected path. Tested against real git repos.
- `manifest.py` and `scripts.sha256`: hash manifest for the trusted scripts; a test fails if the committed manifest is stale.
- **Finding:** Appendix A's inline `locks` check (`git diff --name-only BASE...HEAD`) misses renames, because git lists only the new path. Moving a locked scenario out of `tests/acceptance/` would pass. The script uses `--no-renames` and a test proves the difference. The plan's YAML is not yet changed. The push ruleset is the first lock, so this is a gap in the second lock only.
- Not tested: anything on GHE.com or a Power Platform tenant. Next slices are listed in `factory-gates/README.md`: wire the scripts into the workflow YAML, rulesets and CODEOWNERS as files, the offline `build` job, then the tenant-dependent jobs after the stage 0 spikes.
- Files changed: `factory-gates/` (new), `CLAUDE.md`, `docs/progress.md`.

After PR 9 merged (decision by Boroon, 2 November 2026): **credit funding for client builds is accepted and settled.** Not to be raised again. Recorded in `CLAUDE.md` (biggest risk 1, open questions) and in the plan (section 9.1, spike 0.1 row, risk 1 row, section 15.1, new decision log section 14.4). Files changed: `docs/sources/plan-v3.1.md`, `CLAUDE.md`, `docs/progress.md`.

Done:
- Boroon gave the three-batch skills plan from the chat "Planning the skills to use": batch 1 `lcp` (13 skills, needed before Stage 2, day 15), batch 2 `pcp` (16, before Stage 5, day 46), batch 3 Lane A (8, before Stage 6, day 60). Another session read all 36 and wrote `docs/analysis/skill-batches-review.md`. That file is only on branch `claude/sharp-wright-1muptp` (commit `c3a1c72`), not on `main`. Its verdicts are proposals, and its reads were done by agents, not line by line.
- Checked the 36 skills against this repo: 19 live (4 unchanged, the rest adapted, including `show-me-your-work` as `getai-decision-log`), 1 on the shelf (`principle-migrate-callers-then-delete-legacy-apis`), 16 untouched. This corrects the 18 / 2 / 16 count I gave in chat. Batch 3 is entirely untouched. `idea-refine` was already dropped from batch 3 and folded into the Story Planner.
- Read `show-me-your-work` and `pause-safely` in full (rule 19), from the pinned commit `ae5650f`.

Decisions (Boroon, 2 November 2026):
- **`show-me-your-work`: keep as `getai-decision-log`.** It was already adapted and merged (I wrongly called it shelved in chat). Needs a test, not a rewrite. Gaps: the transcript audit assumes a transcript in the evidence bundle, which the plan does not yet say; nothing checks that the log reached Blob.
- **`pause-safely`: drop.** A 12-line playbook inside `poteto-mode`, not a skill. PARK, `park.json` and the handoff files cover it. Its one useful idea (a `wip:` checkpoint on a non-PARK stop) went into the plan.
- **Plan edit:** section 5.11 has a new paragraph, "Stops that are not a PARK". On a timeout, exhausted cap or killed replica, the driver commits a `wip:` commit, pushes with no PR, logs `INCONCLUSIVE` and leaves the handoff files. Marked `[untested]`.

Then (Session 4, second request), decisions by Boroon:
- **`diagnosing-bugs` read in full and shelved.** Copied unchanged to `skills/pocock/diagnosing-bugs/` (pinned `4ae2317`). Not adopted. **Revisit for the BAU Managed Services mode.** Proposal: rewrite as `pcp-diagnose`, with interactive steps turned into PARKs, model invocation off, the builder's regression test labelled its own check, and lowercase `glossary.md`. Open question for then: may a night agent run all six phases, or only reproduce and minimise (as `pcp-triage` does)?
- Notes for all three reads (`show-me-your-work`, `pause-safely`, `diagnosing-bugs`) are in the new `docs/analysis/skills-reading-notes-skill-batches.md`. `skills/README.md` and `CLAUDE.md` updated.

Then (Session 4, third request), decisions by Boroon:
- **`code-simplification` read in full and shelved.** Copied unchanged to `skills/addy/code-simplification/` (pinned `301b02b`). Not adopted. Reason: plan 5.12 says refactoring belongs to review, not the build loop, so a builder skill that simplifies is the wrong tool. Its three signal tables are worth lifting into the standards reviewer rubric. A refactor-only night story (`pcp-simplify`) is possible later. This differs from the other session's review ("rewrite").

Then (Session 4, fourth request), decisions by Boroon:
- **`deprecation-and-migration` read in full and shelved.** Copied unchanged to `skills/addy/deprecation-and-migration/` (pinned `301b02b`). Not adopted. Mostly human decisions (rules 1 and 9) and it pushes toward deletion. Keep expand/contract (a Dataverse column cannot be renamed, so it is already how a rename works): a block of about 1 KB in the spec preset or agent instructions, drop or rename means PARK `one_way_door`. A plan edit, not yet made. It also supports leaving `principle-migrate-callers-then-delete-legacy-apis` on the shelf. Differs from the other session's review ("rewrite").

Then (Session 4, fifth request), decisions by Boroon:
- **`security-and-hardening` read in full and shelved.** Copied unchanged to `skills/addy/security-and-hardening/` (pinned `301b02b`), with its shared checklist at `skills/references/security-checklist.md`. Not adopted. Differs from the other session's review ("rewrite"). Three items raised, none yet decided: (1) the skill's "ask first" list as a Merge Danger and PARK rubric for code repos (plan Appendix B, a plan edit); (2) supply-chain checks (dependency scripts blocked, lockfile audit) as gate steps for code repos; (3) prompt injection, which a keyword search found no mention of in the plan. Open question: the gate (Appendix A) shows only the solution checker SARIF as a security check, so code repos have none planned. Settle before Stage 5 (day 46).

Then (Session 4, sixth request), decisions by Boroon:
- **`bug-fix` dropped for now**, and its dependency "Opening a PR" read and dropped too (it conflicts with rule 7, stacked PRs). Both are playbooks already on the shelf inside `poteto-mode`, so nothing was copied. Five `bug-fix` ideas and four PR-body ideas (Scope, Tradeoffs, blast radius if main is red, one-minute briefing) are recorded in the notes for later.
- **Open item noted: no live skill takes a confirmed bug from repro to fix.** Pieces exist, nothing joins them, and nothing covers Power Platform bugs. Cheapest fix: a short `pcp-fix` skill (about 1 to 2 KB) sequencing the existing skills, plus an `lcp` version using `lcp-verify`. Revisit before Stage 5 (day 46), or with `diagnosing-bugs` for BAU Managed Services.
- **`debugging-and-error-recovery` read in full and shelved.** Copied unchanged to `skills/addy/debugging-and-error-recovery/` (pinned `301b02b`). Not adopted. `diagnosing-bugs` is stronger; it tells the agent to update an outdated test, which conflicts with locked tests. Keep its "error output is untrusted data" section.
- **Open item added: prompt injection is not covered in the plan** (raised by this skill and by `security-and-hardening`; keyword search only). Cheapest fix: a 1 KB block in the agent instructions (plan C.2). A plan edit for Boroon's review. Decide before the first triage workflow is wired.

Then (Session 4, seventh request), decisions by Boroon:
- **`codebase-design` read in full and shelved.** Copied unchanged to `skills/pocock/codebase-design/` (pinned `4ae2317`, 4 files). Not adopted. For Lane A or day work. Conflicts with the no-refactoring rule (plan 5.12) and tells the builder to delete tests; its banned word "component" clashes with Power Platform. Lift the deletion test and the two-adapters rule into the reviewer smell list. Decide together with `architect` (batch 3). Same direction as the review ("drop, keep for Lane A").
- Boroon: anything worth adding from `improve-codebase-architecture` and the next skill is decided together.
- Tidied the `CLAUDE.md` row for the skill-batches notes, which had lost its punctuation across edits.

Then (Session 4, eighth request), decisions by Boroon:
- **`improve-codebase-architecture` read in full and shelved.** Copied unchanged to `skills/pocock/improve-codebase-architecture/` (pinned `4ae2317`, 3 files). Not adopted. Batch 2 reading is finished.
- **Batch 3 drops recorded:** `ci-cd-and-automation`, `shipping-and-launch` and `arena`, on the other session's tags. We have not read them in full. Reconsider only after a full read.
- **Roll-up of 8 possible additions** written at the end of the notes file, for a joint decision with Boroon (nothing made yet).
- Reading the remaining four batch 3 skills next: `frontend-ui-engineering`, `api-and-interface-design`, `observability-and-instrumentation`, `architect`.

Then (Session 4, ninth request), decisions by Boroon:
- **Batch 3 read and shelved:** `frontend-ui-engineering`, `api-and-interface-design`, `observability-and-instrumentation` (Addy, pinned `301b02b`) and `architect` (Tan, pinned `ae5650f`), copied unchanged, with the two Addy checklists in `skills/references/`. None adopted. **Revisit in Stage 6** (Lane A, from day 60).
- **Decision: Lane A's architecture sketch gets a day approval** (the architect's Phase C checkpoint on by default, at least for Lane A and size L). The plan currently has Lane A's generator write `plan.md` and `tasks.md` at night with no human step, so this needs a plan edit (sections 4 and 5), not yet made. Rule 9 is the reason (the review wrongly cited rule 10).
- **All reading for the three batches is finished** except the three dropped batch 3 skills. Roll-up of 14 possible additions is at the end of `docs/analysis/skills-reading-notes-skill-batches.md`, for a joint decision.

Then (Session 4, tenth request): Boroon asked to update the pull request and merge it, then stopped that and asked for this log update instead. Nothing was merged or rebased by me.
- **State found:** `origin/main` shows "Merge pull request #8" at `b5fcd69`, and `main` has moved since this branch was cut. That merge brought in only the first commit of this session (`1614acb`: the `show-me-your-work` and `pause-safely` verdicts and the plan 5.11 paragraph). I read this from the git log. I did not get to read PR 8 itself.
- **So the later commits on `claude/wizardly-planck-8i7543` were not on `main`; PR 9 now carries them:** the `diagnosing-bugs`, `code-simplification`, `deprecation-and-migration`, `security-and-hardening`, `debugging-and-error-recovery`, `codebase-design`, `improve-codebase-architecture` and batch 3 shelf copies, their notes, the `bug-fix` drop, the roll-up of 14 additions, and the day-approval decision for the Lane A sketch (latest commit `8e48acf`). About 29 files and 4,000 added lines against `main`.
- **Done:** rebased the 10 later commits onto the current `main` (no conflicts; `main` already held the first commit, so nothing was lost) and pushed to the same branch with a lease. Opened PR 9 (https://github.com/boroonmahanta/overnight-ai-factory/pull/9). Not merged by me. Boroon merges it by hand.

Files changed: `docs/sources/plan-v3.1.md` (one paragraph in 5.11), `docs/progress.md`, `docs/analysis/skills-reading-notes-skill-batches.md` (new), `skills/pocock/diagnosing-bugs/` (new, 3 files), `skills/README.md`, `CLAUDE.md`. Also `skills/addy/code-simplification/` (new, 1 file) `skills/addy/deprecation-and-migration/` (new, 1 file), `skills/addy/security-and-hardening/` (new, 2 files) and `skills/references/security-checklist.md` (new).

Open items:
- The review file is not on `main`. Where it differs from what is live: it says drop `wizard` (we have `getai-wizard`), drop `principle-model-the-domain` (adopted), and rewrite the four skills adopted unchanged. Boroon decides each. Not changed.
- All 36 skills in the three-batch plan are now read (or, for `ci-cd-and-automation`, `shipping-and-launch` and `arena`, dropped on the other session's tags without our own full read). Nothing new is adopted. Decide the 14 roll-up additions together, then make the plan edits (rule 17).
- **No bug-fix workflow** (see the sixth request above). Decide before Stage 5.
- Add to the Stage 3 driver spec: the non-PARK stop checkpoint, and where the transcript lives for the decision-log audit.
- Not started: spike 0.9 (environment audit, before 15 November 2026).

Next steps:
1. Boroon merges PR 9. Then branch the next session from `main`.
2. Spike 0.9: audit for unmanaged developer environments before 15 November 2026 (hard date).
3. Decide the 14 roll-up additions with Boroon (end of `docs/analysis/skills-reading-notes-skill-batches.md`), starting with items 1 and 2 (prompt injection, code-repo security checks), then make the plan edits for his review (rule 17). Includes the day approval of the Lane A sketch.
4. Boroon rules on where the other session's review differs from what is live. The review file (`docs/analysis/skill-batches-review.md`) is still only on branch `claude/sharp-wright-1muptp`.
5. Reading is finished. Revisit the shelved Lane A skills at Stage 6 and `diagnosing-bugs` for BAU Managed Services.

## Session 3, 2026-11-02, branch `claude/exciting-babbage-4u2zp4`

Boroon answered the five open items from Session 2.

Done:
- **AutoTask and PRTG reports:** the export route is their APIs or an MCP server. Not built, not tested. Written into `pcp-triage` ("Where reports come from" and step 1 of "Running it by hand") and plan section 4.5. Manual run by day is still the only mode in use. Reports hold personal data, so the scrub-first rule still applies to anything an API or MCP server returns.
- **`Custom.TriageSource`:** added AutoTask and PRTG to the picklist (plan Appendix D). Plan 4.5 inputs table has a new row.
- **Real `main` branch:** created on GitHub from the default branch tip (`696aa3c`, the merge of PR 2). The default branch setting is still `claude/jolly-albattani-818i8e`. Changing the default is a GitHub setting I cannot make. Boroon: Settings, Branches, switch default to `main`. Rule 1 says only humans merge to `main`, so add a branch protection rule while there.
- **Batch 2 skills read in full:** `unslop`, 24 `principle-*`, `grilling`, `domain-modeling`. Copied unchanged to `skills/tan/` and `skills/pocock/` at the same pinned commits. Notes in `docs/analysis/skills-reading-notes-batch2.md`. None adopted.
- **Verification skills fixed:** `create-verification-skill` and `maintain-verification-skill` now write to `.claude/skills/lcp-verify/` (or `pcp-verify`) with name `lcp-verify`. A dated note at the top of each records the change. The shelf copies stay as the originals. Rule 17: these edits need Boroon's review by PR.
- `poteto-mode` was not copied or read in full, as Boroon asked. Only its file list and the first 40 lines of `SKILL.md` were looked at, to give a basis for the discussion.

Findings that need a decision:
- `domain-modeling` writes `GLOSSARY.md`, in capitals, with no implementation details. The plan wants lowercase `glossary.md` with Dataverse schema names, and the protected-paths pattern in Appendix A matches lowercase only. Adopting unchanged would leave the glossary unprotected.
- `grilling` (pinned) asks a round of questions at a time. Plan 6.2 says one question at a time. The plan's wording came from the older v1.1 video.
- `principle-never-block-on-the-human` and `principle-outcome-oriented-execution` conflict with rules 9 and 7. `principle-migrate-callers-then-delete-legacy-apis` assumes no external users.

Files changed:
- New: `docs/analysis/skills-reading-notes-batch2.md`, `skills/tan/unslop/`, `skills/tan/principle-*/` (24), `skills/pocock/grilling/`, `skills/pocock/domain-modeling/`
- Edited: `.claude/skills/create-verification-skill/SKILL.md`, `.claude/skills/maintain-verification-skill/SKILL.md`, `.claude/skills/pcp-triage/SKILL.md`, `docs/sources/plan-v3.1.md` (Appendix D picklist and a 4.5 row), `skills/README.md`, `CLAUDE.md`, `docs/progress.md`
- GitHub: new branch `main`

Open items:
- Discuss `poteto-mode` (questions are at the end of the batch 2 notes).
- Which batch 2 skills to adopt. My proposal is in the notes. Decide rounds against one at a time for `grilling`, and the glossary naming.
- Switch the GitHub default branch to `main` and protect it.
- Review of the two edited verification skills (rule 17).
- AutoTask and PRTG API or MCP integration: who builds it, with what read-only credential, and whether an MCP server for either exists. Not checked.

Next steps:
1. Talk through `poteto-mode`. Then read it in full if wanted.
2. Adopt or adapt batch 2 by Boroon's picks.
3. Write the first `lcp-verify` with `create-verification-skill` (stage 2).

Then (Session 3, second request), decisions by Boroon:
- **Glossary files lowercase.** `getai-domain-modeling` written in `.claude/skills/`: `glossary.md`, `glossary-map.md`, `docs/adr/`, a Schema line per term (Dataverse names or code symbols), day only.
- **Grilling in tranches of five at most.** `getai-grilling` written: most blocking first, the rest held. Plan 6.2 bullet changed from "one question at a time" to this. `ask-me` status line updated.
- **Three principles stay on the shelf** (`never-block-on-the-human`, `outcome-oriented-execution`, `migrate-callers-then-delete-legacy-apis`). Revisit when an issue calls for them. The cases to watch are in the batch 2 notes.
- **`poteto-mode` read.** Copied to `skills/tan/poteto-mode/`. Verdict in `docs/analysis/skills-reading-notes-batch2.md`: a Cursor plugin, not harness agnostic. It has a Claude Code adapter but nothing for GitHub Copilot or VS Code. Several playbooks break rules 1, 2, 6, 9 and 12. Proposal: do not adopt, lift a few small ideas. I did not read the `watch-pr` TypeScript (about 3,800 lines) line by line, only searched it.
- Both new skills are untested and need Boroon's review by PR (rule 17).

Open items added: plan line 703 says the executor's `lcp-verify` copy lives in `.github/skills/lcp-verify/`, while the verification skills now write to `.claude/skills/lcp-verify/` as Boroon asked. Copilot reads both (plan line 858), but the plan should pick one. Not changed. Unslop and the remaining principles: adoption not yet decided. Whether to lift the poteto ideas into `ask-me`.

Then (Session 3, third request), decisions by Boroon:
- **One skills folder: `.claude/skills/`.** Plan edited in five places (section 5.9 line about the two copies, the 8.x table row, C.5 heading, C.7 heading, and the two protected-paths lists, which now put skills under `.claude/**`). Plan 8 now says skills live in `.claude/skills/` only. The gate's trusted copy of `lcp-verify` stays in `factory-gates`. Copilot reading `.claude/skills` rests on the plan's cited GitHub docs and is untested by us. Check it in spike 0.6.
- **Four poteto habits lifted into `ask-me`:** open with the goal, label claims, classify a question before asking, fix/dismiss/ask on review comments. Not lifted: the 22 playbooks and the performance mantras. `ask-me` also now says the verification skills write to `.claude/skills/lcp-verify/`.
- Rule 17: `ask-me` change needs Boroon's review by PR.

Then (Session 3, fourth request), decisions by Boroon:
- **Adopted into `.claude/skills/`:** `unslop` and 21 `principle-*` skills (list in `skills/README.md`). Names unchanged so their links hold. A dated GET AI note sits at the top of each, and `unslop` has a new rule 34 (Australian English). `principle-guard-the-context-window` is adopted because Boroon likes it, with a note tying it to the 200K session limit.
- `ask-me` has a new "Principles to reach for" section. The three conflicting principles are listed there as shelved.
- Known gap: `principle-explain-the-number` links to `benchmark-checklist`, which we do not have. `principle-type-system-discipline` names `typescript-best-practices`, also not adopted. Notes in both skills.
- Batch 2 is finished except for review (rule 17) and testing. Nothing adopted has been run.

Then (Session 3, merges and `main`), done at Boroon's request:
- PR 3 (https://github.com/boroonmahanta/overnight-ai-factory/pull/3) merged the batch 2 work into the old default branch `claude/jolly-albattani-818i8e` (merge commit `9c8b91a`). Rule 17 review met for the batch.
- PR 4 (https://github.com/boroonmahanta/overnight-ai-factory/pull/4) merged that branch into `main` (merge commit `79eb828`), at Boroon's direction (rule 1: a human decides every merge to `main`).
- **`main` is now the GitHub default branch** (Boroon switched it). A ruleset `protect-main` guards it: pull request required, no force pushes, no deletions, all merge methods allowed, Boroon on the bypass list. `claude/jolly-albattani-818i8e` is retired and can be deleted once Boroon is happy.
- From now on, session branches start from `main`, and merge into `main` by pull request with Boroon's go.
- This closes the open items "real `main` branch" and "switch the default and protect it".

Then (Session 3, merge rule), decision by Boroon: **he merges every pull request into `main` by hand, to stay compliant with rule 1.** I open the pull request and stop. Noted in `CLAUDE.md`. PR 6 (log of the merges and `main` as default) was merged by him.

## Session 2, 2026-11-02, branch `claude/hopeful-mccarthy-znxbf8`

Done:
- Started step 1 of `docs/analysis/tshirt-sizing.md` section 4 (read the shortlist in full). Boroon said to use a top-level `skills/` folder that does not auto-load.
- Cloned the three public repos to scratch space, found the 16 skills in the first batch, and copied them unchanged into `skills/addy/` (3), `skills/tan/` (7), `skills/pocock/` (4) and `skills/benny/` (2). 49 files.
- Read every file of all 16 in full, including the four scripts.
- Wrote `skills/README.md` (sources, pinned commits, MIT licences) and `docs/analysis/skills-reading-notes.md` (safety read, assumptions we lack, one line each, findings).

Decisions:
- None approved by Boroon yet. "Read in full" is done. "Adopt" is not.
- Proposed only: nothing found that blocks adoption. Most skills need adapting (Cursor tools, Slack, Linear, Notion). `create-verification-skill` and `maintain-verification-skill` look like the template for `lcp-verify`. The Benny pair is the best built example of the outer loop.

Files changed:
- New: `skills/` (49 copied files plus `skills/README.md`), `docs/analysis/skills-reading-notes.md`
- Edited: `CLAUDE.md` (two rows added to the map), `docs/progress.md`

Open items:
- Which of the 16 to adopt, adapt or leave on the shelf (Boroon).
- Several of the 16 lean on skills we have not read: `unslop`, the `principle-*` skills, `poteto-mode`, `grilling`, `domain-modeling`. Decide if they are next.
- The Benny skills need a control adapter and a configured triage identity before they could run. Not buildable until `lcp-verify` and the ITSM tool are known.

Also done (later in Session 2): Boroon asked to adapt `ask-matt` into "ask-me". Written as `.claude/skills/ask-me/SKILL.md` (live, only runs when invoked). It routes by T-shirt size, day or night, and tags each skill live, shelf or planned. Credits Matt Pocock and the pinned commit. Not yet reviewed by Boroon. Tan, Pocock and Addy skills it names are still shelf, so it tells the user to adopt first or do the step by hand. Update its tags when a skill is adopted or an `lcp-*` skill is written.

Then (Session 2, third request): Boroon said "adopt the first five skills and adapt the rest". Read "first five" as the first five in the reading notes table. Done:
- Adopted unchanged into `.claude/skills/`: `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`, `create-verification-skill`, `maintain-verification-skill`.
- Adapted into `.claude/skills/`: `lcp-blast-radius`, `getai-decision-log`, `getai-correct`, `lcp-how`, `lcp-why`, `getai-intake` (from Pocock `triage`), `getai-wizard`, `getai-questionnaire`, `lcp-triage` (the two Benny skills merged, to match the `lcp-triage` agent in plan 4.5). `ask-me` was already adapted from `ask-matt`.
- `ask-me` tags updated. `skills/README.md` records what became of each skill. Shelf copies kept as pinned originals.
- Decisions made by me, for Boroon to confirm: `lcp-triage` has no fixing and no PR, because the plan has a human decide and rule 3 needs scenarios from someone else. Pocock `triage` became `getai-intake`, the human day step. Adopted skills were left unchanged as asked, so the two verification skills still write to `.cursor/skills/`.
- Nothing adapted has been run. The adopted five were read in full before adoption (rule 19) and pinned.

Open items added: review the nine `lcp-*` skills (rule 17 says reviewed daytime PR). The adopted constraint skill's examples are JavaScript, not Power Platform. `lcp-triage` needs the triage workflow, `lcp-verify` and a Test credential before it can run. Only `create-verification-skill` can build `lcp-verify`.

Then (Session 2, fourth request), decisions by Boroon:
- **Keep the fix and PR step out of `lcp-triage` for now.** It may move in later when trust is built (trust ladder, evidence first, only into `integration`).
- **The skills were reviewed by Boroon and merged** to the default branch `claude/jolly-albattani-818i8e` (there is no `main` yet) by PR 1 (https://github.com/boroonmahanta/overnight-ai-factory/pull/1). This clears the rule 17 review for the nine `lcp-*` skills and `ask-me` as written. They are still untested.
- Boroon asked whether the `lcp-*` skills could be reused under a different prefix. Answer and open question are below in Open items.

Open items added: naming of the reusable skills. Rule 18 and the naming table use `lcp` only for the Power Platform profile. A generic skill (decision log, questionnaire, correct, wizard, intake) is not Power Platform specific. Options were put to Boroon in chat. Not decided.

Then (Session 2, fifth request), decisions by Boroon:
- **Naming.** `pcp` means pro-code platform. Skills that work for any profile are `getai-*`. Skills tied to Power Platform stay `lcp-*`. Code-profile versions will be `pcp-*`. Boroon recalled agreeing `pcp` earlier, but no record of it exists in the repo or in this session, so it is recorded here as agreed now.
- **Renamed** (folder, frontmatter name and all references): `lcp-decision-log`, `lcp-questionnaire`, `lcp-correct`, `lcp-wizard`, `lcp-intake` became `getai-decision-log`, `getai-questionnaire`, `getai-correct`, `getai-wizard`, `getai-intake`. Still `lcp-*`: `lcp-blast-radius`, `lcp-how`, `lcp-why`, `lcp-triage`.
- **Not done:** no `pcp-*` skills written yet. Plan Appendix D has `Custom.LaneProfile` as code or lcp. Adopting `pcp` there is a plan edit, not made.

Then (Session 2, sixth request), decisions by Boroon:
- **Wrote the four pro-code skills:** `pcp-blast-radius`, `pcp-how`, `pcp-why`, `pcp-triage`. Same methods as the `lcp-*` versions, pointed at code repos (dependency and contract breakage, entry points and tests, git and runtime history, repo sandbox repro). `pcp-triage` has no fix or PR step, same as `lcp-triage`. Untested.
- **Plan edit:** `Custom.LaneProfile` picklist is now `pro-code, lcp` (Appendix D) and the ledger `fact_run.profile` is `pro-code, lcp` (section 10.1). Was `code, lcp`. Edited in `docs/sources/plan-v3.1.md`. The naming table in `CLAUDE.md` is updated.
- `ask-me` and `skills/README.md` updated to name the three prefixes.

Open items added: the plan has no triage workflow for code repos. `pcp-triage` is a proposal until Boroon decides the trigger, the runner and the credential. The `pcp-*` skills and the rename are not yet reviewed by Boroon (rule 17). Other plan text that says "code profile" in prose is unchanged. Only the field values changed.

Then (Session 2, seventh request), decisions by Boroon:
- **Code-repo reports come from** AutoTask tickets, PRTG alerts, ADO service hooks, service desk webhooks and manual runs by day. **Start with the manual run by day.** Nothing is automated until manual runs show what is worth it.
- `pcp-triage` now has a "Where reports come from" table and a "Running it by hand" section. The person strips names, emails, phone numbers and record IDs first, because the Function the plan relies on for this does not exist yet. PRTG alerts will often be reroutes (infrastructure, not code).
- Partly answers the open question on ITSM tools: AutoTask and PRTG are named for code repos. The Power Platform clients are still unknown. `CLAUDE.md` updated.

Open items added: how to export from AutoTask and PRTG for a manual run (nobody has said). Whether the plan's `triage-inbox` and `Custom.TriageSource` picklist (service desk, Teams, alert, ADO) should add AutoTask and PRTG as sources. Not changed.

Then (Session 2, eighth request), decisions by Boroon:
- **Reviewed and approved for merge:** the `getai-*` rename, the four `pcp-*` skills, the `Custom.LaneProfile` change to `pro-code`, and the manual-run change to `pcp-triage`. Merged into the default branch `claude/jolly-albattani-818i8e` by a second pull request. Rule 17 is met for every skill in `.claude/skills/`.
- All skills are reviewed but **none has been run**. Reviewed is not the same as tested.

Files changed this session, in total: `skills/` (shelf, 49 copied files plus README), `.claude/skills/` (5 adopted unchanged, `ask-me`, 5 `getai-*`, 4 `lcp-*`, 4 `pcp-*`), `docs/analysis/skills-reading-notes.md`, `docs/sources/plan-v3.1.md` (two lines, pro-code), `CLAUDE.md`, `docs/progress.md`.

Open items still waiting on Boroon: how to export reports from AutoTask and PRTG; whether `Custom.TriageSource` adds AutoTask and PRTG; a real `main` branch (the repo has none, the default is `claude/jolly-albattani-818i8e`); the next skills to read (`unslop`, `principle-*`, `poteto-mode`, `grilling`, `domain-modeling`); fixing the two verification skills so they write to `.claude/skills/` and `lcp-verify`.

Next steps:
1. Boroon reads `docs/analysis/skills-reading-notes.md` and picks adopt, adapt or shelf for each of the 16.
2. Write the GET AI router skill by size (tshirt-sizing step 3), then the first `lcp-*` skills.
3. Update the "Not yet approved" lines in `docs/analysis/tshirt-sizing.md` once Boroon decides.

## Session 1, 2026-11-01, branch `claude/jolly-albattani-818i8e`

Done:
- Added the `/bro` skill at `.claude/skills/bro/SKILL.md`. It is copied unchanged from `cursor/plugins`, `pstack/skills/bro`. It restates the last message in plain language. It only runs when invoked.
- Read and digested, in full: the V3.1 plan, the Spec Kit Part 2 transcript, the Anthropic workshop transcript and Boroon's original Word plan.
- Fixed GitHub push access. The Claude GitHub App was not installed on the repo. Boroon installed it on the one repo. Push now works.
- Built this context structure so work can span many short sessions: `CLAUDE.md` (map), this log, and full sources in `docs/sources/`.
- Boroon re-uploaded five research files. Three were byte-identical to files already saved (Spec Kit transcript, Anthropic workshop transcript, Word plan) and were skipped. The other two, the Tan and Pocock podcast and the Pocock v1.3 transcript, were read in full and saved verbatim.
- Boroon then uploaded two earlier reports, "Grill the Spec, Lock the Tests" and V2.1. Both were read in full and saved verbatim. The main plan supersedes them. They are kept for detail the plan condenses.
- Boroon then uploaded "plan_V3.1_latest" and "plan_V3". The V3.1 file was byte-identical to the copy already saved, so it was skipped. V3 is new. V3.1 is an in-place edit of V3, so a line comparison showed everything unique to V3 is older wording that V3.1 replaced. V3 was saved as a superseded snapshot.
- Boroon then uploaded the Pocock v1.1 transcript, a second copy of the Pocock v1.3 transcript and the Tan podcast (both byte-identical to saved files, skipped), and five research notes. The v1.1 transcript and the notes were saved verbatim under `docs/sources/` and `docs/sources/research-notes/`.
- Boroon added two skills-review transcripts: a review of the pstack skills and a video comparing the packs of Addy Osmani, Matt Pocock and Lauren Tan. Both saved verbatim. Boroon then asked for a comparison. The three repos were cloned into scratch space (not kept) and every skill was listed from them. Two analysis files were written in `docs/analysis/`: `skills-comparison.md` and `tshirt-sizing.md`. Verdicts rest mostly on descriptions and routing documents, not full skill bodies.
- Boroon finally uploaded the full research folder as a zip. Of 43 files, 22 were already in the repo and were skipped, plus two extra copies of the original plan (`uploaded_plan_pandoc.md`, `uploaded_plan_yaml.txt`) whose text matches the version already saved. The new files were added: reports V1 and V2, the runtime and costs note, eight GitHub and Azure notes, five Power Platform notes (including the V3.1 changes brief and the review of the uploaded plan), five workshop slide images, and the engineer one-pager.

Decisions:
- Sessions stay under about 200K tokens. The context file is a short map. Full sources are read on demand by line range.
- Skills live in the repo under `.claude/skills/`, not in a user-level folder.
- **T-shirt sizes approved by Boroon on 1 November 2026:** XS, S, M, L and XL, with the rule that the size is the largest answer across reversibility, blast radius, clarity, verifiability, effort and residency. Summary in `CLAUDE.md`, detail in `docs/analysis/tshirt-sizing.md`. Not yet approved: the skills named for each size, the work-size ADO field, the router skill, and adding the sizes to the plan itself.

Files changed:
- `.claude/skills/bro/SKILL.md`, `CLAUDE.md`, `docs/progress.md`
- `docs/sources/plan-v3.1.md`, `uploaded-plan-software-factory.md` and `.docx`, `transcript-anthropic-agents-run-for-hours.md`, `transcript-spec-kit-part-2.md`, `transcript-tan-pocock-podcast.md`, `transcript-pocock-skills-v1.3.md`, `report-grill-the-spec-lock-the-tests.md`, `report-v2.1-two-lanes-one-gate.md`, `plan-v3.md`, `transcript-pocock-skills-v1.1.md`, `report-v1-fund-nights-on-credits.md`, `report-v2-two-lanes-one-gate.md`, `research-notes/` (19 files in three folders), `workshop-slides/` (five images)
- `docs/one-pager/` (the engineer one-pager as HTML and Markdown)
- `docs/analysis/skills-comparison.md`, `docs/analysis/tshirt-sizing.md`, `docs/sources/transcript-pstack-skills-review.md`, `docs/sources/transcript-skills-comparison-addy-pocock-tan.md`

Open items: see above.

Next steps:
1. Boroon adds more context in the next session. Record it here and in `CLAUDE.md` if it changes a decision.
2. Read the shortlist of skills in full, starting with the first batch in `docs/analysis/tshirt-sizing.md` step 2, once Boroon approves it.
3. Decide the work-size ADO field and the router skill, then add the sizes to the plan if Boroon agrees.
4. Decide the first real build task. The plan's stage 0 and stage 1 are the starting point.
