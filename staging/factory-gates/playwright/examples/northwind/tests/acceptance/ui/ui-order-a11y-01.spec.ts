/**
 * ui-order-a11y-01: the Orders view and form pass the accessibility checks (plan 5.9):
 * an axe-core pass against the kit's baseline of known platform faults, and a
 * keyboard-only journey.
 *
 * Example for Microsoft's Northwind Traders sample (decision D6), model-driven app
 * nwind_NorthwindOrdersModeldriven. AC-5 is a stand-in until the Northwind spec for
 * 2539 maps its real criteria. Untested until DG9.
 */
import { checkAccessibility, expect, keyboardJourney, test } from 'lcp-kit';

const ORDERS = 'nwind_orders';
const TAG_COLUMN = 'nwind_sampledataoriginalid';

test('the Orders view and a new order form have no new accessibility faults', { tag: ['@AC-5'] }, async ({ page, modelDrivenApp }, testInfo) => {
  await modelDrivenApp.navigateToGridView(ORDERS);
  await checkAccessibility(page, testInfo, 'model-driven', 'orders-view');

  await modelDrivenApp.navigateToFormView(ORDERS);
  await checkAccessibility(page, testInfo, 'model-driven', 'order-form');
});

test('a new order can be made with the keyboard alone', { tag: ['@AC-5'] }, async ({ page, modelDrivenApp, rows }, testInfo) => {
  const orderNumber = `KB${Math.floor(Math.random() * 1_000_000).toString().padStart(6, '0')}`;
  await modelDrivenApp.navigateToFormView(ORDERS);

  await keyboardJourney(page, testInfo, [
    { reach: { role: 'textbox', name: 'Order Number' }, then: [{ type: orderNumber }] },
    { reach: { role: 'textbox', name: 'Notes' }, then: [{ type: 'Made with the keyboard alone.' }, { press: 'Control+S' }] },
  ]);

  await expect.poll(async () => (await modelDrivenApp.form.getContext()).entityId).not.toBe('');
  const saved = await modelDrivenApp.form.getContext();
  await rows.tag(ORDERS, saved.entityId, TAG_COLUMN);
  expect(await modelDrivenApp.form.getAttribute('nwind_ordernumber')).toBe(orderNumber);
});
