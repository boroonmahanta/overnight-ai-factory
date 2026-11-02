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
