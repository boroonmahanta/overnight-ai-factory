/**
 * Sign in as the certificate test user, once per run, before any spec (the
 * "sign-in" project). Uses playwright-ms-auth's authenticate(), as Microsoft's
 * toolkit does, reading the MS_AUTH_* variables (README, "Sign-in variables").
 *
 * Unlike Microsoft's sample script, this signs in straight at the app's own URL
 * (no maker portal step first), never reuses an old sign-in, and keeps one copy of
 * the session only: .auth/mda.json or .auth/canvas.json. Untested until DG9.
 */
import * as fs from 'node:fs';
import * as path from 'node:path';
import { test as setup } from '@playwright/test';
import { authenticate, getStorageStatePath, loadConfigFromEnv, validateConfig } from 'playwright-ms-auth';
import { isCI, kitPaths } from './env';

async function signIn(url: string, statePath: string, waitForMsalTokens: boolean): Promise<void> {
  // playwright-ms-auth writes under MS_AUTH_OUTPUT_DIR (read each time it builds a path).
  process.env.MS_AUTH_OUTPUT_DIR = path.join(kitPaths.authDir, 'ms-auth');
  const config = { ...loadConfigFromEnv(), headless: true, waitForMsalTokens };
  validateConfig(config);
  if (isCI && (config.credentialType !== 'certificate' || config.credentialProvider !== 'azure-keyvault')) {
    throw new Error('In CI the kit signs in only with a certificate from Key Vault (MS_AUTH_CREDENTIAL_TYPE, MS_AUTH_CREDENTIAL_PROVIDER)');
  }
  const ms = getStorageStatePath(config.email);
  fs.rmSync(ms, { force: true }); // a fresh sign-in every run
  await authenticate(config, url);
  fs.mkdirSync(path.dirname(statePath), { recursive: true });
  fs.copyFileSync(ms, statePath);
  fs.rmSync(ms, { force: true });
}

setup('sign in to the model-driven app', async () => {
  const url = process.env.MODEL_DRIVEN_APP_URL;
  setup.skip(!url, 'MODEL_DRIVEN_APP_URL is not set');
  // A model-driven app keeps its session in cookies, so no MSAL tokens to wait for.
  await signIn(url!, kitPaths.mdaState, false);
});

setup('sign in to the canvas app', async () => {
  const url = process.env.CANVAS_APP_URL;
  setup.skip(!url, 'CANVAS_APP_URL is not set');
  await signIn(url!, kitPaths.canvasState, true);
});
