# GET AI overnight software factory

This repo holds the plan and, later, the build of GET AI's overnight software factory.
Today it is documents only. There is no code yet.

This file loads at the start of every session. It is a map, not the full plan.
Keep it short. Detail lives in `docs/sources/`.

## How to start and end a session

Start:
1. Read this file.
2. Read `docs/progress.md`. It says what was decided, what changed and what is next.
3. Read only the part of `docs/sources/` the task needs (map below). Do not load every source.
   The sources total about 450 KB, or roughly 110K tokens. Sessions are kept under 200K tokens.

End:
1. Add an entry to `docs/progress.md`: decisions, files changed, open items, next steps.
2. If a decision changes this file, update this file too.
3. Commit and push to the session's working branch. Do not open a pull request unless asked.

## How Boroon likes to work

- Asked to "digest" a document: read all of it, do not summarise, reply with the single word "completed".
- Plain, short language. No jargon. The `/bro` skill restates the last message simply.
- Australian English. No em-dashes in prose.
- Work is spread over many short sessions on purpose. Never rely on chat memory. Write it down here.

## What is in the repo

| Path | What it is |
|---|---|
| `CLAUDE.md` | This map |
| `docs/progress.md` | Running log and next steps. Read second, update last |
| `docs/sources/plan-v3.1.md` | The main plan, "Lock the Gate, Pool the Lanes, Merge by Day", V3.1, 1 November 2026. 2,543 lines |
| `docs/sources/plan-v3.md` | The previous version, V3, 1 November 2026. 1,976 lines. Superseded by V3.1. Kept only to see what changed. V3 differs from V3.1 in: Wayfinder named the planning agent (now Story Planner); auto-merge framed as "Phase 4" (now the trust ladder L0 to L3); one evaluator per PR (now one to three verifiers); one review pass (now two); no `lcp-verify`, outer loop, gardening or prototypes; cost USD 11 per story and USD 144 accepted (now about 15 and 150); a Test queue of 30 minutes per PR (now about 36) |
| `docs/sources/uploaded-plan-software-factory.md` | Boroon's original plan (also as `.docx`). Part A: "End-to-End Specification: The GET AI Microsoft Software Factory". Part B: "Copilot Studio Agents & App Builds". 320 lines. Section 14.1 of the main plan lists every change made to it |
| `docs/sources/transcript-anthropic-agents-run-for-hours.md` | Anthropic workshop, "How to Build Agents That Run for Hours". 1,213 lines |
| `docs/sources/transcript-spec-kit-part-2.md` | GitHub, "Open Source Friday: Spec Kit Part 2", 16 October 2026. 1,159 lines |
| `docs/sources/transcript-tan-pocock-podcast.md` | Matt Pocock's podcast with Lauren Tan ("poteto"): trust ladder, verification, outer and inner loop, Michelin Kitchen. 1,238 lines. Cited in the plan as [Tan podcast mm:ss] |
| `docs/sources/transcript-pocock-skills-v1.3.md` | Matt Pocock on version 1.3 of his skills: implement spec, PR skill, glossary rename, retro. 796 lines. Cut off at 14:28, mid-sentence. Cited in the plan as [Pocock v1.3 mm:ss] |
| `docs/analysis/skills-comparison.md` | Our own analysis, 1 November 2026. Compares the skill packs of Addy Osmani, Matt Pocock and Lauren Tan: full list of every skill, overlaps, which fit GET AI, where they conflict with the 19 rules. Verdicts are proposals. 428 lines |
| `docs/analysis/tshirt-sizing.md` | Our own analysis, 1 November 2026. The T-shirt size approach (XS, S, M, L, XL) that sets ceremony by risk, mapped to the plan's Merge Danger bands and to the skills to use at each size. The sizes and the largest-answer rule were approved by Boroon on 1 November 2026. The skills per size and the next steps are still proposals. 52 lines |
| `docs/sources/transcript-skills-comparison-addy-pocock-tan.md` | A YouTube video comparing the three skill packs (https://www.youtube.com/watch?v=sU9MW8Ycq2M). Source for the effort-level idea behind the T-shirt sizes. 744 lines. Added 1 November 2026 |
| `docs/sources/transcript-pstack-skills-review.md` | A YouTube review of Lauren Tan's pstack skills (https://www.youtube.com/watch?v=lUhXa8GiXns; skills at https://github.com/cursor/plugins/tree/main/pstack). 769 lines. Not cited in the plan. Added 1 November 2026. Covers potato mode, arena, swarm, why, recall, interrogate, create and maintain verification, unslop and bro |
| `docs/sources/transcript-pocock-skills-v1.1.md` | Matt Pocock on version 1.1 of his skills: renames to spec and tickets, grilling fixes (facts versus decisions, confirmation gate), implement and code review (two axes, Fowler smells), Wayfinder, research, prototype, TDD at seams. 856 lines. Cited in the plan as [Pocock v1.1 mm:ss] |
| `docs/sources/research-notes/` | The original research notes behind the plan, saved verbatim. Each has takeaways, cited findings, inferences and gaps per question. Use them to check the evidence behind plan section 3. Top level holds the first research folder (24 October 2026): `anthropic_long_running_harnesses.md`, `evals_quality_gates_metrics.md`, `harness_engineering_practitioner_lessons.md`, `orchestration_patterns_durable_engines.md`, `runtime_options_and_costs.md`, `spec_driven_development_requirements.md` |
| `docs/sources/research-notes/github-azure/` | Eight GitHub and Azure notes (24 to 25 October 2026): cost ledger and FinOps, Azure infrastructure for agents, Copilot billing and partner benefits, Copilot coding agent and Agent HQ, Copilot primitives parity, GitHub Enterprise control plane, and notes on the Spec Kit and workshop transcripts. Not yet read in this project's sessions |
| `docs/sources/research-notes/power-platform/` | Five Power Platform notes (1 November 2026): `pp_alm_identity_environments.md`, `pp_testing_evaluation.md`, `pp_agent_tooling.md`, `review_of_uploaded_plan.md` (the review that produced the plan's corrections to the uploaded plan), and `v3_1_changes_from_transcripts.md` (the brief for the 15 V3.1 changes). Not yet read in this project's sessions |
| `docs/sources/report-v1-fund-nights-on-credits.md` | Earlier report V1, "Fund Nights on Credits, Price at List". The first GitHub and Azure version, before the two-lane design. Superseded |
| `docs/sources/report-v2-two-lanes-one-gate.md` | Earlier report V2, "Two Lanes, One Gate, Priced at List", before the Spec Kit layer was added in V2.1. Superseded |
| `docs/sources/workshop-slides/` | The five slides from the Anthropic workshop, as images 1 to 5. The plan cites a slide called "The simplified harness" |
| `docs/one-pager/` | The engineer one-pager for plan V3.1, as `GET-AI-Overnight-Factory-one-pager.html` and `single-page-artefact.md`. A short summary for GET AI engineers |
| `docs/sources/report-v2.1-two-lanes-one-gate.md` | Earlier report V2.1, "Two Lanes, One Gate, Priced at List". 925 lines. The GitHub and Azure design the main plan builds on: two lanes, harness parity, Spec Kit day gate, traces, credits, ledger schema, Lane A and B cost models, 8-stage plan. Still the best source for Lane A, ACA jobs, the ledger SQL schema and GitHub-side limits |
| `docs/sources/report-grill-the-spec-lock-the-tests.md` | The first report, "Grill the Spec, Lock the Tests". 195 lines. Original evidence base: what each harness resource teaches, the verifier-is-the-weak-point research, the grill gate, Claude Code facts, first design and stages |
| `.claude/skills/bro/SKILL.md` | The `/bro` skill |
| `.claude/skills/` | Live skills. `bro`. `ask-me` (router by size, adapted from `ask-matt`). Adopted unchanged: `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`, `create-verification-skill`, `maintain-verification-skill`. Adapted for GET AI, all untested: `lcp-blast-radius`, `getai-decision-log`, `getai-correct`, `lcp-how`, `lcp-why`, `getai-intake`, `getai-wizard`, `getai-questionnaire`, `getai-grilling`, `getai-domain-modeling`, `lcp-triage`. Also adopted 2 November 2026 with a GET AI note each: `unslop` and 21 `principle-*` skills (three conflicting ones stay on the shelf). Pro-code versions, all untested: `pcp-blast-radius`, `pcp-how`, `pcp-why`, `pcp-triage` (the plan has no code-repo triage workflow yet). Decided by Boroon on 2 November 2026. The two verification skills were then edited to write to `.claude/skills/lcp-verify/`. All of them reviewed by him and merged to the default branch (rule 17 met). Still untested |
| `skills/` | Third-party skills, the pinned originals of the first 16 (Addy 3, Tan 7, Pocock 4, Benny 2). A shelf: it does not auto-load, only `.claude/skills/` does. Provenance, commits and what became of each are in `skills/README.md` |
| `docs/analysis/skills-reading-notes.md` | Our notes from reading those 16: safety read, what each assumes that we lack, one line each with how to adapt, findings. Proposals only |
| `docs/analysis/skills-reading-notes-batch2.md` | Notes on batch 2, read 2 November 2026: `unslop`, the 24 `principle-*` skills, `grilling`, `domain-modeling` (shelved in `skills/tan/` and `skills/pocock/`; `grilling`, `domain-modeling`, `unslop` and 21 principles are live). Also `poteto-mode`, read in full except the `watch-pr` code (Cursor plugin, not harness agnostic, not adopted). Proposals only |

The main plan (V3.1) supersedes both earlier reports and V3. Read them for detail the plan condenses, not for current decisions. If they conflict, the main plan wins.

Timestamps in the plan's citations, such as [Tan podcast 16:21 to 16:53], match the leading timestamps in these transcript files. Search for the start time, for example `grep -n '^16:21' docs/sources/transcript-tan-pocock-podcast.md`.

Everything the plan cites is now in the repo. Boroon supplied the full research folder as a zip, and it was merged by checksum with no duplicates. See `docs/progress.md` for which files were saved but not yet read.

## Where to find what in the main plan

Line numbers are as at 1 November 2026. If the file has changed, run `grep -n '^## ' docs/sources/plan-v3.1.md`.
Read by line range, for example offset 378 and limit 200.

| Lines | Section |
|---|---|
| 1 to 29 | Bottom line and contents |
| 30 to 117 | 1. Naming rule, how to read, what changed (V3.1 against V3, V2.1 and the uploaded plan), key dates |
| 118 to 167 | 2. Operating model on one page: day phases, who owns what, the 19 rules |
| 168 to 305 | 3. What the research teaches, including what each transcript added |
| 306 to 377 | 4. Lanes and routing, the outer loop (triage), night and background workloads |
| 378 to 922 | 5. Lane B for Power Platform in depth: engine, identities, environment pool, night timeline, code over click-ops, the gate, locked scenarios, `lcp-verify`, Merge Danger and trust ladder, ADO state machine, agent instructions, throttling, licensing, promotion, residency |
| 923 to 1034 | 6. The day gate: Spec Kit presets, grilling rules, Factory Eligible, intake, Wayfinder maps, prototypes |
| 1035 to 1127 | 7. Handoff files, traces, weekly routine, gardening |
| 1128 to 1177 | 8. Harness parity, component register, third-party skills policy |
| 1178 to 1242 | 9. Credits, billing modes, model choice, data residency tiers |
| 1243 to 1363 | 10. Cost ledger, story cost model, cost envelope |
| 1364 to 1406 | 11. Staged build plan, stage 0 spikes |
| 1407 to 1443 | 12. Risks, most serious first (32) |
| 1444 to 1459 | 13. Accelerator and IP |
| 1460 to 1521 | 14. Decision log |
| 1522 to 1559 | 15. Open questions and evidence quality |
| 1560 to 2058 | Appendix A: gate workflow YAML (untested) |
| 2059 to 2196 | Appendix B: Merge Danger rubric, verifier count, `trust.yml` |
| 2197 to 2468 | Appendix C: agent definitions, `AGENTS.md`, `lcp-verify` skill, PR body template |
| 2469 to 2524 | Appendix D: ADO fields and states |
| 2525 to 2543 | Appendix E: sources used |

The two transcripts are already digested in plan sections 3.5 (workshop) and 3.6 (Spec Kit). Read the full text only when quoting.

## The plan in brief

Build the Power Platform profile of "Lane B" first. By day, humans shape a high-level spec on Spec Kit 1.2.
Someone other than the builder writes and locks the acceptance scenarios. A human then sets "Factory Eligible" in Azure DevOps (ADO).
At night, Copilot CLI runs headless on a GitHub Actions runner in Australia, one story per lane, across three long-lived Sandbox environments that are Managed Environments.
A required workflow in a separate gate repo runs only trusted checks, imports each PR into a Test environment the builder cannot touch,
runs locked and held-out scenarios, then one to three fresh verifier sessions click through the app.
A deterministic Merge Danger score is computed for every PR. An AI reviewer may raise it, never lower it.
Humans merge in the morning. `main` is always human.
Auto-merge is a rung on a trust ladder (L0 to L3), earned per change class on evidence, only into the `integration` branch.

Lanes:
- **Lane A**: greenfield and feature-sized code builds. One long Copilot SDK session.
- **Lane B, code profile**: issue-sized changes in existing code, via the cloud agent.
- **Lane B, Power Platform profile** (focus): story-sized changes to Power Platform solutions, via Copilot CLI on a runner.
- **Day work**: canvas app authoring, new-harness Copilot Studio agents, environment creation, anything needing an admin login.

New in V3.1: `lcp-verify` (verification skill and CLI the builder uses in its own loop), an outer loop that triages AI Managed Services client reports,
Wayfinder discovery maps, overnight research tickets, gardening scans that feed a findings list instead of PRs, and a human-led weekly retro on real sessions.

## The 19 rules we do not break

1. Humans own intent, spec approval and every merge to `main`. No agent or App merges to `main`.
2. The worker never decides it is done. The gate and an isolated evaluator decide.
3. Acceptance scenarios come from someone other than the worker, locked before the night.
4. A held-out set lives where the worker cannot read it. Only aggregate results return.
5. Credentials and untrusted code never share a job.
6. Four identity roles: execute, verify, review, merge. Per-lane identities. None in any bypass list.
7. One story, one lane, one branch, one PR. A lane runs one story at a time under a lock.
8. Code over click-ops. A step needing the portal or interactive consent PARKs.
9. Facts are looked up; decisions are asked. Clarify by day only. Night agents PARK on decisions.
10. Design first. User-facing changes need an approved mock or throwaway prototype. Prototypes are never promoted.
11. The Merge Danger floor is deterministic. An LLM may raise the score, never lower it.
12. Auto-merge is a rung, not a phase. Only into `integration`, per change class, on evidence. An escaped defect drops the class to L1. Never on a date.
13. Every run has a `run_id`, a credit cap and an iteration cap. Every cost goes in the ledger at list and cash.
14. Price from the list column, never from credits.
15. Client code and data follow the client's residency tier. No client production data in factory lanes.
16. Every transcript, trace and evidence file reaches Blob within the night, tagged with `run_id`.
17. Prompts, rubrics, agents, skills, hooks, gate scripts, `lcp-verify`, `glossary.md`, decision records and coding standards change only by a reviewed daytime PR.
18. Machine-readable names stay product-neutral.
19. Read every third-party skill in full before adoption, then pin it.

## Naming rule

"Power Platform" is today's name and Microsoft is expected to rename it (Ignite, 17 to 20 November 2026). Prose may use product names. Machine-read names may not.

| Thing | Use | Never |
|---|---|---|
| Lane profile | `lcp` (low-code platform), `profile:lcp` | `pp`, `powerplatform` |
| Environments | `factory-lane-1` to `-3`, `factory-test` | `pp-dev-1` |
| Lane codes | `fl1`, `fl2`, `fl3` | |
| Entra apps | `getai-fl1-exec`, `getai-fl1-verify`, `getai-<proj>-test`, `getai-<proj>-deploy` | `ppf-lane1-exec` |
| Labels | `lane:fl1`, `profile:lcp`, `factory=enabled` | |
| Gate files | `factory-gates/.github/workflows/lcp-gate.yml`, `gate/lcp/*` | |
| Spec Kit preset | `getai-lcp` | |
| Pro-code profile (agreed 2 November 2026, edited into plan Appendix D) | `pcp` (pro-code platform), `profile:pcp`, skills `pcp-*`. ADO field `Custom.LaneProfile = pro-code` | `code` as a field value, `code` in skill names |
| Skills that work for any profile | `getai-*` | `lcp-` or `pcp-` on a general skill |
| ADO | tag `factory-eligible`, field `Custom.LaneProfile = lcp` or `pro-code` | |

## Terms

- **Wayfinder**: Matt Pocock's discovery map for foggy work, held in ADO. The planning agent from the uploaded plan is now the **Story Planner**. Boroon chose this on 1 November 2026.
- **Chief of Staff**: dropped as a custom orchestrator. The function survives as grouping steps in triage and the 17:00 night plan.
- **Merge Danger**: score 0 to 10. Bands: 0 to 2 low, 3 to 5 medium, 6 to 10 high. Includes one-way versus two-way door and blast radius.
- **PARK**: the agent stops at a portal-only step or a decision, writes `park.json`, and the story waits in ADO state "Awaiting business".
- **Factory Eligible**: ADO flag a human sets once the spec, locked scenarios, held-out set, mocks and prerequisites exist.
- **Trust ladder**: L0 humans run agents by day. L1 night shift, human approves every PR. L2 auto-merge for eligible classes at score 0 to 2, with a review sample. L3 named score-3 classes (untested).
- **`lcp-verify`**: skill plus CLI with commands `app`, `query`, `flow`, `agent`, `smoke`. The builder uses a lane copy. The gate uses a trusted copy.
- **Michelin Kitchen**: the uploaded plan's metaphor. Humans are executive chefs reviewing agent sous-chefs.
- **Evidence markers in the plan**: no marker means read in full. `[secondary]`, `[snippet]`, `[inference]`, `[untested]`, `[unverified]`, `[user-supplied transcript]`.

## Work sizes (approved 1 November 2026)

Ceremony matches the stakes. Detail and the skills per size are in `docs/analysis/tshirt-sizing.md`.

| Size | Looks like | Merge Danger floor |
|---|---|---|
| XS | Wording, label, colour or view-column tweak. No logic | 0 to 1 |
| S | One additive change in one app or flow. Clear outcome | 0 to 2 |
| M | Flow logic, Copilot Studio topic or tool, shared table, new connection reference, any user-facing UI | 3 to 5 |
| L | One-way door: dropped data, security role, money logic, deploy settings | 6 to 10 |
| XL | Too big or foggy for one session. Wayfinder map first, then split into S, M and L stories | Each child story gets its own |

The size is the largest answer across reversibility, blast radius, clarity, verifiability, effort, and residency. It is not an average. The spec owner proposes it at intake. The gate can raise it, never lower it.

## Dates that force action

| Date | Event |
|---|---|
| April 2026 | Power Apps Test Engine deprecated. Use Playwright only |
| 10 November 2026 | Durable Functions in-process support ends |
| 15 November 2026 | No new unmanaged developer environments. Lanes must be Sandbox plus Managed |
| 17 to 20 November 2026 | Microsoft Ignite. Re-check names, Copilot Studio evaluation APIs, Git integration |
| 30 November and 11 December 2026 | Power Apps Vibe and App Builder close, and some AI features end |
| 15 December 2026 | Existing unmanaged developer environments suspended |
| 15 January 2027 | Unmanaged developer environments deleted |
| February 2027 | Stricter premium licence enforcement for Managed Environments |

## Biggest risks

1. **Credits may not fund client work.** Partner credits are "internal-use-rights". Run client work at cash until Microsoft answers in writing (spike 0.1).
2. Auto-merge letting soft test gaming through. Answer: deterministic floor, rungs earned on evidence.
3. Unmanaged developer environments retiring (dates above).
4. Client code leaving Australia for inference. Copilot residency covers only the US and EU. BYOK to Azure OpenAI in Australia East is the only in-country path found. Each client gets a tier T1 to T4.
5. Whether `pac auth --githubFederated` works on GHE.com. Untested. First spike (0.2).

The full list of 32 is in plan section 12.

## Cost, as modelled (not measured)

- About USD 11.82 per attempt and USD 15 per story in AI credits and compute at list.
- About USD 150 per accepted story fully loaded. Human minutes are about 80% of that.
- Evaluator quality and review minutes move margin far more than token price.
- One partner designation funds about 1.3 Power Platform lanes at three stories a night. Three lanes need a specialisation or cash.

## Build plan

The 45 days build the factory. They move no project up a trust rung. Do not start a stage until the one before passes its exit test.

| Stage | Days | What |
|---|---|---|
| 0 | 1 to 14 | 17 spikes and the money question (credit ruling, OIDC with pac on GHE.com, MCP, `pac copilot`, cloud agent limits, billing, environment audit and more) |
| 1 | 1 to 14 | Safety net: gate repo as required workflow, rulesets, Test environment, Spec Kit presets, humans keep using the AI by day |
| 2 | 15 to 21 | ADO automation, `lcp-verify` v0, ledger v0 |
| 3 | 22 to 30 | Night shift, one lane, rung L1 |
| 4 | 31 to 45 | Three lanes, calibration, held-out set, gardening |
| 5 | 46 to 70 | Lane B for code repos |
| 6 | 60 to 90 | Lane A |
| 7 | about day 75 earliest | Rung L2 per change class, on evidence |
| 8 | ongoing | Scale, bake-offs, accelerator |

## Open questions (owner)

- Can partner credits fund client delivery? (Boroon, spike 0.1)
- Does `pac --githubFederated` work on GHE.com and in ruleset workflows? (Platform team, spike 0.2)
- Which Copilot features work on GHE.com, and which billing identity for the CLI? (Platform team and Boroon, spike 0.6)
- Does Dataverse MCP accept an app-only token? (spike 0.3)
- Lanes in the client's tenant or ours, per client? (Boroon)
- Power Platform licence, capacity and meter prices in AUD. (Commercial)
- What did GitHub Universe and Ignite change? Is there a rename? (Boroon)
- Which ITSM tools do AI Managed Services clients use? (AI Managed Services). For code repos so far: AutoTask tickets and PRTG alerts (read through their APIs or an MCP server, not built), ADO service hooks and service desk webhooks. Power Platform clients not yet known
- Which change classes go in `trust.yml`, and is a 20% random sample at L2 right? (Boroon)

The full list is in plan section 15.1.
