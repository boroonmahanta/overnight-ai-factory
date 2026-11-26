# Playwright kit v0 for locked UI tests

Draft, ADO 2546 (DG7 part 2), Session 52, 25 November 2026. Moves to `GetAI-IP/factory-gates` as `playwright/` in the move (2739, decision D1); the gate runs it from `gate/playwright`. **Nothing here has signed in or run against an environment yet:** that is DG9, in `factory-test` on Northwind. Plan 5.8 (UI row, selector rule, flakiness controls), 5.9 (Accessibility) and 13 (the kit).

## What is here

| Path | What it is |
|---|---|
| `playwright.lcp.config.ts` | The config the gate runs |
| `package.json`, `package-lock.json` | Exact pins. The lockfile carries Microsoft's sha512 for each of the 58 packages, so `npm ci` installs exactly what Microsoft tested |
| `tsconfig.json` | Maps `lcp-kit` and `power-platform-playwright-toolkit` to source here, and the config applies it to every spec, even the PR's |
| `lib/` | Our helpers: `fixtures.ts` (the `test` every spec uses), `selectors.ts`, `run-tag.ts`, `a11y.ts`, `keyboard.ts`, `sign-in.setup.ts`, `env.ts` |
| `a11y-baseline.json` | Known platform accessibility faults. Empty until DG9 sees some |
| `examples/northwind/tests/acceptance/ui/` | Three example specs on Northwind's model-driven app |
| `kit-tests/kit.check.ts` | The kit's own checks: no browser, no sign-in |
| `vendor/power-platform-playwright-toolkit/` | Microsoft's toolkit at commit `3233f3e`, unchanged, MIT. `PROVENANCE.md` says where from; the full read is `docs/analysis/playwright-kit-reading-notes.md` in the planning repo |

## How the gate runs it

```bash
npm ci --ignore-scripts --no-audit --no-fund --no-update-notifier
```

```bash
npx playwright install --with-deps chromium
```

```bash
npx playwright test --config playwright.lcp.config.ts --reporter=html,junit
```

The config:
- reads specs from `TEST_SPECS_DIR` (`*.spec.ts`, and `*.test.ts`, Microsoft's naming);
- one worker, no full parallel, one retry in CI, a trace on the first retry, a screenshot on failure, no video;
- reporters list, HTML and JUnit, written under `LCP_EVIDENCE_DIR` (default `test-results/`): `junit.xml`, `playwright-report/` and `artifacts/`. The gate's `--reporter=html,junit` drops the config's reporter options, so the config also sets `PLAYWRIGHT_JUNIT_OUTPUT_FILE` and `PLAYWRIGHT_HTML_OUTPUT_DIR`, which Playwright reads first. Shown working with that exact command on 25 November;
- three projects: `sign-in` (once per run, below), `model-driven` (storage state `.auth/mda.json`, every test not tagged `@canvas`) and `canvas` (`.auth/canvas.json`, tests tagged `@canvas`). Both depend on `sign-in`;
- sets `RUN_ID` for local runs if the gate has not.

`.auth/` holds live session cookies. Never upload it or put it under the evidence folder. The verifier step reads `.auth/mda.json`, as Appendix A already says.

## Sign-in variables (settled from the code)

Session 46 (finding 5) saw that the gate passes `KEYVAULT_NAME` while Microsoft's material speaks of other names. Reading the code settles it: the variables are read by `playwright-ms-auth` (`loadConfigFromEnv`), which the toolkit wraps.

| Variable | Value in the gate | Read by |
|---|---|---|
| `MS_AUTH_EMAIL` | The project's test user (2541) | `playwright-ms-auth` |
| `MS_AUTH_CREDENTIAL_TYPE` | `certificate` | `playwright-ms-auth`; the toolkit also checks it |
| `MS_AUTH_CREDENTIAL_PROVIDER` | `azure-keyvault` | `playwright-ms-auth` |
| `MS_AUTH_KEYVAULT_ENDPOINT` | `https://<vault>.vault.azure.net/` (a URL, not the vault's name) | `playwright-ms-auth` |
| `MS_AUTH_KEYVAULT_SECRET_NAME` | The name of the test user's Key Vault certificate (its secret has the same name) | `playwright-ms-auth` |
| `MODEL_DRIVEN_APP_URL` | `<Test URL>main.aspx?appid=<the app's ID>` | the kit (Microsoft's sample's name) |
| `CANVAS_APP_URL` | Only for a project with canvas specs | the kit (Microsoft's name) |
| `TEST_SPECS_DIR` | `${{ github.workspace }}/pr/tests/acceptance/ui` | the kit |
| `LCP_EVIDENCE_DIR` | `${{ github.workspace }}/evidence/playwright` | the kit |
| `RUN_ID`, `TEST_ENV_URL`, `CI` | Already set in the job | the kit |

Not used: `KEYVAULT_NAME`, `AZURE_KEYVAULT_URL`, `AZURE_CERTIFICATE_NAME`, and `AZURE_TENANT_ID` (read only by a toolkit helper the kit does not call).

What sign-in needs beyond the variables:
- **The job signed in to Azure as the Test identity before this step.** The Key Vault provider tries the Azure CLI first, and `verify-in-test` already runs `azure/login`.
- **The Test identity may read the certificate's secret** ("Key Vault Secrets User" on the vault, or on that one secret). For 3060 and 2541.
- **A Key Vault certificate in PKCS#12**, so its secret's content type is `application/x-pkcs12`. Anything else is read as a password and sign-in fails.
- **Microsoft Edge on the runner.** `playwright-ms-auth` signs in with the `msedge` channel. GitHub's hosted Ubuntu 24.04 image has Edge 157 (image 20261116); a self-hosted runner needs it.
- **Playwright's Chromium** for the tests themselves: the `playwright install` line above. `npm ci` does not fetch browsers.

### The change to the gate step (a gate pull request later, at Boroon's word)

Appendix A's "Locked Playwright suite" step today passes `MS_AUTH_CREDENTIAL_TYPE`, `MS_AUTH_CREDENTIAL_PROVIDER`, `KEYVAULT_NAME` and `TEST_SPECS_DIR`, runs `npm ci`, then the tests. It should become:

```yaml
      - name: Locked Playwright suite (certificate test user)
        if: steps.settings.outputs.ui == 'true'
        working-directory: gate/playwright
        env:
          MS_AUTH_EMAIL: ${{ steps.settings.outputs.test_user }}
          MS_AUTH_CREDENTIAL_TYPE: certificate
          MS_AUTH_CREDENTIAL_PROVIDER: azure-keyvault
          MS_AUTH_KEYVAULT_ENDPOINT: https://${{ vars.LCP_KEYVAULT }}.vault.azure.net/
          MS_AUTH_KEYVAULT_SECRET_NAME: ${{ steps.settings.outputs.test_user_cert }}
          MODEL_DRIVEN_APP_URL: ${{ vars.LCP_TEST_ENV_URL }}main.aspx?appid=${{ steps.settings.outputs.mda_app_id }}
          TEST_SPECS_DIR: ${{ github.workspace }}/pr/tests/acceptance/ui
          LCP_EVIDENCE_DIR: ${{ github.workspace }}/evidence/playwright
        run: |
          set -euo pipefail
          npm ci --ignore-scripts --no-audit --no-fund --no-update-notifier
          npx playwright install --with-deps chromium
          npx playwright test --config playwright.lcp.config.ts --reporter=html,junit
```

The changes, one by one:
1. `KEYVAULT_NAME` becomes `MS_AUTH_KEYVAULT_ENDPOINT`, as a URL.
2. Add `MS_AUTH_EMAIL`, `MS_AUTH_KEYVAULT_SECRET_NAME`, `MODEL_DRIVEN_APP_URL` and `LCP_EVIDENCE_DIR`.
3. `npm ci` gains `--ignore-scripts --no-audit --no-fund --no-update-notifier`, as the Copilot CLI install in the same job does.
4. Add `npx playwright install --with-deps chromium`.
5. Proposed, not settled: the test user, its certificate's name, the app's ID and whether the project has UI tests come from the project's `gate.json` in the gate repo (where a pull request cannot change them), through `project_settings.py` with four new outputs. That step runs after the Playwright step today, so it moves up. A project with no `tests/acceptance/ui/` would otherwise still sign in. The other way is project variables in the caller repo.

## Writing a locked UI spec

The conventions are in `staging/factory-manifestos/conventions/locked-scenarios.md` ("UI tests"). In short, with the kit:

```ts
import { expect, named, test } from 'lcp-kit';

test('a new order saves', { tag: ['@AC-4'] }, async ({ page, modelDrivenApp, rows }) => {
  await modelDrivenApp.navigateToFormView('nwind_orders');
  await named(page, { role: 'textbox', name: 'Order Number' }).fill('UI123456');
  // ...save, then tag the row the UI made so it is deleted after the test:
  await rows.tag('nwind_orders', (await modelDrivenApp.form.getContext()).entityId, 'nwind_sampledataoriginalid');
});
```

- **File and ID:** `tests/acceptance/ui/<id>.spec.ts`, ID `ui-<slug>-<nn>`. The `runTag` fixture refuses any other name.
- **Criteria:** every test has `{ tag: ['@AC-<n>'] }`. A canvas test also has `@canvas`, which puts it in the canvas project (an addition to the conventions, for the scenario session to take in).
- **Selectors:** `named()` takes a role and accessible name, a label, or (canvas only) a control name. It has no way to take a CSS selector. The kit's checks fail an example spec that calls `.locator(`.
- **Run tags:** `rows.create(table, tagColumn, fields)` seeds a row with the run tag; `rows.tag(table, id, tagColumn)` tags a row the UI made. Both delete the row after the test, pass or fail; a failed delete is noted on the test, and the sweeper finds the row later. Rows are made and deleted with `Xrm.WebApi` inside the signed-in app, so as the test user. Model-driven only.
- **One at a time:** one worker, so no two tests ever run together. Before anyone raises `workers`, tests that change the same table must be put in one serial group.
- **Accessibility:** `checkAccessibility(page, testInfo, 'canvas' | 'model-driven', label)` runs axe-core (WCAG 2.0 and 2.1, A and AA), inside `iframe[name="fullscreen-app-host"]` for canvas, on the whole page for model-driven. It fails on any fault from "moderate" up that `a11y-baseline.json` does not list, as the solution checker fails Accessibility from Medium. The full axe result is attached to the test.
- **Keyboard:** `keyboardJourney(page, testInfo, steps)` reaches each named control with Tab alone and acts with keys alone, then attaches the focus order.
- **Never** use the toolkit's `GenUxPage`: it creates, publishes and deletes apps.

The baseline is in the gate repo on purpose: a project cannot excuse its own faults. An entry needs `surface`, `rule`, a `reason` saying why it is the platform's fault, and `added`; `target_contains` narrows it.

## Northwind examples

Northwind as the factory imports it (`AI-Business-Solutions/ai-factory-nwt`, prefix `nwind`) has no canvas apps (they were left out, Session 48), so all three examples are model-driven, on the app `nwind_NorthwindOrdersModeldriven`. Its site map has one entry, Orders (`nwind_orders`); the Orders form has Order Number (text, 8 characters), Order Status, Order Date, Customer, Employee, Paid Date, Tax Status and Notes; no column is required; quick find searches Order Number.

| ID | Criteria (stand-ins) | What it checks |
|---|---|---|
| `ui-order-grid-01` | `@AC-3` | A seeded, tagged order is found in the Orders view by quick find and opens on its form |
| `ui-order-form-01` | `@AC-4` | An order typed into the form saves, with its number |
| `ui-order-a11y-01` | `@AC-5` | The Orders view and a new order form pass axe against the baseline; an order can be made with the keyboard alone |

`AC-3` to `AC-5` are stand-ins, numbered after the scenario examples' `AC-1` and `AC-2`, until the Northwind spec for 2539 maps its real criteria.

## Checks with no sign-in (run 25 November 2026, in a scratch copy)

| Check | Command | Result |
|---|---|---|
| Install | `npm ci --ignore-scripts` | 58 packages, every one matching its sha512; `npm ls --all` clean |
| Type check | `npm run typecheck` | Passes, the vendored toolkit included |
| List | `npm run list` | 6 tests in 4 files: 2 sign-in steps and the 4 Northwind tests. Also from a folder outside the kit, as the gate's `TEST_SPECS_DIR` will be |
| Kit checks | `LCP_KIT_SELF_TEST=1 npx playwright test --config playwright.lcp.config.ts --project kit-self-test --reporter=html,junit` | 9 passed, with `junit.xml` and the HTML report in the evidence folder. A spec with no criteria tag, and one with a CSS selector, each failed its check |

Node 20 or later (tried on 26.5).

## Open for DG9 and after

1. Nothing has signed in. Untested: signing in straight at the model-driven app's URL (Microsoft's script signs in at the maker portal first, then opens the app), the redirect check in `playwright-ms-auth`, and certificate sign-in under the tenant's Conditional Access (spike 0.11, 2447).
2. The test user needs a security role that can create, read and delete `nwind_orders` rows. Basic User alone may not reach Northwind's tables (2541).
3. Names to confirm in `factory-test`: the Save command ("Save (CTRL+S)", a menu item), the text boxes' names (their field labels), and whether Ctrl+S saves in headless Chromium.
4. The model-driven axe pass covers the whole page. Narrow it to the form if DG9 finds a stable container; fill the baseline with the platform faults it finds, each with a reason.
5. Each model-driven launch waits a fixed 30 seconds inside the toolkit, so four tests cost at least two minutes of waiting. Time them against plan 5.8's estimates.
6. `playwright-ms-auth` is one person's package (risk recorded in the reading notes). Pinned by sha512 at 0.0.19; 0.0.20 exists.
7. A lint in the gate for the selector rule on the project's specs, not only the kit's examples (2538 or later).
8. Canvas: the project, the storage state and `checkAccessibility`'s canvas scope exist, untested, with no example.
