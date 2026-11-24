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

- Mostly documents. The first code, the gate, now lives in its own repo **`GetAI-IP/factory-gates` on `getai.ghe.com`**, branch `release` (moved 3 November 2026, Session 9): stage 1 slice 1 and Builds 1 to 3, 154 tests passing there (gate PR 12, merged 4 November 2026). **Gate PR 15** (Session 30, 21 November 2026, ADO 2511) brings it in line with the live-build plan: **merged by Boroon on 21 November 2026**; `release` is at `96b6c61`, with 163 tests passing. It has not yet run as a gate on any project repo. No pipelines exist yet. The gate's three read-only token Apps exist since 24 November 2026 (Session 45, ADO 2537). The rulesets are files, not applied. **The first tenant objects exist since spike 0.2** (Session 12, 4 November 2026): the Power Platform environment `factory-lane-1` (Sandbox, Managed, Australia, `https://factory-lane-1.crm6.dynamics.com/`) and the Entra app `getai-fl1-exec` with its application user there (System Administrator).
- **Build 1 is done** (Session 6). PR 11 merged into `main` on 3 November 2026.
- **Build 2 is done** (Session 7). PR 12 merged into `main` on 3 November 2026.
- **Build 3 is done** (Session 8). PR 13 merged into `main` on 3 November 2026.
- **The move is done** (Session 9, 3 November 2026): steps 1 to 11 of "Moving to GHE.com" (now in the new repo's README). `factory-gates/` is deleted from this repo: **PR 14 merged into `main` on 4 November 2026**. Step 12, applying the rulesets, is not started. `GetAI-IP` is the central org; four other orgs will use the gate. **Gate work runs from Boroon's laptop:** cloud sessions cannot reach `getai.ghe.com`.
- **Gate upkeep and the self-test workflow** (Session 10) are on `release` in `GetAI-IP/factory-gates`: **PR 7 merged on 4 November 2026**, with `self-test` green on it. The planning record is PR 15, **merged into `main` on 4 November 2026**.
- **The first Dependabot round is done** (Session 11): #1 to #5 in `GetAI-IP/factory-gates` **merged by Boroon on 4 November 2026**, each with `self-test` green. The follow-up, **gate PR 8** (`pin-upkeep`: `setup-node` cache off, tighter pin tests, a Dependabot group for the artifact pair), **merged by Boroon on 4 November 2026**. `release` was then at `d0e19ed`, with 153 tests passing. **Gate PR 12** (.NET `10.0.x` for pac 2.4.1, Session 12) **merged by Boroon on 4 November 2026**. **The second Dependabot round is done** (Session 24): #9 (`setup-python` 7.1.0), #13 (`upload-sarif` 4.39.3) and #14 (`setup-dotnet` 6.1.0) **merged by Boroon on 13 November 2026**, each with `self-test` green: `release` is at `b37a9f0`, with 154 tests passing.
- **Where things live (Boroon, 4 November 2026).** This planning repo stays on github.com, `boroonmahanta/overnight-ai-factory`, for good. Only the workflows and the automation Apps go on `getai.ghe.com`: the gate (`GetAI-IP/factory-gates`), the held-out tests (`factory-holdout`), the caller repos and the GitHub Apps. This replaces the Session 7 note that the planning repo would move to GHE.com when complete. Planning sessions can still run in Claude's cloud; gate work stays on the laptop.
- **Spike 0.2 passed** (Session 12, 4 November 2026): `pac auth create --githubFederated` works on `getai.ghe.com`, both in a job started by hand and inside a ruleset workflow with a `job_workflow_ref` subject. `pac org who` returned the application user both times. Record and portal steps: `docs/plans/spike-0.2/README.md`. The scratch repos `GetAI-IP/oidc-probe` and `GetAI-IP/oidc-probe-target`, the org ruleset `oidc-probe-required` and the two scratch federated credentials were **deleted on 4 November 2026**, at Boroon's word. `getai-fl1-exec` (no credentials now), its application user and `factory-lane-1` stay for the night shift (Stage 3). Planning PR 18 merged into `main` on 4 November 2026.
- **Spike 0.3 passed on both paths** (Session 13, 6 November 2026): Dataverse MCP accepts an app-only token. A job on `getai.ghe.com`, signed in as `getai-fl1-exec` by GitHub OIDC with no secret, made a read and a create through the Dataverse CLI's local proxy and through the remote `/api/mcp` endpoint, once `getai-fl1-exec` was on `factory-lane-1`'s allowed MCP clients list. Record, portal steps and 13 findings: `docs/plans/spike-0.3/README.md`. The two test rows, the scratch repo `GetAI-IP/mcp-probe` and the federated credential `mcp-probe-fl1-exec` are **deleted** (6 November 2026, at Boroon's word). The allowed MCP client entry `new_getaifl1exec` is **kept for Stage 3**, at Boroon's word. The plan is edited for the result (9 lines, Session 13, at Boroon's word). Planning PR 21 merged into `main` on 6 November 2026.
- **Spike 0.18 done: the YAML exit test fails and the XML fallback passes** (Session 19, 8 November 2026, ADO 2462). On a runner, as `getai-fl1-exec` with no secret, on pac 2.14.1 and the gate's pin 2.4.1, `export` then `unpack`, `clone` and `sync` all wrote the XML layout. The XML tree held a table, a cloud flow, a security role, an environment variable and a connection reference; it packed again signed out and with no network; a second export was byte-identical. The plan now makes the XML layout the low-code lane's source format, with the driver running export then unpack (at Boroon's word). Record: `docs/plans/spike-0.18/README.md`. The scratch (repo `GetAI-IP/export-probe`, credential `export-probe-fl1-exec`, solution `FactorySpike` in `factory-lane-1`) was kept for spike 0.19 and 0.14, and **deleted on 21 November 2026** at Boroon's word.
- **Spike 0.19 passed: the reset returns the lane to its reset commit, byte for byte** (Session 20, 10 November 2026, ADO 2463), in `factory-lane-1` alone, not with 0.10. On a runner, as `getai-fl1-exec` with no secret, a probe-only stand-in for `reset_environment.py` did four things:
  - it imported the reset commit with overwrite and publish, which undid a change to the main flow;
  - it set the lane's environment variable value outside the solution;
  - it found and deleted a flow and a column left in the solution and a flow left outside it;
  - the fresh export, unpacked, equalled the reset commit in all 23 files.

  How to find what the lane identity made outside the solution turned out not to be `solutioncomponent.createdby`: the Default Solution's rows are by SYSTEM. The finder asks each component table for its maker, and finds tables and columns by state against a bootstrap list. The plan is edited for it (11 November 2026, at Boroon's word), with his rule that a table or column found outside the solution stops the lane for a person to check (ADO 2843). Record: `docs/plans/spike-0.19/README.md`. The scratch (0.18's plus one environment variable value) was kept for spike 0.14, and **deleted on 21 November 2026** at Boroon's word.
- **Spike 0.14 has all four parts run** (Sessions 25 to 28, 18 to 21 November 2026, ADO 2461, **Done** on 21 November 2026 at Boroon's word; its dates not moved). Part 1 passes: a flow with no connector, made by the Web API as `getai-fl1-exec`, runs, exports and packs again offline. Part 2: the App Spec apply works as the lane identity for a new app (unattended, never `--allow-destructive`); FlowAgent reads and edits flows as the lane identity but cannot list, turn on, turn off or run them (HTTP 401). Part 3: a stdio shim in front of the Dataverse CLI's local proxy counts every MCP call, holds a cap and retries; a retried create whose answer was lost writes twice; every call that reaches Dataverse is billed, tool errors included. Part 4 (Session 28): Copilot CLI runs Microsoft's skills headless as the lane identity on `claude-sonnet-5.5`; the flow story passed; **the App Spec skill stops at the apply on an existing app**, which needs `--allow-destructive` even for one new column; MCP calls per session 0 and 1. Verdict: passed, with the fallback where it applies. **Part 4b (Session 29, 21 November 2026): option (b), an additive change to the existing app with no App Spec apply (the column by Dataverse MCP, the form and view by the Web API through a trusted helper), passed all 18 checks headless as the lane identity (run 40126806).** **Boroon agreed the approach on 21 November 2026:** (b) at night for additive changes to an existing app (a column on an existing table, shown on an existing form and view) through a trusted Web API helper the driver ships; the App Spec apply for a new app; (a), a PARK with the dry run as evidence, for any other change to an existing app until its route is tried. **Edited into the plan the same day, at Boroon's word** (5.6, 11.1, 14.4, 15.1, Appendix C, by Session 29), **with the rest of the spike's results** (Session 28, branch `claude/session-28-2461-plan-edits`: 5.2, 5.4, 5.6, 5.9, 5.11, 5.14, 11.1, risk 34, 14.4, 15.1, Appendices B.1 and D). Record: `docs/plans/spike-0.14/README.md`.
- **Spike 0.17 passes for all four tools** (Session 31, 21 November 2026, ADO 2466, DG2; **Done** at Boroon's word). Each tool gave a readable export of a test session with no client data. Copilot CLI's `--share` writes the fullest (Markdown with tool calls, file edits and shell output), and it also exports Copilot app and VS Code chat sessions, because all three share `~/.copilot/session-state/`; it runs on a copy of the session, so the original never changes. Claude Code's `/export` writes plain text, in a live terminal session only. The how-to for engineers and the checklist for removing client data: `docs/plans/spike-0.17/README.md`. Exports go to `Factory session exports` in Boroon's OneDrive, through a "Request files" link he still has to make (Request files works there, Session 32). Their lasting home, a private channel in an internal Factory Team, is ADO 3019 (Building), waiting on the admins and on Boroon making the Team. The Microsoft 365 connector reads it from the laptop and from a cloud session, so mining batches (2548) can run in the cloud; list the folder by its item ID, not its path.
- **`factory-test` exists** (Session 46, 24 November 2026, ADO 2541, Building): Sandbox, Managed, checker Block, Australia, `https://factory-test.crm6.dynamics.com/`, with the Test identity `getai-nwt-test` (project `nwt`, the Northwind pilot) as its System Administrator application user. The test user, the Key Vault and the federated credentials wait on the identity admins, the CSP subscription's owner and the Northwind project repo. Record: `docs/plans/factory-test/README.md`.
- **The Ignite re-check is done** (Session 33, 23 November 2026, ADO 3024): `docs/analysis/ignite-2026-recheck.md`. No rename, nothing GA for the night lane's tools, Copilot residency still US and EU only; nine GA items touch the plan, **edited into the plan the same day at Boroon's word**.
- **ADO is current** (Session 19): every update Sessions 17 and 18 left is made, and the schedule-order query matches `docs/plans/schedule.md`. Session 20 moved 2463 to Done.
- PR 9 (Session 4) and PR 10 (Session 5) are merged.
- The main plan is V3.1, dated 1 November 2026: `docs/sources/plan-v3.1.md`.
- **The Get AI Engineer's material is assessed** (Session 14, 6 November 2026): `docs/analysis/delivery-vault-assessment.md`. It found the Power Platform standards, patterns and export procedure in the Get AI Engineer's older vault in Azure DevOps, and recommends building live in the lane with the export as the record.
- **Live build is decided (Boroon, 7 November 2026) and edited into the plan** (Session 15). In lane B (low-code), agents build live in the lane. A trusted driver step, not the agent, exports and unpacks the solution, and that export is the PR's source. Builders stay only where Microsoft ships a generator: App Spec, `pac copilot`, code apps, PCF and plug-in source. Pro-code is unchanged. Three spikes must pass before Stage 3: 0.18 (headless YAML export), 0.19 (reset fidelity) and the widened 0.14. `GetAI-IP/factory-gates` now lags the plan; the follow-ups are under Open items.
- Spikes 0.2, 0.3, 0.18 and 0.19 are the only plan items tested on real services. Every other item marked `[untested]` in the plan is still untested. The plan is edited for spike 0.2's result (11 lines, Session 12), spike 0.3's (9 lines, Session 13), the live-build decision (Session 15), spike 0.18's result (Session 19) and spike 0.19's (Session 20), each at Boroon's word.
- **The rest of Stage 1's day gate is planned** (Session 17, 7 November 2026, a cloud session): `docs/plans/stage-1-day-gate-plan.md`, nine build sessions DG1 to DG9 for 2545, 2544, 2546 and 2548 with spike 0.17, dated 12 November to 15 December. Boroon decided D1 to D6, and the plan is edited for them. The gate scripts (2538) wait on spike 0.18.
- **DG1 is done** (Session 18, 7 November 2026, a cloud session, brought forward from 12 November): `staging/` with its README, and `staging/factory-manifestos/` with its README and the three project templates (`glossary.md`, `docs/adr/README.md`, the `coding-standards.md` header). 2545 stays open until DG3 (Friday 20 November).
- **DG3 is run** (Session 23, 13 November 2026, a week early): `GetAI-IP/factory-manifestos` exists on `getai.ghe.com` (private, ruleset `main-protection`), and its pull request 1, merged by Boroon on 13 November 2026, holds the low-code coding standards: 50 with the vault's client-token ones kept, anonymised. 2545 is Done.
- **2544 is built: DG4 and DG5 done** (Sessions 35 and 36, 23 November 2026). Spec Kit pinned at 1.4.3, the `getai` and `getai-lcp` presets, the `getai-spec-check` extension and bundle in `staging/factory-manifestos/spec-kit/`; the spec check `staging/factory-gates/spec/check_spec.py` with 98 passing tests, and its byte-identical copy in the extension. The stage 1 exit clause "a spec with an open marker or no scenarios cannot become Factory Eligible" is shown by two fixtures failing. Pull requests 47 and 48 are merged, and **2544 is Done** in ADO (23 November 2026, at Boroon's word).
- **The third-party skills policy (plan 8.3) is applied to every vendored skill** (Session 21, 11 November 2026, a cloud session, ADO 2549): `docs/analysis/skills-policy-check.md`. All 56 shelf skills match upstream at their pins, all are MIT, and all but `poteto-mode` (shelf only) are read in full. The register's rows now have a file, `docs/component-register.md`, and the shelf holds each source's licence text. All 44 live skills name their source commit in their first lines.
- Boroon said more context will be added in later sessions.
- Work is sized with T-shirt sizes (XS to XL), approved on 1 November 2026. See `CLAUDE.md`.

## Open items

- **Done: `factory-manifestos` pull request 1 merged** (Session 23): https://getai.ghe.com/GetAI-IP/factory-manifestos/pull/1, the 50 low-code standards, merged by Boroon on 13 November 2026 (`fd2e268`); 2545 is Done in ADO. The plan now says 50 (5.10, 5.12 and a 14.4 row, edited at Boroon's word, Session 23). Also still open from DG3: Boroon to ask the Get AI Engineer to review the standards (not blocking); `main-protection` there is a second-approver stopgap that 2520 must raise to 1 approval.
- **Done: ADO updates for 2549, left by Session 21.** Seen in Session 22 (13 November 2026): another laptop session made them that day. 2549 is Done, dated Wed 11 Nov, with its result and Session 21's time-and-tokens line in its body. Kept here one session for the record.
- **The Ignite re-check is edited into the plan** (Session 33, at Boroon's word): `docs/analysis/ignite-2026-recheck.md`. Two actions sit outside the plan, for Boroon: the tenant's routing rules and app creation spaces for Copilot Managed Runtime (plan 5.4), and a check that no team on `getai.ghe.com` sets default Copilot plugins (plan 8.3 point 7).
- **The first component register review was due on Monday 23 November 2026,** with the Ignite re-check (done, Session 33) and A1's first pass (not done). For each row of `docs/component-register.md`, check the source for changes since its pin (the file says how) and update "Last checked". Also look at: the five principle fragments, whether skills and plugins installed on the claude.ai account belong in the register, and the A1 kits as new rows.
- **`poteto-mode` is not read in full** (shelf only): its `watch-pr` code and tests, and most of `check-plan.mjs` and `worktree-audit.sh`. Read them before any adoption (rule 19).
- **"Agile build v1" differs from plan Appendix D.2** (seen 7 November 2026, Session 15). The process exists in the `getai` organisation, but its User Story states are not D.2's, it has no Spike type, and the D.1 custom fields were not checked. Before Stage 2 changes it, find which projects already use it.
- **The factory's own backlog is in ADO,** project `getai-overnight-ai-factory` (created 7 November 2026, Session 15). Keep it current: at the end of each session, add the session's time and tokens to its stories (`CLAUDE.md`, end step 3), and move the stories it finished to Done.
- **`GetAI-IP/factory-gates` lags the plan after live build** (Session 15, 7 November 2026). **Items 1 to 5 and 7 are done in gate PR 15** (Session 30, 21 November 2026, ADO 2511, https://getai.ghe.com/GetAI-IP/factory-gates/pull/15), **merged by Boroon on 21 November 2026** (`96b6c61`); so are item 9's two names. ADO 2511 is Done. Item 6 moved to 2538 (ADO task 2517, at Boroon's word). Items 8 and the rest of 9 stay with 2538. The list as Session 15 wrote it (read from the clone at `85ad2b5`, the same as `release` then):
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
  8. (Added Session 17, D3.) A job in `lcp-gate.yml` that runs the gate's trusted `spec/check_spec.py` on spec PRs and checks the hash of the copy vendored under `.specify/`. The script itself is built in 2544 (DG5) and reaches `factory-gates` in the move (DG8). For 2538. **Built in 2538's slice C** (Session 42, 23 November 2026), as a step in `locks` with `lcp/check_specs.py`, and the script came into `factory-gates` early; on gate branch `verify-in-test`, not merged yet. **Checked in Session 36 (DG5): still right.** What DG5 settled for the job: the vendored copy is at `.specify/extensions/getai-spec-check/scripts/check_spec.py` (seen in a real `specify extension add --dev` on 1.4.3); run `python3 -I gate/spec/check_spec.py --spec pr/specs/<ado-id>-<name>/spec.md --profile <lcp|pcp> --repo pr` once for each spec folder the PR changes (its `spec.md` or `checklists/`); exit 1 fails the job, and the output is plain lines (`FAIL [rule] path:line: message`, `WARN [design-leak] ...`). Take `--profile` from the project manifest or lane map, not from the spec's own header: the script fails a header whose `profile` differs from `--profile`, and that check means nothing if the job reads the value it checks. `spec/check_spec.py` joins `scripts.sha256` when DG8 regenerates it.
  9. (Added Session 19, spike 0.18.) The XML source layout, not YAML: `lcp/pack_offline.py` calls its `--source` "the YAML-format solution folder" (help and docstring), and `lcp-gate.yml`'s `build` step is named "Pack the solution offline (YAML source format)"; plan Appendix A now says "XML source layout". When the manifest check is written, it reads the declared root components from `Other/Solution.xml`; when `danger-rules.yml` is written, its B.1 rows use the XML folders (`Entities/`, `Workflows/`, `Roles/`, `environmentvariabledefinitions/`) and connection references come from the export-diff plan. Consider moving the pac pin from 2.4.1 to 2.14.1 (identical output for the five types tested; read its release notes first, A1). For 2511 and 2538. **Correction from spike 0.19 (Session 20):** `Other/Solution.xml`'s `RootComponents` does not list every root component; in `FactorySpike` it left out the environment variable and the connection reference, which are only in `environmentvariabledefinitions/` and `Other/Customizations.xml`. So the manifest check reads the whole tree, not only `Other/Solution.xml` (`docs/plans/spike-0.19/reset_probe.py`, `read_commit`, does this).
  - **Not on `pending-scripts.txt`:** `export_lane.py`, `reset_environment.py` (now with leftover removal and the proof) and the lane drift check. They run in the execution workflow in `factory-control`, not in `lcp-gate.yml`. They are Stage 3 builds, after spikes 0.18 and 0.19.
- **The gate's managed pack cannot come from the driver's export as tried so far** (found in Session 30, gate README finding 11; untested). `build` packs `solution_managed.zip` from `pr/src`, and `verify-in-test` runs the checker on it and imports it into Test. Microsoft's SolutionPackager page says the tool cannot convert unmanaged to managed, and pac's help says a Managed pack works only from a folder unpacked with `--packagetype Both`, which needs a managed export too. Spike 0.18 exported unmanaged only. Ways out: the driver exports both kinds and unpacks with `Both`; or the gate imports the unmanaged zip into Test; or a trusted step imports unmanaged into a build environment and exports managed (needs credentials). Settle in spike 0.10 (2459) or before the Stage 1 exit test (2539), then a plan change at Boroon's word (5.6, 5.7, Appendix A).
- **Done: two small plan edits from Session 30, made at Boroon's word** ("Yes, edit the plan", 21 November 2026): (1) Appendix A's opening paragraph names the XML layout's folders, not YAML's `src/solutions/<Name>/` and `src/publishers/`, which Session 19 missed; (2) 5.6's gate order, 5.7's job table and trusted-script list, Appendix A's job table and `build` comment, and a new 14.4 row say a project declares generator wrappers in `workflows/build/` and the gate fails any builder that writes under `src/`. Kept here one session for the record.
- **This planning repo is public** (checked 4 November 2026 with `gh repo view`; a signed-out browser could also open it). Anyone can read the plan, the cost model, the org names, `getai.ghe.com`, the gate's design and the identity names. Boroon to decide. Advice: make it private (Settings, General, Danger Zone, Change visibility). The catch: on GitHub Free, rulesets are not enforced on private repos, so `main` loses its ruleset unless the account is on Pro; with Boroon as the only writer that matters less. Making it private stops new readers but does not undo copies already made.
- **Gate work is laptop work (decided 3 November 2026).** Connecting `getai.ghe.com` to Claude's cloud (Git providers) needs a Claude Team or Enterprise plan, and Boroon is on an individual plan. So any change to `GetAI-IP/factory-gates` runs from his laptop: a local Claude Code session, a cloud session attached to a laptop folder by Remote Control, or a cloud session that prepares a patch he applies (as in Session 9). The steps below are kept only in case a Team plan comes later (the docs cover GitHub Enterprise Server and say nothing about `*.ghe.com`).
  - **The steps** (from https://code.claude.com/docs/en/github-enterprise-server, read 3 November 2026; the page covers GitHub Enterprise Server and is silent on `*.ghe.com`). Needs the Owner or Primary Owner role in the Claude org (Team or Enterprise plan) and permission to create GitHub Apps on `getai.ghe.com`. (1) Create the empty private repo `GetAI-IP/factory-gates` (move step 2). (2) claude.ai, Organization settings, Git providers (https://claude.ai/admin-settings/source-control#github-enterprise), GitHub Enterprise section, Connect, "Set up automatically": display name up to 20 characters, hostname `getai.ghe.com`, leave the CA field empty. (3) Continue to GitHub Enterprise, review the pre-filled app, Create GitHub App. (4) Install the app on `factory-gates` only. (5) On claude.ai/code connect your own GitHub Enterprise account from the repository picker, then start a new session with the repo. If the guided redirect is blocked, use "Add manually" (needs app ID, client ID, client secret, webhook secret, private key; copy the webhook URL Claude generates into the app).
  - **Likely trip points, my inference, untested:** the GHE.com API is at `api.getai.ghe.com`, not `/api/v3` as on Server (see `lcp/apply_rulesets.py`), and the page does not say Claude handles that; the app manifest has no Workflows permission, so a push touching `.github/workflows/` (the first push of the split, the step 8 patch) is refused until Workflows read and write is added in the app's settings and approved; an enterprise IP allow list needs Anthropic's outbound IPs; the cloud environment may need `getai.ghe.com` and `api.getai.ghe.com` under Allowed domains.
- **Five orgs, one central gate (Boroon, 3 November 2026).** The enterprise on `getai.ghe.com` is `GetAI`. The central org `GetAI-IP` holds `factory-gates` and the held-out tests (`factory-holdout`). Four orgs will use the gate: `AI-Business-Solutions`, `AI-Managed-Services`, `Cloud-AI-Platforms`, `GetAI-Knowledge`. Org logins have no `_tqa7h098` suffix (checked for `GetAI-IP` by its URL; assumed for the others, check `AI-Business-Solutions` before step 12). **But the OIDC `workflow_ref` claim does carry it** (`GetAI-IP_tqa7h098/oidc-probe/...`, spike 0.2), while `sub` and `job_workflow_ref` do not. Anything that matches on `workflow_ref` must allow for the suffix. The gate is a repo, a workflow file and rulesets, not a GitHub App; its only Apps are the three read-only token Apps (gate reader, holdout reader, team reader; made 24 November 2026, Session 45). **Design, proposed, not built:** `lcp-gate.yml` becomes a reusable workflow; each of the four orgs gets a small private caller repo that its own `factory-required-workflows` ruleset points at; one `org.json` per org. Until then `rulesets/org.json` and `templates/CODEOWNERS` describe `AI-Business-Solutions`. **Checked:** (b) below is true. `factory-gates` Settings, Actions, Access offers "Accessible from repositories in the 'GetAI' enterprise", now set. Access is allowed only from private repos, so the callers must be private. Still to check: (a), (d), and (c) across orgs.
  - The four checks behind that design: (a) a ruleset can only require a workflow from a repo in its own org, hence the callers (belief); (b) a private reusable workflow can be shared across the enterprise (**checked true**); (c) `job_workflow_ref` in the OIDC token names the central workflow when a caller runs it, so the federated credential pin to `release` still works (**checked true within one org**, spike 0.2, 4 November 2026: a ruleset workflow in `GetAI-IP` running on `oidc-probe-target` called `oidc-probe/.../probe.yml@main`, and `job_workflow_ref` was `GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`; across orgs not tested); (d) whether a token App owned by `GetAI-IP` can be installed on the other orgs, or each org needs its own pair (unknown).
- **Until a second approver exists** (Boroon, 3 November 2026): `release-protection` in `GetAI-IP/factory-gates` has 0 required approvals, and `factory-gates` is excluded from the `GetAI-IP` org ruleset `protect-main`. Rule 17's "reviewed" is self-review meanwhile, so keep write access to Boroon alone. Before step 12 makes the gate required on any org: set approvals to 1, tick "Require approval of the most recent reviewable push", and remove the exclusion. When someone other than Boroon starts working on the factory, also make `self-test` a required status check (see the `self-test` bullet below).
- **Done: the second Dependabot round** (Session 24, 13 November 2026). #10 and #11 were closed by Dependabot on 9 November as superseded by #14 and #13; Boroon merged #9, #13 and #14. Kept here one session for the record. **For each new Dependabot pull request, the routine stays:** read the release notes for every major crossed, check the pin against the tag with `git ls-remote`, see `self-test` green on today's `release` (if its run is older than the last merge, `@dependabot rebase` first), then Boroon merges. Close none.
- **Done in gate PR 27 (Session 45, 24 November 2026; merged by Boroon the same day): every token step uses `client-id`**, with the variables `GATE_READER_CLIENT_ID` and `HOLDOUT_READER_CLIENT_ID` in place of `..._APP_ID`. The `app-id` deprecation warning is gone from its run. Plan Appendix A matches, at Boroon's word. From Session 11's follow-ups. Kept here one session for the record.
- **The gate's three token Apps exist** (Session 45, 24 November 2026, ADO 2537, **Done**; runbook `docs/plans/token-apps/README.md`, IDs in ADO 2537). `ai-factory-gate-reader` (Contents read, `factory-gates` only) and `ai-factory-holdout-reader` (Contents read, `factory-holdout` only), both owned by `GetAI-IP`; `ai-factory-team-reader-abs` (organisation Members read), owned by and installed on `AI-Business-Solutions`, one per project org (Boroon's choice). `GetAI-IP/factory-holdout` exists, empty. Their keys and client IDs are in `AI-Business-Solutions` for selected repos, none selected yet; the gate reader's pair is also on `factory-gates`. **Before 2539:** add the project repo to all six (by the API, so no key is needed again). **Rotate the three keys quarterly.** The gate reader's token is proven (gate PR 27, run 40782026); the other two, and a token minted from another org, are first used in 2539.
- **The follow-ups in `GetAI-IP/factory-gates` are done in PR 7** (Session 10), merged 4 November 2026: README step 9 and the move marked done, the `dependabot.yml` comment, and next slice 2, the self-test workflow.
- **`self-test` is not a required status check** on `release-protection`. **Boroon, 4 November 2026: turn it on when someone other than him starts working on the factory**, with the second-approver changes above. The change: in `release-protection`, add "Require status checks to pass" with the check `self-test`, source GitHub Actions; leave "require branches to be up to date" off. Until then `self-test` is advice, not a lock: a pull request into `release` can merge with it red, so check it is green before merging, Dependabot pull requests included.
- **The allowed MCP client entry for `getai-fl1-exec` stays in `factory-lane-1`** (Boroon, 6 November 2026, Session 13): name `getai-fl1-exec`, unique name `new_getaifl1exec`, enabled. It grants nothing while the app has no credential. At Stage 3, either keep it or replace it with one added by code (a GET AI solution with the `getai` publisher, or `dataverse mcp allow`), and give lanes 2 and 3 theirs the same way. The list as it was before the spike is in `docs/plans/spike-0.3/README.md`, step B.
- **The lane's MCP cap is a call count in the driver** (Boroon, 13 November 2026, Session 22; plan 5.11, 5.14, 14.4). Dataverse MCP calls are billed 0.1 Copilot Credit each from the tenant's shared prepaid pool. "Draw from tenant" stays on, with no allocation per lane. The driver counts each session's MCP calls, stops at a cap per session held in the lane config, and retries a failed call up to three times; either stop is a PARK. Still to settle, in spike 0.14 (2461) and the Stage 3 driver spec: the cap's number (from the calls part 4 counts). **Tried in part 3** (Session 27, run 39749076): a stdio shim in front of the local proxy counts and retries (`docs/plans/spike-0.14/mcp_shim.py`); a retried create whose answer was lost **did write twice**, and one with its own row ID did not; the agent's own mistakes (bad query, missing table) came back the same four times, so retrying them only spends calls and would PARK the night on a typo. **Decided (Boroon, 20 November 2026), both as proposed in Session 27:** retry only where it is safe and can help (the table under part 3 in the spike README): no retry on a tool result with `isError`, which goes back to the agent with no PARK; retry no answer, proxy errors and throttling up to three times; retry writes only by row ID, with the shim adding a row ID to every create. And the PARK type `tool_failure` for a call that still fails (`budget` stays for the cap). **In the plan since 21 November 2026** (5.11, 5.14, Appendix D, 14.4; Session 28): the retry rule, `tool_failure`, both never-repeat choices, billing of every call that reaches Dataverse, and the starting cap of 50. **Since Session 28:** the shim follows the accepted rule (21 local checks); the bill confirms every call that reaches Dataverse is billed, tool errors included (20 rows of 0.1 for part 3); part 4's two tiny stories made 0 and 1 MCP calls; the proposed starting cap is 50 per session (spike README, proposal 4).
- **The gate installs Copilot CLI unpinned** (seen in Session 13, not changed): `lcp-gate.yml` on `release`, `verify-in-test`, runs `npm install --global @github/copilot` with no version or hash. Spike 0.3 shows a pattern that works on a hosted runner for a package with no dependencies: fetch the tarball, check it against the registry's `sha512`, `npm install --global --offline --ignore-scripts` from the file. Check first whether `@github/copilot` has dependencies (if so, pin with a lockfile instead). A gate slice, by pull request there.
- **Sources are complete.** Boroon uploaded the whole research folder as a zip. Every file was checked by checksum against the repo, duplicates were skipped, and the rest were added. The other session ("Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`) is no longer needed for sources and can be deleted.
- **Not read in full.** The files added from the zip were saved but not read in this session: the reports V1 and V2, the runtime and costs note, the eight GitHub and Azure notes, the five Power Platform notes and the one-pager. The five workshop slide images were saved but not viewed. The plan condenses most of them. Read one only when a task needs its detail.
- **Decisions still waiting on Boroon** (from `docs/analysis/tshirt-sizing.md`): approve the shortlist of skills to read in full before any are adopted (plan section 8.3); decide whether to write a GET AI router skill that routes by size. The sizes themselves are approved, and the ADO field `Custom.WorkSize` is decided (7 November 2026, Session 16).
- **A second approver is needed by Friday 4 December 2026** (Session 16 schedule). 2520 (undo the stopgaps) and 2521 (apply the rulesets) need a second person and the three CODEOWNERS teams; without them the Stage 1 exit test (2539, Friday 18 December) cannot happen. The dated order is in `docs/plans/schedule.md`.
- **Spike 0.20, time and tokens per story on every engine, is not run** (Session 16). ADO story 2738 under Feature 2737 (Stage 1). It needs Claude Code's OpenTelemetry turned on through managed settings and somewhere to send it: Application Insights does not exist yet, so use a local collector first. The docs do not say whether the VS Code extension or the desktop app export it; this session runs in the desktop app, so test there first.
- **Keep pinned kits current (A1, Boroon, 7 November 2026, Session 17).** Spec Kit moved three releases in five days. Proposed shape in `docs/plans/stage-1-day-gate-plan.md`: a pin register, Dependabot where the ecosystem allows, and a monthly manual pass at the component register review (plan 8.2), the first with the Ignite re-check on 23 November. Not built; an ADO story is to be created.
- **Done: transcript retention is 365 days** (Session 19, 8 November 2026, Boroon's choice): `"cleanupPeriodDays": 365` in `~/.claude/settings.json` on the laptop. Found while checking: Claude Code keeps sessions started or last continued in the desktop app at any age unless `desktopSessionCleanupPeriodDays` or a managed `cleanupPeriodDays` is set, so the 30-day limit hit only terminal sessions (transcripts from 5 August were still on disk). `0` is refused with a validation error. Kept here one session for the record.
- **Done: the scratch of spikes 0.14, 0.18 and 0.19 is deleted** (21 November 2026, at Boroon's word, Session 28). In `factory-lane-1`, as the lane identity by the Web API (`tools.yml` modes `scratch-list` and `scratch-delete`): both cloud flows, the role, the environment variable and its value, the connection reference, the App Spec app with its site map, settings and icon, both `fspk_` tables, the solution `FactorySpike` and the publisher `factoryspike`. The icon's delete timed out twice (HTTP 503, SQL timeout) and went through on a third try under Boroon's own sign-in. A last read-only listing found nothing left. Then the repo `GetAI-IP/export-probe` and the federated credential `export-probe-fl1-exec` were deleted. **Kept for Stage 3:** `getai-fl1-exec` (no credentials now), its application user, `factory-lane-1` and the allowed MCP client `new_getaifl1exec`. Every probe and workflow has a copy in `docs/plans/spike-0.14/`, `spike-0.18/` and `spike-0.19/`. Details: the spike 0.14 README, "Scratch".
- **A table or column outside the lane solution stops the lane** (Boroon, 10 November 2026; plan 5.4 step 4). Metadata keeps no maker, so the reset never deletes one that the bootstrap list does not hold: the lane goes Offline, an ADO bug names it, and a person checks by day. **ADO 2843** builds that check (the bug, a runbook, one trial in `factory-lane-1`). It sits under 2575 "Execution workflow and driver" (Stage 3), after 2577 (`reset_environment.py`); not dated, like the rest of Stage 3.
- **Two things for `reset_environment.py` to learn** (Session 20, not built). It cannot find forms or canvas apps by maker (no `createdby` on their tables), and it must allow the lane manifest's own environment variable values, or step 4 deletes what step 3 set. Both are in the 0.19 record.
- **Keep spike runs in one session.** In Session 19 a "btw" side chat on the laptop started its own setup run in `GetAI-IP/export-probe` (run 37180986) while the main session was running the probe. It queued behind the probe and changed nothing (setup only makes what is missing), but two sessions driving one scratch repo and lane can step on each other. Session 20 kept every run in one session; 0.19's workflow shares 0.18's concurrency group, so runs queue.
- **Fixed: the skill's glossary example broke its own rule** (found and fixed in Session 18, at Boroon's word). In `.claude/skills/getai-domain-modeling/glossary-format.md`, the example term "Customer" had no `_Schema_` line, though the rules say every term has one. It now has `_Schema_: none yet`. It reaches `main` when Boroon merges the Session 18 branch (rule 17). The DG1 template does not use that term, so it needed no change. Kept here one session for the record.
- **Gotcha: the two copies of the glossary and ADR formats split on Friday 4 December** (found in Session 18). Until then the skill (`.claude/skills/getai-domain-modeling/`) and the templates (`staging/factory-manifestos/templates/project/`) sit in this repo, so one PR changes both, as the staging rules say. After the move (DG8) the templates are in `GetAI-IP/factory-manifestos` on GHE and the skill stays here, so one PR cannot change both and the copies can drift. DG8 settles how to keep them the same, for example two PRs that link each other (step 5 of DG8 in `docs/plans/stage-1-day-gate-plan.md`).
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The zip copy is the same, so the source itself is cut off.
- **Credit funding: accepted (Boroon, 2 November 2026).** Builds for customers can be made on credits. Settled.

## Log

## Session 46, 2026-11-24, branch `claude/session-46-2541-factory-test`

ADO 2541: bootstrap `factory-test` with its Test identity and test user. On the laptop (desktop app), track B (the tenant), on its Tue 24 Nov date in Session 37's schedule. Planning branch in its own worktree (`.claude/worktrees/session-46-2541`, from `main` at `8249d1e`), because Session 45 (2537) works in the same folder. Session renamed "40. Stage 1 - Add - factory-test, test identity and test user", at Boroon's word, after "39. Stage 1 - Add - Gate token Apps".

Done (by CLI as Boroon, each create at his word, each read back; record `docs/plans/factory-test/README.md`, IDs in ADO 2541):
- **`factory-test`**: `https://factory-test.crm6.dynamics.com/`, Sandbox, Australia (`australiaeast`), AUD, no security group. Managed Environment on, solution checker **Block**. Dataverse auditing on for the organisation and the Workflows table.
- **`getai-nwt-test`**: Entra app and service principal, single tenant, no secret, no certificate, no API permission, no federated credential yet. Application user in `factory-test` with System Administrator. `getai-fl1-exec` has no user there.
- ADO 2541: **Building**, body rewritten with the result, the IDs and what waits.

Decisions (Boroon, 24 November 2026, asked in this session):
- The Northwind pilot's project code is **`nwt`**: `getai-nwt-test`, `factory-test-nwt@getai.com.au`, `projects/nwt/` in `factory-gates`.
- Claude makes what Boroon's roles allow, by pac and az signed in as him, asking before each create.
- The factory's Key Vault goes in the subscription `AzureCSP_GetAI_CloudandDataPlatforms`.
- The test user and its certificate sign-in are asked of the identity admins (a draft message in the README).

Found (README, Findings):
1. Boroon's account has Power Platform Administrator and Cloud Application Administrator in Entra, and **only Reader** on the CSP subscription. So it cannot make the test user, give its licence, set up certificate sign-in, read the authentication methods or Conditional Access policies, or make the Key Vault.
2. The Connection reference table's auditing cannot be turned on (`CanBeChanged` false); plan 5.3 asks for it.
3. Microsoft's Build Tools page now asks only for the application user with System Administrator, not the API permissions plan 5.3 cites. None added; add PowerApps-Advisor `Analysis.All` only if the checker fails as the Test identity.
4. Right after the change, one admin API read still said `Basic`; with `$expand=properties.governanceConfiguration` it reads `Standard` and `block`. The preflight should read it that way.
5. The gate's Playwright step passes `KEYVAULT_NAME`, but Microsoft's toolkit reads `MS_AUTH_EMAIL`, `AZURE_KEYVAULT_URL`, `AZURE_CERTIFICATE_NAME` and `AZURE_TENANT_ID`. For 2546 and 2447.
6. No ADO story made the Northwind project repo, the Key Vault or the evidence Blob (now 3059 and 3060, below).
7. 19 spare Power Apps Premium licences.
8. **Not imported: Northwind.** An unmanaged import into Test would sit under the gate's managed imports as an unmanaged layer, so Northwind reaches Test through the gate (2459 or 2539). DG9's step 1 ("if 2541 has not") needs Boroon's word.

Files changed: `docs/plans/factory-test/README.md` (new), `docs/progress.md`, `CLAUDE.md` (a row for the new folder), `docs/plans/schedule.md` (2541's status, 3059 and 3060 under "Not dated yet", a Changes line; added after pull request 57, the dashboard sync, brought Session 37's redraft to `main` and was merged into this branch). No date moves.

Time and tokens (in 2541's body; session `93361b73`, measured before the last commit, `--root` the main folder's project transcripts): active time 0 h 23 min (gaps over 10 minutes not counted), from 24 Nov 11:01 to 24 Nov 12:53 (UTC+11). Tokens: 52,247 output; 13,712,079 processed in all, of which 12,927,829 were cache reads. From 1 local transcript.

Open items:
- **Boroon: send the admins' message** (README, "Draft message to the admins"; their names to go in ADO 2541). Two asks: the Entra identity admins (the test user, its licence, a group, the test CA in the trust store, certificate sign-in for that group only, binding rules for that CA, and whether Conditional Access asks it for MFA); the CSP subscription's owner (a resource group `rg-getai-factory-aue` in Australia East, with Boroon as Owner on it).
- **2447 (spike 0.11, Thu 26 Nov) needs the test user and the vault,** so it slips if the admins are not done by then. Dates move only at Boroon's word.
- **Then, back here:** the vault and the certificate by CLI (README, step 2), the test user's `certificateUserIds` value to the admins, Basic User in `factory-test`, and the CA key decision (destroy, or keep in a separate vault).
- **The federated credentials**: the Northwind project repo's, once a story makes that repo; triage's at Stage 2 or later; a scratch one if 2459 runs from a scratch repo.
- **Possible plan edits** (Boroon to decide, none made): 5.3's audit sentence (Connection reference cannot be audited here) and its "App permissions" for the Test identity (Microsoft's page no longer asks for them).
- **Done: two new stories, at Boroon's word** ("Yes, add both", 24 November 2026), both Proposed and not dated (dates at his word): **ADO 3059** "Northwind project repo for the Stage 1 exit test" (under Feature 2536; after 2541, before 2539) and **ADO 3060** "Azure resources for the gate: Key Vault and evidence storage" (under Feature 2540; before 2447 and 2539). 3060 also asks who writes evidence to Blob: plan 5.1 names an evidence-writer managed identity, but the gate uploads as the Test identity (README finding 8).
- Feature 2540 is still "Not Started" in ADO; it could move to In Progress at Boroon's word.

Planning PR: https://github.com/boroonmahanta/overnight-ai-factory/pull/58, opened at Boroon's word on 24 November 2026, **merged by Boroon the same day** (`1d58bf8`). `main` (pull request 57) was merged into the branch first; the only clash was the top of this log.

Later in the session (branch `claude/session-46-3059-nwt-source`, from `main` after pull request 58, in the same worktree):
- **3059's open items settled by Boroon** (24 November 2026): the repo is **`ai-factory-nwt`**, and the solution comes from Microsoft's page "Install Northwind Traders database and apps" (https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/northwind-install). Then the org: **`AI-Business-Solutions`** (Boroon, the same day, added to pull request 59), so the repo is `AI-Business-Solutions/ai-factory-nwt`. Its first gate run is also the gate's first across orgs (spike 0.2 tested within one org only), so 2531, the callers build, may be needed first; noted in 3059 and the README.
- The page's file is `NorthwindTraders_final.zip` on `download.microsoft.com`, 666,816 bytes, last modified 29 January 2025 (headers only; not downloaded, which needs Boroon's word). It holds the tables, choices and business processes, the Northwind Orders canvas and model-driven apps, a Sample Data canvas app that loads the rows after a consent prompt, and tutorial "Begin Part" canvas apps.
- ADO 3059's body now carries the name, the file and two things to watch: the gate's manifest check fails closed on `CanvasApps/`, so a reviewed gate PR must add the kind from the real export (or the canvas apps stay out of the repo's solution) before 2539; and loading sample data is a day step for a person, or the locked scenarios seed their own rows. A fork of this session had already added a comment to 3059 saying the same; no branch of its own.
- README: section 3 names the repo and adds `EVIDENCE_ACCOUNT`; a new section 4, "The Northwind solution".
- Planning PR: https://github.com/boroonmahanta/overnight-ai-factory/pull/59, opened at Boroon's word on 24 November 2026, for him to merge.

Next steps:
1. Boroon sends the admins' message. Done: pull request 58 merged.
2. Wed 25 Nov: 2459 (spike 0.10) in `factory-test`, with `getai-nwt-test`.
3. When the admins are done: finish 2541 (vault, certificate, role), then 2447.

## Session 45, 2026-11-24, branch `claude/session-45-2537-token-apps`

ADO 2537: the gate's three token Apps, on its date. On the laptop (desktop app), session renamed "39. Stage 1 - Add - Gate token Apps". The planning branch is in its own worktree (`.claude/worktrees/session-45-2537`, from `main` at `8249d1e`, later merged up to `2380313`). The gate branch is in a worktree of the gate clone inside it, `factory-gates/`. The shared gate clone was not switched.

Read for it: Sessions 43 and 44's entries; in the gate repo `lcp-gate.yml`'s token steps and README sections "The team reader token" and "Moving to GHE.com"; GitHub's docs on registering and installing Apps, private keys, organisation secrets and ruleset workflows (Enterprise Cloud, read 24 November 2026).

Decisions (Boroon, 24 November 2026, all as recommended):
- **One team reader App per project org**, owned by that org, not one enterprise-owned App. A leaked key shows only that org's members. So whether GHE.com has enterprise-owned Apps was not checked.
- **Make `GetAI-IP/factory-holdout` now, empty**, so the holdout reader can be installed and tested.
- **IDs and keys for selected repos only**: org variables and secrets in `AI-Business-Solutions` with access "selected repositories" (none yet), and the gate reader's pair also on `factory-gates`, so the gate's own pull requests test the token.
- **`client-id` with the variables renamed**, in the gate and in plan Appendix A.
- Boroon named the Apps with an `ai-` prefix (`ai-factory-...`), like the org's teams.

Done:
- **`GetAI-IP/factory-holdout`** (by Claude, at Boroon's word): private, a README as its only commit, ruleset `main-protection` copied from `factory-gates`'s `release-protection` (pull requests only, 0 approvals until a second approver exists, no force push, no deletion, no bypass). Its pull request 1 corrects the App's name in the README: https://getai.ghe.com/GetAI-IP/factory-holdout/pull/1, merged by Boroon on 24 November 2026.
- **The runbook**, `docs/plans/token-apps/README.md`: the three Apps, the portal fields, the key commands Boroon runs himself, rotation, what a leaked key exposes, and what was checked.
- **The Apps** (made by Boroon in the portal, with a side session): `ai-factory-gate-reader` and `ai-factory-holdout-reader` (owner `GetAI-IP`, Contents read, one repo each), `ai-factory-team-reader-abs` (owner `AI-Business-Solutions`, organisation Members read). Checked by API: each installation has exactly its permission and no events. Boroon stored the four keys; Claude never handled them. Claude set the four client ID variables. The org entries have access "selected repositories", none selected.
- **Gate PR 27** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/27, branch `gate-reader-client-id`, on `release` at `7663cc9`): `client-id` in the five gate reader steps and the holdout step; a test that pins every token step's inputs and jobs (643 tests, 4 skipped by design; the test failed on all 12 deliberate breaks); README section "The token Apps (ADO 2537)", with what the run showed. No hashed file changed, so `scripts.sha256` is unchanged. `self-test` green. **Merged by Boroon on 24 November 2026** (06:17 UTC): `release` is at `1c22a4a`, with the same tree as the tested `49c1456`.
- **The first real token** (`lcp-gate` run 40782026 on gate PR 27): `map` and `locks` minted the gate reader token by `client-id`, checked out `release`, passed the hash check, and revoked the token at the end. No `app-id` warning. `lane_map.py` mapped the branch to lane `none`, and the run stopped at `build`: "no solution source to pack: pr/src is missing or empty". That is where a gate pull request should stop. Until today every gate pull request stopped at `map`'s token step.
- **Plan Appendix A**, at Boroon's word: the six token steps on `client-id` with the renamed variables, and a sentence in "The gate reader keys are secrets". The YAML still parses, with all six jobs.
- ADO 2537 **Done** (24 November 2026, at Boroon's word, after both merges), with the IDs, the choices, the check and the time line in its body, and a comment recording the merges. Schedule: 2537 done on its date.

Time and tokens (in 2537's body; session `cf66f678`, measured before the last commit; run with `--root` set to `~/.claude/projects/-Users-Local-VS-Code-10-overnight-ai-factory` and `--session cf66f678`). Active time 0 h 31 min (gaps over 10 minutes not counted), from 24 Nov 11:01 to 24 Nov 17:07 (UTC+11). Tokens: 75,763 output; 18,510,060 processed in all, of which 17,706,941 were cache reads. From 1 local transcript. The side session that helped make the Apps is not counted.

Files changed:
- Here: `docs/plans/token-apps/README.md` (new), `docs/sources/plan-v3.1.md` (Appendix A), `docs/plans/schedule.md`, `docs/progress.md`, `CLAUDE.md` (the `factory-gates` row and a map row).
- In `GetAI-IP/factory-gates` (gate PR 27): `.github/workflows/lcp-gate.yml`, `tests/test_workflow.py`, `README.md`.
- In `GetAI-IP/factory-holdout`: `README.md` (first commit; pull request 1).

Open items:
- **Done: gate PR 27 and holdout PR 1 merged by Boroon on 24 November 2026.** Checked on `release` (`1c22a4a`): 643 tests OK (4 skipped by design); `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` clean; 7 scripts left on `pending-scripts.txt`. The gate worktree and its local branch are removed; the remote branch was deleted on merge. 2537 is Done.
- **Before 2539:** add the Northwind project repo to the six `AI-Business-Solutions` variables and secrets (`PUT .../actions/secrets/<NAME>/repositories/<repo-id>`, and the same for variables). The holdout and team reader tokens, and a token minted from another org for `GetAI-IP`'s installation, are first tried there.
- **Plan edit for Boroon** (none made): Appendix A's `danger` job still lacks the team reader token step (Session 44's open item), and a 14.4 row could record today's choices (one team reader per org, `factory-holdout` made early, selected repos only).
- `GetAI-IP`'s base permission is read, so every `GetAI-IP` member can read `factory-holdout` once it holds tests (Stage 4). Agents are not members. Revisit before the held-out set is written.
- Seen, not touched: another App, `get-ai-project-setup`, is installed on `GetAI-IP` with wide write permissions (administration, contents, repository creation, organisation administration). It is not the factory's.
- Rotate the three keys quarterly; the first by about 24 February 2027.

Planning PR: https://github.com/boroonmahanta/overnight-ai-factory/pull/60, opened at Boroon's word on 24 November 2026, for him to merge. It merges `main` up to `cb8c15e` (Session 46): both log entries and map rows kept, and this session's schedule change line moved into the Changes list, where it belongs.

Next steps:
1. Done: Boroon merged gate PR 27 and holdout PR 1; 2537 is Done.
2. Boroon merges planning PR 60.
3. Wed 25 Nov, as scheduled: 2451 (spike 0.6), then 2531 on Laptop C.


## Dashboard sync, 2026-11-24, branch `claude/schedule-sync-2026-11-24`

Done:
- Reran `tools/progress_snapshot.py` and synced the "Factory build progress" dashboard three times (143 stories, 16 of 40 scheduled done, 71 sessions). Old snapshot files kept.
- ADO: 2538's Finish Date moved from Thu 26 to Tue 24 Nov, the day it was done, at Boroon's word. A one-day shift of 2537, 2541, 3019, 2546 and 2459 was made on a misread clock and undone within minutes; their dates are as Session 37 set them.
- `docs/plans/schedule.md` now carries Session 37's redraft (its branch `claude/session-37-stage-1-this-week` is not merged, and is behind `main`), merged with Sessions 36 and 39's rows: 2538 Done Tue 24 Nov, 3026 kept, 3027 added (Wed 25 to Thu 26 Nov, Laptop A), and the "This week" table's Laptop A column updated.
Decisions:
- Boroon, 24 November 2026: dashboard syncs need no pull request. This branch is pushed, with no pull request.
Files changed: `docs/plans/schedule.md`, `docs/progress.md`.
Open items:
- When Session 37's branch merges, take this branch's `schedule.md`: it holds all of Session 37's rows plus the later ones.
Next steps:
- Today (Tue 24 Nov): 2537, 2541, 3019 and the 2546 draft, as in the schedule.

## Session 44, 2026-11-24, branch `claude/focused-pare-44ad71`

Gate README finding 19 settled in code: **gate PR 26** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/26, branch `gate-merge-policy-token`, commit `0294a7c`, on `release` at `0db69f6` after gate PR 25). `self-test` is green on Python 3.11, 642 tests OK (run 40659146). `lcp-gate` is red at `map lane`, as on every gate PR (run 40659141). **Merged by Boroon on 24 November 2026** (10:46 UTC+11): `release` is at `7663cc9`, with the same tree as the tested `0294a7c`.
- Where it ran: on the laptop (desktop app), as a side session started by Session 43's session. The planning branch is in its own worktree, from `main` and brought up to `ea618a5` (Session 43's merge). The gate branch is in a worktree of the gate clone inside it, `factory-gates/`. The shared gate clone was not switched.

Read for it: Session 43's entry; in the gate repo `lcp/merge_policy.py`, `danger` in `lcp-gate.yml`, `rulesets/org.json`, the tests for both, and README findings 19 and 20.

**What GitHub's docs say** (Enterprise Cloud docs, read 24 November 2026; no live check needed):
- The job token's permissions "are limited to the repository that contains your workflow". None of its `permissions:` keys is at organisation level.
- Both `GET /orgs/{org}/teams/{team}` and `.../memberships/{user}` need the organisation permission Members (read). User and App installation tokens can hold it.
- A token that cannot see a team can get a 404, which GitHub also uses for "not a member". So the policy as written would have shown every approver as outside the team, with no hint at the token.
- The pinned `create-github-app-token` (v3.4.0) takes `client-id`, `owner` and `permission-members: read`. It errors when the App lacks a permission it asks for, and revokes the token in its post step.

**Decision (Boroon, 24 November 2026): a dedicated read-only App,** "New team-reader App", not more permissions on the gate reader App.

Done (gate PR 26):
- **`lcp-gate.yml`, `danger`:** a token step just before the policy, after both review sessions have ended, so no agent runs while the token exists.
  - Its inputs: `client-id: vars.TEAM_READER_CLIENT_ID`, `private-key: secrets.TEAM_READER_KEY`, `owner: github.repository_owner`, `permission-members: read`.
  - Only the policy step reads the token, as `TEAM_READER_TOKEN`. `GH_TOKEN` stays the job token, for the PR and its reviews.
- **`lcp/merge_policy.py`:** each token is used only for its own calls. The team is read first. If that fails, the answer names another team, or a membership read fails with anything but 404, the policy says "the team reader token cannot read @org/team ..., so no approval can count", and names finding 19. A missing team token on the human path is exit 2. The auto-merge path needs neither token.
- **Tests:** 6 new, 642 in all (4 skipped by design). The fake GitHub shows the team only to the team reader token and the PR only to the job token, and every policy test fails if either token reaches the other's calls or shows in any output. Proved by breaking a copy 18 ways; all 18 failed.
- **README:** finding 19 settled in code; a new section "The team reader token (finding 19)" with the docs, the App to make, the workflow, across orgs and the tests; the file table, counts and next slice 6.
- `scripts.sha256` made last. `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` are clean.

**Across orgs (the callers' check (d)), half settled by the docs:**
- A private App "can only be installed on the account that owns the app". The gate reader and holdout reader read only `GetAI-IP` repos, so they need no install anywhere else, only their ID and key in each project org.
- The team reader reads the project org's own teams, so it must be installed on each project org. That means one App per org, owned by that org, or one App owned by the `GetAI` enterprise, which "can only be installed on your enterprise or organizations within your enterprise". The docs don't say whether GHE.com with data residency has enterprise-owned Apps.

ADO: 2538 stays **Done**. Its body gains this session's result and time line, and a comment records the merge. 2537's body gains the third App.

Time and tokens (in 2538's body; session `1980209e`, measured before the last commit; from a worktree, with `--root` set to this worktree's own project folder and `--session`). Active time 0 h 18 min (gaps over 10 minutes not counted), from 24 Nov 10:08 to 24 Nov 10:39 (UTC+11). Tokens: 88,492 output; 17,440,022 processed in all, of which 16,933,544 were cache reads. From 1 local transcript.

Files changed:
- Here: `docs/progress.md`.
- In `GetAI-IP/factory-gates` (gate PR 26): `.github/workflows/lcp-gate.yml`, `lcp/merge_policy.py`, `tests/test_merge_policy.py`, `tests/test_workflow.py`, `README.md`, `scripts.sha256`.

Open items:
- **Done: gate PR 26 merged by Boroon on 24 November 2026.** `release` is at `7663cc9`, with the same tree as the tested `0294a7c` (`2dded0e`); the remote branch was deleted on merge. Checked on `release`: 642 tests OK (4 skipped by design); `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` are clean; 7 scripts left on `pending-scripts.txt`. The gate worktree and its local branch are removed.
- **2537 (Tue 1 Dec) now makes three Apps.** The third is `factory-team-reader`: organisation Members read only, installed on `AI-Business-Solutions`, with the org variable `TEAM_READER_CLIENT_ID` and the secret `TEAM_READER_KEY`. First check in the enterprise settings whether the enterprise can own Apps. Until it exists, `danger` fails at the token step, which is the same answer as before: no human merge passes.
- **Plan edit for Boroon** (none made): Appendix A's `danger` job lacks the team reader token step and `TEAM_READER_TOKEN`. Appendix A's job table (the `danger` row) and its note "The gate reader keys are secrets" could name the third App.
- Not tested: the App and the token step on `getai.ghe.com`; what GitHub answers there to the job token on a team endpoint (403 or 404; both are handled); whether an org installation can select no repositories.
- `CLAUDE.md`'s `factory-gates` row is still several sessions behind (not edited). When it is: `release` is at `7663cc9`, with 642 tests, 7 pending scripts and the team reader token.

Planning PR: https://github.com/boroonmahanta/overnight-ai-factory/pull/56, opened at Boroon's word on 24 November 2026, for him to merge.

Next steps:
1. Done: Boroon merged gate PR 26.
2. Boroon merges planning PR 56.
3. 2537: make the three Apps, then the first real `lcp-gate` run.

## Session 43, 2026-11-24, branch `claude/xenodochial-carson-eb7fd6`

ADO 2538, slice B2: `merge_danger_combine.py` and `merge_policy.py`, the last two Merge Danger scripts, as **gate PR 25** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/25, branch `merge-danger-combine`, commit `b0251f1`, on `release` at `3a4db23` after slice C's gate PR 24). `self-test` is green on Python 3.11 (run 40647126). `lcp-gate` is red at `map lane`, as on every gate PR. Open, for Boroon to merge.
- Where it ran: on the laptop (desktop app). The planning branch is in its own worktree (`.claude/worktrees/xenodochial-carson-eb7fd6`, from `main`, brought up to `0916057` with Session 42's merge). The gate branch is in a worktree of the gate clone inside it, `factory-gates/`. The shared gate clone was not switched.
- Started by Session 41's session as a side session. At Boroon's word it was moved to the top level and renamed "37. Stage 1 - Build - Merge Danger combine and policy", after "36. Stage 1 - Build - Checker, verdicts and spec check" (Session 42).
- This record is **pull request 55** (https://github.com/boroonmahanta/overnight-ai-factory/pull/55), branch `claude/xenodochial-carson-eb7fd6`, into `main`, opened at Boroon's word on 24 November 2026. Boroon merges.

Read for it:
- Sessions 41 and 42's entries.
- Plan 5.10 and Appendix B (B.4 to B.6).
- `lcp-gate.yml`'s `danger` job.
- The gate README's floor and slice C sections.
- `merge_danger_floor.py`, `simple_yaml.py`, `rulesets/org.json`, `apply_rulesets.py` and its fake GitHub.
- Slice C's `parse_verdict.py` and its fixture.

Decision (Boroon, 24 November 2026): **one real review run on the laptop under his Copilot sign-in** ("Yes, run it"), before any code:
- Copilot CLI 1.0.113, on a made-up two-commit diff in the session scratchpad, with no client data.
- The danger step's flags apart from `--agent`, with a 50-credit cap.
- 95 events, exit 0, one premium request.
- Without autopilot there is no `task_complete`. The answer is the content of the last `assistant.message`, with `phase: final_answer`. The tool-calling message is `phase: commentary` and empty. A `result` event follows, with `exitCode` and `usage.codeChanges`.
- A cut-down copy is the fixture `tests/fixtures/review/copilot-1.0.113-standards.jsonl`.

Done (gate PR 25):
- **`lcp/merge_danger_combine.py`** (5.10, B.4). The final score is the highest of the full floor and each review's `raise_to`.
  - A review is **no review** when its log is missing, the session did not finish, it exited non-zero, or it gave no answer.
  - It is **invalid** when the answer is not one B.4 JSON object (bare, or in one ```json fence), names the other axis, misses a field, raises without a written reason, ends on a commentary message, or the session changed files.
  - Neither lowers anything: an invalid answer's readable raise still counts. Both make `reviews_complete` false, so the policy never auto-merges.
  - It writes `danger.json`, then posts a neutral `merge-danger` check run on the head commit. The check run was tested against a fake GitHub only.
- **`lcp/merge_policy.py`** (5.10, B.5). Anything but a PASS verdict is not mergeable, whoever approves.
  - It never auto-merges when any of these hold: anything `unchecked`; the base is `main` or anything but `integration`; a protected path; a floor of 4 or more; a `never` row; a review missing or suspecting drift; the switch off.
  - Otherwise auto-merge needs one class in `trust.yml`, signed off at L2 or above, that holds every row that fired, with the score within the rung's limit.
  - Without auto-merge, the PR needs an approving review on the head commit from an active member of the team that `org.json`'s new `merge_reviewers_team` names, with no team member's latest review requesting changes.
  - In a merge group, the PR number comes from the queue branch.
- **`lcp-gate.yml`, `danger`:**
  - the review wait is `wait "$pid" || true`, as slice C's finding 17;
  - the combine gets `--head-sha`;
  - the policy gets `--verdict`, `--org`, `--pr`, `--head-sha` and `--merge-group-head-ref`, and its `BASE_REF` falls back to the merge group's base.
- `rulesets/org.json` gains `merge_reviewers_team`. `make_rulesets.py` and `apply_rulesets.py` ignore it.
- 73 new tests, 636 in all (4 skipped by design), passing.
  - `test_merge_danger_combine.py` has 37 and `test_merge_policy.py` 35.
  - `test_workflow.py` gains 1, and two more scripts in its flags test.
  - One test makes `danger.json` and `verdict.json` with the real combine and `parse_verdict.py` on their real fixtures, then runs the policy on them.
- Proved by breaking a copy 60 ways.
  - Two survived the first run. One was a typo in the break. The other was a real gap: a trust file that is a link to nothing was read as "no trust file". It still blocked auto-merge, but with the wrong reason. A test was added.
- `pending-scripts.txt` is down to 7, none of them 2538's. `scripts.sha256` was made last. `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` are clean.
- README: the file table, the counts, a section "The combine and the merge policy (ADO 2538, slice B2)" with the choices made, and findings 18 to 20.

Found (gate README):
- **18. The review step names no `--model`**, so Copilot CLI's `auto` picked MAI Code 2 Flash ("the best choice out of the models available in your plan"). It raised a one-column additive change from 2 to 7 for a missing column description. Pin `--model` in both Copilot steps once plan 9.3's choice for review is made (spike 0.6), and calibrate the review prompts against real raises.
- **19. The job token probably cannot read team membership** (untested). The policy counts only an active member's approval, and fails closed with "the token must be able to read the team's members". Before the first PR that needs a human merge goes through the gate (the Stage 1 exit test), give `danger` a token with organisation Members read, or confirm `github.token` can read it on `getai.ghe.com`.
- **20. `danger`'s own evidence is never kept.** `danger.json`, the review logs and the decision live only in the job's workspace, against rule 16. The check run keeps the score and its parts. Not changed.

Made by this session without asking (gate README, slice B2 section; say if any is wrong):
- A readable raise counts even from an invalid answer.
- Every B.4 field is required, and extra fields are ignored.
- A review's drift suspicion blocks auto-merge, not a human merge. Its unknowns put an auto-merged PR in the sample.
- The check run is always `neutral`.
- Where several classes hold the rows, the strictest wins. L2 and L3 classes need `signed_off_by`.
- A broken trust file blocks auto-merge, not a human merge. No trust file means every class is at L1.
- A PR in another org than `org.json`'s cannot pass the human path.
- Not done: B.5's second reviewer at 8 and above on client work (nothing in the inputs says which work is client work), and 5.10's comment beside the check run.

ADO: 2538 is **Done** (24 November 2026, after gate PR 25 merged). Its body holds this session's result and the time line; comments record the plan edits and the merge.

Time and tokens (in 2538's body; session `15db2b29`, measured before the last commit; from a worktree, run `tools/session_usage.py` with `--root` set to this worktree's own project folder and `--session`). Active time 0 h 43 min (gaps over 10 minutes not counted), from 24 Nov 00:35 to 24 Nov 09:56 (UTC+11). Tokens: 132,191 output; 23,208,417 processed in all, of which 22,029,450 were cache reads. From 1 local transcript.

Files changed:
- Here: `docs/progress.md`, `docs/sources/plan-v3.1.md` (Appendix A, a 14.4 row), `CLAUDE.md` (the plan row and the line map).
- In `GetAI-IP/factory-gates` (gate PR 25):
  - `lcp/merge_danger_combine.py`, `lcp/merge_policy.py`, `tests/test_merge_danger_combine.py`, `tests/test_merge_policy.py`, `tests/fixtures/review/` (new);
  - `.github/workflows/lcp-gate.yml`, `rulesets/org.json`, `tests/test_workflow.py`;
  - `README.md`, `pending-scripts.txt`, `scripts.sha256`.

Open items:
- **Done: gate PR 25 merged by Boroon on 24 November 2026.** `release` is at `0db69f6`, with the same tree as the tested `b0251f1`; the remote branch was deleted on merge. Checked on `release`: 636 tests OK (4 skipped by design); `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` are clean; 7 scripts left on `pending-scripts.txt`, none of them 2538's. Slice B2 is done, so **2538 is Done** in ADO (all of A, B and C merged, Boroon's rule of 23 November). The gate worktree and its local branch are removed.
- **`docs/plans/schedule.md` is not edited,** because Session 37's unmerged branch rewrites the same rows (2538 becomes Tue 24 to Thu 26 Nov there). When it merges, 2538's row should say: **Done Tue 24 Nov** (Sessions 38 and 40 to 43; gate PRs 21 to 25). Sessions 34 and 37's branches also change `CLAUDE.md`'s plan row and line map, which this session changed too, so expect a conflict there when they merge.
- **Done: plan Appendix A edited at Boroon's word** ("Yes, edit the plan", 24 November 2026), with a 14.4 row:
  - `verify-in-test`'s verifier step waits with `|| true`, and `parse_verdict.py` gets `--plan` (slice C's finding 17);
  - `danger`'s review step waits with `|| true`, the combine gets `--head-sha`, and the policy step gets the gate's flags, `BASE_REF` and comment (B2).
  - The edited YAML parses with PyYAML. `CLAUDE.md`'s plan row and line map are updated.
- **Done: slice C's plan edits too, at Boroon's word** ("Yes, edit slice C's lines too", 24 November 2026):
  - Appendix A: the spec check step in `locks`; the checker step's flags and comment; the SARIF upload's `checkout_path`; the project settings step, the `if:` on the Copilot Studio and held-out steps, and `verdict_gate.py --settings`.
  - 5.7: the `locks` and `verify-in-test` rows of the job table, and the trusted-script list.
  - A 14.4 row for slice C's decisions: `run_workflow.py` waits for DG7 as ADO 3027, the spec check moved in ahead of DG8, and the optional suites by `gate.json`.
  - Compared step by step with the gate (pins, org names and comments ignored): `locks`, `verify-in-test` and `danger` now match. One difference was left: Appendix A still installed Copilot CLI with `npm install --global`.
- **Done: Appendix A's Copilot CLI install, at Boroon's word** ("Yes, edit it", 24 November 2026). `verify-in-test` and a new `danger` step install it from the gate repo's lockfile with `npm ci --ignore-scripts`, as the gate does since ADO 2509 (gate PR 16; plan 5.2 and spike 0.14's 14.4 row already said so). Compared again, all six jobs match `factory-gates` step by step apart from comments, pins and the `setup-node` cache flag. `CLAUDE.md`'s Appendix A row says so.
- **Before the Stage 1 exit test (2539):** finding 19, a token that can read team membership in `danger`. Without one, no human approval counts and no PR can pass `danger`.
- **For spike 0.6 and plan 9.3:** finding 18, the review model.
- `CLAUDE.md`'s `factory-gates` row is not edited (it is several sessions behind; its plan row and line map are). When it is: `release` is at `0db69f6`, with 636 tests and 7 pending scripts, and 2538's slices A, B and C are all merged (gate PRs 21 to 25).
- The scratch review repo and its raw log stay in the session scratchpad. Nothing was kept outside it.

Next steps:
1. Done: Boroon merged gate PR 25, and 2538 is Done.
2. Wed 25 Nov: spike 0.10 (2459), "export both".
3. Finding 19 before the exit test on Fri 27 Nov.

## Session 42, 2026-11-23 to 24, branch `claude/session-42-2538-c`

ADO 2538, slice C: the scripts for `verify-in-test`'s results and the spec job. On the laptop (desktop app), three days before its Thu 26 Nov date. Planning branch in its own worktree (`.claude/worktrees/session-42-2538-c`, from `main` at `3bce4e9`); gate branch `verify-in-test` in a worktree of the gate clone inside it, first off `release` at `973a421`, then rebased onto `70ce7f4` once Boroon merged slice B1 (gate PR 23) during the session. Session renamed "36. Stage 1 - Build - Checker, verdicts and spec check", at Boroon's word, after "35. Stage 1 - Build - Merge Danger rules" (Session 41). Session 41's entry came in with pull request 53, merged into this branch before its pull request; Sessions 38 and 40's are still on their own branches, so when they merge the order is 42, 41, 40, 39, 38.

Decisions (Boroon, 23 November 2026, each my recommendation):
- **`run_workflow.py` waits for DG7**, which writes the scenario format (`scenario.schema.json`, Tue 24 to Wed 25 Nov under the plan to finish Stage 1 this week). It moves out of 2538 to its own story, **ADO 3027**, Stage 1, **Ready to build, Wed 25 to Thu 26 Nov** (Boroon, 24 November 2026: planned, not proposed), after 2538 and DG7 and before DG9 and the exit test, both Fri 27 Nov. Its output (`scenarios.json`) is already fixed by `verdict_gate.py`.
- **`spec/check_spec.py` moves into `factory-gates` now**, byte for byte with its 98 tests and fixtures, ahead of the DG8 move, so the spec job can be tested end to end. `staging/factory-gates/` is deleted here; DG8 moves only `playwright/` (DG7). Until DG8 nothing checks that the extension's copy in `staging/factory-manifestos/` matches the gate's: change both together (staging README and DG8's step 3 say so).
- **The solution checker run twice from the laptop**, under his existing `pac` sign-in (an internal dev environment's profile), Australia geo, nothing saved to the environment: once on the gate's `FactorySpike` test zip (no results), once on a scratch copy with one JavaScript web resource holding known bad calls. Both reports hold only public documentation links; both are now gate fixtures. Scratch copies stayed in the session scratchpad.

Done (gate branch `verify-in-test`, commit `bdf1554`, pushed to GHE; **no gate PR opened**):
- **`lcp/checker_gate.py`**: reads `pac solution check`'s report, fails on High or Critical, and on Accessibility from Medium (B.3; 5.9), on an analysis that did not run, an unknown severity, or anything but one report with one run. Writes the SARIF with artifact paths as repo paths (`src/...`) and `checker-summary.json` with counts; Medium findings floor Merge Danger at 3 through slice B1's `merge_danger_floor.py`, which reads `counts.Medium` (a new test runs the floor on the real summary). Never prints a message or snippet.
- **`lcp/parse_verdict.py`**: each verifier session's final answer from its Copilot CLI log; strictest wins, PASS, NEEDS_WORK, RESTART, NO_VERDICT. NO_VERDICT for a broken answer, a finding without evidence (B.3), a PASS with findings, a session that did not finish, exited non-zero or stopped early, or a planned focus with no log. Exits 0; it never fails the job.
- **`lcp/verdict_gate.py`**: the job's last step. Requires `checker-summary.json`, `scenarios.json`, `conversations.json`, `holdout-summary.json` and `verdict.json`, all `schema_version` 1, clean and PASS. Defines the suite shape for its three unwritten writers. Prints counts and failed IDs only (rule 4).
- **`lcp/check_specs.py`**, a new step in `locks` (not a new job, so the six jobs and the pinned `lcp-gate` check stay): the trusted spec check on every spec folder the PR changes, and the vendored copy's SHA-256 on every PR that holds `.specify/`.
- `lcp-gate.yml`: the checker step's flags, `checkout_path: pr` on the SARIF upload, `--plan` on `parse_verdict.py`, the verifier wait with `|| true`, the spec step. `pending-scripts.txt` down to 9. README: the file table, a slice C section with the choices made, and findings 15 to 17.
- **198 new tests, 553 in all, 4 skipped by design (the spec check's class that compares copies, not beside it here), passing**; `manifest.py verify`, the hash check and `make_rulesets.py check` clean; the new scripts also pass on Python 3.9. Proved by breaking a copy 30 ways; one survived the first run (rename detection hid a checklist moved out of its spec), so a test was added.
- Here: `staging/factory-gates/` deleted; `staging/README.md`, DG8's step 3 in `docs/plans/stage-1-day-gate-plan.md` and `CLAUDE.md`'s staging row say where the spec check went.
- Sent slice B's running session the shapes of `checker-summary.json`, `verdict.json` and the suite files; its B1 already read `counts.Medium` as agreed.

Found (gate README findings 15 to 17):
- **15. `pac solution check` exits 0 whatever it finds** (two Critical results, exit 0). Severity is each result's `properties.severity`; only Critical results carried SARIF's `level: error`. Accessibility is a rule category (11 rules, all Medium).
- **16. In autopilot, a verifier's answer is the `session.task_complete` summary;** the message that calls `task_complete` is empty (real Copilot CLI 1.0.113 log from spike 0.14 part 4, found in an old scratchpad and cut down as a fixture). A parser of the last message would give every PR no verdict.
- **17. The plan's verifier step could end before the verdict is written:** under `set -euo pipefail`, `wait "$pid"` on a failed session ends the step. Fixed in the gate with `|| true`. `danger`'s review step has the same line, for slice B2.

Choices made without asking (gate README, slice C section; say if any is wrong): NO_VERDICT is the strictest verdict; the first line must be exactly the word (`**PASS**` is NO_VERDICT); a verifier's evidence paths are not yet checked to exist (where `lcp-verify` saves them is stage 2's); every evidence file is required, and a case that is neither pass nor fail is listed as failed; only specs the PR changes are checked, and a spec change in a repo with no `.specify/` fails.

ADO: 2538 stays **Building**; its body holds this session's result and time. New story **3027** for `run_workflow.py` (parent 2536; after 2538; before 2546 and 2539), **Ready to build, Wed 25 to Thu 26 Nov** (dates corrected the same session, at Boroon's word, from an older schedule).

Time and tokens (in 2538's body; session `e5d1f0dc`, measured before the last commit; `--latest` finds no transcript from a worktree, so run with `--root` set to the main folder's project and `--session`): active time 1 h 02 min (gaps over 10 minutes not counted), from 23 Nov 22:48 to 24 Nov 00:11 (UTC+11). Tokens: 142,536 output; 40,340,535 processed in all, of which 39,793,937 were cache reads. From 1 local transcript.

Files changed: here, `staging/factory-gates/` (deleted), `staging/README.md`, `docs/plans/stage-1-day-gate-plan.md`, `CLAUDE.md`, `docs/progress.md`. In `GetAI-IP/factory-gates` (branch `verify-in-test`): `lcp/checker_gate.py`, `lcp/parse_verdict.py`, `lcp/verdict_gate.py`, `lcp/check_specs.py`, `spec/check_spec.py` (all new), five new test files and `test_check_spec.py`, `tests/fixtures/checker/`, `tests/fixtures/verifier/`, `tests/fixtures/specs/`, `.github/workflows/lcp-gate.yml`, `tests/test_workflow.py`, `tests/test_merge_danger_floor.py` (one test), `pending-scripts.txt`, `scripts.sha256`, `README.md`.

Open items:
- **Done: gate PR 24 (slice C) merged by Boroon on 24 November 2026.** `release` is at `3a4db23`, with the same tree as the tested `57c53ec`. Checked on `release`: 563 tests OK (4 skipped by design); `manifest.py verify`, the hash check and `make_rulesets.py check` clean; 9 scripts left on `pending-scripts.txt` (B2's two, `run_workflow.py` for 3027, the six left out). Slice C is done; 2538 waits only on B2. The gate worktree is removed. Recorded in a comment on ADO 2538. Before the merge: the gate PR was opened, at Boroon's word (24 November 2026): https://getai.ghe.com/GetAI-IP/factory-gates/pull/24, head `57c53ec` (`bdf1554` plus the side session's two commits, at Boroon's word: `68c9830`, README only, the new dates for `run_workflow.py`; `57c53ec`, the optional suites), on `release` at `70ce7f4`, mergeable; 563 tests and every check pass there (checked in this session). **`self-test` is green on it** (Python 3.11, run 40577911); `lcp-gate`'s `map lane` is red, as expected on this repo's own PRs (gate README, step 10). For Boroon to merge once `self-test` is green on Python 3.11; if `release` moves first, rebase and make the manifest again. Recorded in a comment on ADO 2538.
- **Plan edits for Boroon** (none made): Appendix A's checker step flags, the SARIF upload's `checkout_path`, `--plan` on `parse_verdict.py`, the verifier wait's `|| true` (finding 17), and the spec step in `locks`; 5.7's job table (`locks` now runs the spec check); a 14.4 row for the three decisions above.
- **Done: optional suites (Boroon, 24 November 2026, option 1, over empty results).** Each project declares `holdout` and `agents` in `projects/<project>/gate.json` in the gate repo; `lcp/project_settings.py` gates the held-out and Copilot Studio steps; `verdict_gate.py --settings` requires a suite the project has and notes a skipped one. Gate commit `57c53ec`, 563 tests. **For 2539:** add Northwind's `gate.json` (both false) by a reviewed gate PR.
- `danger`'s review step has the same `wait "$pid"` (finding 17): slice B2.

Pull request: https://github.com/boroonmahanta/overnight-ai-factory/pull/54, this branch into `main`, opened at Boroon's word on 24 November 2026, after `main` (pull request 53, Session 41) was merged in with the log conflict resolved. For Boroon to merge.

Next steps:
1. Done: gate PR 24 merged (24 November 2026).
2. B2 (`merge_danger_combine.py`, `merge_policy.py`), after one real Copilot review output.
3. Wed 25 Nov: spike 0.10 (2459), "export both".

## Session 41, 2026-11-23, branch `claude/session-41-2538-b-floors`

ADO 2538, slice B: Boroon's two decisions, then slice B1 as **gate PR 23** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/23, branch `merge-danger-floor`, commit `8dac7a0`; `self-test` green on Python 3.11, run 40571776; `lcp-gate` red at `map lane`, as on every gate PR). **Merged by Boroon on 23 November 2026**, so `release` is at `70ce7f4`, with the same tree as the tested commit.
- Checked on `release`: 355 tests OK; `manifest.py verify`, the hash check and `make_rulesets.py check` are clean; 12 scripts left on `pending-scripts.txt`.
- Slice B1 is done. Task 2517 is Closed.
- The gate worktree and its local branch are removed. The remote branch was deleted on merge.
- Where it ran: on the laptop (desktop app), a day before B's Wed 25 Nov date, in its own worktree (`.claude/worktrees/session-41-2538-b`, from `main` at `3bce4e9`), because other sessions share the folder.
- The gate work: a worktree of the gate clone at `factory-gates/` inside it, off `release` at `973a421`. The shared gate clone was not switched.
- Session renamed "35. Stage 1 - Build - Merge Danger rules", at Boroon's word, after "34. Stage 1 - Build - Export plan and lints" (Session 40).
- Sessions 38 and 40's log entries are on their own unmerged branches, so this entry sits above Session 39's here.
- This record is **pull request 53** (https://github.com/boroonmahanta/overnight-ai-factory/pull/53), branch `claude/session-41-2538-b-floors`, into `main`, opened at Boroon's word on 23 November 2026. Boroon merges.

Read for it:
- Sessions 38 and 40's entries (their branches).
- The gate README's rule table and finding 14.
- `plan_from_export.py`, `lint_logic_apps.py` and `lcp-gate.yml` on `release`.
- Plan 5.10 and Appendix B.
- The low-code coding standards on GHE (`factory-manifestos`, `practices/lcp/coding-standards.md`), which the plan's default rule says to use where the plan is silent.

Decisions (Boroon, 23 November 2026, each my recommendation):
- **Merge Danger floors for the findings B.2 had no row for:** Session 40's proposals, with three changes.
  - Column security turned **off** goes to 8, like a widened privilege: more people see the data. Turned on stays 7.
  - A relationship or global choice **added** goes to 2, not 3. A new table brings about six system relationships (the real export pair shows six), so at 3 every new table would floor above B.2's "additive table: 2".
  - **New rule:** auditing turned on or off for a table or column, 7. Plan 5.3 turns auditing on everywhere. The export-diff plan reports it as `table_changed` or `column_changed` with `IsAuditEnabled` in `changed`, without the direction, so the floor matches either way.
  - The rest as Session 40 proposed: a narrower range 6, a removed global choice 6, a changed relationship 6, a removed relationship 8, connection references and environment variables removed or changed 5, everything else 3.
- **The flow check's unsafe text:** keep Session 40's seven kinds and add two, from the vault's `ALM-002` and `ALM-007`:
  - a flow's trigger URL, signed or not (`logic.azure.com/workflows/`, `*.environment.api.powerplatform.com`), because a hard-coded child-flow URL makes Test call Dev while every run passes;
  - a secret inside a string (`client_secret=`, `password=` or `pwd=`, an Azure Functions `code=`, `subscription-key=`).
  GUIDs (`TBL-006` allows fixed ones), mailbox addresses and other endpoints stay with the review agent (B.4) and the gardening scan (7.4).
- **ALM-007 in the flow check:** `lint_logic_apps.py` also runs the same list over environment variable default values, and fails any current-value file in the export.
- **Slice B split in two:** B1 now (offline: rules, floor, verifier count, flow-check additions); B2 next (`merge_danger_combine.py`, `merge_policy.py`), after one real Copilot review output has been captured, because they read Copilot CLI's JSON output and call GitHub's API.
- **What the floor cannot check yet** (shared use, which needs the inventory; scenario coverage, which needs `trace_criteria.py`): scored as seen, listed under `unchecked` in the floor's output, and the merge policy never auto-merges while that list is not empty. Not "fail closed at 3".

Done:
- **Plan B.2 edited at Boroon's word:**
  - a row for every export-diff finding, ordered by floor;
  - a paragraph saying how rules map to rows and why the rows were added;
  - a 14.4 row recording both decisions and the defaults check.
  Plan 5.7 and Appendix A still say "unsafe substrings"; the 14.4 row is the definition.
- **Gate PR 23 (slice B1):**
  - `lcp/danger-rules.yml` (task 2517): B.1's path rows (`deploy` and `protected` equal `check_protected_paths.py`'s list), B.2's rows for every plan rule, B.3's gate rules, and the `unchecked` list.
  - `lcp/merge_danger_floor.py`: `--pre` in `verify-in-test`, full in `danger`. A plan rule no row names stops the run.
  - `lcp/verifier_plan.py`: B.6.
  - `lcp/simple_yaml.py`: the gate scripts stay standard library only (D3), so this is a strict reader of the gate's own YAML, tested against PyYAML.
  - `lint_logic_apps.py`: the nine kinds, defaults and value files.
  - `lcp-gate.yml`: `verify-in-test` checks the PR out with `fetch-depth: 0`, because the pre-floor diffs `BASE...HEAD`.
  - 59 new tests, 355 in all.
  - Proved by breaking a copy 39 ways. The one break that survived the first run was a real gap: a literal secret starting with `@` (`Password=@bcd1234;`) slipped through, so the `@` exclusion went and a test was added.
  - `pending-scripts.txt` is down to 12. `scripts.sha256` was made last, adding the four new files and changing `lint_logic_apps.py`. `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` are clean.
  - The README has a section "The Merge Danger floor (ADO 2538, slice B1)", and finding 14 is settled.
- `CLAUDE.md`: the plan row and the line-number map (it was a session behind).

Made by this session without asking (say if any is wrong; gate README, "The Merge Danger floor"):
- Row ids: `docs`, `dev-tests`, `generator`, `agents`, `code-apps`, `reference-data`, `plugins-dependencies`, `deploy`, `secrets`, `protected`, `unlisted-path`; plan rows `export-additive`, `export-flow-logic`, `export-other`, `connection-environment`, `column-one-way`, `choice-removed`, `relationship-changed`, `security`, `auditing`, `privilege-widened`, `column-security-off`, `role-removed`, `column-dropped`, `table-dropped`. Plan B.6's `trust.yml` example names `export-additive`, `export-flow-logic`, `localisation` and `docs`; the others are new.
- A changed path no row names floors at 3 (`unlisted-path`, never auto-merges). No row yet for localisation files (1), interface changes needing `sync_agent_tools.py` (4) or money logic (8, per project): no path shows them, so they fall to 3. The interface change is the one case where 3 is lower than B.1's floor.
- The paths for B.1's "dependency or tool version bumps" (5): `package.json`, `package-lock.json`, `requirements*.txt`, `global.json`, `*.csproj`, `Directory.Packages.props` at any depth, and `.config/dotnet-tools.json`. For "credentials, secrets" (10): `.env`, `.env.*`, `*.pfx`, `*.p12`, `*.pem`, `*.key` at any depth.
- Specs (`specs/*/spec.md`, `specs/*/checklists/**`) floor at 10 with the other protected paths, though B.1's floor-10 row does not list them.
- "More than 25 changed source files" counts every changed path outside the `docs` row. The real pair (a table swapped) is 29 files, so a story that adds a table and more can reach it.
- The checker's Medium count comes from `checker-summary.json` (`counts.Medium`), which `checker_gate.py` must write in slice C. The full run fails without it.
- Each path and each finding takes only its highest row, so a change class (B2) reads the rows that set each part of the floor.

ADO:
- 2538 stays in **Building**. Its body holds the decisions, gate PR 23 and the time line. Comments record the Appendix A edit and the merge.
- Task 2517 is **Closed** (23 November 2026, after the merge). Its body maps each plan rule to its B.2 floor.

Time and tokens (session `166167c4`, measured before the last commit). `--latest` finds no transcript from a worktree, so run with `--root` set to the main folder's project and `--session`. Active time 1 h 07 min (gaps over 10 minutes not counted), from 23 Nov 22:33 to 24 Nov 00:00 (UTC+11). Tokens: 186,314 output; 42,615,920 processed in all, of which 41,983,360 were cache reads. From 1 local transcript.

Files changed:
- Here: `docs/sources/plan-v3.1.md` (B.2, a 14.4 row, Appendix A's `verify-in-test` checkout), `CLAUDE.md`, `docs/progress.md`.
- In `GetAI-IP/factory-gates` (gate PR 23):
  - `lcp/danger-rules.yml`, `lcp/merge_danger_floor.py`, `lcp/simple_yaml.py`, `lcp/verifier_plan.py` (new);
  - `lcp/lint_logic_apps.py`, `.github/workflows/lcp-gate.yml`;
  - four test files (new) and two changed;
  - `README.md`, `pending-scripts.txt`, `scripts.sha256`.

Open items:
- **Done: gate PR 23 merged by Boroon** (23 November 2026, `70ce7f4`). Kept here one session for the record.
- **Slice C's gate worktree** (`.claude/worktrees/session-42-2538-c/factory-gates`, branch `verify-in-test`) is still on `973a421`. It must rebase on `70ce7f4` and make the manifest last, as agreed.
- **Done: plan Appendix A's `verify-in-test` now checks the PR out with `fetch-depth: 0`**, as gate PR 23 has it (Boroon, "Yes, edit the plan", 23 November 2026); the Session 41 row in 14.4 says so. Kept here one session for the record.
- **Not tested against a real export:** the two new kinds of unsafe text and an environment variable value file. No fixture holds one.
- **A site map entry added comes out as `other_changed` (3),** not B.1's small-addition 2: the export-diff plan does not read site maps. Conservative; teach the plan site maps if a story class needs them at L2.
- **Agreed with the slice C session (ADO 2538 C, gate branch `verify-in-test`), 23 November 2026:**
  - `checker_gate.py` writes `evidence/checker-summary.json` whether or not it fails. Its fields:
    - `schema_version` 1, `fail_on` `High`, and `category_fail_on`, which holds `Accessibility: Medium`;
    - `counts` by severity: `Critical`, `High`, `Medium`, `Low`, `Informational`;
    - `failing`, a list of rule, severity, category, file and line;
    - `failed`, and `notes`.
  - The severity is read from Microsoft's real SARIF, where each result has `properties.severity`. The category is the rule's `properties.primaryCategory`. `pac solution check` exits 0 even with Critical results.
  - B1's floor reads only `counts.Medium`. It does not check `schema_version`.
  - C's gate PR follows gate PR 23's merge, rebased on `release`, with the manifest made last.
- **For B2:** `merge_policy.py` reads the floor's `rows`, `auto_merge`, `protected_paths` and `unchecked`, and never auto-merges while `unchecked` is not empty. It reads `trust.yml` through `simple_yaml.py`, and team names from `rulesets/org.json`. Before writing B2, capture one real `copilot -p --output-format json` review output to read its shape.
  - It also reads C's `evidence/verdict.json` (from `parse_verdict.py`, written whatever the verdict). Its fields:
    - `schema_version` 1, and `verdict`: `PASS`, `NEEDS_WORK`, `RESTART` or `NO_VERDICT`. The strictest wins, in that order. `NO_VERDICT` is B.3's "No verdict: a human looks".
    - `sessions`, each with focus, verdict, reasons, `failed_criteria` and unknowns;
    - `missing_focuses`.
  - Anything but `PASS` is not mergeable, and `NO_VERDICT` never auto-merges.
  - C's suite summaries (`scenarios.json`, `holdout-summary.json`, `conversations.json`, each `{schema_version, suite, total, passed, failed: [case ids]}`) are for `verdict_gate.py`, not the floor.
- `CLAUDE.md`'s `factory-gates` row and `docs/plans/schedule.md` are not edited, because Sessions 34, 37, 38 and 40's unmerged branches touch them. When they are edited: `release` is at `70ce7f4` with 355 tests and 12 pending scripts, and slices A and B1 are done.
- Sessions 38 and 40's branches are not merged here. When they are, the log order is 41, 40, 39, 38.

Next steps:
1. Done: Boroon merged gate PR 23.
2. Slice B2 (`merge_danger_combine.py`, `merge_policy.py`), after one real Copilot review output.
3. Slice C (Thu 26 Nov): `checker_gate.py` (writing `checker-summary.json`), `run_workflow.py`, `parse_verdict.py`, `verdict_gate.py`, and the `check_spec.py` job.

## Session 39, 2026-11-23, branch `claude/session-39-3026-teams-story`

A laptop session, in its own worktree (`.claude/worktrees/session-39-3026`, from `main` at `1f848be`), because Sessions 34 to 38 share the folder. Boroon pasted a side chat about the three CODEOWNERS teams and asked for a story; then he chose new names, and the session did the rename. The `factory-gates` work ran in its own worktree too (`.claude/worktrees/gate-3026-team-names`), apart from Session 38's `static-file-checks`.

**Pull request 50** (https://github.com/boroonmahanta/overnight-ai-factory/pull/50), opened at Boroon's word on 23 November 2026, into `main`. **Merged by Boroon on 23 November 2026 (`b6c5b76`)**, and gate PR 20 the same evening (`release` at `3c23ca5`). Then Boroon made the teams in the portal, and **3026 moved to Done** at his word. These record commits are on branch `claude/session-39-3026-done`, in **pull request 51** (https://github.com/boroonmahanta/overnight-ai-factory/pull/51), opened at Boroon's word the same day. Boroon merges.

**Checked after the merges** (`gh api`, 23 November 2026): `release` at `3c23ca5` passes `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check`, with 172 tests OK. The teams: `ai-factory-platform-admins` (ID 71036), `ai-factory-acceptance-owners` (71041) and `ai-factory-merge-reviewers` (71046) in `AI-Business-Solutions`, and `ai-factory-platform-admins` (71051) in `GetAI-IP`, the only team on `factory-gates`, with Write (`push`). All Visible (`closed`), no parent; the only member is `boroon-mahanta` (a User), no machine account. No identity provider group is linked: members are kept by hand for now, Entra groups later when more people join (Boroon's comment on 3026).

Done:
- **ADO 3026, "Name and create the three CODEOWNERS teams on getai.ghe.com"** (User Story, now Building, under Feature 2519, a predecessor of 2521, related to 2520; Tue 24 to Wed 25 Nov; tags `factory-build`, `stage-1`). Work size S, written in the body (this project has no `Custom.WorkSize` field). Its body holds the steps, the names table and what is left.
- **Checked against `factory-gates`** (`release` at `65031e4`): the old names were `platform-team`, `acceptance-owners` and `factory-reviewers`, written `@AI-Business-Solutions/<team>` in `templates/CODEOWNERS`. **None of the teams exists yet**, by any name, in `AI-Business-Solutions` or `GetAI-IP` (listed with `gh api`, 23 November 2026).
- **Gate PR 20** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/20, branch `ai-factory-team-names`, open): the rename in `templates/CODEOWNERS`, `rulesets/org.json`, `lcp/make_rulesets.py` (`BYPASS_TEAMS`), `lcp/apply_rulesets.py`, `README.md` (step 1 of "Applying to the real organisation" now says to make each team Visible and keep machine accounts out), one comment in `lcp-gate.yml`, the two ruleset tests, and `scripts.sha256` (four lines). The generated rulesets do not change: they hold team IDs, not names. 172 tests OK; `manifest.py verify`, `sha256sum --check --strict` and `make_rulesets.py check` clean; `self-test` green (run 40546006). `lcp-gate`'s `map lane` fails, as on every gate PR (19 and 16 too), because `factory-gates` is not a project repo.
- **The plan and documents:** every `@acceptance-owners` and `@factory-reviewers` in plan 2, 5.1, 5.3, 5.7, 5.8, 5.10, 6.2 and Appendix A; 5.7's bypass line now names `@ai-factory-platform-admins`; a 14.4 row. Also `docs/plans/stage-1-day-gate-plan.md`, `docs/plans/stage-1-gate-build-plan.md`, the staged Spec Kit spec template and checklist, the spec check's two fixture checklists (98 tests OK), `CLAUDE.md` (the plan row and the `factory-gates` row) and the schedule.

Decisions:
- **The team names (Boroon, 23 November 2026):** `ai-factory-platform-admins` (was `platform-team`), `ai-factory-acceptance-owners` (was `acceptance-owners`), `ai-factory-merge-reviewers` (was `factory-reviewers`). One set per org, by role, shared by low-code and pro-code. In the plan as a 14.4 row.

Found (in 3026's body):
- No team IDs need copying by hand: `apply_rulesets.py resolve` reads them from the org into `rulesets/org.json` (2521).
- `factory-gates` has no CODEOWNERS file of its own, so its `release` ruleset alone cannot require the platform admins' approval (README move step 6). For 2520.

Not changed, on purpose: the one-pager (`docs/one-pager/GET-AI-Factory-Ways-of-Working.html` still says `@factory-reviewers`; it is already out of date and is also a published artifact), `docs/plans/factory-gates-move-step-8.patch` (a record), the log above, and "the platform team" where the plan means people rather than the team (5.4, 15.1).

Files changed: `docs/sources/plan-v3.1.md`, `docs/plans/stage-1-day-gate-plan.md`, `docs/plans/stage-1-gate-build-plan.md`, `docs/plans/schedule.md`, `staging/factory-manifestos/spec-kit/presets/getai/templates/spec-template.md`, `staging/factory-manifestos/spec-kit/presets/getai/templates/getai-checklist.md`, `staging/factory-gates/tests/fixtures/specs/project/specs/90101-order-follow-up/checklists/getai.md`, `staging/factory-gates/tests/fixtures/specs/project/specs/90102-open-orders-export/checklists/getai.md`, `CLAUDE.md`, `docs/progress.md`. In `factory-gates`: the nine files of gate PR 20.

Open items:
- **Gate PR 20 and 2538's gate work both change hashed files.** Whichever merges second must make `scripts.sha256` again first.
- Session 37's schedule redraft (branch `claude/session-37-stage-1-this-week`, not merged when this was written) rewrites the same table; whichever merges second needs the 3026 row carried over. Its dates already put the teams on Wed 25 Nov.

Time and tokens (in 3026's body; session `c61993de`, measured before the last commit, the side chat not counted): active time 0 h 39 min (gaps over 10 minutes not counted), from 23 Nov 20:32 to 23 Nov 21:26 (UTC+11). Tokens: 91,625 output; 29,359,346 processed in all, of which 28,998,315 were cache reads. From 1 local transcript.

Next steps:
1. Done: both merged, the teams made, 3026 Done (23 November 2026).
2. **Done the same evening: second approvers named** (Boroon, 23 November 2026). Each of the four teams now has a second person besides Boroon, all User accounts: in `AI-Business-Solutions` one person in the platform admins and acceptance owners, and a different person in the merge reviewers, so the scenario writer is not the reviewer; in `GetAI-IP` a third person in the platform admins. Names and accounts are in ADO 2520 and 2521 only (public repo). For 2520, all of whose stopgaps are in `GetAI-IP`: give `ai-factory-platform-admins` there Write on `factory-manifestos` first (no team is on it, and an approval without Write does not count); the `GetAI-IP` approver uses an admin account for now, and a normal one is better (least privilege); the `AI-Business-Solutions` approver is not in `GetAI-IP`, so cannot approve gate PRs unless added. **Later the same evening:** Boroon added that approver to `GetAI-IP` and its platform admins, so that team has two people besides him; and the team got Write on `factory-manifestos` (his portal change did not save, so the session added it with `gh api`, PUT on the team's repo access, `permission=push`, at his word). Checked: both second people have Write on `factory-gates` and `factory-manifestos`. ADO 2520's comments hold the names. This record is **pull request 52** (https://github.com/boroonmahanta/overnight-ai-factory/pull/52), branch `claude/session-39-approver-access`, opened at Boroon's word the same day. Boroon merges.
3. 2538's gate PR (`static-file-checks`) must make `scripts.sha256` again on top of `3c23ca5` before it merges.

## Session 36, 2026-11-23, branch `claude/nifty-thompson-22d47f`

ADO 2544, part 2: day-gate session DG5, the spec check script. On the laptop (desktop app), in its own worktree, started by Session 35 as a side session. The branch starts from Session 35's branch tip `5fa167c`. Pull request 47 (Session 35, DG4) was merged by Boroon on 23 November 2026 (`7476871`) during this session, and `main`'s content equals `5fa167c`, so this branch's pull request targets `main` and shows only Session 36's commits.

**Pull request 48** (https://github.com/boroonmahanta/overnight-ai-factory/pull/48), opened at Boroon's word on 23 November 2026, into `main`; mergeable, no CI checks on this repo. **Merged by Boroon on 23 November 2026 (`f612980`)**, at 09:16 UTC. At his word the same day, **ADO 2544 moved to Done**, and its Finish Date moved from Wed 25 Nov to today, Mon 23 Nov (in ADO and `docs/plans/schedule.md`). These record commits are in **pull request 49** (https://github.com/boroonmahanta/overnight-ai-factory/pull/49), opened at his word the same day. Boroon merges.

Done:
- **`staging/factory-gates/spec/check_spec.py --spec <spec.md> --profile lcp|pcp [--repo <root>]`.** Standard library only, run with `python3 -I`, exit 0 or 1 (usage errors are 1 too). It reads the DG4 spec format and fails on, by rule name: `header` (the YAML header and its lane, profile, ambition and work size), `ado-id` (digits, and the folder `<ado_id>-<name>`), `design` (the design and prototype fields), `marker`, `checklist`, `nfr`, `assumption`, `criteria` (the `AC-<n>` IDs and the Acceptance Scenario Map), `lcp-field` (all 17 Low-Code Fields), `scenario` (with `--repo`, each map ID resolves to a file under `tests/`) and `spec` (no such file). It warns on `design-leak` (plan 6.6). Each line of output says `FAIL [rule] path:line: message`, with what to do.
- **98 tests** in `staging/factory-gates/tests/test_check_spec.py`, all passing with `python3 -B -m unittest discover -s staging/factory-gates/tests`, on Python 3.9, 3.14 and 3.15. Fixtures in `staging/factory-gates/tests/fixtures/specs/`: `project/`, a project repo with a good low-code spec (90101, order follow-up date) and a good pro-code spec (90102, open orders export), ticked checklists and stand-in scenario files; and `exit-clause/`, the two stage 1 exit fixtures (`open-marker.md`, `no-scenarios.md`), each the good spec with one change, both failing. Every other failing case is made in the test from the good spec by one change, and the test checks it fails on that rule alone. The design-leak cases warn and pass.
- **The extension's copy** at `staging/factory-manifestos/spec-kit/extensions/getai-spec-check/scripts/check_spec.py`, byte-identical; a test compares the hashes, and another checks the script's list of Low-Code Fields against the template's headings.
- **Tested on real Spec Kit 1.4.3** (PyPI `specify-cli==1.4.3` in a scratch venv): `specify extension add --dev` copies the script to `.specify/extensions/getai-spec-check/scripts/`, the hook's path, byte for byte; the hook's own steps passed the good spec; a spec and checklists composed by Spec Kit's resolver from the bare templates failed on every rule.
- **The 2538 item (factory-gates follow-ups, item 8) still holds;** it now also gives the vendored path, the command, and that the job takes `--profile` from the project manifest, not the spec.
- Docs: the spec-kit README (a section on the spec check), `staging/README.md`, the day-gate plan (DG5 done, and the exit-clause row), the schedule, `CLAUDE.md`'s staging row.

Made by this session without asking (say if any is wrong):
- Checks beyond the brief, each a small step from a rule in it or the plan: `profile: lcp` needs `lane: B` (plan 6.3); lane A needs at least 20 criteria (plan 6.6, "the criteria floor" in 6.1); a scenario with no `AC-<n>`, an ID defined twice, and a map row for an undefined ID fail; `checklists/getai.md` (and `lcp.md` for lcp) must exist and hold items, so deleting a checklist does not pass; a design document with no exact version, or a Teams link as the document, fails (plan 6.4).
- `ambition` takes `low` or `high` only, the two values the plan and V2.1 name. Say if `medium` should pass.
- Markers fail even inside HTML comments; everything else ignores comments, so the templates' guidance comments can stay in a spec.
- The Low-Code Fields and the map are exempt from the design-leak warning, like Constraints, because plan 6.3 asks for schema names there.
- A scenario ID resolves to a file named the ID plus its extensions, or to a path under `tests/`. DG7 sets the scenario conventions and may change this.
- The script also runs on Python 3.9 (Apple's `python3`), through one `__future__` import; the extension still declares 3.10 or later.

Files changed: `staging/factory-gates/` (new: `spec/check_spec.py`, `tests/test_check_spec.py`, `tests/fixtures/specs/`, 17 files), `staging/factory-manifestos/spec-kit/extensions/getai-spec-check/scripts/check_spec.py` (new), `staging/factory-manifestos/spec-kit/README.md`, `staging/README.md`, `docs/plans/stage-1-day-gate-plan.md`, `docs/plans/schedule.md`, `CLAUDE.md`, `docs/progress.md`.

Open items:
- **Done: ADO 2544 is Done** (Boroon, 23 November 2026, after pull request 48 merged). Its body holds DG5's result and this session's time and tokens.
- **For DG8:** move `spec/`, `tests/test_check_spec.py` and `tests/fixtures/specs/` into `factory-gates`, regenerate `scripts.sha256` (delete `.DS_Store` first), and add a README row. After the move, the test class `StagedCopyTests` skips, because the extension and the template are in `factory-manifestos`; the gate's CI job (2538) then checks the vendored copy's hash. The extension's copy moves with `factory-manifestos`; keep it byte-identical by copying from `factory-gates` in the same pair of pull requests.
- Not tested: the hook run by an agent inside `/speckit-implement` (the steps were run by hand), and the CI job (2538).

Time and tokens (in 2544's body; session `4d3d63dd`, measured before the last commit): active time 0 h 30 min (gaps over 10 minutes not counted), from 23 Nov 19:39 to 23 Nov 20:09 (UTC+11). Tokens: 121,041 output; 11,203,298 processed in all, of which 10,769,001 were cache reads. From 1 local transcript.

Next steps:
1. Done: pull request 48 merged and 2544 Done (Boroon, 23 November 2026).
2. Tue 24 Nov: 2538, the remaining gate scripts, with the `check_spec.py` job (item 8 above).
3. Thu 26 Nov: 2548's first mining batch.

## Session 35, 2026-11-23, branch `claude/session-35-2544-spec-kit`

ADO 2544, part 1: day-gate session DG4, the Spec Kit pin and the two presets, on its start date. On the laptop (desktop app), in its own worktree, from `main` at pull request 46's merge (`0e2dab1`). Numbered 35 because Session 34 (2509) ran the same day. Session renamed "31. Stage 1 - Build - Pin Spec Kit and the presets", at Boroon's word.

**Pull request 47 merged by Boroon on 23 November 2026 (`7476871`)**, at 08:37 UTC; `main` then equalled this branch's tip `5fa167c`. Recorded by Session 36.

Done:
- **Read the Spec Kit release notes 1.3.0 to 1.4.3.** 1.3.3 (9 November) is the last 1.3; 1.4.0 to 1.4.3 (10 to 19 November) marked nothing as breaking. 1.4.3 adds `replace-section` for presets (#5462); 1.4.2 stamps each generated skill with its source and version (#5456). PyPI's `specify-cli` versions match the tags, published from each tag by Spec Kit's own `publish-pypi.yml` (no provenance attestations).
- **Pinned 1.4.3** (commit `980b3d0`), at Boroon's word. Installed in the scratchpad from the commit, read in full every template and command we override, the lean preset, and the preset, extension and bundle API docs.
- **Built `staging/factory-manifestos/spec-kit/`:** the `getai` preset (a YAML header with ADO ID, lane, profile, ambition, work size, SharePoint design identity and exact version, prototype; an Acceptance Scenario Map with `AC-<n>` IDs; Non-Functional Requirements; Constraints; the GET AI rules wrapped around `specify` and the grilling rules around `clarify`; the GET AI constitution; a reviewer-owned GET AI checklist), the `getai-lcp` preset (the 6.3 fields appended; the delivery vault's design and handoff sections in place of the plan template's source tree; low-code rules around `specify`; a low-code checklist), the `getai-spec-check` extension (the `before_implement` hook, `optional: false`; its command runs `check_spec.py`, which DG5 adds), the `getai-lcp` bundle, and a README with the pin, how to install, the test, the findings and the prototype guide. Each override is one composition step over Spec Kit's own file; no Spec Kit file is copied.
- **DG4's test passes:** in a fresh scratch project, `specify init --integration copilot`, then `specify preset add --dev` for both presets and `extension add` for the three extensions, gives a spec template with the header, every core section, the three GET AI sections and all 17 low-code fields; a plan template with the ten low-code sections; the specify and clarify skills headed by our rules; and the hook registered as mandatory. `specify bundle validate --offline` passes the bundle (warnings only for the three catalog parts).
- **Findings** (in the spec-kit README and DG4's entry in the day-gate plan): the lean preset is left out of the bundle, since its `implement` skips hooks and the checklist gate; a bundle cannot install presets or extensions from local folders, so DG8 makes a private `getai` catalog on GHE (a new DG8 step 5); Spec Kit's shell resolver needs PyYAML on the system `python3`; the three-marker cap is in the core `specify` command; `update-agent-context` is now an opt-in extension that `init` does not install; `init` no longer installs the `git` extension.
- `docs/component-register.md`: a Spec Kit row, the first kit row for A1.

Decisions (Boroon, 23 November 2026, asked in this session):
- **Every spec carries an ADO ID; no Spec Kit numbering** (asked mid-session: "don't fall back to Spec Kit's own numbering, force creation of an ADO ID if one doesn't exist"). The GET AI specify rules now take the ID from the input, else find the story in ADO, else create a User Story in the engagement's project once the owner agrees the project and title; with no ID they stop. The folder is always `specs/<ado-id>-<short-name>`. A new GET AI checklist item, CHK017, checks the ID matches across header, folder and day branch. Retested: the composed specify skill carries the rule.
- **Pin Spec Kit 1.4.3**, not the newest 1.3.x (D2 as written), with the small plan edit that needs. **The plan is edited:** 6.1 and 11.2 say 1.4.3; a 14.4 row "The Spec Kit pin". The plan grew by one line (2,797 to 2,798); `CLAUDE.md`'s line map, plan row, pin and staging row follow.

Made by this session without asking (say if any is wrong):
- The lean preset left out of the bundle (finding above).
- One field beyond plan 6.3's table, marked proposed: "Kind of change to a model-driven app" (plan 5.6), so the owner sees by day whether a story can run at night.
- In clarify, new terms and decision records are written to `glossary.md` and `docs/adr/` on the spec's day branch, so they reach `main` only through the reviewed spec pull request (rule 17).

Files changed: `staging/factory-manifestos/spec-kit/` (new, 16 files), `staging/factory-manifestos/README.md`, `docs/plans/stage-1-day-gate-plan.md`, `docs/plans/schedule.md`, `docs/component-register.md`, `docs/sources/plan-v3.1.md` (at Boroon's word), `CLAUDE.md`, `docs/progress.md`.

Open items:
- **DG5:** `staging/factory-gates/spec/check_spec.py`, its tests and fixtures, and the extension's byte-identical copy in `spec-kit/extensions/getai-spec-check/scripts/`. It reads the YAML header with the standard library (simple `key: "value"` lines), the `AC-<n>` IDs, the Acceptance Scenario Map, the NFR lines, the approval marks on Assumptions, the ADO ID (missing or not digits fails, and so does a spec folder that does not start with it), the Low-Code Fields (`Not applicable: <reason>` allowed, a bracketed placeholder fails) and the checklists.
- Not tested: running specify and clarify with an agent end to end. Worth one dry run on a made-up story before DG6 or 2539.
- The untracked `docs/plans/spike-0.17/engineer-how-to.md` in the main checkout is not this session's; left alone.

Time and tokens (in 2544's body; session `71b14df4`, measured before the last commit): active time 0 h 26 min (gaps over 10 minutes not counted), from 23 Nov 18:40 to 23 Nov 19:25 (UTC+11). Tokens: 72,014 output; 17,417,488 processed in all, of which 17,043,409 were cache reads. From 1 local transcript.

Next steps:
1. DG5 (2544 part 2), Tue 24 or Wed 25 Nov: the spec check script.
2. Tue 24 Nov: 2538, the remaining gate scripts (now with the `check_spec.py` job).
3. Thu 26 Nov: 2548's first mining batch, if exports have arrived.

## Session 33, 2026-11-23, branch `claude/ignite-recheck-df24ce`

The Ignite re-check (the schedule's checkpoint for Mon 23 Nov). Boroon asked, through the session "Ignite re-check for plan" that started this one: "do the Ignite re-check for our plan and tell me anything that influences the plan and has been announced as GA (not In Preview)". On the laptop (desktop app), in its own worktree. Four research agents read the sources in parallel (Power Platform ALM; the night tools and Copilot Studio; GitHub; Azure, licensing and ADO); then every GA row was re-read on its primary page here. One agent claim failed that check and was dropped (that the Copilot SDK's BYOK takes API keys only: its docs show Entra bearer tokens).

Done:
- **`docs/analysis/ignite-2026-recheck.md`**: a table of nine GA items that touch the plan, with wording, date, source, sections, risks and the proposed change; the GA items needing no change; the plan's named re-check items still in preview (no change); an unclear list; facts found along the way; what was looked for and not found.
- **The headline:** no rename (the naming rule stands); nothing GA for the night lane's tools (Dataverse MCP, FlowAgent, App Spec, `pac copilot`, pac solution, Copilot Studio evaluation); no pac release writes YAML; Git integration with GitHub still preview; Copilot data residency still US and EU only (risk 4 stands).
- **The GA items, most important first:** (1) Copilot Managed Runtime is GA and its environment routing is on in every tenant, unchangeable, making managed personal environments; (2) in Australia East, GPT-5.6 Sol is the only current frontier model as a Standard (regional) deployment, which answers half a 15.1 question; (3) the Copilot SDK is GA as Microsoft Copilot SDK 2.0 (Lane A: new package, runtime in process by default); (4) GitHub team customizations are GA and can load plugins into day sessions by default (rule 19); (5) the APAC Data Zone (not in-country); (6) Container Apps Sandboxes (spike 0.8); (7) the Microsoft Copilot harness name and the customer conversation harness; (8) new Copilot models (no pin change); (9) code apps GA since February.
- **Found along the way:** plan 1.4's Vibe and App Builder dates are wrong (editing ends 30 November, access ends 31 December 2026; 11 December belongs to Power Apps Ideas and Copilot formula generation); Purview logs production environments only, which answers a 15.1 question.
- **ADO 3024** (new, under Feature 2711 "Analysis and assessments"): the re-check as a story, Done, with the result and the time line. The checkpoint had no story before.
- `docs/plans/schedule.md`: the checkpoint marked done; a Changes entry.

Decisions (Boroon, 23 November 2026, asked in this session): **"Yes, edit the plan and then open a PR."** The plan is edited for every row of table 1 and the plan facts in section 4: 1.1 (no rename), 1.4 (the Vibe and App Builder dates split into 30 November, 11 December and 31 December), 4.1 (Microsoft Copilot SDK 2.0, pinned, a spawned runtime), 4.4, 5.6, 5.9 and 6.3 (the three Copilot Studio harnesses, new-harness evaluation still preview), 5.3 (Purview covers production only), 5.4 (personal environments from Copilot Managed Runtime routing; routing rules and app creation spaces set first), 5.6 (code apps GA), 8.3 point 7 (no team default plugins), 9.3 (the new Copilot models, no pin change), 9.4 (Australia East's models, SDK BYOK by Entra token [untested], an APAC Data Zone variant of T2), 11.1 (Container Apps Sandboxes in spike 0.8), risks 3, 9 and 27, 15.1 (three rows), 15.2, and a 14.4 row "The Ignite re-check". The plan grew by 9 lines (2,788 to 2,797). `CLAUDE.md` follows: the plan row, a row for the analysis, the line map, the naming note, the dates table, risk 4 and the open question.

Files changed: `docs/analysis/ignite-2026-recheck.md` (new), `docs/sources/plan-v3.1.md` (at Boroon's word), `CLAUDE.md`, `docs/plans/schedule.md`, `docs/progress.md`.

Open items:
- **Boroon:** two actions outside the plan: set the tenant's routing rules and app creation spaces before anyone builds a Copilot Managed Runtime app (5.4); check that no team on `getai.ghe.com` sets default Copilot plugins (8.3 point 7). **Done:** pull request 45, https://github.com/boroonmahanta/overnight-ai-factory/pull/45, the re-check and the plan edits, **merged by Boroon on 23 November 2026** (`f11cb39`). This note came by a later pull request, because its first commit reached the branch after that merge.
- **Not done today, though due:** A1's first pass and the first component register review (both on the Mon 23 Nov checkpoint).
- For spike 0.15 (Universe, 7 December): GitHub Enterprise now "includes GitHub Copilot usage rights at no extra cost" (Partner Center, 4 November); confirm on GitHub's own changelog and re-cost 9.1 and 10 if so.
- For 2509: Copilot CLI's latest stable is 1.0.114 (18 November); the docs now say `-p` exits non-zero on an empty final answer, with no changelog line, so test it on the pinned version.
- If wanted (A1): a `pac solution clone` on pac 2.16.1 in scratch, since Learn's pages still disagree on YAML.

Time and tokens (in 3024's body; session `d328a4d4` with its four research agents and the plan edits, measured before the last commit; the session that started this one is not included): active time 0 h 36 min (gaps over 10 minutes not counted), from 23 Nov 11:31 to 23 Nov 16:12 (UTC+11). Tokens: 244,167 output; 99,341,427 processed in all, of which 96,932,137 were cache reads. From 1 local transcript(s).

Next steps:
1. Boroon does the two actions above (pull request 45 is merged).
2. 2509, pin the Copilot CLI install in `verify-in-test` (due Mon 23 Nov).
3. A1's first pass and the component register review.
4. 2544 (Spec Kit pin and presets), no longer waiting on the re-check.

## Session 32, 2026-11-21, branch `claude/session-32-3019-exports-home`

ADO 3019: a restricted Factory home for session exports. On the laptop (desktop app), with the built-in browser under Boroon's sign-in and the Microsoft 365 connector (read only). Branch from `main` after pull requests 41 and 42 merged. Session renamed "28. Stage 1 - Build - Factory home for session exports", like the others.

Done:
- **Step 1 passes for the OneDrive stopgap.** "Request files" shows in the OneDrive command bar when `Factory session exports` is selected (looked at, not clicked; no link made). So the tenant allows "Anyone" links for OneDrive and the stopgap needs no admin change. The checkpoint (send the engineers the how-to and ask for exports) is unblocked.
- **Corrected a setting name in 3019.** OneDrive's switch is `OneDriveRequestFilesLinkEnabled`; `CoreRequestFilesLinkEnabled` is SharePoint's, which the channel needs (Microsoft, "Enable file requests in SharePoint or OneDrive").
- **Found in Microsoft's pages** (untested): "Private channels in Microsoft Teams" says a private channel's site inherits guest access from its parent Team's site and cannot be shared separately, while "Change the sharing settings for a site" shows an admin setting a channel site's sharing from the Channel sites column. So the admins try the channel's site alone first, and the Team's site too if needed. Microsoft's Entra guidance advises against "Anyone" links and says to set an expiry if they are used. New Teams sites default to guest sharing, not "Anyone".
- The exports folder is empty (web view, connector listing by ID, sync folder): Session 31 deleted its test file at Boroon's word.
- `docs/plans/spike-0.17/README.md`: a new section, "The Factory Team's home (ADO 3019)": what was checked, the steps for Boroon and the admins, and a draft message to the admins. No names (public repo).
- ADO 3019: body rewritten with the decision, the admins' names (ADO is private) and the steps; moved to **Building**.

Decisions (Boroon, 21 November 2026, asked in this session):
- The private channel keeps "Request files", **renewed quarterly**: the link expires after 90 days and Boroon makes and sends a new one each quarter. (Offered instead: one folder per engineer, or a Microsoft Forms upload; both avoid "Anyone" links.)
- The SharePoint and Teams admins: three people, named in ADO 3019.
- **The plan is edited for it** ("Yes, edit the plan"): 7.3's "needs 'Anyone' links allowed on that one site" now says the channel's site, and the Factory Team's site too if the channel's cannot differ (Microsoft's pages disagree; untested), and that the link expires after 90 days and is renewed each quarter; the 14.4 row "Session exports and Teams" says the same. No line count change; `CLAUDE.md`'s plan row notes it.

**Slip: this session's two commits reached `main` directly, not by pull request.** At 18:49 (local clock), the Session 31 scratch-note session, working in the same folder, checked out its own branch and then `main`. So this session's commits `ea71a37` and `c974e65` were made on `main`, and a bare `git push` sent them to GitHub's `main`: Boroon's admin bypass let it through the ruleset, which printed "Changes must be made through a pull request" as a bypassed rule. That broke rule 1 and the merge-by-hand rule in `CLAUDE.md`. Their content is what Boroon agreed in the session. **Boroon, 21 November 2026: "Keep them on main, but do not ever do this again!"** So `main` keeps them, unrewritten, and `CLAUDE.md` end step 4 now says: never push to `main`; check the branch in the same command as every commit; push only with the branch named; read push output in full; use a separate worktree when other sessions may write in this folder. This note and that rule came by pull request from a separate worktree on the session branch: https://github.com/boroonmahanta/overnight-ai-factory/pull/43, **merged by Boroon on 21 November 2026** (`e5b93c2`).

Later in the session (branch `claude/session-32-3019-factory-team`, from `main` after pull request 43, in a separate worktree):
- ADO: every story finished on 21 November was already Done (2461, 2466, 2511 with its tasks Closed, Feature 2510). At Boroon's word, Feature 2464 (trace, redaction and mining spikes) moved from Not Started to **In Progress**, since its story 2466 is Done.
- **3019 step 2 done by Boroon:** the internal Factory Team and a **private** channel, "Cleaned AI Factory Sessions Exports" (the connector shows `membershipType: private`; IDs in ADO 3019, not here, as the repo is public). His first channel for exports was the Team's standard channel, which every Team member can read; asked, he added the private channel, and the standard one is General again (its folder in the Team's library is empty). Boroon then gave the channel site's URL. The connector found the site only by its Graph ID (host name, site ID and web ID, read from the page's context in the built-in browser), not by its path (404, twice); by ID it lists the channel's document library from the laptop, which is empty. The IDs are in ADO 3019.

Files changed: `docs/plans/spike-0.17/README.md`, `docs/plans/schedule.md`, `docs/progress.md`, `docs/sources/plan-v3.1.md` (at Boroon's word), `CLAUDE.md` (the plan row, and end step 4 after the slip).

Open items:
- **Boroon:** make the "Request files" link on `Factory session exports` and send the engineers the how-to (due since Fri 20 Nov); send the admins the README's draft message; make a folder in the private channel's Files (its library is empty, and "Request files" needs a folder). The mining reviewers are not named yet.
- **3019's dates**, at Boroon's word.

Time and tokens (in 3019's body; sessions `1a5096fb` and `25c4345e`, the same session after a restart; measured before the last commit): active time 0 h 46 min (gaps over 10 minutes not counted), from 21 Nov 21:44 to 21 Nov 22:29 (UTC+11). Tokens: 81,304 output; 28,505,649 processed in all, of which 28,108,697 were cache reads. From 2 local transcript(s).

Next steps:
1. Boroon: make the OneDrive link and send the engineers the how-to; send the admins the message; a folder in the private channel's Files.
2. Mon 23 Nov: 2509, the Ignite re-check and the first component register review.
3. Thu 26 Nov: 2548's first mining batch, if exports have arrived.

## Session 31, 2026-11-21, branch `claude/session-31-2466-session-export`

ADO 2466: spike 0.17, session export for mining (DG2). On the laptop (desktop app), apps only, no tenant, a day after its Fri 20 Nov date. Branch stacked on Session 30's (not merged, no pull request yet), so one pull request can carry both. Session renamed "27. Stage 1 - Spike - Session export for mining", like the others. Boroon ran the Copilot app step in a side session.

Done:
- **Spike 0.17 run: passes for all four tools.** `docs/plans/spike-0.17/README.md`: what was tested, 12 findings, the how-to for engineers (one section per tool), the checklist for removing client data, a correction-note template for the fallback, file naming and sending, a draft message for Boroon to send, where exports go, and the scratch list. Each test used a fresh session in the scratchpad with the same small prompt (a file edit, a shell command, an answer), so no client data. Raw exports stayed in the scratchpad.
  - Copilot CLI 1.0.113 (installed in the scratchpad from spike 0.14's lockfile, `npm ci --ignore-scripts`; already signed in through the Copilot app): `-p ... --share <file>` writes Markdown with every tool call, the file edit, shell output and refused calls.
  - GitHub Copilot app 1.2.0: no file export (its menu has "Share as secret gist", which uploads, and "Copy", the session ID). Copilot CLI exports its sessions: they share `~/.copilot/session-state/`.
  - VS Code 1.138.0: "Copy All" is readable but drops output; "Export Chat..." is JSON with everything. Its chat ran on the Copilot CLI engine, so Copilot CLI exported it in full.
  - Claude Code: `/export <name>` writes plain text in a live terminal session, never headless; shell commands are folded to a count, and the opening box shows the account email. The desktop app's Export is a zip of the raw JSONL.
  - The tested export command for any Copilot session: copy the session folder into a throwaway `COPILOT_HOME`, then `copilot --resume <id> --model auto --deny-tool shell --deny-tool write -p "Reply with the single word OK." --share <file>`. The original stays unchanged (checked), a session VS Code holds open can still be exported, and `--model auto` avoids "Model ... is not available". The export turn cost 0.08 AI credits; the CLI's closing figure is the session's running total.
- **The exports folder:** `Factory session exports` in Boroon's OneDrive, made through the Mac's OneDrive sync folder, private to him, with a test file `spike-0.17-cloud-read-test.md` (no client data). The Microsoft 365 connector is read only (`Files.Read.All`, no write scope), so it could not make the folder; it reads the test file from the laptop.
- **The cloud read check: a cloud session can read.** A cloud session, started at Boroon's word and asked only to read, had the same connector and read the test file by its path (token matched). Its listing of the folder by path failed (Graph 400: the connector reads the path's last part as an item ID); from the laptop, the folder lists by its item ID from `sharepoint_folder_search`. Boroon pasted the cloud session's answer here (cloud sessions do not report back). So mining batches (2548) can run in a cloud session.
- 2511 needed nothing: Session 30 had already recorded the merge, 2511 Done and its tasks Closed.
- **Teams first and where exports live, edited into the plan at Boroon's word** ("add the below to this delivery standardisation and factory approach", 21 November 2026). Worded to fit the delivery vault's operating model (`docs/sources/delivery-vault/docs/operating-model.md`), which already sets one internal Team per client and one standard channel per engagement, treats a private channel as an access exception needing admin review, and makes ordinary internal folders readable across GET AI. Plan 6.4: a Teams-first bullet, with a design in a channel folder linked by its exact SharePoint version. Plan 7.3: how each tool exports (spike 0.17) and where exports live: cleaned ones in a private channel of an internal Factory Team, through "Request files" (needs "Anyone" links on that site); the OneDrive folder until then; a raw export, if kept, only in its engagement's GET AI-only channel folder and never with a secret; mining reads only the factory place. A 14.4 row, "Session exports and Teams". Plan now 2,788 lines; `CLAUDE.md`'s line map updated. The spike README gained the lasting home, raw exports and a "What can fail" section; DG4's spec template line and DG6 gained a sentence each.
- **Build stories checked.** One new: **ADO 3019** "A restricted Factory home for session exports", under Feature 2547, Proposed, not dated: first the tenant check that "Request files" can work at all ("Anyone" links; the OneDrive stopgap needs it too), then the Factory Team and private channel, the link, the move, and the connector read check again. No story for the day-gate links: it is part of 2544 (DG4), whose body now says so. No story for raw exports in engagement channels (guidance in the how-to) or for setting up client Teams and channels (the vault keeps that a human checklist). 2548's body now says where mining reads and that it can run in the cloud.
- ADO: 2466 **Done** at Boroon's word ("Yes, close 2466"), with its result and this session's time in its body; its dates not changed. 3019 created; 2544 and 2548 bodies updated.

Decisions (Boroon, 21 November 2026, asked in this session):
- Install Copilot CLI in the scratchpad only, pinned, install scripts off.
- Exports go to a folder only Boroon can read, through a "Request files" link (upload only). No team site was named, so the folder is in his OneDrive.
- Start one small cloud session for the read check.

Found:
- The Copilot app, Copilot CLI and VS Code's chat on the Copilot CLI engine keep one session store; `client_name` in `workspace.yaml` says which tool made a session.
- Every export shows full file paths, and folder names can carry client names (in the checklist).
- The SharePoint search shows client folder names; none is written in this repo.

Files changed: `docs/plans/spike-0.17/README.md` (new), `docs/sources/plan-v3.1.md` (at Boroon's word), `docs/progress.md`, `docs/plans/schedule.md`, `docs/plans/stage-1-day-gate-plan.md`, `CLAUDE.md`.

Open items:
- **Before the engineers are asked: check "Request files" can work** (3019, step 1). Microsoft's page says it needs "Anyone" links allowed for the organisation and on the folder. If the tenant does not allow them, use one subfolder per engineer instead.
- **3019's dates**, at Boroon's word.
- **Boroon makes the "Request files" link** on `Factory session exports` in OneDrive in the browser, then sends the engineers the how-to (the README's draft message). This is the checkpoint set for Fri 20 Nov, now due.
- **Keeping exports** (proposal, Boroon to decide): delete each batch's files once its findings are in `docs/analysis/session-mining.md`, and all of them when DG6 closes (Fri 11 Dec); move the folder to a team site if mining becomes the weekly routine.
- **A possible plan edit** (Boroon to decide): record spike 0.17's result in 11.1, row 0.17.
- **Done: the scratch is deleted** (21 November 2026, at Boroon's word, after the merge): the four Copilot test sessions (the app's through its own Delete, the rest to the Mac's Trash), the Claude Code test session (Trash), the OneDrive test file (OneDrive's recycle bin) and the session scratchpad with the pinned Copilot CLI, the session copies and the raw test exports. Boroon closed the VS Code test window. The empty `Factory session exports` folder stays. Details in the README, last section. Kept here one session for the record.

Time and tokens (in 2466's body; sessions `25494c34` and Boroon's side session `b93b56d7`; measured before the last commit): active time 1 h 03 min (gaps over 10 minutes not counted), from 21 Nov 18:02 to 21 Nov 21:38 (UTC+11). Tokens: 133,345 output; 31,750,296 processed in all, of which 30,675,330 were cache reads. From 2 local transcript(s).

Pull request: https://github.com/boroonmahanta/overnight-ai-factory/pull/41, Sessions 30 and 31 together, **merged by Boroon on 21 November 2026** (`dd2049a`). The scratch note is on branch `claude/session-31-scratch-deleted`, from `main` after the merge.

Next steps:
1. Boroon: check that "Request files" can work in the tenant (3019, step 1), then make the link and send the engineers the how-to.
2. Mon 23 Nov: 2509, the Ignite re-check and the first component register review.
3. Thu 26 Nov: 2548's first mining batch (a cloud session can do it).

## Session 30, 2026-11-21, branch `claude/session-30-2511-gate-live-build`

ADO 2511: bring `GetAI-IP/factory-gates` in line with the live-build plan. On the laptop (desktop app), two days after its Fri 20 Nov finish date. Gate branch `live-build` off `release` at `b37a9f0`.

Done:
- **Gate PR 15** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/15, commits `f99ea9e` and `2cb7b14`), **merged by Boroon on 21 November 2026** (`96b6c61`; 163 tests pass on `release` locally). Tasks 2512 to 2516 and 2518:
  - `pending-scripts.txt`: `create_schema.py` and `create_security.py` out; `plan_from_export.py` and `check_inventory.py` in, under `static`. Still 20 lines.
  - `lcp-gate.yml` matches plan Appendix A: `build` named for generators, packs the XML source layout; `static` with full history, the export-diff plan against the base commit, the `export-plan` artifact and the inventory check; `verify-in-test` without the schema and security plans, downloading `export-plan` into `evidence/`; both floors and the verifier plan read `--plan evidence/export-plan.json`. A normalised diff against the plan's YAML shows only comments, pins and the `setup-node` cache flag.
  - `check_builders.py`: narrowed to generator wrappers, and fails a builder that writes under `src/`, even with the same bytes (inode, size and modification time before and after each builder, so it names the builder). Fixture: its builder now writes `apps/status-app/generated/`, and `src/Other/Solution.xml` stands in for the export.
  - `pack_offline.py`: the source is the XML source layout; says what spikes 0.18 and 0.14 tried and what is untested.
  - `templates/CODEOWNERS`: a note on the commented `/workflows/build/` line. README: rows, a "Live-build follow-ups (ADO 2511)" section, findings 10 and 11. `scripts.sha256` regenerated.
  - Tests: 163 pass (154 before): 8 new in `test_check_builders.py`, 1 in `test_workflow.py`. Manifest verify and rulesets check clean. Eleven deliberate breaks of a scratch copy each failed.
  - On the pull request: **`self-test` green** (run 40136346). `lcp-gate` red at `map lane` (run 40136351), as expected on this repo's own pull requests (README step 10): the gate reader App does not exist yet (2537), so its token step has no `app-id`.
- ADO: task 2517 moved under 2538; 2538's body gained the carry-overs. After Boroon merged gate PR 15: 2511 Done, with its result and time in its body; tasks 2512 to 2516 and 2518 Closed. Session renamed "26. Stage 1 - Build - Gate in line with live build", like the others.

Decisions (Boroon, 21 November 2026, asked in this session):
- A project declares its generator-backed builders as thin wrappers in `workflows/build/`, not a declared list.
- `check_builders.py` fails a builder that writes anything under `src/`, even when the bytes match.
- Task 2517 (`danger-rules.yml`) moves under 2538, to be written with its reader `merge_danger_floor.py`.
- **"Yes, edit the plan"** for Session 30's two proposed edits. Made: Appendix A's opening paragraph now names the XML layout's folders; 5.6 (gate order), 5.7 (job table, trusted-script list), Appendix A (job table, `build` comment) and a new 14.4 row "Generator wrappers and `src/`" carry the two builder decisions. Plan now 2,785 lines; `CLAUDE.md`'s line map updated. Gate PR 15 gained one commit (`2cb7b14`) so its `build` comment uses the plan's wording; a normalised diff of the two files now differs only in comments, pins and the `setup-node` cache flag. 163 tests still pass.

Found:
- **Finding 11 (gate README):** the managed pack cannot come from the unmanaged-only export spike 0.18 tried. Microsoft's docs say pack cannot convert unmanaged to managed. Open item above.
- Plan Appendix A's first paragraph still describes the YAML layout. Proposed edit, open item above.

Files changed: `docs/sources/plan-v3.1.md` (at Boroon's word), `docs/progress.md`, `docs/plans/schedule.md`, `CLAUDE.md`. In `GetAI-IP/factory-gates` (branch `live-build`, commits `f99ea9e` and `2cb7b14`): `.github/workflows/lcp-gate.yml`, `README.md`, `lcp/check_builders.py`, `lcp/pack_offline.py`, `pending-scripts.txt`, `scripts.sha256`, `templates/CODEOWNERS`, `tests/test_check_builders.py`, `tests/test_workflow.py`, the fixture under `tests/fixtures/builder-project/`.

Time and tokens (in 2511's body; session `6df73219`; measured before the last commit, plan edits and closing included): active time 0 h 24 min (gaps over 10 minutes not counted), from 21 Nov 17:38 to 21 Nov 18:01 (UTC+11). Tokens: 84,059 output; 21,489,763 processed in all, of which 21,084,711 were cache reads. From 1 local transcript(s).

Open items:
- Done: Boroon merged gate PR 15 on 21 November 2026; 2511 is Done and its six tasks Closed in ADO, and `CLAUDE.md`'s `factory-gates` row says 163 tests. Feature 2510 ("Gate follow-ups after live build"), which held only 2511, is Done too, at Boroon's word (21 November 2026).
- 2511's dates: done Sat 21 Nov, a day after its Fri 20 Nov finish date. The stories after it are not moved; at Boroon's word only.
- Finding 11 (open item above).

Next steps:
1. Done: gate PR 15 merged, ADO 2511 Done.
2. Mon 23 Nov: 2509 (pin the Copilot CLI install in `verify-in-test`), the Ignite re-check and the first component register review.

## Session 29, 2026-11-21, branch `claude/session-29-2461-option-b`

ADO 2461: spike 0.14, part 4b, option (b) for App Spec stories on an existing app, at Boroon's word (21 November: test (b) in a separate session, then agree the approach). A side session started from Session 28, on the laptop (desktop app). Branch made from `claude/session-28-2461-skills-copilot` at `d6f7127`, in its own git worktree, so Session 28's checkout was not touched. Every run in this session only. Sydney time: 21 November 15:49 to about 16:55.

Done:
- **A `part4b` mode** (copies in `docs/plans/spike-0.14/`; in `GetAI-IP/export-probe` at `35a5779`): part 4's App Spec story again (the column "Category" on `fspk_spikeapprow`, shown on the main form "Spike app row" and in the view "Active Spike app rows"), in one `copilot -p` session as in part 4, with no App Spec apply:
  - the column by Dataverse MCP `update_table` through the shim;
  - the form and view by the Web API, through a new trusted helper, `webapi.py`: it signs in from the Azure CLI's cache, puts the solution header on every write, sends PATCH with `If-Match: *`, and refuses DELETE, PUT, `$batch` and the export, import and removal actions;
  - then `PublishXml`.

  The model-apps plugin stays loaded; the prompt says not to run the build engine, and the probe checks the commands the session started. The driver exports before and after and compares file by file, and checks every form and view ID, the `fspk_` tables, and the helper's and shim's hashes.
- **A `part4b-undo` mode:** takes the column off the forms and views, publishes, then deletes the column. It deletes nothing if any row holds a value.
- **Local checks first** (Session 28's harness, extended: forms and views with published copies, `If-Match`, the helper's headers): four runs. None of Microsoft's code ran on the laptop.
- **Four runs, 21 November:**
  - 40125881: stopped at the first read (`systemform` has no `createdon`), before any change;
  - 40126131: only the column landed; Copilot CLI denied every helper call with a path starting `/` as a file path outside the session (finding 2);
  - 40126711: the undo deleted that column;
  - **40126806: pass, 18 of 18.** Column, form and view changed and published; nothing new or outside the solution; the export changed in exactly three files; packed signed out and offline; 48 s, 15.7 AI credits, 1 MCP call; no `--allow-destructive`; the engine not run; one `rm` refused by the deny list, and the agent went on without it.
- README: "Part 4b" with method, local check, 10 findings, an (a) and (b) side-by-side table, a proposed approach, and 4 proposed plan edits; rows in the parts, runs, left-to-do and scratch tables. `CLAUDE.md`: the map row and the open question.

Decisions:
- **Boroon, 21 November 2026: the approach for App Spec stories on an existing app is agreed,** as part 4b proposed ("Agree", in Session 28, relayed here):
  - at night, (b) for additive changes to an existing app (a column on an existing table, shown on an existing form and view), through a trusted Web API helper the driver ships;
  - the App Spec apply for a new app;
  - (a), a PARK with the dry run as evidence, for any other change to an existing app, until its route is tried.
- **Boroon, 21 November 2026: "Yes, edit the plan"** for this decision. Made in the plan: 5.6 ("Model-driven apps": the three routes as a table, the trusted Web API helper and its rules, columns with the solution header, the App Spec in Git left open; "Live build" points 1 and 3), a note in 11.1 row 0.14, a new 14.4 row, the 15.1 question for 0.14, and an `lcp-executor` rule in Appendix C. `CLAUDE.md`'s line map for the plan is updated.
- **The spike's other plan edits are not made:** part 4's proposals 1 and 3 to 10 (the verdict, `tool_failure`, the MCP cap and retries, the engine, flows, the reset stamp, the gate, 14.4 and 15.1 for those, section 12) and part 4b's 2 to 4 (5.2, section 12, Appendix B). Boroon's "Not yet" stands for them.
- Boroon's decisions of 18 November (Microsoft's plugins unread, pinned, scratch only), 20 November (the retry rule and `tool_failure`) and 21 November (the shim's two cautious choices; test (b) here) were followed.

Files changed: `docs/plans/spike-0.14/` (`README.md`, `tools.yml`, `tools_probe.py`, new `webapi.py`), `docs/sources/plan-v3.1.md` (the decision, at Boroon's word), `CLAUDE.md` (map rows, the plan's line map, the 0.14 question), `docs/progress.md`. In `GetAI-IP/export-probe`: `tools.yml`, `probe/tools_probe.py`, new `probe/webapi.py` (`a0fd9e8`, `74ca863`, `35a5779`). In `factory-lane-1`: the column `fspk_category` on `fspk_spikeapprow`, one row with it on the form "Spike app row", and the column in the view "Active Spike app rows", published (undo: `mode=part4b-undo`, or it goes with the table).

Time and tokens (for 2461's body; session `b2cc769d`; measured before the plan-edit commit): active time 1 h 04 min (gaps over 10 minutes not counted), from 21 Nov 15:49 to 21 Nov 16:53 (UTC+11). Tokens: 192,321 output; 60,829,666 processed in all, of which 60,074,700 were cache reads. From 1 local transcript(s).

Open items:
- **Boroon to say which of the spike's other plan edits to make:** part 4's proposals 1 and 3 to 10, and part 4b's 2 to 4. The App Spec decision itself is agreed and in the plan (above).
- For the Stage 3 helper, now that (b) is agreed: narrow it to the change class's tables, and make columns through it with the solution header (or have the driver add them), because a column made by MCP is in the export only when the table is held with all its parts (finding 3).
- **Copilot CLI's two-word deny rules** (for example `shell(pac solution export:*)`) may never match: its help says a rule names a command and at most its first subcommand. Untested; one refused command on purpose would show it. Part 4b saw `shell(rm:*)` fire.
- The admin centre should show part 4b's 3 MCP calls (3 rows of 0.1) for 21 November, with part 4's 1.
- `GetAI-IP/export-probe` tracks a compiled file, `probe/__pycache__/reset_probe.cpython-315.pyc`, since spike 0.19. Harmless scratch; goes with the repo.

Next steps:
1. ~~Boroon agrees the approach~~ (agreed and in the plan, 21 November 2026). Next: Boroon's word on the verdict and the spike's other plan edits; then those edits, and 2461 to Done.
2. Then 2511, and the dates after 2461 at Boroon's word.

## Session 28, 2026-11-20 to 21, branch `claude/session-28-2461-skills-copilot`

ADO 2461: spike 0.14, part 4 (the skills in `copilot -p`), at Boroon's word, on the laptop (desktop app). Branch made from `main` at PR 39's merge (`427fd15`). One run, in this session only. Sydney time: 20 November 10:18 to 21 November about 15:45. **The app was closed for about a day in the middle, so part 4 did not finish on Friday 20 November as asked; it ran on Saturday 21 November. No date was moved.**

Done:
- **Part 3's bill, read-only in the admin centre** (Boroon's sign-in, the built-in browser). On 20 November the data was last refreshed 18 November (still 6 rows). On 21 November: `factory-lane-1` shows 26 rows of 0.1, 2.6 prepaid credits, last used 19 November. So **part 3 added 20 billed rows: every call that reached Dataverse is billed, tool errors and dropped answers included**; the 2 refused calls are not.
- **`mcp_shim.py` changed to the retry rule Boroon accepted on 20 November.**
  - A tool result with `isError` goes back at once, with no retry and no stop, unless it says throttled.
  - No answer, a JSON-RPC error or the proxy exiting is retried up to 3 times, but only for reads, row writes by ID and creates with IDs; if the proxy exited, it is started again first.
  - Every create gets a row ID before its first attempt, its key named from `EntityDefinitions` (a keys file the probe writes, or the Web API).
  - On a retry, "duplicate key" for a create or "does not exist" for a delete counts as success.
  - A call that still fails is PARK `tool_failure`.
  - Two choices made the safe way, for Boroon to confirm: other tools (table changes, uploads, `invoke_api`) are never repeated, and a batch whose fate is unknown is a PARK.

  The part 3 fake proxy was gone, so it was rebuilt from the README. 21 local checks pass.
- **A `part4` job and mode** (copies in `docs/plans/spike-0.14/`, pushed to `GetAI-IP/export-probe` at `2f194da`, probe fix at `4641e57`).
  - Installs: Copilot CLI 1.0.113 by `npm ci` from a lockfile (`copilot/package-lock.json`), and Microsoft's two plugin repos at their pins, loaded with `--plugin-dir` only.
  - Settings: telemetry off; unattended mode; fresh pac, Dataverse CLI and `az` sign-ins before each story; the shim as the `dataverse` MCP server (cap 60); `--max-ai-credits=150`.
  - Rules: an explicit allow list (10 rules) and deny list (22); `--secret-env-vars` with the OIDC variables. The driver ends a session on a shim stop.
  - Two stories: an App Spec change to the existing app (add a column, show it on the form and view), and the timer flow's Compose step, left off.
- **Local check first:** stand-ins for Copilot, pac, `az` and the Dataverse CLI, and fake Dataverse, token and OIDC services; none of Microsoft's code ran on the laptop. Two runs: all checks passed except the no-network pack (needs Linux); a forced shim stop ended the session with PARK `tool_failure`.
- **Run 40121696, 21 November 2026, 04:25 UTC, 3.9 minutes.**
  - Copilot CLI ran Microsoft's skills headless as the lane identity, on `claude-sonnet-5.5` (the model check passed).
  - **Flow story passed:** FlowAgent's `manage-flows` skill; `list_flows` failed twice with HTTP 401; the agent found the flow with 1 Dataverse MCP read through the shim, then `edit_flow` as a dry run, then applied with its preview token. The flow stayed off and the export holds the change. 12.7 AI credits, 46 s.
  - **App Spec story stopped at the approval point.** Lint and dry run passed (one column to create). The apply was refused: *"refusing to overwrite an existing app. Re-run with --allow-destructive"*. The agent did not pass the flag or work round it, and wrote a clear handoff. 0 MCP calls, 29.7 AI credits, 49 s. Nothing changed in the lane.
  - No tool was denied in either session. The CLI prices 1 AI credit at USD 0.01. The tree packed signed out and offline, round trip byte-identical. No token in the log.
  - The probe's own result said FAIL (10 of 12): the column (rightly not made) and a false alarm on `--allow-destructive` (it matched the engine's refusal text). Two checks fixed after the run (`4641e57`).
- README: part 4's method, local checks, 13 findings, the proposed verdict and 10 proposed plan edits; the bill under part 3; the run table, left to do and the scratch.

Decisions:
- Boroon's decisions of 18 November (Microsoft's plugins unread, pinned, scratch only) and 20 November (the retry rule and `tool_failure`) were followed.
- **Boroon, 21 November 2026:**
  - he confirmed the shim's two cautious choices: tools other than reads and row writes are never repeated, and a batch write of unknown fate is a PARK;
  - he said "not yet" to the plan edits;
  - he asked to test App Spec option (b) (an additive change without the App Spec engine) in a separate session, then agree the approach. That is Session 29, started from this branch.
- He asked what option (a) would really cost. The answer is in the spike README under proposal 2:
  - it hits most XS and S model-driven stories;
  - it adds about a day each, and roughly USD 35 to 60 per accepted story [inference, from the plan's 10.4 model];
  - it keeps `views-forms-additive` off the night path, so that class cannot earn L2.

Files changed: `docs/plans/spike-0.14/` (`README.md`, `mcp_shim.py`, `tools.yml`, `tools_probe.py`, new `copilot/package.json` and `copilot/package-lock.json`), `CLAUDE.md` (map row), `docs/progress.md`. In `GetAI-IP/export-probe`: `tools.yml`, `probe/tools_probe.py`, `probe/mcp_shim.py`, new `probe/copilot/`. In `factory-lane-1`: the timer flow's Compose step (now "v5"), nothing else.

Time and tokens (for 2461's body; session `4476472e`; measured before the closing commit): active time 0 h 45 min (gaps over 10 minutes not counted), from 20 Nov 10:18 to 21 Nov 15:39 (UTC+11). Tokens: 177,351 output; 47,333,965 processed in all, of which 45,999,441 were cache reads. From 1 local transcript(s).

Open items:
- ~~**Boroon to decide**~~: done on 21 November 2026. He confirmed the shim's two choices, agreed the App Spec approach after Session 29 tested option (b), and said "Yes, edit the plan". See "Later the same day" below.
- **2461 is past its date** (Thu 19 Nov). The dates after it move only at Boroon's word; not moved.
- Could follow, not done: a run of the other App Spec route (column by MCP or Web API, form and view by Web API); one refused command on purpose, to test the deny list; the shim's stop as the model sees it; part 4's one MCP call in the admin centre (one more row for 21 November).
- The scratch grows by nothing new: part 4 changed only the timer flow's Compose step. Delete with 0.18's and 0.19's at Boroon's word.

**Later the same day: the plan edits** (branch `claude/session-28-2461-plan-edits`, made from Session 29's `6f08921`, so it holds Sessions 28 and 29). Session 29 had already edited the plan for the App Spec decision (5.6, 11.1, 14.4, 15.1, Appendix C). Session 28 made the rest, at Boroon's word ("Yes, edit the plan", 21 November 2026), and told Session 29 to leave the plan alone:
- 5.2: Copilot CLI as tested headless (lockfile install, `--plugin-dir` only, the shim as the `dataverse` server, explicit allow and deny rules, the path check, `--secret-env-vars` with the OIDC variables, credits and usage, ending a session on a shim stop); where the skills stop for approval.
- 5.4: the version stamp the reset compare and the drift check ignore.
- 5.6: FlowAgent for reading and editing only; the plugins' telemetry switches; an App Spec app's missing dependency (for 2538).
- 5.9: no flow run on demand as the lane identity.
- 5.11 and Appendix D: PARK type `tool_failure`.
- 5.14: the MCP shim, billing of every call, the retry rule as a table, the cap of 50; the premium flow note.
- 11.1 row 0.14: the result. Section 12: risk 34. 14.4: three rows (the retry rule and PARK type, the cap, the verdict). 15.1: two questions closed or answered. Appendix B.1: the small-addition class keyed on the three export files.
- `CLAUDE.md`: the plan's line map (now 2,782 lines), the plan row, the risk count, the open questions. Spike README: the verdict and both proposal lists marked made.

Time and tokens for the whole of Session 28, plan edits and the scratch deletion included (measured before the last commit): active time 1 h 48 min (gaps over 10 minutes not counted), from 20 Nov 10:18 to 21 Nov 17:33 (UTC+11). Tokens: 302,785 output; 138,734,019 processed in all, of which 137,032,579 were cache reads. From 1 local transcript(s).

Next steps:
1. ~~Boroon: move 2461 to Done~~: done on 21 November 2026, at his word ("Yes, move to Done"); its Start and Finish Dates were not moved. ~~When to delete the spike scratch~~: deleted the same day, at his word ("delete the spike scratch", then "Yes, delete it all"); see Current state and the spike 0.14 README, "Scratch". Pull request 40 (https://github.com/boroonmahanta/overnight-ai-factory/pull/40), opened at Boroon's word on 21 November 2026 from `claude/session-28-2461-plan-edits`, carries Sessions 28 and 29, the plan edits and the deletion record. Boroon merges. One pull request from `claude/session-28-2461-plan-edits` would carry Sessions 28 and 29 and the plan edits.
2. Then 2511, and the dates after 2461 at Boroon's word.

## Session 27, 2026-11-19 to 20, branch `claude/session-27-2461-mcp-shim`

ADO 2461: spike 0.14, part 3 (the MCP count-and-retry shim), at Boroon's word, on the laptop (desktop app). Branch made from `main` at PR 38's merge (`7af97fc`). One run, in this session only. Sydney time: 19 November 17:49 to 20 November about 02:30.

Done:
- **`mcp_shim.py`** (new; copy in `docs/plans/spike-0.14/`, pushed to `GetAI-IP/export-probe` at `e598595` as `probe/mcp_shim.py`): a stdio shim between an MCP client and `dataverse mcp`. It passes messages through, counts each `tools/call` and each attempt sent (retries count against the cap), refuses past the cap with a clear error (PARK `budget`), retries a failed call up to three times, stops after the first stop, and logs every call, answer and error as JSON lines with the proxy's stderr. A probe for the Stage 3 driver, not a gate script.
- **A `part3` mode in `tools.yml` and `tools_probe.py`:** the Dataverse CLI 1.0.88 from spike 0.3's pinned tarball and hash, its own `dataverse auth create --githubFederated`, telemetry off; no pac, no Microsoft plugins. Three sessions of a scripted client against `FactorySpike`'s table `fspk_spikeitem`: reads, one create, a bad query, a create on a missing table, a cap of 2, and two creates whose first answer the shim drops (one plain, one with its own row ID; the second was not in the brief, 0.4 credit more). Every row named `spike-0.14 part3 (...)` and deleted by the Web API in the same run.
- **Local check before the run:** a fake `dataverse mcp`, fake Web API, token service and OIDC endpoint; none of Microsoft's code ran on the laptop. The probe's 10 checks and 18 checks of the shim alone (timeouts and late answers, a dying proxy, calls at once against the cap, a server request, redaction, a cap of 0) passed. It caught two bugs, fixed before the run.
- **Run 39749076, 19 November 2026, 09:56 UTC (20:56 Sydney), 1 minute: pass, 10 of 10.**
  - the shim works in front of the real proxy; the counts matched the log; the cap of 2 held and the call past it was refused before it was sent;
  - every failure came back as a tool result with `isError` and a correlation ID, never a JSON-RPC error; the proxy's stderr held no cause (only its cache warning, once per call);
  - a bad query gave "An unexpected error occurred" four times; a missing table gave "Could not find an entity" four times: retrying them wasted 6 calls;
  - **a create whose answer was dropped, retried, wrote twice**; a create carrying its own row ID, retried, got "Cannot insert duplicate key" and wrote once;
  - 20 calls reached Dataverse (6 succeeded, 12 tool errors, 2 dropped successes), 2 refused; so 19 November should show 20 billed rows (2.0 credits), or 8 if only successes bill;
  - the tool list grew since spike 0.3: 16 tools (`invoke_api` new), and `create_record` takes a batch of up to 25;
  - 4 rows made, 4 deleted, none left; no token-shaped string in the log or artifact.
- README updated: part 3's method, local check, 12 findings, proposals for the driver spec, the run, left to do.

Decisions (Boroon, 20 November 2026, after reading the result: "Yes, accept both"):
- **The retry rule:** retry only no answer, proxy errors and throttling, up to three times; retry writes only by row ID, and the shim adds a row ID to every create; a tool result with `isError` (the agent's own mistake) goes back to the agent, with no retry and no PARK.
- **The PARK type `tool_failure`** for a call that still fails after its retries; `budget` stays for the cap.
- Both go into the plan (5.11, 5.14, Appendix D's `Custom.ParkType`) with the spike's other plan edits, at his word. Not edited yet.

Files changed: `docs/plans/spike-0.14/` (`README.md`, `tools.yml`, `tools_probe.py`, new `mcp_shim.py`), `CLAUDE.md` (map row), `docs/progress.md`. In `GetAI-IP/export-probe`: `.github/workflows/tools.yml`, `probe/tools_probe.py`, new `probe/mcp_shim.py`. In `factory-lane-1`: nothing left (4 rows made and deleted).

Time and tokens (for 2461's body; session `9a732068`; measured before the closing commit): active time 0 h 23 min (gaps over 10 minutes not counted), from 19 Nov 17:49 to 20 Nov 02:17 (UTC+11). Tokens: 116,159 output; 13,693,605 processed in all, of which 12,323,891 were cache reads. From 1 local transcript(s).

Open items:
- **2461 is past its date** (Thu 19 Nov in `docs/plans/schedule.md`): part 4 is left. The dates after it move only at Boroon's word; not moved here.
- Check part 3's bill in the admin centre from Fri 20 Nov: 20 or 8 billed rows for 19 November (spike README, part 3 finding 10).
- The accepted retry rule and `tool_failure` PARK type go into plan 5.11, 5.14 and Appendix D with the spike's other plan edits. Until then the plan says the old rule.
- The shim does not yet follow the accepted rule: as run, it retries every failure. Change it at the start of part 4.

Next steps:
0. Pull request 39 (https://github.com/boroonmahanta/overnight-ai-factory/pull/39), opened at Boroon's word on 20 November 2026. Boroon merges.
1. Boroon decides on the dates after 2461.
2. Spike 0.14 part 4 on the laptop (README, "Left to do"): first the shim to the accepted rule, checked locally; then the shim in Copilot CLI's MCP config. Then the exit test verdict and plan edits at Boroon's word. Then 2511.
3. Fri 20 Nov: DG2 (2466), then ask the engineers for their exports.

## Session 26, 2026-11-18 to 19, branch `claude/session-26-2461-app-spec-flowagent`

ADO 2461: spike 0.14, part 2 (the App Spec apply and FlowAgent as the lane identity), at Boroon's word, on the laptop (desktop app). Branch made from `main` at PR 37's merge (`e16329a`). One run, in this session only.

Done:
- **Read, read-only, at the pin** (`power-platform-skills` `05b634d`): the model-apps build engine's command line, sign-in, phases, unattended rules and telemetry switches; its teardown script; FlowAgent's MCP server (tool list, sign-in, the Power Platform API path and when it falls back to the classic flow service, its run routes, its telemetry switches).
- **A `part2` mode in `tools.yml` and `tools_probe.py`** (copies in `docs/plans/spike-0.14/`, pushed to `GetAI-IP/export-probe` at `c7fac82`): the plugins fetched at the full commit ID; telemetry off three ways; Node 22; `az login --service-principal --federated-token` with the job's OIDC token (the same federated credential as pac); the App Spec's lint, dry run and apply; a small stdio MCP client for FlowAgent, on both paths; then export, compare and pack offline. Logs are filtered for token-shaped strings, and a scan step deletes any output file that still holds one before the upload.
- **Local check before the run:** a scratch harness with a fake Dataverse, token service, OIDC endpoint and `az`, a stand-in `pac` (real pack and unpack, never `auth`), and stand-ins for the engine, the lint and FlowAgent's server. None of Microsoft's code ran on the laptop. All checks passed. The plugin fetch step ran for real (git only).
- **Run 39563486, 19 November 2026, 3.6 minutes:**
  - the App Spec apply works as the lane identity for a tiny spec (one new table, a form, a view, an app): unattended, never `--allow-destructive`, apply 109 seconds, verify 13 of 13;
  - all it made landed in `FactorySpike` and the export, and the tree packs again signed out and offline, round trip byte-identical;
  - the export now has a `<MissingDependencies>` block: the app's two settings need definitions from Microsoft's `msdyn_AppFrameworkInfraExtensions`;
  - FlowAgent reads and edits flows as the lane identity (`get_flow`, `get_flow_context`, `update_flow` through Dataverse, `get_run_history`), but `list_flows`, `publish_flow`, `disable_flow` and `run_flow` are refused with HTTP 401 (`x-ms-client-scope` header missing), on both paths;
  - the GitHub OIDC token lasts 5 minutes, and `az` uses it for every new token.
- README updated: the part 2 method, 13 findings, the run, the scratch, what is left.
- ADO: 2461's body has this session's result and time; it stays Building.

Decisions: none new. Boroon's decision of 18 November (Microsoft's plugins run unread for this spike only, pinned, telemetry off, scratch only) was followed: the plugins ran only in `GetAI-IP/export-probe` against `FactorySpike`.

Files changed: `docs/plans/spike-0.14/` (`README.md`, `tools.yml`, `tools_probe.py`), `CLAUDE.md` (map row), `docs/progress.md`. In `GetAI-IP/export-probe`: `tools.yml` and `probe/tools_probe.py`. In `factory-lane-1`, inside `FactorySpike`: the App Spec's table, app, site map, two app settings and icon web resource; the timer flow's Compose step changed by FlowAgent (it stayed off).

Time and tokens (for 2461's body; session `c3cca54e`; measured before the closing commit): active time 0 h 43 min (gaps over 10 minutes not counted), from 18 Nov 23:08 to 19 Nov 10:34 (UTC+11). Tokens: 121,551 output; 25,181,176 processed in all, of which 23,974,793 were cache reads. From 1 local transcript(s).

Open items:
- Parts 3 and 4 of spike 0.14 (the MCP count-and-retry shim; the skills in `copilot -p`), in the spike README under "Left to do". 2461 is due Thu 19 Nov in `docs/plans/schedule.md`; if parts 3 and 4 do not fit today, the dates after it move at Boroon's word.
- **The driver must keep `az` signed in** (part 2 finding 9): the OIDC token lasts 5 minutes and `az`'s tokens an hour. For part 4 and the Stage 3 driver spec.
- **The gate must take an App Spec app's missing dependency** on Microsoft's `msdyn_AppFrameworkInfraExtensions` (part 2 finding 3): the import into Test, the manifest check and the danger rules. For 2538.
- **No route tried starts a flow run on demand as an app identity** (part 1 finding 3, part 2 finding 6). `lcp-verify flow` (plan 5.9) needs another way to see a run. For the plan edit at the end of the spike, at Boroon's word.
- The scratch grows: the App Spec's table, app, site map and icon. An undo mode by the Web API is not written yet; never use Microsoft's `teardown-model-app.js` on it, because its last step deletes the `FactorySpike` solution.

Next steps:
1. Pull request 38 (https://github.com/boroonmahanta/overnight-ai-factory/pull/38), opened at Boroon's word on 19 November 2026. Boroon merges.
2. Spike 0.14 parts 3 and 4 on the laptop (README, "Left to do"), then the exit test verdict and plan edits at Boroon's word. Then 2511.
3. Fri 20 Nov: DG2 (2466), then ask the engineers for their exports.

## Session 25, 2026-11-18, branch `claude/session-25-2461-lane-tools`

ADO 2461: spike 0.14, skills and lane tools headless as the lane identity, started at Boroon's word ("start ADO story 2461"), two days after its Mon 16 to Tue 17 Nov slot. A laptop session (desktop app). Branch made from `main` at PR 36's merge (`c4c0d17`); the folder was on Session 23's branch with two uncommitted edits from the 13 November daily sync (DG2, ADO 2466, brought forward to Mon 16 Nov, at Boroon's word), carried over by stash and kept on this branch. The stash was dropped once this branch was pushed.

Done:
- **Read, read-only:** both of Microsoft's plugin repos at today's heads (`power-platform-skills` `05b634d`, `Dataverse-skills` `79ec1e2`), for how they sign in and where they stop for a person; Microsoft's docs on service principal flows, their licences and the `flowrun` table; GitHub's docs on Copilot CLI in Actions and on GHE.com.
- **Found before any run:** the model-apps plugin and FlowAgent both get every token from `az account get-access-token`, so an `az login` as the lane identity should serve them; FlowAgent's connection tools sign in as a user only. `/app-builder` has an unattended mode (`POWER_PLATFORM_SKILLS_NONINTERACTIVE=1`) that treats the dry run as the approval and never grants `--allow-destructive`; `dv-solution` has none. **A premium flow owned by a service principal needs a licence** (a Process licence, a flow group, or a licensed co-owner), and the Dataverse connector is premium.
- **Run 39346986: Copilot CLI works on a getai.ghe.com runner** with the job's own `GITHUB_TOKEN` (`copilot-requests: write`, `GH_HOST=getai.ghe.com`, CLI 1.0.113): `ready`, exit 0, 2.5 seconds. No seats, no secret. The model and the billing are spike 0.6's to find.
- **Run 39347126: part 1 passes for a flow with no connector.** As `getai-fl1-exec`, the Web API made a schedule flow in `FactorySpike`, updated it, turned it on (it ran at once, `Succeeded`), turned it off; the export held it with the update, and it packed again signed out and with no network, round trip byte-identical. The classic flow service accepted the lane identity's app-only token to read runs. Spike 0.18's Dataverse flow (empty connection reference, premium connector) **turned on** through the Web API, could not be started (HTTP 401, a missing `x-ms-client-scope` header) and was turned off again.
- **Microsoft's server update shows in the export:** `9.2.26101.184` became `9.2.26102.148` in `Other/Solution.xml` and `Other/Customizations.xml` between 10 and 18 November. 0.18 finding 9 expected it; the reset's byte proof and the drift check must ignore those three attributes.
- New: `docs/plans/spike-0.14/` (`README.md`, and copies of `tools.yml`, `copilot-check.yml`, `tools_probe.py`, pushed to `GetAI-IP/export-probe` at `a2e0d57`). Local check before the run: the probe ran end to end against a fake Dataverse with the laptop's real pac (2.15.1, a release past 2.14.1).
- ADO: 2461 to Building (the process has no "In Progress"), with this session's result and time in its body.

Decisions (Boroon, 18 November 2026):
- Run Microsoft's plugins unread for this spike only: pinned, telemetry off, scratch repo and `FactorySpike` only. The full read (rule 19) comes before adoption.
- Try one Copilot call before waiting for spike 0.6.
- Make a flow with no connector, and also try the Dataverse flow.

Files changed: `docs/plans/spike-0.14/` (new), `docs/plans/schedule.md`, `docs/plans/stage-1-day-gate-plan.md` (the DG2 move, from 13 November), `CLAUDE.md` (map row), `docs/progress.md`. In `GetAI-IP/export-probe`: the three files above. In `factory-lane-1`: the flow "Factory spike timer flow" (off, in `FactorySpike`); "Factory spike flow" turned on and off.

Time and tokens (for 2461's body; session `463d72cd`; measured before the closing commit): active time 0 h 40 min (gaps over 10 minutes not counted), from 18 Nov 10:58 to 18 Nov 17:32 (UTC+11). Tokens: 77,897 output; 19,806,510 processed in all, of which 18,987,371 were cache reads. From 1 local transcript(s).

Open items:
- Parts 2 to 4 of spike 0.14 (the App Spec apply and FlowAgent as the lane identity; the MCP shim; the skills in `copilot -p`), listed in the spike README under "Left to do".
- A lane flow that uses Dataverse needs a licence to run as the lane identity (plan 5.9, 5.14). Not in the plan yet; for the plan edit at the end of the spike, at Boroon's word.
- The scratch grows by one flow; delete it with `tools.yml` `flow-undo` before 0.18's teardown.
- 2466 (DG2) is still Proposed in ADO: it was moved to Mon 16 Nov and did not run. Now set to Fri 20 Nov (below).

**Dates moved (Boroon, 18 November 2026: "Thu 19, shift a day"),** here in `docs/plans/schedule.md` and in ADO: 2461 Wed 18 to Thu 19 Nov; 2511 Thu 19 to Fri 20 Nov; 2466 (DG2) Fri 20 Nov, so the checkpoint with the engineers stays Fri 20 Nov; 2509 Mon 23 Nov; 2538 Tue 24 to Mon 30 Nov; 2537 Tue 1 Dec; 2451 (spike 0.6) Wed 2 Dec only, one day not two, because run 39346986 already did part of it (2451's body says what is left). Nothing from Thu 3 Dec on moves; the Stage 1 exit test stays Fri 18 Dec. The documents track does not move. If 2451 needs its second day after all, everything from Thu 3 Dec moves a day and the exit test lands on Mon 21 Dec, in the buffer.

Next steps:
0. Pull request 37 (https://github.com/boroonmahanta/overnight-ai-factory/pull/37), opened at Boroon's word on 18 November 2026. Boroon merges.
1. Thu 19 Nov, laptop: spike 0.14, parts 2 to 4 (README, "Left to do"). Then 2511, Thu 19 to Fri 20 Nov.
2. Fri 20 Nov: DG2 (2466), then ask the engineers for their exports.

## Session 24, 2026-11-13, branch `claude/session-24-2505-dependabot`

ADO 2505: review and merge the Dependabot pull requests in `GetAI-IP/factory-gates`, on its target date. A laptop session (desktop app). Sessions 22 and 23 were working in the same laptop folder at the same time, and Session 23 switched its branch to `claude/session-23-2545-standards-seed` during this session. So this branch was made from `main` at PR 34's merge (`6e16839`) in a separate worktree, and the shared folder's branch was not touched.

Done:
- **#10 and #11 no longer existed.** On Monday 9 November Dependabot closed them ("Superseded by #14", "by #13") and opened #14 (`setup-dotnet` 5.4.0 to 6.1.0) and #13 (`upload-sarif` 3.39.1 to 4.39.3), both on `85ad2b5`. #9 (`setup-python` 5.6.0 to 7.1.0) was still on `d0e19ed`, before gate PR 12.
- **Release notes read** for every major crossed, and each action's `action.yml` compared between the old and new pins:
  - `setup-python`: v6 moves to Node 24; v7 only changes internals (ESM) and drops `pip-install`, which we do not use; 7.1.0 adds opt-in `mirror` inputs. Python 3.11 is still served.
  - `setup-dotnet`: v6.0.0 only changes internals (ESM); 6.1.0 adds `check-latest` (default true, the old behaviour) and `skip-lts-prepass` (default false), and a fallback install folder when the default is not writable.
  - `upload-sarif`: v4 runs on Node 24; 4.39.2 and 4.39.3 change nothing for `upload-sarif`. CodeQL Action v3 is deprecated in December 2026, so this move was needed anyway.
- **Every pin checked with `git ls-remote`** on github.com: each new commit is its tag's (`codeql-action` v4.39.3 is an annotated tag; its peeled commit is the pin), and each old pin matched its old tag.
- **A trial merge of all three onto `release`**, in a throwaway worktree: clean in any order, 154 tests `OK`, manifest verify and rulesets check clean, no old pin left.
- **At Boroon's word, `@dependabot rebase` on #9**, because its `self-test` run predated gate PR 12. Dependabot rebased it onto `85ad2b5` (`c27a240`, the same seven pin lines), and `self-test` passed (run 38469336). #13 and #14 had `self-test` green on `85ad2b5` (runs 37450731 and 37450751). `lcp-gate` red at `map lane` on all three, as expected: the gate reader App does not exist, so the token step fails.
- **Boroon merged #9, #13 and #14** at 08:01 to 08:02 UTC (merge commits `60aee3b`, `90890cc`, `b37a9f0`). Dependabot's branches went on their own. On the laptop afterwards: Finder files cleared, `release` at `b37a9f0`, 154 tests `OK`, manifest and rulesets clean, no old pin left, every `uses:` comment the version alone. No new Dependabot pull request is open.
- **ADO:** 2505 Done, renamed "Review and merge Dependabot PRs #9, #13 and #14 (were #9, #10 and #11)", with the result and this session's time and tokens in its body. Tasks 2506 to 2508 Closed with their results; 2507 and 2508 renamed for #14 and #13.

Findings:
- Dependabot closes its own superseded pull requests when a newer version comes out, so an ADO item named by pull request number can go stale within a week. Name the action and check the live list.
- Only `setup-python` 7.1.0 has run for real on a GHE.com runner (in `self-test`). `setup-dotnet` and `upload-sarif` are used only by gate jobs that are skipped until `map lane` gets its token, as in the first round.
- A merge shows as "unstable" while `lcp-gate` is red, because no status check is required on `release`. It does not block the merge.
- Three sessions in one laptop folder: a branch switch by one moves the others' working tree. Nothing was lost here (the folder was clean), but a session that commits should check its branch first, and use its own worktree when another session is active.

Decisions (Boroon, 13 November 2026): post `@dependabot rebase` on #9 before merging.

Nothing in the tenant was changed.

Files changed: `docs/progress.md`, `docs/plans/schedule.md`. In `GetAI-IP/factory-gates`, by Dependabot's pull requests #9, #13 and #14: `.github/workflows/lcp-gate.yml` and `.github/workflows/self-test.yml`, pin lines only.

Time and tokens (for 2505's body; session `39691d10`; the review, the rebase, the checks and the ADO updates; measured before the closing commit): active time 0 h 19 min (gaps over 10 minutes not counted), from 13 Nov 16:33 to 13 Nov 19:05 (UTC+11). Tokens: 31,067 output; 8,017,868 processed in all, of which 7,654,403 were cache reads. From 1 local transcript(s).

Open items:
- When the gate reader App is made, `client-id` instead of `app-id` (Open items).

Next steps:
1. Pull request 36 (https://github.com/boroonmahanta/overnight-ai-factory/pull/36), opened at Boroon's word. Session 23's pull request 35 merged first, so `main` was merged into this branch: this entry sits above Session 23's, and the schedule keeps both notes. Boroon merges.
2. Mon 16 to Tue 17 Nov, laptop: spike 0.14 (2461).

## Session 23, 2026-11-13, branch `claude/session-23-2545-standards-seed`

ADO 2545, part 2: day-gate session DG3, the coding standards seed, a week before its Fri 20 Nov slot, at Boroon's word ("Start DG3"). A laptop session (desktop app), started from `main` at PR 34's merge (`6e16839`).

Done:
- **Read the older ADO vault, read only** (`getai` / `GETAI-PowerPlatform` / `vault`, `main` at `5f26ede`), through the Azure DevOps connector: the standards index, all seven standards files, the design (SDD) template, the work workflow (for the per-story build brief), the "suggest patterns and skills" workflow and the week workflow. Nothing there was changed.
- **Found: the vault holds 50 standards, not 46.** The six `GS` domains hold 46 (34 rule, 12 judgement), as the plan says. A seventh file, the client-token standards `TOK-001` to `TOK-004` (3 rule, 1 judgement), is the vault's own decision with no `GS` document behind it. **Boroon chose to keep them:** 50 in all, 37 rule and 13 judgement.
- **Created `GetAI-IP/factory-manifestos`** on `getai.ghe.com` (repo ID 5389656): private, default branch `main`, a starter README. Protected the way `factory-gates` is, at Boroon's word: repo ruleset `main-protection` (ID 52231) on `refs/heads/main`, pull request required with 0 approvals, no deletion, no force push, no bypass list. Read back after creation. The org ruleset `protect-main` covers only three named repos and needs 1 approval plus a code owner, so Boroon could not have merged alone.
- **Opened pull request 1 there** (https://getai.ghe.com/GetAI-IP/factory-manifestos/pull/1, branch `2545-lcp-standards`, commit `dcceec6`): `practices/lcp/coding-standards.md`. Every standard keeps its ID, class and meaning. The changes:
  - anonymised: no client, person, programme or engagement names, synthetic examples, engagement counts dropped;
  - the vault's records mapped to the factory's (decision records in `docs/adr/`, the spec and plan for the SDD, flow patterns by name);
  - Australian English, no em-dashes.
  
  Checked before the push: 50 IDs, 37 rule and 13 judgement; a search for every client, programme, person and domain code word in the vault files found none; no em-dashes. **Boroon merged it on 13 November 2026 at 19:02** (merge commit `fd2e268`); the file on `main` matches the pushed file byte for byte. ADO: 2545 Done, Finish Date Fri 13 Nov.
- Updated: `staging/README.md` and `staging/factory-manifestos/README.md` (where the standards are; the starter README is replaced at DG8), `docs/plans/stage-1-day-gate-plan.md` (the repo exists; DG3's run), `docs/plans/schedule.md` (2545's row and a change entry), `CLAUDE.md` (where the standards live, and the count).
- **Not done in DG3:** step 5, sending the engineers the DG2 how-to, waits for DG2 (Wed 18 Nov), so the checkpoint stays on Fri 20 Nov. The eight flow patterns in step 1 were not read in full, only listed: child-flow secret retrieval, composite-key parameter binding, empty-array expressions, environment variable defensive expressions, identifier versus label fields, shared-state orchestration, try/catch and swallowed failures, and plug-in package build and deploy. Read them when `lcp-flow-patterns` is built.

Notes for DG4 and DG6 (DG3 step 4), anonymised:

- **The design (SDD) template's sections**, for the `getai-lcp` plan template (DG4). Guidance: write it so someone who was not in the requirement conversation could build from it; delete a section that truly does not apply rather than leave it empty.
  1. Requirement: one plain paragraph, what was asked and by whom, pointing at the source (or "verbal", with who and when).
  2. Scope: a table of components, each new or existing, with notes. Check the inventory first: never propose a new table, flow or screen without confirming nothing already does it.
  3. Design: the technical shape. For a flow: the trigger, the action sequence in prose or steps, error handling, what it calls and what calls it. For a canvas app: screens, controls, data sources, the change in behaviour. Name every new component now against the coding standards (flow name and number, control names, table and column names, choice values), so naming is a design decision, not a review finding.
  4. Environment variables and connection references needed: schema name, purpose, default value (non-secret only). `ALM-002` and `ALM-007` tie in here: a new child-flow call needs its `-URI` variable, with a value per environment and no default.
  5. Data model changes (deleted if none).
  6. Open questions, split into "we can answer" and "ask the client". The client's answers are pasted back before the design is ready to build.
  7. Decisions this depends on: links only. A fork found while writing is recorded as a decision, not buried in prose.
  8. Risks: links only.
  9. Test plan and acceptance criteria: specific inputs and outcomes, and edge cases (empty input, a duplicate, the case that prompted the requirement).
  10. Build handoff: target environment (DEV unless stated), solutions touched, one or two sentences for the build session. Kept current; the last thing written before handoff.
  11. Status checklist: design complete with no open client questions; reviewed against the standards; ready for build; built (a deployment record); source pulled back.
- **The per-story build brief** (the work workflow's Provision stage), for `handoff/` (DG4):
  - one brief per story, named by the work item ID; never overwritten, never a bare `brief.md`;
  - the whole approved design copied in, with a snapshot time;
  - only the build constraints and the tool and source handoff this story needs;
  - the explicit ADO organisation, project name and ID, team, area, work item URL and source mapping, so the build cannot fall back to a central project;
  - build permissions widened only when needed, never narrowed;
  - no operating manual, skills or standards copied into the build context;
  - the brief's path, snapshot and handoff commented on the work item.

  The Build stage adds: check flow states after each import and record what was and was not checked; never use a flow update that strips a connection's authentication details (assessment section 6, question 4); comment progress and blockers on the work item.
- **The retro workflow's rules**, for mining (DG6). In the vault, "retro" and "suggest patterns and skills" are one workflow, tagged retrospective. The week workflow is timesheets, not a retro.
  - Run only when a person asks; never automatic.
  - The window starts at the last run marker; the first run covers all history.
  - Per active project, Git history in the window is the baseline. Read the worklogs, decisions, risks, reviews and changed designs. Only projects with activity.
  - Changes to standards, patterns, workflows and skills are reviewed once, apart from the projects.
  - Every statement rests on a commit, file or worklog. No story is inferred from missing records.
  - Check existing patterns first. Propose a pattern only for a reusable technique, with its problem, technique and where it does not apply.
  - Propose a skill only after the work was done by hand at least three times and no existing stage covers it; otherwise propose a change to that stage. A first occurrence is an early flag only.
  - Check the backlogs for duplicates; add a dated repeat under an existing candidate.
  - Never write a pattern or make a skill from the review; proposals go to the backlogs.
  - The run marker goes last: the window, the projects reviewed, the proposal counts.
  - Never expose client data, guess at a person's judgement, edit another person's records, treat an inactive project as if work happened, or treat a plug-in's capability as a new skill without saying so.

  This fits DG6: the three-repeat bar is its step 3, and "proposals only, nothing auto-created" matches "a PR or a recorded no action".

Decisions (Boroon, 13 November 2026):
- Run DG3 now, not on Fri 20 Nov.
- Protect `factory-manifestos` like `factory-gates`: its own ruleset, 0 approvals until a second approver.
- Keep the vault's four client-token standards: 50 standards, not 46.
- Edit the plan for it ("Yes, edit the plan").

**The plan is edited** (at Boroon's word, later the same day): 5.10's low-code seed now says 50 (37 rule, 13 judgement) and names `GetAI-IP/factory-manifestos`, `practices/lcp/coding-standards.md`; 5.12's table row says 50; 14.4 has a new row, "The low-code standards seed". The plan is one line longer, so `CLAUDE.md`'s line map is updated from section 14 on. DG3's "done when" in the day-gate plan and 2545's row in the schedule say 50 too. The 14.4 rows of 7 November (assessment item 8, D1) still say 46: they record what was decided then.

Files changed: `staging/README.md`, `staging/factory-manifestos/README.md`, `docs/plans/stage-1-day-gate-plan.md`, `docs/plans/schedule.md`, `docs/sources/plan-v3.1.md`, `CLAUDE.md`, `docs/progress.md`. On GHE: the new repo, its ruleset and pull request 1.

Time and tokens (for 2545's body; session `8f7174db`, measured before the closing commit): active time 0 h 13 min (gaps over 10 minutes not counted), from 13 Nov 16:34 to 13 Nov 16:47 (UTC+11). Tokens: 50,755 output; 7,115,525 processed in all, of which 6,870,749 were cache reads. From 1 local transcript.

Open items:
- Ask the Get AI Engineer to review the standards (assessment section 6, question 2). Their review does not block the merge. Boroon to ask.
- `main-protection` in `factory-manifestos` is a second-approver stopgap, like `release-protection`. 2520 must raise it to 1 approval too.

Next steps:
1. Done: `factory-manifestos` pull request 1 merged; 2545 Done in ADO. This branch needs a pull request here, when Boroon asks.
2. Mon 16 to Tue 17 Nov, laptop: spike 0.14 (2461).
3. Wed 18 Nov: DG2 (2466); Fri 20 Nov: the DG3 checkpoint, sending the engineers the how-to.

## Session 22, 2026-11-13, branch `claude/session-22-2433-mcp-billing`

ADO 2433: check Dataverse MCP billing for `factory-lane-1`, on its target date. A laptop session (desktop app), started from `main` at PR 32's merge (`7ecb357`). Numbered 22 because two branches already use 21 (`session-21-2549-skills-policy` and `session-21-progress-dashboard`).

Done:
- **Read Microsoft's docs** on Dataverse MCP billing: every tool except `search_data` bills at the "text and generative AI tools (basic)" rate, 1 Copilot Credit per 10 responses; the pay-as-you-go meter is USD 0.01 per credit.
- **Checked the Power Platform admin centre**, read-only, in the built-in browser under Boroon's existing sign-in: Licensing, Copilot Studio, Environments, `factory-lane-1`. It shows 0.6 prepaid Copilot Credits, last updated 6 November, as six rows of "Dataverse MCP Server", 0.1 billed each. That matches spike 0.3 run 3's six tool calls. No allocation, no pay-as-you-go, "Draw from tenant" on. The tenant has no pay-as-you-go billing plan and does hold prepaid capacity.
- **So the calls were metered,** from the tenant's shared prepaid pool. "No Copilot Credit source" in the spike record was wrong. One MCP call is USD 0.001 at list.
- `docs/plans/spike-0.3/README.md`: finding 13 corrected and a new section, "Billing check", with what the portal shows and seven points on what it means. Tenant totals, other environments and people are left out (public repo).
- ADO 2433 moved to Done, with the result and this session's time and tokens in its body.
- `docs/plans/schedule.md`: 2433 done Fri 13 Nov. `CLAUDE.md`: the open question on Dataverse MCP now gives the billing answer.

- **The plan is edited for the result** (three lines, at Boroon's word, 13 November 2026): 5.6's table row for `/api/mcp`, "Other meters" in 5.14, and the 15.1 row on Dataverse MCP. Each now gives the rate and the check.

- **The cap decision and the ledger are edited into the plan** (at Boroon's word, later the same day):
  - 5.14 states the cap; 5.11 makes both stops a PARK, an exception to "stops that are not a PARK"; 5.6's row and 15.1 point to it; 14.4 has a new row.
  - 10.2: `fact_run` gains `mcp_calls`; Dataverse MCP leaves `fact_fixed_cost` and is costed per run as `lcp_meter`, checked monthly against the admin centre's report.
  - 10.5 (not 10.4, as first said): MCP leaves the fixed lines and is priced per call.
  - The plan is one line longer (the 14.4 row), so the line map in `CLAUDE.md` is updated from section 14 on.
- **ADO:** 2433's body has the decision and the plan edit. 2461 (spike 0.14) gains three items: count MCP calls per session to set the cap, try a way for the driver to count and retry, and find which MCP errors are safe to retry.

Decisions (Boroon, 13 November 2026):
- Edit the plan's billing lines.
- **The lane's MCP cap:** leave "Draw from tenant" on; the driver stops the session after a set number of MCP calls, the number set from spike 0.14; a failed call is retried three times; either stop is a PARK.
- Cost Dataverse MCP per run in the ledger, not as a fixed monthly line.

Nothing in the tenant was changed.

Files changed: `docs/plans/spike-0.3/README.md`, `docs/sources/plan-v3.1.md`, `docs/plans/schedule.md`, `CLAUDE.md`, `docs/progress.md`.

Time and tokens (for 2433's body; session `2a17603a`; the check, the plan edits, pull request 33 and the ADO updates; measured before the closing commit): active time 0 h 24 min (gaps over 10 minutes not counted), from 13 Nov 16:05 to 13 Nov 16:29 (UTC+11). Tokens: 54,482 output; 13,527,017 processed in all, of which 13,187,821 were cache reads. From 1 local transcript(s). In 2433's body, replacing an early 4-minute reading.

Pull request 33 (https://github.com/boroonmahanta/overnight-ai-factory/pull/33), the first three commits, was merged into `main` by Boroon on 13 November 2026 at 16:29 (merge commit `968201d`). The later commits on this branch (this log fix, the refreshed time and tokens) are not in it.

Open items:
- What spike 0.14 and the driver spec must settle for the MCP cap (Open items).
- 2549's ADO updates, left by Session 21: found already made by another laptop session the same day (Open items).

Next steps:
1. Done: PR 33 merged. The branch's later commits need a second pull request, when Boroon asks.
2. Fri 13 Nov, laptop: 2505 (Dependabot PRs #9 to #11).
3. Mon 16 to Tue 17 Nov, laptop: spike 0.14 (2461). It now also counts MCP calls per story, to set the cap, and checks which MCP errors are safe to retry.

## Session 21, 2026-11-11, branch `claude/session-21-2549-skills-policy`

ADO 2549: the third-party skills policy (plan 8.3) applied to every vendored skill, a day before its Thu 12 to Fri 13 Nov slot. **A cloud session** (documents track). Started from `main` at PR 31's merge (`8e81f24`); `main` was already current.

Done:
- **Listed every third-party skill:** 56 on the shelf (Addy 10, Tan 35, Pocock 9, Benny 2) and the 44 live skills built from them. All 44 come from those three sources.
- **Looked up:**
  - each source cloned at its pin, and every shelf file compared with the upstream file by git blob hash: all byte-identical;
  - every licence read from upstream: all MIT;
  - upstream heads: Addy and Pocock are still at our pins; `cursor/plugins` is at `63912a9`, with no change under `pstack/` since the pin;
  - no plugin install, settings file or network call in any copied script, so nothing auto-updates or reports telemetry.
- **Found and fixed, as facts:**
  - `bro` is Lauren Tan's `bro`, adopted unchanged on 1 November, before the policy, with no shelf copy, pin or licence on record. Now on the shelf at `skills/tan/bro/`, with rows in `skills/README.md`.
  - `doubt-driven-development` points twice at Addy's `references/orchestration-patterns.md`, which was never copied or read. Now copied to `skills/references/` and read in full (18 KB; no scripts, no network, nothing aimed at a reviewer).
  - `skills/README.md` said batch 2 was not yet reviewed; it was merged with PR #4 on 2 November. Corrected. It and the batch 2 notes also said every adopted principle had a GET AI note; six had none. Corrected, after the fix below.
- **At Boroon's word:**
  - the register file `docs/component-register.md`, one row per source at a pin;
  - each source's `LICENSE` copied unchanged to `skills/addy/`, `skills/pocock/`, `skills/tan/` and `skills/benny/`;
  - a source line in the 10 live skills that had none: `constraint-driven-development`, `doubt-driven-development` (also naming its broken link), `source-driven-development`, `bro`, and the principles `build-the-lever`, `encode-lessons-in-structure`, `experience-first`, `fix-root-causes`, `redesign-from-first-principles`, `test-behavior-not-implementation`. Checked: each differs from its shelf original only by that line.
- **The result:** `docs/analysis/skills-policy-check.md`. It has the method, the gaps common to all, one table (skill, source, commit, licence, read in full and where, status, gaps, fix), and notes on points 5 and 6. Only gap left: `poteto-mode` (shelf only) is not read in full.
- `docs/plans/schedule.md`: 2549 done Wed 11 Nov; nothing moves.
- `CLAUDE.md`: rows for the two new files; the `skills/` and `.claude/skills/` rows.

Decisions (Boroon, 11 November 2026):
- The register is a new file here, `docs/component-register.md`, one row per third-party source at a pin. A1 (ADO 2740) adds the kits to it.
- Licence text goes on the shelf, one file per source. None goes in a live skill folder.
- Add a source line to the 10 live skills that lacked one (rule 17: it reaches `main` when Boroon merges this branch).

Files changed: `docs/component-register.md`, `docs/analysis/skills-policy-check.md`, `skills/addy/LICENSE`, `skills/pocock/LICENSE`, `skills/tan/LICENSE`, `skills/benny/LICENSE`, `skills/tan/bro/SKILL.md`, `skills/references/orchestration-patterns.md` (all new); `skills/README.md`; `docs/analysis/skills-reading-notes-batch2.md`; 10 live skills' `SKILL.md` in `.claude/skills/` (named above); `docs/plans/schedule.md`; `CLAUDE.md`; `docs/progress.md`.

Time and tokens (for 2549's body; session `e9ddef2d`, measured before the closing commit): active time 0 h 12 min (gaps over 10 minutes not counted), from 11 Nov 18:28 to 11 Nov 18:40 (UTC+11). Tokens: 59,713 output; 10,495,702 processed in all, of which 10,163,310 were cache reads. From 1 local transcript. This cloud container kept its own transcript, so `tools/session_usage.py` ran here (with `--root ~/.claude/projects/-home-user-overnight-ai-factory`). The transcript goes when the container is reclaimed, so this line is the record. No other story was worked.

**ADO is not updated:** a cloud session cannot reach it. The next laptop session makes the updates (Open items).

Open items:
- The ADO updates for 2549 (Open items).
- The first register review, Monday 23 November (Open items).
- `poteto-mode` not read in full (Open items).

Next steps:
1. Boroon: review this branch, which changes 10 live skills (rule 17). A pull request when he asks.
2. Thu 12 and Fri 13 Nov are now free on the documents track. Fri 13 Nov, laptop: 2433 and 2505, and the ADO updates for 2549.
3. Mon 16 to Tue 17 Nov, laptop: spike 0.14 (2461), reusing 0.18's and 0.19's scratch.

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
