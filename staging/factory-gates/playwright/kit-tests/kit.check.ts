/**
 * The kit's own checks. No browser and no sign-in:
 *   LCP_KIT_SELF_TEST=1 npx playwright test --config playwright.lcp.config.ts --project kit-self-test
 */
import * as fs from 'node:fs';
import * as path from 'node:path';
import { expect, test, type Page } from '@playwright/test';
import { findingsOf, loadBaseline, parseBaseline, splitByBaseline, type Baseline } from '../lib/a11y';
import { kitPaths } from '../lib/env';
import { RUN_TAG_MAX, runTagFor, testIdOf } from '../lib/run-tag';
import { named } from '../lib/selectors';

const examples = path.join(kitPaths.root, 'examples', 'northwind', 'tests', 'acceptance', 'ui');

test.describe('run tags', () => {
  test('a spec file name is its ID', () => {
    expect(testIdOf('/x/tests/acceptance/ui/ui-order-form-01.spec.ts')).toBe('ui-order-form-01');
    expect(testIdOf('ui-order-form-01.test.ts')).toBe('ui-order-form-01');
    for (const bad of ['order-form.spec.ts', 'ui-Order-01.spec.ts', 'ui-order-1.spec.ts', 'ui-order-01.ts', `ui-${'a'.repeat(40)}-01.spec.ts`]) {
      expect(() => testIdOf(bad), bad).toThrow();
    }
  });

  test('the tag is lcp-run:<run ID>/<test ID> and fits the tag column', () => {
    expect(runTagFor('nwt-20261125-3059-lcp_evaluator-1', 'ui-order-form-01')).toBe(
      'lcp-run:nwt-20261125-3059-lcp_evaluator-1/ui-order-form-01',
    );
    expect(() => runTagFor('', 'ui-order-form-01')).toThrow();
    expect(() => runTagFor('a b', 'ui-order-form-01')).toThrow();
    expect(() => runTagFor('x'.repeat(RUN_TAG_MAX), 'ui-order-form-01')).toThrow();
  });
});

test.describe('selectors', () => {
  // A stand-in page that records what was asked for, so no browser is needed.
  const fake = {
    getByRole: (role: string, o: { name: string }) => `role=${role} name=${o.name}`,
    getByLabel: (label: string) => `label=${label}`,
    locator: (css: string) => `css=${css}`,
  } as unknown as Page;

  test('accessible name first, data-control-name second', () => {
    expect(named(fake, { role: 'textbox', name: 'Order Number' })).toBe('role=textbox name=Order Number');
    expect(named(fake, { label: 'Notes' })).toBe('label=Notes');
    expect(named(fake, { controlName: 'SaveButton' })).toBe('css=[data-control-name="SaveButton"]');
  });

  test('a control name cannot smuggle in a CSS selector', () => {
    expect(() => named(fake, { controlName: 'x"] , div[class' })).toThrow();
    expect(() => named(fake, { controlName: '' })).toThrow();
  });
});

test.describe('accessibility baseline', () => {
  const baseline: Baseline = {
    schema_version: 1,
    entries: [
      { surface: 'model-driven', rule: 'region', reason: 'shell', added: '2026-11-25' },
      { surface: 'any', rule: 'color-contrast', target_contains: '#topBar', reason: 'header', added: '2026-11-25' },
      { surface: 'canvas', rule: 'landmark-one-main', reason: 'player', added: '2026-11-25' },
    ],
  };
  const findings = findingsOf([
    { id: 'region', impact: 'moderate', help: 'h', nodes: [{ target: ['#a'] }] },
    { id: 'color-contrast', impact: 'serious', help: 'h', nodes: [{ target: ['#topBar > span'] }, { target: ['#form label'] }] },
  ]);

  test('known platform faults are set aside, others are not', () => {
    const { known, unknown, unused } = splitByBaseline(findings, baseline, 'model-driven');
    expect(known.map((f) => f.target)).toEqual(['#a', '#topBar > span']);
    expect(unknown.map((f) => f.target)).toEqual(['#form label']);
    expect(unused).toEqual([]); // the canvas entry does not count against a model-driven pass
  });

  test('an entry for another surface does not apply', () => {
    const { unknown } = splitByBaseline(findings, baseline, 'canvas');
    expect(unknown.map((f) => f.rule)).toEqual(['region', 'color-contrast']);
  });

  test('the shipped baseline is valid, and a bad one is refused', () => {
    expect(loadBaseline().schema_version).toBe(1);
    expect(() => parseBaseline('{"schema_version":1,"entries":[{"surface":"web","rule":"x","reason":"r","added":"2026-11-25"}]}')).toThrow();
    expect(() => parseBaseline('{"entries":[]}')).toThrow();
  });
});

test.describe('the example specs follow the conventions', () => {
  const files = fs.readdirSync(examples).filter((f) => f.endsWith('.spec.ts'));

  test('there are examples, each named by its ID', () => {
    expect(files.length).toBeGreaterThan(0);
    for (const f of files) expect(() => testIdOf(f)).not.toThrow();
  });

  test('every test is tagged with the criteria it covers, and no spec uses a CSS selector', () => {
    for (const f of files) {
      const source = fs.readFileSync(path.join(examples, f), 'utf8');
      const tests = source.match(/\btest\(\s*'[^']*'/g) ?? [];
      const tagged = source.match(/\btest\(\s*'[^']*',\s*\{\s*tag:\s*\[\s*'@AC-\d+'/g) ?? [];
      expect(tests.length, f).toBeGreaterThan(0);
      expect(tagged.length, `${f}: every test needs { tag: ['@AC-<n>'] }`).toBe(tests.length);
      expect(source, `${f}: select by accessible name, not CSS`).not.toMatch(/\.locator\(|\$\(|querySelector/);
    }
  });
});
