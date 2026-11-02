# Reading notes: batch 2 (27 skills)

Date: 2 November 2026. Status: notes from reading, so every verdict is a proposal until Boroon approves it.

What was read, in full: `unslop` (1 file), the 24 `principle-*` skills (1 file each) from `cursor/plugins` `pstack/skills/` at commit `ae5650febf4320793844c12c4adaa937f417f8da`, and `grilling` (2 files) and `domain-modeling` (4 files) from `mattpocock/skills` at commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`. Both commits are the same pins as batch 1. Copies are unchanged on the shelf (`skills/tan/`, `skills/pocock/`).

**Not read:** `poteto-mode`. Boroon asked to discuss it first. See the last section.

Companion: `skills-reading-notes.md` (batch 1).

## Safety read (rule 19)

- All 27 are plain text. No scripts, no network calls, no instructions aimed at anything outside the skill's job.
- All 25 pstack skills are `disable-model-invocation`, so they run only when someone calls them. `grilling` and `domain-modeling` can be picked up by the model from their descriptions.
- Verdict: nothing blocks adoption. Pinning is in `skills/README.md`.

## Things to know before adopting

1. **The `principle-*` skills link to each other by relative path** (`../principle-build-the-lever/SKILL.md`). Adopt them together into `.claude/skills/` so the links hold, or the links break.
2. **Five are fragments.** `exhaust-the-design-space` (one sentence), `migrate-callers-then-delete-legacy-apis` (three bullets, the first is mid-thought), `guard-the-context-window` (one bullet), `laziness-protocol` (two bullets) and `encode-lessons-in-structure` (two lines) look trimmed upstream. The description line carries most of the meaning.
3. **Dangling references.** `explain-the-number` points at `benchmark-checklist`. `type-system-discipline` points at `typescript-best-practices`. Neither was read. The `prove-it-works` and `sequence-verifiable-units` skills name `show-me-your-work`, which we adapted as `getai-decision-log`.
4. **Wording.** `unslop` and the principles use words the plan also uses as technical terms (harness, surface). `unslop` rule 26 targets the metaphor use only.

## Two conflicts with the plan (need a decision)

1. **`domain-modeling` against `glossary.md`.**
   - The skill says `GLOSSARY.md` must be "totally devoid of implementation details". The plan (6.2) wants each term mapped to its Dataverse table and column, flow and app names.
   - The skill writes `GLOSSARY.md` and `GLOSSARY-MAP.md` in capitals. The plan's protected-paths pattern in Appendix A matches lowercase `glossary\.md`. A capitalised file would sit outside the protected list, so an agent could edit it. This is a real hole if the skill is adopted unchanged.
   - Fix when adapting: lowercase names, a "schema name" line per term, and keep `docs/adr/` (it already matches).
2. **`grilling` against the plan's grilling rules.**
   - Plan 6.2 says "one question at a time", taken from Pocock v1.1. The pinned skill now asks the whole **frontier** in rounds, numbered, each with a recommended answer, and sends sub-agents to find facts.
   - Facts versus decisions and the confirmation gate are the same in both. Only the batching differs.
   - Decision for Boroon: keep one at a time, or move to rounds. Do not edit plan 6.2 until decided.

## One line on each

| Skill | What it does | Fit | Adapt how |
|---|---|---|---|
| `unslop` | 33 numbered rules to cut AI tells from writing. No em dashes, plain words, active voice, no mannered prose | Strong. Matches how Boroon writes (CLAUDE.md: plain, no em dashes) and the `/bro` skill | Add Australian English. Adopt as is otherwise. Day use, and for the PR body and `triage.json` text |
| `grilling` | Interview by design tree, a round at a time, facts looked up not asked, stop only when the frontier is empty and the user confirms | Strong. It is the source of the plan's grilling rules and of rule 9 | Decide rounds or one at a time (above). Say it never runs at night. Name the Spec Kit clarify step it feeds |
| `domain-modeling` | Challenges terms, tests them with scenarios, keeps a glossary and short ADRs. ADR only when hard to reverse, surprising and a real trade-off | Strong. Same job as the plan's glossary and decision records | The conflict above. Keep the three-test rule for ADRs |
| `principle-attack-the-premise` | After two failed fixes with one shared premise, write the premise down and test it | Strong. Fits the iteration cap and the PARK rule: two same-premise failures should PARK | Add to the builder rules and to `getai-correct` |
| `principle-boundary-discipline` | Validate at system boundaries, trust inside, keep logic in pure functions | Good for pro-code. Weak for flows | Pro-code only |
| `principle-build-the-lever` | Build the script that does or proves the work | Strong. Close to `lcp-verify` and to "code over click-ops" (rule 8) | Keep. Add a Power Platform example: a script that exports and diffs the solution |
| `principle-encode-lessons-in-structure` | A repeated instruction becomes a lint, flag or script | Strong. Same as the retro rule and rule 17 | Keep. Output is a reviewed PR |
| `principle-exhaust-the-design-space` | Two or three competing prototypes before a novel design | Good. Fits rule 10 (design first, throwaway prototypes, never promoted) | Fragment. Add the "never promoted" line |
| `principle-experience-first` | Choose user delight over implementation ease | Good for any user-facing change (size M) | Keep. Pair with rule 10 |
| `principle-explain-the-number` | Before trusting a measured number, find what limits it and what else it could be measuring | Strong. Applies to the cost model, verifier pass rates and the stage 4 calibration | Add: a pass rate is a number too. Needs `benchmark-checklist` for performance numbers |
| `principle-fix-root-causes` | Trace the symptom to the first wrong decision; a guard hides a bug when the state is illegitimate | Strong. Feeds `lcp-triage`, `pcp-triage` and `lcp-why` | Keep |
| `principle-foundational-thinking` | Data shapes first, scaffold first, isolate concurrent state | Good for pro-code. For lcp it means Dataverse schema first | Add the schema-first line |
| `principle-guard-the-context-window` | Cap scope per phase to protect the context | Weak as written (one bullet). Idea matches our short sessions | Fragment. Fold into a `CLAUDE.md` line instead |
| `principle-laziness-protocol` | One source of truth, smallest diff | Good for pro-code | Keep for `pcp` |
| `principle-make-operations-idempotent` | Every step converges from any partial state; stale markers must be recognisable | Strong. Fits the lane lock, retries, import to Test and the `run_id` rule | Keep. Add: solution import and ADO transitions |
| `principle-migrate-callers-then-delete-legacy-apis` | Change callers and delete the old API in one wave | Weak. Says it needs "no external users", and clients are external | Leave on the shelf |
| `principle-minimize-reader-load` | Count layers and hidden state a reader must hold | Good for the standards reviewer pass and pro-code | Keep for `pcp` |
| `principle-model-the-domain` | Use a state machine or typed model, not scattered conditionals | Good for pro-code, and for ADO states and Dataverse choice columns | Keep |
| `principle-never-block-on-the-human` | Proceed on reversible work; do not ask "should I?" | **Conflicts with rule 9** at night. Night agents PARK on decisions. It is right for reversible edits, wrong for decisions | Shelf, or adapt: proceed on reversible steps, PARK on decisions and on anything rule 8 covers |
| `principle-outcome-oriented-execution` | Planned breakage between phases is fine if reversible | **Conflicts with one story, one PR, one gate** unless the whole migration is one story. Fine for a planned code migration by day | Shelf. Revisit for XL work |
| `principle-prove-it-works` | Check the real artifact, not a proxy or self-report | Strong. Same as rule 2 | Keep. Add: verifier reads the Test environment, not the builder's claim |
| `principle-redesign-from-first-principles` | Fold a new requirement into the design as if it had always been there | Good for spec changes by day | Keep |
| `principle-separate-before-serializing-shared-state` | Remove shared writes before adding locks | Strong. Backs rule 7 and the environment pool; lock only where one writer is a real invariant | Keep. Cite when designing the lane lock |
| `principle-sequence-verifiable-units` | Small units, each checked before the next; failing test first, then fix | Strong. Fits the PR evidence order and `getai-decision-log` | Keep |
| `principle-subtract-before-you-add` | Remove first, then build | Mixed. In a client solution, deleting a component can be a one-way door (size L) | Adapt: removal in a managed solution is scored as L until proven otherwise |
| `principle-test-behavior-not-implementation` | A test must fail when behaviour breaks and survive a refactor | Strong. Good bar for locked scenarios and the verifier rubric (Appendix B) | Keep. Link from `getai-questionnaire` and the rubric |
| `principle-type-system-discipline` | Brand primitives, parse at the boundary, derive from schema | Pro-code only. TypeScript flavoured | `pcp` only; needs `typescript-best-practices` |

## Findings

1. **Best new fits:** `grilling`, `domain-modeling` (after the fixes above), `unslop`, and the principles `attack-the-premise`, `make-operations-idempotent`, `separate-before-serializing-shared-state`, `prove-it-works`, `test-behavior-not-implementation`, `explain-the-number`, `build-the-lever`, `fix-root-causes`, `encode-lessons-in-structure`, `sequence-verifiable-units`.
2. **Do not adopt as written:** `never-block-on-the-human` and `outcome-oriented-execution` (conflict with rules 9 and 7), `migrate-callers-then-delete-legacy-apis` (assumes no external users).
3. **Pro-code only (`pcp`):** `boundary-discipline`, `foundational-thinking`, `laziness-protocol`, `minimize-reader-load`, `model-the-domain`, `type-system-discipline`.
4. **The glossary case is a real defect** if `domain-modeling` is adopted unchanged: capitalised names miss the protected paths.

## Decisions by Boroon (2 November 2026)

1. Glossary files are lowercase (`glossary.md`, `glossary-map.md`). Done in `getai-domain-modeling`.
2. Grilling asks at most five questions a round, most blocking first, the rest held. Done in `getai-grilling`, and plan 6.2 now says so.
3. `principle-never-block-on-the-human`, `principle-outcome-oriented-execution` and `principle-migrate-callers-then-delete-legacy-apis` stay on the shelf. Revisit when an issue calls for them. Cases to watch: a night agent stalling on a reversible choice (the first), a planned multi-phase migration or XL work (the second), an internal-only API change (the third).

## `poteto-mode`, read 2 November 2026

**What was read.** `SKILL.md` (150 lines), all 22 playbooks, `references/bugbot-triage.md`, `bootstrap.ts`, `package.json`, the start of `check-plan.mjs` and `worktree-audit.sh`, and a search of the `watch-pr` TypeScript for network, shell and path use. **Not read line by line:** the `watch-pr` code and its tests (about 3,800 lines). Read them before any adoption (rule 19). The agent file `agents/poteto-agent.md` and the plugin readme and Claude Code adapter (`docs/harness/claude-code.md`) were also read.

**What it is.** A style and router skill for Lauren Tan's pstack plugin. It sends the agent through 22 playbooks (feature, bug fix, babysit, shipping, autopilot, orchestrate and so on) and a 24-principle index. Autopilot and orchestrate run a fleet of owner and verifier subagents, a one-hour audit loop and (in Autopilot-full) merge PRs.

**Is it harness agnostic? No.** It is a Cursor plugin first.
- Cursor-only names throughout: `Task`, `AskQuestion`, `cursor-team-kit` skills (`control-ui`, `control-cli`, `deslop`), Bugbot, Cursor cloud agents and Automations, Origin (`origin pr`), `/loop`, `.cursor/` paths, and model slugs such as `grok-4.7-xhigh-fast`.
- **Claude Code is supported, with a translation layer.** The plugin ships an official adapter and a generated Claude Code copy (`.claude-plugin`, `harness/pstack/claude-code`). The adapter maps `Task` to `Agent`, `AskQuestion` to `AskUserQuestion`, cloud agents to worktrees, Cursor paths to `.claude/`, and skips Cursor-only steps with a one-line note. So it runs in Claude Code with gaps, and the Cursor skills it names (`control-ui`, `deslop`) stay missing.
- **GitHub Copilot and VS Code: no support found.** A search of pstack for Copilot, VS Code and Codex found nothing. The plan (section 8, line 858) says Copilot CLI reads skills from `.github/skills`, `.claude/skills` or `.agents/skills`, so the `SKILL.md` text would load. The machinery would not: the `poteto-agent` file is a Cursor agent file, not a Copilot `.agent.md`; the per-role model and effort choices, background subagents, `/loop` and the ten-lane swarm have no tested Copilot equivalent. Not tested by us.
- The scripts are portable. `watch-pr` needs Bun and the `gh` CLI (GitHub.com; GHE.com untested). `check-plan.mjs` needs Node. `worktree-audit.sh` reads Cursor transcript folders.

**Safety read.** No hidden network calls found. `watch-pr` shells out to `gh` only. `bootstrap.ts` runs `bun install --frozen-lockfile`, which pulls `commander` 14.0.0 from npm. The dev dependencies `bun-types` and `typescript` are set to `latest`, though the lockfile pins them. `worktree-audit.sh` is read-only. The worktree-cleanup playbook deletes worktrees by hand-run commands, behind its own gates.

**Conflicts with the 19 rules.**
- **Rule 1 and rule 12.** Autopilot-full has owner agents merge PRs. We merge to `main` by human only, and auto-merge only into `integration` by trust rung.
- **Rule 9.** "Never block on the human" and "Under a full-autonomy grant, decide and report" cut across PARK on decisions.
- **Rule 6.** "Just do it. Use any MCP tool... external actions (ticket updates, team chat)" would let an agent write ADO and chat. Plan 4.5 says no agent writes ADO.
- **Rule 2.** The root agent that "owns the verdict" is the same session that spawned the builders. Our gate is a separate required workflow in another repo.
- **Rule 17.** It tells the agent to fix a broken skill "in its own PR, don't block". Skills change only by reviewed daytime PR, which a PR does satisfy, but an agent must never write to protected paths at night.

**Verdict (proposal).** Do not adopt. It is a human's interactive style for Cursor, and its engine (fleet, loops, merge) is what our gate replaces. The pieces worth keeping are small and already ours or cheap to lift:
- The opener: say the goal, the problem and the smallest change before starting. Could go in `ask-me` or the day skills.
- The rule that every claim carries its evidence or label (measured, inferred, guess). Matches the plan's evidence markers.
- The "classify the question" test before asking a human: if running something answers it, run it. Matches rule 9.
- The `bugbot-triage` fix, dismiss, ask rubric and its "ask by default" list (security, data, migration, concurrency). A good seed for the standards reviewer pass. It is for Bugbot, which we do not have, but Copilot code review comments are similar.
- The 22 playbooks as a pattern for naming a step list per task type. Our T-shirt sizes already do this job.
- `perf-issue`'s seven mantras (don't do it, don't repeat it, do it less, later, unseen, concurrently, cheaper) are a handy cost-control order for the cost envelope.

The shelf copy is at `skills/tan/poteto-mode/`. Copied, not adopted.
