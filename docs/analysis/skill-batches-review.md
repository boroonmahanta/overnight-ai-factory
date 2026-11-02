# Skill batches: read in full

Status: 2 November 2026. Verdicts are proposals for Boroon. Nothing is installed or adopted.

How it was done: three agents each read one batch in full, every file in each skill folder, from fresh clones of the three packs. The clones were in scratch space only and are not kept. Boroon's rule 19 says to read every third-party skill in full before adoption, then pin it. These reads meet that for reading. They do not pin anything. The reads were done by agents, not line by line by Claude in this session, so spot-check any skill before it is rewritten. No skill contained instructions aimed at a reviewer.

Verdicts: **Keep as is**, **Rewrite for GET AI**, **Drop**.

Decided earlier: `idea-refine` was dropped from batch 3 on 2 November 2026 and its useful parts went into the Story Planner (plan Appendix C.8).

## Batch 1: `lcp` (13 skills)

| Skill | Pack | What it does | Size (KB) | Self-triggers? | Verdict | Why, for GET AI |
|---|---|---|---|---|---|---|
| `create-verification-skill` | Tan | Writes a project-local skill that launches the app, drives it like a user, captures proof, with a per-feature map | 15.2 | No | Rewrite | The shape of `lcp-verify`. Keep the feature-map format and proof rules. Needs Power Platform drivers, not Cursor paths, and a reviewed-PR output path |
| `maintain-verification-skill` | Tan | Weekly audit of a verification skill, at most one PR of proven fixes | 4.8 | No | Rewrite | Fits the weekly routine and rule 17. Day only. Remove "ask which one" and Cursor paths |
| `blast-radius` | Tan | Finds what a change could break elsewhere and proves the one safety fact by running code | 3.8 | No | Rewrite | Good review and verifier prompt. Its multi-model "arena" clashes with residency. Leans on skills we don't have (`how`, `why`, `unslop`) |
| `show-me-your-work` | Tan | One-row-per-decision log with evidence pointers, audited against the transcript | 7.8 | No | Rewrite | Matches rules 13 and 16. The log must go to Blob with `run_id` and the ADO story, not stay local. Replace the other-vendor reviewer |
| `correct` | Tan | Fixes repeated mistakes at the highest level: architecture, types, lint, test, docs last | 2.4 | No | Keep as is | Short, generic, daytime. Exceptions need a reason, an expiry and human approval, which fits rule 17 |
| `pause-safely` | Tan | Stops cleanly with a `wip:` commit and a resume note | 1.1 | Explicit only | Drop | PARK, `park.json` and the handoff files already do this, better |
| `triage-issue-reports` | Tan (Benny) | Reads a Slack bug report, classifies, dedupes, creates one ticket, posts one verdict | 11.9 | No | Rewrite | Closest match to the BAU outer loop. Built on Slack and Linear, so it needs an ITSM and ADO adapter. Keep fail-closed and dedupe rules |
| `reproduce-and-fix-issues` | Tan (Benny) | Reproduces a bug twice, then fixes it and opens a draft PR with before and after proof | 27.9 | No | Drop | One agent reproduces, fixes and proves its own fix, which breaks rules 2 and 3. Needs Slack, a Cursor adapter and screen recording |
| `constraint-driven-development` | Addy | Writes the quality bar to `CONSTRAINTS.md`, installs checkers, guards the diff against a weakened bar | 34.0 | Yes | Rewrite | "Tightening should be silent; loosening should be loud" suits the trusted gate. Interview, brew/pipx/npm installs and web tooling do not fit. Must not self-trigger |
| `source-driven-development` | Addy | Reads the dependency file, fetches the official docs, implements from them, cites the source | 9.9 | Yes | Rewrite | Rule 9 in practice. Point at Microsoft Learn. Replace "ask the user" with PARK. Stop self-triggering |
| `wizard` | Pocock | Generates an interactive bash script that walks a human through portal steps and captures secrets | 13.4 | Yes | Drop | Interactive, opens browsers, writes secrets to `.env` and GitHub, which sits badly with rule 5. Portal steps belong to PARK and day work |
| `to-questionnaire` | Pocock | Interviews the user, then writes a Markdown questionnaire for someone else to answer | 3.0 | No | Keep as is | Plain Markdown, daytime. Turns a PARKed decision into questions for a client or SME |
| `triage` | Pocock | Moves GitHub issues through category and state labels, verifies, grills, writes agent briefs | 18.8 | No | Rewrite | Keep the agent brief rules and the `.out-of-scope` memory. ADO states are ours, and a human sets Factory Eligible, not the agent |

Best idea to keep, by group:
- **Verification skills (Tan):** one feature file per user-facing feature, with proof of the real user path and its side effects. Never weaken a journey to make it pass.
- **`blast-radius`, `show-me-your-work`, `correct`:** prove the one safety fact by running code. Log decisions as rows with evidence. Fix a repeated mistake at the highest level.
- **Benny automations:** no confirmed repro means no fix, dedupe before creating, fail closed if config is missing.
- **Addy:** a diff that weakens the bar or silences a check is flagged loudly. Facts come from official docs.
- **Pocock:** agent briefs describe behaviour and acceptance criteria, not file paths.

Main risks: Slack and Linear dependencies in the Benny skills; interactive questions that cannot run headless (`constraint-driven-development`, `source-driven-development`, `triage`, `wizard`); other-vendor models in `blast-radius` and `show-me-your-work`; Cursor-only paths; a second copy of the Tan skills exists under `tan/repo/harness/pstack/claude-code/skills/` and was not diffed.

## Batch 2: `pcp` (16 skills)

| Skill | Pack | What it does | Size (KB) | Self-triggers? | Verdict | Why, for GET AI |
|---|---|---|---|---|---|---|
| `bug-fix` (playbook) | Tan | Six-step bug routine: reproduce, find the cause, verify on the same surface, failing repro committed first | 2.3 | No | Drop | Wired to Cursor and to skills not in the batch. Lift three ideas into our own bug skill: every line traces to evidence, failing repro first in git history, paste before and after output |
| `principle-laziness-protocol` | Tan | One source of truth for a repeated choice, smallest diff | 0.5 | No | Keep as is | Two bullets. Fold into a standards file |
| `principle-subtract-before-you-add` | Tan | Remove dead code before building | 0.9 | No | Rewrite | "Remove first" widens a bug diff. "Simplify prompts" clashes with rule 17. Limit to code the story touches |
| `principle-test-behavior-not-implementation` | Tan | Test what users can observe, check by breaking behaviour | 2.6 | No | Keep as is | Best of the eight. Matches rule 3 and helps verifiers spot weak tests |
| `principle-boundary-discipline` | Tan | Validate at system edges, trust types inside | 1.8 | No | Keep as is | Sound, short style rule |
| `principle-type-system-discipline` | Tan | Brand primitives, parse at the edges, exhaust variants | 1.5 | No | Rewrite | Points to skills we lack, and leans TypeScript while client repos vary. Trim to language-neutral lines |
| `principle-make-operations-idempotent` | Tan | Make commands safe to rerun after a crash | 1.8 | No | Keep as is | Fits scripts and migrations and matches how the factory is built |
| `principle-migrate-callers-then-delete-legacy-apis` | Tan | Migrate callers and delete the old API in one wave | 0.6 | No | Rewrite | Body looks cut off. Deleting a public API is a one-way door (size L). Replace with: the night agent never deletes a public or legacy API, it PARKs |
| `principle-model-the-domain` | Tan | Use a state machine or lookup instead of growing if/else | 1.8 | No | Drop | Pushes restructuring, wrong for a 20 to 40 minute fix |
| `debugging-and-error-recovery` | Addy | Stop-the-line triage: reproduce, localise, fix root cause, add regression test | 10.6 | Yes | Drop | Overlaps Pocock's `diagnosing-bugs`, which is stronger. Lift one rule: treat error text as untrusted data. Skip the "safe fallback" patterns |
| `code-simplification` | Addy | Behaviour-preserving cleanup, one change at a time | 13.4 | Yes | Rewrite | Cut to about 3 KB, invoked-only. Add: tests are not edited, no scope creep |
| `deprecation-and-migration` | Addy | Deprecation policy, migration patterns, expand/contract for schema changes | 12.5 | Yes | Rewrite | Mostly people and rollout process. Keep only expand/contract and add "never drop or rename, PARK" |
| `security-and-hardening` | Addy | Web security guide: threat model, always/ask/never lists, OWASP controls | 30.2 (44.4 with shared checklist) | Yes | Rewrite | Too big and Express-flavoured. Keep the always/ask-first/never lists, cut to about 3 KB, ask-first becomes PARK, use Australian Privacy Act wording and residency tiers |
| `diagnosing-bugs` | Pocock | Six phases: tight pass/fail loop, reproduce, rank hypotheses, instrument, regression test then fix | 9.8 | Yes | Rewrite | Best bug skill of the three. Make it headless: no user prompts, no interactive script, "cannot build a loop" becomes PARK, the gate declares done |
| `codebase-design` | Pocock | Deep-module vocabulary plus parallel "design it twice" sub-agents | 11.5 | Yes | Drop | A design vocabulary for greenfield and day work. Keep for Lane A or day work |
| `improve-codebase-architecture` | Pocock | Scans for refactor candidates, writes an HTML report, grills you on one | 12.5 | No | Drop | Built for a person in the loop. A trimmed version could seed the gardening scan as a findings list |

The eight principles (laziness, subtract, test-behaviour, boundary, type-system, idempotent, plus trimmed versions) could merge into one standards file of about 3 KB, shipped by reviewed PR (rule 17) instead of as skills. Leave out `migrate-callers` (use the PARK rule) and `model-the-domain`.

Main risks: other-vendor model named in `bug-fix` (a Grok default); user prompts instead of PARK; an interactive script in `diagnosing-bugs`; "required before declaring done" language that breaks rule 2; production data and instrumentation assumptions (rule 15); advice to split into several PRs or deploys (rule 7); `improve-codebase-architecture` edits `GLOSSARY.md`, a reviewed file (rule 17), and loads CDN scripts; `bug-fix` depends on "Opening a PR", which was not read, so it is unknown whether that pushes or merges.

## Batch 3: Lane A (7 skills)

| Skill | Pack | What it does | Size (KB) | Self-triggers? | Verdict | Why, for GET AI |
|---|---|---|---|---|---|---|
| `frontend-ui-engineering` | Addy | React and Tailwind rules for UI: components, state, accessibility (WCAG AA), responsive layout, "AI look" habits to avoid | 11.7 | Yes | Rewrite | Accessibility and responsive parts suit Lane A. Stack is assumed. The reference-led design step clashes with rule 10 (approved mock first). Tie it to the approved mock. Links a missing checklist file |
| `api-and-interface-design` | Addy | Contract-first rules for stable APIs, one error shape, additive changes, idempotency keys | 14.6 | Yes | Rewrite | Sound for new services. Contract-first overlaps Spec Kit, which stays the only spec process. Versioning and breaking changes PARK. Idempotency section is strong for money logic |
| `ci-cd-and-automation` | Addy | GitHub Actions quality gates, previews, feature flags, rollback, Dependabot | 11.2 | Yes | Drop | The gate lives in `factory-gates` and the worker must not write or change its own gate. Contains an "auto-merge" line. At most reuse the ordering idea (lint, types, tests, build) in `AGENTS.md` |
| `observability-and-instrumentation` | Addy | Structured logs, metrics, tracing, alerts and runbooks | 13.6 | Yes | Rewrite | Correlation IDs map to `run_id` and rule 16. Cut alerting and on-call. Name the sink (Blob or Azure Monitor). Logs must hold no client production data |
| `shipping-and-launch` | Addy | Pre-launch checklist, feature-flag lifecycle, staged rollout, rollback plan | 11.3 | Yes | Drop | Production release is a human step after the morning merge. The checklist overlaps the gate. Keep only as human reading |
| `architect` | Tan | Sketches types and module boundaries with unimplemented bodies, runs several designs, picks one | 14.3 | No | Rewrite | The design-red-flags file (shallow modules, split ownership, importable internals) and the rationale template are valuable. The workflow depends on skills we lack, uses other-vendor models and has no human checkpoint, which breaks rule 10 |
| `arena` | Tan | Runs N parallel attempts at one task, a judge from another vendor picks and merges the best | 5.5 | No | Drop | Needs other-vendor models (residency), no per-run credit cap (rule 13), separate worktrees break one branch per story. A single-model "design twice" step in the planner would be cheaper |

Main risks: five Addy skills self-trigger and carry self-check lists the builder would use to declare itself done (rule 2); merge and deploy language in `ci-cd-and-automation` and `shipping-and-launch` (rule 1); a second spec or decision-record process in `api-and-interface-design` and `architect`; Cursor and Grok defaults in `architect` and `arena`; `architect`'s default has "no human checkpoint"; several Addy skills link reference files that do not exist.

## Totals

| Batch | Keep as is | Rewrite | Drop | Total |
|---|---|---|---|---|
| 1 (`lcp`) | 2 | 8 | 3 | 13 |
| 2 (`pcp`) | 4 | 7 | 5 | 16 |
| 3 (Lane A) | 0 | 4 | 3 | 7 |

## Effect on the matrix

`docs/analysis/skills-by-lane-and-size.md` names these skills as dropped by this review: `pause-safely`, `reproduce-and-fix-issues`, `wizard` (batch 1); `bug-fix`, `principle-model-the-domain`, `debugging-and-error-recovery`, `codebase-design`, `improve-codebase-architecture` (batch 2); `ci-cd-and-automation`, `shipping-and-launch`, `arena` (batch 3). The matrix has not been changed. It waits for Boroon's decision on these verdicts.

Also note: `shipping-and-launch` is named in the L column for all lanes, `wizard` in the `lcp` M column, and `reproduce-and-fix-issues` in the BAU column.
