# `factory-test`: the Test environment, its Test identity and its test user

ADO 2541 (Feature 2540, Stage 1). Plan 5.3 (identities), 5.4 (the environment pool, bootstrap) and 11.2 (stage 1). Session 46, Tuesday 24 November 2026, on the laptop (desktop app). The first project is the Northwind pilot, project code **`nwt`** (Boroon, 24 November 2026).

**Where it stands: the environment and the Test identity exist; the test user, the Key Vault and the federated credentials wait on other people.** Boroon has sent the admins the message below (he said so on 24 November 2026, Session 49). Checked that evening: the test user, the group `factory-cba-test-users` and the resource group `rg-getai-factory-aue` do not exist yet. The IDs (environment, organisation, app, service principal, tenant) are in ADO 2541, not here, because this repo is public.

## What exists now

| Thing | Value | Made | Read back |
|---|---|---|---|
| Environment | `factory-test`, `https://factory-test.crm6.dynamics.com/`. Sandbox, region Australia (Azure region `australiaeast`), currency AUD, English, Dataverse 9.2. No security group, no Dynamics 365 apps, no sample data | `pac admin create`, as Boroon, 24 November 2026. Took under a minute | Admin API: state Enabled, Sandbox |
| Managed Environment | Protection level Standard, solution checker **Block** | `pac admin set-governance-config` | Admin API `governanceConfiguration`: `Standard`, `solutionCheckerMode: block` |
| Auditing | On for the organisation and for the Workflows table (`workflow`). **Not** for the Connection reference table: its audit setting cannot be changed (`IsAuditEnabled.CanBeChanged` is false) | Web API as Boroon: `organizations.isauditenabled`, the `workflow` table definition, then publish | Web API: both `true` |
| Test identity | Entra app `getai-nwt-test`, single tenant, with its service principal. No secret, no certificate, no API permission, no federated credential yet, no owner (Cloud Application Administrators manage it). Notes: "Factory Test identity, project nwt. factory-test only. Federated credentials only, no secrets." | `az ad app create`, `az ad sp create`, as Boroon | `az ad app show`: 0 secrets, 0 certificates, 0 permissions, 0 credentials |
| Application user | `getai-nwt-test` in `factory-test`, root business unit, **System Administrator**, access mode non-interactive, enabled | `pac admin assign-user --application-user` | Web API: one user, the one role |
| Lane identity | `getai-fl1-exec` has **no** user in `factory-test` (plan 5.3: the execute identity can never exist in Test) | | Web API: 0 users |

Not done in this environment, on purpose:

- **No Dataverse MCP, no "Enable code apps", no connections.** Test runs the gate's trusted checks, not an agent; turn them on only when a story needs them.
- **No Northwind import.** DG9's step 1 says to import Northwind into `factory-test` "if 2541 has not". 2541 has not, and should not as an unmanaged import: the gate imports each PR's managed solution into Test (`--stage-and-upgrade`), and an unmanaged copy underneath would leave an unmanaged layer (plan 7.4 lists unmanaged layers in `factory-test` as a gardening finding). Northwind reaches Test through the gate, as a managed solution, in 2459 or 2539. **Confirmed by Boroon on 24 November 2026 (Session 49): gate only, never a hand-made unmanaged import.** DG9's step 1 in `docs/plans/stage-1-day-gate-plan.md` now says so.

## How it was made (reuse for the next project or lane)

Signed in as Boroon (Power Platform Administrator, Cloud Application Administrator), pac 2.15.1, Azure CLI 2.88.0.

```bash
pac admin create --name factory-test --type Sandbox --region australia --currency AUD --domain factory-test
pac admin set-governance-config --environment <environment id> --protection-level Standard --solution-checker-mode block
az ad app create --display-name getai-nwt-test --sign-in-audience AzureADMyOrg
az ad app update --id <app id> --set notes="Factory Test identity, project nwt. factory-test only. Federated credentials only, no secrets."
az ad sp create --id <app id>
pac admin assign-user --environment <environment id> --user <app id> --role "System Administrator" --application-user
```

Auditing: a Web API `PATCH` of `organizations(<id>)` with `isauditenabled: true`; a `GET` of `EntityDefinitions(LogicalName='workflow')`, `IsAuditEnabled.Value` set to `true`, a `PUT` back with `MSCRM.MergeLabels: true`, then `PublishXml` for `workflow`. The token came from `az account get-access-token --resource https://factory-test.crm6.dynamics.com`.

## Findings

1. **One admin API version read the old protection level.** Right after `set-governance-config`, the environment read `Basic` from `api.bap.microsoft.com` with `api-version=2021-04-01` without `$expand`, and with `2023-06-01`. With `$expand=properties.governanceConfiguration`, both versions then read `Standard` and `block`. The preflight check (plan 5.4, "Managed Environment on, checker mode as expected") should read it with the `$expand`.
2. **The Connection reference table's auditing cannot be turned on here.** Plan 5.3 says to turn on auditing for the Workflows and Connection reference tables. In `factory-test`, `connectionreference` has `IsAuditEnabled.CanBeChanged: false`. Organisation and Workflows auditing are on. A plan edit, at Boroon's word, would say so.
3. **Microsoft's Build Tools page no longer lists API permissions.** Plan 5.3 gives the Test identity "App permissions: Dynamics CRM and PowerApps-Advisor `Analysis.All`" from that page. Read today, the page asks only for an application user with a role holding `prvAppendmsdyn_analysisjob` (System Administrator has it), and says nothing about API permissions. So none are added. If `pac solution check` fails for the Test identity in 2459 or 2539, add PowerApps-Advisor `Analysis.All` and grant consent then (a Cloud Application Administrator can, for an API other than Microsoft Graph).
4. **The gate's Playwright step does not pass what Microsoft's toolkit reads.** `lcp-gate.yml` (`verify-in-test`, "Locked Playwright suite") sets `MS_AUTH_CREDENTIAL_TYPE`, `MS_AUTH_CREDENTIAL_PROVIDER` and `KEYVAULT_NAME`. Microsoft's authentication guide for Key Vault uses `MS_AUTH_EMAIL`, `AZURE_KEYVAULT_URL`, `AZURE_CERTIFICATE_NAME` and `AZURE_TENANT_ID`. The gate's `gate/playwright` config does not exist yet, so it may map them; settle it in 2546 (the kit) and 2447 (spike 0.11).
5. **Boroon's account cannot do the rest alone.** It holds Power Platform Administrator and Cloud Application Administrator in Entra, and only Reader on the CSP Azure subscription. So the test user, its licence, certificate sign-in and the Key Vault need other admins (below). It cannot read the authentication methods policy or the Conditional Access policies, so whether certificate sign-in is already on in the tenant is unknown.
6. **Licences:** the tenant has 25 Power Apps Premium (`POWERAPPS_PER_USER`) licences, 6 in use (read 24 November 2026). One goes to the test user (plan 5.14: Test is a Managed Environment).
7. **No story made the Northwind project repo, the Key Vault or the evidence Blob.** 2539 needs a project repo for its human PR, and `verify-in-test` needs the vault (test user certificate) and Blob (evidence, rule 16). **Now ADO 3059** (the Northwind project repo, under Feature 2536, before 2539) **and ADO 3060** (Key Vault and evidence storage, under Feature 2540, before 2447 and 2539), added at Boroon's word on 24 November 2026, Proposed and not dated.
8. **Who writes evidence to Blob is not settled.** Plan 5.1's table names an "evidence-writer managed identity", but the gate's "Copy evidence to Blob" step runs `az storage blob upload-batch --auth-mode login` as the Test identity, into a container named by `PROJECT_ID`. ADO 3060 asks to pick one before the exit test.

## What waits, and on whom

### 1. The test user (the identity admins)

Plan 5.3: `factory-test-<proj>@<tenant>`, an Entra user with certificate sign-in, a business role, no maker rights, a premium licence, certificate in Key Vault.

1. **User** (User Administrator): `factory-test-nwt@getai.com.au`, display name "Factory test user (nwt)", cloud only, no mailbox needed. A long random password that nobody keeps: the user signs in only by certificate.
2. **Licence** (License Administrator or User Administrator): one Power Apps Premium.
3. **Group** (Groups Administrator or User Administrator): a security group `factory-cba-test-users` holding only factory test users (this one now, the lane test users at Stage 3).
4. **Trust store** (Privileged Authentication Administrator): a PKI container `factory-test-ca`, holding one root CA, the GET AI factory test CA, whose public certificate (`.cer`) we send. No CRL: it is a test CA; to revoke, delete the CA or disable the user. Microsoft warns that a CA in the trust store can authenticate any user if bindings are weak, hence steps 5 and 6.
5. **Certificate sign-in** (Authentication Policy Administrator): Authentication methods, Certificate-based authentication, Enable, target **only** `factory-cba-test-users`, never All users (Microsoft: users in scope with no certificate are locked out of other methods). If it is already on for other groups, add this group only.
6. **Binding rules** for this CA only (Authentication Policy Administrator), so the tenant defaults do not change:
   - an authentication binding rule on the issuer, the test CA's subject, with affinity **High**;
   - a username binding `IssuerAndSerialNumber` to `certificateUserIds`, and the user's `certificateUserIds` set to the value we send once the certificate exists (`X509:<I>{issuer}<SR>{serial}`);
   - **the strength is the admins' and Boroon's choice:** single-factor, plus a Conditional Access exclusion for the user if a policy requires MFA; or multifactor for this rule, so no exclusion is needed. Spike 0.11 (2447) tests whichever is chosen.
7. **Role in `factory-test`** (Boroon, once the user is licensed): `pac admin assign-user --environment <id> --user factory-test-nwt@getai.com.au --role "Basic User"`. Northwind's own role, if it has one, comes with its import.

### 2. The Key Vault (the Azure subscription's owner, then Boroon; ADO 3060)

1. **The owner** of `AzureCSP_GetAI_CloudandDataPlatforms` (Boroon's choice of subscription, 24 November 2026) makes a resource group `rg-getai-factory-aue` in Australia East and gives Boroon **Owner** on that group only. Evidence Blob storage (rule 16) can live there later.
2. **Boroon, by CLI** (the same way as above, asking before each create): a Key Vault `kv-getai-factory-aue` (Australia East, Azure RBAC, soft delete on); Boroon gets Key Vault Administrator on it; `getai-nwt-test` gets **Key Vault Certificate User** on the test user's certificate only (scoped to the certificate, not the vault).
3. **The certificate.** In the vault, a certificate `factory-test-nwt` with issuer "Unknown", subject `CN=factory-test-nwt`, the UPN in the subject alternative names, client authentication usage, an exportable RSA 3072 key, valid one year. The vault makes the key and a signing request; a throwaway test CA, made with `openssl` in the session scratchpad, signs it; the signed certificate is merged back. The CA's public certificate goes to the identity admins (step 1.4), and the issuer and serial go to them for `certificateUserIds` (step 1.6). **Boroon to decide then:** destroy the CA's private key after signing (safest: nothing can issue another certificate; renewal makes a new CA, which the admins upload again), or keep it in a separate vault only he can read.

### 3. The federated credentials (when the repos exist)

Plan 5.3: one credential per project repo, plus one for triage, because the subject names the repo where the run happens. Spike 0.2: take the subject from a real run first, then wait about five minutes.

- **The Northwind project repo, `AI-Business-Solutions/ai-factory-nwt`** (not made yet; ADO 3059; the name and the org are Boroon's, 24 November 2026). The gate lives in `GetAI-IP` and this repo in another org, so its first gate run is also the first across orgs: spike 0.2 tested `job_workflow_ref` within one org only, and the callers build (2531) may be needed for the ruleset to reach the repo. Its OIDC subject template must include `repo`, `context` and `job_workflow_ref`, and it needs a GitHub environment `lcp-test` holding the variables `verify-in-test` reads: `TENANT_ID`, `LCP_TEST_APP_ID` (the app ID of `getai-nwt-test`), `LCP_TEST_ENV_URL` (`https://factory-test.crm6.dynamics.com`), `PROJECT_ID` (`nwt`), `LCP_KEYVAULT` and `EVIDENCE_ACCOUNT`. Expected subject shape: `repo:AI-Business-Solutions@<org id>/ai-factory-nwt@<repo id>:environment:lcp-test:job_workflow_ref:GetAI-IP/factory-gates/.github/workflows/lcp-gate.yml@refs/heads/release`. Credential: Other issuer, `https://token.actions.getai.ghe.com`, audience `api://AzureADTokenExchange`.

### 4. The Northwind solution (ADO 3059)

Boroon, 24 November 2026: the solution comes from Microsoft's page "Install Northwind Traders database and apps" (https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/northwind-install).

- **The file:** `NorthwindTraders_final.zip`, from `download.microsoft.com` (the link is on that page), 666,816 bytes, last modified 29 January 2025. Headers read on 24 November 2026; not downloaded, which needs Boroon's word.
- **What it holds (Microsoft's page):** the tables, choices and business processes; the apps Northwind Orders (canvas) and Northwind Orders (model-driven); a canvas app, Northwind Sample Data, that loads the rows; and "Begin Part" canvas apps for the tutorial. The import asks to confirm SDK message handling.
- **Where it goes:** into a lane, not `factory-test`, then exported and unpacked into the repo's `src/`. Proposed: `factory-lane-1`, where `nwt`'s night stories will run, with the driver's export (unmanaged and managed, unpacked with `Both`, as 2459 tries). Whether the zip itself is managed or unmanaged shows in its `solution.xml` once downloaded.
- **Watch for:**
  - **Canvas apps.** The gate's manifest check fails closed on a folder it does not know, `CanvasApps/` among them. So the first export fails it until a reviewed gate PR adds the kind from this real export, or the repo's solution leaves the canvas apps out. Settle before 2539. (Canvas apps stay out of the night either way, plan 5.6.)
  - **Sample data is loaded by hand.** The Sample Data app asks the user to allow Dataverse access, so loading rows into `factory-test` is a day step for a person. Locked scenarios can seed their own rows with a run tag instead.
- **Triage** (plan 4.5): when its workflow exists in `factory-gates`, Stage 2 or later.
- **Spike 0.10 (2459, Wednesday 25 November)** needs to import into `factory-test`; if it runs from a scratch repo, that repo gets its own scratch credential on `getai-nwt-test`, deleted after the spike.

## Draft message to the admins

Names are in ADO 2541. Send at Boroon's word. **Sent by Boroon** (24 November 2026, Session 49); the admins' names are not yet in ADO 2541.

> Hi both,
>
> For GET AI's overnight factory I've set up a Test environment, `factory-test`, and I need two things I don't have the rights to do.
>
> **Entra (identity admins).** A test user that signs in by certificate only, for automated UI tests in `factory-test`:
> 1. Create `factory-test-nwt@getai.com.au` ("Factory test user (nwt)"), cloud only, with a random password nobody keeps, and give it one Power Apps Premium licence (we have spares).
> 2. Create a security group `factory-cba-test-users` with that user in it.
> 3. Trust store: create a PKI `factory-test-ca` and add our test root CA (I'll send its `.cer`), no CRL.
> 4. Certificate-based authentication: enable it for `factory-cba-test-users` only, not All users.
> 5. For our CA only: an issuer binding rule with High affinity, and an IssuerAndSerialNumber to `certificateUserIds` username binding; I'll send the user's `certificateUserIds` value once the certificate exists.
> 6. Tell me whether a Conditional Access policy would ask this user for MFA, and which you prefer: the rule set to multifactor, or a CA exclusion for this one user.
>
> **Azure (owner of the CSP subscription `AzureCSP_GetAI_CloudandDataPlatforms`).** Create a resource group `rg-getai-factory-aue` in Australia East and give me Owner on that group only. It will hold the factory's Key Vault.
>
> Steps and reasons: Microsoft's "Set up Microsoft Entra certificate-based authentication" page. Thanks!

## Clean-up

Nothing here is scratch: `factory-test`, `getai-nwt-test` and its application user stay for Stage 1 and after. A scratch credential made for spike 0.10 is deleted after that spike.
