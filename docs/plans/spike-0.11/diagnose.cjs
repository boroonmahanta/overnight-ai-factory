/**
 * Spike 0.11 (ADO 2447) diagnostic. Drives the same sign-in as playwright-ms-auth 0.0.19
 * (lib/authenticate.js), with its own Key Vault provider and certificate route, but waits
 * for each page instead of checking at once (its isVisible checks do not wait), and prints
 * what Entra shows: the page's accessible names (headings, links, buttons, text), with no
 * link URLs. Saves no storage state. Prints no certificate, token, cookie or URL query.
 *
 * Run from the kit's folder (gate/playwright), so its pinned packages resolve:
 *   node ../../probe/diagnose.cjs
 */
'use strict';
const path = require('node:path');
const { createRequire } = require('node:module');

const kit = createRequire(path.join(process.cwd(), 'package.json'));
const { chromium } = kit('@playwright/test');
const msauth = kit('playwright-ms-auth');

const LOGIN = 'login.microsoftonline.com';
const isCertauth = (url) => new URL(url).host.endsWith(`certauth.${LOGIN}`);

/** Where the page is: the sign-in host alone (its path names the tenant), or host and path. */
function where(page) {
  const url = new URL(page.url());
  return url.host.endsWith(LOGIN) ? url.host : `${url.host}${url.pathname}`;
}

const hostOnly = (text) => text.replace(/https?:\/\/[^\s"')]+/g, (u) => {
  try { return new URL(u).host; } catch { return '<url>'; }
});

async function show(page, label) {
  await page.waitForLoadState('domcontentloaded').catch(() => {});
  await page.waitForTimeout(3000);
  console.log(`--- ${label}: on ${where(page)}, title "${await page.title().catch(() => '')}"`);
  if (!new URL(page.url()).host.endsWith(LOGIN)) return; // only Entra's own pages are shown
  const snapshot = await page.locator('body').ariaSnapshot().catch((e) => `(no snapshot: ${e.message})`);
  const lines = snapshot.split('\n').filter((l) => !/\/url:/.test(l)).map(hostOnly);
  console.log(lines.slice(0, 80).join('\n'));
  const text = await page.locator('body').innerText().catch(() => '');
  const codes = [...new Set(text.match(/AADSTS\d+/g) || [])];
  if (codes.length) console.log(`--- error codes on the page: ${codes.join(', ')}`);
}

async function main() {
  const config = msauth.loadConfigFromEnv();
  msauth.validateConfig(config);
  if (config.credentialType !== 'certificate' || config.credentialProvider !== 'azure-keyvault') {
    throw new Error('certificate from Key Vault only');
  }
  const provider = msauth.CredentialProviderFactory.createProvider(config.credentialProvider, config.providerConfig);
  const credential = await provider.getCredential();
  if (credential.type !== 'certificate') throw new Error(`the secret was read as a ${credential.type}`);

  const browser = await chromium.launch({ headless: true, channel: 'msedge', args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const context = await browser.newContext();
  const page = await context.newPage();
  const certauth = [];
  page.on('response', (r) => { if (isCertauth(r.url())) certauth.push(`${new URL(r.url()).host} HTTP ${r.status()}`); });
  try {
    await msauth.addCertAuthRoute(page, { pfx: credential.value, authEndpoint: LOGIN });
    await page.goto(process.env.MODEL_DRIVEN_APP_URL, { waitUntil: 'domcontentloaded' });
    await page.waitForURL((u) => u.host === LOGIN, { timeout: 30_000 });
    await show(page, 'the first sign-in page');
    await page.getByRole('textbox', { name: 'email' }).fill(config.email);
    await page.getByRole('button', { name: 'next' }).click();
    await show(page, 'after Next');

    const cert = page.getByRole('link', { name: /certificate/i }).or(page.getByRole('button', { name: /certificate/i }));
    const other = page.getByRole('link', { name: /other ways|sign-in options/i })
      .or(page.getByRole('button', { name: /other ways|sign-in options/i }));
    if (!(await cert.first().isVisible()) && (await other.first().isVisible())) {
      console.log(`--- clicking "${((await other.first().textContent()) || '').trim()}"`);
      await other.first().click();
      await show(page, 'after the other ways control');
    }
    const found = await cert.first().waitFor({ state: 'visible', timeout: 15_000 }).then(() => true, () => false);
    if (!found) {
      console.log('--- no certificate control within 15 s of the page above');
    } else {
      console.log(`--- clicking "${((await cert.first().textContent()) || '').trim()}"`);
      await cert.first().click();
      await page.waitForResponse((r) => isCertauth(r.url()), { timeout: 60_000 })
        .then(() => console.log('--- certauth answered'), () => console.log('--- no certauth response in 60 s'));
      await page.waitForURL((u) => !u.host.endsWith(LOGIN), { timeout: 30_000 }).catch(() => {});
      if (new URL(page.url()).host.endsWith(LOGIN)) {
        await show(page, 'after the certificate');
        const stay = page.getByRole('heading', { name: /stay signed in/i });
        if (await stay.isVisible()) {
          console.log('--- "Stay signed in?": clicking Yes');
          await page.getByRole('button', { name: /^yes$/i }).click();
          await page.waitForURL((u) => !u.host.endsWith(LOGIN), { timeout: 30_000 }).catch(() => {});
        }
      }
    }
    console.log(`--- certauth responses: ${certauth.join(', ') || 'none'}`);
    const done = !new URL(page.url()).host.endsWith(LOGIN);
    console.log(`--- final: ${done ? `off the sign-in host, on ${where(page)}, title "${await page.title()}"` : 'still on the sign-in host'}`);
    if (!done) process.exitCode = 1;
  } finally {
    await context.close(); // nothing saved: no storageState call
    await browser.close();
  }
}

main().catch((e) => {
  console.log(`::error::${hostOnly(String(e && e.message ? e.message : e).split('\n')[0])}`);
  process.exit(1);
});
