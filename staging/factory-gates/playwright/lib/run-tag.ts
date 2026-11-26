/**
 * Run tags (locked-scenarios.md, "Run tags"): every row a test makes carries
 * lcp-run:<run ID>/<test ID> in one text column of at least 100 characters, so
 * the test can delete it and the nightly sweeper can find what was left.
 *
 * Model-driven only in v0. Rows are made and deleted through the app's own client
 * API (Xrm.WebApi), inside the signed-in page, so they are made as the test user.
 */
import * as path from 'node:path';
import type { Page, TestInfo } from '@playwright/test';

export const RUN_TAG_PREFIX = 'lcp-run:';
/** The tag column's minimum size in the conventions, and so the tag's maximum. */
export const RUN_TAG_MAX = 100;
/** A UI test's ID: ui-<slug>-<nn>, lower case, at most 40 characters. */
export const UI_TEST_ID = /^ui-[a-z0-9]+(?:-[a-z0-9]+)*-\d{2}$/;
const ID_MAX = 40;
/** A Dataverse logical name, such as nwind_orders or nwind_sampledataoriginalid. */
const LOGICAL_NAME = /^[a-z][a-z0-9_]*$/;

/** The test ID, from a spec file named <id>.spec.ts (or <id>.test.ts). */
export function testIdOf(file: string): string {
  const name = path.basename(file);
  const id = name.replace(/\.(spec|test)\.ts$/, '');
  if (id === name || !UI_TEST_ID.test(id) || id.length > ID_MAX) {
    throw new Error(
      `A UI test file is named <id>.spec.ts, with an id like ui-order-form-01 ` +
        `(lower case, at most ${ID_MAX} characters). Got: ${name}`,
    );
  }
  return id;
}

export function runTagFor(runId: string, testId: string): string {
  if (!runId || /[\s/]/.test(runId)) {
    throw new Error(`RUN_ID must be set, with no spaces or slashes. Got: "${runId}"`);
  }
  const tag = `${RUN_TAG_PREFIX}${runId}/${testId}`;
  if (tag.length > RUN_TAG_MAX) {
    throw new Error(`The run tag is ${tag.length} characters; the tag column holds ${RUN_TAG_MAX}: ${tag}`);
  }
  return tag;
}

/** This test's run tag. RUN_ID comes from the gate (the config sets one for local runs). */
export function runTag(testInfo: Pick<TestInfo, 'file'>): string {
  return runTagFor(process.env.RUN_ID ?? '', testIdOf(testInfo.file));
}

function checkLogicalName(kind: string, name: string): void {
  if (!LOGICAL_NAME.test(name)) {
    throw new Error(`${kind} must be a Dataverse logical name (lower case, with its prefix). Got: "${name}"`);
  }
}

function plainId(id: string): string {
  return id.replace(/[{}]/g, '').toLowerCase();
}

type Made = { table: string; id: string };

/**
 * Rows this test made, tagged, and deleted at the end whether the test passed or not.
 * A failed delete does not fail the test: it is noted on the test, and the sweeper
 * finds the row by its tag later.
 */
export class TaggedRows {
  private readonly made: Made[] = [];

  constructor(
    private readonly page: Page,
    /** The run tag written on every row. */
    readonly runTag: string,
  ) {}

  /** Seed a row before the act. Lookups use Web API syntax: "nwind_customerid@odata.bind": "/nwind_customerses(<id>)". */
  async create(table: string, tagColumn: string, fields: Record<string, unknown>): Promise<string> {
    checkLogicalName('table', table);
    checkLogicalName('tagColumn', tagColumn);
    if (tagColumn in fields) {
      throw new Error(`fields must not set ${tagColumn}: the kit writes the run tag there`);
    }
    const data = { ...fields, [tagColumn]: this.runTag };
    const id = await this.page.evaluate(
      async ({ table, data }) => {
        const xrm = (window as unknown as { Xrm?: any }).Xrm;
        if (!xrm?.WebApi) throw new Error('Xrm.WebApi is not available: open the model-driven app first');
        const result = await xrm.WebApi.createRecord(table, data);
        return String(result.id);
      },
      { table, data },
    );
    this.made.push({ table, id: plainId(id) });
    return plainId(id);
  }

  /** Tag a row the test made through the UI, and delete it at the end. */
  async tag(table: string, id: string, tagColumn: string): Promise<void> {
    checkLogicalName('table', table);
    checkLogicalName('tagColumn', tagColumn);
    const row = { table, id: plainId(id) };
    this.made.push(row); // tracked first, so it is deleted even if tagging fails
    await this.page.evaluate(
      async ({ table, id, data }) => {
        const xrm = (window as unknown as { Xrm?: any }).Xrm;
        if (!xrm?.WebApi) throw new Error('Xrm.WebApi is not available: open the model-driven app first');
        await xrm.WebApi.updateRecord(table, id, data);
      },
      { ...row, data: { [tagColumn]: this.runTag } },
    );
  }

  /** Called by the fixture after the test. */
  async cleanup(testInfo: TestInfo): Promise<void> {
    const failed: string[] = [];
    for (const row of [...this.made].reverse()) {
      try {
        await this.page.evaluate(
          async ({ table, id }) => {
            const xrm = (window as unknown as { Xrm?: any }).Xrm;
            if (!xrm?.WebApi) throw new Error('Xrm.WebApi is not available');
            await xrm.WebApi.deleteRecord(table, id);
          },
          row,
        );
      } catch (error) {
        failed.push(`${row.table} ${row.id}: ${(error as Error).message}`);
      }
    }
    if (failed.length) {
      testInfo.annotations.push({ type: 'cleanup-failed', description: `${this.runTag}: ${failed.join('; ')}` });
    }
  }
}
