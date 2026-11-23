# [PROJECT_NAME] Constitution
<!-- GET AI constitution template (preset getai). The constitution command fills the bracketed placeholders. Keep principles I to VII; a project may add its own after them, never weaken them. -->

## Core Principles

### I. People own intent and merges

People own the intent, approve the spec and make every merge to `main`. No agent merges to `main`. The worker never decides its own work is done: the gate and a separate evaluator decide.

### II. Locked acceptance tests

Acceptance scenarios are written by someone other than the worker and locked before the build starts. The worker never edits them. Every acceptance criterion (`AC-<n>`) maps to at least one locked scenario. A held-out set the worker cannot read checks the work as well.

### III. Tests and docs for every change

Every change carries its tests and the docs it affects, in the same pull request: `glossary.md` for new terms, a decision record in `docs/adr/` for a decision that is hard to reverse, surprising and a real trade-off, and the verify profile for new journeys.

### IV. Evidence, not claims

Every claim that something works rests on evidence a reviewer can open: a test result, a trace, a screenshot or an export, tagged with its run ID. "It should work" is not evidence.

### V. Facts are looked up; decisions are asked

Agents find facts themselves: the repo, the platform's metadata, the backlog, `glossary.md` and `docs/adr/`. They ask the owner only for decisions, and only by day. A night agent that meets a decision stops and parks the story.

### VI. Design first; code over click-ops

A user-facing change needs an approved mock or throwaway prototype first, and a prototype is never promoted. Changes are made by code and tools that leave a record, never by hand in a portal. A step that needs the portal or interactive consent parks.

### VII. Australian English, plain words

Every artefact uses Australian English and plain, short sentences. One word per concept, the one in `glossary.md`.

## Constraints

- Client code and data follow the client's residency tier: [RESIDENCY_TIER]. No client production data in factory lanes, specs, tests or examples.
- No secret in any spec, test, prompt or file. Credentials stay in their store.
- Machine-read names stay product-neutral.
- [PROJECT_CONSTRAINTS]

## Development Workflow

- Specify, then clarify under the grilling rules, then the checklists (a reviewer ticks them), then the locked scenarios, then approval.
- The spec check runs before implement and in CI on every spec pull request. A failed check stops the work.
- The work size sets the ceremony. It is the largest answer across reversibility, blast radius, clarity, verifiability, effort and residency. The gate can raise it, never lower it.
- Prompts, skills, `glossary.md`, decision records, coding standards and this constitution change only by a reviewed daytime pull request.

## Governance

This constitution comes from the GET AI preset. It overrides other practice in this repo where they conflict. Amendments are made by a reviewed daytime pull request that says what changed and why; the version follows MAJOR.MINOR.PATCH (MAJOR when a principle is removed or redefined).

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
