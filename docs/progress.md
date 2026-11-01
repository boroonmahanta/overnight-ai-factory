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

## Open items

- **Missing sources.** These are cited in the plan but are not in this repo. They sit in another Claude session's scratchpad, on a different repo (session "Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`):
  - the Pocock skills v1.1 transcript
  - the research notes (three folders) and the V3.1 changes brief
  - the earlier reports V1 ("Overnight factory on GitHub and Azure"), V2 and the V3 snapshot `plan-v3.md`

  The plan's own digests of them (sections 3.5, 3.6, 3.9) are in the repo. The raw files are not.
  Boroon can download them from that session and upload them to a new session, which should commit them under `docs/sources/`.
  Already recovered and saved: the Tan and Pocock podcast, the Pocock v1.3 transcript, the first report "Grill the Spec, Lock the Tests" and report V2.1.
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The upload was cut off. Ask for the full file if the ending matters.
- Do not delete that other session until those files are saved.
- The credit ruling (spike 0.1) has not been sent to Partner Center. The question text is in plan section 9.1.
- Spike 0.9 has a hard date. Audit for unmanaged developer environments before 15 November 2026.

## Log

## Session 1, 2026-11-01, branch `claude/jolly-albattani-818i8e`

Done:
- Added the `/bro` skill at `.claude/skills/bro/SKILL.md`. It is copied unchanged from `cursor/plugins`, `pstack/skills/bro`. It restates the last message in plain language. It only runs when invoked.
- Read and digested, in full: the V3.1 plan, the Spec Kit Part 2 transcript, the Anthropic workshop transcript and Boroon's original Word plan.
- Fixed GitHub push access. The Claude GitHub App was not installed on the repo. Boroon installed it on the one repo. Push now works.
- Built this context structure so work can span many short sessions: `CLAUDE.md` (map), this log, and full sources in `docs/sources/`.
- Boroon re-uploaded five research files. Three were byte-identical to files already saved (Spec Kit transcript, Anthropic workshop transcript, Word plan) and were skipped. The other two, the Tan and Pocock podcast and the Pocock v1.3 transcript, were read in full and saved verbatim.
- Boroon then uploaded two earlier reports, "Grill the Spec, Lock the Tests" and V2.1. Both were read in full and saved verbatim. The main plan supersedes them. They are kept for detail the plan condenses.

Decisions:
- Sessions stay under about 200K tokens. The context file is a short map. Full sources are read on demand by line range.
- Skills live in the repo under `.claude/skills/`, not in a user-level folder.

Files changed:
- `.claude/skills/bro/SKILL.md`, `CLAUDE.md`, `docs/progress.md`
- `docs/sources/plan-v3.1.md`, `uploaded-plan-software-factory.md` and `.docx`, `transcript-anthropic-agents-run-for-hours.md`, `transcript-spec-kit-part-2.md`, `transcript-tan-pocock-podcast.md`, `transcript-pocock-skills-v1.3.md`, `report-grill-the-spec-lock-the-tests.md`, `report-v2.1-two-lanes-one-gate.md`

Open items: see above.

Next steps:
1. Boroon adds more context in the next session. Record it here and in `CLAUDE.md` if it changes a decision.
2. Recover the missing sources from the other session (see Open items).
3. Decide the first real build task. The plan's stage 0 and stage 1 are the starting point.
