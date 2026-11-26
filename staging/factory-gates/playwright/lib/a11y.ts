/**
 * The locked accessibility pass (plan 5.9, layer two): axe-core inside the canvas
 * app's host frame, or on the model-driven page, against a baseline of known
 * platform faults. Our design, not Microsoft guidance [inference].
 *
 * A fault fails the test from "moderate" up, as the solution checker's
 * Accessibility rules fail from Medium. "minor" faults are noted on the test.
 * Known platform faults in a11y-baseline.json are noted, never failed.
 */
import * as fs from 'node:fs';
import AxeBuilder from '@axe-core/playwright';
import { expect, type Page, type TestInfo } from '@playwright/test';
import { kitPaths } from './env';

export type Surface = 'model-driven' | 'canvas';

/** The canvas player's host frame (plan 5.9). */
export const CANVAS_HOST_FRAME = 'iframe[name="fullscreen-app-host"]';
export const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];
export const FAILING_IMPACTS = ['moderate', 'serious', 'critical'];

export interface BaselineEntry {
  /** Which surface the fault is seen on, or both. */
  surface: Surface | 'any';
  /** The axe rule ID, such as "aria-allowed-role". */
  rule: string;
  /** Optional: only nodes whose axe target contains this text. */
  target_contains?: string;
  /** Why it is the platform's fault, not the app's. */
  reason: string;
  /** When it was first seen, YYYY-MM-DD. */
  added: string;
}

export interface Baseline {
  schema_version: 1;
  entries: BaselineEntry[];
}

export interface Finding {
  rule: string;
  impact: string | null;
  target: string;
  help: string;
}

export function parseBaseline(text: string): Baseline {
  const data = JSON.parse(text) as Baseline;
  if (data?.schema_version !== 1 || !Array.isArray(data.entries)) {
    throw new Error('a11y baseline: needs schema_version 1 and an entries list');
  }
  for (const [i, e] of data.entries.entries()) {
    if (!['model-driven', 'canvas', 'any'].includes(e.surface) || !e.rule || !e.reason || !/^\d{4}-\d{2}-\d{2}$/.test(e.added)) {
      throw new Error(`a11y baseline: entry ${i} needs surface, rule, reason and added (YYYY-MM-DD)`);
    }
  }
  return data;
}

export function loadBaseline(file = kitPaths.baseline): Baseline {
  return parseBaseline(fs.readFileSync(file, 'utf8'));
}

function matches(entry: BaselineEntry, finding: Finding, surface: Surface): boolean {
  return (
    (entry.surface === 'any' || entry.surface === surface) &&
    entry.rule === finding.rule &&
    (!entry.target_contains || finding.target.includes(entry.target_contains))
  );
}

/** Split findings into known platform faults and the rest; also list baseline entries nothing matched. */
export function splitByBaseline(findings: Finding[], baseline: Baseline, surface: Surface) {
  const used = new Set<BaselineEntry>();
  const known: Finding[] = [];
  const unknown: Finding[] = [];
  for (const f of findings) {
    const entry = baseline.entries.find((e) => matches(e, f, surface));
    if (entry) {
      used.add(entry);
      known.push(f);
    } else {
      unknown.push(f);
    }
  }
  const unused = baseline.entries.filter((e) => !used.has(e) && (e.surface === 'any' || e.surface === surface));
  return { known, unknown, unused };
}

type AxeViolation = { id: string; impact?: string | null; help: string; nodes: { target: unknown[]; impact?: string | null }[] };

export function findingsOf(violations: AxeViolation[]): Finding[] {
  return violations.flatMap((v) =>
    v.nodes.map((n) => ({
      rule: v.id,
      impact: n.impact ?? v.impact ?? null,
      target: n.target.map(String).join(' >> '),
      help: v.help,
    })),
  );
}

/**
 * Run the pass and fail the test on any fault from "moderate" up that is not a known
 * platform fault. Model-driven: the whole page for now (the form and the shell around
 * it); DG9 may narrow it to the form once its container is known.
 */
export async function checkAccessibility(
  page: Page,
  testInfo: TestInfo,
  surface: Surface,
  label: string = surface,
): Promise<void> {
  let builder = new AxeBuilder({ page }).withTags(WCAG_TAGS);
  if (surface === 'canvas') builder = builder.include(CANVAS_HOST_FRAME);
  const results = await builder.analyze();
  await testInfo.attach(`axe-${label}.json`, {
    body: JSON.stringify(results, null, 2),
    contentType: 'application/json',
  });

  const { known, unknown, unused } = splitByBaseline(findingsOf(results.violations), loadBaseline(), surface);
  const failing = unknown.filter((f) => FAILING_IMPACTS.includes(f.impact ?? ''));
  const minor = unknown.filter((f) => !FAILING_IMPACTS.includes(f.impact ?? ''));
  if (known.length) testInfo.annotations.push({ type: 'a11y-known-platform', description: `${label}: ${known.length} node(s)` });
  if (minor.length) {
    testInfo.annotations.push({ type: 'a11y-minor', description: `${label}: ${minor.map((f) => f.rule).join(', ')}` });
  }
  if (unused.length) {
    testInfo.annotations.push({ type: 'a11y-baseline-unused', description: unused.map((e) => e.rule).join(', ') });
  }
  expect(
    failing.map((f) => `${f.impact} ${f.rule}: ${f.help} [${f.target}]`),
    `Accessibility faults on ${label} that are not known platform faults`,
  ).toEqual([]);
}
