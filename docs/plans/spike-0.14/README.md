# Spike 0.14: skills and lane tools headless, as the lane identity

Plan section 11.1, row 0.14 (ADO 2461). Session 25, 18 November 2026 (Sydney time), Session 26, 18 to 19 November 2026, Session 27, 19 November 2026, and Session 28, 20 to 21 November 2026, laptop sessions. Started two days after its Mon 16 to Tue 17 Nov slot; all four parts run by Saturday 21 November. The exit test verdict and the plan edits wait on Boroon (proposed at the end of part 4).

**So far (19 November 2026):** part 1 passes for a flow with no connector: made, updated, turned on, run, exported and packed again offline, as the lane identity (run 39347126). Copilot CLI runs on a getai.ghe.com runner with the job's own token (run 39346986), so part 4 can run there. Part 2 (run 39563486): the App Spec apply works as the lane identity, unattended and without `--allow-destructive`, and all it made landed in the solution and packs offline; FlowAgent reads and edits flows as the lane identity but cannot list, turn on, turn off or run them (HTTP 401 on both of its paths). Part 3 (run 39749076): a stdio shim in front of the Dataverse CLI's local proxy counts every MCP call, holds a cap and retries; a retried create whose answer was lost **writes twice**, and a create that carries its own row ID does not; the bill shows every call that reached Dataverse, tool errors included (checked 21 November). Part 4 (run 40121696, 21 November): Copilot CLI ran Microsoft's skills headless as the lane identity, on `claude-sonnet-5.5`, with the shim in front of Dataverse MCP. **The flow story passed** (FlowAgent edited the Compose step; its `list_flows` failed with 401 again, and the agent found the flow with one Dataverse MCP read instead). **The App Spec story stopped at the approval point:** the build engine refuses an unattended apply to an existing app without `--allow-destructive`, even for one new column, and the agent stopped and wrote a clear handoff. MCP calls per session: 0 and 1. AI credits: 29.7 and 12.7. No tool was denied. Findings that matter beyond this spike: Microsoft's server update changed the version stamp in the export (part 1 finding 6); a lane flow that uses the Dataverse connector needs a licence to run as the lane identity (the licence rule, part 1 finding 4); an App Spec app brings a missing dependency on a Microsoft platform solution into the export (part 2 finding 3); and the GitHub OIDC token lasts 5 minutes, so the driver must keep the Azure CLI signed in (part 2 finding 9).

Exit test (plan 11.1): we know where the skills stop for approval; the Web API flow runs, exports and packs again; we know whether the App Spec apply and FlowAgent work as the lane identity. If not: PARK at the approval point, flows by the Web API only, the App Spec apply and FlowAgent by day only. Added 13 November 2026 (Session 22, after 2433): count the MCP calls each session makes, to set the cap; try a way for the driver to count and retry calls; find which MCP errors are safe to retry.

## The parts

| Part | Exit test item | How | State |
|---|---|---|---|
| 1. Flow by the Web API | The flow runs, exports and packs again | Script on a runner, no AI: make, update, turn on, see a run, export, pack signed out and offline | **Pass** for a flow with no connector (run 39347126). A Dataverse flow turned on but was not run |
| 2. App Spec apply and FlowAgent as the lane identity | Whether they work as `getai-fl1-exec` | Script on a runner, no AI: `az login` with the federated token, then the model-apps build engine with `--non-interactive`, and FlowAgent's MCP server called by a small client | **App Spec: works** (run 39563486). **FlowAgent: in part**: reads and edits work; list, turn on, turn off and run are refused (HTTP 401) on both paths |
| 3. MCP count and retry | The cap's number, the shim, safe retries | A stdio shim in front of the Dataverse local proxy, driven by a scripted client; the count per session from part 4's sessions | **Shim works** (run 39749076): counts, cap and retries hold. Safe to retry: reads, and a create with its own ID. Not safe: a plain create (it wrote twice). The cap's number waits on part 4 |
| 4. The skills in `copilot -p` | Where the skills stop for approval | Copilot CLI on a runner, with Microsoft's plugins pinned, `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1`, the lane's sign-ins and the shim in front of Dataverse MCP; two tiny stories | **Known** (run 40121696): the App Spec skill stops at the apply on an existing app (it needs `--allow-destructive`, which the driver never passes); FlowAgent's skill edits with its own dry run and needs no person. Flow story passed; App Spec story parked itself as it should. MCP calls 0 and 1 |
| 4b. Option (b) for an existing app | Whether an App Spec story on an existing app can run at night without the App Spec apply | Copilot CLI as in part 4: the column by Dataverse MCP, the form and view by the Web API through a trusted helper, then publish; export before and after | **Works** (run 40126806, Session 29): all 18 checks; no `--allow-destructive`, the engine not run; only the three expected files changed; packed offline. 48 s, 15.7 credits, 1 MCP call |

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

## Part 3: the MCP count-and-retry shim

`probe/mcp_shim.py`, and the `part3` mode of `tools.yml` and `probe/tools_probe.py`, in `GetAI-IP/export-probe` at `e598595` (copies here). Session 27, 19 November 2026. A probe for the Stage 3 driver (plan 5.11, 5.14), not a gate script. No AI, no pac and none of Microsoft's plugins: only the Dataverse CLI's local proxy.

**The shim.** `python3 -I mcp_shim.py --cap N --log FILE [options] -- dataverse mcp <url>`. It sits between an MCP client, on its own stdin and stdout, and the proxy it starts, and passes newline-delimited JSON-RPC both ways. It touches only `tools/call`:

- **Count.** Each call, and each attempt it sends to the proxy. An attempt goes under the shim's own ID (`shim-<n>`), so a late answer is never taken for a retry's answer.
- **Cap.** The cap counts attempts sent, retries included, because each one that reaches Dataverse is billed. An attempt past the cap is refused with JSON-RPC error -32010 and a message that says so, and nothing goes to the proxy. That is a stop, PARK `budget`.
- **Retry.** A failed attempt is retried up to 3 times, after 1, 2 and 4 seconds. Failed means a JSON-RPC error, a result with `isError`, no answer within 120 seconds, or an answer the probe told the shim to drop. A call that still fails goes back to the client with its last error, and is a stop, PARK type `tool_failure` (proposed below).
- **Stop.** After the first stop the shim refuses every later call (-32011), as the driver would end the session there. `--keep-going` (probe only) lets one session show several failures.
- **Log.** Every call, attempt, answer, retry, refusal, late answer and stop, as JSON lines. The proxy's stderr goes to its own file, and each failed attempt's stderr lines are copied into that attempt's record, because the proxy hid an upstream cause behind -32603 in spike 0.3 (finding 3). Running counts go to a summary file and the first stop to a stop file, for a driver to read. Token-shaped strings are removed from every line.
- **Fault, probe only.** `--fault drop-answer:<tool>:<n>` throws away the proxy's answer to the first attempt of the n-th call of a tool and treats it as no answer, so a retry follows.

Not handled: a client's `notifications/cancelled` for a call (it passes through with the client's ID, which the proxy does not know); starting the proxy again after it exits.

**The run.** As `getai-fl1-exec`: the Dataverse CLI 1.0.88 from spike 0.3's pinned tarball and hash, signed in with its own `dataverse auth create --githubFederated` (it does not share pac's profile), telemetry off. Then three short sessions of a scripted client, each with its own shim and proxy, against spike 0.18's table `fspk_spikeitem` in `FactorySpike`:

| Session | Cap | Calls, in order |
|---|---|---|
| A | 16, `--keep-going` | read `organization`; read the spike table; create one row; read it back; a bad query (`SELEKT ...`); a create on a table that does not exist (`fspk_nosuchtable`) |
| B | 2 | a read; the bad query, whose retry would be the third call; one more read |
| C | 8, two faults | a create whose first answer is dropped; a create with its own row ID (`fspk_spikeitemid`) whose first answer is dropped |

Every row is named `spike-0.14 part3 (...)`. Before and after the sessions, the Web API deletes every row with that prefix that the lane's application user made, and checks that none is left. Session C's second create was not in the brief: it tests one way to make a create safe to retry, for 4 more calls (0.4 credit).

**Local check before the run** (19 November 2026, scratch harness, not committed). None of Microsoft's code ran on the laptop: a fake `dataverse mcp` (stdio JSON-RPC, rows kept in a file), a fake Web API, token service and OIDC endpoint. The probe ran end to end and all 10 checks passed; the dropped-answer create wrote twice and the own-ID create once; the clean-up deleted a planted leftover and kept a row made by another user. A second set of 18 checks drove the shim alone, three rounds: pass-through keeps the client's IDs and is not counted; no answer in time is retried and both late answers are logged; a proxy that dies is not retried and later calls are refused; three calls sent at once against a cap of 2 send exactly two; a request from the server reaches the client and its answer gets back; a token in a call never reaches the log; a cap of 0 sends nothing. The harness found two bugs, fixed before the run: the summary file overwrote the retry count with the retry limit, and two calls ending at once raced on the summary's temporary file.

### Findings (run 39749076, 19 November 2026)

1. **The shim works in front of the real proxy.** `initialize` and `tools/list` passed through (server `dataverse 1.0.88.0`, protocol `2025-06-18`), and so did the reads and the create. In all three sessions the counts in the summary matched the log. Each call took 0.1 to 1.5 seconds. The whole step took 40 seconds, most of it the shim's waits between retries.
2. **The cap held.** Session B (cap 2) sent exactly 2 calls. The bad query's retry, which would have been the third, was refused before it was sent, and so was the read after it. Both answers named the cap and PARK `budget`. Because the cap counts retries, no retry can pass it.
3. **Every failure came back as a tool result with `isError`,** not as a JSON-RPC error, each with a correlation ID:

   | Forced failure | What came back, on each of 4 attempts | Safe to retry? |
   |---|---|---|
   | Bad query (`SELEKT ...`) | "An unexpected error occurred. (correlation ID: ...)" | Safe, but pointless: the same answer every time |
   | Create on a table that does not exist | "Could not find an entity with name fspk_nosuchtable and id 00000000-... (2645799)" | Safe (nothing was written), but pointless |
   | A call past the cap | The shim's own refusal, -32010; nothing sent | No: it is the stop |
   | Create, first answer dropped | The retry: "Created record with ID <a new ID>" | **No: it wrote twice** |
   | Create with its own ID, first answer dropped | The retries: "Cannot insert duplicate key." | **Yes: it wrote once** |

4. **A retried create whose answer was lost writes twice.** The first attempt made a row, the shim threw its answer away, the retry made a second row with a new ID, and the client saw only the second. So the driver must never retry a plain create after no answer.
5. **A create that carries its own row ID is safe to retry.** `create_record` took `fspk_spikeitemid` in `item`, and Dataverse used it. Each retry was refused with "Cannot insert duplicate key", and one row exists. So a shim can make every create safe to retry by adding an ID when the agent gives none, and take "duplicate key" on a retry as success. As run, the shim retried the duplicate answer three times and called it a failure: 3 calls wasted and a stop that was not needed.
6. **The proxy's stderr holds no cause for these failures.** It wrote one line per call, the same unencrypted-cache warning each time (spike 0.3 finding 5), and nothing else. The cause is only in the tool result's text. Spike 0.3's 403 reached stderr because the session start failed, not a tool call. So the night's trace must keep each tool result's text and correlation ID (rule 16); the stderr alone is not enough.
7. **A bad query tells the agent nothing:** "An unexpected error occurred", with no reason. An agent could loop on it. `read_query`'s own description says to find the table with `search` and its columns with `describe` first; the agent instructions should say the same, and to stop after one failed query of the same shape.
8. **Deterministic failures were retried for nothing.** The bad query and the missing table gave the same answer four times: 6 wasted calls in session A. Under the rule as decided (retry any failed call three times, then stop), one typo by the agent would end the night's session as a PARK.
9. **The tool list grew since spike 0.3.** There are 16 tools, not 15: `invoke_api` is new. `create_record` now also takes `items`, a batch of up to 25 records in one call. If a call is billed once whatever it holds, a batch is cheaper, and a lost answer to a batch would write up to 25 rows twice [inference]. Agent instructions must read the tool list (spike 0.3 finding 12).
10. **The billed count, to match later.** 20 calls reached Dataverse, and all were answered: 6 succeeded, 12 were tool errors, and 2 succeeded but their answers were dropped by the shim. The shim refused 2 and sent nothing for them; `initialize` and `tools/list` were made once per session. In the admin centre (Licensing, Copilot Studio, Environments, `factory-lane-1`, Copilot Credits capacity), 19 November 2026 should show **20 billed rows of 0.1 (2.0 credits)** if every answered call is billed, or **8 rows (0.8 credit)** if only the successes are. The run was between 09:56:06 and 09:56:46 UTC (20:56 Sydney time). Part 2 used FlowAgent, not Dataverse MCP, so nothing else should be there that day.

   **Checked 21 November 2026** (Session 28, read-only, Boroon's sign-in, the built-in browser; the data was last refreshed 20 November, 08:00): `factory-lane-1` shows **26 rows** of "Dataverse MCP Server", each 0.1 billed and 0 non-billed, prepaid consumed **2.6** Copilot Credits, last updated 19 November. Spike 0.3's 6 rows made 0.6 on 6 November, so part 3 added **20 billed rows (2.0 credits): every call that reached Dataverse is billed, tool errors and answers the shim dropped included.** The 2 calls the shim refused, and `initialize` and `tools/list`, are not. So a retried call costs what a new one does, and the cap must count attempts sent, as the shim does. (On 20 November, the data was last refreshed 18 November and still showed 6 rows.)
11. **Clean-up.** No leftover rows before. After, the Web API found 4 rows by the lane's application user ("create", two "answer dropped", "own ID"), deleted each (HTTP 204), and found none left.
12. No token-shaped string in the log or the artifact. The Dataverse CLI's profile was removed at the end.

What this does not show: the calls a real night session makes (part 4 counts them, for the cap's number); a transient failure (none came: no timeout, no throttling, no JSON-RPC error); whether a throttled call comes back as `isError` or as an error; updates and deletes retried; a batch create retried; how Copilot CLI shows the shim's refusal to the model (part 4).

### Decided for the Stage 3 driver (Boroon, 20 November 2026)

Proposed in Session 27 and **accepted by Boroon on 20 November 2026**, both the retry rule and the PARK type. They replace "a failed MCP call is retried up to three times" in plan 5.14, and fill the gap plan 5.11 left ("the type for a failed call is for the driver spec"). The plan text is edited with the spike's other plan edits, at Boroon's word; until then the plan still says the old rule.

**Retry only where it is safe and can help.** Findings 4, 5 and 8 say "retry any failed call three times" is wrong both ways: it wastes calls on the agent's own mistakes, and it can write twice.

| Failure | Retry? | Then |
|---|---|---|
| A tool result with `isError`: the tool ran and said no (bad query, missing table, duplicate key) | No | Back to the agent as it is, to fix its call. Counted against the cap. Not a PARK |
| A tool result whose text says throttled, or 429 or 503 (not seen yet) | Up to 3, waiting as long as the answer asks | PARK `tool_failure` if it still fails |
| No answer in time, a JSON-RPC error from the proxy, or the proxy exits, on a read | Up to 3, with back-off; start the proxy again first if it exited | PARK `tool_failure` if it still fails |
| The same, on a create, update or delete by row ID | Up to 3. On a retry, "duplicate key" for a create, or "not found" for a delete, counts as success | PARK `tool_failure` if it still fails |
| The same, on a create without a row ID, or a batch | Never happens: the shim adds a row ID to each record before the first attempt (the primary key's name from the Web API's `EntityDefinitions`) | |

**A PARK type for a call that still fails: `tool_failure`** (the cap stays `budget`). Its `park.json` instruction names the tool, its arguments, the last answer's text and correlation ID, and the shim log in the night's trace. It joins plan 5.11's type list and Appendix D's `Custom.ParkType` picklist; the name is product-neutral (rule 18).

**The cap counts attempts sent, retries included,** as the shim does, because each one is billed. The number itself comes from part 4.

## Part 4: the skills in `copilot -p`

`tools.yml` (job `part4`), `probe/tools_probe.py` (`part4` mode), `probe/mcp_shim.py` and `probe/copilot/package.json` with its `package-lock.json`, in `GetAI-IP/export-probe` (copies here, the lockfile in `copilot/`). Session 28, 20 to 21 November 2026. Run 40121696 ran at `2f194da`; `4641e57` then fixed two of the probe's checks after the run (finding 3 and 6: they now read only the session's tool calls), checked on that run's events.

### The shim, changed to the accepted rule

`mcp_shim.py` now follows the rule Boroon accepted on 20 November (the table under part 3):

- **A tool result with `isError` goes back at once:** no retry, no stop, counted against the cap. The one exception is a result whose text says it was throttled (429, 503, "too many requests", "exceeded the limit"): it is retried up to 3 times, waiting as long as a `Retry-After` in the text asks (at most 300 seconds).
- **No answer in time, a JSON-RPC error, or the proxy exiting** is retried up to 3 times with back-off, but only for a call that is safe to repeat: a read (`read_query`, `search`, `describe`, `file_download`), an update or delete by row ID, or a create whose every record carries a row ID. If the proxy exited, the shim starts it again first and replays the client's `initialize` (at most 3 restarts).
- **Every create gets a row ID before its first attempt.** For each record with none, in `item` or in the batch `items`, the shim adds the table's primary key with a new GUID. The key's name comes from the Web API's `EntityDefinitions`: the probe reads every table's `PrimaryIdAttribute` before the session into a file (`--keys-file`), and the shim asks the Web API for a table made during the session (`--webapi`, with a token from `az`, never logged). A create the shim could not give an ID is sent as it is, but not repeated.
- **On a retry, "duplicate key" for a single create, or "does not exist" for a single delete, counts as success:** the earlier attempt landed. The shim answers the client "Created (or Deleted) record with ID ...", saying why. For a batch it cannot tell which records landed, so that is a stop.
- **A call that still fails is a stop, PARK `tool_failure`,** and so is a call that is not safe to repeat whose answer was lost. The stop file names the tool, the last answer's text and its correlation ID. The cap stays PARK `budget`.
- Also new: the tool names from `tools/list` are logged as they pass, every answer's correlation ID is logged, and a client's `notifications/cancelled` is sent on under the call's current attempt ID.

Two choices the accepted rule did not settle, made the safe way here, **confirmed by Boroon on 21 November 2026** (they go into plan 5.14 with the rule):

1. **Tools outside reads and row writes are never repeated:** `create_table`, `update_table`, `delete_table`, the file upload tools, `invoke_api`, the skill tools, and any tool the shim does not know. A lost answer to one of them is a PARK `tool_failure`. (The Dataverse skills' own advice for a timed-out `create_table` is to `describe` before trying again, which an agent could do by day.)
2. **A batch write whose answer was lost and whose retry then says no** is a PARK, not a guess.

**Local check** (21 November 2026): Session 27's fake proxy was gone with its scratchpad, so it was rebuilt from the part 3 description, answering with the texts the real proxy gave in run 39749076. It can do the work and then never answer, never answer, exit, answer a JSON-RPC error, or answer throttled, on the n-th attempt of a tool. A fake Web API answered `EntityDefinitions`. 21 checks passed:

| Check | Result |
|---|---|
| A read passes; `tools/list` is logged (16 tools) | 1 attempt |
| A bad query comes back as `isError` | once, no retry, no stop; the next call passes; correlation ID logged |
| A create with no ID | the shim adds `fspk_spikeitemid`; the row has that ID |
| A create whose answer is lost (fake or shim drop) | retried, "duplicate key", answered as created: **one row** |
| A delete whose answer is lost | retried, "does not exist", answered as deleted |
| An update after a JSON-RPC error | retried once, applied |
| The proxy exits during a read | started again, `initialize` replayed, retried, later calls pass |
| A throttled read with `Retry-After: 1` | waits a second, retried, passes |
| A read that fails four times | PARK `tool_failure`; the next call refused (-32011) |
| `create_table` whose answer is lost | not repeated; PARK `tool_failure` |
| Cap of 2 | 2 attempts; the third refused, PARK `budget` |
| A batch create with no IDs | an ID added to each record |
| A batch create whose answer is lost | retried, "duplicate key", PARK `tool_failure` (`batch-unconfirmed`); 2 rows, not 4 |
| A create on a table `EntityDefinitions` does not know | sent with no ID; its lost answer is not repeated |
| A missing table on the first try | `isError` back to the client, no stop |
| `item` sent as JSON text | the ID is added inside the text |
| The agent's own ID, in another letter case | kept; no second ID added |
| A token from the token command or in the proxy's stderr | never in any log; the Web API got it |
| The summary's counts | match the log |
| A cancel from the client | sent on as `shim-1` |

The part 3 mode's own checks were written for the old rule (it expects the bad query tried four times), so it would now fail them; part 3 is not run again.

### The run

One job (`part4`), its own `copilot-requests: write` and `id-token: write`, on a hosted runner, as `getai-fl1-exec`:

1. **Installs, all pinned:** pac 2.14.1; the Dataverse CLI 1.0.88 from spike 0.3's hash-checked tarball; **Copilot CLI 1.0.113 by `npm ci --ignore-scripts` from a lockfile** (10 packages, each checked against its integrity value; `@github/copilot` matches Session 25's pin, `@github/copilot-linux-x64` is `sha512-VrNX0yu1...`); `power-platform-skills` at `05b634d` (only `plugins/model-apps` and `plugins/power-automate`) and `Dataverse-skills` at `79ec1e2` (only `.github/plugins/dataverse`), each checked against the full commit ID. Telemetry off: each plugin's kill switch and opt-outs as in part 2, `DATAVERSE_TELEMETRY_OPT_OUT=1`, `COPILOT_TELEMETRY_DISABLED=true` and `--disable-client-telemetry`. `COPILOT_AUTO_UPDATE=false`; `COPILOT_PLUGIN_DIR_ONLY=true`, so only the three plugin folders load; `COPILOT_HOME` is a fresh folder. `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1` for the whole job.
2. **The primary keys:** every table's `PrimaryIdAttribute` from `EntityDefinitions`, into a file for the shim.
3. **A model check:** one prompt ("Reply with the single word: ready") with plan 5.2's model, `claude-sonnet-5.5`. If the CLI refuses the name, the stories run on its default model.
4. **Per story, fresh sign-ins first** (part 2 finding 9): `pac auth create --githubFederated`, `dataverse auth create --githubFederated` and `az login --federated-token`, each with a new GitHub OIDC token, then every `az` token the plugins ask for, fetched at once. Before the first story the probe checks whether `pac`, the Dataverse CLI and `az` still work with the OIDC variables removed (on their cached tokens). If they do, those variables go in `--secret-env-vars` with `GITHUB_TOKEN`, so neither the agent's shell nor its MCP servers can mint a token; if not, only `GITHUB_TOKEN` goes.
5. **One `copilot -p` session per story,** in a folder of its own:
   - `--autopilot --max-autopilot-continues=10 --max-ai-credits=150 --no-ask-user --output-format=json --share --usage-output-file --log-dir --disable-builtin-mcps`;
   - `--plugin-dir` and `--add-dir` for each of the three plugin folders; `--disable-mcp-server=playwright` (the model-apps plugin's browser server; the gate's verifiers do the clicking);
   - `--additional-mcp-config` with two servers: **`dataverse`, the shim in front of `dataverse mcp`, cap 60, timeout 60 seconds** (the Dataverse skills look for any tool whose name holds "dataverse"), and **`flowagent`** from its pinned folder with `PLUGIN_ROOT` set. The power-automate plugin's `microsoft-learn` docs server stays;
   - `PLUGIN_ROOT` set to the story's plugin folder, and `COPILOT_OTEL_FILE_EXPORTER_PATH` to a file (token counts and cost per model call, no content);
   - **allowed** (`--allow-tool`): `shell(node:*)`, `shell(pac:*)`, `shell(az:*)`, `shell(dataverse:*)`, `shell(python3:*)`, `shell(mkdir:*)`, `write`, and the `dataverse`, `flowagent` and `microsoft-learn` servers. Read-only shell commands run without a rule;
   - **denied** (`--deny-tool`, deny wins over allow): `pac solution export`, `import`, `delete` and `pack`; `pac auth create`, `clear`, `delete` and `select`; `az login`, `az logout`, `az account get-access-token`; `dataverse auth`, `dataverse mcp`; `git push`, `curl`, `wget`, `sudo`, `npm`, `npx`, `pip`, `pip3`, `rm`. In `-p` and autopilot runs, a tool no rule allows is denied, not asked about (the CLI's own help), so every denial is in the session's events;
   - the prompt says the run is unattended, names the environment and solution, gives the story, and sets four rules: build in the environment and never export, import, pack or delete a solution; never pass `--allow-destructive` and stop if the change needs it; do not get round a refused tool; write `handoff.md` saying what changed, where it stopped or would have asked for approval, each refusal and what it did then, and what is left.
   - **The driver's guards:** it ends the session if the shim writes a stop file (as a night driver would, then PARK), or after 30 minutes. Afterwards it removes token-shaped strings from every file the session wrote.
6. **The stories:**
   - **App Spec, the update path:** add a text column "Category" (`fspk_category`, 100 characters) to "Spike app row" (`fspk_spikeapprow`), and show it on the main form "Spike app row" and in the view "Active spike app rows", with the model-apps plugin's app-builder skill.
   - **Flow:** change the timer flow's Compose step to "factory spike timer v5 (Copilot CLI, part 4)" and leave the flow off, with the power-automate plugin and FlowAgent.
7. Then, as the driver: read what changed by the Web API (the table's columns, the main form's and the view's XML, the flow's Compose step and state, the solution's components before and after; the timer flow is turned off if a session left it on), export and unpack, compare with the reset commit, sign out, and pack again normally and with no network.

**Local check before the run** (21 November 2026, scratch harness, not committed). None of Microsoft's code ran on the laptop. Stand-ins took the place of `copilot`, `pac`, `az` and `dataverse`, with a fake Dataverse Web API, token service and GitHub OIDC endpoint. The Copilot stand-in recorded its arguments and environment, started the session's `dataverse` server from the MCP config (the real shim in front of the rebuilt fake proxy), made a read and a create through it, wrote events with a refusal and a token in them, and never started FlowAgent. Two runs:

- **Run a:** both stories ran and every probe check passed except the no-network pack, which needs Linux (as in parts 1 to 3). The stand-in saw `NONINTERACTIVE`, `PLUGIN_ROOT` set to the story's plugin, the job token, auto-update and client telemetry off, plugin folders only, the OpenTelemetry file, `--autopilot`, `--no-ask-user`, JSON output, the 10 allow and 22 deny rules, the cap, the model, `playwright` disabled, `--secret-env-vars` with the OIDC variables (the stand-in `pac`, `dataverse` and `az` worked without them), and no `--allow-destructive` outside the prompt. The shim listed 16 tools and added a row ID to the create. The probe found the denial, removed the tokens (no `eyJ` left in any output file), and read the column, form, view, flow change and export as the fake had them.
- **Run b:** in the flow story the stand-in made a `create_table` call whose answer never came: the shim stopped (`not-safe-to-retry`, PARK `tool_failure`) after its 60-second timeout, and the driver ended the session at once (exit -15). The flow did not change, and the checks said so.

### Findings (run 40121696, 21 November 2026)

The job took 3.9 minutes: installs 1 minute, each story under 50 seconds, the export 18 seconds. The probe's own result says FAIL (10 of 12 checks): the column was not made, which is finding 2 and the right outcome; and its `--allow-destructive` check was a false alarm (finding 3). Everything else passed.

1. **Copilot CLI runs Microsoft's skills headless as the lane identity.** On a hosted runner, with the job's own `GITHUB_TOKEN`:
   - Copilot CLI 1.0.113 installed from the lockfile;
   - the three plugin folders loaded and no others;
   - the `dataverse` (the shim), `flowagent` and `microsoft-learn` servers connected;
   - plan 5.2's model, `claude-sonnet-5.5`, was accepted (the model check answered "ready" in 2 seconds).

   Each session ended by itself with `task_complete` (autopilot stopped: task complete), well inside the 30-minute guard. The lane's sign-ins (pac, the Dataverse CLI, `az`) were made fresh before each story with no secret, and all worked.
2. **The App Spec skill stops for approval at the apply on an existing app.** The agent ran `/app-builder` unattended:
   - it confirmed unattended mode and the active pac profile;
   - it listed the apps and downloaded the existing app's spec;
   - it read the spec schema in the plugin folder, and added the column, the view and the form to the spec;
   - the lint passed, and the dry run planned one create (the column) and reuse of everything else.

   Then the apply (`--non-interactive --apply --verify --publish`) was refused before it wrote anything: *"app 'fspk_factoryspikeapp' and solution 'FactorySpike' already exist(s) and this is a non-interactive run — refusing to overwrite an existing app. Re-run with --allow-destructive to authorize"*. The agent did not pass the flag, did not try to get round the refusal (it noted it would not drop `--non-interactive`, "because that would only be a way around the refusal"), and wrote a handoff that names the refusal, what a person must approve, and the command to run after that. So **at night, an App Spec change to an existing app cannot be applied without `--allow-destructive`, even when the change is one new column**. Part 2's new app needed no flag. The app, the table and the solution are unchanged (the Web API read and the export agree).
3. **No build ran with `--allow-destructive`.** The probe's check looked for any event text holding both `build-model-app` and `--allow-destructive`, and the engine's own refusal message holds both. The transcript shows the flag in no command.
4. **The flow story passed.** The agent loaded FlowAgent's `manage-flows` skill and went step by step:
   - `get_current_env` worked; `list_flows` failed twice with HTTP 401 `ClientScopeAuthorizationFailed` (part 2 finding 6), once by name and once by environment; `doctor` passed;
   - it then found the flow's ID with one Dataverse MCP `read_query` on the `workflow` table, through the shim;
   - `get_flow` worked; `edit_flow` ran as a dry run, then applied with the preview token the dry run gave;
   - it read the flow back, wrote the handoff, and finished.

   It did not try to turn the flow on or run it, as told. The Compose step reads the new text, the flow is off, and the export holds the change. `edit_flow` with a preview token is FlowAgent's own two-step approval, and it needs no person.
5. **Where the skills stop, in all:**

   | Skill | Stops for a person? | At night |
   |---|---|---|
   | `/app-builder`, new app (part 2) | No: unattended, the lint, dry run and design are the approval | Runs |
   | `/app-builder`, change to an existing app (part 4) | **Yes:** the apply needs `--allow-destructive` | PARK, or another route (proposal 2 below) |
   | FlowAgent `manage-flows` (part 4) | No: `edit_flow` checks itself with a dry run and preview token | Runs: read and edit only; list, turn on, turn off and run fail with 401 (part 2) |
   | `dv-solution` (read, Session 25) | Yes: publisher, environment, export and import | Not reached here; the driver exports, and the lane config gives the publisher and environment |
   | Copilot CLI itself | No: in autopilot, a tool no rule allows is denied, not asked about | Runs |

6. **No tool request was denied in either session.** All the agent needed was in the allow list: `skill`, `bash` (node, pac, python3, `mkdir`, `grep`, `sed`, `ls`, `cat`), `create`, `tool_search_tool`, `task_complete`, and the `dataverse` and `flowagent` tools. None of the 22 deny rules was hit. Read-only commands (`grep`, `sed`, `ls`) and the compound commands the agent wrote (`export PLUGIN_ROOT=...; cd ...; node ...`) ran under the rules as given. The probe's own denial filter matched ordinary words in the events; the list above is from reading the events. So the deny list is untested: a later run should try one refused command on purpose, to see the model's answer.
7. **MCP calls per session: 0 for the App Spec story, 1 for the flow story.** The App Spec engine talks to Dataverse through its own scripts and `az` tokens, not MCP. The flow story's only call was the `read_query` that stood in for `list_flows`. The shim passed `initialize` and `tools/list` (the same 16 tools) and the call, with no retry, no error and no ID added. These are the cap's first numbers. Small stories are far below 60; the cap should be set from the first nights (proposal 4).
8. **Copilot ends its MCP servers without closing their input,** so the shim never wrote its final summary (`"final": false`). The counts were right, because the shim rewrites the summary after every call. The driver must read the summary as it stands when the session ends, not wait for the final flag.
9. **Time and AI credits, as the CLI reports them** (`--usage-output-file`):

   | | Model calls | Tokens in (of which cache read) | Tokens out | AI credits | Session |
   |---|---|---|---|---|---|
   | Model check | 1 | 19,347 (0) | 4 | 4.84 | 2 s |
   | App Spec story | 9 | 631,056 (549,165) | 3,763 | 29.73 | 48.6 s |
   | Flow story | 12 | 437,029 (410,979) | 2,110 | 12.73 | 45.5 s |

   Each session also counted 1 premium request. The CLI's own budget note after each tool, "[cost: 20% used · $1.20 left]" at the end of the App Spec story with `--max-ai-credits=150`, shows it prices **1 AI credit at USD 0.01**, so the stories cost about USD 0.30 and 0.13. Neither came near the 150-credit cap. Whether these credits are billed to `GetAI-IP` or elsewhere is spike 0.6's question.
10. **`--secret-env-vars` can hide the OIDC variables from the session.** Before the first story, pac, the Dataverse CLI and `az` all worked with `ACTIONS_ID_TOKEN_REQUEST_URL` and `_TOKEN` removed, on their cached tokens. So both sessions ran with those two variables, and `GITHUB_TOKEN`, removed from the agent's shell and its MCP servers. Neither the agent nor a server could mint a new token, and the session still did its work. This only holds while the cached tokens last (about an hour), so a longer session needs the driver to sign in again outside the session. It is not a hard boundary either, as the agent runs as the same user as the job [inference].
11. **The export and pack:** nothing left or joined the solution; the 42-file tree packed again signed out and with no network, with the export's members and root components, and the round trip was byte-identical. The only change from part 2's export is the Compose step's text.
12. **No token-shaped string** in the run's log, and the probe found none to remove in the session files.
13. **The admin centre:** part 3's 20 calls are billed (part 3 finding 10). Part 4's one MCP call should show as one more row of 0.1 for 21 November, once the data refreshes.

What this does not show: a real transient MCP failure; the shim's refusal as the model sees it (no stop happened); the deny list hit; a longer story; any story that needs a connection.

### Exit test: proposed verdict

**Pass, with one fallback for the App Spec update path** (for Boroon to accept):

| Exit test item | Result |
|---|---|
| We know where the skills stop for approval | Yes: the table in finding 5 |
| The Web API flow runs, exports and packs again | Yes (part 1), for a flow with no connector; a premium flow needs a licence |
| Whether the App Spec apply works as the lane identity | Yes for a new app (part 2). For a change to an existing app, only with `--allow-destructive`, which the driver never passes: **so the fallback applies there** (PARK, or by day), unless proposal 2 finds another route |
| Whether FlowAgent works as the lane identity | In part: read and edit yes, in a Copilot session too; list, turn on, turn off and run no (HTTP 401). The fallback applies to those: the Web API turns flows on and off; nothing tried starts a run on demand |
| Count the MCP calls per session, to set the cap | 0 and 1 for two tiny stories; the cap to start from proposal 4 |
| A way to count and retry | The shim, on the accepted rule, in front of the real proxy and inside a real Copilot session |
| Which MCP errors are safe to retry | Settled by Boroon's rule (20 November), from part 3; every call that reaches Dataverse is billed, so a retry costs like a new call |

### Proposed plan edits (not made; at Boroon's word)

1. **11.1, row 0.14:** the result above, and the fallback for existing apps.
2. **5.6 (live build), App Spec on an existing app** (a decision for Boroon). Options:
   - (a) **PARK** such a story at the apply, with the dry run as evidence, and apply it by day. Safe, but most model-driven app stories change an existing app, so many would PARK.
   - (b) **Another route for additive changes:** a column by Dataverse MCP `update_table` (which adds columns) or the Web API, and the form and view by the Web API (`systemform`, `savedquery`), then the driver's export as usual. No `--allow-destructive`. Untested: worth one more part-4 style run before Stage 3.
   - (c) **The driver grants `--allow-destructive`** only when a trusted check of the dry run finds nothing but creates and reuses. Not recommended: the flag authorises every destructive step of the apply, not only what the dry run showed.

   Recommended: (a) for Stage 3, and try (b) first. **Boroon, 21 November 2026:** test (b) in a separate session (Session 29), then agree the approach. **Agreed by Boroon on 21 November 2026, after part 4b:** (b) at night for additive changes to an existing app, the App Spec apply for a new app, and (a) for any other change to an existing app (part 4b, "Approach"). **Edited into the plan on 21 November 2026, at Boroon's word** (5.6, 11.1, 14.4, 15.1, Appendix C; part 4b's plan edits below).

   **What (a) would really cost** (Session 28, 21 November 2026, for that decision; the numbers are estimates from the plan's own story model in 10.4, not measured):
   - **Which stories it hits:** every App Spec change to an existing model-driven app, which means a new column, form, view, chart, navigation entry or role on an app that already exists. By the work sizes, that is most XS stories ("view-column tweak"), most S ("one additive change in one app") and the UI part of many M. These are the factory's lowest-risk, highest-volume stories, and after an engagement's first build most model-driven stories are of this kind [inference: no measured mix yet]. It does not hit new apps (part 2), flows (part 4), Copilot Studio, code parts, or anything the agent does by the Web API or MCP.
   - **What a night does with one:** the agent writes the spec, lints it and dry-runs it, then PARKs with the dry run as evidence, in about a minute for about 30 AI credits (part 4). The lane then sits idle or takes the next story. No PR comes from it that night.
   - **What a person then does by day:** read the handoff and dry run, run the apply in a lane at rung L0 (an interactive run, where the skill can ask), check it, and start the export and PR. The night path (driver export, PR, gate) is replaced by a day path for that story.
   - **Cost:** the plan's model allows 5 human minutes a story for PARK handling. A day apply is more like 20 to 30 minutes [inference], so 15 to 25 minutes more. At the plan's USD 100 an hour that is USD 25 to 42 per attempt, and divided by the 70% yield, as the model does, roughly USD 35 to 60 per accepted story: such a story goes from about USD 150 to about USD 185 to 210 fully loaded. Human minutes are already 80% of the cost, so this goes straight to margin.
   - **Time:** about one more day per story: the night prepares, the day applies, and the gate and merge follow.
   - **Trust ladder:** the plan's own first auto-merge example, `views-forms-additive`, is exactly this class. Under (a) it never runs unattended, so it cannot earn rung L2 through the night path.
   - **What (a) keeps:** no `--allow-destructive` at night, nothing new to build, and the plan's existing fallback ("the App Spec apply by day only"). It is the safe default if (b) fails.
   - **A middle way, if (b) fails:** a person approves the dry run by day (for example in the 17:00 night plan), and the driver passes `--allow-destructive` only for that exact spec (checked by hash) when the night's dry run matches the approved one. The skill itself allows the flag when the authority is "supplied independently". But the flag still authorises every destructive step of the apply, not only the planned ones, so it carries part of (c)'s risk, and the spec work moves to the day.
3. **5.11 and Appendix D:** add the PARK type `tool_failure` (the shim's stop for a call that still fails, or one not safe to repeat whose answer was lost). Its `park.json` instruction names the tool, its arguments, the last answer's text and correlation ID, and the shim log. Add `tool_failure` to `Custom.ParkType`'s picklist. This settles "the type for a failed call is for the driver spec".
4. **5.14, the MCP cap and retries:**
   - replace "A failed MCP call is retried up to three times" with the accepted rule (part 3's table), including the two choices above: other tools are never repeated, and a batch is never guessed;
   - add that every call reaching Dataverse is billed, tool errors included (checked 21 November);
   - start the cap at **50 calls per session** (5 credits, USD 0.05 at list): tiny stories used 0 and 1, so 50 leaves room. Set it from the ledger after the first nights.
5. **5.2 (the engine):**
   - install Copilot CLI by `npm ci --ignore-scripts` from a lockfile (it has a dependency and per-platform packages, so a lockfile, not one tarball);
   - load Microsoft's plugins with `--plugin-dir` and `COPILOT_PLUGIN_DIR_ONLY=true`, and the Dataverse server as the shim under a name holding "dataverse";
   - `--max-ai-credits` has a minimum of 30, and the CLI prices 1 AI credit at USD 0.01;
   - `--usage-output-file` gives credits and tokens per model (for 10.1);
   - `--secret-env-vars` can carry the OIDC variables, with fresh sign-ins before each session;
   - the driver ends the session when the shim writes a stop file.
   Also close "Some Microsoft skills have plan-approval steps, and their headless behaviour is unknown" with finding 5.
6. **5.9 (`lcp-verify flow`) and 5.14 (licensing):** no route tried starts a flow run on demand as the lane identity; a flow runs only on its own trigger. A premium flow owned by the lane identity needs a licence to run (part 1).
7. **5.4 (reset proof and drift check):** the canonical compare ignores the version stamp Microsoft's server updates change (part 1 finding 6).
8. **Appendix A and 2538 (the gate):** the import into Test and the danger rules allow an App Spec app's missing dependency on `msdyn_AppFrameworkInfraExtensions` (part 2 finding 3).
9. **14.4:** a row for spike 0.14's result, the retry rule and `tool_failure` (Boroon, 20 November), and the cap. **15.1:** close the 0.14 question; the MCP question's "The cap's number comes from spike 0.14" gets the number.
10. **Section 12 (risks):** a line that most App Spec stories on existing apps PARK under (a), until (b) is tried.

## Part 4b: option (b), an additive change without the App Spec engine

`tools.yml` (job `part4`, mode `part4b`), `probe/tools_probe.py` (`part4b` mode) and a new `probe/webapi.py`, in `GetAI-IP/export-probe` at `35a5779` (copies here; the passing run ran there). Session 29, 21 November 2026, at Boroon's word (proposal 2: test (b) before agreeing the approach). The plan is not edited.

### Method

**The story** is part 4's App Spec story again, on the same scratch: add a text column "Category" (`fspk_category`, 100 characters) to "Spike app row" (`fspk_spikeapprow`) in `FactorySpike`, and show it on the main form "Spike app row" and in the view "Active Spike app rows". The table has two main forms ("Spike app row", from the App Spec, and "Information", Dataverse's own), so the story names the one to change. "Active Spike app rows" is the stock default view's exact name; part 4's probe checked for "Active spike app rows", which never matched (harmless there, as the column was not made).

**The route, with no App Spec apply:**

- the column by Dataverse MCP `update_table`, through the shim (cap 60, the accepted retry rule; `update_table` is never repeated);
- the form's `formxml` and the view's `layoutxml` and `fetchxml` by the Web API, as updates to the existing `systemform` and `savedquery` rows;
- then `PublishXml` for the table, and a read back.

**The Web API goes through a trusted helper,** `probe/webapi.py` (`python3 webapi.py METHOD PATH [--body JSON|@FILE] [--out FILE]`). It stands in for plan 5.6's "trusted helper scripts for the Web API", which the Stage 3 driver would ship. It:

- gets its token from the Azure CLI's cache, as the lane identity, and never prints or logs it;
- sends every write with `MSCRM.SolutionUniqueName: FactorySpike`, which the agent cannot change;
- takes GET, POST and PATCH only: DELETE and PUT are refused (an additive story deletes nothing, and a metadata PUT replaces a whole definition), and so are `$batch` and the solution actions that export, import or remove;
- sends every PATCH with `If-Match: *`, so a PATCH to a row that does not exist fails instead of making one (a plain PATCH upserts);
- logs each call (method, path, status, seconds, error text) for the driver.

Microsoft's own route was not used: the Dataverse skills' `dv-metadata` makes forms and views with its Python SDK (`PowerPlatform-Dataverse-Client`, installed by `pip`, which the night denies and which is not pinned), and uses `dataverse api request` only to publish. Its own notes say a form or view made by the SDK lands in the default solution and must be added to the solution by hand. Read from the plugin at its pin, not run.

**The session** is one `copilot -p` run, as in part 4 (Copilot CLI 1.0.113, `claude-sonnet-5.5`, unattended, the same allow and deny lists, fresh sign-ins, `--secret-env-vars` with the OIDC variables), with these differences:

- plugins: model-apps and the Dataverse skills, so the build engine is there to reach for; not power-automate, and no FlowAgent server;
- `--add-dir` for the probe folder (where the helper is), and a deny rule on writes there;
- the prompt names the route and says: do not run `build-model-app.js` at all, not even a dry run, and do not use the app-builder skill; update the existing form and view, do not make new ones;
- `PLUGIN_ROOT` is not set.

**No deny rule can stop the engine alone.** Copilot CLI's own help says a shell rule matches a command and at most its first subcommand, and `shell(node:*)` must stay allowed for the plugins. So the guard is the prompt, and a check afterwards on the commands the session started (`tool.execution_start`), not on any event text: any command naming `build-model-app` fails the run, and one with `--apply` is flagged.

**The driver, around the session:**

1. Reads the table's columns, every form and view on it (their XML hashed), the solution's components, the ID of every form and view in the environment, the `fspk_` tables and the other spike table's columns. Stops if `fspk_category` already exists. (The first try, run 40125881, filtered forms by `createdon`, which `systemform` does not have; it stopped at that read, before any change. Spike 0.19 found the same: forms keep no maker. So the probe compares every ID before and after, at `74ca863`.)
2. Exports and unpacks `FactorySpike` before the story, so the story's own change shows file by file.
3. Runs the session, ending it on a shim stop or after 30 minutes.
4. Reads all of step 1 again, and whether the column became a solution component of its own.
5. Exports and unpacks again; compares with the export before; checks that only the table's `Entity.xml`, the one form file and the one view file changed; signs out; packs again normally and with no network.
6. Checks that the helper and the shim were not changed during the session (hashes).

**Exit checks (18):** the session ran and ended itself; the engine was not run; no `--allow-destructive`; the column made (text, 100, "Category"); the column on the form "Spike app row" (published); other forms unchanged; the column in the view's layout and fetch (published); other views unchanged; no new form or view; nothing made outside the solution; nothing left the solution; the column, form and view in the export; only the expected files changed; the trusted files unchanged; packs signed out; packs with no network.

**Local check before the run** (21 November 2026, scratch harness, not committed). None of Microsoft's code ran on the laptop. Session 28's harness was copied and extended: a fake Web API with both main forms, the card form and two views, each with an unpublished and a published copy (a read returns the published one, as Dataverse does; `PublishXml` copies one to the other), `If-Match` handling (without it, a PATCH upserts), and a record of every write's headers; the fake MCP proxy's `update_table` adds the column; the Copilot stand-in drove the real shim and the real helper the way a session would, and the `pac` stand-in exported published forms and views only. Two runs:

- **Run a:** 17 of 18 checks passed; the no-network pack needs Linux (as in parts 1 to 4). The stand-in saw only the `dataverse` server, both plugin folders and the probe folder, the write deny rule, the helper path in the prompt, `PLUGIN_ROOT` unset, and the OIDC variables in `--secret-env-vars`. `update_table` went through the shim once. Every helper write carried the solution header and every PATCH `If-Match: *`. The helper refused DELETE, PUT, `ExportSolution`, `$batch` and a full URL (exit 2), and a PATCH to a form that does not exist came back 404 instead of making one. No token in any output file.
- **Run b:** the stand-in also started `node .../build-model-app.js --apply`: the run failed on "engine not run", and `engine_applied` was set.

After run 40126131 (finding 2), the local check ran twice more: the helper with paths that have no leading slash (run c, as run a), and the new `part4b-undo` mode, which took the column off the form and view, published, and deleted the column (run c), and deleted nothing when a row held a value in the column (run d).

### Findings (runs 40125881, 40126131, 40126711 and 40126806, 21 November 2026)

Four runs: 40125881 stopped at the driver's first read (step 1 above), before any change. 40126131 ran the story and only the column landed (finding 2). 40126711 (`part4b-undo`) deleted that column. 40126806 ran the story again, with the helper fixed, and passed.

1. **Option (b) works, headless, as the lane identity: all 18 checks pass** (run 40126806, at `35a5779`). In one `copilot -p` session of 48 seconds, with no App Spec apply and no `--allow-destructive`:
   - the column by Dataverse MCP `update_table` through the shim (1 call): "Category", text, 100 characters;
   - the main form "Spike app row": one new row with the column, after "Note"; "Information" and the other forms unchanged;
   - the view "Active Spike app rows": the column in its layout and its fetch; the other six views unchanged;
   - `PublishXml` for the table, and a read back of the column, the form and the view, all by the helper.

   No new form or view anywhere (962 forms and 3,246 views, the same IDs before and after), no new table, the other spike table unchanged, and nothing left the solution. The session ended itself (`task_complete`); its handoff lists each change, the one refused command (finding 4) and, under stops and approvals needed, "None".
2. **Copilot CLI reads a shell argument that starts with `/` as a file path, and a night run denies it** (run 40126131). The helper's first form took Web API paths like `/systemforms?...`. Copilot CLI checks paths in shell commands against the working folder, the system temp folder and `--add-dir`, and asks about any other; in `-p` that is a denial: *"Permission denied because no interactive user response was available"*. Only `webapi.py --help` ran. So only the column was made (by MCP); the form and view were not changed, and the agent said so in its handoff and did not try another route. The fix was the helper's documented path form, with no leading slash (`systemforms(<id>)`), at `35a5779`. For Stage 3: trusted helpers must take arguments that do not look like paths outside the session, or the driver adds their folders with `--add-dir`. `--allow-all-paths` would also work, but it removes the check for everything.
3. **A column made by MCP `update_table` reaches the export, but only because the table is in the solution with all its parts** (both runs). `update_table` takes no solution name, and Dataverse adds a column made without one to the default solution only (Microsoft's docs). The column did not become a solution component of its own (no new `solutioncomponent` row). It is in the export because `FactorySpike` holds `fspk_spikeapprow` with `behavior="0"` (include all its parts). A table held with only some of its parts would leave the column outside the solution: the export would not show it, and the leftover finder would stop the lane (plan 5.4). So either lane solutions hold their tables with all parts, or columns go through the helper (a POST to the table's `Attributes` with the solution header, which also adds the component), or the driver adds them with `AddSolutionComponent`.
4. **The deny list matched once, inside a compound command** (run 40126806). One command ended with `rm` of the agent's temporary files; `shell(rm:*)` denied the whole command (*"Permission to run this tool was denied due to the following rules: `shell(rm:*)`"*). The agent ran it again without the `rm`, and named the refusal in its handoff. This is the first deny rule seen to fire in spike 0.14 (part 4 finding 6). The two-word rules, such as `shell(pac solution export:*)`, are still untested; Copilot CLI's help says a rule names a command and at most its first subcommand, so they may never match [inference].
5. **The export changed in exactly the three files expected,** each with a small additive diff:
   - `Entities/fspk_spikeapprow/Entity.xml`: the new `attribute` block (`fspk_Category`, `nvarchar`, `MaxLength` 100, display name "Category");
   - `FormXml/main/{7836bd17-...}.xml`: one `<row>` with one cell and a text control bound to `fspk_category`;
   - `SavedQueries/{e3daadf8-...}.xml`: one `<cell name="fspk_category" width="100" />` and one `<attribute name="fspk_category" />`.

   `Other/Solution.xml` and `Other/Customizations.xml` did not change. The tree packed again signed out and with no network, with the export's members and root components, and the round trip was byte-identical.
6. **What the session did, in order:** read the helper's help; listed the table's main forms and views (helper GETs); added the column (`update_table`); read the form's `formxml` and the view's XML into files under `/tmp`; edited them with short `python3` scripts (new GUIDs for the cell and control, the text control's `classid`); PATCHed the form and the view; published; read all three back, and the "Information" form to check it was untouched. 12 helper calls: 9 reads (one a 400 for a `$select` on the wrong metadata type, which it corrected), 2 PATCHes (3.7 and 1.5 seconds) and `PublishXml` (8.4 seconds). It did not run the build engine, use the app-builder skill, or try `--allow-destructive`. No tool was refused except the `rm` (finding 4).
7. **The helper's rules held,** in the run and the local checks: every write carried `MSCRM.SolutionUniqueName: FactorySpike`, every PATCH `If-Match: *`; the helper and the shim had the same hashes after the session; no token in the run's log or artifact. It is a probe, not a gate script: it allows a PATCH to any table, so a night version should allow only the tables and actions of the change class (for this one: `systemforms`, `savedqueries`, a table's `Attributes`, `PublishXml`).
8. **MCP's `update_table` answer is not a read of what it made.** Its answer said `ALTER TABLE fspk_spikeapprow ADD (fspk_Category VARCHAR(MAX))`; Dataverse made `nvarchar` with `MaxLength` 100, as asked (`describe` and the Web API agree). The agent's arguments were `item: [{name: "Category", type: "string", maxLength: 100}]`; the publisher prefix came from the table. Agents should read a change back, as this one did.
9. **Time, AI credits and MCP calls** (`--usage-output-file`, the shim):

   | Run | Session | Model calls | Tokens in (of which cache read) | Tokens out | AI credits | MCP calls |
   |---|---|---|---|---|---|---|
   | 40126131 (helper denied) | 30.8 s | 7 | 217,631 (184,467) | 1,791 | 11.93 | 2 (`update_table`, `describe`) |
   | 40126806 (pass) | 48.0 s | 8 | 273,594 (235,259) | 3,714 | 15.65 | 1 (`update_table`) |

   The model check took 4.84 credits each time. The passing story cost about USD 0.16 in AI credits (1 credit is USD 0.01, part 4 finding 9) and 0.1 Copilot Credit for its one MCP call: about half the 29.7 credits of part 4's App Spec story, which changed nothing. The whole job took 3.2 minutes, of which the two exports 14 seconds each. The admin centre should show 3 more billed rows of 0.1 for 21 November from part 4b (the 2 and the 1), with part 4's 1.
10. **The undo works for the column** (run 40126711, `part4b-undo`). As the lane identity, by the Web API: it found the column from run 40126131 on no form or view, with no row holding a value, and deleted it (HTTP 204); a read back found it gone. Taking a column off a form and a view, then publishing, was run only in the local check.

What this does not show:

- whether the app shows the new column to a user (no verifier clicked through; the app's form and view keep their IDs, so the app still uses them);
- other kinds of change to an existing app: a new form or view, a site map or navigation entry, a choice or lookup column, a relationship, a role, anything that removes. Each needs its own Web API knowledge; under (b) they would PARK until tried;
- the App Spec in Git, if a project keeps one as the app's builder input (plan 5.6 point 3): a (b) change leaves it stale. The model-apps plugin can download the deployed app back into a spec, as part 4's agent did read-only, so the driver could refresh it after the export [inference, untested];
- a longer or larger story, a real MCP failure, or the shim's stop as the model sees it.

### Option (a) and option (b) side by side (the approach agreed by Boroon, 21 November 2026)

(c), the driver granting `--allow-destructive`, stays not recommended and is left out.

| | (a) PARK at the apply, apply by day | (b) MCP and the Web API at night, no App Spec apply |
|---|---|---|
| Tested | Part 4, run 40121696: spec, lint and dry run at night; the apply refused; the agent PARKed with a handoff | Part 4b, run 40126806: column, form, view and publish at night, as the lane identity; exported, packed offline; all 18 checks |
| What the night delivers | Nothing in the lane; a spec, a dry run and a handoff | The change, in the solution and the export; the PR the same night |
| Night cost (this story) | 49 s, 29.7 AI credits (about USD 0.30), 0 MCP calls | 48 s, 15.7 AI credits (about USD 0.16), 1 MCP call (0.1 Copilot Credit) |
| Human cost | 15 to 25 more minutes per story by day, about USD 35 to 60 per accepted story (Session 28's estimate, [inference]) | The normal morning review; nothing extra [inference] |
| Elapsed | About a day more per story | Same night |
| `--allow-destructive` | Never | Never; the build engine is not run |
| What guards the change | Microsoft's engine refuses; a person approves by day | The trusted helper (solution header, no DELETE or PUT, `If-Match`, an allow-list of tables to add), the shim's cap, the driver's export diff (three files here), the leftover finder and the lane stop rule, then the gate: Merge Danger, the import into Test, the scenarios and the verifiers |
| What it covers | Any App Spec change, once a person approves | Additive changes only: a column on an existing table, and that column on an existing form and view. Anything else on an existing app PARKs, as under (a), until tried |
| How Microsoft supports it | The App Spec loop: spec, lint, dry run, apply, verify | Changing components in the environment through the Web API, then exporting: the loop plan 5.6 already uses. Forms and views are ordinary rows (`systemform`, `savedquery`), as Microsoft's own `dv-metadata` skill treats them. No exported file is edited |
| Its own risks | Many PARKs; `views-forms-additive` never runs at night, so it cannot earn L2 | The agent writes form and view XML; a bad edit would show only later, at publish, the import into Test or the verifiers [inference]. A column made by MCP is outside the solution unless the table is held with all its parts (finding 3). The App Spec in Git goes stale. Copilot CLI's path check (finding 2) |
| To build for Stage 3 | Nothing new | The trusted Web API helper in the driver's repo, narrowed to the change class's tables; the lane instructions naming the route; columns through the helper or added to the solution by the driver; a Merge Danger row for the class; the plan text |

**Approach, agreed by Boroon on 21 November 2026** (proposed here, answered "Agree"): both, by kind of change. At night, (b) for additive changes to an existing app (a column on an existing table, shown on an existing form and view), through a trusted helper the driver ships; the App Spec apply for a new app (part 2); and (a), a PARK with the dry run as evidence, for any other change to an existing app until its route is tried. This keeps `views-forms-additive` on the night path, so it can earn L2 on evidence (rule 12).

### Plan edits from part 4b (the decision made, 21 November 2026; the rest still proposals)

**Made on 21 November 2026, at Boroon's word** ("Yes, edit the plan", for this decision only): 5.6 ("Model-driven apps": the three routes as a table, the trusted Web API helper and its rules, columns with the solution header, and the App Spec in Git left open; point 1 and point 3 of "Live build"), 11.1 row 0.14 (a note in its fallback), 14.4 (a new row), 15.1 (the 0.14 question) and Appendix C (an `lcp-executor` rule). This covers proposal 1 below and the 11.1 part of proposal 3, and settles part 4's proposal 2.

**Still proposals,** waiting on his word with part 4's other proposals:

1. ~~**5.6, "Model-driven apps":**~~ made (above). The three routes by kind of change (the approach above); the trusted Web API helper as a driver component, with its rules (finding 7); a column on an existing table made through the helper with the solution header, or added to the solution by the driver (finding 3); and the App Spec in Git refreshed from the app after a (b) change, if the project keeps one.
2. **5.2 (the engine):** Copilot CLI's path check denies a shell argument that looks like a path outside the session, so helpers take arguments that do not, or their folders are added with `--add-dir` (finding 2); a one-word deny rule matches inside a compound command (finding 4).
3. **Section 12** (the 11.1 note is made): the risk line of proposal 10 becomes "App Spec changes to existing apps other than additive ones PARK".
4. **Appendix B (Merge Danger):** a row for this class, keyed on the export diff: only a table's `Entity.xml` gaining an attribute, and forms and views gaining cells and attributes.

## Run order and results

Runs start with `GH_HOST=getai.ghe.com gh workflow run <file> -R GetAI-IP/export-probe --ref main`, with `-f mode=... -f tenant_id=... -f app_id=... -f env_url=https://factory-lane-1.crm6.dynamics.com/` for `tools.yml`.

| Run | ID | Workflow, mode | Result |
|---|---|---|---|
| 1 | 39346986 | copilot-check | Pass: `ready`, exit 0 |
| 2 | 39347126 | tools, flow | **Pass.** Timer flow made, updated, on, ran (`Succeeded`), off, exported, packed signed out and offline, round trip byte-identical. The Dataverse flow turned on, was not started (HTTP 401, finding 3), and was turned off. 4.4 minutes |
| 3 | 39563486 | tools, part2 | **App Spec works; FlowAgent in part** (13 of 17 checks pass). `az login` as the lane identity; App Spec lint, dry run and apply (109 s, verify 13 of 13); table and app in the export; FlowAgent's update on both paths in the export; packed signed out and offline. Failed: FlowAgent's list, and its run on both paths (HTTP 401, part 2 finding 6). 3.6 minutes |
| 4 | 39749076 | tools, part3 | **Pass** (10 of 10 checks). The shim passed `initialize`, `tools/list`, reads and a create; the cap of 2 held; the bad query and the missing table were each tried four times; the dropped-answer create was retried and wrote twice; the own-ID create wrote once. 20 calls sent, 2 refused. All 4 rows deleted. 1 minute |
| 5 | 40121696 | tools, part4 | **The skills run headless; App Spec stops at an existing app** (probe: 10 of 12 checks; the two misses are the column, rightly not made, and a false alarm on `--allow-destructive`). Model check `claude-sonnet-5.5` "ready". App Spec story: lint and dry run passed, the apply refused without `--allow-destructive`, agent stopped with a handoff; 0 MCP calls, 29.7 credits, 49 s. Flow story: FlowAgent `edit_flow` changed the Compose step, flow left off; `list_flows` 401, flow found by 1 MCP read; 12.7 credits, 46 s. No tool denied. Exported, packed signed out and offline, round trip byte-identical. 3.9 minutes |
| 6 | 40125881 | tools, part4b | **Stopped at the first read,** before any change: `systemform` has no `createdon` to filter on. The probe compares every form and view ID instead (`74ca863`). 0.9 minutes |
| 7 | 40126131 | tools, part4b | **Only the column** (14 of 18 checks pass). The column by MCP `update_table` landed and exported; every helper call but `--help` was denied by Copilot CLI's path check (paths starting with `/`); the agent stopped with a clear handoff. 30.8 s, 11.9 credits, 2 MCP calls. Packed signed out and offline. 3.5 minutes |
| 8 | 40126711 | tools, part4b-undo | **Pass.** Run 40126131's column, on no form or view and with no value in any row, deleted by the Web API (HTTP 204) and gone on a read back. 0.4 minutes |
| 9 | 40126806 | tools, part4b | **Pass** (18 of 18) at `35a5779`, the helper taking paths with no leading slash. Column by MCP, form and view by the helper, published; nothing new or outside the solution; the export changed in the three expected files only; packed signed out and offline, round trip byte-identical. 48 s, 15.7 credits, 1 MCP call; one `rm` refused by the deny list. 3.2 minutes |

## Left to do

1. ~~**Part 2**~~: done in Session 26 (run 39563486), above.
2. ~~**Part 3**~~: done in Session 27 (run 39749076), above.
3. ~~**Part 4**~~: done in Session 28 (run 40121696), above.
4. ~~**Check the bill for part 3**~~: done 21 November: 20 billed rows (part 3 finding 10).
5. **Boroon:** accept or change the exit test verdict, ~~choose between the App Spec options (proposal 2)~~ (agreed 21 November 2026, part 4b), and say which plan edits to make (proposals 1 to 10, with the retry rule and `tool_failure` he accepted on 20 November). Then the plan edits, and the scratch deleted at his word.
6. Not done, could follow: one refused command on purpose, to see the model's answer and test the two-word deny rules (part 4b saw `shell(rm:*)` fire, finding 4); the shim's stop as the model sees it; part 4's one MCP call in the admin centre (one row of 0.1 for 21 November).
7. ~~**Option (b)**~~: done in Session 29 (run 40126806): it works for an additive change. ~~**Boroon:** agree the approach~~: agreed on 21 November 2026 (part 4b, "Approach"). Still for Boroon: which of part 4b's plan edits to make, with part 4's. Part 4b's three MCP calls in the admin centre (21 November).

## Scratch

New in this spike, kept until it ends, then deleted with 0.18's and 0.19's at Boroon's word:

| Thing | Where | How to delete |
|---|---|---|
| `tools.yml`, `copilot-check.yml`, `probe/tools_probe.py`, `probe/mcp_shim.py` and their runs | `GetAI-IP/export-probe` | Go with the repo (0.18's list) |
| Part 3's rows in `fspk_spikeitem` | `factory-lane-1` | None left: run 39749076 deleted all 4 by the Web API |
| Cloud flow "Factory spike timer flow", in `FactorySpike`, off (made by run 39347126; its Compose step changed by FlowAgent in run 39563486, and again by the Copilot session in run 40121696, to "factory spike timer v5 (Copilot CLI, part 4)") | `factory-lane-1` | `tools.yml`, `mode=flow-undo`; 0.18's `teardown` does not know it, so run this first |
| Part 4 (run 40121696) added nothing else to the lane: the App Spec apply was refused before it wrote anything, so there is no `fspk_category` column and the app, form and view are unchanged; its one MCP call was a read. The session's downloaded spec and handoff were on the runner only | `factory-lane-1` | Nothing to undo beyond the flow row above |
| Part 4b's change (run 40126806): the text column `fspk_category` ("Category", 100) on `fspk_spikeapprow`, one row with it on the main form "Spike app row", and the column in the view "Active Spike app rows", published. Not solution components of their own; in `FactorySpike` through the table (`behavior="0"`). Run 40126131's column was deleted by run 40126711 | `factory-lane-1` | `tools.yml`, `mode=part4b-undo` (off the form and view, publish, then the column; it deletes nothing if a row holds a value; run for the column alone in run 40126711, the rest only in the local check). Or it goes with the table when the App Spec scratch below is deleted |
| `probe/webapi.py` and the `part4b` and `part4b-undo` modes, and their runs | `GetAI-IP/export-probe` | Go with the repo |
| The App Spec's table "Spike app row" (`fspk_spikeapprow`) with its forms and views, the app "Factory spike app" (`fspk_factoryspikeapp`) with its site map and two app settings, and the icon web resource `fspk_factoryspikeapp_icon`, all in `FactorySpike` (made by run 39563486) | `factory-lane-1` | Not written yet: a `part2-undo` mode by the Web API (the app, then the site map, the table and the web resource), run before 0.18's `teardown`. **Do not use Microsoft's `teardown-model-app.js`:** its last step deletes the solution the spec names, which is `FactorySpike` |
| FlowAgent's own backups of the flow (it keeps one before each change) | the runner's home folder | Gone with the runner |

Spike 0.18's "Factory spike flow" was turned on and off again by run 39347126; it is off, and its files are as in the reset commit.

0.18's and 0.19's scratch is still kept (their READMEs).
