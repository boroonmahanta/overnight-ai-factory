/**
 * Paths and settings the kit reads, in one place.
 *
 * Variable names are Microsoft's where Microsoft's code reads them (MS_AUTH_*,
 * MODEL_DRIVEN_APP_URL, CANVAS_APP_URL), and product-neutral where they are ours
 * (TEST_SPECS_DIR, RUN_ID, TEST_ENV_URL, LCP_*). The README lists them all.
 */
import * as path from 'node:path';

export const kitRoot = path.resolve(__dirname, '..');

export const isCI = !!process.env.CI;

/** Where the specs are. The gate sets this to the PR's tests/acceptance/ui. */
export const specsDir = path.resolve(
  process.env.TEST_SPECS_DIR ?? path.join(kitRoot, 'examples', 'northwind', 'tests', 'acceptance', 'ui'),
);

export const kitPaths = {
  root: kitRoot,
  lib: path.join(kitRoot, 'lib'),
  kitTests: path.join(kitRoot, 'kit-tests'),
  /** Signed-in browser state. Never upload this folder: it holds live session cookies. */
  authDir: path.join(kitRoot, '.auth'),
  /** The verifier step in lcp-gate.yml reads this path. */
  mdaState: path.join(kitRoot, '.auth', 'mda.json'),
  canvasState: path.join(kitRoot, '.auth', 'canvas.json'),
  /** Reports, JUnit and traces. The gate points this under its evidence folder. */
  evidenceDir: path.resolve(process.env.LCP_EVIDENCE_DIR ?? path.join(kitRoot, 'test-results')),
  /** Known platform accessibility faults. Lives in the gate repo, so a project cannot add to it. */
  baseline: path.join(kitRoot, 'a11y-baseline.json'),
};

/** A run ID for local runs, when the gate's RUN_ID is not set. */
export function localRunId(now = new Date()): string {
  const stamp = now.toISOString().replace(/[-:T]/g, '').slice(0, 14);
  return `local-${stamp}`;
}
