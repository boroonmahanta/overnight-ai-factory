/**
 * The fixtures every locked UI test uses. Adapted from Microsoft's mda.fixtures.ts
 * (power-platform-playwright-samples, packages/e2e-tests/fixtures, MIT, at the pin in
 * vendor/power-platform-playwright-toolkit/PROVENANCE.md).
 */
import { test as base, expect } from '@playwright/test';
import { AppLaunchMode, AppProvider, AppType, ModelDrivenAppPage } from 'power-platform-playwright-toolkit';
import { runTag, TaggedRows } from './run-tag';

type KitFixtures = {
  /** lcp-run:<run ID>/<test ID>, for rows this test makes. */
  runTag: string;
  /** The model-driven app at MODEL_DRIVEN_APP_URL, launched and ready. */
  modelDrivenApp: ModelDrivenAppPage;
  /** Rows this test makes, tagged and deleted at the end. Needs the model-driven app. */
  rows: TaggedRows;
};

export const test = base.extend<KitFixtures>({
  // eslint-disable-next-line no-empty-pattern
  runTag: async ({}, use, testInfo) => {
    await use(runTag(testInfo));
  },

  modelDrivenApp: async ({ page, context }, use) => {
    const directUrl = process.env.MODEL_DRIVEN_APP_URL;
    if (!directUrl) {
      throw new Error('MODEL_DRIVEN_APP_URL is not set: https://<env>.crm6.dynamics.com/main.aspx?appid=<app id>');
    }
    const provider = new AppProvider(page, context);
    await provider.launch({
      app: 'model-driven app under test',
      type: AppType.ModelDriven,
      mode: AppLaunchMode.Play,
      skipMakerPortal: true,
      directUrl,
    });
    await use(provider.getModelDrivenAppPage());
  },

  rows: async ({ page, runTag, modelDrivenApp }, use, testInfo) => {
    void modelDrivenApp; // Xrm.WebApi exists only once the app is open
    const rows = new TaggedRows(page, runTag);
    await use(rows);
    await rows.cleanup(testInfo);
  },
});

export { expect };
