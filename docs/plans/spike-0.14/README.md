# Spike 0.14: skills and lane tools headless, as the lane identity

Plan section 11.1, row 0.14 (ADO 2461). Session 25, 18 November 2026 (Sydney time), a laptop session. Started two days after its Mon 16 to Tue 17 Nov slot. Not finished in one session: what is done and what is left are below.

**So far (18 November 2026):** part 1 passes for a flow with no connector: made, updated, turned on, run, exported and packed again offline, as the lane identity (run 39347126). Copilot CLI runs on a getai.ghe.com runner with the job's own token (run 39346986), so part 4 can run there. Parts 2, 3 and 4 are still to do. Two findings matter beyond this spike: Microsoft's server update changed the version stamp in the export (finding 6), and a lane flow that uses the Dataverse connector needs a licence to run as the lane identity (the licence rule, finding 4).

Exit test (plan 11.1): we know where the skills stop for approval; the Web API flow runs, exports and packs again; we know whether the App Spec apply and FlowAgent work as the lane identity. If not: PARK at the approval point, flows by the Web API only, the App Spec apply and FlowAgent by day only. Added 13 November 2026 (Session 22, after 2433): count the MCP calls each session makes, to set the cap; try a way for the driver to count and retry calls; find which MCP errors are safe to retry.

## The parts

| Part | Exit test item | How | State |
|---|---|---|---|
| 1. Flow by the Web API | The flow runs, exports and packs again | Script on a runner, no AI: make, update, turn on, see a run, export, pack signed out and offline | **Pass** for a flow with no connector (run 39347126). A Dataverse flow turned on but was not run |
| 2. App Spec apply and FlowAgent as the lane identity | Whether they work as `getai-fl1-exec` | Script on a runner, no AI: `az login` with the federated token, then the model-apps build engine with `--non-interactive`, and FlowAgent's MCP server called by a small client | Not started |
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

## Run order and results

Runs start with `GH_HOST=getai.ghe.com gh workflow run <file> -R GetAI-IP/export-probe --ref main`, with `-f mode=... -f tenant_id=... -f app_id=... -f env_url=https://factory-lane-1.crm6.dynamics.com/` for `tools.yml`.

| Run | ID | Workflow, mode | Result |
|---|---|---|---|
| 1 | 39346986 | copilot-check | Pass: `ready`, exit 0 |
| 2 | 39347126 | tools, flow | **Pass.** Timer flow made, updated, on, ran (`Succeeded`), off, exported, packed signed out and offline, round trip byte-identical. The Dataverse flow turned on, was not started (HTTP 401, finding 3), and was turned off. 4.4 minutes |

## Left to do

1. **Part 2,** a new mode in `tools.yml`: `az login --service-principal --federated-token` with the job's OIDC token (the same federated credential; `--allow-no-subscriptions`), then:
   - the model-apps build engine on a tiny App Spec (one table, one form, one app): dry run, then apply, with `--non-interactive` and never `--allow-destructive`; export and see what lands in the solution;
   - FlowAgent's MCP server, started from the pinned plugin, called by a small MCP client: list flows, get the timer flow, update it, run it (finding 3's route), read its runs, on the Power Platform API path and the fallback.
2. **Part 3:** a stdio shim in front of `dataverse mcp` (the local proxy, pinned) that counts `tools/call`, stops at a cap and retries a failed call up to three times; driven by a scripted client with reads, a create and forced failures; plus which errors the proxy returns for each.
3. **Part 4:** Copilot CLI on the runner with the pinned plugins, `POWER_PLATFORM_SKILLS_NONINTERACTIVE=1`, the lane's pac and `az` sign-ins, and the shim in front of Dataverse MCP: one small App Spec story and one small flow story. Record where each stops, which tools it asked for, and the MCP calls per session (the cap's first number).
4. Then the exit test verdict, the plan edits at Boroon's word, and the scratch deleted at his word.

## Scratch

New in this spike, kept until it ends, then deleted with 0.18's and 0.19's at Boroon's word:

| Thing | Where | How to delete |
|---|---|---|
| `tools.yml`, `copilot-check.yml`, `probe/tools_probe.py` and their runs | `GetAI-IP/export-probe` | Go with the repo (0.18's list) |
| Cloud flow "Factory spike timer flow", in `FactorySpike`, off (made by run 39347126) | `factory-lane-1` | `tools.yml`, `mode=flow-undo`; 0.18's `teardown` does not know it, so run this first |

Spike 0.18's "Factory spike flow" was turned on and off again by run 39347126; it is off, and its files are as in the reset commit.

0.18's and 0.19's scratch is still kept (their READMEs).
