# GET AI overnight software factory

This repo holds the plan and the start of the build of GET AI's overnight software factory.
Mostly documents. The first code, the gate, lives in its own repo `GetAI-IP/factory-gates` on `getai.ghe.com` (stage 1: slice 1 and Builds 1 to 3; moved out of this repo 3 November 2026; tested, not yet run as a gate or on a tenant).
**Where things live (Boroon, 4 November 2026):** this planning repo stays on github.com, `boroonmahanta/overnight-ai-factory`, for good. Only the workflows and the automation Apps go on `getai.ghe.com`: the gate, the held-out tests, the caller repos and the GitHub Apps. **The day-gate files go there too (D1, Boroon, 7 November 2026):** presets, templates and scenario rules to `GetAI-IP/factory-manifestos` (private), the spec check and the Playwright kit to `factory-gates`. Until Friday 4 December 2026 they are drafted in `staging/` here. The low-code coding standards are only on GHE: `GetAI-IP/factory-manifestos` (created 13 November 2026, ruleset `main-protection` with 0 approvals until a second approver), `practices/lcp/coding-standards.md`, 50 standards with the vault's four client-token ones kept (Boroon, 13 November 2026; `docs/plans/stage-1-day-gate-plan.md`). This repo is public (checked 4 November 2026); whether to make it private is open (`docs/progress.md`). **ADO (Boroon, 7 November 2026):** GET AI's Azure DevOps (`getai` organisation) holds Kanban boards only, one project per engagement on the process "Agile build v1", plus one internal project for the factory's own build; repos stay on GET AI's GitHub Enterprise, with pipelines and tests on GitHub Actions (plan 6.4). **The internal project is `getai-overnight-ai-factory`** (created 7 November 2026, private, boards only): Epics per stage 0 to 9 plus "Planning, research and skills", with past work as Done and future work as Proposed, tagged `factory-build` and `seeded-2026-11-07`. Spikes are User Stories tagged `spike` (the process has no Spike type).

This file loads at the start of every session. It is a map, not the full plan.
Keep it short. Detail lives in `docs/sources/`.

## How to start and end a session

Start:
1. Read this file.
2. Read `docs/progress.md`. It says what was decided, what changed and what is next. `docs/plans/schedule.md` says which story is next and its target date.
3. Read only the part of `docs/sources/` the task needs (map below). Do not load every source.
   The sources total about 450 KB, or roughly 110K tokens. Sessions are kept under 200K tokens.

End:
1. Add an entry to `docs/progress.md`: decisions, files changed, open items, next steps.
2. If a decision changes this file, update this file too.
3. Record the session's time and tokens (Boroon, 7 November 2026). Run `python3 -I tools/session_usage.py --latest` (or `--session <id prefixes>` to add forks and side sessions), and add its last line to the body of the session's stories in the ADO project `getai-overnight-ai-factory`. Cloud sessions have no local transcript; say so instead.
4. Commit and push to the session's working branch. Do not open a pull request unless asked.
5. `main` is the default branch and is protected by a ruleset. Start session branches from `main`. Merge into `main` only by pull request (rule 1). **Boroon merges every pull request into `main` himself, by hand (decided 2 November 2026). Open the pull request and stop. Do not merge it, even if asked to in passing, unless he says so in that moment.**

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
| `docs/sources/plan-v3.1.md` | The main plan, "Lock the Gate, Pool the Lanes, Merge by Day", V3.1, 1 November 2026. 2,722 lines. Edited in place since, each time at Boroon's word; the largest edit is live build in lane B (low-code), 7 November 2026 (Session 15). Session 16 added time and tokens per story on every engine (rule 13, 10.1 to 10.3, spike 0.20, Appendix D). Session 17 added the day-gate decisions D1 to D6 (6.1, 5.8, 5.12, 11.2, 14.4), including the Spec Kit pin, now 1.3.x. Session 19 made the XML layout the low-code lane's solution source after spike 0.18 (5.6, 8.1, 11.1, risk 12, 14.4, Appendices A, B.1 and C). Session 20 edited the reset for spike 0.19: how leftovers are found, the bootstrap list, the rule that a table or column outside the solution stops the lane for a person (ADO 2843), byte equality, the whole-tree manifest check (5.4, 5.6, 11.1, risk 17, 14.4, 15.1). Session 22 edited it for Dataverse MCP billing after ADO 2433: 0.1 Copilot Credit a call, from the tenant's prepaid pool, capped per session by a call count in the driver, with three retries on a failed call and a PARK on either stop, and MCP costed per run in the ledger (5.6, 5.11, 5.14, 10.2, 10.5, 14.4, 15.1) |
| `docs/sources/plan-v3.md` | The previous version, V3, 1 November 2026. 1,976 lines. Superseded by V3.1. Kept only to see what changed. V3 differs from V3.1 in: Wayfinder named the planning agent (now Story Planner); auto-merge framed as "Phase 4" (now the trust ladder L0 to L3); one evaluator per PR (now one to three verifiers); one review pass (now two); no `lcp-verify`, outer loop, gardening or prototypes; cost USD 11 per story and USD 144 accepted (now about 15 and 150); a Test queue of 30 minutes per PR (now about 36) |
| `docs/sources/uploaded-plan-software-factory.md` | Boroon's original plan (also as `.docx`). Part A: "End-to-End Specification: The GET AI Microsoft Software Factory". Part B: "Copilot Studio Agents & App Builds". 320 lines. Section 14.1 of the main plan lists every change made to it |
| `docs/sources/transcript-anthropic-agents-run-for-hours.md` | Anthropic workshop, "How to Build Agents That Run for Hours". 1,213 lines |
| `docs/sources/transcript-spec-kit-part-2.md` | GitHub, "Open Source Friday: Spec Kit Part 2", 16 October 2026. 1,159 lines |
| `docs/sources/transcript-tan-pocock-podcast.md` | Matt Pocock's podcast with Lauren Tan ("poteto"): trust ladder, verification, outer and inner loop, Michelin Kitchen. 1,238 lines. Cited in the plan as [Tan podcast mm:ss] |
| `docs/sources/transcript-pocock-skills-v1.3.md` | Matt Pocock on version 1.3 of his skills: implement spec, PR skill, glossary rename, retro. 796 lines. Cut off at 14:28, mid-sentence. Cited in the plan as [Pocock v1.3 mm:ss] |
| `docs/analysis/skills-comparison.md` | Our own analysis, 1 November 2026. Compares the skill packs of Addy Osmani, Matt Pocock and Lauren Tan: full list of every skill, overlaps, which fit GET AI, where they conflict with the 19 rules. Verdicts are proposals. 428 lines |
| `docs/analysis/tshirt-sizing.md` | Our own analysis, 1 November 2026. The T-shirt size approach (XS, S, M, L, XL) that sets ceremony by risk, mapped to the plan's Merge Danger bands and to the skills to use at each size. The sizes and the largest-answer rule were approved by Boroon on 1 November 2026, and the ADO field `Custom.WorkSize` on 7 November 2026 (plan Appendix D). The skills per size and the other next steps are still proposals |
| `docs/analysis/delivery-vault-fast-track.md` | Our own analysis, 6 November 2026 (Session 13). What lane 1 can take from a lane 1 engineer's delivery vault (a day-time kit: four skills, operating rules, design and handoff templates) and from a call with its author, combined with `factory-lane-1`: a mapping to plan stages, five fast-track steps, a pilot scoped to work with no client connections, and five differences to settle (chiefly: build live then export, versus the plan's builders). The Power Platform pieces described on the call are not in the vault yet. Client names left out (public repo). Proposals only; the plan is not changed. Partly superseded by `delivery-vault-assessment.md` (Session 14) |
| `docs/analysis/delivery-vault-assessment.md` | Our own assessment, 6 November 2026 (Session 14), for lane B (low-code). Verdict table first: 37 pieces of the Get AI Engineer's material judged combine, replace, keep ours or gap. Sources: the GHE delivery vault; the Get AI Engineer's older Power Platform vault in Azure DevOps (`getai` org, project `GETAI-PowerPlatform`, repo `vault`; it holds 46 standards with IDs, 8 flow patterns, an export procedure and past engagement records, and names clients, so it is not copied here); Microsoft's `power-platform-skills`. Recommends building live in the lane with the driver's export as the record. Also day versus night, dates by scenario, questions for the Get AI Engineer, 15 proposed plan edits, and differences from Session 13. Decided 7 November 2026 and edited into the plan in Session 15: section 7 items 1 to 7, 11 and 13 (live build), items 8, 9 and 14 (low-code), item 10 (all lanes) and item 12 (moved to a new stage 9). Section 7 has the status. Section 10 holds the item 15 decision matrix (inventories, low-code and pro-code), still for Boroon to decide |
| `docs/sources/delivery-vault/` | Verbatim copy of `AI-Business-Solutions/delivery-vault` (private, `getai.ghe.com`) at commit `19877b8`, copied read-only 6 November 2026; all 19 files match the source's blob hashes. `PROVENANCE.md` says what it is. A source, not adopted: its nested skills do not load. The source repo stays the truth. The source moved to `51fdde5` on 6 November (onboarding guides only); this copy is not refreshed |
| `docs/sources/transcript-skills-comparison-addy-pocock-tan.md` | A YouTube video comparing the three skill packs (https://www.youtube.com/watch?v=sU9MW8Ycq2M). Source for the effort-level idea behind the T-shirt sizes. 744 lines. Added 1 November 2026 |
| `docs/sources/transcript-pstack-skills-review.md` | A YouTube review of Lauren Tan's pstack skills (https://www.youtube.com/watch?v=lUhXa8GiXns; skills at https://github.com/cursor/plugins/tree/main/pstack). 769 lines. Not cited in the plan. Added 1 November 2026. Covers potato mode, arena, swarm, why, recall, interrogate, create and maintain verification, unslop and bro |
| `docs/sources/transcript-pocock-skills-v1.1.md` | Matt Pocock on version 1.1 of his skills: renames to spec and tickets, grilling fixes (facts versus decisions, confirmation gate), implement and code review (two axes, Fowler smells), Wayfinder, research, prototype, TDD at seams. 856 lines. Cited in the plan as [Pocock v1.1 mm:ss] |
| `docs/sources/research-notes/` | The original research notes behind the plan, saved verbatim. Each has takeaways, cited findings, inferences and gaps per question. Use them to check the evidence behind plan section 3. Top level holds the first research folder (24 October 2026): `anthropic_long_running_harnesses.md`, `evals_quality_gates_metrics.md`, `harness_engineering_practitioner_lessons.md`, `orchestration_patterns_durable_engines.md`, `runtime_options_and_costs.md`, `spec_driven_development_requirements.md` |
| `docs/sources/research-notes/github-azure/` | Eight GitHub and Azure notes (24 to 25 October 2026): cost ledger and FinOps, Azure infrastructure for agents, Copilot billing and partner benefits, Copilot coding agent and Agent HQ, Copilot primitives parity, GitHub Enterprise control plane, and notes on the Spec Kit and workshop transcripts. Not yet read in this project's sessions |
| `docs/sources/research-notes/power-platform/` | Five Power Platform notes (1 November 2026): `pp_alm_identity_environments.md`, `pp_testing_evaluation.md`, `pp_agent_tooling.md`, `review_of_uploaded_plan.md` (the review that produced the plan's corrections to the uploaded plan), and `v3_1_changes_from_transcripts.md` (the brief for the 15 V3.1 changes). Not yet read in this project's sessions |
| `docs/sources/report-v1-fund-nights-on-credits.md` | Earlier report V1, "Fund Nights on Credits, Price at List". The first GitHub and Azure version, before the two-lane design. Superseded |
| `docs/sources/report-v2-two-lanes-one-gate.md` | Earlier report V2, "Two Lanes, One Gate, Priced at List", before the Spec Kit layer was added in V2.1. Superseded |
| `docs/sources/workshop-slides/` | The five slides from the Anthropic workshop, as images 1 to 5. The plan cites a slide called "The simplified harness" |
| `docs/one-pager/` | The engineer one-pager for plan V3.1, as `GET-AI-Overnight-Factory-one-pager.html` and `single-page-artefact.md`. A short summary for GET AI engineers. It still says client work runs at cash, which the credit decision of 2 November 2026 replaced. Also `GET-AI-Factory-Ways-of-Working.html` (5 November 2026): how low-code and pro-code FDE squads work with the factory, for technical and non-technical readers, on the GET AI design system. Published as a private artifact, https://claude.ai/artifact/Ufn9wxxTA29eCRCLWHn9sg; the repo copy is the same page with a document wrapper so it opens in a browser |
| `docs/sources/report-v2.1-two-lanes-one-gate.md` | Earlier report V2.1, "Two Lanes, One Gate, Priced at List". 925 lines. The GitHub and Azure design the main plan builds on: two lanes, harness parity, Spec Kit day gate, traces, credits, ledger schema, Lane A and B cost models, 8-stage plan. Still the best source for Lane A, ACA jobs, the ledger SQL schema and GitHub-side limits |
| `docs/sources/report-grill-the-spec-lock-the-tests.md` | The first report, "Grill the Spec, Lock the Tests". 195 lines. Original evidence base: what each harness resource teaches, the verifier-is-the-weak-point research, the grill gate, Claude Code facts, first design and stages |
| `docs/plans/schedule.md` | The dated order of the remaining stage 0 and stage 1 stories, from Monday 9 November 2026 to the Stage 1 exit test on Friday 18 December, then the start of stage 2 in January (Session 16, at Boroon's word). Two tracks (laptop, documents), checkpoints, and what depends on other people (a second approver by 4 December). ADO holds the same dates as Start and Finish Date and the dependencies as predecessor links. At each session's end, mark finished stories and move later dates if one slipped, here and in ADO |
| `docs/plans/stage-1-day-gate-plan.md` | The plan for the day-gate builds of Stage 1 (Session 17, 7 November 2026, ADO 2543): 2545 templates and the standards seed, 2544 Spec Kit pin, presets and the spec check, 2546 scenario conventions and the Playwright kit, 2548 mining with spike 0.17. Nine sessions DG1 to DG9, dated 7 November (DG1, done in Session 18) to 15 December, and Boroon's decisions D1 to D6 plus action A1 (keep pinned kits current). Read it at the start of any of those sessions. The gate scripts (2538) are not in it |
| `staging/` | Drafts of the day-gate files (D1), moved to `GetAI-IP` on Friday 4 December 2026 (DG8), then deleted here. `staging/README.md` says where each part moves. So far: `factory-manifestos/` with its README and the three project templates in `templates/project/` (`glossary.md`, `docs/adr/README.md`, the `coding-standards.md` header), DG1, Session 18. Nothing in it may name a client, a person or an engagement (public repo) |
| `docs/plans/stage-1-gate-build-plan.md` | The plan for three build sessions (workflow file, rulesets and CODEOWNERS, offline build checks). Read it at the start of any Stage 1 build session. D1 to D3 decided. Builds 1 to 3 done 3 November 2026, then moved to `GetAI-IP/factory-gates` (Session 9). Paths in it that start `factory-gates/` now mean that repo's root |
| `docs/plans/spike-0.2/` | Spike 0.2, GHE.com OIDC with pac: **passed 4 November 2026** (Session 12). `README.md` has the portal steps for an Entra app, a federated credential, a lane environment and an application user (reuse for lanes 2 and 3), the claims seen and the clean-up list. `probe.yml` and `required.yml` are copies of the workflows that ran in the scratch repos `GetAI-IP/oidc-probe` and `oidc-probe-target`, with placeholders for the IDs. The scratch repos, their ruleset and the two scratch credentials were deleted on 4 November 2026; `getai-fl1-exec`, its application user and `factory-lane-1` stay |
| `docs/plans/spike-0.3/` | Spike 0.3, Dataverse MCP with an app-only token: **passed on both paths 6 November 2026** (Session 13), the local proxy (`dataverse mcp`) and the remote `/api/mcp`, as `getai-fl1-exec` by GitHub OIDC. `README.md` has the portal steps (federated credential, the GA MCP toggle, the allowed MCP clients entry and its publisher prefix), the allowed-clients list as it was before the spike, three runs and 13 findings. `probe.yml` and `mcp_probe.py` are copies of what ran in the scratch repo `GetAI-IP/mcp-probe` (deleted 6 November 2026, with its credential). The allowed-clients entry `new_getaifl1exec` stays in `factory-lane-1` for Stage 3 |
| `docs/plans/spike-0.18/` | Spike 0.18, headless YAML export as the lane identity (ADO 2462): **YAML fails, the XML fallback passes, 8 November 2026** (Session 19). On a runner as `getai-fl1-exec`, on pac 2.14.1 and 2.4.1, `export` then `unpack`, `clone` and `sync` all wrote XML; the XML tree held all five parts, packed signed out and with no network, and a second export was byte-identical. Also: a one-column Web API update clears an environment variable's default value. `README.md` has the runs, 11 findings and the scratch list. `probe.yml` and `export_probe.py` are copies of what runs in the scratch repo `GetAI-IP/export-probe` (setup, probe, teardown modes). The scratch (the repo, the credential `export-probe-fl1-exec`, the solution `FactorySpike` and its parts in `factory-lane-1`) is kept for spike 0.14, then deleted only at Boroon's word |
| `docs/plans/spike-0.19/` | Spike 0.19, reset fidelity (ADO 2463): **passed 10 November 2026** (Session 20), in `factory-lane-1` alone (not with 0.10). As `getai-fl1-exec` on a runner, a probe-only stand-in for `reset_environment.py` imported the reset commit with overwrite and publish, set the lane's environment variable value, found and deleted a flow and a column left in the solution and a flow left outside it, and the fresh export equalled the reset commit byte for byte. Also found: `solutioncomponent.createdby` cannot find what the lane identity made (the Default Solution's rows are by SYSTEM), so the finder asks each component table for its maker, and finds tables and columns by state against a bootstrap list; `Other/Solution.xml` does not list every root component. `README.md` has the runs, 12 findings and the scratch list. Edited into the plan on 11 November 2026, at Boroon's word, with his rule that a table or column found outside the solution stops the lane for a person to check (ADO 2843). `reset.yml`, `reset_probe.py` and `lane-fl1.json` are copies of what runs in `GetAI-IP/export-probe`; not gate scripts. The scratch is 0.18's plus one environment variable value, kept for spike 0.14 |
| `docs/plans/factory-gates-move-step-8.patch` | The record of move step 8 (the gate workflow pointed at `GetAI-IP`), merged in `GetAI-IP/factory-gates` 3 November 2026 |
| `GetAI-IP/factory-gates` (not in this repo) | The gate repo on `getai.ghe.com`, protected branch `release`. Moved out of this repo's `factory-gates/` folder on 3 November 2026 with its history, and deleted here (Session 9). Enterprise `GetAI`; `GetAI-IP` is the central org and also holds the held-out tests (`factory-holdout`, not yet created). Four orgs (`AI-Business-Solutions`, `AI-Managed-Services`, `Cloud-AI-Platforms`, `GetAI-Knowledge`) will use the gate through small private caller repos, a later build. Cloud sessions cannot reach `getai.ghe.com` (Git providers needs a Team or Enterprise plan; Boroon is on an individual plan), so changes to it run from his laptop, by pull request there. Until a second approver exists, `release-protection` has 0 approvals and `factory-gates` is excluded from the org ruleset `protect-main`. Holds `.github/workflows/lcp-gate.yml` (Appendix A; every action pinned to a full commit ID; the comment on a `uses:` line is the version alone, or Dependabot leaves it stale; Dependabot runs; its first five pull requests merged 4 November 2026 (Session 11); for each new one, read the release notes, check the pin against the tag, and see `self-test` green first; Boroon merges), `.github/workflows/self-test.yml` (runs the tests, manifest verify and rulesets check on every pull request to `release`, read-only, no secrets; added by PR 7, merged 4 November 2026; not a required check until someone other than Boroon works on the factory, his choice on 4 November 2026; until then check it is green before merging), `lcp/` (`lane_map`, `check_protected_paths`, `manifest`, `make_rulesets`, `audit_bypass`, `apply_rulesets`, `check_builders`, `pack_offline`), `rulesets/` (`org.json` for `AI-Business-Solutions`, four generated rulesets, not applied), `templates/CODEOWNERS`, `scripts.sha256` (hashes every file a gate job reads), `pending-scripts.txt` (20 unwritten scripts; the live-build decision of 7 November 2026 changes that list and narrows `check_builders`, a laptop gate slice listed in `docs/progress.md`, Session 15) and 154 tests (gate PR 12, merged 4 November 2026, moved .NET to `10.0.x` for pac 2.4.1). Tests need Python 3.10 or later and a virtual environment outside the clone: `pip install --require-hashes -r requirements-test.txt`, then `python3 -B -m unittest discover -s tests`. **Boroon browses the laptop folders in Finder (4 November 2026), so before every local check, and whenever the local folders are used, delete Finder's files in the clone first:** `find . -name .DS_Store -not -path './.git/*' -type f -print -delete`. A root `.DS_Store` fails `manifest.py verify` and 2 tests as "unlisted"; it is not a real failure. Its README holds the findings, the move steps and the next slices. The plan still calls it `getai/factory-gates`, except in section 5.3 |
| `tools/session_usage.py` | Time and tokens per Claude Code session, from the local transcripts (forks and subagents included, duplicates removed). Used at the end of every session for the ADO story bodies. Added 7 November 2026. In the plan (10.1, Session 16) it is the fallback for sessions with no telemetry, not a gate script: it runs on a laptop over files the engineer controls, so its numbers are self-reported. At Stage 2 it gains a ledger-shaped output for a trusted loader |
| `.claude/skills/bro/SKILL.md` | The `/bro` skill, Lauren Tan's `bro` adopted unchanged (1 November 2026) |
| `.claude/skills/` | Live skills, all 44 built from third-party skills; each names its source and pinned commit in its first lines (since 11 November 2026, ADO 2549). `bro`. `ask-me` (router by size, adapted from `ask-matt`). Adopted unchanged: `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`, `create-verification-skill`, `maintain-verification-skill`. Adapted for GET AI, all untested: `lcp-blast-radius`, `getai-decision-log`, `getai-correct`, `lcp-how`, `lcp-why`, `getai-intake`, `getai-wizard`, `getai-questionnaire`, `getai-grilling`, `getai-domain-modeling`, `lcp-triage`. Also adopted 2 November 2026 with a GET AI note each: `unslop` and 21 `principle-*` skills (three conflicting ones stay on the shelf). Pro-code versions, all untested: `pcp-blast-radius`, `pcp-how`, `pcp-why`, `pcp-triage` (the plan has no code-repo triage workflow yet). Decided by Boroon on 2 November 2026. The two verification skills were then edited to write to `.claude/skills/lcp-verify/`. All of them reviewed by him and merged to the default branch (rule 17 met). Still untested |
| `skills/` | Third-party skills: the pinned originals of all 56 we hold (Addy 10, Tan 35, Pocock 9, Benny 2), 4 shared Addy reference files, and each source's MIT licence text (`skills/*/LICENSE`, 11 November 2026). A shelf: it does not auto-load, only `.claude/skills/` does. Provenance, commits and what became of each are in `skills/README.md`. Every file matched upstream at its pin on 11 November 2026 |
| `docs/component-register.md` | The component register's rows (plan 8.2 and 8.3 point 4), made 11 November 2026 (Session 21, ADO 2549) at Boroon's word: one row per third-party source at a pin, with what we take, licence, where it is copied, where the full read is recorded, how it is watched and when last checked. Today the three skill sources; A1 (ADO 2740) adds the kits. Review monthly, first on Monday 23 November 2026 with the Ignite re-check |
| `docs/analysis/skills-policy-check.md` | Plan 8.3's policy checked against every vendored skill (Session 21, 11 November 2026, ADO 2549): how it was checked, gaps common to all, one table (skill, source, commit, licence, read in full and where, status, gaps, fix), and Boroon's three decisions (the register, licence text on the shelf, a source line in the 10 live skills that lacked one). Only `poteto-mode` (shelf) is not read in full |
| `docs/analysis/skills-reading-notes.md` | Our notes from reading those 16: safety read, what each assumes that we lack, one line each with how to adapt, findings. Proposals only |
| `docs/analysis/skills-reading-notes-batch2.md` | Notes on batch 2, read 2 November 2026: `unslop`, the 24 `principle-*` skills, `grilling`, `domain-modeling` (shelved in `skills/tan/` and `skills/pocock/`; `grilling`, `domain-modeling`, `unslop` and 21 principles are live). Also `poteto-mode`, read in full except the `watch-pr` code (Cursor plugin, not harness agnostic, not adopted). Proposals only |
| `docs/analysis/skills-reading-notes-skill-batches.md` | Notes from the three-batch skills plan (batch 1 `lcp` 13, batch 2 `pcp` 16, batch 3 Lane A 8, from the chat "Planning the skills to use"). Full reads so far: `show-me-your-work` (live as `getai-decision-log`); `pause-safely`, `bug-fix` and "Opening a PR" (dropped; open item: no live bug-fix workflow); shelved in `skills/`: `diagnosing-bugs` (revisit for BAU Managed Services), `code-simplification` (keep its signal tables for the reviewer rubric), `deprecation-and-migration` (keep expand/contract), `debugging-and-error-recovery` (keep its untrusted-error-output section), `security-and-hardening` (checklist in `skills/references/`) `codebase-design` (Lane A; decide with `architect`) and `improve-codebase-architecture` (hot-spots idea for gardening). Batch 3 `frontend-ui-engineering`, `api-and-interface-design`, `observability-and-instrumentation` and `architect` are read in full and shelved (checklists in `skills/references/`); revisit at Stage 6. `ci-cd-and-automation`, `shipping-and-launch` and `arena` are dropped (not read in full by us). Boroon decided 2 November 2026 that Lane A's architecture sketch gets a day approval (plan not yet edited). A roll-up of fourteen possible additions is at the end of the notes. Open items: code-repo security checks and prompt injection are not in the plan. Proposals only. A separate agent-made review of all 36 is on branch `claude/sharp-wright-1muptp`, not `main` |

The main plan (V3.1) supersedes both earlier reports and V3. Read them for detail the plan condenses, not for current decisions. If they conflict, the main plan wins.

Timestamps in the plan's citations, such as [Tan podcast 16:21 to 16:53], match the leading timestamps in these transcript files. Search for the start time, for example `grep -n '^16:21' docs/sources/transcript-tan-pocock-podcast.md`.

Everything the plan cites is now in the repo. Boroon supplied the full research folder as a zip, and it was merged by checksum with no duplicates. See `docs/progress.md` for which files were saved but not yet read.

## Where to find what in the main plan

Line numbers are as at 13 November 2026 (Session 22, after ADO 2433). If the file has changed, run `grep -n '^## ' docs/sources/plan-v3.1.md`.
Read by line range, for example offset 379 and limit 200.

| Lines | Section |
|---|---|
| 1 to 29 | Bottom line and contents |
| 30 to 117 | 1. Naming rule, how to read, what changed (V3.1 against V3, V2.1 and the uploaded plan), key dates |
| 118 to 167 | 2. Operating model on one page: day phases, who owns what, the 19 rules |
| 168 to 305 | 3. What the research teaches, including what each transcript added |
| 306 to 378 | 4. Lanes and routing, the outer loop (triage), night and background workloads |
| 379 to 947 | 5. Lane B for Power Platform in depth: architecture and the driver (5.1), engine, identities, environment pool and reset with the leftover finder (5.4 at 487), night timeline, live build and code over click-ops (5.6), the gate (5.7 at 643), locked scenarios, `lcp-verify`, Merge Danger and trust ladder, ADO state machine, agent instructions, throttling, licensing, promotion, residency |
| 948 to 1077 | 6. The day gate: Spec Kit presets (6.3 `getai-lcp`), grilling rules, Factory Eligible and one ADO project per engagement (6.4, with day branches carrying the ADO ID), intake, Wayfinder maps, prototypes |
| 1078 to 1172 | 7. Handoff files, traces, weekly routine, gardening |
| 1173 to 1222 | 8. Harness parity, component register, third-party skills policy |
| 1223 to 1287 | 9. Credits, billing modes, model choice, data residency tiers |
| 1288 to 1418 | 10. Cost ledger (10.1 time and tokens per story on every engine), schema, the matrix and its baseline page (10.3), story cost model, cost envelope |
| 1419 to 1465 | 11. Staged build plan, stage 0 spikes (20), stages 1 to 9 |
| 1466 to 1503 | 12. Risks, most serious first (33) |
| 1504 to 1519 | 13. Accelerator and IP |
| 1520 to 1602 | 14. Decision log (14.4 holds the decisions after V3.1: live build, the precedence rule, ADO projects, assessment items, the day gate (D1 to D6), time and tokens per story, the XML source layout (spike 0.18), the reset and leftover removal (spike 0.19), Dataverse MCP credits per lane (2433)) |
| 1603 to 1643 | 15. Open questions and evidence quality |
| 1644 to 2211 | Appendix A: gate workflow YAML (untested; tags shown, `factory-gates` holds commit pins). `map` and `locks` match `factory-gates` as at Build 3, 3 November 2026. Since 7 November 2026 (live build) the plan is ahead of `factory-gates` in four places: `build` runs only generator-backed builders and packs the XML source layout (spike 0.18), `static` runs the export-diff plan (`plan_from_export.py`), and `verify-in-test` no longer runs the two Test plan scripts. Since 4 November 2026 it sets up .NET `10.0.x` (spike 0.2), as `factory-gates` does since gate PR 12 |
| 2212 to 2352 | Appendix B: Merge Danger rubric (B.1 low-code path rules, on the XML layout's folders), verifier count, `trust.yml` |
| 2353 to 2642 | Appendix C: agent definitions, `AGENTS.md`, `lcp-verify` skill, PR body template |
| 2643 to 2704 | Appendix D: ADO fields (including Work Size, AI Tokens, Agent Minutes, and human minutes split into spec, review and PARK) and states |
| 2705 to 2723 | Appendix E: sources used |

The two transcripts are already digested in plan sections 3.5 (workshop) and 3.6 (Spec Kit). Read the full text only when quoting.

## The plan in brief

Build the Power Platform profile of "Lane B" first. By day, humans shape a high-level spec on Spec Kit (pinned at the newest 1.3.x, D2, 7 November 2026).
Someone other than the worker writes and locks the acceptance scenarios. A human then sets "Factory Eligible" in Azure DevOps (ADO).
At night, Copilot CLI runs headless on a GitHub Actions runner in Australia, one story per lane, across three long-lived Sandbox environments that are Managed Environments.
The agent builds live in its lane. The driver, a trusted step, then exports the solution, and that export is the PR's source (decided 7 November 2026).
Our plan wins on design. The Get AI Engineer's material (the delivery vault and the older ADO vault) is the default for anything the plan does not settle: use it as it is or with the least change, and do not write our own (Boroon, 7 November 2026). Anything from the older ADO vault comes over anonymised, by a reviewed PR.
A required workflow in a separate gate repo runs only trusted checks, imports each PR into a Test environment the worker cannot touch,
runs locked and held-out scenarios, then one to three fresh verifier sessions click through the app.
A deterministic Merge Danger score is computed for every PR. An AI reviewer may raise it, never lower it.
Humans merge in the morning. `main` is always human.
Auto-merge is a rung on a trust ladder (L0 to L3), earned per change class on evidence, only into the `integration` branch.

Lanes:
- **Lane A**: greenfield and feature-sized code builds. One long Copilot SDK session.
- **Lane B, code profile**: issue-sized changes in existing code, via the cloud agent.
- **Lane B, Power Platform profile** (focus): story-sized changes to Power Platform solutions, via Copilot CLI on a runner.
- **Day work**: canvas app authoring, new-harness Copilot Studio agents, environment creation, anything needing an admin login.

New in V3.1: `lcp-verify` (verification skill and CLI the worker uses in its own loop), an outer loop that triages AI Managed Services client reports,
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
13. Every run has a `run_id`, a credit cap and an iteration cap. Every cost goes in the ledger at list and cash. Every story's time and tokens are recorded, by day and night, on every engine (plan 10.1, 7 November 2026).
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
- **`lcp-verify`**: skill plus CLI with commands `app`, `query`, `flow`, `agent`, `smoke`. The executor agent uses a lane copy. The gate uses a trusted copy.
- **Live build** (decided 7 November 2026, plan 5.6 and 14.4): in lane B (low-code), the agent changes the lane through pac, the Web API, Dataverse MCP and the App Spec apply, never by editing exported files. The driver's export is the PR's source, in the XML layout (`pac solution export` then `unpack`; spike 0.18, 8 November 2026).
- **Builder (low-code only)**: a script or Microsoft tool that makes solution source from an input kept in Git. From 7 November 2026, only Microsoft's own: the App Spec, `pac copilot`, and the build tools for code apps, PCF and plug-ins. The code parts among these work the pro-code way: source in Git, built by Microsoft's tools.
- **Driver (low-code lane)** (plan 5.1): the trusted steps of the night execution workflow that run around the agent session. They come from the gate repo and are never written by the agent. Before the session, the driver resets the lane and starts the Copilot CLI session. Between stops it runs the fast checks, up to 5 loops. After the session it exports and unpacks the solution, commits it, pushes the branch and opens the PR. The agent builds in the lane and writes its handoff files. It never exports, commits the solution, pushes or opens the PR. The lane drift check is a separate job, run as the lane's read-only verify identity.
- **Driver (Lane A)**: the TypeScript program in the ACA job that runs the generator and evaluator Copilot SDK sessions. Same role for code builds, without the export.
- **Pro-code**: no builders and no export. The agent edits the source, and the gate builds and tests it. In Lane B's code profile there is no trusted driver: the orchestrator dispatches through the tasks API, an `agentStop` hook runs the fast checks, and the cloud agent opens its own PR. The live-build decision changes nothing here.
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

The size is the largest answer across reversibility, blast radius, clarity, verifiability, effort, and residency. It is not an average. The spec owner proposes it at intake. The gate can raise it, never lower it. It is held in the ADO field `Custom.WorkSize` (plan Appendix D, decided 7 November 2026), and the matrix's baseline page groups time, tokens and cost per accepted story by size and profile, for sizing and pricing (plan 10.3).

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

1. **Credits for client work: accepted (Boroon, 2 November 2026).** Builds for customers can be made on credits. Settled; do not reopen.
2. Auto-merge letting soft test gaming through. Answer: deterministic floor, rungs earned on evidence.
3. Unmanaged developer environments retiring (dates above). Spike 0.9 closed 4 November 2026: the only unmanaged ones are four personal environments, not used by the factory or clients; their owners are told. New lanes must be Sandbox plus Managed.
4. Client code leaving Australia for inference. Copilot residency covers only the US and EU. BYOK to Azure OpenAI in Australia East is the only in-country path found. Each client gets a tier T1 to T4.
5. **Closed by spike 0.2 (4 November 2026):** `pac auth create --githubFederated` works on GHE.com, started by hand and inside a ruleset workflow with a `job_workflow_ref` subject. New repos get the immutable subject, with owner and repo IDs. pac 2.4.1 needs .NET 10; the gate sets it up since gate PR 12 (merged 4 November 2026). Across orgs untested.

The full list of 33 is in plan section 12. Risk 12 happened and was lowered on 8 November 2026: no headless pac command writes YAML (spike 0.18), so low-code lane repos use the XML layout, which passed the rest of the exit test. Canvas apps stay out of the night.

## Cost, as modelled (not measured)

- About USD 11.82 per attempt and USD 15 per story in AI credits and compute at list.
- About USD 150 per accepted story fully loaded. Human minutes are about 80% of that.
- Evaluator quality and review minutes move margin far more than token price.
- One partner designation funds about 1.3 Power Platform lanes at three stories a night. Three lanes need a specialisation or cash.

## Build plan

The 45 days build the factory. They move no project up a trust rung. Do not start a stage until the one before passes its exit test.

| Stage | Days | What |
|---|---|---|
| 0 | 1 to 14 | 20 spikes and the money question (credit ruling, OIDC with pac on GHE.com, MCP, `pac copilot`, cloud agent limits, billing, environment audit, headless YAML export (0.18), reset fidelity (0.19), time and tokens per story on every engine (0.20, run in stage 1) and more) |
| 1 | 1 to 14 | Safety net: gate repo as required workflow, rulesets, Test environment, Spec Kit presets, humans keep using the AI by day |
| 2 | 15 to 21 | ADO automation, `lcp-verify` v0, ledger v0 |
| 3 | 22 to 30 | Night shift, one lane, rung L1 |
| 4 | 31 to 45 | Three lanes, calibration, held-out set, gardening |
| 5 | 46 to 70 | Lane B for code repos |
| 6 | 60 to 90 | Lane A |
| 7 | about day 75 earliest | Rung L2 per change class, on evidence |
| 8 | ongoing | Scale, bake-offs, accelerator |
| 9 | last, no date | Learning from past engagements: a mining agent of its own, every engagement type, anonymised findings only (added 7 November 2026) |

## Open questions (owner)

- ~~Does `pac --githubFederated` work on GHE.com and in ruleset workflows?~~ Yes, within one org (spike 0.2, 4 November 2026). Across orgs, with the callers build.
- Which Copilot features work on GHE.com, and which billing identity for the CLI? (Platform team and Boroon, spike 0.6)
- ~~Does Dataverse MCP accept an app-only token?~~ Yes, through the local proxy and the remote endpoint, once the app is on the environment's allowed MCP clients list (spike 0.3, 6 November 2026). Each tool call is billed 0.1 Copilot Credit (USD 0.001 at list), drawn from the tenant's shared prepaid pool (ADO 2433, 13 November 2026). Boroon's cap, the same day: the driver stops the session at a set number of MCP calls (the number from spike 0.14), retries a failed call three times, and either stop PARKs.
- ~~Does a headless export write YAML as the lane identity?~~ No: XML only, on pac 2.14.1 and 2.4.1; the XML layout is used (spike 0.18, 8 November 2026).
- ~~Under live build, does the reset leave the lane equal to `integration`?~~ Yes, byte for byte, for a table, column, flow, role, environment variable and connection reference (spike 0.19, 10 November 2026). Forms, canvas apps and metadata made outside the solution are still open.
- Do flows by the Web API, the App Spec apply and FlowAgent work as the lane identity? (Platform team, spike 0.14, before Stage 3)
- Lanes in the client's tenant or ours, per client? (Boroon)
- Power Platform licence, capacity and meter prices in AUD. (Commercial)
- What did GitHub Universe and Ignite change? Is there a rename? (Boroon)
- Which ITSM tools do AI Managed Services clients use? (AI Managed Services). For code repos so far: AutoTask tickets and PRTG alerts (read through their APIs or an MCP server, not built), ADO service hooks and service desk webhooks. Power Platform clients not yet known
- Which change classes go in `trust.yml`, and is a 20% random sample at L2 right? (Boroon)
- Do the Claude Code VS Code extension and desktop app export OpenTelemetry as the CLI does, and does Copilot in VS Code for day sessions? (Platform team, spike 0.20)

The full list is in plan section 15.1.
