# Spike 0.2: GHE.com OIDC with pac

Plan section 11.1, row 0.2. Session 12, 4 November 2026. The result is in `docs/progress.md` (Session 12).

Exit test: `pac org who` returns the application user in both cases: a job started by hand, and the same job inside a ruleset workflow.

## What runs where

| Thing | Where | State |
|---|---|---|
| `probe.yml` | `GetAI-IP/oidc-probe` (private, scratch), `.github/workflows/probe.yml` | Pushed 4 November 2026 |
| `required.yml` | Same repo, `.github/workflows/required.yml`. The copy here has placeholders for the three IDs | Pushed 4 November 2026 (`ac9b369`) |
| `oidc-probe-target` | `GetAI-IP/oidc-probe-target` (private, scratch, repo 5328491). Holds the test pull request for step 5 (PR 1, never merged). No workflows | Created 4 November 2026 |
| Org ruleset `oidc-probe-required` | `GetAI-IP`, id 50511, targets `oidc-probe-target` only, by repository ID | Active since 4 November 2026 |
| Entra app `getai-fl1-exec` | GET AI tenant. Two federated credentials | Created by Boroon, 4 November 2026 |
| Environment `factory-lane-1` | Power Platform, Australia, Sandbox, Managed. Application user `getai-fl1-exec`, System Administrator | Created by Boroon, 4 November 2026 |

**Result: pass** (4 November 2026). `pac org who` returned the application user in both cases.

Neither workflow checks anything out, so no pull request code runs (rule 5). Ruleset workflows run only on `pull_request`, `pull_request_target` or `merge_group` (GitHub docs, `ruleset-workflow-event-triggers`), so step 5 uses `pull_request`; GitHub reads `required.yml` and `probe.yml` from `main` of `oidc-probe`, not from the pull request.

pac is 2.4.1, the gate's pin. It ships for `net10.0` only (NuGet catalogue, read 4 November 2026), so the probe sets up .NET 10.0.x. The gate's `lcp-gate.yml` sets up 8.0.x, which looks wrong: a finding for the gate, not fixed here.

## Portal steps (Boroon)

Order matters: the subject must come from a real run before the credential is made, because Entra accepts a wrong subject and then fails the exchange without an error.

### A. Entra app registration

Needs: Application Developer, Cloud Application Administrator or Application Administrator (or app registration open to users). The creator becomes the owner and can add federated credentials.

1. https://entra.microsoft.com, Entra ID, App registrations, New registration.
2. Name `getai-fl1-exec`. Supported account types: this organisational directory only (single tenant). Redirect URI: leave empty. Register.
3. Overview: copy the Application (client) ID and the Directory (tenant) ID.
4. API permissions: add nothing. App-only sign-in to Dataverse is authorised by the application user (step C), not by an API permission.
5. Certificates & secrets, Federated credentials tab, Add credential:
   - Federated credential scenario: **Other issuer**
   - Issuer: `https://token.actions.getai.ghe.com`
   - Type: **Explicit subject identifier**
   - Value: the `sub` the probe printed (case 1 below)
   - Name: as below. It cannot be changed later
   - Description (optional, not checked by Entra): `Spike 0.2 scratch. GitHub Actions OIDC from getai.ghe.com, repo GetAI-IP/oidc-probe, environment fl1-exec. Remove after the spike.`
   - Audience: `api://AzureADTokenExchange` (the default)
   - Add. No client secret, no certificate.

### B. Environment `factory-lane-1`

Needs: Power Platform Administrator or Dynamics 365 Administrator, 1 GB free Dataverse database capacity, and a tenant policy that allows creation.

1. https://admin.powerplatform.microsoft.com, Manage, Environments, New.
2. Name `factory-lane-1`. Region Australia. Get new features early: No. Type **Sandbox**. Purpose: "Factory lane 1. Spike 0.2 first". Add a Dataverse data store: Yes. Pay-as-you-go with Azure: No. Next.
3. Language English. URL `factory-lane-1` (if taken, `getai-factory-lane-1`). Currency AUD. Enable Dynamics 365 apps: No. Deploy sample apps and data: No. Security group: a group of factory admins only if one exists, otherwise None (application users do not need to be in it). Save, and wait until the state is Ready.
4. Select `factory-lane-1` on the Environments list, then **Enable Managed Environments** on the command bar. Keep the defaults. Enable.
5. Copy the Environment URL from Details. It should be `https://<name>.crm6.dynamics.com/`.

### C. Application user

Needs: System Administrator in `factory-lane-1` (the admin who made it has this), or Power Platform Administrator.

1. `factory-lane-1`, Settings, Users + permissions, Application users, New app user.
2. Add an app, find `getai-fl1-exec`, Add. Business unit: the root one. Security roles: **System Administrator** (plan 5.3: lower roles cannot deploy plug-ins; limit by scope, not role). Create.

## Case 1: started by hand

- Subject seen (run 36381961, 4 November 2026): `repo:GetAI-IP@801576/oidc-probe@5328416:environment:fl1-exec`. The repo was made after 15 July 2026, so GitHub uses the immutable form with the owner and repo IDs.
- Credential name: `oidc-probe-fl1-exec`.
- Run: `gh workflow run probe.yml -R GetAI-IP/oidc-probe --ref main -f tenant_id=... -f app_id=... -f env_url=...` (with `GH_HOST=getai.ghe.com`).
- **Passed** (run 36384161, 4 November 2026): `'<app id>' authenticated successfully`, `Connected to... factory-lane-1`, and `pac org who` showed `Connected as <app id>` with the application user's User ID. pac 2.4.1 on .NET 10.0.14.

## Case 2: inside a ruleset workflow

Each step needs Boroon's word first.

1. Create `GetAI-IP/oidc-probe-target`, private, with a README on `main`.
2. `oidc-probe`: Settings, Actions, General, Access: accessible from repositories in the `GetAI-IP` organisation.
3. `oidc-probe-target`: OIDC subject template `{"use_default": false, "include_claim_keys": ["repo", "context", "job_workflow_ref"]}` (repo-level only; no org template exists).
4. Push `required.yml` to `oidc-probe` `main` with the three real values.
5. Org ruleset `oidc-probe-required` in `GetAI-IP`: target branch `~DEFAULT_BRANCH`, condition `repository_id` = `oidc-probe-target` only, rule `workflows` with `.github/workflows/required.yml` at `refs/heads/main` from `oidc-probe`, active, no bypass.
6. Open a pull request in `oidc-probe-target`. Its first run prints the subject; pac fails because no credential exists yet.
7. Boroon adds a second credential on `getai-fl1-exec`, name `oidc-probe-target-ruleset`, with that subject. Expected shape: `repo:GetAI-IP@801576/oidc-probe-target@<id>:environment:fl1-exec:job_workflow_ref:GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`.
8. Re-run the failed job.

Seen so far (4 November 2026): steps 1 to 6 done. `oidc-probe-target` is repo 5328491; the ruleset is id 50511. First ruleset run 36385301 (event `pull_request`, `ref` `refs/pull/1/merge`) failed at the sign-in as expected, with `AADSTS700213: No matching federated identity record found for presented assertion subject '...'`. So Entra does name the subject it was shown, at least through pac. Claims:

- `sub`: `repo:GetAI-IP@801576/oidc-probe-target@5328491:environment:fl1-exec:job_workflow_ref:GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`
- `job_workflow_ref`: `GetAI-IP/oidc-probe/.github/workflows/probe.yml@refs/heads/main`. It names the central reusable workflow, not the caller: check (c), within one org
- `workflow_ref`: `GetAI-IP_tqa7h098/oidc-probe/.github/workflows/required.yml@refs/heads/main`. This one carries the enterprise suffix `_tqa7h098` on the org; `sub` and `job_workflow_ref` do not
- `gh run view` cannot show a ruleset run (it looks for the workflow in the target repo and gets 404). Read it with `gh api repos/<target>/actions/runs/<id>/jobs` and `.../actions/jobs/<id>/logs`

**Passed** on attempt 3 of run 36385301: `pac org who` returned the same application user as case 1. Attempt 2, seconds after the second credential was saved, failed with the same `AADSTS700213`, though the saved subject, issuer and audience matched byte for byte; about four minutes later it worked. **Wait about five minutes after saving a new credential.**

## Clean-up after the spike

Delete the ruleset, both scratch repos and both federated credentials. Keep `getai-fl1-exec`, its application user and `factory-lane-1` for the night shift (Stage 3), when the real lane workflow gets its own credential.
