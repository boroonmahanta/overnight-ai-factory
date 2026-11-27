# Spike 0.11: the test user signs in by certificate, headless in CI

Plan section 11.1, row 0.11 (ADO 2447). Session 61, Friday 27 November 2026, on the laptop (desktop app), laptop track B. Dated Thursday 26 November; the last Stage 0 spike the Stage 1 exit test (2539, Friday 27 November) needs.

**Result (27 November 2026, runs 41604351 to 41608426, 02:12 to 02:32 UTC): the certificate sign-in works, but the exit test does not pass yet. Two things stop it, and neither is Conditional Access:**

1. **A tenant rule stops the sign-in after the certificate.** Entra accepted the certificate and counted it as multifactor, then interrupted the sign-in to make the test user register for self-service password reset (SSPR): **AADSTS50125**, "Sign-in was interrupted due to a password reset or password registration entry", "User authentication was blocked because they need to provide password reset information" (Entra sign-in log, 02:21:46 UTC). The page says "Let's keep your account secure", with only a Next button. Conditional Access status: success, no policy applied. **Changed no policy and stopped**, as the brief says; the message for the identity team is below.
2. **`playwright-ms-auth` 0.0.19 cannot click the certificate link.** After the email, Entra shows "Enter password" with a link "Use a certificate or smart card". The package looks for it with Playwright's `isVisible`, which does not wait (Playwright's own docs: the timeout option "is ignored"), so it checks before the page is drawn, never clicks, and fails 1.7 minutes later on the sign-in page. So even once item 1 is fixed, the kit's sign-in step as written fails. The fix is a change to the kit, by its own gate PR (proposal 1).

What was proved:

- **The role is enough, and no wider** (point 1 of the brief). As `getai-nwt-test`, holding only Key Vault Secrets User on the secret `factory-test-nwt`, the job read the secret: `application/x-pkcs12`, enabled, valid 26 November 2026 to 26 November 2027, managed by the certificate, 3,556 bytes. Listing the vault's secrets and reading the certificate object were both refused (HTTP 403, `ForbiddenByRbac`). `playwright-ms-auth` read the same secret through the Azure CLI and took it as a certificate.
- **The certificate sign-in itself works headless, under the tenant's policies.** With waits (the `diagnose` mode), the certificate request to `certauth.login.microsoftonline.com` returned HTTP 200, and Entra's sign-in log shows: X.509 certificate, succeeded; "MFA requirement satisfied by certificate based authentication"; the binding `IssuerAndSerialNumber` to `certificateUserIds`, rank 4; affinity High; the authentication level multifactor, by the issuer rule; the CA's subject key identifier `84C7154B…`; the certificate's serial `04858E42…` and thumbprint `BD6F1F95…`, as in the `factory-test` README. No browser prompt, no password, `CI` set.
- **The Azure sign-in lasts at least 7 minutes.** With a 7-minute wait after `azure/login`, the Key Vault read still worked (run 41608426).
- **Not proved yet** (points 2 and 3 of the brief): a storage state file and one page in `factory-test` as the test user. Both wait on items 1 and 2.

Exit test (plan 11.1): a Playwright storage state for the `factory-test` test user, made headless in CI, by certificate sign-in under the tenant's Conditional Access, with the certificate from Key Vault. If it fails: record the exact error, change no policy, and draft a message for the identity team (plan 11.1's fallback).

## What runs where

Each scratch part was made at Boroon's word ("Yes, make both", 27 November 2026), the same pattern as spike 0.10.

| Thing | Where | State |
|---|---|---|
| `probe.yml` (copy here) | `GetAI-IP/signin-probe` (private, scratch, repo 5474206), `.github/workflows/probe.yml` | Pushed 27 November 2026 (`d3ff2ed`, last `eca4563`). **Exists** |
| `signin_probe.py`, `diagnose.cjs`, `check_vars.sh`, `specs/ui-signin-probe-01.spec.ts` (copies here) | Same repo, `probe/` | Probe-only, not gate scripts. **Exist** |
| The Playwright kit | Same repo, `gate/playwright/`: **the gate's own kit**, copied unchanged from `GetAI-IP/factory-gates` at `release` `2080a82` (gate PR 33), with the kit's 72 lines of the gate's `scripts.sha256` as `gate/scripts.sha256`; every `signin` and `diagnose` run checked every file against them. Not copied here: the gate holds it | **Exists** |
| Repository variables `TENANT_ID`, `TEST_APP_ID`, `TEST_URL`, `KEYVAULT`, `TEST_USER`, `TEST_USER_CERT` | Same repo. Not secret; kept there so the IDs stay out of this public repo | **Exist** |
| GitHub environment `lcp-test` | Same repo, made by the first run, no protection rules | **Exists** |
| Federated credential `signin-probe-lcp-test` | On `getai-nwt-test`, subject `repo:GetAI-IP@801576/signin-probe@5474206:environment:lcp-test` (the immutable subject; `azure/login` printed exactly this subject, and signed in, on every run) | Made 27 November 2026, 02:12 UTC, by `az`. **Exists** |

Nothing was made in `factory-test`. The only sign-in was the test user's own, which Entra stopped before any session existed.

## How the probe works

`workflow_dispatch` only, from `main` only, one job, as the Test identity only, in environment `lcp-test` (rule 5, plan 5.3). Actions are pinned to the gate's commit SHAs. One concurrency group, so one run at a time.

**Nothing is uploaded.** No `upload-artifact` step at all. The storage state is a live credential (reading notes, point 17), the certificate is a secret, and `playwright-ms-auth`'s sign-in screenshots show the signed-in page. They stay on the runner, and a last step (`if: always()`) deletes the `.auth/` folder, any `.playwright-ms-auth/` folder and the evidence folder, signs Azure out, and fails if anything is left. It passed on every run. Playwright runs with `--retries=0 --trace=off` and the list reporter only, so no trace or HTML report is written (a trace records the session's network, and so its cookies [inference]).

Modes:

1. **`vault`** (no browser): signs in to Azure as the Test identity by OIDC (`azure/login`, as the gate's `verify-in-test`), then `signin_probe.py vault`:
   - reads the secret `factory-test-nwt` by the Key Vault REST API and prints its metadata only: content type (it must be `application/x-pkcs12`, or `playwright-ms-auth` reads it as a password), enabled, not before, expires, whether a certificate manages it, and the value's length. Never the value;
   - tries to list the vault's secrets, and to read the certificate object `factory-test-nwt`, and prints the HTTP status and error codes. Both should be 403. A 200 is a warning: the role is wider than the one secret.
2. **`signin`**: everything in `vault`, and first, before the Azure sign-in:
   - checks the kit against the gate's hashes (`sha256sum --check --strict`);
   - Node `22.x` (not `lts/*`, which failed on a GHE.com runner, spike 0.6), then `npm ci --ignore-scripts --no-audit --no-fund --no-update-notifier` in the kit: its 58 pinned packages, each checked against its sha512. Microsoft's toolkit is vendored in the kit; nothing is installed by its npm name, which is a security placeholder;
   - `npx playwright install --with-deps chromium`, and checks for Microsoft Edge at `/opt/microsoft/msedge/msedge` (`playwright-ms-auth` launches Edge); if Edge is missing, it installs it with Playwright and warns.

   Then, after the vault read:
   - **the kit's `sign-in` project**, unchanged: `npx playwright test --config playwright.lcp.config.ts --project sign-in`, with `CI=true` and the variables `playwright-ms-auth` reads (reading notes, point 1; kit README, "Sign-in variables"): `MS_AUTH_EMAIL`, `MS_AUTH_CREDENTIAL_TYPE=certificate`, `MS_AUTH_CREDENTIAL_PROVIDER=azure-keyvault`, `MS_AUTH_KEYVAULT_ENDPOINT=https://kv-getai-factory-aue.vault.azure.net/`, `MS_AUTH_KEYVAULT_SECRET_NAME=factory-test-nwt`, and `MODEL_DRIVEN_APP_URL=<Test URL>main.aspx` (there is no app in `factory-test` to point at). `SYSTEM_DEBUG=true` turns on `playwright-ms-auth`'s log lines (input `debug`). Timed;
   - `signin_probe.py state` reads `.auth/mda.json` and prints its size, the number of cookies and origins, and the cookies per domain. It fails if no cookie is for `factory-test.crm6.dynamics.com`;
   - **one page as the test user**: `specs/ui-signin-probe-01.spec.ts` in the kit's `model-driven` project with `--no-deps`, so it uses the stored state and signs in again nowhere. It opens `main.aspx`, checks the page stays on `factory-test`, then calls `WhoAmI` and reads the user's `domainname` by the Web API on the stored cookies alone, with no redirects followed, and checks it is the test user.
3. **`diagnose`** (added after run 2): the same installs and vault read, then `diagnose.cjs`, which drives the same sign-in as `playwright-ms-auth` with its own Key Vault provider and certificate route, but waits for each page. It prints each Entra page's accessible names (headings, links, buttons, text), with no link URLs and no sign-in paths, and any `AADSTS` code on the page. It saves no storage state.
4. Input **`vault_delay`** (`0` or `7` minutes) waits between the Azure sign-in and the first Key Vault read, to see whether the GitHub OIDC token behind `azure/login` (about 5 minutes, spike 0.14) runs out for `az`.

## Runs

All on `ubuntu-latest`, which on `getai.ghe.com` is **Ubuntu 26.04** (image `20261116.202.1`), with **Microsoft Edge 157.0.4341.60** already installed. Playwright 1.64.1 fetched Chromium headless shell 156.0.8078.4.

| # | Run | Mode | Result |
|---|---|---|---|
| 1 | 41604351 | `vault` | **Pass**, 13 s. `azure/login` signed in by OIDC with the subject above, within a minute of the credential being made. The secret read and the two refusals, as above |
| 2 | 41604586 | `signin` | **Fail** at the kit's sign-in, after 1.7 minutes. Kit hashes matched; `npm ci` 58 packages; Edge already there. `playwright-ms-auth` read the secret as a certificate (3,556 bytes), opened `main.aspx`, reached `login.microsoftonline.com`, typed the email, pressed Next. It never logged "Selecting certificate authentication", sent no certificate request ("Certificate authentication response not detected" after 60 s), and ended with "Authentication may have failed. Expected to be on https://factory-test.crm6.dynamics.com or similar, but got https://login.microsoftonline.com/…/oauth2/authorize?…". The state check and the page did not run. No sign-in reached Entra's log |
| 3 | 41606651 | `diagnose` | **Stopped by SSPR registration.** The pages, in order: "Sign in" (email box, Next, "Sign-in options"); after Next, "Enter password" with the links "Forgot my password" and **"Use a certificate or smart card"**; after clicking it, certauth answered HTTP 200; then **"Let's keep your account secure. We'll help you set up another way to verify it's you."**, with "Use a different account" and Next only. Final: still on the sign-in host. The sign-in log entry (02:21:46 UTC) is in the result above: 50125, Conditional Access success, MFA satisfied by the certificate |
| 4 | 41608426 | `vault`, `vault_delay` 7 | **Pass.** The wait ran 02:25:13 to 02:32:13 UTC, then `az` got a Key Vault token and the read and refusals were as in run 1 |

The test user's Entra sign-in log, read as Boroon after run 3 (Graph `auditLogs/signIns`, beta): one entry, from run 3. Run 2 never sent the certificate, so it left none.

## Checked locally before the runs (27 November 2026, no sign-in, nothing sent)

| Check | Result |
|---|---|
| The kit at `release` `2080a82` against the gate's `scripts.sha256` | All 72 files in `playwright/` are listed there, and a copy taken by `git archive` matches every hash |
| `npm ci --ignore-scripts` in a scratch copy of the kit (Node 26.5) | 58 packages, as the kit's README says |
| `tsc --noEmit` with the kit's `tsconfig.json`, the probe spec added | Passes |
| `npx playwright test --list`, `--project sign-in`, with `CI=true` | The kit's 2 sign-in steps (model-driven and canvas; canvas skips with no `CANVAS_APP_URL`) |
| `npx playwright test --list`, `--project model-driven --no-deps`, `TEST_SPECS_DIR` the probe's `specs/` | 1 test in 1 file, from outside the kit; `--no-deps` exists in Playwright 1.64.1 |
| `check_vars.sh` | Passes with the real names; fails a `TEST_URL` without its trailing slash |
| `signin_probe.py state` on fake state files | Prints counts and domains, never a cookie value; fails a state with no `factory-test` cookie, and a missing file |
| `signin_probe.py vault` with the network replaced | Prints metadata only, never the value or the token; fails a wrong content type and an expired secret; reports two 403s as expected |
| `diagnose.cjs` | `node --check`; its imports resolve from the kit's folder |
| The workflow parses as YAML | 15 steps, conditions as meant. `actionlint` is not on the laptop, so not run |

## Findings

1. **The certificate, the trust store and the bindings are right.** Entra matched the user by `IssuerAndSerialNumber` to `certificateUserIds` (the value the admins set at 01:00 UTC; finding 14 in the `factory-test` README is settled), at High affinity, and rated it multifactor by the issuer rule. Nothing about the certificate needs a re-sign.
2. **AADSTS50125, SSPR registration.** Microsoft's error list calls it `PasswordResetRegistrationRequiredInterrupt`. It comes from SSPR's "Require users to register when signing in" setting, for users in SSPR's scope; Microsoft's SSPR deployment guide recommends that setting on, with SSPR for **All** users. Microsoft's SSPR FAQ: "If you define enough authentication information on their behalf, users don't have to register." Boroon's roles cannot read the SSPR settings, so whether SSPR is on for All or a selected group is not known here.
3. **It is not Conditional Access.** The log's `conditionalAccessStatus` is success, and no policy applied to this sign-in. So no Conditional Access exclusion is needed for the test user.
4. **`playwright-ms-auth` 0.0.19 checks for the certificate link without waiting.** In `lib/authenticate.js`, `handleCertificateAuth` calls `isVisible({ timeout: 5000 })` for "Work or school account" and for a link or button named "certificate". Playwright 1.64.1's own type notes say that timeout "is ignored" and `isVisible` "does not wait". Right after Next, the password page is not drawn yet, so both checks are false, the link is never clicked, and the 60 s wait for certauth runs out. It then treats any page as success once off the sign-in host, and reports a stuck page only by its URL. The same file waits correctly elsewhere (`toHaveURL`, `waitForResponse`). With waits, `diagnose.cjs` found and clicked the link at once. Whether 0.0.20 fixes this is not known (not read).
5. **When the certificate does get through, the package would not see SSPR's page as a failure either:** it is on the sign-in host, so the package throws its URL-only error. Only the sign-in log says why.
6. **The Azure sign-in outlives the OIDC token by at least 2 minutes.** `azure/login` v3.1.0 then `az` got a fresh Key Vault token 7 minutes after signing in. Untested beyond 7 minutes. The gate's `verify-in-test` signs in to Azure before the solution checker and the managed import (up to 30 minutes, `--max-async-wait-time 30`), and its Playwright step comes after both.
7. **The runner is Ubuntu 26.04 and has Edge.** So `playwright-ms-auth`'s Edge launch works on the gate's hosted runner with no install; the kit's `npx playwright install --with-deps chromium` is still needed for the tests' own browser.
8. **The GitHub environment's name alone decides the credential**, as in spike 0.10: `azure/login` printed the subject `repo:GetAI-IP@801576/signin-probe@5474206:environment:lcp-test` and the `job_workflow_ref` of the scratch workflow, and signed in on the first try.

## Message for the identity team (draft, for Boroon to send)

> Hi both,
>
> Thanks for setting `certificateUserIds` on the factory test user this morning. The certificate sign-in now works: Entra matched the user by IssuerAndSerialNumber, counted it as multifactor, and Conditional Access passed.
>
> One thing still stops it. Straight after the certificate, Entra asks the test user to register for self-service password reset ("Let's keep your account secure", AADSTS50125, sign-in log at 02:21 UTC today). The user is only for automated tests, signs in by certificate only and has no password anyone keeps, so it can never answer that. Could you take `factory-test-nwt@getai.com.au` out of that requirement, whichever way suits you?
>
> 1. If SSPR is on for a selected group, keep `factory-cba-test-users` out of that group.
> 2. If SSPR is on for All users, set its password reset information on its behalf, so it has nothing to register (Microsoft's SSPR FAQ: "If you define enough authentication information on their behalf, users don't have to register"). For example, an authentication email to <a team mailbox>.
>
> Please leave the tenant-wide "Require users to register when signing in" setting as it is. Let me know when it's done and I'll rerun the test.
>
> Thanks!

Boroon picks the team mailbox for option 2 before sending. Names are in ADO 2541.

## Proposals for Boroon (none made)

1. **The kit's sign-in, by its own gate PR.** `lib/sign-in.setup.ts` stops calling `playwright-ms-auth`'s `authenticate()` and drives the sign-in itself, with waits, as `diagnose.cjs` does: the package's own Key Vault provider (`CredentialProviderFactory`) and certificate route (`addCertAuthRoute`), the same pages and clicks, then `context.storageState()` to `.auth/mda.json`. It should also fail with the page's heading and any `AADSTS` code when it is stuck on the sign-in host, not only the URL. The other way, moving to `playwright-ms-auth` 0.0.20, needs a full read first (rule 19) and may not fix it.
2. **The gate's "Locked Playwright suite" step** (`factory-test` README, finding 4; kit README, "The change to the gate step"): the variables in the kit README's proposed step are the right ones, all six seen working here (`MS_AUTH_EMAIL`, `MS_AUTH_CREDENTIAL_TYPE`, `MS_AUTH_CREDENTIAL_PROVIDER`, `MS_AUTH_KEYVAULT_ENDPOINT` as a URL, `MS_AUTH_KEYVAULT_SECRET_NAME`, `MODEL_DRIVEN_APP_URL`), and `KEYVAULT_NAME` goes. Two additions from these runs: a second `azure/login` right before the step (cheap; the gap after the checker and import can pass 7 minutes, finding 6), and `--retries` and `--trace` settings that keep a trace of a signed-in session out of the evidence Blob. Boroon picks `gate.json` or caller variables for the test user, the certificate's name and the app's ID. Its fix is its own gate PR.
3. **Plan 5.3, the Test identity's role on the certificate:** Key Vault Secrets User on the certificate's secret, not Key Vault Certificate User on the certificate (proved, finding above; the certificate object itself is refused with that role, and is not needed).
4. **The test CA key** waits until the full sign-in passes (the brief's rule). The certificate itself is now proved, so no re-sign is expected; when the sign-in passes, Boroon deletes `~/factory-test-ca/factory-test-ca.key`, then its passphrase from his password manager, noted in the `factory-test` README and in ADO 2541.

## Scratch and clean-up

Still there, for Boroon to say whether to keep them until the rerun (after the identity team's change and the kit fix) or delete them now and make them again then: the repo `GetAI-IP/signin-probe` (with its environment, variables, runs and logs) and the federated credential `signin-probe-lcp-test` on `getai-nwt-test`. Either way they are deleted at the end, at his word, and read back gone. Kept for good: `getai-nwt-test`, its role on the secret, `ai-factory-nwt-lcp-test`, the vault, the certificate and the test user. The test CA key in `~/factory-test-ca` was not read, copied or moved by this spike.
