/**
 * What a locked UI spec imports: `import { test, expect, named } from 'lcp-kit';`
 * The path is mapped in tsconfig.json, which the config applies to every spec.
 */
export { test, expect } from './fixtures';
export { named, describeTarget, type Named, type Scope } from './selectors';
export { runTag, runTagFor, testIdOf, TaggedRows, RUN_TAG_PREFIX } from './run-tag';
export { checkAccessibility, CANVAS_HOST_FRAME, type Surface } from './a11y';
export { keyboardJourney, type KeyStep, type KeyAction } from './keyboard';
