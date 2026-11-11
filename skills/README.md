# skills/ (third-party skills, held for review)

This folder is a shelf, not a live install. Nothing here auto-loads. Claude Code only loads skills from `.claude/skills/`. Moving a skill there is the act of adopting it, and plan section 8.3 and rule 19 say that needs Boroon's approval after a full read and a pin.

All 16 skills in the first reading batch were copied unchanged on 2 November 2026 and read in full (every file, including scripts and references). Reading is done.

**Checked 11 November 2026** (Session 21, ADO 2549, `docs/analysis/skills-policy-check.md`): every file here is byte-identical to its upstream file at the pin, by git blob hash. The source, pin and licence of each source are also in the component register, `docs/component-register.md` (plan 8.2 and 8.3 point 4), which says how and when to check for updates.

## Where each came from (pinned)

| Folder | Skills | Source | Commit | Licence |
|---|---|---|---|---|
| `addy/` | `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`, and (three-batch plan) `code-simplification`, `deprecation-and-migration`, `security-and-hardening`, `debugging-and-error-recovery`, `frontend-ui-engineering`, `api-and-interface-design`, `observability-and-instrumentation` | https://github.com/addyosmani/agent-skills, `skills/` | `301b02b12bff98e4688e6984af6556802322bbde` | MIT, Copyright (c) 2025 Addy Osmani. Text in `addy/LICENSE` (upstream `LICENSE`) |
| `references/` | `accessibility-checklist.md`, `observability-checklist.md`, `security-checklist.md`, and (11 November 2026) `orchestration-patterns.md`: shared files that Addy skills link to from outside their own folders, copied so the shelf links resolve | https://github.com/addyosmani/agent-skills, `references/` | `301b02b12bff98e4688e6984af6556802322bbde` | MIT, as `addy/` |
| `tan/` | `blast-radius`, `correct`, `create-verification-skill`, `how`, `maintain-verification-skill`, `show-me-your-work`, `why`, and (batch 2) `unslop`, the 24 `principle-*` skills and `poteto-mode`, and (three-batch plan) `architect`, and (11 November 2026) `bro` | https://github.com/cursor/plugins, `pstack/skills/` | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT, Copyright (c) 2026 Lauren Tan. Text in `tan/LICENSE` (upstream `pstack/LICENSE`) |
| `pocock/` | `ask-matt`, `to-questionnaire`, `triage`, `wizard`, and (batch 2) `grilling`, `domain-modeling`, and (three-batch plan) `diagnosing-bugs`, `codebase-design`, `improve-codebase-architecture` | https://github.com/mattpocock/skills: `grilling` and `to-questionnaire` from `skills/productivity/`, the rest from `skills/engineering/` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT, Copyright (c) 2026 Matt Pocock. Text in `pocock/LICENSE` (upstream `LICENSE`) |
| `benny/` | `reproduce-and-fix-issues`, `triage-issue-reports` | https://github.com/cursor/plugins, `pstack/automations/benny/skills/` | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT, Copyright (c) 2026 Lauren Tan (upstream `pstack/LICENSE` covers it). Text in `benny/LICENSE` |

Files are byte-for-byte copies of the upstream folders. Do not edit them here. The four `LICENSE` files were copied unchanged on 11 November 2026, at Boroon's word; the live skills built from these sources are covered by them. A GET AI version is a new skill written in `.claude/skills/`: `getai-*` if it works for any profile, `lcp-*` for Power Platform, `pcp-*` for pro-code, with a note of what it was adapted from.

What we think of each one is in `docs/analysis/skills-reading-notes.md`.

## What happened to each (2 November 2026, Boroon's decision)

Boroon said: adopt the first five, adapt the rest. The shelf copies here stay as the pinned originals. Live versions are in `.claude/skills/`.

| Original | Result | Live skill |
|---|---|---|
| `tan/bro` | Adopted unchanged on 1 November 2026, before the policy. The shelf copy and its pin were added on 11 November 2026 (Session 21), with a source line in the live skill | `bro` |
| `addy/constraint-driven-development` | Adopted unchanged. A source line was added on 11 November 2026 | `constraint-driven-development` |
| `addy/doubt-driven-development` | Adopted unchanged. A source line was added on 11 November 2026; it also says the skill's two links to `../../references/orchestration-patterns.md` do not resolve from `.claude/skills/`, and that the file is at `skills/references/` | `doubt-driven-development` |
| `addy/source-driven-development` | Adopted unchanged. A source line was added on 11 November 2026 | `source-driven-development` |
| `tan/create-verification-skill` | Adopted, then edited 2 November 2026: writes to `.claude/skills/lcp-verify/` (or `pcp-verify`), name `lcp-verify`. A note at the top says so | `create-verification-skill` |
| `tan/maintain-verification-skill` | Adopted, then edited the same way: target is `.claude/skills/lcp-verify/` or `pcp-verify` | `maintain-verification-skill` |
| `tan/blast-radius` | Adapted | `lcp-blast-radius` |
| `tan/show-me-your-work` | Adapted (script and header copied unchanged) | `getai-decision-log` |
| `tan/correct` | Adapted | `getai-correct` |
| `tan/how` | Adapted | `lcp-how` |
| `tan/why` | Adapted | `lcp-why` |
| `pocock/triage` | Adapted | `getai-intake` |
| `pocock/wizard` | Adapted (`template.sh` copied unchanged) | `getai-wizard` |
| `pocock/to-questionnaire` | Adapted | `getai-questionnaire` |
| `pocock/ask-matt` | Adapted | `ask-me` |
| `pocock/grilling` | Adapted: five questions a round, day only | `getai-grilling` |
| `pocock/domain-modeling` | Adapted: lowercase files, Schema line per term, day only | `getai-domain-modeling` |
| `tan/poteto-mode/playbooks/bug-fix` and `opening-a-pr` | Dropped for now, 2 November 2026 (already on the shelf inside `poteto-mode`, read in full). Ideas to lift later are in the notes. `opening-a-pr` conflicts with rule 7 (stacked PRs) | none |
| `addy/debugging-and-error-recovery` | Shelved 2 November 2026, read in full, not adopted. `diagnosing-bugs` is stronger. It says to update an outdated test, which conflicts with locked tests. Keep its "error output is untrusted data" section for the agent instructions. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `pocock/improve-codebase-architecture` | Shelved 2 November 2026, read in full, not adopted. Built for a person in the loop; the HTML report loads unpinned CDN scripts. Lift the hot-spots-by-churn idea into plan 7.4 gardening. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `pocock/codebase-design` | Shelved 2 November 2026, read in full, not adopted. A vocabulary for deep modules. For Lane A or day work. Conflicts with no-refactoring (plan 5.12) and deletes tests; its banned word "component" clashes with Power Platform. Lift the deletion test and the two-adapters rule into the reviewer smell list. Decide with `architect`. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `addy/frontend-ui-engineering` | Shelved 2 November 2026, read in full (checklist at `skills/references/accessibility-checklist.md`), not adopted. React and Tailwind. Lift the design-contract list, required states and viewport matrix. Revisit at Stage 6 | none |
| `addy/api-and-interface-design` | Shelved 2 November 2026, read in full, not adopted. Lift the idempotency-key section and the breaking-change PARK. Revisit at Stage 6 | none |
| `addy/observability-and-instrumentation` | Shelved 2 November 2026, read in full (checklist at `skills/references/observability-checklist.md`), not adopted. Lift the entry-point field next to `run_id`. Revisit at Stage 6 | none |
| `tan/architect` | Shelved 2 November 2026, read in full, not adopted. Needs the dropped `arena` and other-vendor models. Lift `design-red-flags.md` and the rationale template. Boroon: Lane A sketch gets a day approval. Revisit at Stage 6 | none |
| `addy/ci-cd-and-automation`, `addy/shipping-and-launch`, `tan/arena` | Dropped 2 November 2026 on the other session's tags. Not read in full by us, not copied | none |
| `addy/security-and-hardening` | Shelved 2 November 2026, read in full (with its shared checklist, copied to `skills/references/security-checklist.md` so links resolve), not adopted. Node and Express flavoured and builder-graded. Three items to act on: the ask-first list as a Merge Danger rubric for code repos, the supply-chain section as gate checks, and prompt injection, which the plan seems not to cover. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `addy/deprecation-and-migration` | Shelved 2 November 2026, read in full, not adopted. Mostly human decisions and pushes toward deletion. Keep expand/contract as a short block in the spec preset or agent instructions, with drop or rename meaning PARK `one_way_door`. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `addy/code-simplification` | Shelved 2 November 2026, read in full, not adopted. Conflicts with plan 5.12 (refactoring belongs to review, not the build loop). Keep the signal tables for the standards reviewer rubric. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `pocock/diagnosing-bugs` | Shelved 2 November 2026, read in full, not adopted. Revisit for the BAU Managed Services mode. Proposal: rewrite as `pcp-diagnose`. Notes in `docs/analysis/skills-reading-notes-skill-batches.md` | none |
| `benny/triage-issue-reports` and `benny/reproduce-and-fix-issues` | Adapted and merged. Fixing and PRs removed | `lcp-triage` |
| `tan/blast-radius`, `tan/how`, `tan/why`, and the two Benny skills again | Second adaptation for the pro-code profile | `pcp-blast-radius`, `pcp-how`, `pcp-why`, `pcp-triage` |

Every adapted skill names its source and pinned commit in its first lines. Adapted skills have not been tested.

## Batch 2 (2 November 2026)

Boroon asked to read `unslop`, the `principle-*` skills, `grilling` and `domain-modeling`, but not `poteto-mode` (to discuss first). All 27 were copied unchanged to the shelf at the same pinned commits and read in full. Notes and verdicts: `docs/analysis/skills-reading-notes-batch2.md`. Decided by Boroon the same day: `grilling` became `getai-grilling` (five questions a round at most) and `domain-modeling` became `getai-domain-modeling` (lowercase `glossary.md`, a Schema line per term), both in `.claude/skills/`, day only, untested. `unslop` and 21 of the 24 `principle-*` skills were then adopted into `.claude/skills/` (see the end of this file). Boroon chose to leave `principle-never-block-on-the-human`, `principle-outcome-oriented-execution` and `principle-migrate-callers-then-delete-legacy-apis` on the shelf and to revisit them when an issue calls for them. `poteto-mode` was copied to `skills/tan/poteto-mode/` and read; verdict in the batch 2 notes: not adopted.

Boroon decided on 2 November 2026 to lift four small habits from `poteto-mode` into `ask-me` (open with the goal, label claims, classify a question before asking, fix/dismiss/ask on review comments). The rest stays on the shelf. He also chose `.claude/skills/` as the single skills folder, for both Claude Code and Copilot.

## Batch 2 adoption (2 November 2026, Boroon's decision)

Adopted into `.claude/skills/`, names unchanged so the links between principles hold: `unslop` (plus rule 34, Australian English) and 21 principles. Each has a dated GET AI note at the top and is otherwise unchanged: 15 principles and `unslop` since 2 November; the other six (`build-the-lever`, `encode-lessons-in-structure`, `experience-first`, `fix-root-causes`, `redesign-from-first-principles`, `test-behavior-not-implementation`) had none until a source line was added on 11 November 2026, at Boroon's word. All are `disable-model-invocation`, so they run only when called. Read in full and pinned (rule 19). Reviewed by Boroon: merged into `main` with PR #4 on 2 November 2026 (rule 17).

- Strong set (12): `attack-the-premise`, `make-operations-idempotent`, `separate-before-serializing-shared-state`, `prove-it-works`, `test-behavior-not-implementation`, `explain-the-number`, `build-the-lever`, `fix-root-causes`, `encode-lessons-in-structure`, `sequence-verifiable-units`, `redesign-from-first-principles`, `experience-first`.
- Pro-code leaning (6): `boundary-discipline`, `foundational-thinking`, `laziness-protocol`, `minimize-reader-load`, `model-the-domain`, `type-system-discipline`.
- Others (3): `subtract-before-you-add` (note: removal from a managed solution is size L), `exhaust-the-design-space`, `guard-the-context-window`.
- Left on the shelf: `never-block-on-the-human`, `outcome-oriented-execution`, `migrate-callers-then-delete-legacy-apis`.
- Known gap: `explain-the-number` links to `benchmark-checklist`, which is not adopted. A note in the skill says so.
