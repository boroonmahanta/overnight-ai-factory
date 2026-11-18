# Spike 0.14: skills and lane tools headless, as the lane identity

Plan section 11.1, row 0.14 (ADO 2461). Session 25, 18 November 2026 (Sydney time), and Session 26, 18 to 19 November 2026, laptop sessions. Started two days after its Mon 16 to Tue 17 Nov slot. Not finished yet: what is done and what is left are below.

**So far (19 November 2026):** part 1 passes for a flow with no connector: made, updated, turned on, run, exported and packed again offline, as the lane identity (run 39347126). Copilot CLI runs on a getai.ghe.com runner with the job's own token (run 39346986), so part 4 can run there. Part 2 (run 39563486): the App Spec apply works as the lane identity, unattended and without `--allow-destructive`, and all it made landed in the solution and packs offline; FlowAgent reads and edits flows as the lane identity but cannot list, turn on, turn off or run them (HTTP 401 on both of its paths). Parts 3 and 4 are still to do. Findings that matter beyond this spike: Microsoft's server update changed the version stamp in the export (part 1 finding 6); a lane flow that uses the Dataverse connector needs a licence to run as the lane identity (the licence rule, part 1 finding 4); an App Spec app brings a missing dependency on a Microsoft platform solution into the export (part 2 finding 3); and the GitHub OIDC token lasts 5 minutes, so the driver must keep the Azure CLI signed in (part 2 finding 9).

Exit test (plan 11.1): we know where the skills stop for approval; the Web API flow runs, exports and packs again; we know whether the App Spec apply and FlowAgent work as the lane identity. If not: PARK at the approval point, flows by the Web API only, the App Spec apply and FlowAgent by day only. Added 13 November 2026 (Session 22, after 2433): count the MCP calls each session makes, to set the cap; try a way for the driver to count and retry calls; find which MCP errors are safe to retry.

## The parts

| Part | Exit test item | How | State |
|---|---|---|---|
| 1. Flow by the Web API | The flow runs, exports and packs again | Script on a runner, no AI: make, update, turn on, see a run, export, pack signed out and offline | **Pass** for a flow with no connector (run 39347126). A Dataverse flow turned on but was not run |
| 2. App Spec apply and FlowAgent as the lane identity | Whether they work as `getai-fl1-exec` | Script on a runner, no AI: `az login` with the federated token, then the model-apps build engine with `--non-interactive`, and FlowAgent's MCP server called by a small client | **App Spec: works** (run 39563486). **FlowAgent: in part**: reads and edits work; list, turn on, turn off and run are refused (HTTP 401) on both paths |
| 3. MCP count and retry | The cap's number, the shim, safe retries | A stdio shim in front of the Dataverse local proxy, driven by a scripted client; the count per session from part 4's sessions | Not started |
| 4. The skills in `copilot -p` | Where the skills stop for approval | Copilot CLI on a runner, with Microsoft's plugins pinned, `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1` and the lane's sign-ins | Copilot works on the runner (check below); skills not run yet |

## Decisions (Boroon, 18 November 2026)

- **Run Microsoft's plugins unread, for this spike only.** Pinned to the commits below, telemetry off, in the scratch repo `GetAI-IP/export-probe` and the `FactorySpike` scratch in `factory-lane-1` only. They are too big to read in full for a spike (the model-apps plugin is 36 MB; FlowAgent ships as one 2.7 MB bundle). The full read (rule 19, plan 8.3) still comes before any adoption.
- **Try one Copilot call first** for part 4, before waiting for spike 0.6.
- **Test flows:** a flow with no connector, and also try the existing Dataverse flow, to see what Microsoft does with a premium flow owned by the lane identity.

Pins read on 18 November 2026: `microsoft/power-platform-skills` at `05b634d` (17 November 2026), `microsoft/Dataverse-skills` at `79ec1e2` (16 November 2026), `@github/copilot` 1.0.113 (`sha512-x7P0jgiX...`, published 17 November 2026; the package is a 6 KB loader that pulls a platform binary, `@github/copilot-linux-x64` 1.0.113).

## Found before any run (read-only)

From the two plugin repos at their pins, and Microsoft's docs.

**How they sign in.**

- **The model-apps plugin (App Spec) gets every token from the Azure CLI:** `az account get-access-token` for the Dataverse URL and for `https://service.powerapps.com/` (`scripts/lib/dataverse-auth.js`). It also reads the active pac profile (`pac auth list`, `pac org who`). So `az login --service-principal --federated-token` with the job's GitHub OIDC token, plus the federated pac profile, should make it act as the lane identity. Untested.
- **FlowAgent (the power-automate plugin) also gets its tokens from the Azure CLI,** for `https://service.flow.microsoft.com`, and calls the Power Platform API (`*.environment.api.powerplatform.com/powerautomate/...`) with a fallback to the classic flow service (`api.flow.microsoft.com/providers/Microsoft.ProcessSimple/...`). It names a solution flow by its `workflowidunique`, and turns a flow on through Dataverse (`statecode` 1, `statuscode` 2). Its connection tools sign in separately, through an interactive MSAL sign-in, so they are user only: connections stay a bootstrap step or a PARK, as plan 5.6 has it.
- **The Dataverse skills' helper (`scripts/auth.py`)** tries a service principal secret or certificate first, then the Azure CLI. With no secret set, `az login` as the lane identity is the path.

**Where they stop for a person.**

- **`/app-builder` has an unattended mode.** `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1` (or `--non-interactive`) means "no user": it skips its questions, records each as "Unattended default: ..." in `workflow-log.md`, treats the lint, preview, design document and build dry-run as the approved plan, and goes on to apply. It halts rather than guess an ambiguous environment, app identity or destructive change. Being unattended never grants destructive authority: that needs `--allow-destructive`, which the skill says never to add unless it was "supplied independently". So the night's approval point is that flag: the driver never passes it, and a story that needs it PARKs. This fits plan 5.6 ("If the plan holds a one-way door ... the agent PARKs with the plan as evidence"). Untested headless.
- **`dv-solution` has no unattended mode.** It asks the user before it makes a publisher or picks a prefix, and asks the user to confirm the target environment before any export or import. At night the publisher and environment come from the lane config, and the driver, not the agent, exports.
- **Power Automate:** `create-flow` asks the user to confirm the design before it creates; `build-flow` is the autonomous one.
- In `copilot -p`, a tool the run did not pre-approve is denied, not asked about (GitHub's docs), and `--no-ask-user` removes the ask tool.

**Service principal flows (Microsoft's docs).**

- A service principal can own and run a solution flow; its connections need not be shared with it.
- **A premium flow owned by a service principal needs a licence:** a Process or per-flow licence on the flow, a flow group with a Process licence, or a licensed user named on the flow who is also a co-owner. Otherwise it "can be suspended". A flow that uses no premium connector is exempt. **The Dataverse connector is premium** (Microsoft's list of premium connectors). So any lane flow that uses Dataverse, which is most of them, cannot run in the lane, or in Test, owned by the lane identity, without one of those. A finding for the plan (5.9 `lcp-verify flow`, 5.14 licensing).
- Power Platform's service principal docs: flow APIs work for a service principal "in situations where a license isn't required".
- Flow runs of solution flows are kept in the Dataverse `flowrun` table (28 days by default), readable by Web API.

## Copilot CLI on a getai.ghe.com runner (run 39346986, 18 November 2026)

**It works.** `.github/workflows/copilot-check.yml` in `GetAI-IP/export-probe`: a job with `permissions: copilot-requests: write`, no OIDC, no secrets, `GH_HOST=getai.ghe.com`, the job's own `GITHUB_TOKEN`, Copilot CLI 1.0.113 installed from npm. `copilot -p "Reply with the single word: ready" -s --no-ask-user` answered `ready` and exited 0, in 2.5 seconds; the install took 7 seconds. No token-shaped string in the log.

So "Allow use of Copilot CLI billed to the organization" is on for `GetAI-IP`, as GitHub says it is by default when the CLI is on. `GetAI-IP` has a Copilot Business plan with no seats. Not known: which model answered, and where the request was billed. That is spike 0.6's question (ADO 2451), with OpenTelemetry and `--max-ai-credits`.

## Part 1: a flow by the Web API

`.github/workflows/tools.yml` and `probe/tools_probe.py` in `GetAI-IP/export-probe` (copies here), `flow` mode. As `getai-fl1-exec`, on pac 2.14.1:

1. Make "Factory spike timer flow" in `FactorySpike` with the solution header: a schedule trigger every minute and one Compose step, no connector, off.
2. Update its Compose step through the Web API.
3. Turn it on through the Web API, wait up to 7 minutes for a run (the `flowrun` table, and the flow service as FlowAgent calls it), turn it off.
4. Try to turn on the Dataverse flow from spike 0.18 ("Factory spike flow": a Dataverse action through a connection reference with no connection). If it turns on, start it through the flow service and turn it off again.
5. Export and unpack; compare with the reset commit; sign out; pack again normally and in a sandbox with no network; unpack the repack and compare.

`flow-undo` deletes the timer flow and turns the Dataverse flow off.

Local check before the run (18 November 2026, scratch harness, not committed): the probe ran end to end against a fake Dataverse and flow service, with the laptop's real pac 2.15.1 packing and unpacking the reset commit plus a timer flow. Every check passed except the no-network pack, which needs Linux.

### Findings (run 39347126, 18 November 2026)

1. **Part 1 passes for a flow with no connector.** As `getai-fl1-exec`, with no secret:
   - the Web API made the timer flow inside `FactorySpike` (the solution header was enough, as in 0.18), owned by the lane identity;
   - a `clientdata` update through the Web API took;
   - turning it on through the Web API worked (`statecode` 1, `statuscode` 2, HTTP 204), and the schedule fired at once: one run, `Succeeded`, started within a second of turning it on;
   - it turned off the same way;
   - the export held the flow as `Workflows/Factoryspiketimerflow-<id>.json` and its `.json.data.xml`, with the updated step, and one new root component in `Other/Solution.xml`;
   - the tree packed again after `pac auth clear`, and again in a sandbox with no network (`curl` exit 6), with the same members and root components as the export; unpacking the repack gave byte-identical files.
2. **The classic flow service accepts the lane identity's app-only token, at least to read runs.** A client-credentials token for `https://service.flow.microsoft.com` (the GitHub OIDC token as the assertion, no API permission on the app, no `roles` or `scp` in the token) listed the timer flow's runs at `api.flow.microsoft.com/providers/Microsoft.ProcessSimple/environments/<id>/flows/<workflowidunique>/runs` (HTTP 200). That is FlowAgent's fallback path; its main path, the Power Platform API, is not tried yet (part 2).
3. **Starting a manual-trigger flow through the classic flow service needs more than a token:** `POST .../triggers/manual/run` answered HTTP 401 `ClientScopeAuthorizationFailed: The x-ms-client-scope header must not be null or empty`. FlowAgent's code says the same: a manual or Power Apps trigger has to go through its own route. For part 2.
4. **The Dataverse flow turned on with no connection.** Spike 0.18's "Factory spike flow" (a Dataverse action through a connection reference that has no connection, and a premium connector) took `statecode` 1 through the Web API (HTTP 204) and read back as on. It was not run: finding 3 stopped the start, and nothing ran it in three minutes. It was turned off again; its exported files are unchanged from the reset commit. So Dataverse does not refuse to turn on a flow whose connection reference is empty, nor one that would need a licence, at least not at once. Whether Microsoft suspends it later, or fails its first run, is not known. Do not take "turned on" as "will run": `lcp-verify flow` must see a run (plan 5.9).
5. **The run showed in the flow service at once, but not in the Dataverse `flowrun` table** in the one read made (the probe stopped polling when the service showed the run). The environment keeps run history (`flowruntimetoliveinseconds` 2,419,200, 28 days). So the table may lag, or may not take runs of flows owned by an application user; not settled. Use the flow service to see runs until it is.
6. **Microsoft updated `factory-lane-1` between 10 and 18 November, and the export shows it.** `Other/Solution.xml` and `Other/Customizations.xml` now say `9.2.26102.148` where the reset commit says `9.2.26101.184` (`version`, `OrganizationVersion`, `CRMServerServiceabilityVersion`). Nothing else in the tree changed. Spike 0.18 (finding 9) expected this; now it is seen. So the reset's byte-for-byte proof (plan 5.4, step 5) and the lane drift check would fail after any service update unless the compare ignores these three attributes. Plan 5.4 already says the canonical form must ignore the stamp if it changes; this is the evidence. For 2577 and the drift check.
7. **Timings on a hosted runner:** make the flow 11 seconds (the first Web API write, sign-in included), update 5, turn on 2, first run within 1, turn off 3, export 16, unpack 1, pack 1. The whole job 4.4 minutes, of which three were the wait on the Dataverse flow.
8. The OIDC subject and the sign-in were as in 0.18 and 0.19 (`Connected as` the app ID). No token-shaped string in either run's log.

What this does not show: a flow with a Dataverse action running as the lane identity (it needs a connection and a licence, finding 4 and the licence rule above); a flow made by FlowAgent or the App Spec apply (part 2).

## Part 2: the App Spec apply and FlowAgent as the lane identity

`tools.yml` and `probe/tools_probe.py` in `GetAI-IP/export-probe` (copies here), `part2` mode, Session 26 (19 November 2026). No AI in it: a script drives Microsoft's tools the way a skill would.

**Set-up.** The job fetches `microsoft/power-platform-skills` at `05b634d` (only `plugins/model-apps` and `plugins/power-automate`, checked against the full commit ID), sets Node 22 (the build engine's bundle was built on it), and turns the plugins' telemetry off three ways: each plugin's own kill switch (`"disabled": true` in its `scripts/lib/telemetry/ikey.json`, which stops the local mirror too), each plugin's opt-out (`POWER_PLATFORM_SKILLS_TELEMETRY_<PLUGIN>_OPTOUT=1`), and FlowAgent's engine switches (`FLOWAGENT_TELEMETRY=0`, `POWER_PLATFORM_SKILLS_TELEMETRY=0`); the Azure CLI's own telemetry is off too. `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1` is set for the whole job. pac signs in as before (federated profile).

**Steps, as `getai-fl1-exec`:**

1. `az login --service-principal --federated-token <the job's GitHub OIDC token> --allow-no-subscriptions`, with the same federated credential pac uses (`export-probe-fl1-exec`). Then `az account show`, and one `az account get-access-token` for each resource the two plugins ask for (Dataverse, `service.powerapps.com`, `service.flow.microsoft.com`) and the Power Platform API, so each token is cached while the OIDC token is fresh. The probe signs in again just before FlowAgent. The OIDC token is passed to `az` only, never logged; every log line goes through a filter that removes token-shaped strings, and a last step deletes any output file that still holds one before the artifact upload.
2. **The App Spec.** A tiny spec in `FactorySpike` (publisher prefix `fspk`): one new table "Spike app row" (`fspk_spikeapprow`, a name column and a text column), its main form (auto layout), one view, and the app "Factory spike app" with one navigation entry. Then what `/app-builder` runs when no user is waiting: `lint-app-spec.js --json` (errors stop it), `build-model-app.js` as a dry run with `--non-interactive` (in unattended mode the dry run is the approval), then `--apply --verify --publish --non-interactive`. Never `--allow-destructive`. The probe reads the solution's components before and after.
3. **FlowAgent.** Its MCP server started as its own `.mcp.json` starts it (`node -e` with a small loader that imports `server/mcp.mjs`, `PLUGIN_ROOT` set), driven by a small stdio MCP client in the probe that counts every `tools/call`. On the timer flow from part 1: `whoami`, `doctor`, `list_flows`, `get_flow`, `get_flow_context`, `update_flow` (the Compose step to "v3"), `run_flow` while it is off, `publish_flow` (turn on), `run_flow` with `wait`, `get_run_history`, `disable_flow`. FlowAgent tries the Power Platform API (`<env>.environment.api.powerplatform.com`) first and falls back to the classic flow service only when that host does not resolve or answers `InsufficientCdsPermissions`; so a second server, with `PA_PPAPI_BASE_URL` pointed at a host that never resolves (`.invalid`), repeats the list, get, update ("v4"), turn on, run, runs and turn off on the fallback. The probe turns the flow off through the Web API if a session leaves it on.
4. Export and unpack; compare with the reset commit; sign out; pack again normally and with no network (as in part 1).

**Local check before the run** (19 November 2026, scratch harness, not committed). None of Microsoft's code ran on the laptop (the decision limits it to the scratch repo): stand-ins took the place of the build engine, the lint and FlowAgent's server, with a fake Dataverse, token service, OIDC endpoint and `az`, and a stand-in `pac` that passed pack and unpack to the laptop's real pac and never touched its sign-ins. Checked: both sign-ins kept the OIDC token out of every log and record; the stand-in engine saw `--non-interactive`, the unattended and telemetry settings, and never `--allow-destructive`; the MCP client answered a request from the server and skipped its notifications; the forced fallback was seen; the flow ended off; the scan deleted a planted token file and kept the rest. The plugin fetch step ran for real on the laptop (git only): the head is the pin and both kill switches set.

### Findings (run 39563486, 19 November 2026)

1. **The App Spec apply works as the lane identity, for this tiny spec.** Lint 0.1 seconds (four warnings, no errors). Dry run 1.7 seconds: a live plan to reuse the solution and create the table, the column, the view, the form, the app and its site map, and a generated icon. Apply 109 seconds, `--verify` 13 of 13 present, customizations published. In unattended mode it asked nothing and needed no `--allow-destructive`. It found `FactorySpike` and reused it (it warned that it "will UPDATE the existing app"; the warning is about the solution).
2. **Everything it made landed in `FactorySpike`.** In Dataverse the solution gained the table, the web resource, the site map, the app and two app settings (component type 10090). The export gained:
   - `Entities/fspk_spikeapprow/`: `Entity.xml`, `RibbonDiff.xml`, four forms (the spec's main form, and Dataverse's own main, card and quick create forms for a new table) and seven views (the stock ones, one of them carrying the spec's view, finding 4);
   - `AppModules/fspk_factoryspikeapp/AppModule.xml` and `AppModuleSiteMaps/fspk_factoryspikeapp/AppModuleSiteMap.xml`;
   - `WebResources/fspk_factoryspikeapp_icon` and its `.data.xml`;
   - five new root components in `Other/Solution.xml` (the table, the web resource, the site map, the app, and part 1's timer flow), and changes to the four files in `Other/Relationships/` for the new table's relationships to business unit, owner, user and team.

   Nothing left the solution. Whether the engine made anything outside it was not checked (spike 0.19's finder would tell).
3. **The export now carries missing dependencies.** The engine wrote two app settings into `AppModule.xml` (`AppChannel` 1, `HeaderAndNavigationRefresh` 2). Their definitions belong to Microsoft's `msdyn_AppFrameworkInfraExtensions` (1.0.0.28, from the PowerAppsAppFramework package), so `Other/Solution.xml` has a `<MissingDependencies>` block for the first time. An import into an environment without that solution would fail. Microsoft ships it with the model-driven app framework, so `factory-test` very likely has it [inference, not checked]. For the gate (2538): the import into Test must take it, and the manifest check and the Merge Danger rules must not read a missing dependency on a Microsoft platform solution as a fault.
4. **The spec's view merged onto the table's stock view.** "Active spike app rows" is also the name Dataverse gives a new table's default view, so the engine updated that view's columns and description instead of making a second view. The lint warned before the build, and the build warned that filters and sort are not reapplied to an existing view. A spec should not name a view "Active <plural name>".
5. **The app opens for two roles only.** `AppModule.xml` maps it to two roles (which two was not checked). With no `personas[]`, the lint said a new app gets System Administrator only. A story whose users are not makers needs `personas[]` or `roleGrants[]` in its spec, which is security work (size L under the work sizes).
6. **FlowAgent works as the lane identity for reads and edits, but not to list, turn on, turn off or run a flow.** On both paths:

   | Works | Refused: HTTP 401 `ClientScopeAuthorizationFailed` |
   |---|---|
   | `whoami`, `doctor`, `get_flow`, `get_flow_context`, `update_flow`, `get_run_history` | `list_flows`, `publish_flow` (turn on), `disable_flow` (turn off), `run_flow` (also while the flow was off) |

   The error is part 1's finding 3: the flow service refuses these calls on an app-only token without an `x-ms-client-scope` header, and FlowAgent does not send one. FlowAgent's own fallback to turning a flow on through Dataverse starts only on a different error (`CannotStartUnpublishedSolutionFlow`), so it does not help here. Turning a flow on and off through the Web API works (part 1). So at night, the lane identity can read and edit flows with FlowAgent and turn them on and off by the Web API, but nothing tried starts a run on demand; a flow runs only on its own trigger (a schedule flow fires when it is turned on, part 1).
7. **`update_flow` writes a solution flow through Dataverse,** not the flow service, which is why it works: 10.3 seconds the first time, 3.7 the second. `get_flow_context` found the flow in `FactorySpike`, not managed. FlowAgent names the flow by its `workflowidunique`. The export holds the second update.
8. **Both paths were used.** The Power Platform API answered as `Microsoft.Flow/environments/flows`, so the per-environment host resolves for `factory-lane-1`. With that host pointed at `.invalid`, FlowAgent logged "Falling back to classic Flow RP API" and answered as `Microsoft.ProcessSimple/...`. `get_run_history` read part 1's run on both paths.
9. **The GitHub OIDC token lasts 5 minutes, and the Azure CLI uses it to get every new token.** The tokens `az` got last one hour. That was enough here, with a fresh sign-in before each part and every token asked for at once. A night session that runs past an hour, or that needs a token for a new resource more than 5 minutes after signing in, would fail to get one. So the driver must keep `az` signed in: sign in again with a fresh OIDC token before each tool step, or on a timer. For part 4 and the Stage 3 driver.
10. **The Azure CLI as the lane identity:** `az login` took 1 second. `az account show` gave a tenant-level account (no subscription) for a service principal, the lane app, in the right tenant. Tokens for Dataverse (with and without the trailing slash), `service.powerapps.com`, `service.flow.microsoft.com` and `api.powerplatform.com` were all issued app-only (`idtyp` app, no roles).
11. **The tree still packs offline.** Now 42 files: packed signed out and with no network, with the export's members and root components, and the round trip was byte-identical.
12. **Telemetry:** both kill switches read `disabled: true` at run time, and the opt-outs were set. Whether anything was sent anyway was not measured (no network capture). The token scan found nothing to remove.
13. **Counts and timings:** FlowAgent offered 62 tools; the two sessions made 11 and 8 tool calls (FlowAgent's, not Dataverse MCP's, so no Copilot Credits; part 3 counts those). The whole job took 3.6 minutes: the App Spec apply 109 seconds, the FlowAgent sessions 22 and 7, the export 26.

What this does not show: a larger spec (relationships, choices, roles, pages); an App Spec change to an existing app or table, which is what most night stories would be; whether the app imports into Test; FlowAgent's `create_flow` (its connection tools are user only, Session 25); a run started on demand as the lane identity by any route.

**Where part 2 leaves the exit test.** The App Spec apply works as the lane identity, so it can run at night, with the driver never passing `--allow-destructive`. FlowAgent works in part: reading and editing flows yes; listing, turning on and off, and running no. The plan's fallback ("flows by the Web API only") still holds for turning flows on and off, and for seeing a run. The verdict and any plan edits come at the end of the spike, at Boroon's word.

## Run order and results

Runs start with `GH_HOST=getai.ghe.com gh workflow run <file> -R GetAI-IP/export-probe --ref main`, with `-f mode=... -f tenant_id=... -f app_id=... -f env_url=https://factory-lane-1.crm6.dynamics.com/` for `tools.yml`.

| Run | ID | Workflow, mode | Result |
|---|---|---|---|
| 1 | 39346986 | copilot-check | Pass: `ready`, exit 0 |
| 2 | 39347126 | tools, flow | **Pass.** Timer flow made, updated, on, ran (`Succeeded`), off, exported, packed signed out and offline, round trip byte-identical. The Dataverse flow turned on, was not started (HTTP 401, finding 3), and was turned off. 4.4 minutes |
| 3 | 39563486 | tools, part2 | **App Spec works; FlowAgent in part** (13 of 17 checks pass). `az login` as the lane identity; App Spec lint, dry run and apply (109 s, verify 13 of 13); table and app in the export; FlowAgent's update on both paths in the export; packed signed out and offline. Failed: FlowAgent's list, and its run on both paths (HTTP 401, part 2 finding 6). 3.6 minutes |

## Left to do

1. ~~**Part 2**~~: done in Session 26 (run 39563486), above.
2. **Part 3:** a stdio shim in front of `dataverse mcp` (the local proxy, pinned) that counts `tools/call`, stops at a cap and retries a failed call up to three times; driven by a scripted client with reads, a create and forced failures; plus which errors the proxy returns for each.
3. **Part 4:** Copilot CLI on the runner with the pinned plugins, `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1`, the lane's pac and `az` sign-ins, and the shim in front of Dataverse MCP: one small App Spec story and one small flow story. Record where each stops, which tools it asked for, and the MCP calls per session (the cap's first number). From part 2: keep `az` signed in for the whole session (finding 9); expect FlowAgent's list, turn on, turn off and run tools to fail (finding 6); an App Spec story on the existing app is the update path, not yet tried.
4. Then the exit test verdict, the plan edits at Boroon's word, and the scratch deleted at his word.

## Scratch

New in this spike, kept until it ends, then deleted with 0.18's and 0.19's at Boroon's word:

| Thing | Where | How to delete |
|---|---|---|
| `tools.yml`, `copilot-check.yml`, `probe/tools_probe.py` and their runs | `GetAI-IP/export-probe` | Go with the repo (0.18's list) |
| Cloud flow "Factory spike timer flow", in `FactorySpike`, off (made by run 39347126; its Compose step changed by FlowAgent in run 39563486) | `factory-lane-1` | `tools.yml`, `mode=flow-undo`; 0.18's `teardown` does not know it, so run this first |
| The App Spec's table "Spike app row" (`fspk_spikeapprow`) with its forms and views, the app "Factory spike app" (`fspk_factoryspikeapp`) with its site map and two app settings, and the icon web resource `fspk_factoryspikeapp_icon`, all in `FactorySpike` (made by run 39563486) | `factory-lane-1` | Not written yet: a `part2-undo` mode by the Web API (the app, then the site map, the table and the web resource), run before 0.18's `teardown`. **Do not use Microsoft's `teardown-model-app.js`:** its last step deletes the solution the spec names, which is `FactorySpike` |
| FlowAgent's own backups of the flow (it keeps one before each change) | the runner's home folder | Gone with the runner |

Spike 0.18's "Factory spike flow" was turned on and off again by run 39347126; it is off, and its files are as in the reset commit.

0.18's and 0.19's scratch is still kept (their READMEs).
