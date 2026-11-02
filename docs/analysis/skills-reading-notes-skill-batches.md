# Reading notes: the three-batch skills plan

Started 2 November 2026. Proposals only. Nothing here is adopted unless a line says so.

The three-batch plan comes from Boroon's chat "Planning the skills to use":

| Batch | For | Skills | Needed before |
|---|---|---|---|
| 1 | `lcp` (the focus) | 13 | Stages 2 and 3 (day 15) |
| 2 | `pcp` | 16 | Stage 5 (day 46) |
| 3 | Lane A | 8 (7 after `idea-refine` was dropped) | Stage 6 (day 60) |

Another session read all 36 and wrote `docs/analysis/skill-batches-review.md`. That file is on branch `claude/sharp-wright-1muptp` (commit `c3a1c72`), not on `main`. Its reads were done by agents. The notes below are our own full reads of single skills, one at a time, as rule 19 asks. Each section says which files were read.

Pinned sources are in `skills/README.md`.

## `show-me-your-work` (Tan), read 2 November 2026

Files read in full: `SKILL.md`, `scripts/log.sh`, `references/decision-log-template.tsv`. Pinned `cursor/plugins` commit `ae5650f`.

- **Status:** already adapted and live as `getai-decision-log`. The other session's review said "rewrite", but the rewrite had already happened.
- **Safety read:** `log.sh` appends to one local file, makes no network calls, strips tabs and newlines, and puts a quote in front of cells starting `=`, `+`, `-` or `@` so a spreadsheet cannot run them. Nothing aimed at a reviewer.
- **Verdict:** keep `getai-decision-log`. It needs a test, not a rewrite.
- **Gaps:** the transcript audit assumes a transcript sits in the evidence bundle, and the plan does not say so yet. Nothing checks that the log reached Blob (rule 16).

## `pause-safely` (Tan), read 2 November 2026

File read in full: `pstack/skills/poteto-mode/playbooks/pause-safely.md` (12 lines). It is a playbook inside `poteto-mode`, not a skill folder of its own. The shelf copy under `skills/tan/poteto-mode/playbooks/` is identical.

- **What it does:** stop at a safe boundary, take no irreversible action, make one `wip:` commit, write a resume note.
- **Verdict:** drop. PARK, `park.json` and the handoff files (plan 5.11 and 7.1) already do this.
- **One idea kept:** a stop that is not a PARK (timeout, exhausted cap, killed replica) needs a checkpoint. It went into plan 5.11 as "Stops that are not a PARK", owned by the driver, marked `[untested]`.

## `diagnosing-bugs` (Pocock), read 2 November 2026

Files read in full: `SKILL.md` (8.7 KB), `scripts/hitl-loop.template.sh` (1.3 KB), `agents/openai.yaml` (103 bytes). Also read, as background only: Pocock's `docs/engineering/diagnosing-bugs.md`, which is not part of the skill and is not copied. Copied unchanged to `skills/pocock/diagnosing-bugs/`. Pinned `mattpocock/skills` commit `4ae2317`, MIT.

**What it does.** A six-phase gate for one known bug or regression. The agent may not form a theory until it names a fast, deterministic command that it has already run once and that goes red on this bug. Phases: build the loop, reproduce and minimise, rank 3 to 5 falsifiable hypotheses, instrument one variable at a time with tagged logs, write the regression test before the fix (only if a correct seam exists), clean up.

**Safety read.**
- Nothing in any file is aimed at a reviewer.
- `hitl-loop.template.sh` only prints prompts, reads typed answers with `read -r -p` and prints them back. No network, no file writes, no other commands. The doc says Snyk flags the skill for shipping a script, and calls that a false positive. Our read agrees.
- It has a Redact section: write `<REDACTED>` for secrets and build loops against environment variables. This suits rules 5 and 15. The doc says issue #674 asks for this guardrail, so the pinned copy may be ahead of the doc.
- `agents/openai.yaml` is a display name and a one-line description. Harmless, and unused by us.

**What fits GET AI.**
- Phase 1 is rule 2 in practice: check the real artifact, not a proxy. It matches `pcp-triage`, which already refuses to call reading source or running a unit test a repro.
- "No correct seam exists" as a finding maps to the refactor candidates in the PR body (plan Appendix C.7).
- `[DEBUG-xxxx]` tags could become a deterministic gate check: grep the PR diff for the prefix.
- Naming the winning hypothesis in the commit message fits `handoff/<id>/pr.md`.

**What must change before use.**
1. **Interactive steps become PARKs (rules 8 and 9).** "Stop and ask the user" when no loop can be built becomes PARK `ambiguity` or `portal_step`. "Show the hypotheses to the user" becomes a write to `learnings.json`. The human-in-the-loop script is day work only.
2. **It self-triggers.** Its description fires on "debug this" or "broken", and its doc reports four people hitting over-firing (issue #578). It needs `disable-model-invocation`.
3. **The builder would grade itself (rules 2 and 3).** The regression test the builder writes is its own red-green check (`tests/dev/<ado-id>/`, plan 5.12), not acceptance evidence. The skill needs a line saying so. A fix still needs a locked scenario from someone other than the builder.
4. **Capitalised glossary.** It reads `GLOSSARY.md`. Ours is lowercase `glossary.md`.
5. **Drop `agents/openai.yaml`.**
6. **Power Platform needs its own loop.** The ten ways to build a loop are code-flavoured. For `lcp` the loop is `lcp-verify` in the lane. Write the `pcp` version first, since the plan sends bugs to the code profile.

**Overlap.** `pcp-triage` already does Phases 1 and 2 as a bounded repro with no fix. `diagnosing-bugs` would be the deeper step after triage returns `reproduced`. `pcp-why` may overlap too. Not compared line by line.

**Verdict (proposal): rewrite as `pcp-diagnose`, not now.** Boroon, 2 November 2026: shelved, and to be revisited for the BAU Managed Services mode. That is the outer loop, where AI Managed Services client reports arrive through `pcp-triage` and a confirmed repro needs a next step. Questions to settle then:
- May a night agent run all six phases, or only Phases 1 and 2 with the fix left to a human? Rule 3 is why `pcp-triage` has no fix step.
- Does an `lcp` version follow, with `lcp-verify` as the loop?
- Does it run after `pcp-triage` returns `reproduced`, on the same lane, or as its own story?

Not adopted. Not edited. Nothing written to `.claude/skills/`.

## `code-simplification` (Addy), read 2 November 2026

Files read in full: `skills/code-simplification/SKILL.md` (13.7 KB). Also read, as background only and not copied: Addy's eval case JSON and its config-parser test fixture, which are test material for his own evals. Copied unchanged to `skills/addy/code-simplification/`. Pinned `addyosmani/agent-skills` commit `301b02b`, MIT.

**What it does.** Simplifies working code without changing behaviour. Four steps: understand first (Chesterton's Fence, git blame), scan three signal tables (structural, naming, redundancy), change one thing at a time and run the tests after each, then compare before and after and revert if it is harder to follow. Five principles: preserve behaviour, follow project conventions, prefer clarity over cleverness, keep balance, scope to what changed. A "Rule of 500" says to use codemods past 500 lines. Examples in TypeScript, JavaScript, Python and React.

**Safety read.** No scripts, no network calls, nothing aimed at a reviewer. The one external link credits the Claude Code simplifier plugin. Frontmatter is `name` and `description` only, and the description invites self-triggering, even on pasted code.

**Why it is shelved, not rewritten** (the other session's review said "rewrite, cut to about 3 KB, add: tests are not edited").
1. **It conflicts with the plan.** Plan lines 877 and 2259: "No refactoring outside the ticket"; the executor lists candidates under "Refactor candidates" in `pr.md`, because "refactoring belongs to review, not the build loop" (Pocock v1.1). A skill that tells the builder to simplify is the wrong tool for the night loop.
2. **"Tests are not edited" is already in it.** The skill requires tests to pass "without modification" and lists editing tests as a red flag. Tests are also protected paths at Merge Danger 10 (plan line 764), so the gate enforces it.
3. **It is already headless.** Its "ask before every change" questions are self-checks, not questions to a person, so the PARK rewrite the review expects is not needed.
4. **The generic parts are covered.** Chesterton's Fence and git blame overlap `pcp-why`. Subtraction and laziness overlap `principle-subtract-before-you-add` and `principle-laziness-protocol`. Reader load overlaps `principle-minimize-reader-load`.
5. **Stack coverage.** Examples are TypeScript, JavaScript, Python and React. The stacks of the AI Managed Services client repos are not known.

**Worth keeping.**
- **The three signal tables** (nesting of 3 or more levels, functions over 50 lines, boolean flag parameters, "what" comments against "why" comments, and so on). They could seed the standards reviewer's smell list (plan line 2352) when Appendix B and C.9 are next edited.
- **A possible later use as its own story.** A behaviour-preserving refactor is the easiest change to verify: locked tests unchanged and passing is the proof (rule 3 fits). It could be a refactor-only night story fed from the "Refactor candidates" list or the weekly gardening findings. That ties to BAU Managed Services. It would be a `pcp-simplify`, written only if Boroon wants it.

**Verdict (proposal): shelve.** Not adopted, not edited, nothing written to `.claude/skills/`. Revisit when the standards reviewer rubric is edited, or for the BAU Managed Services mode.

## `deprecation-and-migration` (Addy), read 2 November 2026

Files read in full: `skills/deprecation-and-migration/SKILL.md` (12.8 KB). Also read, as background only and not copied: Addy's eval case JSON and an API inventory fixture, which are test material for his own evals. Copied unchanged to `skills/addy/deprecation-and-migration/`. Pinned `addyosmani/agent-skills` commit `301b02b`, MIT.

**What it does.** Treats removal as a discipline: code is a liability, Hyrum's Law (with enough users every observable behaviour is depended on), plan deprecation at design time. A five-question deprecation decision, advisory against compulsory deprecation, a four-step migration (build the replacement, announce, migrate one consumer at a time, remove), three patterns (strangler, adapter, feature flag), a database section on expand/contract with a worked column rename, zombie code, rationalisations, red flags and a verification list.

**Safety read.** No scripts, no network calls, nothing aimed at a reviewer. `npx migrate-check` is only an example inside a sample notice. It refers to `incremental-implementation`, a skill we do not have. The description is broad enough to self-trigger.

**Why it is shelved, not rewritten** (the other session's review said "rewrite, keep only expand/contract, plus never drop or rename, PARK").
1. **Most of it is a human decision.** Whether to deprecate, advisory or compulsory, consumer notice periods and removal dates are intent and client-contract questions (rules 1 and 9). A night agent should never run the removal step.
2. **It pushes toward deletion.** "Code is a liability" and "if it is needed later, rebuild it" clash with the one-way-door rule. Plan 5.x scores column drops at 8 and table drops at 9, and `create_schema.py --plan` flags them. Adopted `principle-subtract-before-you-add` already scores removal from a managed solution as size L.
3. **It supports leaving `principle-migrate-callers-then-delete-legacy-apis` on the shelf.** That principle changes callers and deletes the old API in one wave. This skill says migrate one consumer at a time and remove only after zero usage, which is the safer rule.
4. **The patterns need what we do not have.** Strangler, adapter and feature-flag migration need production traffic and flags. Client production is human work (rule 15). Examples are TypeScript and Postgres.

**Worth keeping: expand/contract.** It fits Power Platform because a Dataverse column's logical name cannot be renamed, so a "rename" is already add a new column, dual-write, backfill, switch reads, drop later. Rules that carry over:
- additive first, destructive last and alone;
- a drop or rename ships as its own change, after nothing references the old shape;
- backfill in batches;
- test the way back.

Each phase would be its own story (rule 7). The contract step is size L, so a human approves it. For Power Platform the way back is restoring from the Test baseline, because dropped data cannot be reverted by a redeploy.

**Verdict (proposal): shelve.** Lift the expand/contract steps into a block of about 1 KB in the spec preset or the agent instructions, with "a drop or rename means PARK `one_way_door`". That is a plan edit needing Boroon's review (rule 17), to be made when Appendix C is next edited or for BAU Managed Services, where client schema changes are the likely trigger. Not adopted, not edited, nothing written to `.claude/skills/`.

## `security-and-hardening` (Addy), read 2 November 2026

Files read in full: `SKILL.md` (17.6 KB), `references/hardening-patterns.md` (13.4 KB), and the shared `references/security-checklist.md` (14.5 KB) that the skill links to from outside its own folder. About 45 KB in all, not the 30 KB the other session's review gave. Also read, as background only and not copied: Addy's eval case and a deliberately vulnerable webhook fixture. Copied unchanged to `skills/addy/security-and-hardening/`, with the shared checklist at `skills/references/security-checklist.md` so the skill's relative links resolve on our layout (upstream they point at the repo root). Pinned `addyosmani/agent-skills` commit `301b02b`, MIT.

**What it does.** Web-app security for agents. Threat model first (trust boundaries, assets, STRIDE, abuse cases). A three-tier rule list: always do, ask first (human approval), never do. Controls for injection, XSS, access control, sessions, headers and CORS, validation and uploads, SSRF, destructive operations on derived paths, rate limiting and secrets. A supply-chain section (install-script gate, audit against the committed lockfile, reachability triage). Privacy (classify, minimise, retain, delete). An AI/LLM section (OWASP LLM Top 10). Rationalisations, red flags and a checklist.

**Safety read.** No scripts, no network calls, nothing aimed at a reviewer. The only commands are read-only, such as `git diff --cached ... --name-only` for a secret check. `npm audit fix --force` is named only to forbid it. The long description would self-trigger on anything touching auth, input, dependencies or personal data.

**Why it is shelved as a whole** (the other session's review said "rewrite, too big and Express-flavoured, keep always/ask/never").
1. **Wrong shape.** Node and Express flavoured (helmet, bcrypt, express-rate-limit, zod, npm/pnpm/Yarn). Nothing for C#, .NET, Python or Power Platform. Client stacks are not known yet.
2. **The builder would grade itself (rule 2).** The checklist is self-reported. Security checks need to be deterministic gate steps and reviewer rubric items.
3. **Its human steps become PARKs.** "Ask first (requires human approval)" and "audit before every release" are PARKs or human steps (rules 1 and 9).
4. **Size.** About 45 KB across three files, mostly irrelevant to a given story.

**Three things worth acting on.**
1. **The "ask first" list is a ready-made Merge Danger and PARK list for code repos.** New auth flows, new categories of sensitive data, new external integrations, CORS, file uploads, rate limiting, elevated roles. Plan Appendix B already scores a security role at 7. For pro-code these become path and change-class rules that raise the score or PARK for design approval. A plan edit for Boroon's review (rule 17).
2. **Rule 5 has a concrete form in the supply-chain section.** An `npm install` runs other people's code. Blocking dependency scripts before first execution and auditing the committed lockfile belong in the gate (deterministic), not in the builder's instructions.
3. **Prompt injection looks unaddressed in the plan.** A search of the plan for "prompt injection" and "injection" found no hit. The whole plan was not re-read to be sure. The skill's point is that model output and any text in the context (a ticket, a fetched page) is untrusted, and permissions are enforced in code, not in the prompt. It matters for `pcp-triage`, which reads AutoTask and PRTG ticket text, and for Copilot Studio agents.

**Plan gap to confirm.** The only security-type check found in the gate (Appendix A) is the solution checker SARIF, which is Power Platform. No secret scan, dependency audit or code scanning for code repos turned up in a keyword search. To be settled before Stage 5 (day 46, Lane B for code repos). A plan question, not a skill question.

**Verdict (proposal): shelve.** Record the three items above as open items. Not adopted, not edited, nothing written to `.claude/skills/`.

## `bug-fix` playbook and "Opening a PR" (Tan), read 2 November 2026

Files read in full: `skills/tan/poteto-mode/playbooks/bug-fix.md` (2.4 KB) and `opening-a-pr.md` (5.6 KB), which `bug-fix` ends with and the other session's review marked as unread. Both are playbooks inside `poteto-mode`, already on the shelf and byte-identical to the pinned `cursor/plugins` commit `ae5650f`. Nothing was copied.

**`bug-fix` verdict: dropped for now (Boroon, 2 November 2026).** Wired to Cursor (the `Task` tool, `/loop`, a "control skill", and an other-vendor model slug that clashes with the residency tiers). The lead agent owns the verdict, which breaks rule 2. It leans on `architect`, `interrogate` and `tdd`, which we have not adopted.

Ideas worth lifting later (the review listed three; these are five):
1. Every shipped line traces to runtime evidence. "Belt-and-suspenders that might help is a hypothesis, not a fix." A good standards-reviewer check.
2. Revert what a refuted hypothesis motivated.
3. "Inconclusive" or wrong-surface is not a pass (rule 2, `principle-prove-it-works`).
4. The failing repro lands before the fix in git history. The gate can check this deterministically and put it in the PR evidence. It extends "red before green" in plan 5.12.
5. The reply pastes failing-then-passing output verbatim, which fits the before/after table in the PR template (plan C.7).

For bugs the repro should come from `pcp-triage`, written by someone other than the builder and locked before the night (rule 3). The builder's own repro stays a `tests/dev/` check, not acceptance evidence.

**"Opening a PR" verdict: dropped.** It conflicts with rule 7: it prefers five narrow stacked PRs, each child targeting its parent branch. It uses Cursor's `/deslop`, `/no-comments` and `/technical-writing`, and Origin and Graphite. Our driver opens the PR from `pr.md`, not the agent.

Worth lifting into the planned `pr-body` skill (plan C.7), whose template already has what and why, a diagram, a before/after table and refactor candidates:
- a **Scope** section: what the PR deliberately leaves out;
- a **Tradeoffs** section: rejected alternatives a reviewer would ask about, only when there was a real choice;
- "if main is red, state the cost of leaving it red" in the blast radius;
- the PR body is a one-minute briefing, with full SHAs and long verdicts in a linked artifact.

Conventional Commit titles may not match client repo conventions. Skills follow the project's own conventions.

## Open item: no live skill takes a confirmed bug from repro to fix

Checked 2 November 2026 against the live descriptions. Pieces exist: `getai-intake`, `pcp-triage` and `lcp-triage` (read-only, no fix), `pcp-how`, `pcp-why`, `pcp-blast-radius` and `lcp-blast-radius`, `getai-decision-log`, and the principles `fix-root-causes`, `sequence-verifiable-units`, `prove-it-works` and `test-behavior-not-implementation`. Nothing joins them from a locked repro to a fix and evidence, and nothing covers Power Platform bugs. `diagnosing-bugs` is shelved for BAU Managed Services.

Known and decided, not an oversight: bugs go to Lane B (code) at Stage 5 (day 46), and `pcp-triage` stops before the fix because of rule 3. Cheapest fix when needed: a short `pcp-fix` skill of about 1 to 2 KB that sequences the existing pieces (start from the locked repro in `triage.json`, commit the failing check before the fix, make the smallest change the evidence justifies, run `pcp-blast-radius`, put failing-then-passing output in the PR body), with the five `bug-fix` ideas above folded in. An `lcp` version would use `lcp-verify` as the loop. Revisit before Stage 5, or with `diagnosing-bugs` for BAU Managed Services.
