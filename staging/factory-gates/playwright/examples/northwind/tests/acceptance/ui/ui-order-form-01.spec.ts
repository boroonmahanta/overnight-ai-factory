/**
 * ui-order-form-01: a user creates an order on the Orders form, and it saves.
 *
 * Example for Microsoft's Northwind Traders sample (decision D6), model-driven app
 * nwind_NorthwindOrdersModeldriven. Written on the toolkit's API after Microsoft's
 * model-driven samples (power-platform-playwright-samples, packages/e2e-tests, MIT),
 * with their CSS selectors replaced by accessible names.
 * AC-4 is a stand-in until the Northwind spec for 2539 maps its real criteria.
 * Untested until DG9.
 */
import { expect, named, test } from 'lcp-kit';

const ORDERS = 'nwind_orders';
const TAG_COLUMN = 'nwind_sampledataoriginalid';

function newOrderNumber(): string {
  return `UI${Math.floor(Math.random() * 1_000_000).toString().padStart(6, '0')}`;
}

test('a new order saves with the number and notes typed in', { tag: ['@AC-4'] }, async ({ page, modelDrivenApp, rows }) => {
  const orderNumber = newOrderNumber();
  await modelDrivenApp.navigateToFormView(ORDERS);

  // Typed into the form as a user would, found by accessible name.
  await named(page, { role: 'textbox', name: 'Order Number' }).fill(orderNumber);
  await named(page, { role: 'textbox', name: 'Notes' }).fill('Made by a locked UI test.');
  // The command bar's Save, by its full accessible name (the toolkit's saveRecord() asks for
  // a button named "Save", which also matches "Save & Close"). Name to confirm in DG9.
  await named(page, { role: 'menuitem', name: 'Save (CTRL+S)', exact: true }).click();

  // Saved: the form has an ID and nothing unsaved.
  await expect.poll(async () => (await modelDrivenApp.form.getContext()).entityId).not.toBe('');
  const saved = await modelDrivenApp.form.getContext();
  expect(saved.isDirty).toBe(false);
  // The row was made through the UI, so it is tagged now and deleted after the test.
  await rows.tag(ORDERS, saved.entityId, TAG_COLUMN);

  expect(await modelDrivenApp.form.getAttribute('nwind_ordernumber')).toBe(orderNumber);
});
