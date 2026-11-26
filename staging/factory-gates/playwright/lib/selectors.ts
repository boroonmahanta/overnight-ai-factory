/**
 * The selector rule (plan 5.8): accessible name first, data-control-name second,
 * never CSS paths or positions. The names come from the spec's Testability contract,
 * so a renamed control breaks the test, as it should.
 *
 * There is deliberately no way to pass a CSS selector here.
 */
import type { FrameLocator, Locator, Page } from '@playwright/test';

export type Scope = Page | FrameLocator | Locator;
export type Role = Parameters<Page['getByRole']>[0];

export type Named =
  /** First choice: a role and its accessible name, such as { role: 'textbox', name: 'Order Number' }. */
  | { role: Role; name: string | RegExp; exact?: boolean }
  /** Also accessible name: the control's label. */
  | { label: string | RegExp; exact?: boolean }
  /** Second choice, for a canvas control with no accessible name: its name in Power Apps Studio. */
  | { controlName: string };

/** A control name we can put inside a CSS attribute value safely. */
const CONTROL_NAME = /^[^"\\\r\n]{1,128}$/;

export function named(scope: Scope, target: Named): Locator {
  if ('role' in target) {
    return scope.getByRole(target.role, { name: target.name, exact: target.exact });
  }
  if ('label' in target) {
    return scope.getByLabel(target.label, { exact: target.exact });
  }
  if (!CONTROL_NAME.test(target.controlName)) {
    throw new Error(`Not a usable control name: ${JSON.stringify(target.controlName)}`);
  }
  return scope.locator(`[data-control-name="${target.controlName}"]`);
}

/** For messages: how a target was asked for. */
export function describeTarget(target: Named): string {
  if ('role' in target) return `${target.role} "${String(target.name)}"`;
  if ('label' in target) return `label "${String(target.label)}"`;
  return `control "${target.controlName}"`;
}
