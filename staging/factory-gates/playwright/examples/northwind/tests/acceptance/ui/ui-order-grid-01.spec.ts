/**
 * ui-order-grid-01: the Orders view finds an order by its number and opens it on its form.
 *
 * Example for Microsoft's Northwind Traders sample (decision D6), model-driven app
 * nwind_NorthwindOrdersModeldriven. Written on the toolkit's API after Microsoft's
 * model-driven samples (power-platform-playwright-samples, packages/e2e-tests, MIT),
 * with their CSS selectors replaced by accessible names.
 * AC-3 is a stand-in until the Northwind spec for 2539 maps its real criteria.
 * Untested until DG9.
 */
import { expect, named, test } from 'lcp-kit';

const ORDERS = 'nwind_orders';
const TAG_COLUMN = 'nwind_sampledataoriginalid';

/** Order Number holds 8 characters. Made up, never real data. */
function newOrderNumber(): string {
  return `UI${Math.floor(Math.random() * 1_000_000).toString().padStart(6, '0')}`;
}

test('an order in the Orders view opens on its form', { tag: ['@AC-3'] }, async ({ page, modelDrivenApp, rows }) => {
  const orderNumber = newOrderNumber();
  await rows.create(ORDERS, TAG_COLUMN, { nwind_ordernumber: orderNumber });

  await modelDrivenApp.navigateToGridView(ORDERS);
  // Quick find searches Order Number ("Quick Find Active Orders").
  await modelDrivenApp.grid.filterByKeyword(orderNumber);
  await expect.poll(() => modelDrivenApp.grid.getRowCount()).toBe(1);
  await modelDrivenApp.grid.openRecord({ columnName: 'nwind_ordernumber', columnValue: orderNumber });

  await expect(named(page, { role: 'textbox', name: 'Order Number' })).toHaveValue(orderNumber);
  expect(await modelDrivenApp.form.getAttribute('nwind_ordernumber')).toBe(orderNumber);
});
