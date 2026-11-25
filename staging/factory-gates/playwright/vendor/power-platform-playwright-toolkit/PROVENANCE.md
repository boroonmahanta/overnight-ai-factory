# Provenance

This folder is Microsoft's Power Platform Playwright toolkit, vendored unchanged.

- Source: https://github.com/microsoft/power-platform-playwright-samples, folder `packages/power-platform-playwright-toolkit/`
- Pin: commit `3233f3e73e30960e8ab7349f1cb06b520ca010e4` (28 October 2026)
- Licence: MIT. `LICENSE` and `NOTICE.md` here are the repo root's, copied unchanged.
- Copied: 25 November 2026 (Session 52, ADO 2546), at Boroon's word. All 50 toolkit files plus `LICENSE` and `NOTICE.md` matched GitHub's blob hashes at the pin.
- Read in full before adoption (rule 19): `docs/analysis/playwright-kit-reading-notes.md` in the planning repo.
- Not changed in any way. The kit imports `src/index.ts` through a path in its `tsconfig.json`; this folder's own `package.json`, `tsconfig.json` and `eslint.config.js` are not used.
- To move the pin: read the diff of this folder in full, copy the new commit's files over, check their hashes, and update this file, the component register and the reading notes in one reviewed pull request.

This file is ours, not Microsoft's.
