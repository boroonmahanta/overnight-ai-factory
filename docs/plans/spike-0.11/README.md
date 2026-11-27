# Spike 0.11: the test user signs in by certificate, headless in CI

Plan section 11.1, row 0.11 (ADO 2447, **Done** on 27 November 2026 at Boroon's word). Session 61, Friday 27 November 2026, on the laptop (desktop app), laptop track B. Dated Thursday 26 November; the last Stage 0 spike the Stage 1 exit test (2539, Friday 27 November) needs. The scratch is deleted and read back gone.

**Result (27 November 2026, runs 41604351 to 41622946, 02:12 to 03:13 UTC): the exit test passes**, with the kit's sign-in step fixed by gate PR 34 (https://getai.ghe.com/GetAI-IP/factory-gates/pull/34, merged by Boroon on 27 November 2026, `release` at `5826414`). In run 41622946, as the Test identity on a `getai.ghe.com` runner, with no secret in any repo:

1. **The role is enough, and no wider.** Holding only Key Vault Secrets User on the secret `factory-test-nwt`, the job read it: `application/x-pkcs12`, enabled, valid 26 November 2026 to 26 November 2027, managed by the certificate, 3,556 bytes. Listing the vault's secrets and reading the certificate object were both refused (HTTP 403, `ForbiddenByRbac`), in every run.
2. **The test user signed in by certificate, headless, with `CI` set: no browser prompt, no password**, in 36 s, under the tenant's Conditional Access. Entra matched the user by `IssuerAndSerialNumber` to `certificateUserIds` (High affinity) and rated the sign-in multifactor by the issuer rule; Conditional Access status success.
3. **The storage state was written** (17,272 bytes, 23 cookies, two for `factory-test.crm6.dynamics.com`), **and one page loaded as the test user from it** with no new sign-in: `main.aspx` on `factory-test` ("Microsoft Dynamics 365"), and the Web API's `WhoAmI` gave `factory-test-nwt@getai.com.au`, enabled. Then the state was deleted.

Two things had to change first, found by the earlier runs:

- **The kit's sign-in step (gate PR 34).** `playwright-ms-auth` 0.0.19's `authenticate()` never clicked "Use a certificate or smart card": it looks for it with Playwright's `isVisible`, which does not wait (Playwright's own docs: the timeout option "is ignored"), so it checks before the page is drawn (run 41604586). The fixed step uses the package's own Key Vault provider and certificate route, but drives Entra's pages itself with waits, and handles Entra going to `certauth` by itself, which it did once the user had signed in by certificate (run 41621996, then 41622946).
- **SSPR registration, the identity team's.** After the certificate, Entra first stopped the sign-in to make the test user register for self-service password reset: **AADSTS50125**, "Sign-in was interrupted due to a password reset or password registration entry" (run 41606651, sign-in log 02:21:46 UTC); not Conditional Access. No policy was changed here. At 02:51 UTC an identity admin registered an email authentication method for the user (a GET AI team mailbox), on its behalf, with no tenant-wide change (the directory audit log: "Admin registered security info"). The next sign-ins had no interrupt.

Exit test (plan 11.1): a Playwright storage state for the `factory-test` test user, made headless in CI, by certificate sign-in under the tenant's Conditional Access, with the certificate from Key Vault. If it fails: record the exact error, change no policy, and draft a message for the identity team (plan 11.1's fallback).

## What runs where

Each scratch part was made at Boroon's word ("Yes, make both", 27 November 2026), the same pattern as spike 0.10.

| Thing | Where | State |
|---|---|---|
| `probe.yml` (copy here) | `GetAI-IP/signin-probe` (private, scratch, repo 5474206), `.github/workflows/probe.yml` | Pushed 27 November 2026 (`d3ff2ed`; the workflow last changed in `eca4563`, the repo last pushed `f67fd32`). **Deleted** |
| `signin_probe.py`, `diagnose.cjs`, `check_vars.sh`, `specs/ui-signin-probe-01.spec.ts` (copies here) | Same repo, `probe/` | Probe-only, not gate scripts. **Deleted** with the repo |
| The Playwright kit | Same repo, `gate/playwright/`: **the gate's own kit**, copied unchanged from `GetAI-IP/factory-gates` at `release` `2080a82` (gate PR 33), with the kit's 72 lines of the gate's `scripts.sha256` as `gate/scripts.sha256`, for runs 1 to 4; from run 5, the kit from the gate branch `gate-2447-kit-signin` (gate PR 34) with its 73 lines. Every `signin` and `diagnose` run checked every file against them. Not copied here: the gate holds it | **Deleted** with the repo |
| Repository variables `TENANT_ID`, `TEST_APP_ID`, `TEST_URL`, `KEYVAULT`, `TEST_USER`, `TEST_USER_CERT` | Same repo. Not secret; kept there so the IDs stay out of this public repo | **Deleted** with the repo |
| GitHub environment `lcp-test` | Same repo, made by the first run, no protection rules | **Deleted** with the repo |
| Federated credential `signin-probe-lcp-test` | On `getai-nwt-test`, subject `repo:GetAI-IP@801576/signin-probe@5474206:environment:lcp-test` (the immutable subject; `azure/login` printed exactly this subject, and signed in, on every run) | Made 27 November 2026, 02:12 UTC, by `az`. **Deleted** |

Nothing was made in `factory-test`. The only sign-ins were the test user's own; the one session that existed (run 6) was saved on the runner only and deleted at the end of its job.

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
| 5 | 41621996 | `signin`, gate PR 34's first version | **Fail, and a new path seen.** After Next, Entra went to `certauth` by itself (HTTP 200), with no link shown, then to "Stay signed in?". No SSPR page: the admin had registered the email method at 02:51 UTC. The step was still waiting for the link, and failed after 30 s with "Sign-in stopped: no certificate sign-in option after the email ...; heading \"Stay signed in?\"". The state was deleted |
| 6 | 41622946 | `signin`, gate PR 34 as opened | **Pass.** `[sign-in] Entra went to the certificate by itself`, `certauth answered HTTP 200`, `answering "Stay signed in?" with Yes`, `signed in, on syd--ocecrmlivesg603.crm6.dynamics.com/` (Dynamics' own regional host, after the redirect), `state saved to .auth/mda.json`: 36 s. The state check: 17,272 bytes, 23 cookies (13 for `login.microsoftonline.com`, 1 for `certauth.login.microsoftonline.com`, 2 for `login.live.com`, 3 for `crm6.dynamics.com`, 2 for `factory-test.crm6.dynamics.com`, 2 for `syd--ocecrmlivesg603.crm6.dynamics.com`). The page: landed only on `factory-test.crm6.dynamics.com/main.aspx`, title "Microsoft Dynamics 365", signed in as `factory-test-nwt@getai.com.au` (access mode 0, enabled), 866 ms. Then everything was deleted and Azure signed out |

The test user's Entra sign-in log, read as Boroon (Graph `auditLogs/signIns`, beta): run 3 at 02:21:46 UTC, error 50125; run 6 at 03:12:08 UTC, 50140 ("Keep me signed in" interrupt, the normal entry for that page), Conditional Access success, multifactor. Run 2 never sent the certificate, so it left none; run 5's entry had not appeared when read.

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
2. **AADSTS50125, SSPR registration.** Microsoft's error list calls it `PasswordResetRegistrationRequiredInterrupt`. It comes from SSPR's "Require users to register when signing in" setting, for users in SSPR's scope; Microsoft's SSPR deployment guide recommends that setting on, with SSPR for **All** users. Microsoft's SSPR FAQ: "If you define enough authentication information on their behalf, users don't have to register." Boroon's roles cannot read the SSPR settings, so whether SSPR is on for All or a selected group is not known here. **Settled at 02:51 UTC** by an identity admin registering an email authentication method for the user on its behalf (the directory audit log: "Admin registered security info", "Admin registered Email Authentication Method for user"), a GET AI team mailbox; no tenant-wide change. Runs 5 and 6 had no interrupt.
3. **It is not Conditional Access.** The log's `conditionalAccessStatus` is success, and no policy applied to this sign-in. So no Conditional Access exclusion is needed for the test user.
4. **`playwright-ms-auth` 0.0.19 checks for the certificate link without waiting.** In `lib/authenticate.js`, `handleCertificateAuth` calls `isVisible({ timeout: 5000 })` for "Work or school account" and for a link or button named "certificate". Playwright 1.64.1's own type notes say that timeout "is ignored" and `isVisible` "does not wait". Right after Next, the password page is not drawn yet, so both checks are false, the link is never clicked, and the 60 s wait for certauth runs out. It then treats any page as success once off the sign-in host, and reports a stuck page only by its URL. The same file waits correctly elsewhere (`toHaveURL`, `waitForResponse`). With waits, `diagnose.cjs` found and clicked the link at once. Whether 0.0.20 fixes this is not known (not read).
5. **When the certificate does get through, the package would not see SSPR's page as a failure either:** it is on the sign-in host, so the package throws its URL-only error. Only the sign-in log says why.
6. **The Azure sign-in outlives the OIDC token by at least 2 minutes.** `azure/login` v3.1.0 then `az` got a fresh Key Vault token 7 minutes after signing in. Untested beyond 7 minutes. The gate's `verify-in-test` signs in to Azure before the solution checker and the managed import (up to 30 minutes, `--max-async-wait-time 30`), and its Playwright step comes after both.
7. **The runner is Ubuntu 26.04 and has Edge.** So `playwright-ms-auth`'s Edge launch works on the gate's hosted runner with no install; the kit's `npx playwright install --with-deps chromium` is still needed for the tests' own browser.
8. **The GitHub environment's name alone decides the credential**, as in spike 0.10: `azure/login` printed the subject `repo:GetAI-IP@801576/signin-probe@5474206:environment:lcp-test` and the `job_workflow_ref` of the scratch workflow, and signed in on the first try.
9. **Once the user has signed in by certificate, Entra goes to `certauth` by itself after Next**, with no link shown (runs 5 and 6, after run 3's certificate sign-in). So a sign-in step must handle both: the link (a user's first certificate sign-in, or after Entra forgets) and no link. This is likely why `playwright-ms-auth`'s non-waiting check works where its test users have signed in by certificate before [inference]. Gate PR 34 waits for either.
10. **The landing host is Dynamics' regional one.** After "Stay signed in?", the browser landed on `syd--ocecrmlivesg603.crm6.dynamics.com/` before `factory-test`'s own pages; the state holds cookies for both, and `main.aspx` then loaded on `factory-test.crm6.dynamics.com` directly. A check that the sign-in "landed on the app's host" would have failed here; gate PR 34 checks only that the browser left the sign-in host, as the package did.
11. **"Stay signed in?" is logged as 50140** in the sign-in log, with Conditional Access success. It is the normal interrupt for that page, not a failure; the step answers Yes, as the package did.

## Message for the identity team (drafted; the team acted at 02:51 UTC, option 2)

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

## Proposals for Boroon (the first two made, as gate PRs 34 and 36)

1. **Done as gate PR 34** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/34, opened 27 November 2026 at Boroon's word, "Yes, write it"; merged by him the same day, `release` at `5826414`), which passed run 6. The proposal as written: **The kit's sign-in, by its own gate PR.** `lib/sign-in.setup.ts` stops calling `playwright-ms-auth`'s `authenticate()` and drives the sign-in itself, with waits, as `diagnose.cjs` does: the package's own Key Vault provider (`CredentialProviderFactory`) and certificate route (`addCertAuthRoute`), the same pages and clicks, then `context.storageState()` to `.auth/mda.json`. It should also fail with the page's heading and any `AADSTS` code when it is stuck on the sign-in host, not only the URL. The other way, moving to `playwright-ms-auth` 0.0.20, needs a full read first (rule 19) and may not fix it.
2. **Done as gate PR 36** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/36, Session 62, 27 November 2026; open, for Boroon to merge). Boroon chose `gate.json` for the settings and a lookup of the app's ID in Test after the import. The plan's Appendix A edit for it is below, proposed, not made. The proposal as written: **The gate's "Locked Playwright suite" step** (`factory-test` README, finding 4; kit README, "The change to the gate step"): the variables in the kit README's proposed step are the right ones, all six seen working here (`MS_AUTH_EMAIL`, `MS_AUTH_CREDENTIAL_TYPE`, `MS_AUTH_CREDENTIAL_PROVIDER`, `MS_AUTH_KEYVAULT_ENDPOINT` as a URL, `MS_AUTH_KEYVAULT_SECRET_NAME`, `MODEL_DRIVEN_APP_URL`), and `KEYVAULT_NAME` goes. Two additions from these runs: a second `azure/login` right before the step (cheap; the gap after the checker and import can pass 7 minutes, finding 6), and `--retries` and `--trace` settings that keep a trace of a signed-in session out of the evidence Blob. Boroon picks `gate.json` or caller variables for the test user, the certificate's name and the app's ID. Its fix is its own gate PR.
3. **Plan 5.3, the Test identity's role on the certificate:** Key Vault Secrets User on the certificate's secret, not Key Vault Certificate User on the certificate (proved, finding above; the certificate object itself is refused with that role, and is not needed).
4. **The test CA key can now be destroyed** (the full sign-in passed in run 6, the brief's rule). Boroon deletes `~/factory-test-ca/factory-test-ca.key`, then its passphrase from his password manager. Noted in the `factory-test` README and in ADO 2541. After that, a renewal or a second test user needs a new CA, which the admins upload again.

## Plan edit for gate PR 36 (proposed, not made; Session 62)

For Boroon's word, once gate PR 36 is merged. Plan Appendix A's `verify-in-test` (lines 2014 to 2242 as at 27 November 2026) keeps tags, not commit pins, as it does elsewhere. Gate PR 36 has the exact steps; in the plan they would read:

1. **Move the `settings` step** from after the Playwright step to straight after `actions/setup-python@v5`, renamed "Project gate settings (held-out set, Copilot Studio agents, UI suite)", with this comment: the settings say which optional suites the project has and what its UI suite signs in with; they come from its `gate.json`, hashed in the gate repo, so the PR under test cannot change them; read first, so a bad file fails before the checker and the import.
2. **After "Locked scenarios"**, three steps:

   ```yaml
      - id: app
        name: The model-driven app's URL in Test
        if: steps.settings.outputs.ui == 'true'
        env:
          MDA_APP: ${{ steps.settings.outputs.mda_app }}
        run: python3 -I gate/lcp/app_in_test.py --app "$MDA_APP" --env "$TEST_ENV_URL" --out evidence/app-in-test.json
      - uses: azure/login@v2              # again: the first sign-in came before the checker and import (spike 0.11)
        with:
          client-id: ${{ vars.LCP_TEST_APP_ID }}
          tenant-id: ${{ vars.TENANT_ID }}
          allow-no-subscriptions: true
      - name: Locked Playwright suite (certificate test user)
        if: steps.settings.outputs.ui == 'true'
        working-directory: gate/playwright
        env:
          MS_AUTH_EMAIL: ${{ steps.settings.outputs.test_user }}
          MS_AUTH_CREDENTIAL_TYPE: certificate
          MS_AUTH_CREDENTIAL_PROVIDER: azure-keyvault
          MS_AUTH_KEYVAULT_ENDPOINT: https://${{ steps.settings.outputs.keyvault }}.vault.azure.net/
          MS_AUTH_KEYVAULT_SECRET_NAME: ${{ steps.settings.outputs.test_user_cert }}
          MODEL_DRIVEN_APP_URL: ${{ steps.app.outputs.url }}
          TEST_SPECS_DIR: ${{ github.workspace }}/pr/tests/acceptance/ui
          LCP_EVIDENCE_DIR: ${{ github.workspace }}/evidence/playwright
        run: |
          set -euo pipefail
          # fails here when tests/acceptance/ui holds no spec (gate PR 36 has the line)
          npm ci --ignore-scripts --no-audit --no-fund --no-update-notifier
          npx playwright install --with-deps chromium
          npx playwright test --config playwright.lcp.config.ts --reporter=html,junit --trace=off
   ```

   with the comments gate PR 36 carries: why the app's ID comes from Test (the export holds only the unique name, and the toolkit reads `appid`), why the second sign-in, and why `--trace=off` (a trace of a signed-in session would hold its cookies, and `evidence/` goes to Blob; the retry stays).
3. **After the verifier sessions**, "Delete the test user's storage state", `if: always()`: deletes `gate/playwright/.auth` and `.playwright-ms-auth`, deletes any `trace.zip` under `evidence/`, and fails if either was there, before the evidence is hashed and copied.
4. **The job's header comment** gains "the install-or-upgrade import and the Playwright step (ADO 2539)"; the first `azure/login`'s comment loses nothing.
5. **Section 5.7's trusted-script list** (line 692) gains the app lookup (`app_in_test.py`, run by `verify-in-test` as the Test identity after the import), and the project settings reader's entry says it also holds the UI suite's test user, vault, certificate and app.
6. **A 14.4 row**, "The Playwright step's settings (2539)": the UI settings are in the project's `gate.json`, not caller variables; the app's ID is looked up in Test after the import; a second Azure sign-in before the suite; `--trace=off`; the storage state deleted after the verifiers (Boroon, 27 November 2026).

Independent of Session 61's proposed edit for the install-or-upgrade import (the `in-test` step before the import, also waiting on his word): the `app` step sits after the import in either form.

## Scratch and clean-up

**Deleted on 27 November 2026, at Boroon's word ("Yes, close it out"), and read back gone:**

| Thing | Where | How | Read back |
|---|---|---|---|
| Federated credential `signin-probe-lcp-test` | `getai-nwt-test` in Entra | `az ad app federated-credential delete`, 03:39:25 UTC (first, so nothing could sign in from the repo) | `az ad app federated-credential list`: only `ai-factory-nwt-lcp-test` is left (Session 48's, kept). No secret or certificate |
| Repo `GetAI-IP/signin-probe`, with its environment, variables, runs and logs | `getai.ghe.com` | `gh repo delete`, 03:39:27 UTC, after checking it was the scratch (its description) and no run was in progress | `gh api repos/GetAI-IP/signin-probe`: HTTP 404 |
| Local copies (the repo's working copy, the kit copies, the fake state files) | The session's scratchpad on the laptop | Deleted | |

Kept for good: `getai-nwt-test`, its Key Vault Secrets User role on the secret, `ai-factory-nwt-lcp-test`, the vault, the certificate and the test user, and its email authentication method. The test CA key in `~/factory-test-ca` was not read, copied or moved by this spike; Boroon destroys it (proposal 4). Every probe file has its copy here; the kit's fix is in gate PR 34.
