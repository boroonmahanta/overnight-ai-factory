/**
 * Spike 0.11 (ADO 2447): one page in factory-test loads as the test user, from the
 * storage state the kit's sign-in project wrote (.auth/mda.json), with no new sign-in.
 *
 * Probe-only, not a locked spec. Imports 'lcp-kit' from outside the kit, as the gate's
 * TEST_SPECS_DIR will. Prints no cookie, token or ID.
 */
import { expect, test } from 'lcp-kit';

const envUrl = process.env.TEST_ENV_URL ?? '';
const email = process.env.MS_AUTH_EMAIL ?? '';

test('a page in factory-test loads as the test user', { tag: ['@AC-0'] }, async ({ page }) => {
  expect(envUrl, 'TEST_ENV_URL').toMatch(/^https:\/\/factory-test\.crm6\.dynamics\.com\/$/);
  expect(email, 'MS_AUTH_EMAIL').not.toBe('');
  const host = new URL(envUrl).host;

  // Every top-level page the browser lands on: factory-test's host and path, or another
  // host alone (no query, which can carry sign-in context; no sign-in path, which names the tenant).
  const landed: string[] = [];
  page.on('framenavigated', (frame) => {
    if (frame === page.mainFrame()) {
      const url = new URL(frame.url());
      landed.push(url.host === host ? `${url.host}${url.pathname}` : url.host);
    }
  });

  // 1. The page.
  const response = await page.goto(new URL('main.aspx', envUrl).href, { waitUntil: 'load' });
  expect(response?.status() ?? 0, 'main.aspx status').toBeLessThan(400);
  const finalUrl = new URL(page.url());
  console.log(`[probe] pages landed on: ${landed.join(' -> ')}`);
  console.log(`[probe] main.aspx: final host ${finalUrl.host}, path ${finalUrl.pathname}, title "${await page.title()}"`);
  expect(finalUrl.host, 'stayed on factory-test (no sign-in page)').toBe(host);
  if (landed.some((l) => l.startsWith('login.microsoftonline.com'))) {
    console.log('[probe] note: the page passed through the sign-in host on its way (single sign-on from the stored state)');
  }

  // 2. Who the session belongs to, from the Web API, on the stored cookies alone.
  const who = await page.request.get(new URL('api/data/v9.2/WhoAmI', envUrl).href, { maxRedirects: 0 });
  expect(who.status(), 'WhoAmI on the stored session').toBe(200);
  const { UserId } = (await who.json()) as { UserId: string };
  const me = await page.request.get(
    new URL(`api/data/v9.2/systemusers(${UserId})?$select=domainname,accessmode,isdisabled`, envUrl).href,
    { maxRedirects: 0 },
  );
  expect(me.status(), 'read the signed-in user').toBe(200);
  const user = (await me.json()) as { domainname: string; accessmode: number; isdisabled: boolean };
  console.log(`[probe] signed in as ${user.domainname} (access mode ${user.accessmode}, disabled ${user.isdisabled})`);
  expect(user.domainname.toLowerCase(), 'the signed-in user is the test user').toBe(email.toLowerCase());
});
