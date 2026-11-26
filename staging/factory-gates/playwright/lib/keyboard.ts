/**
 * The keyboard-only journey (plan 5.9, layer three): reach each named control with
 * Tab alone, then act on it with keys alone. No mouse. Our design, not Microsoft
 * guidance [inference].
 *
 * The order of everything focused on the way is attached to the test as evidence.
 */
import type { Locator, Page, TestInfo } from '@playwright/test';
import { describeTarget, named, type Named, type Scope } from './selectors';

export type KeyAction =
  /** Press one key or chord, such as 'Enter', 'Space' or 'Control+S'. */
  | { press: string }
  /** Type text into the focused control. */
  | { type: string };

export interface KeyStep {
  /** The control to reach, by accessible name (or canvas control name). */
  reach: Named;
  /** What to do once it has focus. */
  then?: KeyAction[];
  /** Give up after this many presses of Tab. Default 80. */
  maxTabs?: number;
}

async function hasFocus(target: Locator): Promise<boolean> {
  return target
    .evaluate((el) => {
      const active = el.ownerDocument.activeElement;
      return !!active && (el === active || el.contains(active));
    })
    .catch(() => false);
}

/** A short description of what has focus, looking into same-origin frames. */
async function focused(page: Page): Promise<string> {
  return page
    .evaluate(() => {
      let doc: Document = document;
      let el: Element | null = doc.activeElement;
      while (el && el.tagName === 'IFRAME') {
        try {
          const inner = (el as HTMLIFrameElement).contentDocument;
          if (!inner) break;
          doc = inner;
          el = doc.activeElement;
        } catch {
          break;
        }
      }
      if (!el) return '(nothing)';
      const role = el.getAttribute('role') ?? el.tagName.toLowerCase();
      const name = el.getAttribute('aria-label') ?? el.getAttribute('title') ?? (el.textContent ?? '').trim().slice(0, 60);
      return `${role} "${name}"`;
    })
    .catch(() => '(unknown)');
}

export async function keyboardJourney(
  page: Page,
  testInfo: TestInfo,
  steps: KeyStep[],
  scope: Scope = page,
): Promise<void> {
  const order: string[] = [];
  try {
    for (const step of steps) {
      const target = named(scope, step.reach).first();
      await target.waitFor({ state: 'visible' });
      const max = step.maxTabs ?? 80;
      let reached = await hasFocus(target);
      for (let i = 0; !reached && i < max; i++) {
        await page.keyboard.press('Tab');
        order.push(await focused(page));
        reached = await hasFocus(target);
      }
      if (!reached) {
        throw new Error(`Keyboard journey: ${describeTarget(step.reach)} was not reached in ${max} presses of Tab`);
      }
      order.push(`  reached ${describeTarget(step.reach)}`);
      for (const action of step.then ?? []) {
        if ('press' in action) await page.keyboard.press(action.press);
        else await page.keyboard.type(action.type);
      }
    }
  } finally {
    await testInfo.attach('keyboard-journey.txt', { body: order.join('\n'), contentType: 'text/plain' });
  }
}
