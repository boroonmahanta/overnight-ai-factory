/**
 * Locked UI tests for low-code apps (plan 5.8). The gate runs this from gate/playwright:
 *
 *   npm ci
 *   npx playwright test --config playwright.lcp.config.ts --reporter=html,junit
 *
 * Settings follow Microsoft's advice for a shared Dataverse environment: one worker,
 * no full parallel, one retry in CI, a trace on the first retry.
 */
import * as path from 'node:path';
import { defineConfig } from '@playwright/test';
import { isCI, kitPaths, localRunId, specsDir } from './lib/env';

// One run ID for the whole run. Workers inherit it.
process.env.RUN_ID ??= localRunId();

// The gate's --reporter=html,junit drops the reporter options below, so the output
// paths are also set where Playwright looks first.
const junitFile = path.join(kitPaths.evidenceDir, 'junit.xml');
const htmlDir = path.join(kitPaths.evidenceDir, 'playwright-report');
process.env.PLAYWRIGHT_JUNIT_OUTPUT_FILE ??= junitFile;
process.env.PLAYWRIGHT_HTML_OUTPUT_DIR ??= htmlDir;
process.env.PLAYWRIGHT_HTML_OPEN ??= 'never';

const selfTest = process.env.LCP_KIT_SELF_TEST === '1';

export default defineConfig({
  // One tsconfig for every file, so specs outside the kit (the PR's tests) can import 'lcp-kit'.
  tsconfig: './tsconfig.json',
  testDir: specsDir,
  testMatch: ['**/*.spec.ts', '**/*.test.ts'],
  workers: 1,
  fullyParallel: false,
  retries: isCI ? 1 : 0,
  forbidOnly: isCI,
  timeout: 6 * 60_000,
  expect: { timeout: 30_000 },
  outputDir: path.join(kitPaths.evidenceDir, 'artifacts'),
  reporter: [
    ['list'],
    ['html', { outputFolder: htmlDir, open: 'never' }],
    ['junit', { outputFile: junitFile }],
  ],
  use: {
    baseURL: process.env.TEST_ENV_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'off',
    viewport: { width: 1920, height: 1080 },
    // Microsoft's toolkit matches English labels.
    locale: 'en-US',
    actionTimeout: 60_000,
    navigationTimeout: 60_000,
  },
  projects: [
    {
      name: 'sign-in',
      testDir: kitPaths.lib,
      testMatch: 'sign-in.setup.ts',
      retries: 0,
      timeout: 4 * 60_000,
    },
    {
      name: 'model-driven',
      grepInvert: /@canvas\b/,
      dependencies: ['sign-in'],
      use: { storageState: kitPaths.mdaState },
    },
    {
      name: 'canvas',
      grep: /@canvas\b/,
      dependencies: ['sign-in'],
      use: { storageState: kitPaths.canvasState },
    },
    // The kit's own checks: no browser, no sign-in. LCP_KIT_SELF_TEST=1 ... --project kit-self-test
    ...(selfTest ? [{ name: 'kit-self-test', testDir: kitPaths.kitTests, testMatch: '*.check.ts' }] : []),
  ],
});
