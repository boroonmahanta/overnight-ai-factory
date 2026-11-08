# Spike 0.18: headless YAML export as the lane identity

Plan section 11.1, row 0.18 (ADO 2462). Session 19, 8 November 2026. The result is in `docs/progress.md` (Session 19).

**Result: the YAML exit test fails; the plan's fallback, the XML layout, passes every check** (runs 37180916 and 37181366, 8 November 2026). On a runner, signed in as `getai-fl1-exec` with no secret, `pac solution export` and `unpack`, `clone` and `sync` all worked headless, on pac 2.14.1 and on the gate's pin, 2.4.1. None of them wrote YAML: every extract was the XML layout (`Other/Solution.xml`). The XML tree held all five parts, packed again signed out and with no network, unpacked from the repack to the same files, and a second export gave byte-identical files. Findings below.

Exit test (plan 11.1): on a runner, as `getai-fl1-exec`, `pac solution export` then `unpack`, and `pac solution clone` and `sync`, for a solution holding a table, a flow, a security role, an environment variable and a connection reference. Pass if the output is the YAML format, packs offline again with `pac solution pack`, and a second export gives the same canonical files. If it fails, the plan's fallback is the XML layout for flows and tables, with canvas apps kept out of the night (plan 5.6, risk 12).

## What runs where

| Thing | Where | State |
|---|---|---|
| `probe.yml` | `GetAI-IP/export-probe` (private, scratch, repo 5352096), `.github/workflows/probe.yml` | Pushed 8 November 2026 (`b41b1a2`, last `1dcf2e9`). Scratch |
| `export_probe.py` | Same repo, `probe/export_probe.py` | Pushed with it. Scratch |
| GitHub environment `fl1-exec` | In that repo, made by the first run, no protection rules | Scratch |
| Federated credential `export-probe-fl1-exec` | On `getai-fl1-exec`, subject `repo:GetAI-IP@801576/export-probe@5352096:environment:fl1-exec` | Added by Boroon 8 November 2026; read back at 06:05 UTC. Scratch |
| Test solution `FactorySpike` and its parts | `factory-lane-1` (list under "Scratch to delete") | Made by run 37180771. Scratch |
| Entra app `getai-fl1-exec`, its application user, `factory-lane-1` | GET AI tenant | Exist; kept for Stage 3 |

## How the probe works

One job per pac version, `workflow_dispatch` only, and it refuses any ref but `main`. It checks out its own repo at the dispatched commit, never pull request code (rule 5). Permissions `id-token: write` and `contents: read`. No secrets: the tenant ID, app ID and Dataverse URL come in as inputs, so they stay out of this public repo. The job runs in the GitHub environment `fl1-exec`, as plan 5.3 has it. Actions are pinned to the gate's commit SHAs. pac is installed at a pinned version with `dotnet tool install` on .NET `10.0.x`, telemetry off.

Modes:

1. **`claims`:** print the OIDC claims, never the token. Proves the installs.
2. **`setup`:** through the Web API, as the lane's app user (an app-only token with the GitHub OIDC token as the client assertion), make the test solution the way an agent would build live (plan 5.6): publisher `factoryspike` (prefix `fspk`), solution `FactorySpike`, table `fspk_spikeitem` with one extra column, connection reference `fspk_spikedataverse` (Dataverse connector, no connection), environment variable `fspk_SpikeSetting` (text, with a default value), cloud flow "Factory spike flow" (manual trigger, one Dataverse action through the connection reference, left off) and security role "Factory spike role" (read, write and create on the table). Each create carries the `MSCRM.SolutionUniqueName` header; the script then checks every part is a solution component and would add any that is not. It publishes at the end. Safe to run again: it makes only what is missing.
3. **`probe`:** a matrix, pac 2.14.1 (latest, 21 October 2026) then 2.4.1 (the gate's pin), one after the other. Sign in with `pac auth create --githubFederated`, then:
   - two rounds of `export` (unmanaged), `unpack` and `clone` (`--packagetype Unmanaged`);
   - when a clone is YAML, `unpack` into a copy of it, to see whether unpack keeps the layout it finds (not reached: no clone was YAML);
   - `sync` after a change in the lane (the environment variable's description, through the Web API), then `sync` after the change is undone;
   - `pac auth clear`, then `pac solution pack` of each tree, once normally and once inside `sudo unshare --net` (a sandbox with no network, checked first: `curl` to the sign-in host must fail there);
   - unpack each repack and compare it with the unpack of the export; compare the zips' member names and root components.
   It writes `results.json` and uploads the work folder as a three-day artifact (scratch files only, no credentials).
4. **`envvar-repro`:** added after run 3 (see finding 6).
5. **`teardown`:** deletes what setup made, children first, each matched by its scratch name. Not run: only at Boroon's word.

Trees are compared file by file, first byte for byte, then in a canonical form (UTF-8 BOM removed, line endings LF, trailing spaces trimmed), with a short diff kept for any file that still differs.

Local checks before any run (8 November 2026, scratch harness, not committed): the script compiled; the probe ran end to end on the laptop against a stand-in `pac` that faked export, clone and sync and passed `unpack` and `pack` to the laptop's real pac 2.14.1, with an empty solution built by `pac solution init` and `dotnet build`. Both branches ran, a clone that is XML and one that is YAML. The harness caught one bug (a failed `sudo` read as "no network"), fixed before any run. The Web API code was not covered by the harness; run 2 caught a missing URL encoding (below).

## Found before any run (read-only)

- **Microsoft's pages disagree.** The YAML format reference says the format is written when you "Extract solutions using `pac solution clone` or `pac solution sync`", and recommends `clone` to "Obtain a complete YAML folder from Dataverse". The Git integration FAQ says the `unpack`, `clone` and `sync` commands "don't currently support YAML format". The `pac solution` reference says `unpack` writes XML by default, and that folders "extracted by using `pac solution clone`" use YAML. None of the three commands has a format option in pac 2.14.1's own help.
- **pac moved ten releases past the gate's pin.** The gate pins 2.4.1 (the first version with YAML support, per Microsoft). NuGet's latest is 2.14.1 (21 October 2026); 2.13.1 came 7 October, 2.12.2 on 11 September. The laptop's copy (from the VS Code extension) is 2.14.1.
- **pac 2.14.1's packager reads YAML but cannot write it.** In `SolutionPackagerLib.dll` (the code behind `pack` and `unpack`), the YAML pieces are `ConvertYamlToXml`, `ConvertYamlToJson` and `YamlToXmlStreamReader`, plus the YAML file names it reads; nothing converts XML to YAML. `bolt.module.solution.dll` (the code behind `clone` and `sync`) holds no YAML strings at all. So the FAQ looked right before the runs. An inference from the binary; the runs confirm it.
- **The only YAML writer Microsoft documents is native Dataverse Git integration**, which the plan does not use for the factory yet (plan 5.6: public preview for GitHub, developer environments only, GitHub App and Key Vault, no source says it supports GHE.com).

## Findings (after runs 3 and 5, 8 November 2026)

1. **No headless pac command writes YAML, on 2.14.1 or 2.4.1.** `export` then `unpack`, and `clone`, each gave the XML layout (`Other/Solution.xml`, `Other/Customizations.xml`, `Entities/`, `Workflows/`, `Roles/`, `environmentvariabledefinitions/`), in both rounds, on both versions. `sync` kept the XML layout too. The format reference is wrong, or ahead of the tool; the Git integration FAQ is right. The YAML exit test fails.
2. **The XML layout passes every check the exit test sets,** on both versions, as the lane identity, headless:
   - all five parts are in the tree: the table (`Entities/fspk_SpikeItem/`, with its forms and views), the flow (`Workflows/Factoryspikeflow-<id>.json` and its `.json.data.xml`), the role (`Roles/Factory spike role.xml`), the environment variable (`environmentvariabledefinitions/fspk_SpikeSetting/environmentvariabledefinition.xml`) and the connection reference (in `Other/Customizations.xml`, and named in the flow's JSON);
   - `pac solution pack` worked after `pac auth clear`, and again inside a sandbox with no network (`curl` exit 6, cannot resolve host), with the same root components as the export;
   - unpacking the repacked zip gave files identical to unpacking the export;
   - a second export minutes later gave **byte-identical** files, before any canonical form, and so did a run ten minutes apart. No timestamps or run-specific values in the unpacked files.
3. **`clone` adds nothing for the driver.** Its `src/` folder is byte-for-byte the export's `unpack`; it adds `FactorySpike.cdsproj` and a `.gitignore`. It takes about as long (about 9 seconds, against about 10 for export and unpack together). Export then unpack keeps the zip as evidence and has no project file to maintain.
4. **pac 2.14.1 and 2.4.1 wrote identical files.** Moving the gate's pin changes nothing in the output for these five component types.
5. **`sync` follows a change in the lane.** After the environment variable's description changed through the Web API, `sync` changed exactly that one file; after the change was undone, `sync` returned the tree to equal the first clone. It needs the `.cdsproj` that `clone` writes.
6. **A one-column Web API update on an environment variable definition clears its default value.** Run 3's sync test changed only `description`; the next export had no `<defaultvalue>`, and the row's `defaultvalue` was empty (read under Boroon's sign-in). The repro (run 37181326, as the lane identity): setting `defaultvalue` alone kept the description; setting `description` alone cleared `defaultvalue`; setting both kept both. So an agent or helper script that updates an environment variable must send the default value with every update. The export showed the loss as a removed line, which is what the drift check and the PR's removal list are for (plan 5.6). The default value is restored.
7. **Setup by code works as the lane identity.** The Web API made the publisher, solution, table and column, connection reference, environment variable, flow and role as `getai-fl1-exec`, in about 70 seconds. The `MSCRM.SolutionUniqueName` header put all five components in the solution; no `AddSolutionComponent` was needed. A cloud flow was accepted with a connection reference that has no connection (it stays off). In this org the connection reference's solution component type is 10167 (an org-specific type code), the others the fixed 1, 20, 29 and 380.
8. **Timings on a hosted runner,** for this small solution: export about 9 seconds (23 seconds the first time on a fresh runner), unpack about 1, clone about 9, sync about 9, pack about 1.
9. **What a canonical compare needs, so far: nothing,** for these five types. Two expected sources of churn were not seen and stay untested: the server version stamp in `Other/Solution.xml` and `Other/Customizations.xml` (`version="9.2.26101.184"` and `OrganizationVersion`), which will change when Microsoft updates the environment [inference], and canvas apps, forms edited in the designer, and plug-ins, which were not in the solution.
10. **The repacked zip's `solution.xml` and `customizations.xml` differ in bytes from the export's,** with the same member names and root components. Pack re-serialises them. So compare unpacked trees, never zips.
11. **The OIDC subject is the immutable form again:** `repo:GetAI-IP@801576/export-probe@5352096:environment:fl1-exec`, as in spikes 0.2 and 0.3.

Not tested: managed export; `clone --packagetype Both` (the default); canvas apps, model-driven apps, plug-ins and Copilot Studio agents; a solution large enough to need `--async`; whether `pack` of an XML tree drops a component silently when its files are missing, as Microsoft documents for YAML (plan 5.6's manifest check assumes `rootcomponents.yml`; in the XML layout the root components are in `Other/Solution.xml`).

## Portal steps (Boroon)

### A. Federated credential on `getai-fl1-exec` (after run 1)

As spike 0.3, step A, with:

- Value: `repo:GetAI-IP@801576/export-probe@5352096:environment:fl1-exec` (from run 1)
- Name: `export-probe-fl1-exec`
- Description: `Spike 0.18 scratch. GitHub Actions OIDC from getai.ghe.com, repo GetAI-IP/export-probe, environment fl1-exec. Remove after spikes 0.18 and 0.19.`

Done 8 November 2026. Read back (read-only, `az ad app federated-credential list`) at 06:05 UTC: one credential, name, issuer `https://token.actions.getai.ghe.com`, subject and audience `api://AzureADTokenExchange` all as above; no secrets or certificates.

No other portal step was needed.

## Run order and results

Runs start with `GH_HOST=getai.ghe.com gh workflow run probe.yml -R GetAI-IP/export-probe --ref main -f mode=<mode> -f tenant_id=... -f app_id=... -f env_url=https://factory-lane-1.crm6.dynamics.com/`. Run 1 passes only `mode=claims`.

| Run | ID | Mode | Result |
|---|---|---|---|
| 1 | 37178901 | claims | Pass. `sub` as above; `job_workflow_ref` `GetAI-IP/export-probe/.github/workflows/probe.yml@refs/heads/main`; pac 2.14.1 installed |
| 2 | 37180581 | setup | Failed in the probe's own code before any write: the OData `$filter` had raw spaces, which Python's HTTP client refuses. The sign-in had worked (WhoAmI, organisation `factory-lane-1`, language 1033). Fixed in `b1bdfc0` |
| 2a | 37180771 | setup | Pass. All seven parts made; all five components in the solution |
| 3 | 37180916 | probe | Both versions: YAML fails, XML passes. The sync test cleared the environment variable's default value (finding 6), so pac 2.4.1's job started without it |
| 4 | 37181326 | envvar-repro | Reproduced finding 6 as the lane identity; default value restored |
| 5 | 37181366 | probe | Both versions, with the sync test sending the default value too: YAML fails; XML passes every check; sync returns to equal after the undo |

Each probe job ran in 1.3 to 1.8 minutes, install included. No token-shaped string (`eyJ`) in any of the six run logs (the scripts never print a token; the claims step prints claims only).

## What this means for the plan

Edited into the plan on 8 November 2026, at Boroon's word ("Yes, edit now"): sections 5.6 (format, the export result, the driver's method, the manifest check), 8.1, 11.1 row 0.18, 12 risk 12, 14.4, 15.1, Appendix A (the pack step's name), B.1 (the folder names) and C.1 (the executor rule).

- **Low-code lane repos use the XML layout** (the plan's fallback), one format per repo. The driver runs `pac solution export` then `pac solution unpack`, not `clone`. Canvas apps stay out of the night, as before.
- **Environment variable updates send the default value every time** (finding 6): in plan 5.6 for the trusted Web API helper scripts, and in the executor's instructions (C.1).
- **Recheck YAML at each pac release and Microsoft event** (A1): the day pac writes YAML headless, a new project may start on it. Existing repos stay on XML until a quiet week.

Left for `GetAI-IP/factory-gates` (the follow-up list in `docs/progress.md`, for 2511 and 2538), not changed here:

- `lcp/pack_offline.py` calls its source "the YAML-format solution folder" and `lcp-gate.yml` names its step "YAML source format": both to the XML layout.
- The manifest check reads the root components from `Other/Solution.xml` in the XML layout, not `rootcomponents.yml`.
- `danger-rules.yml` maps the B.1 rows to the XML folders; connection references come from the export-diff plan, not a path.
- The pac pin can move from 2.4.1 to 2.14.1: the output was identical for these five types. Read its release notes first (A1).

## Scratch to delete (only at Boroon's word)

**Kept until spike 0.19 is written up** (Boroon, 8 November 2026): 0.19 reuses the solution as its baseline, and the repo and credential to run as the lane identity. Then delete all of it, at his word.

| Thing | Where | How |
|---|---|---|
| Solution `FactorySpike` with: table `fspk_spikeitem`, cloud flow "Factory spike flow", security role "Factory spike role", environment variable `fspk_SpikeSetting`, connection reference `fspk_spikedataverse` | `factory-lane-1` | `mode=teardown` (deletes the parts, then the solution, then the publisher) |
| Publisher `factoryspike` (prefix `fspk`) | `factory-lane-1` | The same teardown run |
| Repo `GetAI-IP/export-probe`, with its `fl1-exec` environment, runs and artifacts (artifacts expire after three days) | `getai.ghe.com` | `gh repo delete GetAI-IP/export-probe` (after teardown, which runs from it) |
| Federated credential `export-probe-fl1-exec` | `getai-fl1-exec` in Entra | `az ad app federated-credential delete`, or the portal |

Kept for Stage 3, as before: `getai-fl1-exec`, its application user, `factory-lane-1` and the allowed MCP client `new_getaifl1exec`.
