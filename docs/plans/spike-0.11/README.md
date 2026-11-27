# Spike 0.11: the test user signs in by certificate, headless in CI

Plan section 11.1, row 0.11 (ADO 2447). Session 61, Friday 27 November 2026, on the laptop (desktop app), laptop track B. Dated Thursday 26 November; the last Stage 0 spike the Stage 1 exit test (2539, Friday 27 November) needs.

**Status (27 November 2026, 01:10 UTC): not run. The probe and its workflow are written and checked locally. Nothing exists yet in the tenant or on `getai.ghe.com` for it.** The sign-in cannot pass yet: the test user's `certificateUserIds` is still empty (read back as Boroon at 00:54 UTC, `[]`; `docs/plans/factory-test/README.md`, finding 14). The identity admins set it to the value in that README (section 2, step 3). The `vault` mode below does not need that value, so it can run as soon as the scratch exists.

Exit test (plan 11.1): a Playwright storage state for the `factory-test` test user, made headless in CI, by certificate sign-in under the tenant's Conditional Access, with the certificate from Key Vault. If it fails: record the exact error, change no policy, and draft a message for the identity team (plan 11.1's fallback).

What the probe proves, as the Test identity `getai-nwt-test` on a `getai.ghe.com` runner, with no secret in any repo:

1. **The role is enough.** It reads the secret `factory-test-nwt` from `kv-getai-factory-aue` holding only Key Vault Secrets User on that secret. It also tries to list the vault's secrets and to read the certificate object; both should be refused (HTTP 403).
2. **The sign-in works headless.** `playwright-ms-auth`, through the kit's own `sign-in` project, signs in as `factory-test-nwt@getai.com.au` by certificate with `CI` set: no browser prompt, no password.
3. **The state works.** The storage state file is written, and one page in `factory-test` loads as the test user from it, with no new sign-in.

## What runs where

Nothing below is made yet. Each scratch part is made only at Boroon's word, asked before it is made, and deleted at the end (the same pattern as spike 0.10).

| Thing | Where | State |
|---|---|---|
| `probe.yml` (copy here) | `GetAI-IP/signin-probe` (private, scratch), `.github/workflows/probe.yml` | Written, not pushed |
| `signin_probe.py`, `check_vars.sh`, `specs/ui-signin-probe-01.spec.ts` (copies here) | Same repo, `probe/` | Written, not pushed. Probe-only, not gate scripts |
| The Playwright kit | Same repo, `gate/playwright/`: **the gate's own kit**, copied unchanged from `GetAI-IP/factory-gates` at `release` `2080a82` (gate PR 33), with the kit's 72 lines of the gate's `scripts.sha256` as `gate/scripts.sha256`; the job checks every file against them. Not copied here: the gate holds it | Not pushed |
| Repository variables `TENANT_ID`, `TEST_APP_ID`, `TEST_URL`, `KEYVAULT`, `TEST_USER`, `TEST_USER_CERT` | Same repo. Not secret; kept there so the IDs stay out of this public repo | Not made |
| GitHub environment `lcp-test` | Same repo, made by the first run, no protection rules | Not made |
| Federated credential `signin-probe-lcp-test` | On `getai-nwt-test`, subject `repo:GetAI-IP@801576/signin-probe@<repo id>:environment:lcp-test` (the immutable subject, as spike 0.10's) | Not made |

Nothing is made in `factory-test`. The sign-in touches only the test user's own session; the page is `main.aspx` and two Web API reads. No Northwind, no rows.

## How the probe works

`workflow_dispatch` only, from `main` only, one job, as the Test identity only, in environment `lcp-test` (rule 5, plan 5.3). Actions are pinned to the gate's commit SHAs. One concurrency group, so one run at a time.

**Nothing is uploaded.** No `upload-artifact` step at all. The storage state is a live credential (reading notes, point 17), the certificate is a secret, and `playwright-ms-auth`'s sign-in screenshots show the signed-in page. They stay on the runner, and a last step (`if: always()`) deletes the `.auth/` folder, any `.playwright-ms-auth/` folder and the evidence folder, signs Azure out, and fails if anything is left. Playwright runs with `--retries=0 --trace=off` and the list reporter only, so no trace or HTML report is written (a trace records the session's network, and so its cookies [inference]).

Modes:

1. **`vault`** (no browser): signs in to Azure as the Test identity by OIDC (`azure/login`, as the gate's `verify-in-test`), then `signin_probe.py vault`:
   - reads the secret `factory-test-nwt` by the Key Vault REST API and prints its metadata only: content type (it must be `application/x-pkcs12`, or `playwright-ms-auth` reads it as a password), enabled, not before, expires, whether a certificate manages it, and the value's length. Never the value;
   - tries to list the vault's secrets, and to read the certificate object `factory-test-nwt`, and prints the HTTP status and error codes. Both should be 403. A 200 is a warning: the role is wider than the one secret.
2. **`signin`**: everything in `vault`, and first, before the Azure sign-in:
   - checks the kit against the gate's hashes (`sha256sum --check --strict`);
   - Node `22.x` (not `lts/*`, which failed on a GHE.com runner, spike 0.6), then `npm ci --ignore-scripts --no-audit --no-fund --no-update-notifier` in the kit: its 58 pinned packages, each checked against its sha512. Microsoft's toolkit is vendored in the kit; nothing is installed by its npm name, which is a security placeholder;
   - `npx playwright install --with-deps chromium`, and checks for Microsoft Edge at `/opt/microsoft/msedge/msedge` (`playwright-ms-auth` launches Edge); if Edge is missing, it installs it with Playwright and warns.

   Then, after the vault read:
   - **the kit's `sign-in` project**, unchanged: `npx playwright test --config playwright.lcp.config.ts --project sign-in`, with `CI=true` and the variables `playwright-ms-auth` reads (reading notes, point 1; kit README, "Sign-in variables"): `MS_AUTH_EMAIL`, `MS_AUTH_CREDENTIAL_TYPE=certificate`, `MS_AUTH_CREDENTIAL_PROVIDER=azure-keyvault`, `MS_AUTH_KEYVAULT_ENDPOINT=https://kv-getai-factory-aue.vault.azure.net/`, `MS_AUTH_KEYVAULT_SECRET_NAME=factory-test-nwt`, and `MODEL_DRIVEN_APP_URL=<Test URL>main.aspx` (there is no app in `factory-test` to point at). `SYSTEM_DEBUG=true` turns on `playwright-ms-auth`'s log lines (input `debug`): the email, the certificate's SHA-256 fingerprint, the secret's metadata, each step, and on a certificate failure the error details Entra shows. Never a secret. Timed;
   - `signin_probe.py state` reads `.auth/mda.json` and prints its size, the number of cookies and origins, and the cookies per domain. It fails if no cookie is for `factory-test.crm6.dynamics.com`;
   - **one page as the test user**: `specs/ui-signin-probe-01.spec.ts` in the kit's `model-driven` project with `--no-deps`, so it uses the stored state and signs in again nowhere. It opens `main.aspx` and checks the page stays on `factory-test` (it lists every host it passes through, without query strings or sign-in paths), then calls `WhoAmI` and reads the user's `domainname` by the Web API on the stored cookies alone, with no redirects followed, and checks it is the test user. It imports `lcp-kit` from outside the kit, as the gate's `TEST_SPECS_DIR` will.
3. Input **`vault_delay`** (`0` or `7` minutes) waits between the Azure sign-in and the first Key Vault read. The GitHub OIDC token behind `azure/login` lasts about 5 minutes (spike 0.14). A run with `7` shows whether `az` can still get a Key Vault token after it runs out. The gate's `verify-in-test` signs in to Azure before the checker and the import, many minutes before its Playwright step, so this decides where that step's Azure sign-in goes.

All slow steps (installs, browsers) come before the Azure sign-in, for the same reason.

## Runs

None yet. The order, once the scratch exists:

1. `vault` (does not need `certificateUserIds`): proves point 1 and the federated credential. A wrong subject fails `azure/login` with AADSTS700213, which names the right one; then fix the credential and wait about five minutes (spike 0.2).
2. `signin`, once the admins say `certificateUserIds` is set and it reads back as Boroon: proves points 2 and 3.
3. `vault` with `vault_delay: 7`: the 5-minute question above.
4. Then, as Boroon, read the test user's Entra sign-in log (`GET /auditLogs/signIns?$filter=userPrincipalName eq '<test user>'`; readable by Boroon, checked at 01:05 UTC: no sign-ins yet). It gives the authoritative result: the error code if any, the Conditional Access result and policies, the authentication method and whether the multifactor rule satisfied MFA. For a failure, this is where the exact error comes from: `playwright-ms-auth` reports a Conditional Access block only as "Authentication may have failed ... but got https://login.microsoftonline.com/..." (below).

## Checked locally (27 November 2026, no sign-in, nothing sent)

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
| The workflow parses as YAML | 14 steps, conditions as meant. `actionlint` is not on the laptop, so not run |

## What the code says, before any run

From reading `playwright-ms-auth` 0.0.19 in the kit's lockfile (`lib/authenticate.js`, `certAuth.js`, `providers/AzureKeyVaultProvider.js`, `config.js`, `utils.js`), as installed above. These are expectations, not results [untested]:

1. **The flow it drives:** open the target URL; expect a redirect to `https://login.microsoftonline.com/` within 30 s; type the email into the textbox named like "email" and press "Next"; route every request to `https://*certauth.login.microsoftonline.com/**` through Node with the PFX as the client certificate; click a link or button whose name contains "certificate" if one shows within 5 s; wait up to 60 s for the certauth response; then press "Yes" on "Stay signed in?" if shown. It counts the sign-in a success as soon as the page is **off the sign-in host**, wherever it is.
2. **What it reports on a failure:** for a certificate failure page ("Certificate validation failed" or "We couldn't sign you in with a certificate") it opens "More details" and logs the error details (`SYSTEM_DEBUG`). For anything else that leaves the page on the sign-in host, a Conditional Access block included, it throws only "Authentication may have failed. Expected to be on <origin> or similar, but got <URL>". So the exact error for a block comes from the Entra sign-in log (run 4).
3. **If Entra hides the certificate option** behind "Other ways to sign in", step 1 finds no "certificate" control, waits out the 60 s, and fails at the end with the message in point 2. The `SYSTEM_DEBUG` line "Selecting certificate authentication" shows whether it found one.
4. **Key Vault:** it reads the secret through `AzureCliCredential` first (then Azure PowerShell and Azure Developer CLI; never a browser with `CI` set), so the job's `az` sign-in serves. The `vault` step fetches a Key Vault token first, which `az` then keeps for about an hour.
5. **The state:** written under `MS_AUTH_OUTPUT_DIR`, which the kit sets to `.auth/ms-auth`, then copied to `.auth/mda.json` and the original deleted. The sign-in screenshots go to `.auth/ms-auth/screenshots/`, inside the folder the last step deletes.

## Proposals for Boroon (after the runs; none made)

Drafted once the runs say what is true:

1. The variables the gate's "Locked Playwright suite" step should pass (`factory-test` README, finding 4; the kit README's proposed step), and where its Azure sign-in goes (run 3). Its fix is its own gate PR; Boroon picks `gate.json` or caller variables for the test user, the certificate's name and the app's ID.
2. Plan 5.3's edit for the role: Key Vault Secrets User on the secret, not Key Vault Certificate User on the certificate (run 1).
3. Once the sign-in passes: the test CA key can be destroyed. Boroon deletes `~/factory-test-ca/factory-test-ca.key`, then its passphrase from his password manager; noted in the `factory-test` README and ADO 2541.

## Scratch and clean-up

To be deleted at the end, at Boroon's word, and read back gone: the repo `GetAI-IP/signin-probe` (with its environment, variables, runs and logs) and the federated credential `signin-probe-lcp-test` on `getai-nwt-test`. Kept: `getai-nwt-test`, its role on the secret, `ai-factory-nwt-lcp-test`, the vault, the certificate and the test user. The test CA key in `~/factory-test-ca` is not read, copied or moved by this spike.
