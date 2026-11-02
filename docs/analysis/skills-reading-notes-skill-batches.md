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
