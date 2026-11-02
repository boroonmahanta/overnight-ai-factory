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
- **Session 4 work is in PR 9** (https://github.com/boroonmahanta/overnight-ai-factory/pull/9), opened 2 November 2026 from `claude/wizardly-planck-8i7543`, rebased onto `main`. PR 8 had merged with only the first commit. Boroon merges PR 9 by hand. Once he has, nothing from Session 4 is outstanding on a branch.
- The main plan is V3.1, dated 1 November 2026: `docs/sources/plan-v3.1.md`.
- Nothing from the plan has been built or tested. Every item marked `[untested]` in the plan is still untested.
- Boroon said more context will be added in later sessions.
- Work is sized with T-shirt sizes (XS to XL), approved on 1 November 2026. See `CLAUDE.md`.

## Open items

- **Sources are complete.** Boroon uploaded the whole research folder as a zip. Every file was checked by checksum against the repo, duplicates were skipped, and the rest were added. The other session ("Overnight AI software factory", id `session_019bVvHWrUECf7G5YiXU3fKW`) is no longer needed for sources and can be deleted.
- **Not read in full.** The files added from the zip were saved but not read in this session: the reports V1 and V2, the runtime and costs note, the eight GitHub and Azure notes, the five Power Platform notes and the one-pager. The five workshop slide images were saved but not viewed. The plan condenses most of them. Read one only when a task needs its detail.
- **Decisions still waiting on Boroon** (from `docs/analysis/tshirt-sizing.md`): approve the shortlist of skills to read in full before any are adopted (plan section 8.3); decide whether to add a work-size field to ADO (Appendix D); decide whether to write a GET AI router skill that routes by size. The sizes themselves are approved.
- The Pocock v1.3 transcript ends mid-sentence at 14:28. The zip copy is the same, so the source itself is cut off.
- **Credit ruling (spike 0.1): answered yes by Partner Center support, per Boroon, 2 November 2026.** Builds for customers can be made on credits. The written answer is not yet on file, so the spike's exit test is still open (file the answer, then check the next invoice shows "Azure credits applied" against GitHub lines).
- Spike 0.9 has a hard date. Audit for unmanaged developer environments before 15 November 2026.

## Log

## Session 4, 2026-11-02, branch `claude/wizardly-planck-8i7543`

After PR 9 merged (decision by Boroon, 2 November 2026): **partner credits can fund client builds.** He checked with Partner Center support, who said builds for customers can be made on credits, and told me to take it as a yes. Recorded in `CLAUDE.md` (biggest risk 1 and the open questions) and in the plan: section 9.1 note, spike 0.1 row, risk 1 row, section 15.1 open question and a new decision log section 14.4. Caveats written down: the answer came from support, not a written ruling filed here, so spike 0.1's exit test stays open until he files it; which credit type and designation it covers was not stated; rules 13 and 14 are unchanged (ledger at list and cash, price from list). If the written copy contradicts this, client work goes back to cash. Files changed: `docs/sources/plan-v3.1.md`, `CLAUDE.md`, `docs/progress.md`.

Done:
- Boroon gave the three-batch skills plan from the chat "Planning the skills to use": batch 1 `lcp` (13 skills, needed before Stage 2, day 15), batch 2 `pcp` (16, before Stage 5, day 46), batch 3 Lane A (8, before Stage 6, day 60). Another session read all 36 and wrote `docs/analysis/skill-batches-review.md`. That file is only on branch `claude/sharp-wright-1muptp` (commit `c3a1c72`), not on `main`. Its verdicts are proposals, and its reads were done by agents, not line by line.
- Checked the 36 skills against this repo: 19 live (4 unchanged, the rest adapted, including `show-me-your-work` as `getai-decision-log`), 1 on the shelf (`principle-migrate-callers-then-delete-legacy-apis`), 16 untouched. This corrects the 18 / 2 / 16 count I gave in chat. Batch 3 is entirely untouched. `idea-refine` was already dropped from batch 3 and folded into the Story Planner.
- Read `show-me-your-work` and `pause-safely` in full (rule 19), from the pinned commit `ae5650f`.

Decisions (Boroon, 2 November 2026):
- **`show-me-your-work`: keep as `getai-decision-log`.** It was already adapted and merged (I wrongly called it shelved in chat). Needs a test, not a rewrite. Gaps: the transcript audit assumes a transcript in the evidence bundle, which the plan does not yet say; nothing checks that the log reached Blob.
- **`pause-safely`: drop.** A 12-line playbook inside `poteto-mode`, not a skill. PARK, `park.json` and the handoff files cover it. Its one useful idea (a `wip:` checkpoint on a non-PARK stop) went into the plan.
- **Plan edit:** section 5.11 has a new paragraph, "Stops that are not a PARK". On a timeout, exhausted cap or killed replica, the driver commits a `wip:` commit, pushes with no PR, logs `INCONCLUSIVE` and leaves the handoff files. Marked `[untested]`.

Then (Session 4, second request), decisions by Boroon:
- **`diagnosing-bugs` read in full and shelved.** Copied unchanged to `skills/pocock/diagnosing-bugs/` (pinned `4ae2317`). Not adopted. **Revisit for the BAU Managed Services mode.** Proposal: rewrite as `pcp-diagnose`, with interactive steps turned into PARKs, model invocation off, the builder's regression test labelled its own check, and lowercase `glossary.md`. Open question for then: may a night agent run all six phases, or only reproduce and minimise (as `pcp-triage` does)?
- Notes for all three reads (`show-me-your-work`, `pause-safely`, `diagnosing-bugs`) are in the new `docs/analysis/skills-reading-notes-skill-batches.md`. `skills/README.md` and `CLAUDE.md` updated.

Then (Session 4, third request), decisions by Boroon:
- **`code-simplification` read in full and shelved.** Copied unchanged to `skills/addy/code-simplification/` (pinned `301b02b`). Not adopted. Reason: plan 5.12 says refactoring belongs to review, not the build loop, so a builder skill that simplifies is the wrong tool. Its three signal tables are worth lifting into the standards reviewer rubric. A refactor-only night story (`pcp-simplify`) is possible later. This differs from the other session's review ("rewrite").

Then (Session 4, fourth request), decisions by Boroon:
- **`deprecation-and-migration` read in full and shelved.** Copied unchanged to `skills/addy/deprecation-and-migration/` (pinned `301b02b`). Not adopted. Mostly human decisions (rules 1 and 9) and it pushes toward deletion. Keep expand/contract (a Dataverse column cannot be renamed, so it is already how a rename works): a block of about 1 KB in the spec preset or agent instructions, drop or rename means PARK `one_way_door`. A plan edit, not yet made. It also supports leaving `principle-migrate-callers-then-delete-legacy-apis` on the shelf. Differs from the other session's review ("rewrite").

Then (Session 4, fifth request), decisions by Boroon:
- **`security-and-hardening` read in full and shelved.** Copied unchanged to `skills/addy/security-and-hardening/` (pinned `301b02b`), with its shared checklist at `skills/references/security-checklist.md`. Not adopted. Differs from the other session's review ("rewrite"). Three items raised, none yet decided: (1) the skill's "ask first" list as a Merge Danger and PARK rubric for code repos (plan Appendix B, a plan edit); (2) supply-chain checks (dependency scripts blocked, lockfile audit) as gate steps for code repos; (3) prompt injection, which a keyword search found no mention of in the plan. Open question: the gate (Appendix A) shows only the solution checker SARIF as a security check, so code repos have none planned. Settle before Stage 5 (day 46).

Then (Session 4, sixth request), decisions by Boroon:
- **`bug-fix` dropped for now**, and its dependency "Opening a PR" read and dropped too (it conflicts with rule 7, stacked PRs). Both are playbooks already on the shelf inside `poteto-mode`, so nothing was copied. Five `bug-fix` ideas and four PR-body ideas (Scope, Tradeoffs, blast radius if main is red, one-minute briefing) are recorded in the notes for later.
- **Open item noted: no live skill takes a confirmed bug from repro to fix.** Pieces exist, nothing joins them, and nothing covers Power Platform bugs. Cheapest fix: a short `pcp-fix` skill (about 1 to 2 KB) sequencing the existing skills, plus an `lcp` version using `lcp-verify`. Revisit before Stage 5 (day 46), or with `diagnosing-bugs` for BAU Managed Services.
- **`debugging-and-error-recovery` read in full and shelved.** Copied unchanged to `skills/addy/debugging-and-error-recovery/` (pinned `301b02b`). Not adopted. `diagnosing-bugs` is stronger; it tells the agent to update an outdated test, which conflicts with locked tests. Keep its "error output is untrusted data" section.
- **Open item added: prompt injection is not covered in the plan** (raised by this skill and by `security-and-hardening`; keyword search only). Cheapest fix: a 1 KB block in the agent instructions (plan C.2). A plan edit for Boroon's review. Decide before the first triage workflow is wired.

Then (Session 4, seventh request), decisions by Boroon:
- **`codebase-design` read in full and shelved.** Copied unchanged to `skills/pocock/codebase-design/` (pinned `4ae2317`, 4 files). Not adopted. For Lane A or day work. Conflicts with the no-refactoring rule (plan 5.12) and tells the builder to delete tests; its banned word "component" clashes with Power Platform. Lift the deletion test and the two-adapters rule into the reviewer smell list. Decide together with `architect` (batch 3). Same direction as the review ("drop, keep for Lane A").
- Boroon: anything worth adding from `improve-codebase-architecture` and the next skill is decided together.
- Tidied the `CLAUDE.md` row for the skill-batches notes, which had lost its punctuation across edits.

Then (Session 4, eighth request), decisions by Boroon:
- **`improve-codebase-architecture` read in full and shelved.** Copied unchanged to `skills/pocock/improve-codebase-architecture/` (pinned `4ae2317`, 3 files). Not adopted. Batch 2 reading is finished.
- **Batch 3 drops recorded:** `ci-cd-and-automation`, `shipping-and-launch` and `arena`, on the other session's tags. We have not read them in full. Reconsider only after a full read.
- **Roll-up of 8 possible additions** written at the end of the notes file, for a joint decision with Boroon (nothing made yet).
- Reading the remaining four batch 3 skills next: `frontend-ui-engineering`, `api-and-interface-design`, `observability-and-instrumentation`, `architect`.

Then (Session 4, ninth request), decisions by Boroon:
- **Batch 3 read and shelved:** `frontend-ui-engineering`, `api-and-interface-design`, `observability-and-instrumentation` (Addy, pinned `301b02b`) and `architect` (Tan, pinned `ae5650f`), copied unchanged, with the two Addy checklists in `skills/references/`. None adopted. **Revisit in Stage 6** (Lane A, from day 60).
- **Decision: Lane A's architecture sketch gets a day approval** (the architect's Phase C checkpoint on by default, at least for Lane A and size L). The plan currently has Lane A's generator write `plan.md` and `tasks.md` at night with no human step, so this needs a plan edit (sections 4 and 5), not yet made. Rule 9 is the reason (the review wrongly cited rule 10).
- **All reading for the three batches is finished** except the three dropped batch 3 skills. Roll-up of 14 possible additions is at the end of `docs/analysis/skills-reading-notes-skill-batches.md`, for a joint decision.

Then (Session 4, tenth request): Boroon asked to update the pull request and merge it, then stopped that and asked for this log update instead. Nothing was merged or rebased by me.
- **State found:** `origin/main` shows "Merge pull request #8" at `b5fcd69`, and `main` has moved since this branch was cut. That merge brought in only the first commit of this session (`1614acb`: the `show-me-your-work` and `pause-safely` verdicts and the plan 5.11 paragraph). I read this from the git log. I did not get to read PR 8 itself.
- **So the later commits on `claude/wizardly-planck-8i7543` were not on `main`; PR 9 now carries them:** the `diagnosing-bugs`, `code-simplification`, `deprecation-and-migration`, `security-and-hardening`, `debugging-and-error-recovery`, `codebase-design`, `improve-codebase-architecture` and batch 3 shelf copies, their notes, the `bug-fix` drop, the roll-up of 14 additions, and the day-approval decision for the Lane A sketch (latest commit `8e48acf`). About 29 files and 4,000 added lines against `main`.
- **Done:** rebased the 10 later commits onto the current `main` (no conflicts; `main` already held the first commit, so nothing was lost) and pushed to the same branch with a lease. Opened PR 9 (https://github.com/boroonmahanta/overnight-ai-factory/pull/9). Not merged by me. Boroon merges it by hand.

Files changed: `docs/sources/plan-v3.1.md` (one paragraph in 5.11), `docs/progress.md`, `docs/analysis/skills-reading-notes-skill-batches.md` (new), `skills/pocock/diagnosing-bugs/` (new, 3 files), `skills/README.md`, `CLAUDE.md`. Also `skills/addy/code-simplification/` (new, 1 file) `skills/addy/deprecation-and-migration/` (new, 1 file), `skills/addy/security-and-hardening/` (new, 2 files) and `skills/references/security-checklist.md` (new).

Open items:
- The review file is not on `main`. Where it differs from what is live: it says drop `wizard` (we have `getai-wizard`), drop `principle-model-the-domain` (adopted), and rewrite the four skills adopted unchanged. Boroon decides each. Not changed.
- All 36 skills in the three-batch plan are now read (or, for `ci-cd-and-automation`, `shipping-and-launch` and `arena`, dropped on the other session's tags without our own full read). Nothing new is adopted. Decide the 14 roll-up additions together, then make the plan edits (rule 17).
- **No bug-fix workflow** (see the sixth request above). Decide before Stage 5.
- Add to the Stage 3 driver spec: the non-PARK stop checkpoint, and where the transcript lives for the decision-log audit.
- Not started: spike 0.9 (environment audit, before 15 November 2026). Spike 0.1 is answered but the written copy is not filed.

Next steps:
1. Boroon merges PR 9. Then branch the next session from `main`.
2. Spike 0.9: audit for unmanaged developer environments before 15 November 2026 (hard date).
3. Spike 0.1: file the written Partner Center answer (ticket reference or email), then check the next invoice for "Azure credits applied".
4. Decide the 14 roll-up additions with Boroon (end of `docs/analysis/skills-reading-notes-skill-batches.md`), starting with items 1 and 2 (prompt injection, code-repo security checks), then make the plan edits for his review (rule 17). Includes the day approval of the Lane A sketch.
5. Boroon rules on where the other session's review differs from what is live. The review file (`docs/analysis/skill-batches-review.md`) is still only on branch `claude/sharp-wright-1muptp`.
6. Reading is finished. Revisit the shelved Lane A skills at Stage 6 and `diagnosing-bugs` for BAU Managed Services.

## Session 3, 2026-11-02, branch `claude/exciting-babbage-4u2zp4`

Boroon answered the five open items from Session 2.

Done:
- **AutoTask and PRTG reports:** the export route is their APIs or an MCP server. Not built, not tested. Written into `pcp-triage` ("Where reports come from" and step 1 of "Running it by hand") and plan section 4.5. Manual run by day is still the only mode in use. Reports hold personal data, so the scrub-first rule still applies to anything an API or MCP server returns.
- **`Custom.TriageSource`:** added AutoTask and PRTG to the picklist (plan Appendix D). Plan 4.5 inputs table has a new row.
- **Real `main` branch:** created on GitHub from the default branch tip (`696aa3c`, the merge of PR 2). The default branch setting is still `claude/jolly-albattani-818i8e`. Changing the default is a GitHub setting I cannot make. Boroon: Settings, Branches, switch default to `main`. Rule 1 says only humans merge to `main`, so add a branch protection rule while there.
- **Batch 2 skills read in full:** `unslop`, 24 `principle-*`, `grilling`, `domain-modeling`. Copied unchanged to `skills/tan/` and `skills/pocock/` at the same pinned commits. Notes in `docs/analysis/skills-reading-notes-batch2.md`. None adopted.
- **Verification skills fixed:** `create-verification-skill` and `maintain-verification-skill` now write to `.claude/skills/lcp-verify/` (or `pcp-verify`) with name `lcp-verify`. A dated note at the top of each records the change. The shelf copies stay as the originals. Rule 17: these edits need Boroon's review by PR.
- `poteto-mode` was not copied or read in full, as Boroon asked. Only its file list and the first 40 lines of `SKILL.md` were looked at, to give a basis for the discussion.

Findings that need a decision:
- `domain-modeling` writes `GLOSSARY.md`, in capitals, with no implementation details. The plan wants lowercase `glossary.md` with Dataverse schema names, and the protected-paths pattern in Appendix A matches lowercase only. Adopting unchanged would leave the glossary unprotected.
- `grilling` (pinned) asks a round of questions at a time. Plan 6.2 says one question at a time. The plan's wording came from the older v1.1 video.
- `principle-never-block-on-the-human` and `principle-outcome-oriented-execution` conflict with rules 9 and 7. `principle-migrate-callers-then-delete-legacy-apis` assumes no external users.

Files changed:
- New: `docs/analysis/skills-reading-notes-batch2.md`, `skills/tan/unslop/`, `skills/tan/principle-*/` (24), `skills/pocock/grilling/`, `skills/pocock/domain-modeling/`
- Edited: `.claude/skills/create-verification-skill/SKILL.md`, `.claude/skills/maintain-verification-skill/SKILL.md`, `.claude/skills/pcp-triage/SKILL.md`, `docs/sources/plan-v3.1.md` (Appendix D picklist and a 4.5 row), `skills/README.md`, `CLAUDE.md`, `docs/progress.md`
- GitHub: new branch `main`

Open items:
- Discuss `poteto-mode` (questions are at the end of the batch 2 notes).
- Which batch 2 skills to adopt. My proposal is in the notes. Decide rounds against one at a time for `grilling`, and the glossary naming.
- Switch the GitHub default branch to `main` and protect it.
- Review of the two edited verification skills (rule 17).
- AutoTask and PRTG API or MCP integration: who builds it, with what read-only credential, and whether an MCP server for either exists. Not checked.

Next steps:
1. Talk through `poteto-mode`. Then read it in full if wanted.
2. Adopt or adapt batch 2 by Boroon's picks.
3. Write the first `lcp-verify` with `create-verification-skill` (stage 2).

Then (Session 3, second request), decisions by Boroon:
- **Glossary files lowercase.** `getai-domain-modeling` written in `.claude/skills/`: `glossary.md`, `glossary-map.md`, `docs/adr/`, a Schema line per term (Dataverse names or code symbols), day only.
- **Grilling in tranches of five at most.** `getai-grilling` written: most blocking first, the rest held. Plan 6.2 bullet changed from "one question at a time" to this. `ask-me` status line updated.
- **Three principles stay on the shelf** (`never-block-on-the-human`, `outcome-oriented-execution`, `migrate-callers-then-delete-legacy-apis`). Revisit when an issue calls for them. The cases to watch are in the batch 2 notes.
- **`poteto-mode` read.** Copied to `skills/tan/poteto-mode/`. Verdict in `docs/analysis/skills-reading-notes-batch2.md`: a Cursor plugin, not harness agnostic. It has a Claude Code adapter but nothing for GitHub Copilot or VS Code. Several playbooks break rules 1, 2, 6, 9 and 12. Proposal: do not adopt, lift a few small ideas. I did not read the `watch-pr` TypeScript (about 3,800 lines) line by line, only searched it.
- Both new skills are untested and need Boroon's review by PR (rule 17).

Open items added: plan line 703 says the executor's `lcp-verify` copy lives in `.github/skills/lcp-verify/`, while the verification skills now write to `.claude/skills/lcp-verify/` as Boroon asked. Copilot reads both (plan line 858), but the plan should pick one. Not changed. Unslop and the remaining principles: adoption not yet decided. Whether to lift the poteto ideas into `ask-me`.

Then (Session 3, third request), decisions by Boroon:
- **One skills folder: `.claude/skills/`.** Plan edited in five places (section 5.9 line about the two copies, the 8.x table row, C.5 heading, C.7 heading, and the two protected-paths lists, which now put skills under `.claude/**`). Plan 8 now says skills live in `.claude/skills/` only. The gate's trusted copy of `lcp-verify` stays in `factory-gates`. Copilot reading `.claude/skills` rests on the plan's cited GitHub docs and is untested by us. Check it in spike 0.6.
- **Four poteto habits lifted into `ask-me`:** open with the goal, label claims, classify a question before asking, fix/dismiss/ask on review comments. Not lifted: the 22 playbooks and the performance mantras. `ask-me` also now says the verification skills write to `.claude/skills/lcp-verify/`.
- Rule 17: `ask-me` change needs Boroon's review by PR.

Then (Session 3, fourth request), decisions by Boroon:
- **Adopted into `.claude/skills/`:** `unslop` and 21 `principle-*` skills (list in `skills/README.md`). Names unchanged so their links hold. A dated GET AI note sits at the top of each, and `unslop` has a new rule 34 (Australian English). `principle-guard-the-context-window` is adopted because Boroon likes it, with a note tying it to the 200K session limit.
- `ask-me` has a new "Principles to reach for" section. The three conflicting principles are listed there as shelved.
- Known gap: `principle-explain-the-number` links to `benchmark-checklist`, which we do not have. `principle-type-system-discipline` names `typescript-best-practices`, also not adopted. Notes in both skills.
- Batch 2 is finished except for review (rule 17) and testing. Nothing adopted has been run.

Then (Session 3, merges and `main`), done at Boroon's request:
- PR 3 (https://github.com/boroonmahanta/overnight-ai-factory/pull/3) merged the batch 2 work into the old default branch `claude/jolly-albattani-818i8e` (merge commit `9c8b91a`). Rule 17 review met for the batch.
- PR 4 (https://github.com/boroonmahanta/overnight-ai-factory/pull/4) merged that branch into `main` (merge commit `79eb828`), at Boroon's direction (rule 1: a human decides every merge to `main`).
- **`main` is now the GitHub default branch** (Boroon switched it). A ruleset `protect-main` guards it: pull request required, no force pushes, no deletions, all merge methods allowed, Boroon on the bypass list. `claude/jolly-albattani-818i8e` is retired and can be deleted once Boroon is happy.
- From now on, session branches start from `main`, and merge into `main` by pull request with Boroon's go.
- This closes the open items "real `main` branch" and "switch the default and protect it".

Then (Session 3, merge rule), decision by Boroon: **he merges every pull request into `main` by hand, to stay compliant with rule 1.** I open the pull request and stop. Noted in `CLAUDE.md`. PR 6 (log of the merges and `main` as default) was merged by him.

## Session 2, 2026-11-02, branch `claude/hopeful-mccarthy-znxbf8`

Done:
- Started step 1 of `docs/analysis/tshirt-sizing.md` section 4 (read the shortlist in full). Boroon said to use a top-level `skills/` folder that does not auto-load.
- Cloned the three public repos to scratch space, found the 16 skills in the first batch, and copied them unchanged into `skills/addy/` (3), `skills/tan/` (7), `skills/pocock/` (4) and `skills/benny/` (2). 49 files.
- Read every file of all 16 in full, including the four scripts.
- Wrote `skills/README.md` (sources, pinned commits, MIT licences) and `docs/analysis/skills-reading-notes.md` (safety read, assumptions we lack, one line each, findings).

Decisions:
- None approved by Boroon yet. "Read in full" is done. "Adopt" is not.
- Proposed only: nothing found that blocks adoption. Most skills need adapting (Cursor tools, Slack, Linear, Notion). `create-verification-skill` and `maintain-verification-skill` look like the template for `lcp-verify`. The Benny pair is the best built example of the outer loop.

Files changed:
- New: `skills/` (49 copied files plus `skills/README.md`), `docs/analysis/skills-reading-notes.md`
- Edited: `CLAUDE.md` (two rows added to the map), `docs/progress.md`

Open items:
- Which of the 16 to adopt, adapt or leave on the shelf (Boroon).
- Several of the 16 lean on skills we have not read: `unslop`, the `principle-*` skills, `poteto-mode`, `grilling`, `domain-modeling`. Decide if they are next.
- The Benny skills need a control adapter and a configured triage identity before they could run. Not buildable until `lcp-verify` and the ITSM tool are known.

Also done (later in Session 2): Boroon asked to adapt `ask-matt` into "ask-me". Written as `.claude/skills/ask-me/SKILL.md` (live, only runs when invoked). It routes by T-shirt size, day or night, and tags each skill live, shelf or planned. Credits Matt Pocock and the pinned commit. Not yet reviewed by Boroon. Tan, Pocock and Addy skills it names are still shelf, so it tells the user to adopt first or do the step by hand. Update its tags when a skill is adopted or an `lcp-*` skill is written.

Then (Session 2, third request): Boroon said "adopt the first five skills and adapt the rest". Read "first five" as the first five in the reading notes table. Done:
- Adopted unchanged into `.claude/skills/`: `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`, `create-verification-skill`, `maintain-verification-skill`.
- Adapted into `.claude/skills/`: `lcp-blast-radius`, `getai-decision-log`, `getai-correct`, `lcp-how`, `lcp-why`, `getai-intake` (from Pocock `triage`), `getai-wizard`, `getai-questionnaire`, `lcp-triage` (the two Benny skills merged, to match the `lcp-triage` agent in plan 4.5). `ask-me` was already adapted from `ask-matt`.
- `ask-me` tags updated. `skills/README.md` records what became of each skill. Shelf copies kept as pinned originals.
- Decisions made by me, for Boroon to confirm: `lcp-triage` has no fixing and no PR, because the plan has a human decide and rule 3 needs scenarios from someone else. Pocock `triage` became `getai-intake`, the human day step. Adopted skills were left unchanged as asked, so the two verification skills still write to `.cursor/skills/`.
- Nothing adapted has been run. The adopted five were read in full before adoption (rule 19) and pinned.

Open items added: review the nine `lcp-*` skills (rule 17 says reviewed daytime PR). The adopted constraint skill's examples are JavaScript, not Power Platform. `lcp-triage` needs the triage workflow, `lcp-verify` and a Test credential before it can run. Only `create-verification-skill` can build `lcp-verify`.

Then (Session 2, fourth request), decisions by Boroon:
- **Keep the fix and PR step out of `lcp-triage` for now.** It may move in later when trust is built (trust ladder, evidence first, only into `integration`).
- **The skills were reviewed by Boroon and merged** to the default branch `claude/jolly-albattani-818i8e` (there is no `main` yet) by PR 1 (https://github.com/boroonmahanta/overnight-ai-factory/pull/1). This clears the rule 17 review for the nine `lcp-*` skills and `ask-me` as written. They are still untested.
- Boroon asked whether the `lcp-*` skills could be reused under a different prefix. Answer and open question are below in Open items.

Open items added: naming of the reusable skills. Rule 18 and the naming table use `lcp` only for the Power Platform profile. A generic skill (decision log, questionnaire, correct, wizard, intake) is not Power Platform specific. Options were put to Boroon in chat. Not decided.

Then (Session 2, fifth request), decisions by Boroon:
- **Naming.** `pcp` means pro-code platform. Skills that work for any profile are `getai-*`. Skills tied to Power Platform stay `lcp-*`. Code-profile versions will be `pcp-*`. Boroon recalled agreeing `pcp` earlier, but no record of it exists in the repo or in this session, so it is recorded here as agreed now.
- **Renamed** (folder, frontmatter name and all references): `lcp-decision-log`, `lcp-questionnaire`, `lcp-correct`, `lcp-wizard`, `lcp-intake` became `getai-decision-log`, `getai-questionnaire`, `getai-correct`, `getai-wizard`, `getai-intake`. Still `lcp-*`: `lcp-blast-radius`, `lcp-how`, `lcp-why`, `lcp-triage`.
- **Not done:** no `pcp-*` skills written yet. Plan Appendix D has `Custom.LaneProfile` as code or lcp. Adopting `pcp` there is a plan edit, not made.

Then (Session 2, sixth request), decisions by Boroon:
- **Wrote the four pro-code skills:** `pcp-blast-radius`, `pcp-how`, `pcp-why`, `pcp-triage`. Same methods as the `lcp-*` versions, pointed at code repos (dependency and contract breakage, entry points and tests, git and runtime history, repo sandbox repro). `pcp-triage` has no fix or PR step, same as `lcp-triage`. Untested.
- **Plan edit:** `Custom.LaneProfile` picklist is now `pro-code, lcp` (Appendix D) and the ledger `fact_run.profile` is `pro-code, lcp` (section 10.1). Was `code, lcp`. Edited in `docs/sources/plan-v3.1.md`. The naming table in `CLAUDE.md` is updated.
- `ask-me` and `skills/README.md` updated to name the three prefixes.

Open items added: the plan has no triage workflow for code repos. `pcp-triage` is a proposal until Boroon decides the trigger, the runner and the credential. The `pcp-*` skills and the rename are not yet reviewed by Boroon (rule 17). Other plan text that says "code profile" in prose is unchanged. Only the field values changed.

Then (Session 2, seventh request), decisions by Boroon:
- **Code-repo reports come from** AutoTask tickets, PRTG alerts, ADO service hooks, service desk webhooks and manual runs by day. **Start with the manual run by day.** Nothing is automated until manual runs show what is worth it.
- `pcp-triage` now has a "Where reports come from" table and a "Running it by hand" section. The person strips names, emails, phone numbers and record IDs first, because the Function the plan relies on for this does not exist yet. PRTG alerts will often be reroutes (infrastructure, not code).
- Partly answers the open question on ITSM tools: AutoTask and PRTG are named for code repos. The Power Platform clients are still unknown. `CLAUDE.md` updated.

Open items added: how to export from AutoTask and PRTG for a manual run (nobody has said). Whether the plan's `triage-inbox` and `Custom.TriageSource` picklist (service desk, Teams, alert, ADO) should add AutoTask and PRTG as sources. Not changed.

Then (Session 2, eighth request), decisions by Boroon:
- **Reviewed and approved for merge:** the `getai-*` rename, the four `pcp-*` skills, the `Custom.LaneProfile` change to `pro-code`, and the manual-run change to `pcp-triage`. Merged into the default branch `claude/jolly-albattani-818i8e` by a second pull request. Rule 17 is met for every skill in `.claude/skills/`.
- All skills are reviewed but **none has been run**. Reviewed is not the same as tested.

Files changed this session, in total: `skills/` (shelf, 49 copied files plus README), `.claude/skills/` (5 adopted unchanged, `ask-me`, 5 `getai-*`, 4 `lcp-*`, 4 `pcp-*`), `docs/analysis/skills-reading-notes.md`, `docs/sources/plan-v3.1.md` (two lines, pro-code), `CLAUDE.md`, `docs/progress.md`.

Open items still waiting on Boroon: how to export reports from AutoTask and PRTG; whether `Custom.TriageSource` adds AutoTask and PRTG; a real `main` branch (the repo has none, the default is `claude/jolly-albattani-818i8e`); the next skills to read (`unslop`, `principle-*`, `poteto-mode`, `grilling`, `domain-modeling`); fixing the two verification skills so they write to `.claude/skills/` and `lcp-verify`.

Next steps:
1. Boroon reads `docs/analysis/skills-reading-notes.md` and picks adopt, adapt or shelf for each of the 16.
2. Write the GET AI router skill by size (tshirt-sizing step 3), then the first `lcp-*` skills.
3. Update the "Not yet approved" lines in `docs/analysis/tshirt-sizing.md` once Boroon decides.

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
