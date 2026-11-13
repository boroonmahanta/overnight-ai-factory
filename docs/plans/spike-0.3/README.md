# Spike 0.3: Dataverse MCP with an app-only token

Plan section 11.1, row 0.3. Session 13, 5 and 6 November 2026. The result is in `docs/progress.md` (Session 13).

**Result: pass on both paths** (run 36819036, 6 November 2026). A read and a create succeeded headless through the local proxy and through the remote endpoint, signed in as `getai-fl1-exec` with no secret. Findings below.

Exit test: a read and a create succeed headless. Record which of the two paths work:

1. **Local proxy.** A job on `getai.ghe.com` signs in as `getai-fl1-exec` with a federated pac profile (as in spike 0.2), then runs the Dataverse CLI's MCP proxy (`dataverse mcp <url>`, the same thing `npx @microsoft/dataverse mcp <url>` runs) against `factory-lane-1`, and makes one read and one create through it.
2. **Remote endpoint.** With `getai-fl1-exec` on `factory-lane-1`'s allowed MCP clients list, the same read and create against `https://<org>/api/mcp` with an app-only token.

If both fail, record what broke and stop. The fallback (the night stays on pac and trusted Web API scripts) is for a later session.

## What runs where

| Thing | Where | State |
|---|---|---|
| `probe.yml` | `GetAI-IP/mcp-probe` (private, scratch, repo 5331556), `.github/workflows/probe.yml` | Pushed 5 November 2026 (`4ab9682`, then `237ac5b`), at Boroon's word. Repo **deleted 6 November 2026** |
| `mcp_probe.py` | Same repo, `probe/mcp_probe.py` | Pushed with it; deleted with the repo |
| Entra app `getai-fl1-exec` | GET AI tenant. Kept from spike 0.2. Federated credential `mcp-probe-fl1-exec` added for the spike, **deleted 6 November 2026**; no credentials now | Exists |
| Allowed MCP client `new_getaifl1exec` | `factory-lane-1`, for `getai-fl1-exec` | Added 6 November 2026; **kept for Stage 3** (Boroon) |
| Environment `factory-lane-1` | Power Platform, Australia, Sandbox, Managed. Application user `getai-fl1-exec`, System Administrator | Exists |

## How the probe works

One job, `workflow_dispatch` only, and it refuses any ref but `main`. It checks out its own repo at the dispatched commit (for `mcp_probe.py`), never pull request code (rule 5). Permissions `id-token: write` and `contents: read`. No secrets: the tenant ID, app ID and Dataverse URL come in as inputs, so they stay out of this public repo. The job runs in the GitHub environment `fl1-exec`, as plan 5.3 has it; the first run creates that environment in the scratch repo, with no protection rules (as in spike 0.2).

Steps, in order:

1. Print the OIDC claims, never the token.
2. Install pac 2.4.1 (on .NET `10.0.x`) and the Dataverse CLI. The CLI is `@microsoft/dataverse` **1.0.88**, fetched as a tarball from the npm registry, checked against the pinned `sha512` (the registry's own integrity value, read 5 November 2026), then installed with `npm install --global --offline --ignore-scripts` from that file. `npx` is not used, because it would fetch from the registry without our hash check. Print the CLI's own `--help` for the flags used.
3. Only when an app ID is given: `pac auth create --githubFederated` and `pac org who`. Then see whether the Dataverse CLI can use that pac profile (its docs say the profiles are compatible). If it cannot, make its own: `dataverse auth create --githubFederated ... --accept-cleartext-caching` (a plaintext token cache on a throwaway runner; the job removes it).
4. `dataverse mcp <url> --validate`, for information only.
5. **Local path:** start `dataverse mcp <url>` and speak MCP to it over stdio: `initialize`, `tools/list`, `read_query` (`SELECT TOP 1 name FROM organization`, falling back to `account`), and when `write` is on, `create_record` on `account` with the name `spike-0.3 probe (local)`, then read it back.
6. **Remote path:** get an app-only token (client credentials, the GitHub OIDC token as the client assertion, scope `https://<org>/.default`), print its claims (not the token), then the same calls against `https://<org>/api/mcp` over streamable HTTP. Row name `spike-0.3 probe (remote)`.
7. **Clean-up** (always, when `write` is on): through the Web API, delete only `account` rows whose name starts with `spike-0.3 probe` **and** that this app user created, then check none are left.
8. Clear both CLIs' profiles. Write the result table; the job fails if a chosen path failed or a probe row is left.

The tool argument names are not documented, so the script reads them from each tool's `inputSchema` and prints that schema.

Local checks before any run (5 November 2026, scratch harness, not committed): 48 checks of `mcp_probe.py` against a fake OIDC endpoint, token endpoint, `/api/mcp` (server-sent events, session ID, protocol header), Web API and stdio proxy. Covered: both paths with and without `write`; clean-up deletes only this app's probe rows; no credential (`AADSTS700213` shown); client not allowed (`401` with `WWW-Authenticate` shown); the proxy dying at start; a create refused (for example for billing); `organization` not readable. No token, request token or signature in any output. The YAML has only `workflow_dispatch`, `permissions: {}` at the top, the two job permissions, and three actions, each pinned to a full commit SHA checked against its tag with `git ls-remote` (the gate's pins). `npm install --offline` from the tarball works with no network.

## Found before any run (read-only)

- **`mcp.tools` is a delegated scope only.** The Dataverse API (`00000007-0000-0000-c000-000000000000`) in the GET AI tenant publishes two scopes, `user_impersonation` and `mcp.tools`, both of type User, and **no app roles**. So an app-only token carries neither. Whether `/api/mcp` accepts it is exactly what this spike tests. Microsoft's page for the remote endpoint asks for the `mcp.tools` permission and says the flow "depends on the MCP client"; it says nothing about app-only.
- **The Dataverse CLI app (`0c412cc3-0dd6-449b-987f-05b053db9457`) has no service principal in the tenant**, so its admin consent was never given. That consent is for people signing in through the CLI's own app. With `--githubFederated` the token is `getai-fl1-exec`'s, so the probe does not ask for that consent (my inference; the runs will show).
- **The package.** `@microsoft/dataverse` 1.0.88 (29 October 2026): no dependencies, no install scripts, MIT, published by Microsoft's npm accounts with registry signatures. It holds a 1 KB JavaScript launcher and a native binary per platform (Linux x64 is 40 MB), 145 MB packed. The launcher only starts the binary; it updates itself only on an explicit `dataverse install`. The README says "Running a command does not contact the npm registry."
- **Billing.** Microsoft: since 15 December 2025, Dataverse MCP tools "are charged when accessed by AI agents created outside of Microsoft Copilot Studio", in Copilot Credits (the basic rate per 10 responses for every tool used here). A create may be refused if `factory-lane-1` has no Copilot Credit source. Not set up in advance; only if a run says so.
- **`dataverse mcp allow <appId>`** can add an app to the allowed clients list from code, as a Dataverse admin. The probe does not use it; the list is changed in the portal (step C).

## Findings (after run 3, 6 November 2026)

**Result: pass on both paths.** A read and a create succeeded headless through the local proxy and through the remote endpoint, signed in as `getai-fl1-exec` with no secret (run 3).

1. **`/api/mcp` accepts an app-only token, and tool calls work with it.** The token has no `roles` and no `scp` (the API publishes `mcp.tools` only as a delegated scope), yet `read_query` and `create_record` both worked once the app was on the allowed list. Before that, the answer was 403, not 401: "The application '<app id>' is not authorized to access MCP".
2. **The allowed list is checked against the token's app ID.** For both paths the entry needed is the lane's own app (`getai-fl1-exec`). The Dataverse CLI's own app (`0c412cc3-...`), its admin consent and its list entry are not needed when the job signs in as our app.
3. **The local proxy forwards the job's token.** It answers `initialize` itself and opens the real session on the first call that needs the server. An upstream error reaches the MCP client only as `-32603 An error occurred`; the cause (here `403 Forbidden`) is only in the proxy's stderr. A lane must keep the proxy's stderr in the night's trace (rule 16), or a failure is unreadable.
4. **The Dataverse CLI does not share pac's profiles,** at least for a federated profile on Linux: it saw none after `pac auth create`. It needs its own `dataverse auth create --githubFederated`, which works first time and needs no secret.
5. **The Dataverse CLI keeps its token cache unencrypted on Linux** (`~/.local/share/Microsoft/DataverseCli/tokencache_spn_msalv3.dat`), with a warning on every command, because a hosted runner has no keyring. Any process in the job can read it. In a lane the builder agent runs in that job by design, as the execute identity, so this adds no new reach; the job must still remove the profile at the end (`dataverse auth remove --all`, which also clears the cache).
6. **`dataverse mcp --validate` gives the wrong advice for an app sign-in:** it tells you to allow the CLI's app, not the one in the token. Do not use it as a gate check.
7. **The Dataverse CLI sends usage data by default.** Set `DATAVERSE_TELEMETRY_OPT_OUT=1` in every job that runs it.
8. **An allowed MCP client is a solution component** (table `allowedmcpclient`). Its unique name must start with a publisher's customisation prefix (`new_getaifl1exec` here; plain `getaifl1exec` was refused). So the entry for each lane app can ship in a GET AI solution with the `getai` publisher, or be added by `dataverse mcp allow <app id>`, instead of by hand in the portal (rule 8). Not tried here.
9. **The package can be pinned properly.** `@microsoft/dataverse` has no dependencies and no install scripts; fetching the tarball, checking it against the registry's `sha512`, and `npm install --global --offline --ignore-scripts` from that file works on a GitHub-hosted runner. `npx` would skip the hash check.
10. **Read a federated credential back before the first run.** Entra accepts any subject string; a lost first letter (`epo:` for `repo:`) was caught only by reading it back with `az ad app federated-credential list`.
11. **MCP writes are attributed to the lane's application user,** like Web API writes, so audit stays per lane. They still change the environment, so the lane drift check (plan 5.5) must catch them if they skip the builders.
12. **The tool list differs from Microsoft's page:** 15 tools on both paths, no `search_data` (needs Dataverse search), no `invoke_api`, an undocumented `create_skill_resource`. `create_record` takes `item` as an object. Agent instructions should read the tool list, not the docs.
13. **MCP tool calls are metered, at 0.1 Copilot Credit each, from the tenant's prepaid pool** (checked 13 November 2026, ADO 2433; section "Billing check" below). Run 3's six tool calls show as six billed rows of 0.1 credit in `factory-lane-1`. They were not refused because the environment draws from the tenant's unallocated prepaid Copilot Credit capacity by default; "no Copilot Credit source" was wrong.

## Billing check (ADO 2433, 13 November 2026)

Read-only, in the Power Platform admin centre under Boroon's own sign-in, from the laptop session's built-in browser. Nothing was changed. Tenant totals, other environments and people are left out here (public repo).

**Where:** Licensing, Products, **Copilot Studio**, then the **Environments** tab, then `factory-lane-1` (its **Copilot Credits capacity** tab). The **Summary** tab's "Capacity consumption by product" card also lists a **Dataverse** row.

**What it shows for `factory-lane-1`** (month to date, data last refreshed 12 November 2026, 11:00):

| Column | Value |
|---|---|
| Allocated capacity | none |
| Managed | Yes |
| Pay-as-you-go | No |
| Prepaid consumed | 0.6 Copilot Credits |
| Pay-as-you-go consumed | 0 |
| Overage | No |
| Draw from tenant | **Yes** |
| Last updated | 2026-11-06 |

Its detail grid ("Message consumption by resource") has six rows, each: name **Dataverse MCP Server**, product Dataverse, feature **Text and generative AI tools (basic)**, billed **0.1**, non-billed 0. Channel, knowledge sources, tool invoked and LLM model are all blank. Product total: Dataverse, prepaid 0.60, pay-as-you-go 0.00.

The tenant has no pay-as-you-go billing plan, and it does hold prepaid Copilot Credit capacity.

**What it means:**

1. **MCP calls are metered.** Six billed rows match run 3's six billed tool calls: per path, `read_query`, `create_record` and the read-back `read_query`. So `initialize` and `tools/list` are not billed, run 2's refused calls (403) are not billed, and the clean-up (Web API, not MCP) is not billed. The match is by count; the grid names no tool or run [inference].
2. **The rate is Microsoft's stated one.** Every Dataverse MCP tool except `search_data` bills at the "text and generative AI tools (basic)" rate, 1 Copilot Credit per 10 responses ([Dataverse MCP](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-mcp), [rates](https://learn.microsoft.com/microsoft-copilot-studio/requirements-messages-management)). `search_data` bills by usage at another rate; it is absent in `factory-lane-1` (Dataverse search is off).
3. **The source is the tenant's shared prepaid pool.** "Draw from tenant" is on by default, so a lane with no allocation draws from the same unallocated prepaid capacity as everyone else's agents in the tenant, with no cap. That is why the spike's calls were not refused.
4. **List price.** The Copilot Studio pay-as-you-go meter is USD 0.01 per credit ([meters](https://learn.microsoft.com/power-platform/admin/pay-as-you-go-meters)), so one MCP tool call is USD 0.001 at list. A story that makes 500 calls would cost USD 0.50 at list, small against the modelled USD 15 per story. The calls per story are unknown until Stage 3 [inference]. While the prepaid pool lasts, the cash cost of each call is nil at the margin.
5. **The portal cannot feed the ledger per run.** It shows no tool, no run and no time finer than a day, and it lags by up to a day. So the night trace must count MCP tool calls per run and price them at 0.1 credit (rules 13 and 14). The environment report (Summary tab, Download report) is for a monthly check against those counts.
6. **No cap per lane in the tenant.** Rule 13 wants a credit cap on every run. Two ways were open: (a) allocate a fixed number of credits to each lane environment and turn off "Draw from tenant" (Licensing, Copilot Studio, Manage Copilot Credits), though what Dataverse MCP does when the allocation runs out is not documented; or (b) leave the setting and have the driver stop the session at a call count. **Decided (Boroon, 13 November 2026): (b).** The driver stops the session after a set number of MCP calls (the number set from spike 0.14), retries a failed call three times, and either stop is a PARK. In the plan: 5.11, 5.14 and 14.4.
7. **The licence exemption does not help a lane** [inference]. Microsoft exempts users with qualifying Dynamics 365 Premium licences or a Microsoft 365 Copilot licence when they reach Dynamics 365 data ([FAQ](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-mcp-faq)). A lane signs in as an application user with neither.

## Portal steps (Boroon)

### A. Federated credential on `getai-fl1-exec` (after run 1)

Needs: owner of the app registration (you created it, so you are) or Application Administrator or Cloud Application Administrator.

1. https://entra.microsoft.com, Entra ID, App registrations, All applications, `getai-fl1-exec`.
2. Certificates & secrets, Federated credentials tab, Add credential:
   - Federated credential scenario: **Other issuer**
   - Issuer: `https://token.actions.getai.ghe.com`
   - Type: **Explicit subject identifier**
   - Value: the `sub` run 1 prints. Expected shape: `repo:GetAI-IP@801576/mcp-probe@<repo id>:environment:fl1-exec`
   - Name: `mcp-probe-fl1-exec` (cannot be changed later)
   - Description: `Spike 0.3 scratch. GitHub Actions OIDC from getai.ghe.com, repo GetAI-IP/mcp-probe, environment fl1-exec. Remove after the spike.`
   - Audience: `api://AzureADTokenExchange` (the default)
   - Add. No secret, no certificate, no API permission.
3. **Wait five minutes** before the next run (spike 0.2: a new credential took about four minutes to work).
4. Before the run, read the credential back (read-only): `az ad app federated-credential list --id <app id> --query "[].{name:name,issuer:issuer,subject:subject,audiences:audiences}"`. On 6 November 2026 the first save had the subject `epo:GetAI-IP@...` (the leading `r` lost in the paste); the read-back caught it, Boroon edited the value in place, and the second read-back matched at 23:27 UTC. Entra accepts any subject string, so only a read-back or a failed sign-in shows a typo.

### B. Check the Dataverse MCP server is on in `factory-lane-1` (before run 2)

Needs: Power Platform Administrator (Microsoft's stated role for these settings). The environment is already Managed.

1. https://admin.powerplatform.microsoft.com, Manage, Environments, select `factory-lane-1`, then **Settings** on the command bar.
2. Product, **Features**. Scroll to **Dataverse Model Context Protocol**.
3. Check **Allow MCP clients to interact with Dataverse MCP server** is on (Microsoft says it is on by default). If it is off, turn it on and Save. There are two toggles with that name: use the GA one. Leave the one ending **(Preview version)** as it is: it serves `/api/mcp_preview` and its preview tools (not covered by support, may change without notice), and the probe calls only `/api/mcp`. Change nothing else here yet. (Asked by Boroon, 6 November 2026.)
4. Optional, read-only: select **Advanced Settings** and note which clients are listed and enabled. Tell me; do not change any.

Seen by Boroon on 6 November 2026, before any change ("Active Allowed MCP Clients" in `factory-lane-1`). This is the state to return to after the spike:

| Name | Unique name | Application ID | Enabled |
|---|---|---|---|
| Agent 365 Tools | `agent365tools` | `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1` | Yes |
| Dataverse MCP CLI tool | `dataversemcpcli` | `0c412cc3-0dd6-449b-987f-05b053db9457` | No |
| Enterprise Copilot Platform | `enterprisecopilotplatform` | `fb8d773d-7ef8-4ec0-a117-179f88add510` | No |
| Microsoft Copilot Studio App | `microsoftcopilotstudio` | `7ab7862c-4c57-491e-8a45-d52a7e023983` | Yes |
| Microsoft Copilot Studio App - OBO | `microsoftcopilotstudioobo` | `96ff4394-9197-43aa-b393-6a41652e21f8` | Yes |
| Microsoft Cowork | `microsoftcowork` | `6ab48b67-cd74-4ad4-81af-5932984589be` | No |
| Microsoft GitHub Copilot App | `microsoftgithubcopilot` | `aebc6443-996d-45c2-90f0-388ff96faa56` | No |
| vibepowerapps | `developeragentsprod` | `8e38132a-0fcc-47e2-8178-724bda6fc696` | Yes |

All are Microsoft's own apps. `getai-fl1-exec` is not on the list, as run 2 needs. Nothing changed for the spike so far.

### C. Add `getai-fl1-exec` to the allowed MCP clients (after run 2)

Needs: Power Platform Administrator. The Advanced Settings page opens a list inside the environment, so you may also need a security role there; you have System Administrator in `factory-lane-1` as its creator.

1. As B steps 1 and 2, then **Advanced Settings** under Dataverse Model Context Protocol.
2. **New** (a new client entry):
   - Name: `getai-fl1-exec`
   - Unique Name: `new_getaifl1exec`. It must start with a publisher's customisation prefix: `getaifl1exec` on its own was refused on 6 November 2026 with "Export key attribute uniquename for component allowedmcpclient must start with a valid customization prefix" (error `0x800608ad`). `new` is the usual prefix of "Default Publisher for <environment>"; if refused, read the prefix from make.powerapps.com, Solutions, Publishers. The Microsoft entries have no prefix because they come from Microsoft's own solutions. **Finding:** an allowed MCP client is a solution component (`allowedmcpclient`), so the entry can ship in a solution or be added by code (`dataverse mcp allow`), not by hand per lane
   - Application (client) ID: `getai-fl1-exec`'s Application (client) ID
   - **Is Enabled**: Yes
3. **Save & Close**. Done by Boroon on 6 November 2026 at 01:10:58 UTC. Read back (read-only, Web API under Boroon's own sign-in, table `allowedmcpclient`, entity set `allowedmcpclients`): name `getai-fl1-exec`, unique name `new_getaifl1exec`, `isenabled` true, state active, `applicationid` equal to `getai-fl1-exec`'s app ID. Give it five minutes before run 3 (a cache delay is likely; Microsoft documents about five minutes for the Finance and Operations list).

### D. Only if a run asks for it

- A Copilot Credit source for `factory-lane-1` (a pay-as-you-go billing policy with an Azure subscription, or prepaid capacity), if a tool call is refused for billing. A tenant setting: stop and decide. (Not needed: the environment already draws from the tenant's prepaid pool; see "Billing check".)
- Admin consent for the Dataverse CLI app, and enabling the **Dataverse CLI** client (`0c412cc3-...`) on the list, only if the local path names that app. Not expected with a federated app profile.

## Run order

Runs 2 and 3: `GH_HOST=getai.ghe.com gh workflow run probe.yml -R GetAI-IP/mcp-probe --ref main -f tenant_id=... -f app_id=... -f env_url=https://factory-lane-1.crm6.dynamics.com/ -f paths=both -f write=<false|true>`. Run 1 passes no inputs.

| Run | Before it | `write` | What it shows |
|---|---|---|---|
| 1 | Repo pushed | - | Claims only (no app ID): the subject for step A. Also proves the pinned installs and prints the CLI's `--help` |
| 2 | Step A, five minutes, step B | false | Both paths, reads only, with `getai-fl1-exec` **not** on the allowed list: what breaks, and where |
| 3 | Step C, five minutes | true | Both paths with `getai-fl1-exec` on the list. One create per path, deleted in the same job. The exit test |

So the spike writes two rows in all (one per path, in run 3), unless a run is repeated.

## Results

### Run 1: claims only (run 36506161, 5 November 2026): pass

- `sub`: `repo:GetAI-IP@801576/mcp-probe@5331556:environment:fl1-exec`. The immutable form, as in spike 0.2.
- `job_workflow_ref`: `GetAI-IP/mcp-probe/.github/workflows/probe.yml@refs/heads/main`. `issuer_scope`: none.
- The tarball matched the pinned `sha512`; `npm install --offline` from it worked ("added 1 package"). Node `lts/*` gave v26.13.0. pac 2.4.1 installed.
- The CLI's own help confirms `--githubFederated` (`-ghf`) and `--accept-cleartext-caching` on `auth create`, and `--clientid` defaults to "DataverseCLI app".
- **The CLI collects usage data by default:** its first line is "DataverseCLI collects anonymous usage data to improve the product. To opt out: set DATAVERSE_TELEMETRY_OPT_OUT=1". The workflow sets that from run 2 on. The factory's lane jobs should set it too.
- No token-shaped string (`eyJ`) in the log.

### Run 2: both paths, read only, `getai-fl1-exec` not on the allowed list (run 36783926, 6 November 2026): both refused, as expected

IDs are shown as `<app id>` here; the private run log has them.

- **pac sign-in worked** (second time, as in spike 0.2): `'<app id>' authenticated successfully`, `Connected to... factory-lane-1`, and `pac org who` gave the application user.
- **The Dataverse CLI did not see the pac profile.** After `pac auth create`, `dataverse auth list` said "No authentication profiles found" and `dataverse org who` said "No active authentication profile". So "compatible with PAC CLI auth profiles" does not mean shared, at least for a federated profile on Linux. Its own `dataverse auth create --githubFederated` worked at once: profile type `GitHubFederated`, `Connected as <app id>`, the same application user ID as pac.
- **The Dataverse CLI keeps its token cache unencrypted on Linux,** with a warning on every command: "No usable keyring detected on headless Linux; MSAL token cache will be stored UNENCRYPTED at /home/runner/.local/share/Microsoft/DataverseCli/tokencache_spn_msalv3.dat". In a lane job, any process in that job can read it.
- **`--validate`:** both the GA and preview endpoints returned 403 (Forbidden). Its advice names the CLI's own app (`0c412cc3-...`), which is the wrong app when the profile is a service principal.
- **Local path:** the proxy answered `initialize` itself (server `dataverse 1.0.88.0`, protocol `2025-06-18`, capabilities logging, prompts, resources, tools). On `tools/list` it opened its upstream session and got `MCP initialize failed for https://factory-lane-1.crm6.dynamics.com/api/mcp: 403 Forbidden` (in its stderr log). The client saw only `JSON-RPC error -32603: An error occurred.` So the proxy forwards our app's token, and hides the cause from the MCP client.
- **Remote path:** the app-only token had `aud` `https://factory-lane-1.crm6.dynamics.com`, `appid` `<app id>`, `idtyp` `app`, `roles` none, `scp` none, `ver` 1.0. `/api/mcp` answered **HTTP 403**, body: `The application '<app id>' is not authorized to access MCP. For details on approved clients and instructions to enable additional applications, see: https://aka.ms/configuremcpclientlist`. Not 401: the token was accepted as a sign-in, and the refusal is the allowed-clients check, by the token's app ID.
- Both paths are blocked by the same thing: `getai-fl1-exec` is not on the list. The Dataverse CLI app entry is not involved when the profile is our own app.
- No token-shaped string (`eyJ`) in the log. Profiles cleared at the end ("Removed all 1 authentication profile(s)", "Authentication profiles and token cache removed").

### Run 3: both paths with a create, `getai-fl1-exec` on the allowed list (run 36819036, 6 November 2026): **pass on both paths**

Started at 03:22 UTC, about two hours after the list entry was saved.

| Path | initialize | tools | read | create | read back |
|---|---|---|---|---|---|
| Local proxy (`dataverse mcp`, own federated profile) | pass | 15 | pass | pass | pass |
| Remote `/api/mcp`, app-only token | pass | 15 | pass | pass | pass |

- **`--validate`** now says "GA endpoint is valid, but Preview endpoint is not configured" (the Preview toggle is off, as intended).
- **Servers:** the local proxy reports `dataverse 1.0.88.0` with capabilities logging, prompts, resources and tools; the remote endpoint reports `Microsoft Dataverse MCP Server 1.0.0` with tools only. Both list the same 15 tools: `commit_file_upload`, `create_record`, `create_skill_resource`, `create_table`, `delete_record`, `delete_skill`, `delete_table`, `describe`, `file_download`, `init_file_upload`, `read_query`, `search`, `update_record`, `update_table`, `upsert_skill`. Against Microsoft's list: no `search_data` (it needs Dataverse search on), no `invoke_api`, and an undocumented `create_skill_resource`.
- **Argument names:** `read_query` takes `querytext` (string, required) and `top` (integer, optional). `create_record` takes `tablename` (string) and `item` (an **object** of column values, not a JSON string).
- **Read:** `SELECT TOP 1 name FROM organization` returned `factory-lane-1` on both paths.
- **Create:** `create_record` on `account` replied "Created record with ID <guid>" on both paths; the read-back by name found each row.
- **Who made the rows:** the clean-up found both by `_createdby_value` = `getai-fl1-exec`'s application user. So MCP writes are attributed to the lane's own identity, which keeps audit per lane.
- **Billing:** neither the reads nor the creates were refused, though no Copilot Credit source was set up for `factory-lane-1`. Whether they were metered is not checked yet. **Checked 13 November 2026: they were metered** (section "Billing check" below).
- **Clean-up:** "Probe rows created by this app user: 2", each deleted with HTTP 204, "Probe rows left: 0". Checked again afterwards, read-only under Boroon's own sign-in: no `account` row starting `spike-0.3`, and the `account` table is empty.
- No token-shaped string (`eyJ`) in the log. Profiles cleared.

## Clean-up after the spike

**Done 6 November 2026, at Boroon's word:**

- The two test rows: deleted by run 3's clean-up step; checked again read-only under Boroon's sign-in (no `spike-0.3` row; `account` empty).
- The scratch repo `GetAI-IP/mcp-probe`, with its `fl1-exec` environment and three runs: deleted after a last look; returns 404.
- The federated credential `mcp-probe-fl1-exec`: deleted with `az ad app federated-credential delete`; `getai-fl1-exec` has no federated credentials, secrets or certificates.
- The allowed MCP client entry `new_getaifl1exec`: **kept for Stage 3** (Boroon's choice). It grants nothing while the app has no credential. To return to the state before the spike, delete it in Advanced Settings (the list before is in step B).
- Kept for the night shift (Stage 3): `getai-fl1-exec`, its application user and `factory-lane-1`.
