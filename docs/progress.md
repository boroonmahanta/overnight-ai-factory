# Progress log

Read this second, after `CLAUDE.md`. Add a new entry at the top of the log at the end of every session.
Keep entries short. Write for a reader who has no memory of the chat.

Entry template:

```
## Session N, <date>, branch <name>
Done:
Decisions:
Files changed:
Open items:
Next steps:
```

## Current state

- Documents only. No code, no pipelines, no environments exist yet.
- The main plan is V3.1, dated 1 November 2026: `docs/sources/plan-v3.1.md`. It was edited in Session 2 (see below). Every addition is marked with its date.
- Nothing from the plan has been built or tested. Every item marked `[untested]` in the plan is still untested.
- Work is sized with T-shirt sizes (XS to XL), approved on 1 November 2026. See `CLAUDE.md`.
- The skills proposal is a matrix by lane and size: `docs/analysis/skills-by-lane-and-size.md`. Boroon accepted it.
- Rule from Boroon: story first. Every unit of work, in every lane, mode and size, is an ADO story drafted by the Story Planner, so all effort and cost can be tracked.

## Open items

- **Next work: read skill batch 1 in full** (13 skills for `lcp`, about 39K tokens; list in `skills-by-lane-and-size.md` section 7). Then write the router skill. Batches 2 (`pcp`) and 3 (Lane A) wait until nearer stages 5 and 6.
- **Story Planner agent** is defined in plan Appendix C.8 but untested. It needs a build in stage 2.
- **Plan wording that may still say "code profile" only**, without `pcp`: plan sections 4.2 and 4.4, and the one-pager. Not changed.
- **Not read in full.** Files added from the zip were saved but not read: reports V1 and V2, the runtime and costs note, the eight GitHub and Azure notes, the five Power Platform notes and the one-pager. The five workshop slide images were saved but not viewed. The plan condenses most of them. Read one only when a task needs its detail.
- **Other session** ("Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`) is no longer needed and can be deleted.
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The source itself is cut off.
- The credit ruling (spike 0.1) has not been sent to Partner Center. The question text is in plan section 9.1.
- Spike 0.9 has a hard date. Audit for unmanaged developer environments before 15 November 2026.

## Log

## Session 2, 2026-11-01 and 2026-11-02, branch `claude/sharp-wright-1muptp`

Done:
- Redid the skills proposal as a matrix: `docs/analysis/skills-by-lane-and-size.md`. Rows: Greenfield Lane A, Lane B `lcp`, Lane B `pcp`, plus an "All lanes" base row. Columns: Prototype, XS, S, M, L, XL, BAU Managed Services. It also lists the skills that moved, what GET AI must write itself, and a read-in-full order tied to build stages.
- Added `pcp` (pro-code platform) to the naming rule in `CLAUDE.md` and plan section 1.1.
- Extended plan Appendix D: human minutes split into five phase fields, `Custom.WorkSize`, `Custom.WorkMode`, `Custom.StoryOrigin`, `Custom.OverheadClass`, `Custom.ClarityTest`, the `overhead` tag, `pcp` and `lane_a` in the Lane Profile picklist, and a new section D.4 "Story first". The ledger schema line in section 10.2 got the same profile values plus `work_size` and `work_mode`.
- Rewrote plan section 6.5: the Copilot Studio front door is the default. Other customer requirements (documents, SOW or RFP, emails, meeting notes, service desk requests, ADO items, triage groups) can feed the Story Planner and Wayfinder directly. A draft ADO item is made first, so intake cost has an `ado_id`. The Story Planner runs a grouping check (duplicates, same table or flow or app, shared root cause). The Chief of Staff paragraph explains why it was dropped and lists three grouping steps that keep its function: intake, triage and the 17:00 night plan. Five other "optional front door" mentions were fixed.
- Added plan Appendix C.8: the `story-planner` agent definition (read-only, writes `planning/<intake-id>/plan.json`, the orchestrator files the ADO items). Untested.
- Measured skill sizes from clones in scratch space (rough, bytes divided by 4): Wayfinder `SKILL.md` is 12.4 KB, about 3,100 tokens, and runs only when invoked. Reading batch 1 in full is about 39K tokens, batch 2 about 29K, batch 3 about 31K. Largest single skills: `idea-refine` 41 KB, `constraint-driven-development` 33 KB, `security-and-hardening` 31 KB, `reproduce-and-fix-issues` 29 KB.

Decisions (Boroon):
- 1 November: `pcp` means pro-code platform, the plan's "Lane B, code profile".
- 1 November: Lane A has no XS or S. Prototype is a mode and BAU is an on-ramp. Neither is a size. The matrix is accepted.
- 1 November: story first. A story is required for every unit of work in every lane, mode and size. The Story Planner drafts it by default. Human-written stories are allowed but not the default and are flagged.
- 2 November: Wayfinder is not run for every story. The clarity test runs on every story and is recorded; a map is built only when it fails.
- 2 November: a router skill is wanted. It maps size, mode and lane to the skills to use. Write it after batch 1 is read.
- 2 November: skills are read in batches. Batch 1 is approved now. Batches 2 and 3 are read later. `idea-refine` is proposed for removal from batch 3; not yet confirmed.

Files changed:
- New: `docs/analysis/skills-by-lane-and-size.md`.
- Edited: `CLAUDE.md` (map row, naming table, lane list, Story first term), `docs/analysis/tshirt-sizing.md` (pointer), `docs/sources/plan-v3.1.md` (sections 1.1, 1.2, 2, 4, 6.5, 8, 10.2, decision log, Appendix C.8, Appendix D and D.4), `docs/progress.md`.

Open items: see the top of this file.

Next steps:
1. New session: read skill batch 1 in full. For each skill report keep, rewrite for GET AI, or drop, and quote anything risky. Install nothing.
2. Write the router skill.
3. Build the Story Planner and `lcp-verify` in stage 2.
4. Confirm whether to drop `idea-refine` from batch 3.

## Session 1, 2026-11-01, branch `claude/jolly-albattani-818i8e`

Done:
- Added the `/bro` skill at `.claude/skills/bro/SKILL.md`. It is copied unchanged from `cursor/plugins`, `pstack/skills/bro`. It restates the last message in plain language. It only runs when invoked.
- Read and digested, in full: the V3.1 plan, the Spec Kit Part 2 transcript, the Anthropic workshop transcript and Boroon's original Word plan.
- Fixed GitHub push access. The Claude GitHub App was not installed on the repo. Boroon installed it on the one repo. Push now works.
- Built this context structure so work can span many short sessions: `CLAUDE.md` (map), this log, and full sources in `docs/sources/`.
- Boroon re-uploaded five research files. Three were byte-identical to files already saved (Spec Kit transcript, Anthropic workshop transcript, Word plan) and were skipped. The other two, the Tan and Pocock podcast and the Pocock v1.3 transcript, were read in full and saved verbatim.
- Boroon then uploaded two earlier reports, "Grill the Spec, Lock the Tests" and V2.1. Both were read in full and saved verbatim. The main plan supersedes them. They are kept for detail the plan condenses.
- Boroon then uploaded "plan_V3.1_latest" and "plan_V3". The V3.1 file was byte-identical to the copy already saved, so it was skipped. V3 is new. V3.1 is an in-place edit of V3, so a line comparison showed everything unique to V3 is older wording that V3.1 replaced. V3 was saved as a superseded snapshot.
- Boroon then uploaded the Pocock v1.1 transcript, a second copy of the Pocock v1.3 transcript and the Tan podcast (both byte-identical to saved files, skipped), and five research notes. The v1.1 transcript and the notes were saved verbatim under `docs/sources/` and `docs/sources/research-notes/`.
- Boroon added two skills-review transcripts: a review of the pstack skills and a video comparing the packs of Addy Osmani, Matt Pocock and Lauren Tan. Both saved verbatim. Boroon then asked for a comparison. The three repos were cloned into scratch space (not kept) and every skill was listed from them. Two analysis files were written in `docs/analysis/`: `skills-comparison.md` and `tshirt-sizing.md`. Verdicts rest mostly on descriptions and routing documents, not full skill bodies.
- Boroon finally uploaded the full research folder as a zip. Of 43 files, 22 were already in the repo and were skipped, plus two extra copies of the original plan (`uploaded_plan_pandoc.md`, `uploaded_plan_yaml.txt`) whose text matches the version already saved. The new files were added: reports V1 and V2, the runtime and costs note, eight GitHub and Azure notes, five Power Platform notes (including the V3.1 changes brief and the review of the uploaded plan), five workshop slide images, and the engineer one-pager.

Decisions:
- Sessions stay under about 200K tokens. The context file is a short map. Full sources are read on demand by line range.
- Skills live in the repo under `.claude/skills/`, not in a user-level folder.
- **T-shirt sizes approved by Boroon on 1 November 2026:** XS, S, M, L and XL, with the rule that the size is the largest answer across reversibility, blast radius, clarity, verifiability, effort and residency. Summary in `CLAUDE.md`, detail in `docs/analysis/tshirt-sizing.md`. Not yet approved: the skills named for each size, the work-size ADO field, the router skill, and adding the sizes to the plan itself.

Files changed:
- `.claude/skills/bro/SKILL.md`, `CLAUDE.md`, `docs/progress.md`
- `docs/sources/plan-v3.1.md`, `uploaded-plan-software-factory.md` and `.docx`, `transcript-anthropic-agents-run-for-hours.md`, `transcript-spec-kit-part-2.md`, `transcript-tan-pocock-podcast.md`, `transcript-pocock-skills-v1.3.md`, `report-grill-the-spec-lock-the-tests.md`, `report-v2.1-two-lanes-one-gate.md`, `plan-v3.md`, `transcript-pocock-skills-v1.1.md`, `report-v1-fund-nights-on-credits.md`, `report-v2-two-lanes-one-gate.md`, `research-notes/` (19 files in three folders), `workshop-slides/` (five images)
- `docs/one-pager/` (the engineer one-pager as HTML and Markdown)
- `docs/analysis/skills-comparison.md`, `docs/analysis/tshirt-sizing.md`, `docs/sources/transcript-pstack-skills-review.md`, `docs/sources/transcript-skills-comparison-addy-pocock-tan.md`

Open items: see above.

Next steps:
1. Boroon adds more context in the next session. Record it here and in `CLAUDE.md` if it changes a decision.
2. Read the shortlist of skills in full, starting with the first batch in `docs/analysis/tshirt-sizing.md` step 2, once Boroon approves it.
3. Decide the work-size ADO field and the router skill, then add the sizes to the plan if Boroon agrees.
4. Decide the first real build task. The plan's stage 0 and stage 1 are the starting point.
