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

- Mostly documents. The first code, the gate, now lives in its own repo **`GetAI-IP/factory-gates` on `getai.ghe.com`**, branch `release` (moved 3 November 2026, Session 9): stage 1 slice 1 and Builds 1 to 3, 154 tests passing there (gate PR 12, merged 4 November 2026). It has not yet run as a gate on any project repo. No pipelines or GitHub Apps exist yet. The rulesets are files, not applied. **The first tenant objects exist since spike 0.2** (Session 12, 4 November 2026): the Power Platform environment `factory-lane-1` (Sandbox, Managed, Australia, `https://factory-lane-1.crm6.dynamics.com/`) and the Entra app `getai-fl1-exec` with its application user there (System Administrator).
- **Build 1 is done** (Session 6). PR 11 merged into `main` on 3 November 2026.
- **Build 2 is done** (Session 7). PR 12 merged into `main` on 3 November 2026.
- **Build 3 is done** (Session 8). PR 13 merged into `main` on 3 November 2026.
- **The move is done** (Session 9, 3 November 2026): steps 1 to 11 of "Moving to GHE.com" (now in the new repo's README). `factory-gates/` is deleted from this repo: **PR 14 merged into `main` on 4 November 2026**. Step 12, applying the rulesets, is not started. `GetAI-IP` is the central org; four other orgs will use the gate. **Gate work runs from Boroon's laptop:** cloud sessions cannot reach `getai.ghe.com`.
- **Gate upkeep and the self-test workflow** (Session 10) are on `release` in `GetAI-IP/factory-gates`: **PR 7 merged on 4 November 2026**, with `self-test` green on it. The planning record is PR 15, **merged into `main` on 4 November 2026**.
- **The first Dependabot round is done** (Session 11): #1 to #5 in `GetAI-IP/factory-gates` **merged by Boroon on 4 November 2026**, each with `self-test` green. The follow-up, **gate PR 8** (`pin-upkeep`: `setup-node` cache off, tighter pin tests, a Dependabot group for the artifact pair), **merged by Boroon on 4 November 2026**. `release` was then at `d0e19ed`, with 153 tests passing. **Gate PR 12** (.NET `10.0.x` for pac 2.4.1, Session 12) **merged by Boroon on 4 November 2026**: `release` is at `85ad2b5`, with 154 tests passing.
- **Where things live (Boroon, 4 November 2026).** This planning repo stays on github.com, `boroonmahanta/overnight-ai-factory`, for good. Only the workflows and the automation Apps go on `getai.ghe.com`: the gate (`GetAI-IP/factory-gates`), the held-out tests (`factory-holdout`), the caller repos and the GitHub Apps. This replaces the Session 7 note that the planning repo would move to GHE.com when complete. Planning sessions can still run in Claude's cloud; gate work stays on the laptop.
- **Spike 0.2 passed** (Session 12, 4 November 2026): `pac auth create --githubFederated` works on `getai.ghe.com`, both in a job started by hand and inside a ruleset workflow with a `job_workflow_ref` subject. `pac org who` returned the application user both times. Record and portal steps: `docs/plans/spike-0.2/README.md`. The scratch repos `GetAI-IP/oidc-probe` and `GetAI-IP/oidc-probe-target`, the org ruleset `oidc-probe-required` and the two scratch federated credentials were **deleted on 4 November 2026**, at Boroon's word. `getai-fl1-exec` (no credentials now), its application user and `factory-lane-1` stay for the night shift (Stage 3). Planning PR 18 merged into `main` on 4 November 2026.
- **Spike 0.3 passed on both paths** (Session 13, 6 November 2026): Dataverse MCP accepts an app-only token. A job on `getai.ghe.com`, signed in as `getai-fl1-exec` by GitHub OIDC with no secret, made a read and a create through the Dataverse CLI's local proxy and through the remote `/api/mcp` endpoint, once `getai-fl1-exec` was on `factory-lane-1`'s allowed MCP clients list. Record, portal steps and 13 findings: `docs/plans/spike-0.3/README.md`. The two test rows, the scratch repo `GetAI-IP/mcp-probe` and the federated credential `mcp-probe-fl1-exec` are **deleted** (6 November 2026, at Boroon's word). The allowed MCP client entry `new_getaifl1exec` is **kept for Stage 3**, at Boroon's word. The plan is edited for the result (9 lines, Session 13, at Boroon's word). Planning PR 21 merged into `main` on 6 November 2026.
- **Spike 0.18 done: the YAML exit test fails and the XML fallback passes** (Session 19, 8 November 2026, ADO 2462). On a runner, as `getai-fl1-exec` with no secret, on pac 2.14.1 and the gate's pin 2.4.1, `export` then `unpack`, `clone` and `sync` all wrote the XML layout. The XML tree held a table, a cloud flow, a security role, an environment variable and a connection reference; it packed again signed out and with no network; a second export was byte-identical. The plan now makes the XML layout the low-code lane's source format, with the driver running export then unpack (at Boroon's word). Record: `docs/plans/spike-0.18/README.md`. The scratch (repo `GetAI-IP/export-probe`, credential `export-probe-fl1-exec`, solution `FactorySpike` in `factory-lane-1`) is **kept for spike 0.19**, then deleted at Boroon's word.
- **Spike 0.19 passed: the reset returns the lane to its reset commit, byte for byte** (Session 20, 10 November 2026, ADO 2463), in `factory-lane-1` alone, not with 0.10. On a runner, as `getai-fl1-exec` with no secret, a probe-only stand-in for `reset_environment.py` did four things:
  - it imported the reset commit with overwrite and publish, which undid a change to the main flow;
  - it set the lane's environment variable value outside the solution;
  - it found and deleted a flow and a column left in the solution and a flow left outside it;
  - the fresh export, unpacked, equalled the reset commit in all 23 files.

  How to find what the lane identity made outside the solution turned out not to be `solutioncomponent.createdby`: the Default Solution's rows are by SYSTEM. The finder asks each component table for its maker, and finds tables and columns by state against a bootstrap list. The plan is edited for it (11 November 2026, at Boroon's word), with his rule that a table or column found outside the solution stops the lane for a person to check (ADO 2843). Record: `docs/plans/spike-0.19/README.md`. The scratch (0.18's plus one environment variable value) is **kept for spike 0.14**, at Boroon's word.
- **ADO is current** (Session 19): every update Sessions 17 and 18 left is made, and the schedule-order query matches `docs/plans/schedule.md`. Session 20 moved 2463 to Done.
- PR 9 (Session 4) and PR 10 (Session 5) are merged.
- The main plan is V3.1, dated 1 November 2026: `docs/sources/plan-v3.1.md`.
- **The Get AI Engineer's material is assessed** (Session 14, 6 November 2026): `docs/analysis/delivery-vault-assessment.md`. It found the Power Platform standards, patterns and export procedure in the Get AI Engineer's older vault in Azure DevOps, and recommends building live in the lane with the export as the record.
- **Live build is decided (Boroon, 7 November 2026) and edited into the plan** (Session 15). In lane B (low-code), agents build live in the lane. A trusted driver step, not the agent, exports and unpacks the solution, and that export is the PR's source. Builders stay only where Microsoft ships a generator: App Spec, `pac copilot`, code apps, PCF and plug-in source. Pro-code is unchanged. Three spikes must pass before Stage 3: 0.18 (headless YAML export), 0.19 (reset fidelity) and the widened 0.14. `GetAI-IP/factory-gates` now lags the plan; the follow-ups are under Open items.
- Spikes 0.2, 0.3, 0.18 and 0.19 are the only plan items tested on real services. Every other item marked `[untested]` in the plan is still untested. The plan is edited for spike 0.2's result (11 lines, Session 12), spike 0.3's (9 lines, Session 13), the live-build decision (Session 15), spike 0.18's result (Session 19) and spike 0.19's (Session 20), each at Boroon's word.
- **The rest of Stage 1's day gate is planned** (Session 17, 7 November 2026, a cloud session): `docs/plans/stage-1-day-gate-plan.md`, nine build sessions DG1 to DG9 for 2545, 2544, 2546 and 2548 with spike 0.17, dated 12 November to 15 December. Boroon decided D1 to D6, and the plan is edited for them. The gate scripts (2538) wait on spike 0.18.
- **DG1 is done** (Session 18, 7 November 2026, a cloud session, brought forward from 12 November): `staging/` with its README, and `staging/factory-manifestos/` with its README and the three project templates (`glossary.md`, `docs/adr/README.md`, the `coding-standards.md` header). 2545 stays open until DG3 (Friday 20 November).
- Boroon said more context will be added in later sessions.
- Work is sized with T-shirt sizes (XS to XL), approved on 1 November 2026. See `CLAUDE.md`.

## Open items

- **"Agile build v1" differs from plan Appendix D.2** (seen 7 November 2026, Session 15). The process exists in the `getai` organisation, but its User Story states are not D.2's, it has no Spike type, and the D.1 custom fields were not checked. Before Stage 2 changes it, find which projects already use it.
- **The factory's own backlog is in ADO,** project `getai-overnight-ai-factory` (created 7 November 2026, Session 15). Keep it current: at the end of each session, add the session's time and tokens to its stories (`CLAUDE.md`, end step 3), and move the stories it finished to Done.
- **`GetAI-IP/factory-gates` lags the plan after live build** (Session 15, 7 November 2026). A laptop gate slice, by pull request there; Boroon merges. Not started. Before any local check, delete Finder's `.DS_Store` files in the clone. What to change (read from the clone at `85ad2b5`, the same as `release`):
  1. `pending-scripts.txt`: delete `lcp/create_schema.py` and `lcp/create_security.py` (verify-in-test); add `lcp/plan_from_export.py` and `lcp/check_inventory.py` under `# static`. `tests/test_workflow.py` keeps this list and the workflow in step.
  2. `.github/workflows/lcp-gate.yml`, to match plan Appendix A:
     - in `build`, the step name and comment for generator-backed builders;
     - in `static`, `fetch-depth: 0`, the "Export-diff plan against the base commit" step and the `export-plan` artifact;
     - in `verify-in-test`, drop the "Schema and security plan" step and download `export-plan` into `evidence/`;
     - `merge_danger_floor.py` (pre-floor and floor) and `verifier_plan.py` read `--plan evidence/export-plan.json` instead of `--schema-plan` and `--security-plan`.
  3. `lcp/check_builders.py`: narrow it to generator-backed parts. Its docstring still says agents edit per-component builders. Decide how a project declares its generator-backed builders: keep `workflows/build/*.py` as thin wrappers around Microsoft's generators, or use a declared list. Consider failing any builder that writes under `src/`, which only the driver writes now. Update `tests/test_check_builders.py` and the fixture `tests/fixtures/builder-project/`: its builder is a per-component builder.
  4. `README.md`: the rows and findings about per-component builders (the `check_builders.py` and fixture rows, the `build` job steps, and the findings on `workflows/build/`).
  5. `templates/CODEOWNERS`: the commented `/workflows/build/` line. `builders/lib/**` stays protected in `check_protected_paths.py` and `rulesets/protected-paths.json`, as the plan keeps it.
  6. When `lcp/danger-rules.yml` is written: the new B.1 rows and the rule names `export-additive` and `export-flow-logic`.
  7. Regenerate `scripts.sha256` with `lcp/manifest.py` after the script changes.
  8. (Added Session 17, D3.) A job in `lcp-gate.yml` that runs the gate's trusted `spec/check_spec.py` on spec PRs and checks the hash of the copy vendored under `.specify/`. The script itself is built in 2544 (DG5) and reaches `factory-gates` in the move (DG8). For 2538.
  9. (Added Session 19, spike 0.18.) The XML source layout, not YAML: `lcp/pack_offline.py` calls its `--source` "the YAML-format solution folder" (help and docstring), and `lcp-gate.yml`'s `build` step is named "Pack the solution offline (YAML source format)"; plan Appendix A now says "XML source layout". When the manifest check is written, it reads the declared root components from `Other/Solution.xml`; when `danger-rules.yml` is written, its B.1 rows use the XML folders (`Entities/`, `Workflows/`, `Roles/`, `environmentvariabledefinitions/`) and connection references come from the export-diff plan. Consider moving the pac pin from 2.4.1 to 2.14.1 (identical output for the five types tested; read its release notes first, A1). For 2511 and 2538. **Correction from spike 0.19 (Session 20):** `Other/Solution.xml`'s `RootComponents` does not list every root component; in `FactorySpike` it left out the environment variable and the connection reference, which are only in `environmentvariabledefinitions/` and `Other/Customizations.xml`. So the manifest check reads the whole tree, not only `Other/Solution.xml` (`docs/plans/spike-0.19/reset_probe.py`, `read_commit`, does this).
  - **Not on `pending-scripts.txt`:** `export_lane.py`, `reset_environment.py` (now with leftover removal and the proof) and the lane drift check. They run in the execution workflow in `factory-control`, not in `lcp-gate.yml`. They are Stage 3 builds, after spikes 0.18 and 0.19.
- **This planning repo is public** (checked 4 November 2026 with `gh repo view`; a signed-out browser could also open it). Anyone can read the plan, the cost model, the org names, `getai.ghe.com`, the gate's design and the identity names. Boroon to decide. Advice: make it private (Settings, General, Danger Zone, Change visibility). The catch: on GitHub Free, rulesets are not enforced on private repos, so `main` loses its ruleset unless the account is on Pro; with Boroon as the only writer that matters less. Making it private stops new readers but does not undo copies already made.
- **Gate work is laptop work (decided 3 November 2026).** Connecting `getai.ghe.com` to Claude's cloud (Git providers) needs a Claude Team or Enterprise plan, and Boroon is on an individual plan. So any change to `GetAI-IP/factory-gates` runs from his laptop: a local Claude Code session, a cloud session attached to a laptop folder by Remote Control, or a cloud session that prepares a patch he applies (as in Session 9). The steps below are kept only in case a Team plan comes later (the docs cover GitHub Enterprise Server and say nothing about `*.ghe.com`).
  - **The steps** (from https://code.claude.com/docs/en/github-enterprise-server, read 3 November 2026; the page covers GitHub Enterprise Server and is silent on `*.ghe.com`). Needs the Owner or Primary Owner role in the Claude org (Team or Enterprise plan) and permission to create GitHub Apps on `getai.ghe.com`. (1) Create the empty private repo `GetAI-IP/factory-gates` (move step 2). (2) claude.ai, Organization settings, Git providers (https://claude.ai/admin-settings/source-control#github-enterprise), GitHub Enterprise section, Connect, "Set up automatically": display name up to 20 characters, hostname `getai.ghe.com`, leave the CA field empty. (3) Continue to GitHub Enterprise, review the pre-filled app, Create GitHub App. (4) Install the app on `factory-gates` only. (5) On claude.ai/code connect your own GitHub Enterprise account from the repository picker, then start a new session with the repo. If the guided redirect is blocked, use "Add manually" (needs app ID, client ID, client secret, webhook secret, private key; copy the webhook URL Claude generates into the app).
  - **Likely trip points, my inference, untested:** the GHE.com API is at `api.getai.ghe.com`, not `/api/v3` as on Server (see `lcp/apply_rulesets.py`), and the page does not say Claude handles that; the app manifest has no Workflows permission, so a push touching `.github/workflows/` (the first push of the split, the step 8 patch) is refused until Workflows read and write is added in the app's settings and approved; an enterprise IP allow list needs Anthropic's outbound IPs; the cloud environment may need `getai.ghe.com` and `api.getai.ghe.com` under Allowed domains.
- **Five orgs, one central gate (Boroon, 3 November 2026).** The enterprise on `getai.ghe.com` is `GetAI`. The central org `GetAI-IP` holds `factory-gates` and the held-out tests (`factory-holdout`). Four orgs will use the gate: `AI-Business-Solutions`, `AI-Managed-Services`, `Cloud-AI-Platforms`, `GetAI-Knowledge`. Org logins have no `_tqa7h098` suffix (checked for `GetAI-IP` by its URL; assumed for the others, check `AI-Business-Solutions` before step 12). **But the OIDC `workflow_ref` claim does carry it** (`GetAI-IP_tqa7h098/oidc-probe/...`, spike 0.2), while `sub` and `job_workflow_ref` do not. Anything that matches on `workflow_ref` must allow for the suffix. The gate is a repo, a workflow file and rulesets, not a GitHub App; its only Apps are the two read-only token Apps. **Design, proposed, not built:** `lcp-gate.yml` becomes a reusable workflow; each of the four orgs gets a small private caller repo that its own `factory-required-workflows` ruleset points at; one `org.json` per org. Until then `rulesets/org.json` and `templates/CODEOWNERS` describe `AI-Business-Solutions`. **Checked:** (b) below is true. `factory-gates` Settings, Actions, Access offers "Accessible from repositories in the 'GetAI' enterprise", now set. Access is allowed only from private repos, so the callers must be private. Still to check: (a), (d), and (c) across orgs.
  - The four checks behind that design: (a) a ruleset can only require a workflow from a repo in its own org, hence the callers (belief); (b) a private reusable workflow can be shared across the enterprise (**checked true**); (c) `job_workflow_ref` in the OIDC token names the central workflow when a caller runs it, so the federated credential pin to `release` still works (**checked true within one org**, spike 0.2, 4 November 2026: a ruleset workflow in `GetAI-IP` running on `oidc-probe-target` called `oidc-probe/.../probe.yml@main`, and `job_workflow_ref` was `GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`; across orgs not tested); (d) whether a token App owned by `GetAI-IP` can be installed on the other orgs, or each org needs its own pair (unknown).
- **Until a second approver exists** (Boroon, 3 November 2026): `release-protection` in `GetAI-IP/factory-gates` has 0 required approvals, and `factory-gates` is excluded from the `GetAI-IP` org ruleset `protect-main`. Rule 17's "reviewed" is self-review meanwhile, so keep write access to Boroon alone. Before step 12 makes the gate required on any org: set approvals to 1, tick "Require approval of the most recent reviewable push", and remove the exclusion. When someone other than Boroon starts working on the factory, also make `self-test` a required status check (see the `self-test` bullet below).
- **Three Dependabot pull requests are open in `GetAI-IP/factory-gates`** (seen 4 November 2026, Session 12, not touched): #9 `setup-python` 5.6.0 to 7.1.0, #10 `setup-dotnet` 5.4.0 to 6.0.0, #11 `codeql-action/upload-sarif` 3.39.1 to 4.39.1. The first five and gate PR 8 (https://getai.ghe.com/GetAI-IP/factory-gates/pull/8) are merged. **For each Dependabot pull request:** read the release notes for every major crossed, check the pin against the tag with `git ls-remote`, see `self-test` green, then merge. Close none.
- **Gate PR 12, merged 4 November 2026: pac needs .NET 10** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/12, branch `dotnet-10`, commit `fa2e92b`, Session 12). pac 2.4.1 (the gate's pin) ships for `net10.0` only (NuGet catalogue, 4 November 2026), but `lcp-gate.yml` on `release` sets up `dotnet-version: 8.0.x` in `build` and `verify-in-test`, which works only if the runner image carries .NET 10. PR 12 moves both to `10.0.x` and adds `test_setup_dotnet_matches_the_pac_pin` (154 tests). `self-test` passed on it (run 36419851); `lcp-gate` red at `map lane` as expected. A trial merge with Dependabot #10 was clean, so merge them in either order. Plan Appendix A already says `10.0.x`. **Boroon merged it at 12:37 UTC** (merge commit `85ad2b5`); the branch went on its own. Done; kept here one session for the record.
- **The follow-ups in `GetAI-IP/factory-gates` are done in PR 7** (Session 10), merged 4 November 2026: README step 9 and the move marked done, the `dependabot.yml` comment, and next slice 2, the self-test workflow.
- **`self-test` is not a required status check** on `release-protection`. **Boroon, 4 November 2026: turn it on when someone other than him starts working on the factory**, with the second-approver changes above. The change: in `release-protection`, add "Require status checks to pass" with the check `self-test`, source GitHub Actions; leave "require branches to be up to date" off. Until then `self-test` is advice, not a lock: a pull request into `release` can merge with it red, so check it is green before merging, Dependabot pull requests included.
- **The allowed MCP client entry for `getai-fl1-exec` stays in `factory-lane-1`** (Boroon, 6 November 2026, Session 13): name `getai-fl1-exec`, unique name `new_getaifl1exec`, enabled. It grants nothing while the app has no credential. At Stage 3, either keep it or replace it with one added by code (a GET AI solution with the `getai` publisher, or `dataverse mcp allow`), and give lanes 2 and 3 theirs the same way. The list as it was before the spike is in `docs/plans/spike-0.3/README.md`, step B.
- **Dataverse MCP billing is unchecked** (spike 0.3). Reads and creates through MCP were not refused, though `factory-lane-1` has no Copilot Credit source. Microsoft says MCP tools are charged in Copilot Credits for agents outside Copilot Studio. Check Power Platform admin centre, Licensing, for any Copilot Credit use by `factory-lane-1` on 6 November 2026, before the night uses MCP.
- **The gate installs Copilot CLI unpinned** (seen in Session 13, not changed): `lcp-gate.yml` on `release`, `verify-in-test`, runs `npm install --global @github/copilot` with no version or hash. Spike 0.3 shows a pattern that works on a hosted runner for a package with no dependencies: fetch the tarball, check it against the registry's `sha512`, `npm install --global --offline --ignore-scripts` from the file. Check first whether `@github/copilot` has dependencies (if so, pin with a lockfile instead). A gate slice, by pull request there.
- **Sources are complete.** Boroon uploaded the whole research folder as a zip. Every file was checked by checksum against the repo, duplicates were skipped, and the rest were added. The other session ("Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`) is no longer needed for sources and can be deleted.
- **Not read in full.** The files added from the zip were saved but not read in this session: the reports V1 and V2, the runtime and costs note, the eight GitHub and Azure notes, the five Power Platform notes and the one-pager. The five workshop slide images were saved but not viewed. The plan condenses most of them. Read one only when a task needs its detail.
- **Decisions still waiting on Boroon** (from `docs/analysis/tshirt-sizing.md`): approve the shortlist of skills to read in full before any are adopted (plan section 8.3); decide whether to write a GET AI router skill that routes by size. The sizes themselves are approved, and the ADO field `Custom.WorkSize` is decided (7 November 2026, Session 16).
- **A second approver is needed by Friday 4 December 2026** (Session 16 schedule). 2520 (undo the stopgaps) and 2521 (apply the rulesets) need a second person and the three CODEOWNERS teams; without them the Stage 1 exit test (2539, Friday 18 December) cannot happen. The dated order is in `docs/plans/schedule.md`.
- **Spike 0.20, time and tokens per story on every engine, is not run** (Session 16). ADO story 2738 under Feature 2737 (Stage 1). It needs Claude Code's OpenTelemetry turned on through managed settings and somewhere to send it: Application Insights does not exist yet, so use a local collector first. The docs do not say whether the VS Code extension or the desktop app export it; this session runs in the desktop app, so test there first.
- **Keep pinned kits current (A1, Boroon, 7 November 2026, Session 17).** Spec Kit moved three releases in five days. Proposed shape in `docs/plans/stage-1-day-gate-plan.md`: a pin register, Dependabot where the ecosystem allows, and a monthly manual pass at the component register review (plan 8.2), the first with the Ignite re-check on 23 November. Not built; an ADO story is to be created.
- **Done: transcript retention is 365 days** (Session 19, 8 November 2026, Boroon's choice): `"cleanupPeriodDays": 365` in `~/.claude/settings.json` on the laptop. Found while checking: Claude Code keeps sessions started or last continued in the desktop app at any age unless `desktopSessionCleanupPeriodDays` or a managed `cleanupPeriodDays` is set, so the 30-day limit hit only terminal sessions (transcripts from 5 August were still on disk). `0` is refused with a validation error. Kept here one session for the record.
- **Spike 0.18's and 0.19's scratch is kept for spike 0.14** (Boroon, 8 November 2026, then 10 November 2026). What it holds:
  - the repo `GetAI-IP/export-probe`: its `fl1-exec` environment and runs, and since 0.19 also `reset.yml`, `reset_probe.py`, `lane/fl1.json` and the reset commit `reset-commit/`;
  - the federated credential `export-probe-fl1-exec` on `getai-fl1-exec`;
  - in `factory-lane-1`: the publisher `factoryspike`, and the solution `FactorySpike` with its table, flow, role, environment variable and connection reference;
  - since 0.19, one environment variable value for `fspk_SpikeSetting`, outside the solution.

  The lists and how to delete each are in `docs/plans/spike-0.18/README.md` and `docs/plans/spike-0.19/README.md`; 0.18's teardown also takes the value. Delete all of it together after 0.14, at Boroon's word.
- **A table or column outside the lane solution stops the lane** (Boroon, 10 November 2026; plan 5.4 step 4). Metadata keeps no maker, so the reset never deletes one that the bootstrap list does not hold: the lane goes Offline, an ADO bug names it, and a person checks by day. **ADO 2843** builds that check (the bug, a runbook, one trial in `factory-lane-1`). It sits under 2575 "Execution workflow and driver" (Stage 3), after 2577 (`reset_environment.py`); not dated, like the rest of Stage 3.
- **Two things for `reset_environment.py` to learn** (Session 20, not built). It cannot find forms or canvas apps by maker (no `createdby` on their tables), and it must allow the lane manifest's own environment variable values, or step 4 deletes what step 3 set. Both are in the 0.19 record.
- **Keep spike runs in one session.** In Session 19 a "btw" side chat on the laptop started its own setup run in `GetAI-IP/export-probe` (run 37180986) while the main session was running the probe. It queued behind the probe and changed nothing (setup only makes what is missing), but two sessions driving one scratch repo and lane can step on each other. Session 20 kept every run in one session; 0.19's workflow shares 0.18's concurrency group, so runs queue.
- **Fixed: the skill's glossary example broke its own rule** (found and fixed in Session 18, at Boroon's word). In `.claude/skills/getai-domain-modeling/glossary-format.md`, the example term "Customer" had no `_Schema_` line, though the rules say every term has one. It now has `_Schema_: none yet`. It reaches `main` when Boroon merges the Session 18 branch (rule 17). The DG1 template does not use that term, so it needed no change. Kept here one session for the record.
- **Gotcha: the two copies of the glossary and ADR formats split on Friday 4 December** (found in Session 18). Until then the skill (`.claude/skills/getai-domain-modeling/`) and the templates (`staging/factory-manifestos/templates/project/`) sit in this repo, so one PR changes both, as the staging rules say. After the move (DG8) the templates are in `GetAI-IP/factory-manifestos` on GHE and the skill stays here, so one PR cannot change both and the copies can drift. DG8 settles how to keep them the same, for example two PRs that link each other (step 5 of DG8 in `docs/plans/stage-1-day-gate-plan.md`).
- **One checkout, two sessions** (found in Session 21, 10 November 2026). Session 20 (spike 0.19) and Session 21 (the dashboard) ran from the same folder. At 18:28 on 9 November, Session 21 made its branch with `git switch`, which moved the folder off `claude/session-20-2463-reset-fidelity`. Session 20 had no commits and no file changes then, so nothing was lost. At 09:58 on 10 November the folder went back to Session 20's branch, and Session 21 moved to its own worktree. **Session 20: run `git status` and `git branch --show-current` before you commit.** For later: when two local sessions run at once, give the second its own worktree.
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The zip copy is the same, so the source itself is cut off.
- **Credit funding: accepted (Boroon, 2 November 2026).** Builds for customers can be made on credits. Settled.

## Log

## Session 21, 2026-11-09 to 10, branch `claude/session-21-progress-dashboard`

A progress dashboard for the factory build. A local session on Boroon's laptop, the same chat as Session 16, started from `main` at PR 30's merge (`1176ce4`). It ran while Session 20 (spike 0.19) was open; see "One checkout, two sessions" under Open items.

Done:
- Boroon asked for a page that updates as the project moves, with a button to sync it. Made from the claude.ai Dashboard type: **Factory build progress**, https://claude.ai/artifact/DraME5jmLBvouXuH1Kvkk1, private. It uses the visual-analysis layout Boroon picked on the empty page.
- Claude.ai has no Azure DevOps or GitHub connector, so the page can't run a live query. Its data is a snapshot:
  - new `tools/progress_snapshot.py`: every Epic, Feature and User Story read with `az boards query` (Boroon's sign-in), each story's stage taken from its Epic, plus the Track column of `docs/plans/schedule.md`;
  - `tools/session_usage.py --json`: every session's time and tokens as rows.
- The first snapshot is uploaded: 137 stories (34 scheduled) and 19 laptop sessions.
- What the page shows, the Sync button, and the four sync steps: `docs/plans/progress-dashboard.md`.
- `CLAUDE.md` end step 3 now also syncs the dashboard. The repo table has a row for the new note.
- Not checked: the page rendering. The dashboard writes a check after it loads, and none had come back. Boroon to open it and say if anything looks wrong.
- Interrupted once: the first run of the snapshot script lost its permission prompt when the app restarted. It ran fine on the retry.

Decisions:
- Data from a laptop snapshot, not a live query, until claude.ai has a connector for ADO or GitHub.
- The Sync button reloads the newest snapshot. It cannot reach ADO itself, and the page says so.

Files changed: new `tools/progress_snapshot.py`, `docs/plans/progress-dashboard.md`; `tools/session_usage.py` (`--json`), `CLAUDE.md`, `docs/progress.md`.

- **Daily sync set up** (Boroon said "Yes, daily sync", 10 November 2026). It's a scheduled task in the desktop app, `factory-progress-sync`, every day at about 7:30. It runs the snapshot from a temporary detached worktree, so it never moves the shared folder's branch. Then it uploads the two files, points the datasets at them and deletes the old ones. The script gained `--transcripts` for that. First run started by hand at about 10:15 on 10 November, so its tool approvals get saved. Details in `docs/plans/progress-dashboard.md`.

Open items:
- No ADO story for this work yet.

Next steps:
1. Boroon: open the dashboard and check it; review this branch, and ask for a pull request when ready.
2. Each laptop session: sync the dashboard at the end (`CLAUDE.md`, end step 3). The daily task covers the days with no session.
3. If the daily sync fails, run `az login` on the laptop, then Run now on the task.

Later (10 to 11 November 2026, same chat and branch):
- **10 November:** in the first run, Boroon stopped the task from deleting the two old snapshot files, and kept them to review (a memory note on the laptop). The task still said to delete until 11 November.
- **11 November, Boroon: "sync button is not working".** What was wrong:
  - **The sync stopped at a prompt.** The 7:30 run started at 10:03 (the app was closed at 7:30). It took the snapshot, then stopped at the permission prompt for the upload. The prompt was interrupted, and the run still shows as succeeded. So the page kept the 10 November snapshot.
  - **The button gave no sign.** Sync only reloads the newest uploaded snapshot. With no newer one, a click looked like it did nothing.
- **Fixed:**
  - `tools/progress_snapshot.py` stamps every story row with `snapshot_at`, the time the board was read.
  - The page shows "Board read at ..." next to Sync. After a click it says "Newer snapshot loaded" or "No newer snapshot yet", and the button is disabled only while a sync runs.
  - A fresh snapshot is on the page: 138 stories, 3 of the 34 scheduled ones done (2543, 2462, 2463), and 21 sessions. The old files are kept.
  - The dashboard's own check passed (no errors, no blank charts, no overlapping labels).
  - The scheduled task's prompt no longer deletes. It reports which step didn't finish, if any.
  - `docs/plans/progress-dashboard.md` covers the board-read time, the approvals and the no-delete rule.
- Merged `origin/main` (Session 20, PR 31) into this branch. The only conflict was in this log, and both entries are kept.
- Open item: the next run may ask for approval again. Pick the option that remembers it.

## Session 20, 2026-11-09 to 11, branch `claude/session-20-2463-reset-fidelity`

Spike 0.19 (ADO 2463), on its target date. **A local session on Boroon's laptop**, in the desktop app. Started from `main` at PR 30's merge (`1176ce4`); local `main` was fast-forwarded first. Finder's `.DS_Store` files were deleted before any local check. The app was quit overnight and the session resumed on 10 November; the plan edits followed on 11 November.

Done:
- **Looked up first:**
  - `solutioncomponent` has `createdby`;
  - a component made without a solution context goes only into the Default Solution;
  - `pac solution import` has `--force-overwrite` and `--publish-changes`;
  - in 0.18's export, `Other/Solution.xml` left out two root components.
- **The probe**, in the scratch repo `GetAI-IP/export-probe` next to 0.18's: `reset.yml`, `reset_probe.py` (a probe-only stand-in for `reset_environment.py`, not a gate script), `lane/fl1.json` (a stand-in lane manifest) and `.gitattributes`. Modes: baseline, plant, reset, unplant (not run). Local checks first, against 0.18's export and a fake lane, repeated after each change.
- **Five runs**, every one in this session:
  - 37428706, baseline: the finder built on `solutioncomponent.createdby` was blind (finding 3);
  - 37558056, baseline: the rebuilt finder, which met a recycle-bin row;
  - 37558641, baseline: clean. Its export became the reset commit `0c6e2d5`, and it was byte for byte the same as 0.18's;
  - 37559106, plant;
  - 37559661, reset: **pass**.
- **Read-only checks under Boroon's sign-in**, to find out why run 1 saw nothing:
  - the Default Solution's rows are by SYSTEM;
  - the platform adds Default-only rows on its own;
  - the lane holds 14 unmanaged custom columns of Microsoft's own;
  - `solutioncomponentdefinitions` maps 220 component types to their tables;
  - the `entity` and `attribute` tables keep no maker.
- **Result** (`docs/plans/spike-0.19/README.md`, 12 findings):
  - the export after the reset equalled the reset commit byte for byte, all 23 files;
  - the import alone undid the flow change but left all three leftovers;
  - step 4 found and deleted them;
  - the environment variable value stayed out of the solution.
- `docs/plans/spike-0.19/`: `README.md`, and copies of `reset.yml`, `reset_probe.py` and `lane-fl1.json` as run (scratch repo at `0c6e2d5`).
- Tidy-up: spike 0.18's compiled `__pycache__/export_probe.cpython-315.pyc` was committed to `main` by mistake; removed, and a `.gitignore` now ignores `__pycache__/`.
- ADO: 2463 Done, with the result and the time and tokens in its body.
- `docs/plans/schedule.md`: 2463 done Tue 10 Nov; nothing moves.
- **Plan edits** (`docs/sources/plan-v3.1.md`, now 2,722 lines), at Boroon's word (11 November 2026):
  - 5.4: bootstrap step 7 (the bootstrap list); reset step 3 (values outside the solution); step 4 (how leftovers are found, the brakes, and the rule that a table or column outside the solution stops the lane for a person); step 5 (byte equality, a clean second pass, the result);
  - 5.6: the manifest check reads the whole XML tree; the lane drift check runs the reset's finder;
  - 11.1 row 0.19 (run and passed), 12 risk 17 (lowered), 14.4 (a new row "Reset and leftover removal") and 15.1 (the reset question settled; the 0.14 question on its own row).
- ADO **2843** "Human check when the reset finds a table or column outside the lane solution": a User Story under 2575, predecessor 2577, related to 2463, Proposed, tagged `factory-build`, `lcp`, `stage-3`, `session-20`.
- `docs/plans/spike-0.19/README.md`: its plan section now says what was edited, and Boroon's rule.
- `CLAUDE.md`: a row for `docs/plans/spike-0.19/`, the 0.18 row's scratch note, the open questions, the plan row and the line map (the plan grew 12 lines).

Decisions (Boroon):
- Plant two leftovers inside the solution, a flow and a column, in the same run (9 November 2026).
- Keep 0.18's and 0.19's scratch for spike 0.14, then delete it together (10 November 2026).
- Edit the plan for spike 0.19 (11 November 2026).
- A table or column found outside the lane solution, not on the bootstrap list, stops the lane for a person to check, rather than being deleted; add an ADO story for the check (11 November 2026). It is 2843.

Files changed: `docs/plans/spike-0.19/README.md`, `reset.yml`, `reset_probe.py` and `lane-fl1.json` (all new); `.gitignore` (new); `docs/plans/spike-0.18/__pycache__/export_probe.cpython-315.pyc` (deleted); `docs/sources/plan-v3.1.md`; `docs/plans/schedule.md`; `CLAUDE.md`; `docs/progress.md`.

Time and tokens (in 2463's body; session `47db9c0a`, measured before the closing commit): active time 1 h 20 min (gaps over 10 minutes not counted), from 09 Nov 09:28 to 11 Nov 18:23 (UTC+11). Tokens: 172,927 output; 37,832,978 processed in all, of which 35,726,883 were cache reads. From 1 local transcript. It covers the spike, the plan edits and making 2843; no other story was worked.

Open items:
- ADO 2843, the human check (Open items).
- The scratch, kept for 0.14 (Open items).
- Not tested in 0.19:
  - step 1 (test data);
  - a resume from a branch head;
  - a connection reference bound to a connection;
  - the refusal paths and a metadata stray on the real lane;
  - forms and canvas apps;
  - an environment variable value already in the solution;
  - running with 0.10.

Next steps:
1. Boroon: review this branch. A pull request when he asks.
2. Wed 11 and Thu 12 Nov are free on the laptop track. Thu 12 to Fri 13 Nov, documents: 2549 (cloud). Fri 13 Nov, laptop: 2433 and 2505.
3. Mon 16 to Tue 17 Nov, laptop: spike 0.14 (2461), reusing the scratch; then delete 0.18's and 0.19's scratch at Boroon's word.

## Session 19, 2026-11-08, branch `claude/session-19-2462-yaml-export`

Spike 0.18 (ADO 2462), two days early, plus the ADO updates the two cloud sessions left and the transcript retention setting. **A local session on Boroon's laptop**, in the desktop app. Started from `main` at PR 29's merge (`22ae1b6`); local `main` was behind and was fast-forwarded first. Finder's `.DS_Store` files were deleted before any local check.

Done:
- **ADO** (`getai-overnight-ai-factory`), Session 17's list with its item 2 replaced by Session 18's:
  - 2543 Done, dated Sat 7 Nov, predecessor link from 2462 removed, body added.
  - 2545 in progress ("Building", the process's in-progress state), Start Sat 7 Nov, Finish Fri 20 Nov, body added.
  - Bodies added to 2466 (DG2), 2544 (DG4 and DG5; title now "Pin Spec Kit 1.3.x; GET AI and getai-lcp presets v0"), 2546 (DG7 and DG9, D4, D6), 2548 (DG6, D5), 2538 (the `check_spec.py` job) and 2539 (Northwind, D6).
  - 2546 gained predecessors 2541 and 2538.
  - New **2739** "Move the staged day-gate files to GetAI-IP (DG8)", under Feature 2542, Fri 4 Dec, predecessors 2544 and 2546, successor 2539. New **2740** "A1: keep pinned kits current", under 2542, Proposed, no dates. Both tagged `factory-build`, `stage-1`, `session-17`.
  - 2549 to Thu 12 to Fri 13 Nov (Session 18).
  - The schedule-order query (User Stories with a Start Date, by start then finish): all 34 come back with the same dates as `docs/plans/schedule.md`. The only order differences are same-day ties and the two done stories that sort first.
- **Transcript retention:** `"cleanupPeriodDays": 365` in `~/.claude/settings.json` (Boroon chose 365 days; the other options were 3650 and 120). Desktop-app sessions were already kept at any age (Open items).
- **Spike 0.18, `docs/plans/spike-0.18/`** (new: `README.md`, `probe.yml`, `export_probe.py`):
  - Looked up first: Microsoft's pages disagree on which commands write YAML; the gate's pac pin (2.4.1) is ten releases behind the latest (2.14.1, 21 October 2026); pac 2.14.1's packager reads YAML but has no code that writes it.
  - Scratch repo `GetAI-IP/export-probe` (private, repo 5352096) with one workflow and one standard-library script, modelled on spike 0.3. Modes: claims, setup (the test solution made through the Web API as the lane identity, at Boroon's choice "By code"), probe (a matrix over pac 2.14.1 and 2.4.1), envvar-repro, teardown (not run).
  - Local checks first, with a stand-in `pac` around the laptop's real pac: one bug found and fixed before any run.
  - Boroon added the federated credential `export-probe-fl1-exec` in Entra; read back before use.
  - Six runs (37178901, 37180581, 37180771, 37180916, 37181326, 37181366), plus one setup run (37180986) from a side chat. Run 2 failed in the probe's own code (no URL encoding) before any write.
  - **Result:** no headless pac command writes YAML, on either version. The XML layout passes every other check: all five parts present, pack signed out and with no network, unpack of the repack equal to unpack of the export, a second export byte-identical. `clone` is export plus unpack with a project file. pac 2.14.1 and 2.4.1 wrote identical files.
  - **Found on the way:** a Web API update of only `description` on an environment variable definition clears its `defaultvalue` (reproduced as the lane identity; the default is restored). Pack re-serialises `solution.xml` and `customizations.xml`, so compare unpacked trees, never zips.
- **Plan edits** (`docs/sources/plan-v3.1.md`, now 2,710 lines), at Boroon's word ("Yes, edit now"): 5.6 (the XML layout for the low-code lane, the export result, the driver runs export then unpack, the manifest check for XML), 8.1, 11.1 row 0.18, risk 12, 14.4 (a new row), 15.1, Appendix A (the pack step's name), B.1 (the XML folders), C.1 (send the default value with any environment variable update).
- `CLAUDE.md`: the plan row, a row for `docs/plans/spike-0.18/`, the line map, the live build term, risk 12 and the open questions.
- `docs/plans/schedule.md`: 2462 done Sun 8 Nov; 2463 moved to Mon 9 to Tue 10 Nov; the retention checkpoint done; 2739 and 2740 named; a "Changes" line. ADO: 2462 Done and dated Sun 8 Nov; 2463 dated Mon 9 to Tue 10 Nov.

Decisions (Boroon, 8 November 2026):
- Transcript retention 365 days.
- The spike's test solution is made by code, as the lane identity.
- Edit the plan now for spike 0.18: the XML layout in the low-code lane, export then unpack, the environment variable rule.
- Keep the spike's scratch until spike 0.19 is written up.
- Move spike 0.19 forward to Mon 9 to Tue 10 Nov.

Files changed: `docs/plans/spike-0.18/README.md`, `docs/plans/spike-0.18/probe.yml`, `docs/plans/spike-0.18/export_probe.py` (all new), `docs/sources/plan-v3.1.md`, `docs/plans/schedule.md`, `CLAUDE.md`, `docs/progress.md`. Outside the repo: `~/.claude/settings.json` on the laptop.

Time and tokens (in 2462's body; this session `07d7caa1` and the side chat `980641b4`, measured at close): active time 1 h 16 min (gaps over 10 minutes not counted), from 08 Nov 16:26 to 08 Nov 17:54 (UTC+11). Tokens: 158,231 output; 41,984,993 processed in all, of which 41,230,181 were cache reads. From 2 local transcripts. The ADO updates and the retention setting are counted in it; no other story was worked.

Open items:
- `factory-gates` follow-ups for the XML layout (Open items, the `factory-gates` list, item 9).
- The spike's scratch, kept for 0.19 (Open items).
- Not tested in 0.18: managed export, canvas apps, model-driven apps, plug-ins, agents, large solutions, and whether XML pack drops a component silently.

Next steps:
1. Boroon: review this branch. A pull request when he asks.
2. Mon 9 to Tue 10 Nov, laptop, **Session 20**: spike 0.19 (2463), reset fidelity, reusing `GetAI-IP/export-probe` and the `FactorySpike` solution as the baseline. Read plan 5.4 (line 487, the reset and its proof at line 543) and the 0.19 row (line 1437). Then delete the 0.18 and 0.19 scratch at Boroon's word.
3. Thu 12 to Fri 13 Nov, documents: 2549 (cloud). Wed 11 and Thu 12 Nov are free on the laptop track.

## Session 18, 2026-11-07, branch `claude/session-18-2545-templates`

DG1 of the day-gate plan: the templates half of ADO 2545, brought forward from Thursday 12 November. **A cloud session**, started from `main` at PR 27's merge (`aae617e`). It could not reach `getai.ghe.com`, the tenant or Azure DevOps, and did not try. Boroon followed on his phone. The session opened on another of his repos; this one was attached at his word.

Done:
- Read `CLAUDE.md`, this log (current state, open items, Session 17), `docs/plans/schedule.md`, `docs/plans/stage-1-day-gate-plan.md`, plan 6.2, 5.10 (standards pass), 5.12, the protected paths (5.7 and Appendix B.1), the executor and reviewer prompts (Appendix C), and the two format files in `.claude/skills/getai-domain-modeling/`.
- **New `staging/README.md`:** what the folder is, where each part moves on Fri 4 Dec (DG8), and the folder's rules.
- **New `staging/factory-manifestos/README.md`:** what the repo will hold (plan 5.12), what is here and which DG builds the rest, and how a project repo takes the templates: copied in at the same paths by a reviewed daytime PR, into protected paths, with the template notes deleted.
- **New templates in `staging/factory-manifestos/templates/project/`:**
  - `glossary.md`: the skill's format with one example term (Invoice, from the skill's own example). A template note at the top gives the `_Schema_` line for low-code, pro-code and "none yet", and is deleted on copy.
  - `docs/adr/README.md`: the skill's ADR format and the three tests. No `0000` record; records start at `0001`.
  - `coding-standards.md`: the header only. Who reads the file, "rule" items as gate lints that can raise the floor, "judgement" items for the reviewer, protected and changed only by a reviewed daytime PR, kept out of `AGENTS.md`. No entry format: DG3 takes the Get AI Engineer's format as it is.
- **Checked "Done when":**
  - A diff against the skill's files: the glossary body is the skill's block with two of its three example terms left out. The ADR README differs from `adr-format.md` in three places only: the title, with a one-line intro added; the "create the folder lazily" line, replaced by "no example record" and the protected-path line; and the heading "When to write an ADR" (was "When to offer an ADR").
  - A search of `staging/` found no client, person or engagement names.
- `docs/plans/schedule.md`: DG1 done on Sat 7 Nov; 2545 now starts Sat 7 Nov and still finishes Fri 20 Nov; a "Changes" line.
- `docs/plans/stage-1-day-gate-plan.md`: DG1's date and a done line.
- `CLAUDE.md`: the day-gate plan row's dates, and a row for `staging/`.
- This log: Session 17's next steps now name the Monday laptop session as Session 19.

Decisions:
- None asked. One choice taken from the sources, for Boroon to change in review if he wants: **when a project copies each template.** `glossary.md` when the first term is resolved and `docs/adr/README.md` with the first record (the skill creates both lazily); `coding-standards.md` at project set-up, because the reviewer reads it on every PR (plan 5.10).

Files changed: `staging/README.md`, `staging/factory-manifestos/README.md`, `staging/factory-manifestos/templates/project/glossary.md`, `staging/factory-manifestos/templates/project/docs/adr/README.md`, `staging/factory-manifestos/templates/project/coding-standards.md` (all new), `docs/plans/schedule.md`, `docs/plans/stage-1-day-gate-plan.md`, `CLAUDE.md`, `docs/progress.md`.

Time and tokens: **not recorded.** This was a cloud session, which has no local transcript for `tools/session_usage.py`.

**ADO updates for the next laptop session** (project `getai-overnight-ai-factory`; this session could not reach ADO). Do Session 17's list first, with its item 2 replaced by item 1 here:
1. **2545:**
   - Start Date to Sat 7 Nov 2026 (Session 17's list said Thu 12 Nov). Finish Date stays Fri 20 Nov.
   - State to the process's in-progress state. Done after DG3.
   - Add to its body: "DG1 (templates) done 7 November 2026 in Session 18, a cloud session, brought forward from 12 November. Output: `staging/README.md`, `staging/factory-manifestos/README.md` and `staging/factory-manifestos/templates/project/` (`glossary.md`, `docs/adr/README.md`, the `coding-standards.md` header). Branch `claude/session-18-2545-templates`. Time and tokens: not recorded; cloud session, no local transcript. DG3 (the standards seed, laptop, Fri 20 Nov) finishes the story."
2. Then re-run the schedule-order query (Session 17's item 11) and check it matches `docs/plans/schedule.md`.

Open items:
- **Thu 12 Nov's documents slot was free.** Boroon moved 2549 (third-party skills policy) into it, later in this session: see below.
- **The skill's glossary example breaks its own rule.** In `glossary-format.md`, the term "Customer" has no `_Schema_` line, though the rules say one per term. Not changed here (rule 17). The template does not use that term.
- **"Change both in the same PR" stops working after DG8.** The skill stays in this repo on github.com; the templates move to `GetAI-IP/factory-manifestos` on GHE. DG8 should decide how to keep them in step, for example paired PRs that link each other.

Next steps:
1. Boroon: review this branch. A pull request when he asks.
2. Monday 9 November, laptop, **Session 19**: the ADO updates from Sessions 17 and 18, and raise `cleanupPeriodDays`, at Boroon's word. Then spike 0.18 (2462), then 0.19 (2463), on `claude/session-19-2462-yaml-export`.
3. Next on the documents track: 2549 on Thu 12 and Fri 13 Nov (moved, see below), a cloud session. Then DG3 on the laptop on Fri 20 Nov.

Later (same session, at Boroon's word: "make sure we have these two gotchas recorded"): the skill's missing `_Schema_` line and the split of the two format copies after 4 December are now in Open items at the top of this file. The second is also step 5 and the "done when" of DG8 in `docs/plans/stage-1-day-gate-plan.md`, and both staging READMEs say the "same PR" rule holds only until the move.

Later again (same session, at Boroon's word: "add the Customer fix to this branch"): `.claude/skills/getai-domain-modeling/glossary-format.md` now gives the example term "Customer" the line `_Schema_: none yet`. That closes the first gotcha. The template needed no change.

Then Boroon merged PR 28 (https://github.com/boroonmahanta/overnight-ai-factory/pull/28, merge commit `a5f70e3`), which holds everything above. The branch was restarted from `main` at that merge for the change below.

Later still (same session, at Boroon's word: "move 2549 to Thursday 12 November"):
- `docs/plans/schedule.md`: 2549 now runs Thu 12 to Fri 13 Nov, from Thu 19 to Fri 20 Nov, still two days. It needs nothing first and nothing waits on it. A "Changes" line.
- **One more ADO update for the next laptop session:** 2549, Start Date Thu 12 Nov 2026 and Finish Date Fri 13 Nov 2026 (were Thu 19 and Fri 20 Nov). It has no predecessor or successor links to change. Then the schedule-order query (Session 17's item 11) should still match `docs/plans/schedule.md`.

## Session 17, 2026-11-07, branch `claude/session-17-2543-day-gate-plan`

The rest of Stage 1's day gate planned (ADO 2543, brought forward from 12 November). **A cloud session**, started from `main` at PR 26's merge (`889d7f9`). It could not reach `getai.ghe.com`, the tenant or Azure DevOps, and did not try. Boroon answered on his phone, one decision at a time.

Done:
- Read `CLAUDE.md`, this log (current state, open items, Sessions 15 and 16), `docs/plans/schedule.md`, `docs/plans/stage-1-gate-build-plan.md` (the model for the new plan), plan 5.8, 6.1 to 6.4, 6.6, 6.7, 7.3, 8.2, 8.3 and the 11.1 and 11.2 rows, the assessment's verdicts, timeline and questions, and the delivery vault's standards, operating rules and three templates. Also the live skills `getai-domain-modeling` (its glossary and ADR formats become the templates).
- Looked up facts (sources in the new plan's "Facts checked"):
  - Spec Kit is at 1.3.2 (6 November); 1.2.6 (2 November) is the last 1.2. Presets, extensions, bundles and hooks as documented.
  - Hooks are declared by extensions, not presets.
  - Microsoft's Playwright toolkit is source to reference locally, not an npm package. Its samples test the Northwind Traders solution, and Microsoft advises one worker on a shared environment.
  - Claude Code's `/export` writes plain text, and transcripts are deleted after 30 days by default.
  - Not checked: VS Code and GitHub Copilot chat export. Their docs hosts did not resolve from this session, so spike 0.17 checks them by hand.
- **New `docs/plans/stage-1-day-gate-plan.md`:** nine build sessions in order, DG1 to DG9, each with what to read, the steps and "done when":
  - DG1 Thu 12 Nov, cloud: templates (2545).
  - DG2 Wed 18 Nov, laptop apps: spike 0.17, the export how-to and a restricted SharePoint folder (2466).
  - DG3 Fri 20 Nov, laptop: the 46 standards, anonymised, into a new private `GetAI-IP/factory-manifestos`, and the older vault's retro and design templates read (2545).
  - DG4 and DG5, 23 to 25 Nov, cloud: Spec Kit pin, the two presets, the hook extension, the bundle and the spec check script (2544).
  - DG6, 26 Nov to 11 Dec, four batches: mining (2548).
  - DG7, 30 Nov to 2 Dec, cloud: scenario conventions, the schema and the Playwright kit draft (2546).
  - DG8 Fri 4 Dec, laptop: move `staging/` to GHE.
  - DG9, 14 to 15 Dec, laptop: test the kit in `factory-test` (2546).
  - Also: the exit-test mapping, risks, and what is left for 2538.
- **Plan edits** (`docs/sources/plan-v3.1.md`, now 2,707 lines), at Boroon's word ("Yes, edit now"):
  - 6.1: the Spec Kit pin and the hook's home;
  - 5.8: the server logic row;
  - 5.12: where `factory-manifestos` lives;
  - 11.2: the stage 1 build cell;
  - 14.4: a new row for D1 to D6.
- **`docs/plans/schedule.md`:**
  - 2543 marked done;
  - 2545 split (12 Nov and 20 Nov), so it finishes on 20 Nov, not 17 Nov;
  - 2466 moved to the laptop track;
  - 2544 now pins 1.3.x;
  - 2546 needs 2541 and 2538 too;
  - a new move story on 4 Dec;
  - checkpoints on 9 Nov (transcript retention), 23 Nov (A1's first pass) and 4 Dec (D5 cut-off);
  - a "Changes" section.
- `CLAUDE.md`: where the day-gate files live (D1), the plan row, a row for the new file, the line map (Session 17) and the Spec Kit pin.

Decisions (Boroon, 7 November 2026):
- **D1.** The day-gate files are drafted in `staging/` here and moved to `GetAI-IP` on Fri 4 Dec: presets, templates and conventions to `factory-manifestos`, the spec check and Playwright kit to `factory-gates`. The 46 standards go only to GHE. Accepted: the staged presets stay in this public repo's history.
- **D2.** Pin the newest 1.3.x of Spec Kit, not 1.2.x. Plus action **A1**: keep Spec Kit and the other pinned kits current (shape proposed, not built).
- **D3.** The spec check script is built in 2544 with the presets; its gate job joins the 2538 list (Open items, item 8).
- **D4.** Locked Web API tests are YAML in the workflow scenario schema, read by the trusted runner.
- **D5.** Mining: engineers' sessions first; if fewer than 20 by Fri 4 Dec, Boroon's own top up, at most 10 of the 20.
- **D6.** Microsoft's Northwind Traders sample solution is the test target for the kit and the Stage 1 exit PR.
- Edit the main plan now for D1 to D6 (done, above).

Files changed: `docs/plans/stage-1-day-gate-plan.md` (new), `docs/plans/schedule.md`, `docs/sources/plan-v3.1.md`, `CLAUDE.md`, `docs/progress.md`. `staging/` is not created yet (DG1).

Time and tokens: **not recorded.** This was a cloud session, which has no local transcript for `tools/session_usage.py`.

**ADO updates for the next laptop session** (project `getai-overnight-ai-factory`; this session could not reach ADO):
1. **2543:**
   - State to Done.
   - Start Date and Finish Date to Sat 7 Nov 2026 (were 12 and 13 Nov).
   - Remove its predecessor link from 2462: it no longer waits on spike 0.18.
   - Add to its body: "Done 7 November 2026 in Session 17, a cloud session. Output: `docs/plans/stage-1-day-gate-plan.md`, nine build sessions DG1 to DG9, Boroon's decisions D1 to D6 and action A1. Also updated: `docs/plans/schedule.md`, `docs/sources/plan-v3.1.md` (6.1, 5.8, 5.12, 11.2, 14.4), `CLAUDE.md`. Branch `claude/session-17-2543-day-gate-plan`. Time and tokens: not recorded; cloud session, no local transcript."
2. **2545:** Start Thu 12 Nov, Finish Fri 20 Nov. Body: DG1 (templates, cloud) and DG3 (standards seed, laptop).
3. **2466:** body: DG2; a laptop step (VS Code and the other apps), no tenant. Dates unchanged.
4. **2544:** title "Pin Spec Kit 1.3.x; GET AI and `getai-lcp` presets v0" (was 1.2.x). Body: DG4 and DG5, including the spec check script (D3). Dates unchanged.
5. **2546:**
   - Add predecessor links from 2541 and 2538.
   - Body: DG7 and DG9, on Northwind (D6), API tests as YAML (D4).
   - Dates unchanged.
6. **2548:** body: DG6, the four batches and D5's cut-off. Dates unchanged.
7. **2538:** body: add the `check_spec.py` gate job (Open items, `factory-gates` follow-ups, item 8).
8. **2539:** body: on the Northwind sample solution (D6).
9. **New User Story** "Move the staged day-gate files to GetAI-IP (DG8)":
   - parent: the Feature that holds 2544;
   - Start and Finish Fri 4 Dec;
   - tags `factory-build`, `stage-1`, `session-17`;
   - predecessors 2544 and 2546; successor 2539.
10. **New User Story** "A1: keep pinned kits current":
    - same Feature, Proposed, no dates;
    - tags `factory-build`, `stage-1`, `session-17`;
    - body: the A1 shape from the new plan.
11. Re-run the schedule-order query and check it matches `docs/plans/schedule.md`.

Open items:
- A1 and the transcript retention setting (Open items, top of this file).
- DG2 is the first real check of VS Code and Copilot chat export.
- The project code for the Northwind pilot (for `getai-<proj>-test` and `gate/projects/<proj>/`) is set in 2541.
- The Get AI Engineer's review of the standards seed is asked for in DG3 but does not block it.

Next steps:
1. Boroon: review this branch. A pull request when he asks.
2. Monday 9 November, laptop, **Session 19** (renumbered in Session 18, a cloud session on 7 November that took the number 18): spike 0.18 (2462), then 0.19 (2463), on `claude/session-19-2462-yaml-export`. First make the ADO updates above, and raise `cleanupPeriodDays`, at Boroon's word.
3. Done early: DG1 (2545 templates) ran on 7 November in Session 18, not on Thursday 12 November.

## Session 16, 2026-11-07, branch `claude/session-16-time-tokens`

Time and tokens per story, on every engine, written into the plan. A local session on Boroon's laptop, in the desktop app. Started from `main` at PR 24's merge (`a11c913`).

Done:
- Boroon pasted a note (from another chat) proposing three additions: a rule that every engagement records time and tokens per story; moving `tools/session_usage.py` into the gate repo as a shared tool that writes ledger rows; and a baseline view by size and lane.
- Checked the note against the plan (10.1, 7.2, 11.2 stage 2, Appendix D) and the V2.1 ledger schema. Its gaps are real. Found four more: day spec time was not recorded in ADO (Human Minutes held review and PARK only, while the model counts 30 of 50 human minutes as day spec work); no work size on the story; no story key for day sessions; agent time is not human time. Correction to what I said in chat: the V2.1 `fact_human_time` table already has activities for spec work; only `scenarios` and `park` were missing.
- Checked Claude Code's telemetry in its docs (a helper agent read the monitoring and settings pages, in part): native OpenTelemetry with token use by type and model, a cost estimate, active time split into user and CLI time, an event per API request, custom keys in `OTEL_RESOURCE_ATTRIBUTES`, managed settings for every user, prompts redacted by default. Silent on the VS Code extension and the desktop app. Not checked: the macOS path of the managed settings file.
- Advised against point 2: a laptop tool reads files the engineer controls, so its numbers are self-reported wherever the copy lives, and ledger rows from laptops would mean ledger keys on every laptop. Proposed Claude Code's own OpenTelemetry instead, with the script as the fallback writing a ledger-shaped file for a trusted loader. Boroon said "Yes, as proposed".
- Edited `docs/sources/plan-v3.1.md` (now 2,706 lines):
  - **Rule 13:** every story's time and tokens recorded, by day and night, on every engine.
  - **10.1:** new paragraph "Time and tokens per story, on every engine, from day one": engines with OpenTelemetry send it (Copilot; Claude Code, cited, `[snippet]`); the transcript tool as the fallback, out of the gate repo, with a `fact_usage`-shaped output at Stage 2 and `measure_source = transcript`; the story key from day branches; agent time versus human time.
  - **10.2:** `fact_run` gains engine `copilot-vscode`, `active_user_min` and `active_agent_min`; `fact_usage.measure_source` gains `transcript`; a new `fact_human_time` row (activities `scenarios` and `park`); `fact_outcome.work_size`.
  - **10.3:** the baseline page: per accepted story, by size and profile, at P50 and P80 with the count; under 10 stories is too few to price from (assumed). **10.5:** the pricing rule takes its P80 from that page.
  - **6.4:** day branches carry the ADO ID, for example `<ado-id>-<slug>`.
  - **11.1:** spike 0.20 (run in stage 1). **11.2:** stage 2 build and exit test, stage 4 matrix.
  - **5.11 field list and Appendix D.1:** AI Tokens, Agent Minutes, Human Minutes as the total of Spec, Review and PARK Minutes, and Work Size.
  - **14.4:** a decision row. **15.1:** an open question for spike 0.20.
- Updated `CLAUDE.md` (plan row, tshirt-sizing row, tool row, line map, rule 13, work sizes, stage 0 row, open questions) and `docs/analysis/tshirt-sizing.md` (the field is decided).
- **ADO** (`getai-overnight-ai-factory`): created Feature **2737** "Time and tokens per story, every engine" under the Stage 1 epic (2467), and User Story **2738** "Spike 0.20: Record time and tokens on each story, every engine" under it, Proposed, tagged `factory-build`, `spike`, `stage-1`, `session-16`, related to 2666.
- **Time and tokens** (in story 2738's body, refreshed at close, including the schedule work): active 0 h 41 min, from 11:56 to 12:56 AEDT; 96,087 output tokens; 17,286,969 processed in all, 16,695,128 of them cache reads; one local transcript.

Decisions:
- **Time and tokens per story on every engine** (Boroon, 7 November 2026), as in plan 10.1 and 14.4. The transcript tool stays a fallback and out of the gate repo.
- **`Custom.WorkSize` is added to Appendix D**, which settles that open sizing decision.
- Spike 0.20 sits in the plan's spike table (stage 0 runs alongside stage 1) and in ADO under the Stage 1 epic, as Boroon named it.

Files changed: `docs/sources/plan-v3.1.md`, `CLAUDE.md`, `docs/analysis/tshirt-sizing.md`, `docs/progress.md`, and later the new `docs/plans/schedule.md`. `tools/session_usage.py` is unchanged.

Open items:
- Spike 0.20 is not run (Open items, top of this file).
- The transcript tool's ledger output is a Stage 2 change; not written.
- The "Agile build v1" process does not have the new D.1 fields yet, like the rest of D.1 (a Stage 2 job, after checking which projects use the process).
- The one-pager and the Ways-of-Working page do not mention this. Refresh them only if they are shared again.

Next steps:
1. Done: Boroon merged PR 25 (the plan edits, https://github.com/boroonmahanta/overnight-ai-factory/pull/25) at 12:29 AEDT on 7 November 2026. The schedule commit was pushed after that merge, so it goes in a second pull request.
2. Follow `docs/plans/schedule.md`. Session 17, Monday 9 November: ADO 2462 (spike 0.18), then 2463 (spike 0.19), as a local session on the laptop, on a branch that carries the ADO ID (`claude/session-17-2462-yaml-export`).
3. Spike 0.20 is dated 3 December, after spike 0.6.

Later (7 November 2026, same branch, at Boroon's word in this chat):
- Opened PR 25 into `main` (ready for review). The repo runs no CI on it. Boroon merged it at 12:29 AEDT, with the plan edits only.
- Wrote the message to start Session 17 on ADO 2462 and 2463 (in the chat; the schedule holds the same order).
- Set out the logical order of the 35 open stage 0 and stage 1 stories. Boroon asked for it to be recorded with a date against each, from Monday 9 November 2026.
- **New `docs/plans/schedule.md`:**
  - every open stage 0 and stage 1 story, dated from 9 November, on two tracks: laptop and documents;
  - the Stage 1 exit test (2539) on Friday 18 December;
  - 21 December to 8 January left as buffer and holidays;
  - stage 2 starting Monday 11 January with spike 0.13 (2448), then spikes 0.4 and 0.12 after the Ignite re-check;
  - three checkpoints that are not ADO stories (engineers' session exports by 20 November, the Ignite re-check on 23 November, a second approver and the three CODEOWNERS teams by 4 December);
  - 2450 and 2454 left undated (stages 5 and 6).
- **ADO:**
  - Start Date and Finish Date set on 33 User Stories (09:00 to 17:00 Sydney time);
  - 32 predecessor links added for the real dependencies, as in the schedule's "Needs first" column;
  - checked by a query: all 33 come back in schedule order.
- `CLAUDE.md`: start step 2 points at the schedule, and the repo table has a row for it.

## Session 15, 2026-11-07, branch `claude/session-15-live-build`

The plan rewritten for live build in lane B (low-code). A local session on Boroon's laptop. Started from `main` at PR 23's merge (`1fcac59`), after checking that PR 23 (Session 14) is merged.

Done:
- Read `CLAUDE.md`, the Session 14 entry, assessment sections 3, 3.5 and 7, and the plan parts the change touches. Checked Microsoft Learn for the YAML export doubt: the format reference, the Git integration FAQ and the `pac solution` reference, all cited in plan 5.6.
- Proposed the edits as a list (assessment section 7 items 1 to 7, 11 and 13, plus the lines elsewhere that would contradict the decision). Boroon said "Yes, as proposed", which took my picks on two choices: (A) the plan check diffs the PR's export against its base commit, in `static`, not against Test; (B) fix the contradicting lines now.
- Two of Boroon's forked sessions asked, by message, for two additions, and they were folded in under his yes: a clear definition of "driver" (item 13), and the low-code versus pro-code meanings of "builder" and "driver" (item 14). One claim in the second was corrected against plan 4.2: Lane B's code profile has no trusted driver. The orchestrator dispatches the task, an `agentStop` hook runs the fast checks, and the cloud agent opens its own PR.
- Edited `docs/sources/plan-v3.1.md` in place (now 2,659 lines):
  - **Bottom line and 2.1:** live build in a clause each; rule 5's note.
  - **5.1:** execution and lane-close rows, the flow text, and the new "Driver (low-code lane)" paragraph with Lane A's driver and the code profile.
  - **5.2:** the cloud agent example.
  - **5.4:** the reset gains leftover removal and a proof (export equals the reset commit, else Offline). A story resuming after a PARK or a NEEDS_WORK round resets to its own branch.
  - **5.5:** the per-story row and the gate row.
  - **5.6:**
    - The headless YAML export doubt, with the XML fallback.
    - "Builders and the drift gate" becomes "Live build, export as the record": the driver's export procedure and inventories; builders only for generators; code parts work the pro-code way; builders are low-code only.
    - A new lane drift check: a second export equals the PR head, and no component sits outside the solution.
    - The FlowAgent row and the plugin notes.
  - **5.7:** the `build`, `static` and `verify-in-test` rows. The trusted scripts drop `create_schema.py --plan`, `create_security.py --plan` and `sync_solutions.py`, and add `export_lane.py`, `plan_from_export.py` and a standards lint. The builder-protection paragraph is rewritten.
  - **5.10:** the floor inputs, the spec pass and the never-auto-merge line.
  - **5.11:** a PARK or a safe stop exports the lane first, or the next reset would wipe the work.
  - **5.12:** skills `lcp-live-build` (replaces `builder-pattern`) and `lcp-flow-patterns`, the new rules, and a context cap.
  - **Other sections:** 5.15, 6.3, 6.7, 7.3, 7.4 and 8.2 in wording.
  - **11.1:** spike 0.14 widened; new 0.18 (headless YAML export) and 0.19 (reset fidelity).
  - **11.2:** stages 1 and 3 and the stage 3 drift exit test.
  - **12:** new risk 12 (the YAML export doubt). Old 12 to 32 are now 13 to 33. Old 16 (now 17) is reworded for live build.
  - **14.4:** a new row for the decision, including "nothing changes for pro-code".
  - **15.1:** a new open question for the three spikes.
  - **Appendix A:**
    - The layout note and the job table.
    - In `build`, the step name and comments.
    - In `static`, the export-diff step and artifact.
    - In `verify-in-test`, the Test plan step is gone and the export plan is downloaded.
    - The pre-floor, verifier plan and floor read `export-plan.json`.
    - The YAML still parses (checked with PyYAML in a scratch venv).
  - **Appendices B and C:**
    - B.1 has four low-code rows remapped, plus a note that pro-code rules come at Stage 5.
    - The B.2 heading, B.4, and the B.6 rule names `export-additive` and `export-flow-logic`.
    - C.1 `lcp-executor`: live build, inventories first, flow patterns, no export commands, the loop, commits, the context cap.
    - C.3 reviewer point 1 (the export against `state.md`), and the C.4 layout.
  - **Appendix D:** the D.2 Finding states.
- **Beyond the approved list, small and needed for consistency:**
  - the 5.4 resume rule and the 5.11 export-before-park, without which live build loses parked work;
  - the 15.1 open question;
  - the bottom-line clause;
  - the 6.3 preset line;
  - the B.6 `flow-definition-logic` rename;
  - C.1 saying the agent commits only its own files.
- Kept as history: section 1's V3.1 change list, the 14.1 "builder protection" row, and the older 14.4 Build 3 row.
- Updated `CLAUDE.md`:
  - the plan row, the assessment row and the factory-gates row;
  - the line map (Session 15 line numbers; Appendix A now ahead of `factory-gates`);
  - the plan in brief, plus "builder" changed to "worker" or "executor" where it meant the agent;
  - Terms: Live build, Builder (low-code only), Driver (low-code lane), Driver (Lane A), Pro-code;
  - 33 risks, 19 spikes, and one open question.
- Read-only: the local clone of `GetAI-IP/factory-gates` (`85ad2b5`), to list the follow-ups accurately. Nothing changed there, on `getai.ghe.com`, in Azure DevOps or in the tenant.

Decisions:
- **Live build in lane B (low-code)** (Boroon, 7 November 2026). Agents build live in the lane. A trusted driver step, not the agent, exports and unpacks the solution, and that export is the PR's source. Builders stay only where Microsoft ships a generator: App Spec, `pac copilot`, code apps, PCF and plug-in source.
- The plan check diffs the export against the PR's base commit, in `static` (choice A, Boroon's yes to the proposal).
- "Driver" and "builder" are defined as above; pro-code is unchanged (Boroon's forked sessions, under his yes).

Files changed: `docs/sources/plan-v3.1.md`, `CLAUDE.md`, `docs/progress.md`. The vault copy and the assessment are unchanged.

Open items:
- The factory-gates follow-ups (Open items, top of this file). A laptop gate slice for later.
- Spikes 0.18, 0.19 and the widened 0.14 must pass before Stage 3. If 0.18 fails, the plan's fallback is XML for flows and tables, with canvas apps kept out of the night.
- (Since decided the same day, except item 15; see "Later" below.) Assessment section 7 items 8, 9, 10, 12, 14 and 15 are still proposals (standards seed, `getai-lcp` preset additions, one ADO project per engagement, mining set, "start my day", inventories as a blast-radius input; the last is partly done: the reviewer now reads the inventories).
- The one-pager and the Ways-of-Working page do not mention live build. Refresh them only if they are to be shared again.

Next steps:
1. Boroon: review this branch; a planning pull request when he asks.
2. A spike session in `factory-lane-1`: 0.18 and 0.19 together, then the widened 0.14 (flow by the Web API as `getai-fl1-exec`).
3. The factory-gates slice, on the laptop.

Later (7 November 2026, same branch, each at Boroon's word in this chat):
- **Precedence rule** (sent by a forked session, then agreed here): our plan wins on design. The Get AI Engineer's material is the default source for anything the plan does not settle: use it as it is or with the least change, and do not write our own. Where they clash, ours applies. Anything from the older ADO vault comes over anonymised, by a reviewed PR. Recorded in plan 14.4 and `CLAUDE.md`.
- **Item 10, ADO projects, all lanes:**
  - one ADO project per engagement, on "Agile build v1", and the vault's engagement projects can take it;
  - ADO is GET AI's and holds Kanban boards only;
  - code repos sit on GET AI's GitHub Enterprise, with pipelines and tests on GitHub Actions;
  - a project manifest `gate/projects/<proj>/project.json`;
  - one internal project for the factory's own build.
  Made in plan 6.4, Appendix D, the 5.1 work-queue row and 14.4.
- **Item 8** (low-code): `coding-standards.md` starts from the Get AI Engineer's 46 standards. "Rule" items become lints that can raise the floor; "judgement" items go to the reviewer. Plan 5.10 and 5.12.
- **Item 9** (low-code): five additions to the `getai-lcp` preset in plan 6.3: the values table, names at design time, reference components, the inventory check, and open questions split by who answers.
- **Item 12:** moved out of the current stages into a new last stage, **stage 9, "Learning from past engagements"**, with a mining agent of its own for every engagement type (plan 11.2, 7.3; heading now "Stages 1 to 9").
- **Item 14** (low-code): the delivery vault's "start my day", extended with the least change, is the reviewer's morning entry point (plan 2.1).
- **Item 15:** assessed for low-code and pro-code as a decision matrix in `docs/analysis/delivery-vault-assessment.md` section 10. Not in the plan yet; three decisions are waiting on Boroon. Section 7 of the assessment now has a status note.
- **ADO, read only, through Boroon's Azure CLI sign-in:**
  - No factory project exists in the `getai` organisation yet.
  - **"Agile build v1" exists**, inherited from Agile. Its types are Epic, Feature, User Story, Task, Bug, Risk, Issue and a few custom ones. It has **no Spike type**.
  - **Its User Story states do not match plan D.2.** Live: Proposed, Analysis, Awaiting business, Ready to build, Building, Testing, UAT Ready, In UAT, PROD Ready, In PVT, Blocked, Done. D.2 also has Queued, Awaiting review, Needs rework and Integrated, and has no Analysis, In PVT or Blocked.
  - Other projects may already use this process, so changing it is a Stage 2 job, to check first.
  - The organisation's project list names clients, so it is not copied here.
- **Item 15 decided** (Boroon):
  1. shared use raises the floor to at least 3 in both profiles (plan 5.10, B.1);
  2. pro-code inventories are made by the gate and never committed (plan 11.2 stage 5);
  3. a lint fails any inventory holding a value. Boroon said "agreed, but with reasons"; I read that as a lint whose failure gives its reasons (the entry, why values are barred, the fix), written in plan 5.6. Boroon confirmed this reading the same day.
  Low-code inventories are regenerated by the gate, which fails on a difference (`check_inventory.py` in Appendix A `static`). The B.6 verifier test now uses the inventory's used-by links. 14.4 has a row.
- **The internal ADO project `getai-overnight-ai-factory` is created** (Boroon named it). It is private, on "Agile build v1", through Boroon's Azure CLI sign-in, with Repos, Pipelines, Test Plans and Artifacts turned off, so it holds boards only.
- **The backlog is loaded:**
  - 312 work items: 11 Epics (stages 0 to 9, plus "Planning, research and skills"), 38 Features, 134 User Stories and 129 Tasks.
  - Past work is Done or Closed; future stages, spikes and open items are Proposed or New.
  - All are tagged `factory-build` and `seeded-2026-11-07`; spikes are User Stories tagged `spike`.
  - Drafted by a helper from this log and plan section 11, checked here, then created by a script that makes each item in its starting state and then moves it.
- **Time and tokens per story** (Boroon asked):
  - `tools/session_usage.py` totals them from the local transcripts, with forks and subagents included and duplicates removed. Active time leaves out gaps over 10 minutes.
  - Every story of Sessions 10 to 15 and the Ways-of-Working page has its session's totals in its body.
  - Sessions 1 to 9 ran in Claude's cloud, so their stories say "not recorded".
  - `CLAUDE.md` now has an end-of-session step to do this every time.
  - Session 15's numbers were refreshed at close on its four stories (ADO 2666, 2668, 2674, 2724): active 1 h 21 min, from 09:54 to 11:50 AEDT; 291,012 output tokens; 44,432,129 processed in all, 43,226,145 of them cache reads; from this session and its three forks.
- **ADO check after the load:** all 312 items (IDs 2425 to 2736) match the draft on type, state, title and parent. 26 Stories are Done and 108 Proposed; 78 Tasks are Closed and 51 New.

## Session 14, 2026-11-06, branch `claude/session-14-vault-assessment`

A fresh assessment of the Get AI Engineer's material and the 5 November call, for lane B (low-code). A local session on Boroon's laptop. Started from `main` at PR 22's merge (`63f83f2`), after checking that the Session 13 close-out (PR 22) is on `main`.

Done:
- Read `CLAUDE.md`, this log, the vault copy in full (`docs/sources/delivery-vault/`, 19 files), the call transcript (pasted in the chat, not stored here), plan sections 2, 5, 6, 7.3 and 11 and Appendices C and D, `docs/analysis/tshirt-sizing.md`, and the spike 0.2 and 0.3 READMEs.
- Read-only on `getai.ghe.com`: the vault has moved to `51fdde5` (two commits after our copy, 4 to 6 November: offline HTML onboarding guides, Mac notes, channel naming; nothing on building). No other repo of the Get AI Engineer's. The handbook holds no low-code standards.
- At Boroon's request in the chat, read-only in Azure DevOps: the Get AI Engineer's older Power Platform vault, `getai` organisation, project `GETAI-PowerPlatform`, repo `vault` (`main` at `5f26ede`), and the folder layout of its per-client source repos. It holds the Power Platform material the call described and the GHE vault lacks. Its folder names name clients, so nothing from it is copied here.
- Read Microsoft's `power-platform-skills` (commit `3ffa5b8`) and Microsoft Learn on source control with solution files, the YAML format, `pac solution` and cloud flows by code.
- Wrote `docs/analysis/delivery-vault-assessment.md`, verdict table first: 37 pieces judged (combine, replace, keep ours, gap), an inventory, a recommendation on how agents build, day versus night, dates by scenario, questions for the Get AI Engineer, 15 proposed plan edits, and where it differs from Session 13. The comparison with `delivery-vault-fast-track.md` was written after the draft, as asked.

Findings, in short:
1. **The older ADO vault has what we lack:** 46 Power Platform standards with stable IDs, each marked "rule" (34, for the gate's lints and floor) or "judgement" (12, for the reviewer); 8 flow patterns; an export and unpack procedure with inventories; a design template; full records of the past engagement. Verdict: the standards replace our unwritten `coding-standards.md` seed; the export procedure replaces the plan's thin export step (keeping our YAML format).
2. **How agents build:** recommend building live in the lane through supported tools, with the driver (not the agent) exporting the solution as the PR's source; builders only where Microsoft ships a generator. Microsoft's own source control page does not support editing extracted files. This would drop the per-component builders and their plan checks from the gate's unwritten scripts.
3. **Microsoft's pages disagree** on whether `pac solution unpack`, `clone` and `sync` write the YAML format. A spike is needed before Stage 3.
4. **Microsoft's Power Automate plugin signs in as a user** (`az login` plus MSAL); the canvas plugin needs an open Studio tab. Neither is a safe night assumption. Solution flows can be written through the Dataverse Web API, which Microsoft documents.
5. **New gap:** an unmanaged import does not remove components, so under live build a lane reset must prove the lane equals `integration`.
6. **Dates (estimates):** about one week earlier than the Session 13 baseline. One person: L0 trial week of 30 November, L1 from about 18 January 2027. With a second engineer and the Get AI Engineer's time: L0 about 23 to 27 November, Stage 3 exit about mid-December. The Get AI Engineer's time makes a live-engagement trial possible; it does not much speed the build.

Decisions: none. Everything in the assessment is a proposal.

Files changed: `docs/analysis/delivery-vault-assessment.md` (new), `docs/progress.md`, `CLAUDE.md` (map rows). The plan and the vault copy are unchanged. Nothing changed on `getai.ghe.com`, in Azure DevOps or in the tenant.

Open items:
- **How agents build: Boroon to decide** (assessment section 3). It changes plan 5.4, 5.6, 5.7, B.1 and C.1.
- Which of the 15 proposed plan edits to make (assessment section 7).
- The questions and asks for the Get AI Engineer (assessment section 6), including whether the ADO vault is retired and who owns the standards.
- The vault copy here is at `19877b8`; the source is at `51fdde5` (onboarding guides only). Refresh only if a later session needs them.
- The ADO vault stays in Azure DevOps. It names clients and holds engagement records, so any part the factory takes comes over anonymised, by a reviewed PR (rule 17).

Next steps:
1. Boroon: decide the build method, then which plan edits to make.
2. Boroon: send the Get AI Engineer the section 6 questions and asks.
3. Next spike session: either spike 0.6 (Copilot CLI on GHE.com), or a combined lane spike in `factory-lane-1`: headless YAML export, reset fidelity, and one flow created through the Web API as `getai-fl1-exec` (assessment section 3.4).

Later (7 November 2026, same branch, at Boroon's word):
- Added assessment section 3.5: live build against builders, side by side, 18 factors with green and red markers. Score: live build 10, builders 5, ties 3. Each builder win has a fix under live build, listed below the table.
- Renamed "the author" to "the Get AI Engineer" in the assessment, this entry and its map row, and changed his/him to they/them there. Session 13's file and older entries still say "the vault's author", as written.
4. A planning pull request for this branch, when Boroon asks.

## Session 13, 2026-11-05 to 06, branch `claude/session-13-spike-0-3`

Spike 0.3, Dataverse MCP with an app-only token. A local session on Boroon's laptop. Started from `main` at PR 19's merge (`e9e2741`); PR 19 (the Session 12 close-out) was checked as merged first. The ways-of-working one-pager (next entry) was a side task on the same branch; PR 20 took this branch to `main` up to that commit (`419b101`).

**Result: pass on both paths.** Exit test met (run 36819036, 6 November 2026): a read and a create succeeded headless through the Dataverse CLI's local proxy and through the remote `/api/mcp` endpoint, as `getai-fl1-exec` signed in by GitHub OIDC, no secret. Versions: `@microsoft/dataverse` **1.0.88** (tarball `sha512-QxxPjz7C...I49xWzw==`, the registry's value), pac **2.4.1** on .NET `10.0.x`, Node `lts/*` (v26.13.0). What broke along the way, all fixed in the session: run 2 was refused on both paths until the app was on the allowed list (by design); the first credential save lost the `r` of `repo:`; the allowed-client unique name needed a publisher prefix.

Done:
- Read the Dataverse MCP docs (local proxy, remote endpoint, allowed clients, CLI reference, tools, FAQ, preview tools) and the npm package `@microsoft/dataverse` 1.0.88 in full except its native binaries: no dependencies, no install scripts, a 1 KB launcher that starts a bundled binary, updates only on an explicit `install`.
- Read-only checks in the tenant (Boroon's `az` sign-in): the Dataverse API publishes `user_impersonation` and `mcp.tools`, both delegated, and no app roles; the Dataverse CLI app has no service principal (never consented); `getai-fl1-exec` had no credentials, only Graph `User.Read`.
- Wrote `docs/plans/spike-0.3/probe.yml` (one job, `workflow_dispatch` from `main` only, `id-token: write` and `contents: read`, no secrets; three actions pinned to the gate's commit SHAs, checked with `git ls-remote`; pac 2.4.1 on .NET `10.0.x`; the Dataverse CLI from a tarball checked against the registry's `sha512`, installed offline with scripts off), `mcp_probe.py` (standard library MCP client for stdio and streamable HTTP; never prints a token; clean-up deletes only `spike-0.3 probe` rows this app created) and `README.md` (portal steps, run order, results, findings). 48 local checks against fakes passed; the harness stayed in the scratchpad.
- At Boroon's word: created private `GetAI-IP/mcp-probe` (repo 5331556) and pushed `4ab9682`, then `237ac5b` (the telemetry opt-out). Run 1 (36506161, claims only) passed. Boroon added the federated credential `mcp-probe-fl1-exec` (the first save had `epo:` for `repo:`; a read-back caught it and he fixed it), checked the GA MCP toggle is on, and left the Preview toggle alone. Run 2 (36783926, reads only, `getai-fl1-exec` not yet allowed): both paths refused with 403 by the allowed-clients check. Boroon then added `getai-fl1-exec` to the allowed MCP clients (unique name `new_getaifl1exec`, after `getaifl1exec` was refused for lacking a publisher prefix); read back as enabled, with the right app ID, at 01:10:58 UTC on 6 November.

- Run 3 (36819036, `write=true`, started 03:22 UTC): both paths passed initialize, `tools/list` (15 tools), `read_query` (`SELECT TOP 1 name FROM organization` gave `factory-lane-1`), `create_record` (`account`, `spike-0.3 probe (local)` and `(remote)`) and a read-back. The clean-up step found both rows by name and by `getai-fl1-exec`'s application user as creator, deleted them (HTTP 204) and found none left. Checked again read-only under Boroon's sign-in: no `spike-0.3` row, `account` empty. No token-shaped string in any of the three logs.
- **Clean-up, at Boroon's word:** deleted `GetAI-IP/mcp-probe` after a last look (three files, `main` only, environment `fl1-exec`, no secrets, three runs); it returns 404. Deleted the federated credential `mcp-probe-fl1-exec` with `az ad app federated-credential delete`; `getai-fl1-exec` again has no federated credentials, secrets or certificates. **Kept** the allowed MCP client entry `new_getaifl1exec` for Stage 3 (Boroon's choice).

Findings: the 13 in `docs/plans/spike-0.3/README.md`, "Findings". In short:
1. `/api/mcp` accepts an app-only token with no `roles` or `scp`; tool calls work once the app is on the allowed list. Before that: 403 naming the app, not 401.
2. The allowed list is checked by the token's app ID. The lane's own app needs the entry; the Dataverse CLI app, its consent and its entry are not needed.
3. The local proxy forwards the job's token and shows upstream errors to the client only as `-32603 An error occurred`; keep its stderr in the night's trace.
4. The Dataverse CLI does not see pac's profiles (federated, Linux); `dataverse auth create --githubFederated` works first time.
5. Its token cache is unencrypted on Linux; remove the profile at job end.
6. `dataverse mcp --validate` advises the wrong app for an app sign-in.
7. It sends usage data unless `DATAVERSE_TELEMETRY_OPT_OUT=1`.
8. An allowed MCP client is a solution component (`allowedmcpclient`); its unique name needs a publisher prefix; it can ship in a solution or come from `dataverse mcp allow`.
9. The package pins properly: no dependencies, no install scripts; tarball plus `sha512` plus offline install works; `npx` skips the hash check.
10. Read a federated credential back before the first run.
11. MCP writes are attributed to the lane's application user.
12. The tool list differs from Microsoft's page (no `search_data`, no `invoke_api`, an undocumented `create_skill_resource`); `create_record` takes `item` as an object.
13. Billing unclear: nothing refused without a Copilot Credit source; metering unchecked.

Decisions (Boroon, 6 November 2026): use the GA MCP toggle and leave Preview off; the allowed-clients entry stays for Stage 3; the scratch repo and credential are deleted.

Plan edits, proposed and then **made at Boroon's word** ("Make the edits"), the same session. 9 lines changed in `docs/sources/plan-v3.1.md`, none added (still 2,604 lines), so every line number in `CLAUDE.md` still holds:
- Line 509 (bootstrap step 5): name the lane's execute app as the allowed MCP client; the GA toggle only; the entry's unique name needs a publisher prefix and can ship in a solution or come from `dataverse mcp allow`.
- Line 594 (remote `/api/mcp`): app-only token accepted, no `roles` or `scp` needed, allowed list checked by the token's app ID (spike 0.3); usable from a runner job as the lane's execute identity; still not on the cloud agent.
- Line 595 (local proxy): "Profiles compatible with pac" becomes "own profiles; does not see pac's; `auth create --githubFederated` works on GHE.com"; "After the stage 0 app-only spike passes" becomes "passed 6 November 2026; preview package; pin 1.0.88 by hash; `DATAVERSE_TELEMETRY_OPT_OUT=1`; keep its stderr; remove the profile at job end".
- Line 601 (night default): MCP is cleared for night use as the execute identity; writes stay on pac and trusted Web API scripts until Stage 3 decides; MCP writes are recorded against the lane's application user; drift check unchanged. The line says the fact-lookup question is open. **Still Boroon's call:** whether MCP becomes the night default for fact lookups (lines 846 and 954 already allow it).
- Line 614 (click-ops table, "Enabling features per environment"): the MCP client entry can be code; the feature toggle stays a bootstrap step.
- Line 900 (other meters): spike 0.3's MCP reads and creates were not refused with no Copilot Credit source; metering unchecked.
- Line 1379 (row 0.3): passed 6 November 2026, Session 13, both paths.
- Line 1427 (risk 14): add "Dataverse CLI pinned by tarball hash" to the answer.
- Line 1546 (open question): answered yes, both paths, spike 0.3.

Files changed: `docs/plans/spike-0.3/README.md`, `probe.yml`, `mcp_probe.py` (new), `docs/sources/plan-v3.1.md` (9 lines), `docs/progress.md`, `CLAUDE.md`. On `getai.ghe.com`: `GetAI-IP/mcp-probe` created and deleted. In the tenant (Boroon in the portals): the credential `mcp-probe-fl1-exec` added and deleted; the allowed MCP client `new_getaifl1exec` added and kept. In `factory-lane-1`: two test rows created and deleted. Nothing in `GetAI-IP/factory-gates` changed. Dependabot #9 to #11 untouched. `protect-main`, `release-protection`, the gate's rulesets and the four other orgs untouched. No secrets, no client data. Not recorded in this public repo: the tenant ID, the app ID, and the Dataverse org, user and row IDs (they were in the private run logs, now deleted with the repo).

Open items: the billing check and the kept MCP entry (both in Open items above); whether MCP becomes the night default for fact lookups; the gate's unpinned Copilot CLI install (Open items).

Next steps:
1. Done: the plan edits, at Boroon's word. Still open: whether MCP becomes the night default for fact lookups (Boroon).
2. Boroon: check Copilot Credit use for `factory-lane-1` in the Power Platform admin centre.
3. A planning pull request for this branch, when Boroon asks.
4. The next stage 0 spike in plan 11.1.

Later the same day (close-out, branch `claude/session-13-close-out`, from `main` at PR 21's merge, `47ead67`):
- **Boroon merged planning PR 21** (https://github.com/boroonmahanta/overnight-ai-factory/pull/21) at 06:02 UTC: runs 2 and 3, the findings, the clean-up record and the nine plan edits.
- **Where the build stands, 6 November 2026.** Stage 0 (17 spikes) and Stage 1 (safety net) run side by side over days 1 to 14; no start day is set formally (about day 6 if counted from the plan's date, 1 November). Stage 0: 0.2 and 0.3 passed, 0.9 closed, 0.1 half done (the credit ruling is accepted; the Mode A and Mode B billing profiles, the test cost centre and the invoice check are not recorded anywhere in this log, and the invoice check takes one to three weeks, so it is the long pole); 13 not started. Stage 1: the gate repo, workflow, rulesets (as files), CODEOWNERS template, hash manifest and 154 tests are built; the gate has never run as a gate, 20 of its scripts are unwritten, the rulesets are not applied (move step 12), `factory-test` and its identity and test user do not exist, and the Spec Kit presets, glossary and ADR templates, Playwright kit v0 and session mining are not started (they need their own planning session). Stages 2 to 8 are not started, though `factory-lane-1` and `getai-fl1-exec` (Stage 3 objects) exist from the spikes.
- **Proposed next session:** spike 0.6, Copilot CLI on GHE.com (the night shift's engine, and an open question in `CLAUDE.md`). If the vault's author has sent the Power Platform pieces by then, combine it with spike 0.14 as in `docs/analysis/delivery-vault-fast-track.md`, step 2. Alternatives: confirm or start spike 0.1's billing half (it is the long pole), or the Stage 1 planning session for presets, templates, the Playwright kit and mining.

- **Delivery vault read, fast-track analysis written** (at Boroon's word, after his 5 November call with the vault's author, a lane 1 low-code engineer). Read `AI-Business-Solutions/delivery-vault` on `getai.ghe.com` read-only (commit `19877b8`, 19 files); copied it verbatim to `docs/sources/delivery-vault/` (every file matches the source's blob hash; scanned: no client names, staff names, emails or secrets; `PROVENANCE.md` added). Wrote `docs/analysis/delivery-vault-fast-track.md`, with client names left out because this repo is public. Findings: the vault is a stack-neutral day-time kit (four skills, operating rules, templates) that fits the day gate and L0; the Power Platform pieces described on the call (naming standards, solution export and unpack, build self-tests, use of Microsoft's skills) are not in it yet. Proposed: ask the author for those; run spikes 0.6 and 0.14 together in `factory-lane-1`; pilot on the author's current engagement, limited to work with no client connections, if it is T1; start session mining with that team now. Boroon: client-tenant lanes are a later stage. The plan is not changed.

Files changed (close-out): `docs/progress.md`, `CLAUDE.md` (two map rows), `docs/analysis/delivery-vault-fast-track.md` (new), `docs/sources/delivery-vault/` (new, 19 files plus `PROVENANCE.md`).

## Ways-of-working one-pager, 2026-11-05, branch `claude/session-13-spike-0-3`

A side task in the Session 13 folder, separate from spike 0.3. Spike 0.3 still needs its own entry.

Done:
- Wrote a one-pager for GET AI low-code and pro-code FDE squads on how the factory works, for technical and non-technical readers. Built on the GET AI design system ("GET AI Diagrams" artifact: tokens, `bundle.css`, logo, three icons).
- Sections: where we are; in one minute; a story's path through ADO plus the Factory Eligible checklist; a day and a night (a 06:00 to 06:00 timeline, then five phases, each with "You" and "Under the hood"); which lane (low-code and pro-code side by side); size the work (XS to XL, the six questions); Merge Danger and the trust ladder (a 0 to 10 floor scale with examples, L0 marked "We are here"); who does what; your rhythm; 13 of the 19 rules and a glossary; stages and key dates.
- Boroon's layout changes (version 3): Day gate is phase 1 and Triage phase 2; the Night card head is solid electric blue like the night shift bar, and the Morning head solid turquoise like the review bars; Lane A sits above Lane B, code in the pro-code panel; "A story's path" comes before "A day and a night".
- Sources: plan V3.1 sections 2, 4, 5.5, 5.10, 5.11, 6.4 to 6.7, 7.3, `docs/analysis/tshirt-sizing.md`, and this log.
- Published as a private artifact, https://claude.ai/artifact/Ufn9wxxTA29eCRCLWHn9sg (version 3; version 2 lined up the five phase cards by section). Checked in headless Firefox at desktop and phone width.

Decisions:
- Left out the skills per size (still proposals) and most cost figures (kept one line: human minutes are about 80% of a story's cost, model).
- Left out the old one-pager's "client work runs at cash", since credits for client work were accepted on 2 November 2026.
- Boroon asked what PARK stands for. It is not an acronym: it is the word "park", written in capitals because the agent prints `PARK: <instruction>` as its last line. The page does not say this yet.

Files changed: `docs/one-pager/GET-AI-Factory-Ways-of-Working.html` (new), `CLAUDE.md` (the `docs/one-pager/` row), `docs/progress.md`.

Open items:
- The artifact is private. Boroon shares it with the team from the page's Share menu.
- The older `GET-AI-Overnight-Factory-one-pager.html` still says client work runs at cash. Update or retire it.
- The page's "Where we are" box and status section are true at 5 November 2026. Refresh them as stages pass.

Next steps:
1. Share the artifact with the squads.
2. Optional: add "PARK is the word park, not an acronym" to the page's glossary.

## Session 12, 2026-11-04, branch `claude/session-12-spike-0-2`

Spike 0.2, GHE.com OIDC with pac. A local session on Boroon's laptop. Started from `main` at PR 17's merge (`129c285`).

**Result: pass.** Exit test met: `pac org who` returned the application user in both cases, a job started by hand and the same job inside a ruleset workflow with a `job_workflow_ref` subject.

Done:
- Session 11's log was not on `main`. At Boroon's word, opened planning PR 17 for `claude/session-11-dependabot`; he merged it; this branch was made from the new `main`.
- Read-only checks on `getai.ghe.com`: `GetAI-IP` allows all actions, SHA pinning is not forced, the default token is read-only. The enterprise policy could not be read (the token lacks `admin:enterprise`). No org OIDC subject template exists. `protect-main` covers three named repos only. The discovery document at `https://token.actions.getai.ghe.com/.well-known/openid-configuration` has that issuer and lists `job_workflow_ref` and `issuer_scope`.
- pac goes in with `dotnet tool install`, so `microsoft/powerplatform-actions` is not needed (and the policy would allow it). Pinned to 2.4.1, the gate's pin. The only action is `actions/setup-dotnet` v5.4.0, pinned to `26b0ec14…`, checked against the tag with `git ls-remote`.
- Wrote `docs/plans/spike-0.2/probe.yml` (hand start or `workflow_call`; prints chosen claims, never the token; pac only when an app ID is given; inputs checked as GUIDs and a `crm6` URL) and `required.yml` (the ruleset caller, `pull_request` only, calls `probe.yml@main`). Neither checks anything out. Local checks: YAML shape, one pinned action, the claims step against a fake token server (audience sent; token, signature and request token never printed; unlisted claims not printed), the input checks with good and bad values.
- At Boroon's word, on `getai.ghe.com`: created private `GetAI-IP/oidc-probe` (repo 5328416) and pushed `f7de924` (`probe.yml`, README) and `ac9b369` (`required.yml`, with the real IDs; the planning copy has placeholders); created private `GetAI-IP/oidc-probe-target` (repo 5328491) with a README; set `oidc-probe`'s Actions access to the org; set an OIDC subject template on `oidc-probe-target` only (`use_default: false`; `repo`, `context`, `job_workflow_ref`); created the org ruleset `oidc-probe-required` (id 50511: default branch of `oidc-probe-target` only, by repo ID; rule `workflows`, `required.yml` at `refs/heads/main` from `oidc-probe`; active; no bypass); pushed branch `probe-pr` and opened PR 1 in `oidc-probe-target`; re-ran its job. The first run in each repo created environment `fl1-exec` there (no protection rules).
- Boroon, in the portals: Entra app `getai-fl1-exec` (single tenant, no API permissions, no secret, no certificate) with two federated credentials; environment `factory-lane-1` (Sandbox, Managed, Australia, Dataverse, AUD); its application user with System Administrator. The steps are in `docs/plans/spike-0.2/README.md`.

Case 1, started by hand (claims run 36381961, then pac run 36384161):
- `iss`: `https://token.actions.getai.ghe.com`. `aud`: `api://AzureADTokenExchange`.
- `sub`: `repo:GetAI-IP@801576/oidc-probe@5328416:environment:fl1-exec`. The immutable form with owner and repo IDs, because the repo was made after 15 July 2026.
- `job_workflow_ref`: `GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`.
- pac 2.4.1 (`.NET 10.0.14`): `'<app id>' authenticated successfully`, `Connected to... factory-lane-1`; `pac org who`: `Connected as <app id>`, with the application user's User ID.

Case 2, inside the ruleset workflow (run 36385301 on PR 1; event `pull_request`, `ref` `refs/pull/1/merge`):
- `sub`: `repo:GetAI-IP@801576/oidc-probe-target@5328491:environment:fl1-exec:job_workflow_ref:GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`.
- `job_workflow_ref` names the central `probe.yml`, not the caller `required.yml`. So check (c) is true within one org.
- `workflow_ref`: `GetAI-IP_tqa7h098/oidc-probe/.github/workflows/required.yml@refs/heads/main`, with the enterprise suffix.
- Attempt 1 failed as expected (no credential yet): `AADSTS700213: No matching federated identity record found for presented assertion subject '...'`. Attempt 2, seconds after Boroon saved the second credential, failed the same way, though the saved subject, issuer and audience matched the presented ones byte for byte (read with `az ad app federated-credential list`, read-only). Attempt 3, about four minutes later, passed: `pac org who` returned the same application user (same User ID as case 1).
- No token-shaped string (`eyJ`) in any log of either case.

Findings:
1. On GHE.com a new repo's subject is the immutable form, `repo:<org>@<org-id>/<repo>@<repo-id>:...`, and the IDs stay in a customised subject too. The repo-level subject API now also returns `use_immutable_subject` and `sub_claim_prefix`.
2. A wrong subject does not fail silently in practice: through pac, Entra's `AADSTS700213` names the subject it was shown. Reading the subject from a first run is still the right order.
3. A new federated credential took a few minutes to start working. Wait about five minutes after saving one before the first run.
4. App-only sign-in to Dataverse needed no API permission on the app registration.
5. `gh run view` cannot show a ruleset run: it looks for the workflow in the target repo and gets 404. Read it with `gh api repos/<target>/actions/runs/<id>/jobs` and `.../actions/jobs/<id>/logs` (`--allow-escape-sequences`, then strip colour codes).
6. pac 2.4.1 is built for .NET 10 only; the gate sets up .NET 8 (Open items).
7. The `workflow_ref` claim carries the `_tqa7h098` suffix; `sub` and `job_workflow_ref` do not (Open items, five orgs).

Not tested: a caller in another org calling a `GetAI-IP` reusable workflow (check (c) across orgs); an environment with protection rules; `merge_group`; the gate's own `lcp-gate.yml`; self-hosted runners.

Plan edits, proposed and then **made at Boroon's word** ("make the proposed plan edits now"), the same session. 11 lines changed in `docs/sources/plan-v3.1.md`, none added, so every line number in `CLAUDE.md` still holds:
- Lines 256 and 445 ("No source confirms it on GHE.com", "Nobody has confirmed `--githubFederated` on GHE.com"): confirmed by spike 0.2, 4 November 2026.
- Line 469 (subject): give the immutable form as the default for new repos, with the example from case 1.
- Line 470: replace "[inference; untested for ruleset workflows]" with "tested in spike 0.2 within one org, through a reusable workflow called by a ruleset workflow; across orgs untested". Also `getai/factory-gates` to `GetAI-IP/factory-gates`. Added while editing: the subject names the project repo, so the Test identity needs one credential per project repo plus one for triage; and the `workflow_ref` suffix.
- Line 471: add that pac shows `AADSTS700213` with the presented subject, and that a new credential takes minutes to work.
- Line 473: drop "[inference]" on `ACTIONS_ID_TOKEN_REQUEST_URL`; add that pac 2.4.1 needs .NET 10. Added while editing: the app registration needs no API permission.
- Line 469 also says that a rename or re-creation breaks the credential, since the name and the IDs are both in the subject.
- Line 1378 (row 0.2): mark passed, 4 November 2026, Session 12.
- Line 1420 (risk 7): lower it. The fallback stays for code apps (`pa app push` needs a secret) and self-hosted runners.
- Line 1543 (open question): answered yes, within one org.
- Appendix A lines 1757 and 1883: `dotnet-version: 10.0.x`.

Files changed: `docs/plans/spike-0.2/README.md`, `probe.yml`, `required.yml` (new), `docs/sources/plan-v3.1.md` (11 lines), `docs/progress.md`, `CLAUDE.md`. On `getai.ghe.com`: the two scratch repos, their settings and the ruleset above. Nothing in `GetAI-IP/factory-gates` changed. Dependabot #9 to #11 untouched. `protect-main`, `release-protection` and the four other orgs untouched. No secrets, no client data. The tenant ID and app ID are not recorded in this public repo.

Open items: only check (c) across orgs (with the callers build). The clean-up, gate PR 12 and plan row 0.9 are done (close-out, below).

Next steps:
1. Done: the plan edits, at Boroon's word.
2. Done: the scratch clean-up (below).
3. Done: gate PR 12, merged by Boroon (below).
4. Spike 0.3 (does Dataverse MCP accept an app-only token?) can reuse `getai-fl1-exec` and `factory-lane-1`.

Later the same day (close-out, branch `claude/session-12-close-out`, from `main` at PR 18's merge, `d151ef1`):
- **Boroon merged planning PR 18.** At his word ("shall we close what is still open now?", then each item ticked):
- **Scratch deleted** on `getai.ghe.com`, each looked at first: the org ruleset `oidc-probe-required` (id 50511), then `GetAI-IP/oidc-probe-target` (with its PR 1 and environment) and `GetAI-IP/oidc-probe`. Both repos now return 404. `protect-main` is the only org ruleset left.
- **Both scratch credentials deleted** from `getai-fl1-exec` with `az ad app federated-credential delete`, under Boroon's sign-in. The app now has none.
- **Leftover branch deleted:** `point-workflow-at-getai-ip` in `GetAI-IP/factory-gates`, after checking its tip (`96a7bc1`) is in `release` (PR 6, merged 3 November 2026). Left: `release` and the three Dependabot branches.
- **Gate PR 12** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/12), branch `dotnet-10` from `release` at `d0e19ed`, one commit `fa2e92b`: `dotnet-version: 10.0.x` in `build` and `verify-in-test`; new test `test_setup_dotnet_matches_the_pac_pin` (maps pac 2.4.1 to `10.0.x`, only those two jobs set up .NET, a new pac pin fails until its framework is checked); README at 154 tests with the new check. Locally, after clearing Finder files: 154 tests `OK`, manifest and rulesets silent, no hashed file changed. The test failed on five broken copies (either job on `8.0.x`, pac 2.14.1, the version line removed, a third `setup-dotnet` in `static`) and passed on the unchanged copy. A local trial merge with Dependabot #10, discarded: clean, 154 tests `OK`. On the PR, `self-test` passed (run 36419851) and `lcp-gate` is red at `map lane` as expected (no gate reader App). Dependabot #9 to #11 untouched.
- **Boroon merged gate PR 12 at 12:37 UTC** (merge commit `85ad2b5`). On the laptop: Finder files cleared, `release` at `85ad2b5`, **154 tests `OK`**, manifest and rulesets silent, both jobs on `10.0.x`. The `dotnet-10` branch went on its own on `getai.ghe.com`; the local copy is deleted. Planning PR 19 holds this close-out.
- **Plan row 0.9 marked closed** (one line in 11.1, line 1385). Spike 0.9 closed in Session 10. No lines added, so `CLAUDE.md` line numbers hold.

Files changed (close-out): `docs/sources/plan-v3.1.md` (line 1385), `docs/progress.md`, `CLAUDE.md`. In `GetAI-IP/factory-gates`: branch `dotnet-10` (`.github/workflows/lcp-gate.yml`, `tests/test_workflow.py`, `README.md`).

## Session 11, 2026-11-04, branch `claude/session-11-dependabot`

The five Dependabot pull requests in `GetAI-IP/factory-gates`. A local side session on Boroon's laptop, started by the Session 10 session. Started from `main` at PR 15's merge (`985f454`). Another session was using the laptop folder on `claude/session-10-repo-home`, so this branch was made in a separate worktree and the shared folder's branch was not switched.

Done:
- PR 15 (Session 10 planning) checked: merged into `main` on 4 November 2026.
- Gate clone, before any change: Finder files cleared (none found), `release` at `0b05d84`, up to date. 151 tests `OK`, `manifest.py verify` and `make_rulesets.py check` silent.
- Read the release notes for every major version crossed, and each README's breaking-change section. Checked each against how `lcp-gate.yml` (and `self-test.yml` for checkout) uses the action. Every job runs on `ubuntu-latest`.
- Checked every pin with `git ls-remote` on github.com: each new commit ID is the tag's commit (`azure/login` v3.1.0 is an annotated tag; it resolves to the pinned commit), and each old pin matched too.
- At Boroon's word: `@dependabot rebase` on #2, #3 and #4. Dependabot rebased all three onto `0b05d84`. **The #4 rebase also moved the checkout pin in `self-test.yml`**, so no `recreate` was needed (the Session 10 inference held).
- At Boroon's word, pushed one commit to each of two Dependabot branches, after running the checks on the branch merged into `release`:
  - #1, `0310952`: the comment now says `# v3.1.0`. Dependabot had moved the commit but left `# v2.3.1`, because the comment had a note after the version. The note ("for Key Vault ... and Blob") moved to its own line above, so the `uses:` line ends with the version.
  - #5, `c97ee08`: the four `download-artifact` pins move from v4.3.0 to v8.0.2 (`9000827ccba6bdab643e8b6fd33ac0654aef8333`, checked against the tag), so the `map` to `build` hand-off moves in one merge.
- `self-test` green on all five current heads (runs 36280921, 36280741, 36280751, 36280761, 36281156; 151 tests `OK` each). `lcp-gate` red on all five as expected: `map lane` stops at the token step because the gate reader App does not exist.
- All five merged in a row into a local copy of `release`: no conflicts, 151 tests `OK`, manifest and rulesets clean, no old pin left, every `uses:` comment ends with its version. So the order does not matter.
- Scratch worktrees removed. The gate clone is back on `release`, clean. Nothing merged, closed or set on `getai.ghe.com`. Rulesets untouched.

Verdicts (all five: merge; Boroon merges, one at a time):
- **#1 `azure/login` 2.3.1 to 3.1.0: merge.** v3.0.0 only moved Node 20 to 24. v3.0.2 hardened the PowerShell path (we use the CLI path). v3.1.0 adds opt-in inputs only. The gate passes `client-id`, `tenant-id`, `allow-no-subscriptions`, all unchanged.
- **#2 `actions/create-github-app-token` 2.2.2 to 3.3.0: merge.** v3.0.0: Node 24, and behind a proxy it now needs `NODE_USE_ENV_PROXY=1` (hosted runners have no proxy). v3.1.0 deprecates `app-id` for `client-id`; `app-id` still works with a warning. `owner`, `repositories`, `private-key` and the `token` output are unchanged.
- **#3 `actions/setup-node` 4.4.0 to 7.1.0: merge, plus a follow-up.** v5 Node 24 and automatic npm caching; v6 limits it to npm and removes `always-auth`; v7 is ESM and drops the dummy `NODE_AUTH_TOKEN`. None touches us: no `cache`, `registry-url` or `always-auth`, and the auto cache reads only `$GITHUB_WORKSPACE/package.json` (read in the v7.1.0 source), which the gate does not have (checkouts go to `pr/` and `gate/`).
- **#4 `actions/checkout` 5.1.0 to 7.0.1: merge.** v6 keeps persisted credentials in a separate file (we always set `persist-credentials: false`). v7 refuses fork code only on `pull_request_target` and `workflow_run` (the gate uses `pull_request` and `merge_group`). Our v5.1.0 pin already had the July 2026 backport. Its `self-test` run used v7.0.1 for real on the GHE.com runner.
- **#5 `actions/upload-artifact` 4.6.2 to 7.0.2, with `download-artifact` to 8.0.2: merge.** Upload v5 and v6 are Node 24; v7 adds opt-in unzipped uploads (`archive: false`) and ESM. Download v5 changed paths only for `artifact-ids` (we use `name`); v8 skips unzipping non-zip files and **fails on a digest mismatch by default**, which suits the hand-off of hash-checked scripts. The gate's inputs (`name`, `path`, `if-no-files-found`, `retention-days`) are unchanged, and the `test_workflow.py` hand-off tests pass.

Findings:
- `self-test` checks that pins are well formed and the tests pass. It does not run the five actions as the gate does. Two small real signals: #4's `self-test` ran checkout v7.0.1, and #2's `map lane` ran `create-github-app-token` v3.3.0 up to its new error ("The 'client-id' (or deprecated 'app-id') input must be set"). The rest run for real only once `lcp-gate` can run, after the gate reader App exists.
- Dependabot updates the version comment only when the comment is the version alone (seen on #1; the exact rule is my inference). The pin test allows text after the version, so a stale comment passes.
- No test makes one action use one pin across both workflows. Had #4 missed `self-test.yml`, `self-test` would still have passed.
- Four of the five were still based on the original split (`f91750e`), before PR 6 and PR 7. Only #4 had been rebased once. GitHub showed all five as mergeable.
- After a human push, Dependabot no longer rebases #1 or #5. Neither conflicts with the others.

Follow-ups found (1 to 3 done in gate PR 8, below):
1. In `lcp-gate.yml`, `package-manager-cache: false` on both `setup-node` steps. The README advises it for jobs with secrets (`verify-in-test` has OIDC and Key Vault). It cannot fire today; this keeps it off if a `package.json` ever lands at the workspace root.
2. Tighten the pin tests: a `uses:` comment must be `# vX.Y.Z` and nothing else, and one action has one pin across all workflows.
3. A Dependabot `groups:` entry for `upload-artifact` and `download-artifact`, so they arrive as one pull request.
4. Not done: when the gate reader and holdout reader Apps are made, `client-id` instead of `app-id`. If `verify-in-test` moves to a self-hosted runner: runner v2.327.1 or later.
- Dependabot's next wave, now its five slots are free: likely `setup-python` v5.6.0, `setup-dotnet` v5.4.0, `codeql-action` v3.39.1. Same routine.

Later the same day:
- **Boroon merged #1 to #5** between 01:51 and 01:52 UTC, in number order (merge commits `d6c9bff`, `9edd7fd`, `734cfed`, `cd2fbef`, `ad92400`). Dependabot's branches went on their own.
- On the laptop after the merges: Finder files cleared, `release` at `ad92400`. 151 tests `OK`, manifest and rulesets clean, no old pin left, every `uses:` comment ends with its version. No new Dependabot pull request yet.
- At his word ("Yes, after merges", then "Push and open PR"): **gate PR 8** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/8), branch `pin-upkeep`, one commit `32221a4`, follow-ups 1 to 3:
  - `lcp-gate.yml`: `package-manager-cache: false` on both `setup-node` steps.
  - `tests/test_workflow.py`: the comment rule now ends at the version; new test `test_setup_node_never_caches` (only in `verify-in-test` and `danger`, flag `false`, no `cache`).
  - `tests/test_self_test_workflow.py`: the same comment rule; new test `test_each_action_has_one_pin_and_one_version_across_all_workflows`, keyed by owner and repo.
  - `.github/dependabot.yml`: group `artifact-pair` for the two artifact actions, and a note to keep the comment to the version alone. Untested: whether GHE.com's Dependabot honours the group.
  - `README.md`: 153 tests, the new checks, how they were proved.
  - Broke a copy 12 ways (text after a version in either workflow, no comment, the cache flag dropped from either job or set true, `cache: npm`, a third `setup-node`, the self-test checkout on the old pin, one gate checkout left behind, one `download-artifact` left behind, one commit with two version comments). Each failed; the unchanged copy passed.
  - 153 tests `OK`, manifest and rulesets clean, locally and in a fresh clone. No hashed file changed.
  - CI on PR 8: **`self-test` passed** (run 36304241, on `32221a4`, 153 tests `OK`). `lcp-gate` red as expected (`map lane`, run 36304246). The app bound PR 8 and watches its checks. Auto-fix is off; it would only chase the expected `lcp-gate` failure.
- The planning branch merged `main` (PR 16, "where things live") with no conflicts. The planning repo is public (PR 16); this entry adds no secrets, only names, commit and run IDs of the kind already here.
- **Boroon merged gate PR 8 at 03:09 UTC** (merge commit `d0e19ed`; its tree equals PR 8's head tree). On the laptop: Finder files cleared, `release` at `d0e19ed`, **153 tests `OK`**, manifest and rulesets clean. The `pin-upkeep` branch went on its own on `getai.ghe.com`; the local copy is deleted. No pull request is open in the gate repo.

Files changed: `docs/progress.md`, `CLAUDE.md`. In `GetAI-IP/factory-gates`: commits `0310952` (#1) and `c97ee08` (#5) on Dependabot branches, `.github/workflows/lcp-gate.yml` only; PR 8 (`.github/workflows/lcp-gate.yml`, `.github/dependabot.yml`, `README.md`, two test files). No hashed file changed.

Open items: follow-up 4 waits for the reader Apps. The leftover branch `point-workflow-at-getai-ip`. PR 8 and the five Dependabot pull requests are merged.

Next steps:
1. Done: Boroon merged gate PR 8 on 4 November 2026; `release` passes 153 tests.
2. The next Dependabot wave, one at a time, same routine. If `upload-artifact` and `download-artifact` arrive apart despite the group, note it.
3. Checks (a), (c), (d) on `getai.ghe.com`, then the callers build (next slice 6).
4. Step 12, the rulesets, once the three teams exist and the approval stopgaps are undone. `apply --yes` only when Boroon says so.

## Session 10, 2026-11-04, branch `claude/session-10-gate-upkeep`

Gate repo upkeep and the self-test workflow (next slice 2). A local Claude Code session on Boroon's laptop, so it could reach `getai.ghe.com`. Started from `main` at PR 14's merge (`8cbeabe`).

Done in this repo:
- The laptop folder `/Users/Local VS Code/10-overnight-ai-factory` held plain files, not a git clone. I made it one in place (`git init`, fetch `origin`, branch from `main`). Nothing was overwritten. `.git/info/exclude` keeps the laptop-only items out of git: `/factory-gates/` (the gate clone), `/Research/`, `/Research.zip`, `/plan.md`, `.DS_Store`, `/.claude/settings.local.json`.
- Current state: PR 14 merged on 4 November 2026.

Done in `GetAI-IP/factory-gates`:
- Before any change, on `release` after `git pull`, Python 3.15.0 in `~/.venvs/factory-gates`: 141 tests `OK`, `manifest.py verify` and `make_rulesets.py check` silent.
- **PR 7** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/7), branch `self-test-workflow`, two commits, head `9f22f8b`. Pushed and opened at Boroon's word. **Merged by Boroon on 4 November 2026 at 11:36** (merge commit `0b05d84`).
  - `.github/workflows/self-test.yml` (new). On every pull request to `release` it installs the test requirements by hash, then runs the unit tests, `manifest.py verify` and `make_rulesets.py check`. `permissions: {}` at the top and `contents: read` on the job. No secrets, tokens, OIDC or environment, and checkout drops its credentials. The same commit pins as `lcp-gate.yml` (checkout v5.1.0, setup-python v5.6.0) and the same Python, 3.11. The check reports as `self-test`.
  - `tests/test_self_test_workflow.py` (new, 10 tests): the trigger, the permissions, no credentials, the README commands in order, no way to skip a check, Python equal to the gate's, and every action in every workflow pinned to a full commit ID with its version beside it. Broke a copy 28 ways; each was caught. 151 tests in all.
  - README: the move marked done (steps 1 to 11, 3 November 2026; step 12 still to do). Step 9 says Python 3.10 or later, a virtual environment outside the clone, and to delete Finder's `.DS_Store` files first. Step 6 records the 0 approvals, step 10 records option B, next slices 1 and 2 are done, and a new section lists what the new tests check.
  - `.github/dependabot.yml`: the comment now says Dependabot runs on GHE.com and covers both workflows.
  - No hashed file changed, so `scripts.sha256` is unchanged.
- Checked locally before the push, and again in a fresh clone of the branch: 151 tests `OK`, manifest and rulesets clean.
- CI on PR 7: **`self-test` passed** (run 36242716, CPython 3.11.17, 151 tests `OK`, manifest and rulesets steps green). `lcp-gate` red as expected (run 36242711): `map lane` fails with `appId option is required`, and the other five jobs skipped.
- After the merge: the merge commit's tree equals PR 7's head tree (`bb39aad`). The laptop clone is on `release` at `0b05d84`. Finder files cleared first, then 151 tests `OK`, manifest and rulesets clean. Dependabot ran on `release` after the merge (run 36261386) and left #1 to #5 as they were, so none has a `self-test` run yet.
- Boroon deleted the `self-test-workflow` branch, on the laptop and on `getai.ghe.com`, and turned on "Automatically delete head branches" in the repo's settings. Merged branches, Dependabot's included, now go on their own.
- Dependabot #1 to #5 and the rulesets untouched. `apply_rulesets.py` not run.

Decisions (Boroon, 4 November 2026):
- **Finder files.** He browses the laptop folders in Finder. So before every local check, and whenever the local folders are used, delete the `.DS_Store` files in the gate clone first (command in `CLAUDE.md` and in the gate README step 9). Do not teach `manifest.py` to skip them: it is a hashed gate script, and an unknown file is rightly "unlisted".
- **`self-test` as a required status check on `release-protection`: not now.** Offered once `self-test` was green. It stays a visible check, not a required one. **Turn it on when someone other than Boroon starts working on the factory** (he said so later the same day, after asking what each choice means).
- **Spike 0.9, the environment audit: closed.** Boroon ran it in the admin centre: four unmanaged developer environments, all personal, none client facing, none a factory lane; the rest are managed. Not critical to the factory. He has told the four owners, who handle their own before 15 December 2026 (suspended then, deleted 15 January 2027). The factory tracks them no further. The plan's pass test (none in use by 15 December) is set aside for these four, because no lane or client work uses them.
- **Where things live.** The planning repo stays on github.com for good; only the workflows and the automation Apps go on `getai.ghe.com` (Current state). Decided after PR 15 merged, when he asked why the planning pull request was not on GHE. Recorded on branch `claude/session-10-repo-home`.

Findings:
- Finder wrote `.DS_Store` files into the clone mid-session. The next local run failed `manifest.py verify` and 2 tests (`test_committed_manifest_matches_the_scripts`, `test_committed_manifest_passes_sha256sum`) as "unlisted: .DS_Store". Not a real failure. CI runners have no Finder files.
- Python 3.10 reached end of life in October 2026. The scripts need 3.10 or later; both workflows run 3.11. If `PY_VERSION` in `lcp-gate.yml` moves, `self-test.yml` must move with it: a test fails if they differ.
- Dependabot's five pull requests were opened before `self-test.yml` existed, so they have no `self-test` run. Each needs a new push to get one, for example a `@dependabot rebase` comment. Check that #4 then also moves the checkout pin in `self-test.yml`; if not, `@dependabot recreate`. My inference, untested.

Files changed: `CLAUDE.md`, `docs/progress.md`. In `GetAI-IP/factory-gates`, by PR 7: `.github/workflows/self-test.yml` (new), `tests/test_self_test_workflow.py` (new), `README.md`, `.github/dependabot.yml`.

Open items: PR 7 and PR 15 merged. The Dependabot pull requests, the required-check choice and the public planning repo (Open items above). Spike 0.9 closed.

Next steps:
1. Done: Boroon merged PR 15 (https://github.com/boroonmahanta/overnight-ai-factory/pull/15), this session's planning pull request, and gate PR 7, both on 4 November 2026.
2. Boroon decides whether to make this planning repo private (Open items).
3. The Dependabot pull requests, one at a time: a new push to get a `self-test` run, read the release notes, merge. `upload-artifact` together with `download-artifact`.
4. Checks (a), (c), (d) on `getai.ghe.com`, then the callers build (next slice 6).
5. Step 12, the rulesets, once the three teams exist and the approval stopgaps are undone. `apply --yes` only when Boroon says so.

## Session 9, 2026-11-03, branch `claude/wonderful-lamport-vbdypu`

The move of `factory-gates/` to GHE.com, from `main` (PR 13, Build 3, merged 3 November 2026). The 141 tests passed before any change. Boroon expected a laptop session. This one ran in a cloud container that cannot reach `getai.ghe.com` (the host is not allowed, there is no login for it, SSO cannot run there). So I did the steps that need no GHE.com, prepared the rest, and checked each of his laptop steps from the output he pasted.

Done in this session (cloud):
- Current state: PR 13 merged on 3 November 2026.
- Steps 1, 3 and 4 rehearsed in a fresh clone of `main`: `git subtree split` gave 13 commits, head `f91750ec6a4d9982cb2d55b117ddbdf6003f2d90`, tree `2651ffba434dcd658540a4a261cf47b51db0e024`, equal to `main:factory-gates`. A plain clone of the split passed the 141 tests, `manifest.py verify` and `make_rulesets.py check`.
- Step 8 made and tested as `docs/plans/factory-gates-move-step-8.patch` (kept as the record). `GATE_REPO`, all six token `owner:` fields (each reads only `factory-gates` or `factory-holdout`), the holdout checkout and the header comment name `GetAI-IP`; the `GATE_REPO` test assertion matches; the README is no longer a "staging copy", names the central org and the four orgs, and adds next slice 6 (callers). No hashed file changed. Checked with `git am` on a fresh clone of the split: 141 tests, manifest and rulesets clean, tree `1e7ece8621aafa27a22798d61c5b997c2340560b`. (A first version for `AI-Business-Solutions` was replaced when `GetAI-IP` became the central org.)
- Step 11: deleted `factory-gates/` from this repo (33 files). `CLAUDE.md`, `docs/plans/stage-1-gate-build-plan.md` and this file point at the new repo.
- Nothing was pushed to `getai.ghe.com` from here.

Done by Boroon, 3 November 2026 (`getai.ghe.com` and his Mac, git 2.56.0, Python 3.15.0):
- Step 2: created `GetAI-IP/factory-gates`, private and empty.
- Steps 3 to 5: same split head and tree IDs as the rehearsal. The push created `release`, the default branch.
- Step 6: repository ruleset `release-protection` on `release`: pull request required, force push and deletion blocked, empty bypass list, 0 required approvals (decision below).
- Step 7: Actions Access set to "Accessible from repositories in the 'GetAI' enterprise". Actions permissions: enterprise actions plus GitHub's own and `azure/login@*`, full-SHA pins required (all nine actions in the workflow already are).
- Step 8: applied the patch, opened and merged the new repo's first pull request, after excluding `factory-gates` from the org ruleset `protect-main` (decision below).
- Step 9: fresh clone `~/factory-gates-check`, venv `~/.venvs/factory-gates`: tree `1e7ece86…` as expected, 141 tests `OK`, manifest and rulesets check silent.
- Step 10: option B (below).

Decisions (Boroon, 3 November 2026):
- **Central org `GetAI-IP`** holds the gate and the held-out tests (`GetAI-IP/factory-holdout`, not yet created). Four orgs will use the gate: `AI-Business-Solutions`, `AI-Managed-Services`, `Cloud-AI-Platforms`, `GetAI-Knowledge`, all in the enterprise `GetAI`. Replaces `AI-Business-Solutions` as the gate's home. The callers design is in Open items.
- **The cloud route is closed.** Git providers needs a Claude Team or Enterprise plan; he is on an individual plan. Gate work runs from his laptop.
- **No github.com stand-in.** Proposed, chosen, then dropped before anything was made: a personal account cannot do any of stage 1's org-level work, and it would add a second host and set of identities.
- **0 approvals on `release-protection`, and `factory-gates` excluded from `protect-main`, until a second approver exists.** `protect-main` is a `GetAI-IP` org ruleset on each repo's default branch (1 approval, by someone other than the last pusher). It blocked step 8, because no one can approve their own pull request. Undo both before step 12 (Open items).
- **Step 10: B.** Accept the red `lcp-gate` run on the gate repo's own pull requests. It ends when the callers build makes the central workflow call-only, and the self-test workflow (next slice 2) gives the real signal.
- One gate repo serves many teams and both profiles (`profile:lcp` now, `profile:pcp` with its own `pcp-gate.yml` at stage 5).

Findings:
- **Dependabot runs on `getai.ghe.com`** (open since Build 1). Within 15 minutes of the push it opened five major-bump pull requests: `azure/login` 2.3.1 to 3.1.0 (#1), `actions/create-github-app-token` 2.2.2 to 3.3.0 (#2), `actions/setup-node` 4.4.0 to 7.1.0 (#3), `actions/checkout` 5.1.0 to 7.0.1 (#4), `actions/upload-artifact` 4.6.2 to 7.0.2 (#5). Five is its default limit; `download-artifact`, `setup-python`, `setup-dotnet` and `codeql-action` will follow. Advice: merge none and close none (closing makes it skip that version) until the self-test workflow exists; then one at a time after reading the release notes, with `upload-artifact` and `download-artifact` together (the `map` to `build` hand-off uses both). Maybe group those two and set the limit in `dependabot.yml`.
- A private repo's workflows can be shared with the whole enterprise, but only to private repos. The callers must be private.
- The red `lcp-gate` run fails at the first token step, `appId option is required`: `vars.GATE_READER_APP_ID` is not set because the gate reader App does not exist yet. Expected. The same log shows the Actions permissions let GitHub's actions run, and the token step asks for `GetAI-IP/factory-gates`.
- "Require approval of the most recent reviewable push", which I advised for step 6, also needs a second person, even at 0 approvals. My mistake; left unticked until there is a second approver.
- The scripts need Python 3.10 or later (`Path | None`); macOS's built-in `python3` is 3.9. Homebrew's Python needs a virtual environment, and it must sit outside the clone: `manifest.py` calls every unknown file under the root "unlisted" (correct, an unknown file is an unreviewed file), so a `.venv` inside failed 2 tests on the first try. The new repo's README says neither yet.
- The test output shows "401 Bad credentials" and "created ruleset … id 901": that is `test_apply_rulesets.py`'s fake GitHub. Nothing is sent.
- The Claude Code page for GitHub Enterprise Server (read 3 November 2026) says nothing about `*.ghe.com`. A token route for the cloud (allowed domain plus a stored token) is undocumented and untested.
- Local Claude Code on the laptop needs nothing special for GHE.com; it uses the laptop's git and `gh`. The laptop already holds a login for `getai.ghe.com` (the push did not prompt).
- **Boroon's working copy** of the gate (chosen 3 November 2026): a git clone of `GetAI-IP/factory-gates` at `/Users/Local VS Code/10-overnight-ai-factory/factory-gates` (a clone, not copied files, so it stays linked to the real repo). Virtual environment at `~/.venvs/factory-gates`, outside the clone. Cloned and checked the same day: tree `1e7ece86…`, on `release`. The day's temporary folders (`~/factory-move`, `~/factory-gates`, `~/factory-gates-check`, `~/step-8.patch`) are deleted.

Files changed: `CLAUDE.md`, `docs/progress.md`, `docs/plans/stage-1-gate-build-plan.md`, `docs/plans/factory-gates-move-step-8.patch` (new), `factory-gates/` (deleted).

Open items: in the Open items section above (laptop-only gate work, the callers checks (a), (c), (d), the approver stopgaps, the Dependabot pull requests, the README follow-ups). Spike 0.9 before 15 November 2026, unchanged.

Next steps:
1. Boroon reviews and merges PR 14 (https://github.com/boroonmahanta/overnight-ai-factory/pull/14), opened at his request on 3 November 2026. Merging it removes `factory-gates/` from `main`.
2. In `GetAI-IP/factory-gates`, by pull request there, from his laptop: the README step 9 fixes and the `dependabot.yml` comment, then next slice 2, the self-test workflow.
3. Checks (a), (c), (d) on `getai.ghe.com`, then the callers build (next slice 6).
4. Step 12, the rulesets, once the three teams exist and the approval stopgaps are undone. `apply --yes` only when Boroon says so.

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
