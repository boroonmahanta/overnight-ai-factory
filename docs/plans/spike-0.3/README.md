# Spike 0.3: Dataverse MCP with an app-only token

Plan section 11.1, row 0.3. Session 13, 5 November 2026. The result goes in `docs/progress.md` (Session 13).

Exit test: a read and a create succeed headless. Record which of the two paths work:

1. **Local proxy.** A job on `getai.ghe.com` signs in as `getai-fl1-exec` with a federated pac profile (as in spike 0.2), then runs the Dataverse CLI's MCP proxy (`dataverse mcp <url>`, the same thing `npx @microsoft/dataverse mcp <url>` runs) against `factory-lane-1`, and makes one read and one create through it.
2. **Remote endpoint.** With `getai-fl1-exec` on `factory-lane-1`'s allowed MCP clients list, the same read and create against `https://<org>/api/mcp` with an app-only token.

If both fail, record what broke and stop. The fallback (the night stays on pac and trusted Web API scripts) is for a later session.

## What runs where

| Thing | Where | State |
|---|---|---|
| `probe.yml` | `GetAI-IP/mcp-probe` (private, scratch, repo 5331556), `.github/workflows/probe.yml` | Pushed 5 November 2026 (`4ab9682`), at Boroon's word |
| `mcp_probe.py` | Same repo, `probe/mcp_probe.py` | Pushed with it |
| Entra app `getai-fl1-exec` | GET AI tenant. Kept from spike 0.2. No credentials now | Exists |
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
   - Application (client) ID: `getai-fl1-exec`'s Application (client) ID
   - **Is Enabled**: Yes
3. **Save & Close**. Give it five minutes before run 3 (a cache delay is likely; Microsoft documents about five minutes for the Finance and Operations list).

### D. Only if a run asks for it

- A Copilot Credit source for `factory-lane-1` (a pay-as-you-go billing policy with an Azure subscription, or prepaid capacity), if a tool call is refused for billing. A tenant setting: stop and decide.
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

## Clean-up after the spike

Delete the scratch repo `GetAI-IP/mcp-probe` (with its `fl1-exec` environment) and the federated credential `mcp-probe-fl1-exec`. Decide whether `getai-fl1-exec` stays on the allowed MCP clients list (only if the night will use MCP). Check no `spike-0.3 probe` row is left in `factory-lane-1`. Keep `getai-fl1-exec`, its application user and `factory-lane-1` for the night shift (Stage 3).
