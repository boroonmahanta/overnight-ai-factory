# Reading notes: Microsoft's Playwright toolkit and `playwright-ms-auth`

Session 52, 25 November 2026, ADO 2546 (DG7 part 2). The full read that rule 19 and plan 8.3 ask for before the kit vendors third-party code. The kit is `staging/factory-gates/playwright/`; its README says how it uses what is below.

## What was read, and how

| Source | Pin | Files | Read in full | By |
|---|---|---|---|---|
| `microsoft/power-platform-playwright-samples`, `packages/power-platform-playwright-toolkit/` (MIT) | commit `3233f3e73e30960e8ab7349f1cb06b520ca010e4`, 28 October 2026 (still the head on 25 November) | 50, 407,052 bytes | Yes, every line | Four reader agents of this session, a quarter each, each confirming every file read. Their full reports are in the session's shared notes folder on the laptop (`session-52-toolkit-read-part-1` to `-4`) |
| The same repo: `LICENSE`, `NOTICE.md`, root `package.json` and `package-lock.json` | same | 4 | Yes (the lockfile by script: the 58 entries the kit needs, their versions, licences and install scripts) | This session |
| The same repo: 17 files of `packages/e2e-tests` (config, fixtures, the auth script, the Northwind page object, the model-driven tests and READMEs) | same | 17 | The config, `mda.fixtures.ts`, `authenticate.ts`, `NorthwindModelDrivenAppPage.ts`, `common.ts`, the globals and `.env.example` in full; the three model-driven tests and READMEs not line by line | This session. Adapted, not vendored |
| npm `playwright-ms-auth` 0.0.19 (MIT, Copyright (c) Microsoft Corporation in its `LICENSE`; published by one person's account) | sha512 in the kit's lockfile | 60 | Every `.js` and `.d.ts` file, `package.json`, `bin/` and `LICENSE`. The `.map` files hold mappings only (no `sourcesContent`). Its README was searched, not read in full | This session |

Every file was downloaded at Boroon's word (25 November 2026) into the session scratchpad first, and each GitHub file matched its blob hash at the pin. No text in any file is addressed to an AI agent.

## What the toolkit is

Page objects over Playwright for Power Apps: `AppProvider` (launch an app by name, ID or direct URL), `ModelDrivenAppPage` with `GridComponent`, `FormComponent` and `CommandingComponent`, `CanvasAppPage` (Studio authoring), `CanvasAppRuntimePage` (play mode), `PowerAppsPage` (maker portal), `GenUxPage` (the AI page designer), locators, page waiters, and auth helpers that wrap `playwright-ms-auth`. Microsoft ships it as source to reference locally, not as a supported package.

## Findings that matter to the kit

**Sign-in (`playwright-ms-auth`)**
1. The variables are read by `playwright-ms-auth`'s `loadConfigFromEnv`, not the toolkit: `MS_AUTH_EMAIL`, `MS_AUTH_CREDENTIAL_TYPE` (`password` or `certificate`), `MS_AUTH_CREDENTIAL_PROVIDER` (`azure-keyvault`, `local-file`, `environment`, `github-secrets`), and for Key Vault `MS_AUTH_KEYVAULT_ENDPOINT` (a URL) and `MS_AUTH_KEYVAULT_SECRET_NAME`. Session 46's finding 5 (`AZURE_KEYVAULT_URL`, `AZURE_CERTIFICATE_NAME`, `AZURE_TENANT_ID`) does not match the code: `AZURE_TENANT_ID` is read only by `ConfigHelper.getTenantId`, which the kit does not call.
2. The Key Vault provider signs in to Azure through a chain: Azure CLI, Azure PowerShell, Azure Developer CLI, and an interactive browser only when neither `CI` nor `TF_BUILD` is set. In the gate, the job's `azure/login` as the Test identity serves.
3. It reads the certificate as a Key Vault **secret** and treats it as a certificate only when the secret's content type is `application/x-pkcs12`; anything else is taken as a password. It checks the secret is enabled and in date.
4. Certificate sign-in routes `https://*certauth.login.microsoftonline.com/**` (or `MS_AUTH_LOGIN_ENDPOINT`) through Node with the PFX as the client certificate. Nothing else gets the certificate.
5. **It launches Microsoft Edge** (`channel: "msedge"`), headless by default, with `--no-sandbox`. GitHub's hosted Ubuntu 24.04 image has Edge 157 (image 20261116); a self-hosted runner needs it added.
6. It writes the storage state to `<project root>/.playwright-ms-auth/state-<email>.json`, or under `MS_AUTH_OUTPUT_DIR`, with full-page screenshots of the sign-in beside it. It skips signing in when that file is under 24 hours old. The toolkit's comments say `~/.playwright-ms-auth`; the code says the project root.
7. Logging is off unless `SYSTEM_DEBUG=true`; then it prints the email, the certificate's SHA-256 fingerprint and the names of browser storage keys, never a secret. One line always prints (the headless setting).
8. **It comes from one person's npm account and repo** (`deepakkamboj/playwright-ms-auth`, 5 stars), at 0.0.x, though its `LICENSE` names Microsoft. 0.0.20 exists (17 October 2026); Microsoft's lockfile and the kit stay on 0.0.19. It runs in the gate job that holds the Test identity's Azure session and the test user's certificate. Recorded as a risk; the kit pins it by sha512 and installs with `--ignore-scripts` (it has no install script).

**The toolkit**
9. Importing it runs `dotenv.config()`, which loads a `.env` from the working folder (`gate/playwright`, trusted). The kit's `.gitignore` keeps `.env` out.
10. `ModelDrivenAppPage`'s constructor reads a PFX from `MS_AUTH_LOCAL_FILE_PATH` when `MS_AUTH_CREDENTIAL_TYPE` is `certificate`, and on any error only logs and carries on (fail-open). The gate sets no `MS_AUTH_LOCAL_FILE_PATH`, so this does nothing there.
11. Launching a model-driven app by direct URL waits a fixed 30 seconds every time, then checks only that the host is `dynamics.com` or `powerapps.com`. The Australian `crm6` host passes. Many waits swallow their failure and carry on, so a test can reach a login or error page and fail later with a less clear message.
12. Form reads and writes go through `Xrm.Page` (deprecated but present in Unified Interface) by `page.evaluate`; `FormComponent.execute` runs any function the test gives it in the app page.
13. Defaults assume the public cloud (`make.powerapps.com`, `apps.powerapps.com`, `login.microsoftonline.com`), with overrides except the canvas play URL built from IDs. English labels throughout.
14. `GenUxPage` drives the maker portal's AI page designer: it creates, publishes and deletes apps, and can delete every app whose name starts with a prefix (no cap). The kit never uses it, and specs must not.
15. Selectors: the toolkit's own locators mix roles and accessible names with Fluent and ag-Grid attributes, class fragments and some XPath. That is the toolkit's business; the kit's rule binds only the locked specs.
16. Microsoft's sample config sets `ignoreHTTPSErrors: true`, records video for every test, retries twice in CI and runs fully parallel outside CI. The kit does none of these.
17. The toolkit's `getAuthToken` can pull any MSAL or cookie token out of a storage state file. Not used by the kit. The storage state is a live credential: the kit keeps it under `.auth/`, never in evidence.

**Dependencies (from Microsoft's lockfile)**
18. The kit needs 58 packages: Playwright 1.64.1, `@axe-core/playwright` and `axe-core` 4.12.1 (MPL-2.0), `dotenv`, `playwright-ms-auth` and its Azure SDK, MSAL, `jsonwebtoken` and small helpers, plus TypeScript 5.9.3 and `@types/node` for the type check. All MIT, Apache-2.0, BSD, ISC or 0BSD apart from axe. None has an install script. Microsoft's lockfile resolves them from its own Azure Artifacts mirrors; the kit's lockfile keeps the same sha512 values and points at registry.npmjs.org, so `npm ci` fails if any tarball differs.
