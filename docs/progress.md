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
- The main plan is V3.1, dated 1 November 2026: `docs/sources/plan-v3.1.md`.
- Nothing from the plan has been built or tested. Every item marked `[untested]` in the plan is still untested.
- Boroon said more context will be added in later sessions.
- Work is sized with T-shirt sizes (XS to XL), approved on 1 November 2026. See `CLAUDE.md`.

## Open items

- **Sources are complete.** Boroon uploaded the whole research folder as a zip. Every file was checked by checksum against the repo, duplicates were skipped, and the rest were added. The other session ("Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`) is no longer needed for sources and can be deleted.
- **Not read in full.** The files added from the zip were saved but not read in this session: the reports V1 and V2, the runtime and costs note, the eight GitHub and Azure notes, the five Power Platform notes and the one-pager. The five workshop slide images were saved but not viewed. The plan condenses most of them. Read one only when a task needs its detail.
- **Decisions still waiting on Boroon** (from `docs/analysis/tshirt-sizing.md`): approve the shortlist of skills to read in full before any are adopted (plan section 8.3); decide whether to add a work-size field to ADO (Appendix D); decide whether to write a GET AI router skill that routes by size. The sizes themselves are approved.
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The zip copy is the same, so the source itself is cut off.
- The credit ruling (spike 0.1) has not been sent to Partner Center. The question text is in plan section 9.1.
- Spike 0.9 has a hard date. Audit for unmanaged developer environments before 15 November 2026.

## Log

## Session 2, 2026-11-01, branch `claude/sharp-wright-1muptp`

Done:
- Read `docs/progress.md`, then redid the skills proposal as a matrix by lane and size, as Boroon asked. New file: `docs/analysis/skills-by-lane-and-size.md`. Rows: Greenfield Lane A, Lane B `lcp`, Lane B `pcp`. Columns: Prototype, XS, S, M, L, XL, BAU Managed Services. Added a base row for skills common to all lanes.
- Listed the skills that moved (section 5 of the new file), what GET AI must write itself (section 6) and a read-in-full order tied to build stages (section 7).

Decisions (Boroon, 1 November 2026):
- `pcp` means pro-code platform. It is the plan's "Lane B, code profile". Added to the `CLAUDE.md` naming table and plan section 1.1, with `profile:pcp`, `Custom.LaneProfile = pcp` and skill prefix `pcp-`.
- Lane A has no XS or S.
- Prototype is a mode and BAU Managed Services is an on-ramp. Neither is a size.
- The matrix is accepted, except where Wayfinder and the Story Planner apply.
- Open: Boroon wants Wayfinder and the Story Planner in all lanes and modes, not only at XL. Claude's proposed wording: a map is a trigger, not a default step. If the clarity test fails at any size (no locked scenarios can be written today), escalate to a Wayfinder map. The Story Planner applies wherever one request can become more than one story (M and up, Lane A, BAU clusters). XS and S stay light. Prototype is a Wayfinder child type, so the map wraps the prototype. Waiting on Boroon's answer before the matrix is changed.
- Boroon: all effort and cost (human minutes and tokens) must be tracked, so a user story in ADO is required for every unit of work in every lane, mode and size. Not negotiable. Claude's refinement, awaiting a yes: the story is always required; the Story Planner agent need not run for XS and S (a human can use a template). Gaps found in the plan: `Custom.HumanMinutes` covers review and PARK only, not day-phase spec and scenario time (about 30 of the 50 modelled minutes); day-phase AI sessions need `ado_id`; triage, gardening, retro and skill reading need standing overhead items; `Custom.WorkSize` and a mode field are now needed. Plan Appendix D not yet changed.
- **Decided (Boroon, later in the session):** story first applies in every lane, mode and size. The Story Planner drafts the story by default in all of them. No human story writing as the default, though it is allowed. Done: plan Appendix D now has the human-minutes split (five phase fields), `Custom.WorkSize`, `Custom.WorkMode`, `Custom.StoryOrigin`, `Custom.OverheadClass`, `overhead` tag, `pcp` and `lane_a` in the Lane Profile picklist, and a new D.4 "Story first". The ledger schema line (plan section 10.2) now has `profile` values `pcp`, `lcp`, `lane_a` and new `work_size` and `work_mode` columns. The matrix says "Story first" in every column of the base row.
- Still open: Wayfinder as a trigger (clarity test fails) or always. Plan text that calls the Story Planner "optional" (intake front door, section 6.5 and elsewhere) now conflicts with D.4 and needs a pass. The router skill. Approval of the three read-in-full skill batches.

Files changed:
- `docs/analysis/skills-by-lane-and-size.md` (new), `docs/analysis/tshirt-sizing.md` (pointer added), `CLAUDE.md` (map row, naming table, lane list), `docs/sources/plan-v3.1.md` (section 1.1 naming table, ledger schema line, Appendix D and new D.4), `docs/progress.md`

Open items:
- Wayfinder as trigger or always (see Decisions). The plan's "optional" Story Planner wording needs a pass.
- Approve the three read-in-full batches. Still open from Session 1: the work-size ADO field and the router skill.
- Other places that still say only "code profile" may need `pcp` added: plan sections 4.2 and 4.4, and the one-pager. Not changed.

Next steps:
1. Boroon answers the Wayfinder and Story Planner question. Then update the matrix.
2. Read batch 1 of the skills in full (the `lcp` set), then write `lcp-verify` and the router skill.

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
