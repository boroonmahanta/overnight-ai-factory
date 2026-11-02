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

## Session 2, 2026-11-02, branch `claude/admiring-lovelace-jf49ez`

Done:
- Read in full the 16 skills of "batch 1", the first batch listed in `docs/analysis/tshirt-sizing.md` section 4, step 2. Read from fresh clones kept in scratch space only (not saved in the repo). Every file inside each skill folder was read, including references, scripts and templates.
- Commits read: `addyosmani/agent-skills` 301b02b, `mattpocock/skills` 4ae2317, `cursor/plugins` ae5650f (the same commits the comparison used).
- Addy Osmani: `constraint-driven-development` (with `references/floor-guard.md` and `scripts/quality-gate.mjs`), `doubt-driven-development`, `source-driven-development`.
- Lauren Tan (pstack): `create-verification-skill` (with its feature-map example), `maintain-verification-skill`, `blast-radius`, `show-me-your-work` (with `log.sh` and the TSV template), `correct`, `how` (with both prompts), `why` (with epistemics, investigator and synthesizer prompts, and all source playbooks).
- Matt Pocock: `triage` (with `AGENT-BRIEF.md` and `OUT-OF-SCOPE.md`), `wizard` (with `template.sh`), `to-questionnaire`, `ask-matt` (with `PHASE-BOUNDARIES.md`).
- Benny (Tan, under `pstack/automations/benny/skills`): `triage-issue-reports` and `reproduce-and-fix-issues`, with all their references.
- Not read: the `harness/pstack/claude-code/` copies of the Tan skills. They are near-identical variants (sizes differ by a few hundred bytes). Read the `pstack/skills/` originals only.

Decisions:
- None. Nothing is adopted. Plan rule 19 (read in full, then pin) is now met for batch 1, but pinning and adaptation are still open and need Boroon's go-ahead.

What the reading showed (for the later `lcp-*` rewrite, not decisions):
- Most useful for the gate: `constraint-driven-development` floor guard (diff scan for lowered thresholds, skipped tests, new suppressions, exit code 2 when it cannot run). Fits rule 11 (deterministic floor) and the "gate can raise, never lower" size rule. It is JavaScript and git based, so it needs an `lcp` version for solution files and flows.
- `create-verification-skill` and `maintain-verification-skill` give the shape for `lcp-verify`: Launch, Doctor, Drive, Evidence, Cleanup, plus a feature map with fixed headings. Its proof standard (real user path, evidence survives cleanup, never weaken a journey to pass) matches plan rules 2 to 4.
- `reproduce-and-fix-issues` needs a control adapter with seven capabilities, a symptom seen twice through the real UI, and before and after proof. Compare with plan section 4.5 (outer loop). It is Slack and Cursor specific, so only the pattern carries over.
- `triage-issue-reports` freezes source coordinates, posts one verdict, and fails closed on tickets. Useful for the outer loop. Slack specific.
- `triage` (Pocock) has the agent brief rules: describe behaviour not file paths, testable acceptance criteria, explicit out of scope. Close to what a Factory Eligible story needs.
- `blast-radius` and `doubt-driven-development` both say: prove the one fact it is safe because of, and send only artifact plus contract (never the claim) to the reviewer. Matches the fresh verifier sessions.
- `why` and `how` need many MCP sources (Linear, Notion, Slack, Datadog, Sentry, Databricks) and sub-agent model settings from a Cursor rule file. Heavy for GET AI. Likely adapt `how` only, or use ADO and git as the sources for `why`.
- `show-me-your-work` is a decision log in TSV. Overlaps plan section 7 traces and the ledger. Its cross-model review step needs a second model family.
- `wizard`, `to-questionnaire` and `ask-matt` fit day work (human-only steps, questions for a client, routing). `wizard` matches rule 8 (PARK on portal-only steps).
- `correct` turns repeated mistakes into architecture, types, lint, tests, then docs last. Fits rule 17 and `coding-standards.md`.
- `source-driven-development` says cite official docs only. Fits the Microsoft Learn rule for Power Platform work.
- Several skills call other skills not in batch 1 (`unslop`, `interview-me`, `grilling`, `domain-modeling`, `poteto-mode`, the `principle-*` skills). Those would need reading before the dependants are adopted.

Later in session 2 (Boroon's instructions, nothing built yet):
- Boroon asked for: a work-size field in ADO (Appendix D) on all work item types, rolling up programmatically to features and epics; a router skill that routes by size; and to adopt and adapt all 16 batch 1 skills ("every one of them is important", order does not matter).
- Boroon asked whether create-verification-skill and maintain-verification-skill apply to all lanes (Lane A, Lane B code, Lane B lcp). Answer given: yes. They are generators, so each lane gets its own verify skill: `lcp-verify` for Lane B lcp, one generated per repo for Lane B code, one for the Lane A app. Each has a builder copy and a trusted gate copy (rule 5). The upkeep skill runs weekly per lane, fixes by daytime PR only (rule 17). The name is `lcp`, never `pcp` or `pp`.
- Proposed design, awaiting Boroon's go-ahead:
  - ADO fields on Story, Task, Bug, Feature and Epic: `Custom.WorkSizeProposed` (spec owner, at intake), `Custom.WorkSizeGate` (gate only, can raise never lower), `Custom.WorkSize` (the larger of the two, the one everything reads). A parent gets `Custom.WorkSizeRollup` = largest child size, set by a service-hook-triggered job. The job goes into Appendix D as untested YAML.
  - Router skill `getai-size-router` (lane-neutral name). Input: size, lane, Merge Danger band. Output: skills to load, verifier count, human gate, refusal for XL (Wayfinder first). Routes live in `size-routes.yml` so changes are a reviewed PR. Modelled on `ask-matt` and `tshirt-sizing.md`.
  - Order: (1) read the skills the batch 1 skills call (`unslop`, `interview-me`, `grilling`, `domain-modeling`, `poteto-mode`, `tdd`, `pr`, the `principle-*` skills), (2) Appendix D, a sizing section in plan section 5, and `CLAUDE.md`, (3) pin the 16 originals with commit, licence and review note (rule 19), (4) write the adapted versions plus the per-lane verification generators, (5) write the router, (6) log. About three sessions.
- Confirmed with Boroon: the 16 were read in full. Caveats: the `harness/` copies of the Tan skills were not read; the dependants above were not read; `why`, `triage-issue-reports`, `reproduce-and-fix-issues` and `show-me-your-work` are tied to other tools, so only their patterns carry over.

Files changed:
- `docs/progress.md` only.

Open items:
- **Decision for Boroon:** where adapted skills live. Proposal: a top-level `skills/` folder that does not auto-load, keeping only `/bro` in `.claude/skills/`, because `.claude/skills/` loads descriptions into every session. Also still needs a go-ahead to start step 1.
- Batch 1 is read. The rest of the section 5 shortlist in `skills-comparison.md` is not.
- Still waiting on Boroon: which of the 16 to adapt first, the work-size ADO field, and the router skill.

Next steps:
1. Boroon confirms the skills folder location and says go.
2. Read the dependants named above before adopting anything that calls them.
3. Do the ADO field, plan section and `CLAUDE.md`, then pin, adapt and write the router, in the order above.

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
