# Lock the Gate, Pool the Lanes, Merge by Day

**The GET AI overnight software factory. Combined plan V3, focused on Lane B for Power Platform. 1 November 2026.**

**Bottom line.** Build the Power Platform profile of Lane B first, and keep the rest of V2.1. By day, a spec owner shapes a high-level spec on Spec Kit 1.2 with the GET AI preset and a new Power Platform preset. Someone other than the worker writes the acceptance scenarios and locks them. A human then sets "Factory Eligible" in Azure DevOps (ADO). At night, Copilot CLI runs headless on a GitHub Actions runner in Australia, with pac and Microsoft's Power Platform skill plugins pre-installed. It builds one story per lane across a pool of three long-lived Sandbox environments that are Managed Environments. A required workflow in a separate gate repo runs only trusted checks. It imports the PR into a Test environment the worker cannot touch, runs locked Playwright, Web API, flow and Copilot Studio scenarios plus a held-out set, and then a fresh evaluator session clicks through the app. A deterministic Merge Danger floor scores every PR, and the review agent may raise that score but never lower it. Humans merge in the morning. Auto-merge comes later, only into the integration branch, only for low-danger changes, and only when 30 days of evidence say it is safe, never on a date. Four identity roles keep build, verify, review and merge apart, with per-lane identities for each lane's environment, all secretless over OIDC if pac federation works on GHE.com, which is the first spike. Three dates force action now: no new unmanaged developer environments from 15 November 2026, suspension from 15 December 2026 and deletion from 15 January 2027. Power Apps Test Engine is deprecated, so all UI tests are Playwright. Copilot inference cannot stay in Australia today, so decide residency per client; BYOK to Azure OpenAI in Australia East is the only in-country path the research found. On our model a Power Platform story costs about USD 11 in AI credits and compute at list, and about USD 144 fully loaded, with human minutes over 80% of that. The biggest risk is still the credit ruling: run client work at cash until Microsoft answers in writing.

## Contents

1. Bottom line, naming, how to read, what changed, key dates (this section)
2. The operating model on one page
3. What the research teaches
4. Lanes and routing
5. Lane B for Power Platform in depth
6. The day gate
7. Handoff files, traces, and the weekly calibration and retro
8. Harness parity and the component register
9. Credits, billing modes, model choice and data residency
10. The cost ledger, profitability matrix and cost envelope
11. Staged build plan
12. Risks, most serious first
13. The accelerator and IP
14. Decision log
15. Open questions and evidence quality
- Appendix A: gate workflow YAML for the Power Platform profile (untested)
- Appendix B: Merge Danger rubric
- Appendix C: custom agent definitions and AGENTS.md
- Appendix D: ADO fields and state map
- Appendix E: sources and transcripts used

## 1. Naming, how to read this, what changed and key dates

### 1.1 Naming note: "Power Platform" is today's name, not an identifier

Microsoft is expected to rename Power Platform soon. No new name was published as of 1 November 2026. The research found only that Power Platform release plans now carry "As of October 2026, this content is archived and no longer maintained", pointing to the "AI at Work" roadmap ([release plan entry](https://learn.microsoft.com/power-platform/release-plan/2026wave1/power-platform-governance-administration/github-support-source-code-integration-power-platform); [blog listing](https://www.microsoft.com/en-us/power-platform/blog/content-type/news/) [snippet]). Learn pages read on 1 November 2026 still say Power Platform, Power Apps, Power Automate, Copilot Studio and Dataverse. Ignite runs 17 to 20 November 2026 ([Ignite guide](https://partner.microsoft.com/en-us/blog/article/ignite-2026-overview) [snippet]), so a rename would most likely land there. Adjacent renames already happened: the Power Automate app in Teams is now "Workflows" ([Learn](https://learn.microsoft.com/power-automate/teams/install-teams-app)), and Microsoft 365 Copilot is now "Microsoft Copilot" ([Learn](https://learn.microsoft.com/microsoft-365/copilot/microsoft-copilot-requirements)).

In this plan, "Power Platform" means the current product family: Power Apps (canvas, model-driven and code apps), Power Automate, Copilot Studio and Dataverse.

**The naming rule.** Prose may use product names. Nothing that machines read may.

| Thing | Product-neutral identifier | Never |
|---|---|---|
| The lane profile | `lcp` (low-code platform), as in `profile:lcp` | `pp`, `powerplatform` |
| Factory environments | `factory-lane-1`, `factory-lane-2`, `factory-lane-3`, `factory-test` | `pp-dev-1` |
| Lane codes in branches and identities | `fl1`, `fl2`, `fl3` | |
| Entra apps and application users | `getai-fl1-exec`, `getai-fl1-verify`, `getai-<proj>-test`, `getai-<proj>-deploy` | `ppf-lane1-exec` |
| Labels, custom properties | `lane:fl1`, `profile:lcp`, `factory=enabled` | |
| Gate workflow and scripts | `factory-gates/.github/workflows/lcp-gate.yml`, `gate/lcp/*` | |
| Spec Kit preset | `getai-lcp` | |
| ADO tags and fields | `factory-eligible`, `Custom.LaneProfile = lcp` | |

So a rename touches prose only. Re-check names in the week after Ignite.

### 1.2 How to read this

- **Prices** are USD list as read on 24 to 25 October 2026. Power Platform licence and capacity prices were not researched.
- **Dates.** Original research read 24 October 2026; GitHub and Azure research 24 to 25 October; Power Platform research 1 November 2026. GitHub Universe (28 to 29 October 2026) has not yet been checked (section 15).
- **Models versus measurements.** **Model** means arithmetic on stated assumptions. **Estimate** means a researcher's judgement, such as a run time. Only figures cited to a published run are measured.
- **Markers.** No marker: read in full. **[secondary]**: a third-party write-up. **[snippet]**: a search summary only, unverified. **[inference]**: our reasoning from documented pieces. **[untested]**: nobody has run it; stage 0 or 1 must prove it. **[unverified]**: not checked against a primary source.
- **Talks.** **[talk mm:ss]** cites Anthropic's workshop "How to Build Agents That Run for Hours (Without Losing the Plot)" ([edited transcript](https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript)) **[user-supplied transcript]**. **[Spec Kit talk mm:ss]** cites GitHub's "Open Source Friday: Spec Kit Part 2", 16 October 2026 ([video](https://www.youtube.com/watch?v=8hHCpNVLhmI)) **[user-supplied transcript]**. Boroon supplied both, plus the workshop's five slides.
- **Names.** "The uploaded plan" is Boroon's "End-to-End Specification: The GET AI Microsoft Software Factory" plus "Copilot Studio Agents & App Builds" (1 November 2026), in Part A and Part B. "V2.1" is "Two Lanes, One Gate, Priced at List". This plan stands alone; earlier documents appear in Appendix E only as sources.

### 1.3 What changed

**Against V2.1**

- A Power Platform profile of Lane B is added and built first, on Copilot CLI in an Actions runner, not the cloud agent (sections 4 and 5).
- ADO Boards is the queue and system of record; the orchestrator owns its state (section 5.11).
- Merge Danger, with a deterministic floor and blast radius, joins every lane (section 5.10, Appendix B).
- Four identity roles with per-lane application users (section 5.3), and an environment pool with bootstrap, preflight, reset and lane locks (section 5.4).
- New verification and residency facts: Test Engine out, Playwright toolkit and Copilot Studio evaluation in; Copilot inference residency for the US and EU only, BYOK for Australia (sections 5.8, 5.9 and 9.4).
- Handoff files add `state.md`, `park.json` and `lessons-learned.md`; calibration and the Retro Loop merge (section 7). The build plan follows the 45-day timeline with new spikes (section 11). New dated risks (section 12) and the naming rule (section 1.1).

**Against the uploaded plan** (full table in section 14.1)

- Part B is the architecture. Part A's Foundry and Agent Framework orchestrator and "Azure AutoGen" are dropped; Copilot Studio and Wayfinder survive as an optional front door.
- Auto-merge is rebuilt: deterministic floor, LLM may only raise, never for tests, scripts, builders, workflows, hooks or agent instructions, only into `integration`, only on evidence.
- The gate is a required workflow in a separate repo; credentialed jobs run only trusted code; lanes map to environments with a lock each.
- Locked scenarios from someone other than the worker, a held-out set, and a separate Test environment and identity. One identity becomes four.
- The money is fixed (credits by default, caps, `run_id`, ledger), the Dev lanes become Sandbox plus Managed, the evaluator uses the app, runs are resumable, transcripts go to Blob, stories stay at "what and why", and the small edits are fixed.

### 1.4 Key dates

| Date | What happens | What we do |
|---|---|---|
| April 2026 | Power Apps Test Engine deprecated; docs and repo "no longer maintained" ([deprecations](https://learn.microsoft.com/power-platform/important-changes-coming#deprecation-of-test-engine)) | No `pac test run`. Playwright only |
| Since 15 July 2026 | New, renamed or transferred repos get an immutable OIDC subject with numeric IDs ([GitHub OIDC reference](https://raw.githubusercontent.com/github/docs/main/content/actions/reference/security/oidc.md)) | Read the real `sub` before creating each federated credential |
| Since 1 October 2026 | Actions retention also deletes checks, runs and statuses ([retention](https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)) | Export evidence to Blob nightly |
| From October 2026 | Pipelines deploying to unmanaged targets get 30 days plus one 30-day extension, then are blocked ([admin deployment page](https://learn.microsoft.com/power-platform/alm/admin-deployment-hub)) | UAT and Prod are Managed Environments |
| 1 November 2026 | Partner credits align to the offer purchase date ([August 2026 announcements](https://learn.microsoft.com/partner-center/announcements/2026-august)) | Check credit expiry in the runway view |
| 10 November 2026 | Durable Functions in-process support ends ([external events](https://learn.microsoft.com/azure/durable-task/common/durable-task-external-events)) | Isolated worker only, if we use Durable Functions |
| 15 November 2026 | No new unmanaged developer environments; one managed developer environment per user; no new Dataverse for Teams environments ([control environment creation](https://learn.microsoft.com/power-platform/admin/control-environment-creation#developer-environments)) | Lanes are Sandbox plus Managed |
| 17 to 20 November 2026 | Microsoft Ignite | Re-check names, Copilot Studio evaluation APIs, Git integration status |
| 30 November and 11 December 2026 | Power Apps Vibe and App Builder close; "Create descriptions using AI", Power Apps Ideas and Copilot formula generation end ([important changes](https://learn.microsoft.com/power-platform/important-changes-coming)) | Do not build on them |
| 15 December 2026 | Existing unmanaged developer environments suspended ([important changes](https://learn.microsoft.com/power-platform/important-changes-coming#deprecation-of-unmanaged-developer-environments-and-the-power-apps-developer-plan)) | Convert or move any lane before then |
| 15 January 2027 | Unmanaged developer environments deleted (same source) | Same |
| February 2027 | Stricter premium licence enforcement for apps in Managed Environments and model-driven apps ([licensing FAQ](https://learn.microsoft.com/power-platform/admin/powerapps-licensing-faq)) | Licence every human and test user who opens apps |
| 30 October 2027 | Dataverse for Teams decommissioned ([important changes](https://learn.microsoft.com/power-platform/important-changes-coming)) | Not used |

## 2. The operating model on one page

Humans own intent, spec approval and the merge. Agents build and verify overnight. Every agent run, night and project is costed, so cost to build feeds pricing and the profitability matrix. GitHub Enterprise on GHE.com (`getai.ghe.com`, Australian data residency) and GitHub Copilot are the engine, paid from Microsoft partner credits where the rules allow. Azure provides infrastructure. ADO Boards is the work queue and the system of record.

### 2.1 The four phases of a day

| Phase | When (Sydney) | What happens | Output |
|---|---|---|---|
| **Day gate** | Business hours, locked by 17:00 | Intake (optionally through the Copilot Studio front door). Spec Kit idea assessment, specify and clarify with the GET AI and Power Platform presets. Test author writes acceptance scenarios; acceptance owners lock them. Design mocks approved for user-facing work. Human sets Factory Eligible. 17:00: the orchestrator builds the night plan from ADO; an acceptance owner approves it | Approved spec, locked scenarios, night plan |
| **Night** | 21:47 to 05:00 | Kickoff and preflight. One story per lane: reset, build with Copilot CLI, fast checks, push, PR. Portal-only steps PARK. Lane drift check. Lane released | One PR per story, or a parked story |
| **Verify** | On each PR, through the night | Required gate workflow: trusted static checks, import into Test, locked and held-out scenarios, evaluator click-through, Merge Danger. NEEDS_WORK goes back to a lane, two rounds at most | Evidence bundle, verdict, Merge Danger score |
| **Morning** | 05:41 digest; 09:00 to 10:00 review | Teams card and ADO updates. Trace review agent drafts fixes. Humans read evidence, read one failed trace in full, resolve PARKs, approve PRs into `integration`, approve the release PR to `main` and the UAT deployment | Merged work, answered questions, logged review minutes |

### 2.2 Who owns what

| Role | Owns | Never does |
|---|---|---|
| Development manager (Boroon) | The factory, the rules below, Phase 4 entry, the credit ruling | Approve, alone, a client release he started |
| Spec owner (consultant, PM or client PM) | Idea assessment answers, the spec, clarify answers, design mock approval | Write the acceptance scenarios for their own spec alone |
| Test author (a person, or the `test-author` agent by day) and `@acceptance-owners` | Acceptance scenarios, locked tests, held-out set, Copilot Studio test sets | Edit locked tests at night |
| Platform team | Gate repo, rulesets, identities, environment bootstrap, runner images, pinned tool versions | Sit in any bypass list for day-to-day merges |
| AI Managed Services practice | Weekly calibration and Retro, trace reading, manifesto updates by PR | Change prompts, rubrics or skills outside a reviewed PR |
| Morning reviewers (`@factory-reviewers`) | Approving PRs into `integration`, release PRs to `main`, UAT promotion | Approve a PR they initiated or authored |
| Client | UAT sign-off, residency tier, production approval where contracted | Receive credits, subscriptions or GitHub accounts paid by GET AI's partner benefits |
| Orchestrator (Actions plus an Azure Function) | ADO state, lane locks, night plan, PARK handling, dispatch | Make judgement calls about quality |
| Agents | Building (executor), grading (evaluator), scoring (reviewer), drafting fixes (trace reviewer) | Merge, approve, edit their own checks, or write ADO directly |

### 2.3 The rules we do not break

1. **Humans own intent, spec approval and every merge to `main`.** No agent and no App merges to `main`, ever.
2. **The worker never decides it is done.** The gate and an isolated evaluator decide. Self-reported "done" counts for nothing.
3. **Acceptance scenarios come from someone other than the worker.** They are locked before the night, and nothing at night weakens them.
4. **A held-out set lives where the worker cannot read it.** Only aggregate results come back to the PR.
5. **Credentials and untrusted code never share a job.** PR code (builders, the agent's own tests) runs only in jobs with no credentials. Jobs with credentials run only trusted scripts from the gate repo and treat PR files as data.
6. **Four identity roles: execute, verify, review, merge.** Each lane has its own execution and verification identities. None of them sits in any bypass list.
7. **One story, one lane, one branch, one PR.** A lane runs one story at a time under a lock.
8. **Code over click-ops.** A step that needs the portal or an interactive consent PARKs. Agents never invent inputs or work around the requirement.
9. **Clarify by day only.** A night agent that hits a material ambiguity writes it down and PARKs.
10. **Design first.** User-facing changes need an approved mock in the work item before the night.
11. **The Merge Danger floor is deterministic.** An LLM may raise the score, never lower it.
12. **Auto-merge only into `integration`,** only when the final score is 2 or less, never for protected paths, and only after the evidence criteria in section 5.10 are met. Never on a date.
13. **Every run has a `run_id`, a credit cap and an iteration cap.** Every cost lands in the ledger at list and at cash.
14. **Price from the list column,** never from credits.
15. **Client code and data follow the client's residency tier** (section 9.4). No client production data in factory lanes.
16. **Every transcript, trace and evidence file reaches Blob within the night,** tagged with `run_id`.
17. **Prompts, rubrics, agents, skills, hooks and gate scripts change only by a reviewed daytime PR,** and a new evaluator version re-runs the graded set first.
18. **Machine-readable names stay product-neutral** (section 1.1).

## 3. What the research teaches

This section keeps the evidence base in condensed form. Every design choice later in the plan points back here.

### 3.1 What each resource teaches

| Resource | Core lesson | Key numbers | Evidence |
|---|---|---|---|
| Anthropic, "Effective harnesses for long-running agents" (Nov 2025) ([post](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)) | An initialiser writes a feature list, `init.sh` and a progress file. Each later session reads them, builds one feature, verifies it in the browser, commits. Agents may only flip `passes`. JSON because models overwrite it less | Over 200 features, all `passes: false` at start | Primary |
| Anthropic, "Harness design for long-running application development" (Mar 2026) ([post](https://www.anthropic.com/research/harness-design-long-running-apps)) | Planner, generator, evaluator. V1 used sprint contracts and context resets. V2 on Opus 4.6 dropped both: one long generator session with compaction, one evaluator pass at the end. Claude is "a poor QA agent" out of the box and stays "inclined to be generous" | Solo run USD 9 in 20 minutes, broken. Full harness USD 200 in 6 hours, playable. DAW build USD 124.70 in 3 h 50 min; QA about USD 10 of 125 | Primary |
| Anthropic, "Building a C compiler with a team of parallel Claudes" (Feb 2026) ([post](https://www.anthropic.com/engineering/building-c-compiler)) | 16 bash loops relaunching `claude -p`. Git push conflicts as the lock. The human wrote verifiers, never pair-programmed. CI arrived late because new features broke old ones | About 2,000 sessions, two weeks, just under USD 20,000, 100,000 lines of Rust, 99% on most test suites | Primary |
| Anthropic workshop "How to Build Agents That Run for Hours" ([transcript](https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript)) **[user-supplied transcript]** | The operating detail behind the March post: adversarial evaluator using the app, rubrics, high-level planner, sprint contracts (now removed), trace reading, handoff files, deleting scaffolding (section 3.5) | Frontend-only runs used 5 to 15 rounds [talk 22:32 to 22:49]; 27 contract criteria [talk 32:04] | Primary for the talk |
| OpenAI "Harness engineering" (Lopopolo, Feb 2026) ([corpus](https://github.com/lopopolo/harness-engineering/blob/trunk/README.md); [essay](https://openai.com/index/harness-engineering/) [snippet]) | Hold the model constant; improve context and tools. `AGENTS.md` is a map, not a manual. Policy must be executable: lints whose error text names the fix. Reviewer agents "bias toward merging". Background agents prune drift | About a million lines, about 1,500 PRs, 3 to 7 engineers, no hand-written code ([hyperbo.la](https://hyperbo.la/w/production-function-changed/)) | Primary for the corpus; essay figures snippet only |
| GitHub Spec Kit 1.2.3 ([repo](https://github.com/github/spec-kit)) and Spec Kit Part 2 talk **[user-supplied transcript]** | A chain from constitution to converge. Clarify asks at most five questions, one at a time, from a ten-category scan. Checklists are "unit tests for English" and reviewer-owned. Version 1.2 adds presets, bundles, five workflows, the assess and bug extensions, converge and a lean preset | 1.0.0 on 21 August 2026; 1.2.3 on 22 October 2026 ([releases](https://github.com/github/spec-kit/releases)) | Primary |
| Microsoft Learn path "Develop agents and applications using agentic programming tools" ([path](https://learn.microsoft.com/en-us/training/paths/create-embed-custom-code-agents/)) | A tutorial on Copilot customisation, Spec Kit and the Copilot SDK, not a factory design | Four modules, 42 units | Primary |
| LangGraph and durable engines ([checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)) | LangGraph preserves state, not execution. Durable engines detect dead workers and wait for humans without compute. Add one only when a run outlives a process or waits for a person | | Primary for the docs |
| Anthropic, "Demystifying evals for AI agents" ([post](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) | Grade the outcome, not the path. Use pass^k when consistency matters. Start with 20 to 50 tasks from real failures. Clean environment per trial. "Do not trust scores until someone reads transcripts and checks the grading" | 75% per trial gives about 42% for pass^3 | Primary |
| Robert Brennan, OpenHands talk ([talk page](https://ai.engineer/talks/software-development-agents-what-works-and-what-doesn-t) [snippet]; [bssw.io](https://bssw.io/items/ai-coding-agents-what-works-and-what-doesn-t) [secondary]) | Agents win when they run an inspect, edit, run, read-errors loop in a sandbox. Delegate precise tasks with feedback, bounded permissions and a named human owner. OpenHands later named verification as the bottleneck and "drift from the original prompt" as the commonest failure | | Secondary only |

Three newer Anthropic artefacts matter for any Claude-based lane. The Code with Claude 2026 repo turns the November 2025 pattern into hooks, a kill switch, a steer file and a read-only evaluator that returns `PASS` or `NEEDS_WORK` on its first line ([cwc-long-running-agents](https://github.com/anthropics/cwc-long-running-agents)). `/goal` is a built-in outer loop judged by a fresh small model ([Claude Code docs](https://code.claude.com/docs/en/goal)). The best-practices page states the rule under all of it: "If you can't verify it, don't ship it" ([best practices](https://code.claude.com/docs/en/best-practices)).

### 3.2 Where the sources agree

Each point below appears in at least three independent sources.

- **Never let the worker decide it is done.** Anthropic moved from "tell the model to verify" to a separate evaluator to hooks that stop the model flipping the flag. Spec Kit says implementation "must not silently self-approve" checklists ([Agentic SDD reference](https://raw.githubusercontent.com/github/spec-kit/main/docs/reference/agentic-sdd.md)).
- **State lives in files and git, not in context.** Feature lists, progress files, lock files and checked-in plans all do this.
- **A machine-readable contract only flips from failing to passing.** It is the answer to "declared done too early", the failure every harness guide names first.
- **Enforcement belongs in tooling, not longer Markdown.** "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic" ([best practices](https://code.claude.com/docs/en/best-practices)). "If it matters, it belongs in a verifier owned by the repo" ([Lopopolo](https://hyperbo.la/w/production-function-changed/)).
- **The human holds authority at the merge.** Copilot's initiator approval "won't count toward the required number of approvals" ([GitHub docs](https://docs.github.com/en/copilot/how-tos/agents/copilot-coding-agent/reviewing-a-pull-request-created-by-copilot) [snippet]). Brennan: "accountability cannot be delegated" ([Tessl recap](https://tessl.io/blog/ai-engineering-sf-fair-2025-learnings) [secondary]).
- **A planner or spec step prevents under-scoping.** Anthropic's autonomy data: **32% of human interruptions supply missing technical context**, and **35% of Claude's self-stops present a choice between approaches** ([Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy)). Nobody is awake at 3 am to answer either. This is why the day gate exists and why the night PARKs.
- **Delete harness parts when models improve.** Anthropic, the workshop and Lopopolo all say it ([fixed-worker doc](https://github.com/lopopolo/harness-engineering/blob/trunk/docs/fixed-worker/README.md)).

### 3.3 The disagreements, and how this plan settles them

| Question | One side | Other side | This plan |
|---|---|---|---|
| Fresh context per task, or one long session? | November 2025: one feature per fresh session was "critical" | March 2026: Opus 4.6 held "a two-hour continuous build coherently" in one session [talk 34:14 to 36:08] | By lane. Lane A runs one long session per build. Lane B, including the Power Platform profile, runs one bounded story per session |
| How much spec ceremony? | Critics: 1,300 to 2,500 lines of Markdown for small features, "10x slower" ([field study](https://github.com/ianhxu/agentic-engineering-field-study/blob/main/04-spec-driven-development.md) [secondary]) | Anthropic and Lopopolo: the hard part is under-specified non-functional requirements | Spec Kit 1.2 presets size the ceremony: lean preset for stories, full preset for features. The interrogation stays |
| Does lights-off stay healthy? | Lopopolo: yes, with executable policy and garbage-collection agents ([Latent Space](https://www.latent.space/p/harness-eng) [snippet]) | Horthy: his lights-off attempt ended in a hand rewrite after about four months ([Why Software Factories Fail](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md)). Faros: incidents per PR up 242.7% ([Faros](https://faros.ai/research/ai-acceleration-whiplash) [secondary]) | A night shift, not a replacement for review. Auto-merge only into `integration`, only on evidence: 30 days of escaped-defect data first |

### 3.4 The verifier is the weak point, not the generator

The research changes what the gate must defend against. Outright tampering is rare. Soft gaming is common.

- **Outright tampering runs at low single digits.** EvilGenie measured Claude Code hardcoding tests on about 2.1% of problems and taking heuristic shortcuts on 20.7% ([EvilGenie](https://arxiv.org/abs/2511.21654) [snippet]). A 2026 re-run found newer models hack at most 2% of the time ([HVTB](https://arxiv.org/pdf/2608.22103) [snippet]). Over 30 to 50 tasks or stories a night, expect zero to two attempts: rare enough to miss by eye, common enough to need a detector.
- **Tests written to confirm one implementation over-accept by about a fifth.** Strengthening SWE-bench Verified tests rejected **19.78% of previously passing patches** ([SWE-ABS](https://icml.cc/virtual/2026/poster/62669) [snippet]).
- **Agent-written tests mostly assert nothing.** Across 86,156 test patches from agent PRs, **80.2% had weak or no oracle** ([All Smoke, No Alarm](https://arxiv.org/pdf/2606.18168) [snippet]).
- **Agents saturate visible tests and fail held-out ones.** The gap grows **by 28 points for every tenfold increase in code size** ([SpecBench](https://arxiv.org/pdf/2605.21384) [snippet]).
- **LLM judges are generous or swayed by surface cues.** They misclassify correct code, and an authority cue flipped a verdict ([Jin and Chen](https://arxiv.org/abs/2603.00539) [snippet]; [Don't Judge Code by Its Cover](https://arxiv.org/abs/2505.16222) [snippet]). Anthropic: "a reviewer prompted to find gaps will usually report some, even when the work is sound" ([best practices](https://code.claude.com/docs/en/best-practices)).
- **Automation catches a minority of real defects.** Anthropic estimates **about one-third** of the bugs behind past claude.ai incidents would be caught by its automated processes ([SDLC post](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle)).
- **Budgets must live outside the model.** An agent offered approval at its token limit took it **97%** of the time ([Ramp Labs](https://labs.ramp.com/research/coding-agents-ignore-spend/) [snippet]).

So the threat is not "the agent deletes the tests". It is "the agent writes code and tests from the same reading of the spec", plus "the agent fits the visible tests and misses integration". Four rules follow, and every lane applies them:

1. **Separate authorship.** One author writes the tests; another writes the code ([best practices](https://code.claude.com/docs/en/best-practices)).
2. **Lock the tests two ways.** A push ruleset blocks the path, and a hash or diff check in the gate catches anything that slips through.
3. **Keep a held-out set** the worker never sees.
4. **Treat reviewer findings as claims with evidence.** A finding without evidence is "no verdict", not a pass and not a fail ([Code Review PR page](https://code.claude.com/docs/en/code-review-pull-requests)).

The uploaded plan's Phase 4 broke rules 1 and 2: PRs with an LLM score of 0 to 2, test edits included, would auto-merge. That is exactly the soft-gaming path above. Section 5.10 fixes it.

### 3.5 What the workshop transcript added

The transcript **[user-supplied transcript]** turned snippets into operating detail. The quotes that shape this plan:

- **Use the app, not the diff.** The evaluator "isn't just reading diffs"; it opens live pages with Playwright [talk 18:42 to 19:31]. Its best catches, a FastAPI route-ordering bug that "passes every unit test but might actually break in prod" and a delete-key Boolean bug, were "only caught because the evaluator's actually using the app" [talk 31:19 to 31:49]. This is why the Power Platform evaluator clicks through the app in Test (section 5.9).
- **Harsh critics are tractable.** "Tuning a standalone critic to be harsh is actually very tractable, but tuning a builder to be somewhat self-critical is not" [talk 20:05].
- **Out of the box, Claude is generous.** "A really, really bad just general QA agent" [talk 32:40 to 34:08].
- **Taste is gradable.** Write the opinion down as a rubric, calibrated with examples [talk 21:31 to 22:23]. The tuning "generalize[s] quite well" across projects [talk 40:35 to 41:21].
- **The planner stays high level.** An early technical error "is going to cascade through every single one of these sprints" [talk 24:12 to 24:46]. This is why stories stay at "what and why".
- **Granular criteria give useful critiques.** "If you have vague criteria, you have vague critiques" [talk 32:04 to 32:40].
- **Restart beats patching.** A single loop "keeps trying to patch the same thing" [talk 23:08 to 23:42].
- **Isolate the evaluator.** Feeding it the generator's context risks "muddying of thoughts"; "it's very easy for the model to kid itself" [talk 60:03 to 61:04].
- **Read the traces.** "The primary debugging loop" is reading what the agent did [talk 33:51]. "No, you gotta read the whole thing" [talk 73:25 to 74:41].
- **Handoffs beat compaction.** A JSON learnings log plus a live structure doc "are more than enough for Claude Code and a human to come in and start iterating" [talk 54:08 to 56:04].
- **Tools absorb harness patterns.** "The harness patterns that work tend to get absorbed back into the tools" [talk 37:58 to 38:52]. This is the IKEA warning behind section 8.
- **Brownfield needs more control.** Monitoring raises an issue, an agent makes the PR, a review runs, a human reviews before merge [talk 71:00 to 72:06]. That is Lane B.

### 3.6 What the Spec Kit Part 2 talk added

Spec Kit 1.2 is "more kit than spec" [Spec Kit talk 8:52]. Presets encode "standardized ways of working" [Spec Kit talk 36:44 to 37:04], bundles are "a vetted set of things" [Spec Kit talk 6:02 to 6:23], and presets fit regulated work such as a medical-device "binder of all the things you had to check" [Spec Kit talk 56:29 to 57:51]. The assess extension returns go, kill or needs clarification, "a pocket PM" [Spec Kit talk 7:29 to 7:54; 55:02]. The bug workflow runs assess, fix, test [Spec Kit talk 8:12 to 8:32]. Converge asks "Did I overreach? Did I under-deliver? Did I break something?" and appends tasks [Spec Kit talk 9:29 to 12:30]. The lean preset "only creates three files" [Spec Kit talk 47:24 to 50:10]. `specify init` generates skills for Copilot, Claude or Codex, so one process serves every engine [Spec Kit talk 24:54 to 26:32]. The maintainer sees specs as "mostly transient" [Spec Kit talk 14:56 to 15:51], so client traceability needs our own retention policy (section 7).

### 3.7 What the Power Platform research adds (1 November 2026)

Section 5 cites each fact in full. In short:

- **Secretless ALM exists, with one unknown.** `pac auth create --githubFederated` needs only a tenant and an app ID ([pac auth](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)). No source confirms it on GHE.com.
- **The environment model changed.** Unmanaged developer environments are being retired; sandboxes are "best used for testing and ALM build environments" ([environment strategy](https://learn.microsoft.com/power-platform/guidance/adoption/environment-strategy)).
- **Per-run environments need humans.** "A service principal can't register itself" ([create SP](https://learn.microsoft.com/power-platform/admin/powerplatform-api-create-service-principal)), and OAuth connections need a sign-in. Pooled lanes are the right answer.
- **Limits are per user; the daily pool is per tenant** ([API limits](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits); [request limits](https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations)).
- **Test Engine is gone.** Microsoft's Playwright toolkit "works headlessly in GitHub Actions" ([Playwright samples](https://learn.microsoft.com/power-platform/developer/playwright-samples/overview)).
- **Copilot Studio testing is mostly automatable** on the standard harness, not on the new one ([REST API](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-rest-api)).
- **Much of the platform is now code:** `pac copilot` workspaces, Microsoft's skill plugins, and the YAML solution format "for all new projects" ([source control](https://learn.microsoft.com/power-platform/alm/use-source-control-solution-files)).
- **Pack can drop a component silently**, with exit code 0 ([SolutionPackager troubleshooting](https://learn.microsoft.com/power-platform/alm/solution-packager-tool#troubleshooting)).
- **Copilot inference residency covers only the US and EU** ([Copilot with data residency](https://raw.githubusercontent.com/github/docs/main/content/admin/data-residency/github-copilot-with-data-residency.md)).

### 3.8 Runtime facts that shape every night

- The Copilot cloud agent stops at 59 minutes: "This limit cannot be extended or bypassed" ([Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github)).
- Hosted Actions jobs stop at 6 hours, self-hosted jobs at 5 days, and queued jobs drop after 24 hours ([Actions limits](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/limits)). So self-hosted runners are for pre-built images and private networking, not for time.
- `schedule` "can be delayed during periods of high loads" and "some queued jobs may be dropped" ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)). Practitioners report 15 to 30 minute delays [snippet] ([Crontap](https://crontap.com/blog/github-actions-cron-drift-problem)).
- Container Apps jobs: "Platform maintenance ... might interrupt long-running job replicas", so set retry to at least 1 and design for at-least-once ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs#advanced-job-configuration)). The AVM module defaults `replicaTimeout` to 1,800 seconds ([AVM job module](https://github.com/Azure/bicep-registry-modules/blob/main/avm/res/app/job/README.md)).
- Copilot CLI autopilot runs until the model calls `task_complete`: self-declared, with no judge ([CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)). So the external gate stays.
- Billing "generally cannot trace consumed credits to specific prompts, sessions, or exact features" ([monitor AI usage](https://docs.github.com/en/copilot/how-tos/manage-and-track-spending/monitor-ai-usage)). CLI and SDK runs are measured through OpenTelemetry instead (section 10).

## 4. Lanes and routing

Two lanes run into one gate design. Lane B has two profiles: code repos, and Power Platform. The lane is a spec header field set by the preset and checked by the gate script.

### 4.1 Lane A: greenfield and feature-sized code builds (summary)

Unchanged from V2.1. By day, Spec Kit runs idea assessment, specify, clarify and checklist on Opus 5.5, with at least 20 testable acceptance behaviours; no plan or tasks [talk 23:59 to 24:56]. At night, one ACA job per build runs a TypeScript driver and one long Copilot SDK session (`generator`, Sonnet 5.5 through Copilot, Opus 5.5 for hard builds). The generator writes `plan.md` and `tasks.md`, runs `analyze`, passes the gate hook, builds and runs converge; a fresh `evaluator` grades the running app: PASS, NEEDS_WORK or RESTART, over 2 to 3 passes. Hosted SDK sessions have no 59-minute cap ([SDK backend services](https://docs.github.com/en/copilot/how-tos/copilot-sdk/setup/backend-services)). Builds are resumable (session state on Azure Files, frequent commits, explicit `replicaTimeout`). Model: USD 100 to 200 per build at list.

### 4.2 Lane B for code repos (summary)

Unchanged from V2.1, plus Merge Danger. By day, a lean-preset spec, or the bug workflow's assess step. At night, the cloud agent takes a 20 to 40 minute task through the tasks API ([agent tasks API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api)); `agentStop` runs fast checks; the gate evaluator grades the PR; at most two `@copilot` rounds; the merge queue integrates into `integration`; a human approves `integration` to `main`. Model: USD 2.26 to 8.86 per task at list.

### 4.3 Lane B for Power Platform (the focus)

Story-sized changes to Power Platform solutions: Dataverse tables, columns, views and forms, model-driven apps, cloud flows, plug-ins, code apps, and Copilot Studio agents on the standard harness. Each story runs as one Copilot CLI session in a GitHub Actions job, against one of three pooled lane environments, under a lane lock. The gate imports the result into a shared Test environment, tests it there and scores it. Section 5 has the detail.

### 4.4 The routing rule

| Route to | When |
|---|---|
| **Lane A** | Any of: expected agent work over about 40 minutes; a new app or service in code; a feature that spans UI, API and data; design-heavy UI where taste matters |
| **Lane B, code profile** | All of: issue-sized change in an existing codebase; 20 to 40 minutes of agent work; files no other task touches; existing tests and CI cover the area. Bugs always go here, through the bug workflow |
| **Lane B, Power Platform profile** | All of: the change lives in a Power Platform solution; it is story-sized (about 30 to 60 minutes of agent work, plus import and test time); its acceptance scenarios are locked; every interactive prerequisite (OAuth connection, consent, first share) is already bootstrapped or listed as a PARK step |
| **Day work, human-led with AI** | Any of: canvas app authoring (the supported authoring path needs a live Studio session, section 5.6); behaviour of agents on Copilot Studio's new GitHub Copilot harness; creating environments or tenant settings; anything that needs an admin with a username and password |
| **Not the factory** | The client's residency tier forbids AI on its code or data (section 9.4) |

**Large Power Platform features.** Wayfinder (or the spec owner) splits a new Power Platform app into stories with predecessor links in ADO. Dependent stories run in order, across nights when needed. This is a deliberate exception to V2.1's "do not split features into a chain of tasks". V2.1's rule exists because the cloud agent's 59-minute cap forces sprint scaffolding the model no longer needs. Here the chain comes from the platform itself: each story must import, publish and pass tests in a real environment, and lanes are scarce. [inference] Trial a Lane A-style long session that holds one lane all night for a greenfield solution in stage 8, once the lane is stable, and compare yield.

**Why the Power Platform lane is not the cloud agent.** Three reasons, set out in section 5.2: Power Platform work has slow, real-environment steps that strain a 59-minute cap; the cloud agent cannot use OAuth remote MCP servers and needs undocumented firewall entries for Dataverse; and Copilot CLI on a runner gives OpenTelemetry measurement, which the cloud agent lacks.

## 5. Lane B for Power Platform in depth

This is the uploaded plan's Part B, corrected. The shape stays: ADO queue, scheduled Actions as dispatcher, a headless agent, a pool of three long-lived lanes, PR checks, a review agent, Merge Danger, PARK, and an orchestrator that owns state. What changes is who can touch what, where verification runs, and when auto-merge is allowed.

### 5.1 Architecture and components

| Component | Runs on | Identity | Job |
|---|---|---|---|
| Intake front door (optional) | Copilot Studio intake agent plus the Wayfinder planning agent | The human user | Clarifying questions, `glossary.md`, a draft Epic and stories in ADO with predecessor links. What and why only. Feeds the day gate, never the night (section 6.5) |
| Day gate | Spec Kit 1.2 with the GET AI preset and the `getai-lcp` preset, in VS Code, Copilot CLI or the Copilot app | Human Copilot seats | Spec, clarify, design mocks, locked scenarios |
| Work queue and system of record | ADO Boards, `getai` organisation, process "Agile build v1" | Orchestrator service principal | Stories tagged `factory-eligible` in "Ready to build". State changes come only from the orchestrator |
| Orchestrator | `factory-control` repo: scheduled Actions (kickoff, dispatch, tick, digest) plus an Azure Function for GHE.com webhooks | Factory GitHub App; orchestrator service principal for ADO and Key Vault | Night plan, preflight, lane locks, dispatch, PARK handling, ADO state, provisional ledger rows |
| Execution | Actions job in `factory-control`, GitHub environment `fl<n>-exec`, on an ephemeral runner in Australia | `getai-fl<n>-exec`, over OIDC | Per-story reset, one Copilot CLI session with the `lcp-executor` agent, fast checks, then the driver pushes and opens the PR |
| Lane environments | `factory-lane-1` to `factory-lane-3`: Sandbox, Managed Environment, Australia region | Bootstrapped once by a human | Hold the manual OAuth connections. One story at a time |
| Lane close | Last job of the execution workflow, still under the lane lock | `getai-fl<n>-verify` (read only) | Drift check of the lane against the repo; posts the `lane/drift` check; releases the lock |
| Gate | Required workflow `lcp-gate.yml` in `factory-gates`, protected `release` branch (Appendix A) | No-credential jobs; a read-only gate App; `getai-<proj>-test` over OIDC | Trusted checks, import into Test, locked and held-out scenarios, evaluator, Merge Danger |
| Test environment | `factory-test`: Sandbox, Managed Environment, Australia region | `getai-<proj>-test` and a certificate test user | Managed import of each PR; morning preview of `integration` |
| Evaluator | Fresh Copilot CLI session inside the gate's Test job | Test user's browser session; no Dataverse write | Click-through of the app; PASS, NEEDS_WORK or RESTART |
| Review agent | Gate job `danger` | Job token with `checks: write`; no Dataverse access | Raises Merge Danger above the floor where warranted; writes the blast radius |
| Merge | Humans in `@factory-reviewers`; in Phase 4 only, a `factory-merger` App for `integration` | No bypass anywhere | Approve and enqueue |
| Promotion | Release workflow in `factory-control`; GitHub environments `uat` and `prod` with required reviewers | `getai-<proj>-deploy`, the only identity in UAT and Prod | Build the managed artefact from `main`, check it, import it with a settings file |
| Evidence, traces, ledger | Blob, Application Insights and Log Analytics in Australia East; ledger Function, PostgreSQL, Power BI | Evidence-writer managed identity | Everything keyed by `run_id` |

The flow, end to end:

```text
ADO "Ready to build" + Factory Eligible + locked scenarios
  -> 17:00 night plan (acceptance owner approves)
  -> 21:47 kickoff: preflight every lane, bypass audit, budgets
  -> per lane, one story at a time, under lock lane-fl<n>:
       reset -> Copilot CLI (lcp-executor) -> fast checks (max 5 loops)
       -> driver pushes agent/fl<n>/<ado-id>-<attempt> and opens PR into integration
       -> lane drift check -> release lock -> next story
  -> PR triggers lcp-gate (required workflow, trusted code only):
       map -> locks -> build (no credentials) -> static (trusted)
       -> verify-in-test (Test lock): plan, checker, import, locked, held-out, evaluator
       -> danger (floor, raise-only review) -> merge policy
  -> 05:41 digest; 09:00 to 10:00 humans approve -> merge queue -> integration
  -> release PR integration -> main (human) -> uat (approval) -> prod (approval)
```

### 5.2 The engine: Copilot CLI on an Actions runner

**Default: Copilot CLI, headless, in a GitHub Actions job.** Install `@github/copilot` and pin it (`COPILOT_AUTO_UPDATE=false`). Run `copilot -p` with `--autopilot`, the `lcp-executor` custom agent (`--agent`), explicit `--allow-tool` and `--deny-tool` lists, `--max-autopilot-continues`, `--max-ai-credits`, `--no-ask-user`, `--secret-env-vars`, `--output-format json` and `--share` ([CLI programmatic reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference); [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)). Pre-install pac (pinned), Python 3.11, Node LTS, `@microsoft/power-apps-cli`, `@microsoft/dataverse`, Playwright browsers, and Microsoft's skill plugins pinned to a vendored commit. Default model: Claude Sonnet 5.5 through Copilot, credit-funded; Opus 5.5 for stories the spec marks hard.

Why this engine:

- **No 59-minute cap.** Hosted jobs run up to 6 hours and self-hosted up to 5 days ([Actions limits](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/limits)). A story with two solution imports, a publish and a checker run needs headroom.
- **GitHub OIDC is native in Actions.** `pac auth create --githubFederated` reads the runner's token, so each lane's identity stays secretless (section 5.3).
- **Microsoft supports this pairing.** Its skills README documents headless flags for Copilot CLI, such as `--allow-tool 'shell(pac *)'` ([power-platform-skills](https://github.com/microsoft/power-platform-skills)). Its code apps quickstart uses Copilot CLI with the `code-apps-preview` plugin ([quickstart](https://learn.microsoft.com/power-apps/developer/code-apps/how-to/quickstart-github-copilot)).
- **It is measured.** CLI emits OpenTelemetry with `github.copilot.nano_aiu` per `invoke_agent` span, so cost per story is measured, not estimated ([Copilot OpenTelemetry](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)).
- **It is credit-funded.** Claude through Copilot bills GitHub AI credits; the Anthropic API would bill cash.

**Where it runs.** Start on GHE.com hosted runners in `australiaeast` or `australiacentral` ([GHE.com network details](https://github.com/github/docs/blob/main/content/admin/data-residency/network-details-for-ghecom.md)). Move to ephemeral self-hosted runners on ACA jobs in Australia East for a pre-baked image or private networking; they cannot run Docker inside ([runner tutorial](https://learn.microsoft.com/azure/container-apps/tutorial-ci-cd-runners-jobs)). Self-hosted does not remove time limits, so every story is resumable from its branch and handoff files.

**Billing identity.** It must follow the Mode A and Mode B split (section 9.2). Stage 0 picks one of two:

1. `GITHUB_TOKEN` with `permissions: copilot-requests: write`. Usage "is metered directly to the organization" when the org policy allows it, and user budgets do not apply ([CLI in Actions](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/copilot-cli-in-github-actions)). No personal token, so no Conditional Access problem; per-project cost still comes from OpenTelemetry. Client work then needs its own organisation or cost centre tied to the cash subscription [inference].
2. A seated machine account per project, as in V2.1, with a hard-stop user budget. But a personal token on EMU with Conditional Access "will likely be blocked" ([CAP support](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/configuring-authentication-for-enterprise-managed-users/about-support-for-your-idps-conditional-access-policy)).

**Secondary engine: Claude Code at cash.** Same runner, same skill marketplace (Microsoft lists Claude Code for every plugin, and `dataverse@claude-plugins-official` exists ([Dataverse-skills](https://github.com/microsoft/Dataverse-skills))), same pac and Dataverse profiles, MCP via `claude mcp add` ([PAC MCP](https://learn.microsoft.com/power-platform/developer/howto/use-mcp)). Use `--max-budget-usd` and `--max-turns`. Bills the Anthropic API at cash; inference is offshore. Use it for bake-offs and as a fallback when the Copilot pool is spent.

**The cloud agent: only where its limits allow.** It can reach Dataverse in principle: setup steps may request `id-token: write` and run OIDC logins ([configure MCP servers](https://github.com/github/docs/blob/main/content/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers.md)), and a custom allowlist entry for `dynamics.com` covers `*.crm6.dynamics.com` ([customise the firewall](https://github.com/github/docs/blob/main/content/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall.md)). But the session stops at 59 minutes, including setup and tests. The default allowlist has no entry for `dynamics` or `login.microsoftonline.com` ([allowlist reference](https://github.com/github/docs/blob/main/content/copilot/reference/copilot-allowlist-reference.md)), and no source lists the full Power Platform host set. The firewall "only applies to processes started by the agent via its Bash tool". It cannot use OAuth remote MCP servers, sees only Agents secrets ([secrets](https://github.com/github/docs/blob/main/content/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables.md)), and emits no OpenTelemetry. So use it only for bounded edits that need no live environment, such as a builder change checked by an offline pack. Test first, in stage 0: OIDC plus `pac auth create -ghf` in setup steps on GHE.com; an allowlist of `dynamics.com`, `login.microsoftonline.com`, `api.bap.microsoft.com`, `api.powerapps.com` and `powerplatform.com`; and whether a 45-minute story with one import fits.

**Where the research is uncertain.** Nobody has confirmed `--githubFederated` on GHE.com. The Copilot CLI billing path on GHE.com is not documented separately. Some Microsoft skills have plan-approval steps, and their headless behaviour is unknown. Copilot feature availability on GHE.com (CLI policy, OpenTelemetry, code review, cloud agent) was not researched. Each is a stage 0 item.

### 5.3 Identities: four roles, separated per lane

The uploaded plan used one "Pipeline App Reg" for execution, verification and review, against its own "strict separation of duties". This plan uses four roles. Where a lane has its own environment, the identity is per lane, so a lane cannot touch another lane's environment.

| Role | Identity | Exists in | Dataverse role | GitHub side | Can never |
|---|---|---|---|---|---|
| **Execute** (per lane) | `getai-fl<n>-exec`: Entra app plus application user | `factory-lane-<n>` only | System Administrator. Lower roles "can't deploy plug-ins and other code components" ([delegated deployments](https://learn.microsoft.com/en-us/power-platform/alm/delegated-deployments-setup)), so limit by scope, not role | Job in environment `fl<n>-exec`. The model has no push token; the driver pushes to `agent/fl<n>/*` with the factory App | Exist in Test, UAT or Prod; be a tenant management app; push to `integration` or `main` |
| **Verify, lane** (per lane) | `getai-fl<n>-verify` | `factory-lane-<n>` | Custom read-only role: organisation-level Read on solution, solution component, workflow, canvas app and customisation tables; no customisation privileges | Lane-close job, environment `fl<n>-verify` | Fix what it checks |
| **Verify, Test** (per project) | `getai-<proj>-test` | `factory-test` only | System Administrator in Test, so it can import; this includes `prvAppendmsdyn_analysisjob` for the checker ([Build Tools SP](https://learn.microsoft.com/power-platform/alm/devops-build-tools#configure-service-connections-using-a-service-principal)). App permissions: Dynamics CRM and PowerApps-Advisor `Analysis.All` | Gate job `verify-in-test`, environment `lcp-test`, subject pinned to the gate workflow | Exist in lanes, UAT or Prod |
| **Verify, test user** (per project) | `factory-test-<proj>@<tenant>`: an Entra user with certificate sign-in | `factory-test` only | A business role, no maker rights | Certificate in Key Vault; read via the Test identity | Make or customise anything |
| **Review** (per project) | No Entra identity. The gate job's token with `checks: write` and read scopes | Nowhere in Dataverse | None | Posts a check run and a comment. Never submits a PR review, so it can never count as an approval | Approve or merge |
| **Merge** (per project) | Humans in `@factory-reviewers`. In Phase 4 only, a `factory-merger` GitHub App that enables auto-merge into `integration` | n/a | n/a | No bypass in any ruleset | Merge to `main` (the App); approve own work (humans) |
| **Deploy** (part of merge, per project) | `getai-<proj>-deploy` | UAT and Prod only (plus the pipelines host in design B) | System Administrator in targets; Deployment Pipeline Administrator in the host | Release workflow, environments `uat` and `prod` with required reviewers | Run without a human approval |

**The test user.** Microsoft's documented CI path for Playwright is certificate sign-in for a dedicated test user, with the certificate in Key Vault ([authentication guide](https://learn.microsoft.com/power-platform/developer/playwright-samples/authentication-guide)). That user must satisfy, or be excluded from, any Conditional Access policy that demands interactive MFA [inference]. It needs a premium licence, because Test is a Managed Environment (section 5.14).

**OIDC federation on GHE.com.** Create each federated credential like this:

- **Issuer:** `https://token.actions.getai.ghe.com`. On GHE.com the issuer "must substitute `githubusercontent.com`" with the data residency domain; discovery is at `/.well-known/openid-configuration` ([GitHub OIDC reference](https://raw.githubusercontent.com/github/docs/main/content/actions/reference/security/oidc.md)).
- **Entra scenario:** "Other issuer". The GitHub scenario in the portal fills in the github.com issuer, and "Pattern matching isn't supported for branches and tags" ([Entra workload identity federation](https://learn.microsoft.com/entra/workload-id/workload-identity-federation-create-trust)).
- **Audience:** `api://AzureADTokenExchange`.
- **Subject:** `repo:<org>/<repo>:environment:<env>` for an environment job. Repos created, renamed or transferred after 15 July 2026 use the immutable form `repo:<org>@<org-id>/<repo>@<repo-id>:environment:<env>` ([GitHub OIDC reference](https://raw.githubusercontent.com/github/docs/main/content/actions/reference/security/oidc.md); [Databricks example](https://learn.microsoft.com/azure/databricks/dev-tools/auth/provider-github)). Read the real `sub` from a debug job before creating the credential.
- **Pin the gate's Test identity to the gate workflow.** Customise the subject with `include_claim_keys: ["repo", "context", "job_workflow_ref"]`, which yields `repo:ORG/REPO:environment:ENV:job_workflow_ref:REUSABLE-WORKFLOW-PATH` (same source). Point it at `getai/factory-gates/.github/workflows/lcp-gate.yml@refs/heads/release`. Then only the trusted gate can obtain the Test token, even if a workflow elsewhere names the same environment [inference; untested for ruleset workflows].
- **Limits:** "A maximum of 20 federated identity credentials can be added to an application"; issuer plus subject must be unique per app; each field has a 600-character limit; and a wrong subject is accepted at creation, after which "the exchange fails without error" ([Entra FIC considerations](https://learn.microsoft.com/entra/workload-id/workload-identity-federation-considerations)). One app per identity keeps us far below 20. Flexible credentials with a restricted expression language are in preview ([flexible FIC](https://learn.microsoft.com/entra/workload-id/workload-identities-flexible-federated-identity-credentials)).

The pac command, built from documented flags: `pac auth create --name fl1-exec --githubFederated --tenant <tenantId> --applicationId <clientId> --environment https://<org>.crm6.dynamics.com`, in a job with `permissions: id-token: write` ([pac auth](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)). The Oceania Dataverse host is `crm6.dynamics.com` ([data centre regions](https://learn.microsoft.com/power-platform/admin/new-datacenter-regions)). pac reads the token from the runner's `ACTIONS_ID_TOKEN_REQUEST_URL`, which on GHE.com should point at the ghe.com issuer [inference]. Call pac directly in `run:` steps after `actions-install`: the `export-solution` and `who-am-i` action definitions on `main` list only secret or password inputs, which conflicts with Microsoft's tutorial ([export-solution action.yml](https://raw.githubusercontent.com/microsoft/powerplatform-actions/main/export-solution/action.yml); [OIDC/FIC tutorial](https://learn.microsoft.com/en-us/power-platform/alm/tutorials/github-actions-oidc-fic)). Pin pac; the tutorial pins 2.4.1.

**If the GHE.com spike fails,** fall back to certificate credentials in Key Vault, then managed identity on self-hosted ACA runners (`pac auth create --managedIdentity`) [untested for application users], then client secrets rotated monthly. Code apps need a secret anyway: `pa app push` documents only a client secret ([publish with SP](https://learn.microsoft.com/power-apps/developer/code-apps/how-to/use-service-principal)).

**Audit.** Turn on Dataverse auditing everywhere, plus the Workflows and Connection reference tables ([auditing for flows](https://learn.microsoft.com/power-automate/guidance/coding-guidelines/use-auditing-dataverse)), and use Purview for admin and Copilot Studio events ([Purview](https://learn.microsoft.com/power-platform/admin/activity-logging-auditing/activity-logs-overview)). Alert when a lane execution identity appears in any Test, UAT or Prod log. Confirm whether Purview covers sandboxes.

**Entra Agent ID, later.** Dataverse agent users are in preview, and "Support for creating Entra Agent Application Users from agent identities isn't available yet" ([agent users](https://learn.microsoft.com/power-platform/admin/agent-users)). Keep classic app registrations; revisit when they ship.

### 5.4 The environment pool

**Why a pool.** A new environment per run needs humans. The tenant management app registration must be done by an admin with a username and password, and once registered the service principal acts like a Power Platform Administrator with no granular scoping ([create SP](https://learn.microsoft.com/power-platform/admin/powerplatform-api-create-service-principal)). OAuth connections such as Teams and Outlook need an interactive sign-in. So: three long-lived lanes, bootstrapped once by a human.

**Environment types.** Unmanaged developer environments are being retired: no new ones from 15 November 2026, suspension from 15 December 2026, deletion from 15 January 2027 ([important changes](https://learn.microsoft.com/power-platform/important-changes-coming#deprecation-of-unmanaged-developer-environments-and-the-power-apps-developer-plan)). Developer environments are also "intended only for use by the owner", capped at 750 flow runs a month and 2 GB, with no capacity add-ons ([Developer Plan](https://learn.microsoft.com/power-platform/developer/plan)). So every lane is a **Sandbox** enabled as a **Managed Environment** in the Australia region. Sandboxes support copy, reset and backup. Do this now: filter the tenant for Type = Developer and Managed = No, and convert or move any lane before 15 December 2026.

| Lane code | Environment | Type | Purpose | Application users | GitHub environments |
|---|---|---|---|---|---|
| `fl1` | `factory-lane-1` | Sandbox, Managed, Australia | Night builds | `getai-fl1-exec`, `getai-fl1-verify` | `fl1-exec`, `fl1-verify` |
| `fl2` | `factory-lane-2` | Same | Same | `getai-fl2-exec`, `getai-fl2-verify` | `fl2-exec`, `fl2-verify` |
| `fl3` | `factory-lane-3` | Same | Same | `getai-fl3-exec`, `getai-fl3-verify` | `fl3-exec`, `fl3-verify` |
| `test` | `factory-test` | Same; solution checker set to Block | PR verification; morning preview | `getai-<proj>-test`; test user | `lcp-test` |
| `uat` | `<client>-uat` | Sandbox, Managed; checker Block | Client UAT | `getai-<proj>-deploy` | `uat` |
| `prod` | `<client>-prod` | Production, Managed; checker Block | Production | `getai-<proj>-deploy` | `prod` |

Use `pac admin create --type Sandbox --region australia` (pac defaults to `unitedstates`), and `pac solution check --geo Australia` ([pac admin](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/admin); [pac solution](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution)). Australian provisioning needs the tenant's account country to be Australia, New Zealand or Fiji ([Microsoft Cloud Australia](https://learn.microsoft.com/power-platform/admin/about-microsoft-cloud-australia)).

**Which tenant.** Two options per client, and the choice is ours to make [inference]:

- **Lanes in the client's tenant** (recommended for client work). Connections, data, licences and residency stay with the client, and Power Platform pipelines can reach UAT and Prod. The client pays capacity and licences, and a client admin must do the bootstrap.
- **Lanes in GET AI's tenant.** We carry capacity and licences and deliver managed solutions across tenants with GitHub Actions. Pipelines do not deploy across tenants: "No. We recommend using Azure DevOps or GitHub" ([pipelines](https://learn.microsoft.com/power-platform/alm/pipelines)). Use this for internal work and for clients without capacity.

**Bootstrap (a human, once per environment).** Record every value in `gate/projects/<proj>/lanes.json`, the lane manifest:

1. Create the environment with its security group; enable Managed Environments (`pac admin set-governance-config --protection-level Standard`, with `--solution-checker-mode block` for Test, UAT and Prod).
2. Add the application users and roles. The Power Platform API's `addAppUser` "always adds the application user as a System Administrator" ([create application user](https://learn.microsoft.com/power-platform/admin/create-dataverseapplicationuser)), so set the read-only roles by hand afterwards.
3. Sign in and create the OAuth connections (Teams, Outlook), the Dataverse connection and any connector secrets; set the connection references.
4. Set hierarchy security exclusions. No source says a service principal cannot; treat this as convenience, not a hard block.
5. Turn on what the stories need: "Enable code apps", the Dataverse MCP allowed clients, auditing, Application Insights for flow telemetry, backup retention.
6. Name a licensed human as the designated licensed user for service-principal-owned premium flows (section 5.14).
7. Run preflight once by hand and save the baseline.

**Nightly preflight (automated, before a lane accepts work).** The lane's verify identity checks what it can see from inside the lane:

- `pac auth create -ghf` and `pac org who`.
- `pac connection list`: every connection in the manifest exists and is healthy.
- `hierarchysecurityconfiguration` matches the manifest.

The orchestrator checks the rest, because these need tenant or admin reads that no lane identity should hold [inference]:

- Entra app permissions and federated credentials against the manifest (Graph).
- Managed Environment on, runtime state Enabled, checker mode as expected.
- At least 1 GB free database capacity, so a restore is possible ([backup FAQ](https://learn.microsoft.com/power-platform/admin/backup-restore-environments#faq)).
- Tenant request usage for Caller Type Application against the daily pool (section 5.13).
- Backups. System backups are continuous and kept 7 days ([back up and restore](https://learn.microsoft.com/power-platform/admin/backup-restore-environments)). A labelled manual backup (`pac admin backup --label "fl1-pre-<night>"`, about 10 minutes, no capacity cost) needs admin rights, so only the platform team's admin identity runs it, never a lane job.

Any failure marks the lane **Offline**, raises an ADO bug with the failing check, and puts it in the digest. The night runs on the remaining lanes.

**Per-story reset (automated, before the agent starts).** A trusted `reset_environment.py` from the gate repo runs as the execution identity, in a step before the agent gets control:

1. Delete transactional test data: rows that carry a test-run tag, plus the tables the manifest lists. Batch size 10 at first; honour `Retry-After`.
2. Import the unmanaged solution built from the head of `integration`, with overwrite and publish.
3. Re-apply the lane's environment variable values.
4. Confirm with a quick export and diff.

Never use `pac admin reset` in the loop. It wipes connections, application users, hierarchy exclusions and the pipelines link, all of which a human bootstrapped. If design B pipelines link a lane, a reset also forces you to "re-create the environment record" ([pipelines](https://learn.microsoft.com/power-platform/alm/pipelines)).

**Lane locks.** The execution workflow uses `concurrency: group: lane-fl<n>` with `cancel-in-progress: false`. The lock covers reset, build, push and the lane drift check, so a reset can never land mid-check. Concurrency groups are per repository, which is why every lane-touching job lives in `factory-control` [inference]. The gate's Test jobs use their own group per project repo, with `queue: max` (up to 100 pending, FIFO, "ordering is not guaranteed") ([concurrency](https://docs.github.com/en/enterprise-cloud@latest/actions/how-tos/write-workflows/choose-when-workflows-run)). The orchestrator mirrors lane state (Free, Busy, Offline) for the digest.

**Disaster path.** Restore last night's backup ("You can restore a managed environment only to another managed environment"), or copy a golden sandbox with `pac admin copy --type MinimalCopy`, which "can take up to 8 hours" and leaves OAuth connections for a human to rebind ([copy an environment](https://learn.microsoft.com/power-platform/admin/copy-environment)).

### 5.5 A night in the Power Platform lane

Times are Sydney local. All estimates; stage 3 measures them.

| When | Step | What happens |
|---|---|---|
| By 17:00 | Night plan | The orchestrator queries ADO for Factory Eligible stories in "Ready to build", orders them by priority and predecessors, assigns lanes, models and per-story budgets, and writes `factory/nights/<night_id>.json`. An acceptance owner approves it through a GitHub environment approval (waits are free) |
| 21:47 | Kickoff | Preflight every lane. Bypass audit. Budgets and credit runway. Mint `night_id` |
| 21:55 | Dispatch | One `workflow_dispatch` per free lane, paced from one job (secondary limit: 80 content-creating requests a minute ([rate limits](https://docs.github.com/en/enterprise-cloud@latest/rest/using-the-rest-api/rate-limits-for-the-rest-api))) |
| Per story, about 60 to 75 minutes | Execution | Reset (10 to 15 min) -> Copilot CLI session (30 to 45 min) -> fast checks after each stop (builders, diff, pack, manifest, lints), up to 5 loops -> driver commits, pushes, opens a PR into `integration` with `Factory-Run-Id` and `AB#<id>` -> lane drift check (3 to 5 min) -> release lock |
| On each PR, about 20 to 45 minutes | Gate | Static checks in parallel; then, under the Test lock: plan against the Test baseline, checker, import, locked and held-out scenarios, evaluator; then Merge Danger |
| :13, :33, :53 | Tick | NEEDS_WORK: re-queue to the next free lane with `findings.md`, two rounds at most. RESTART: fresh branch, attempt plus 1. PARK: ADO "Awaiting business", next story. No new dispatch after 04:00 |
| 05:41 | Digest | Teams card and ADO updates: PRs with score, door type and blast radius; PARKs with exact instructions; Copilot Studio items needing a human; cost per story |
| 06:00 | Trace review | `trace-reviewer` reads failed, parked and restarted runs and drafts fixes as PRs |
| 09:00 to 10:00 | Human review | Approve PRs into `integration`; resolve PARKs; approve mocks; answer questions; approve the release PR and the UAT deployment; log review minutes |

**Throughput, model.** One Test environment verifies about two PRs an hour (30 minutes each). Three lanes at three stories a night, plus about 30% rework, is about 12 gate runs, or 6 hours of Test time. That fits an 8-hour night but is the bottleneck. Add a second Test environment if the queue stays above 5 hours for a week.

### 5.6 Code over click-ops: what can be code, and what still PARKs

**Solution format.** Use the YAML source-control format for new projects. It gives "cleaner, more readable per-component diffs", supports multi-solution repos, and is the only format that holds canvas `.msapp` files and modern flows. Microsoft says use it "for all new projects" ([source control with solution files](https://learn.microsoft.com/power-platform/alm/use-source-control-solution-files)). It needs pac 2.4.1 or later ([pac solution](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution)). Keep existing XML repos on XML until a quiet week, then migrate; one format per repo. Put manifests under `solutions/<Name>/`, or the tool falls back to XML with a misleading error ([SolutionPackager troubleshooting](https://learn.microsoft.com/power-platform/alm/solution-packager-tool#troubleshooting)).

Do not use native Dataverse Git integration for the factory yet. GitHub support entered public preview on 31 August 2026, it needs Managed Environments, it is for developer environments only, it uses a GitHub App and Key Vault, and no source says it supports GHE.com ([Git integration overview](https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview); [connect to GitHub](https://learn.microsoft.com/power-platform/alm/git-integration/connecting-to-github)). Keep `pac solution export` and `unpack` in Actions as the source of truth.

**Builders and the drift gate.** Microsoft does not support hand-editing `customizations.xml` for tables, columns, processes, plug-ins, security roles and more ([when to edit the customisations file](https://learn.microsoft.com/power-platform/alm/when-edit-customization-file)). So:

1. Builders emit the YAML format. Agents edit builder inputs and per-component builders, never generated output.
2. Builders are deterministic: stable ordering, no timestamps, no fresh GUIDs on a re-run, fixed line endings. Otherwise the drift gate flaps.
3. One builder owns version stamps, which otherwise live in several files at once [secondary] ([Flowline wiki](https://github.com/RemyDuijkeren/Flowline/wiki/11-Philosophy) [snippet]).
4. Where Microsoft already has a generator, wrap it and drift-check its output: `pa app add data-source` and `pa app refresh data-source` for code apps ([pa CLI](https://learn.microsoft.com/power-apps/developer/code-apps/reference/cli)), `pac copilot pack` for agents, and the model-apps App Spec. Microsoft's own model-apps plugin follows this loop: spec, lint, dry-run, idempotent apply, verify, "downloads a deployed app back into an editable App Spec" ([model-apps README](https://github.com/microsoft/power-platform-skills/blob/main/plugins/model-apps/README.md)).

The gate then runs, in order: every builder; `git diff --exit-code`; `pac solution pack`; **a manifest check**; the solution checker. The manifest check exists because pack can drop a component silently. If a component is in `rootcomponents.yml` but its files are missing, "The tool still succeeds (exit code 0) and produces a valid .zip file, but the declared component is omitted" ([SolutionPackager troubleshooting](https://learn.microsoft.com/power-platform/alm/solution-packager-tool#troubleshooting)). The check fails if any declared root component has no files, or if the packed zip's component list differs from the declared list.

**The lane drift check.** After the agent finishes, the lane-close job exports the lane's solution, unpacks it and compares it with the PR's source. Anything in the environment that is not in the repo is drift, and drift blocks the PR. This catches an agent that changed the environment through the Web API or MCP and skipped the builders. Dataverse re-serialises on export, so compare canonicalised files [secondary] ([DataverseDrift](https://www.nuget.org/packages/DataverseDrift) [snippet]). Run a weekly round-trip test on `integration` the same way.

**Copilot Studio agents as code.** `pac copilot init | clone | pull | push | pack` gives a Git-friendly workspace (`agent.mcs.yaml`, `topics/*.mcs.yaml`, `actions/`, `knowledge/`, `workflows/*/workflow.json`, `settings.mcs.yml`, connection references). `pack` "is a local operation ... needs no authentication and no environment, so it's safe to run in a build pipeline" ([pac copilot](https://learn.microsoft.com/power-platform/developer/cli/reference/copilot)). Rules:

- CI uses `pac copilot pack` plus `pac solution import`. `push` runs only in the agent's own lane, because "A successful push mutates the live agent"; apply is not publish ([synchronise changes](https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-synchronization)). `pull` and `push` need sync metadata from `clone` or `init`, so commit it deliberately.
- Factory agents use the standard harness; agents cannot move between harnesses ([harnesses](https://learn.microsoft.com/microsoft-copilot-studio/harnesses-overview)). The VS Code extension is GA and Microsoft names GitHub Copilot and Claude Code for "agent-driven development" ([extension overview](https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview)). The `cli-copilot` authoring mode is too early to build on.
- Untested: `clone`, `pull` and `push` under a federated service principal profile (stage 0).

**Code apps.** React or Vue apps on Power Platform with 1,500+ connectors ([overview](https://learn.microsoft.com/power-apps/developer/code-apps/overview)). `pac code` is "(Preview)" and will be deprecated for the npm `pa` CLI ([pac code](https://learn.microsoft.com/power-platform/developer/cli/reference/code)). Deploy with `pa app push --non-interactive` as a service principal, after a maker shares the app with it once, because "A service principal can't grant itself access" ([publish with SP](https://learn.microsoft.com/power-apps/developer/code-apps/how-to/use-service-principal)). Code apps are outside Git integration, which suits us. Treat `pa` and the `code-apps-preview` plugin as preview.

**Model-driven apps.** The `model-apps` plugin's `/app-builder` produces an App Spec, shows a dry-run plan, builds after approval and can verify the result ([Learn](https://learn.microsoft.com/power-apps/maker/model-driven-apps/model-driven-app-external-tools)). Microsoft advises "a general-purpose coding model or an advanced reasoning model". At night the agent may produce the App Spec and the dry-run plan. If the plan holds a one-way door (a column drop, a security role change), the agent PARKs with the plan as evidence and the apply waits for a human. Headless behaviour of the approval step is untested; stage 1.

**MCP servers.**

| Server | Auth | Night use |
|---|---|---|
| Dataverse MCP, remote `/api/mcp` ([Learn](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-mcp)) | Entra OAuth; each client allowed per environment ([configure](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-mcp-disable)) | Not on the cloud agent (no OAuth remote MCP). Billed since 15 December 2025 ([release plan](https://learn.microsoft.com/power-platform/release-plan/2025wave2/data-platform/dataverse-mcp-server)) |
| Dataverse CLI local proxy, `npx @microsoft/dataverse mcp <url>` ([non-Microsoft clients](https://learn.microsoft.com/power-apps/maker/data-platform/data-platform-mcp-other-clients)) | Profiles compatible with pac; `auth create` supports `--githubFederated` ([npm](https://registry.npmjs.org/@microsoft%2Fdataverse)) | After the stage 0 app-only spike passes. Preview package |
| PAC CLI MCP, `pac copilot mcp --run` ([Learn](https://learn.microsoft.com/power-platform/developer/howto/use-mcp)) | The active pac profile | Optional. Microsoft frames it as "designed for local development and testing purposes" |
| Copilot Studio MCP ([Learn](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/copilot-studio-mcp)) | Browser sign-in | Day only |
| Canvas Authoring MCP ([AGENTS.md](https://github.com/microsoft/power-platform-skills/blob/main/plugins/canvas-apps/AGENTS.md)) | Needs an open Studio coauthoring tab | Day only |
| FlowAgent MCP (power-automate plugin) ([README](https://github.com/microsoft/power-platform-skills/tree/main/plugins/power-automate)) | `az login` plus MSAL | Optional after a spike; builders first |

Night default: pac plus trusted helper scripts for the Web API. Any write through MCP still changes the environment, so the lane drift check catches it if it skips the builders.

**Microsoft's skill plugins.** `microsoft/power-platform-skills` ships 11 plugins for Copilot CLI and Claude Code, MIT-licensed, and its installer also installs pac and enables auto-update ([README](https://github.com/microsoft/power-platform-skills)). `microsoft/Dataverse-skills` adds `dv-connect`, `dv-query`, `dv-data`, `dv-metadata`, `dv-solution`, `dv-security` and more ([README](https://github.com/microsoft/Dataverse-skills)). Rules: vendor and pin a commit; turn telemetry off with `POWER_PLATFORM_SKILLS_TELEMETRY_<PLUGIN>_OPTOUT`; review each version before adoption, because agents execute this code; treat `code-apps-preview` and `pcf` as preview.

**What still needs the portal, and therefore PARKs or stays in bootstrap.**

| Step | Why | Where it goes |
|---|---|---|
| OAuth connections and consent (Teams, Outlook, most Microsoft 365 connectors) | Needs an interactive sign-in | Bootstrap; a new one at night PARKs |
| Copilot Studio connection consent | "Complete any required sign-in or consent through the supported interactive experience" ([Copilot Studio MCP](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/copilot-studio-mcp)) | PARK |
| Tenant management app registration | Admin with username and password | Platform team, once |
| First share of a code app to the service principal | "A service principal can't grant itself access" | PARK on first publish |
| Canvas app authoring | `.pa.yaml` files are "read-only and can't be modified"; supported AI authoring needs a live Studio tab ([canvas source](https://learn.microsoft.com/power-apps/maker/canvas-apps/power-apps-yaml)) | Day work |
| Enabling features per environment (code apps, MCP clients) | Admin centre settings | Bootstrap |
| Admin consent for API permissions | Entra admin | Bootstrap |
| Copilot Studio agent accounts and agent identities | Created in the portal; you "cannot bring your own" ([agent identities](https://learn.microsoft.com/microsoft-copilot-studio/govern-agents-identities-overview)) | PARK |
| Evaluation of new-harness Copilot Studio agents | Preview UI only, no API | Human check in the morning |
| Direct Line secured access changes | "can take up to two hours" to take effect ([web security](https://learn.microsoft.com/microsoft-copilot-studio/configure-web-security) [snippet]) | Bootstrap |
| Flow designer test pane, Studio accessibility checker | Interactive only | Replaced by scenario tests and solution checker |


### 5.7 The gate: a required workflow in a separate repo

The uploaded plan's PR checks ran the agent's own scripts from the PR branch, with `id-token: write` against the Dataverse app registration. So the agent could edit the checks it is judged by, while the job held real credentials. The fix has three parts.

**1. The gate lives where the agent cannot write.** `lcp-gate.yml` sits in `getai/factory-gates` on a protected `release` branch. An organisation ruleset, "Require workflows to pass before merging", applies it to every repo with the custom property `factory=enabled`. Ruleset workflows run only on `pull_request`, `pull_request_target` and `merge_group` with default activity types, and their `branches`, `paths` and `types` filters are ignored. Inside them, the only CodeQL action that works is `upload-sarif` ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)).

**2. Credentials and untrusted code never share a job.**

| Job | Runs PR code? | Credentials | Purpose |
|---|---|---|---|
| `map` | No | None | Lane from the branch name `agent/fl<n>/<ado-id>-<attempt>`, validated against an allowed list |
| `locks` | No | None | Second lock on protected paths; locked scenarios and the spec unchanged against the base |
| `build` | **Yes** (builders) | **None**: `contents: read`, no `id-token` | Builders, `git diff --exit-code`, offline `pac solution pack` and `pac copilot pack`. Uploads the zips |
| `static` | No | Read-only gate App token | Trusted scripts from the gate repo, hash-checked, read the PR files and zips as data: manifest check, lints, criteria trace |
| `verify-in-test` | No (locked tests are proven unchanged by `locks`) | `getai-<proj>-test` over OIDC, pinned to the gate workflow; test user certificate | Plan against the Test baseline, solution checker SARIF, import, locked scenarios, Playwright, Copilot Studio conversations, held-out set, evaluator |
| `danger` | No | Job token with `checks: write`; Copilot requests | Deterministic floor, raise-only review agent, merge policy |

Trusted scripts from the uploaded plan move into the gate repo: `run_workflow.py`, `lint_logic_apps.py` (fails on an `if()` expression over 8,192 characters or unsafe substrings), `check_root_components.py`, `create_schema.py --plan`, `create_security.py --plan`, `sync_solutions.py` and `reset_environment.py`. New trusted scripts: the manifest check, a static-results lint, a `.pa.yaml` schema lint against Microsoft's published schema ([canvas source](https://learn.microsoft.com/power-apps/maker/canvas-apps/power-apps-yaml)), an accessible-label lint, a criteria-to-scenario trace, the Merge Danger floor and the merge policy. The gate verifies a `scripts.sha256` manifest before running any of them.

**3. Rulesets lock the paths, the branches and the bypass list,** following V2.1's stack ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)):

- **`main-gate`**: empty bypass list; no deletions or force pushes; linear history; at least 1 approval, stale approvals dismissed, code owner review, approval of the most recent push; pinned checks; merge queue.
- **`integration-gate`**: 1 approval in Phases 1 to 3; pinned checks `lcp-gate` and `lane/drift`; merge queue. Phase 4 changes in section 5.10.
- **`protected-paths`** (push ruleset): `tests/acceptance/**`, `tests/scenarios/**`, `specs/*/spec.md`, `specs/*/checklists/**`, `.specify/**`, `.github/**`, `AGENTS.md`, `CLAUDE.md`, `.claude/**`, `.mcp/**`, `scripts/**`, `builders/lib/**`, `deploy/**`. Bypass: `@acceptance-owners` and the platform team only.
- **`factory-required-workflows`** (organisation) as above. A nightly audit fails the kickoff if any App, machine account, the write role or Copilot appears in a bypass list. GitHub's docs suggest adding Copilot as a bypass actor when a ruleset blocks it: that is the trap.

**A refinement of the review's fix.** The review listed `workflows/build/` among the push-protected paths. In the uploaded repo those are the per-component builders: the agent must edit them to change any flow. So this plan protects the shared builder library (`builders/lib/**`) and every check script, and leaves per-component builders writable. Every builder change gets a Merge Danger floor of at least 3, so a human always merges it. The intent of the fix holds: the agent cannot edit any check it is judged by, because the builder check proves only that generated files match their builders.

**GitHub environments.** One per identity: `fl1-exec` to `fl3-exec`, `fl1-verify` to `fl3-verify`, `lcp-test`, `uat`, `prod`. Deployment branch rules restrict `uat` and `prod` to `main` and the release workflow, with required reviewers and "Prevent self-review" on ([environments](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/deployments-and-environments)). Branch rules do not fit PR-triggered gate jobs, so the gate's own protection comes from the `job_workflow_ref` subject pin (section 5.3).

Appendix A has the YAML. It is a starting point and untested.

### 5.8 Locked acceptance scenarios and the held-out set

**Who writes them.** A test author who is not the worker: a person, or the `test-author` agent in its own day session that sees the spec but no implementation. `@acceptance-owners` review and merge them. The spec owner checks that they match the intent. For Copilot Studio agents, the agent's business owner writes the conversations.

**What they are.**

| Type | Format | Location | Runs as |
|---|---|---|---|
| Workflow scenarios (`run_workflow.py`) | YAML: seed data with a run tag, trigger (HTTP or Dataverse row), expected side effects, cleanup | `tests/scenarios/*.yaml` | `getai-<proj>-test` over the Web API |
| Server logic | Web API integration tests for plug-ins, low-code plug-ins and entity-scoped business rules; assert computed fields and `plugintracelogs` | `tests/acceptance/api/` | Same |
| UI | Playwright TypeScript on Microsoft's toolkit (`CanvasAppPage`, `ModelDrivenAppPage`, `GridComponent`, `FormComponent`) ([canvas](https://learn.microsoft.com/power-platform/developer/playwright-samples/canvas-application); [model-driven](https://learn.microsoft.com/power-platform/developer/playwright-samples/model-driven-application)) | `tests/acceptance/ui/*.spec.ts` | Certificate test user |
| Copilot Studio conversations | YAML scripts: turns, expected keywords or attachments, expected tools, rubric reference | `tests/acceptance/agents/*.yaml` | Direct Line runner in the gate |
| Copilot Studio built-in test sets | CSV with Question and Expected response; up to 100 single-response cases or 20 conversations of up to 12 messages ([single response](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-create); [conversation](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-multi-turn)) | Kept in the repo; created in `factory-test` by the test owner | Test user |
| Held-out set | All of the above, for the same stories | Private `factory-holdout` repo, readable only by the gate's held-out reader App | Same; only aggregate scores and failing case IDs return to the PR |

**Selector rule.** Canvas controls carry `data-control-name`, which "matches the control name you set in Power Apps Studio" ([canvas](https://learn.microsoft.com/power-platform/developer/playwright-samples/canvas-application)). So the spec's testability contract names the required controls and their accessible labels, and locked tests select by accessible name first. That breaks a test, correctly, if the agent renames a control, and it doubles as an accessibility check.

**Why a separate Test environment.** Built-in Copilot Studio test sets are visible to "Any maker with access to the agent", and evaluation "runs as the currently signed-in user" ([about agent evaluation](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro)). The execution identity has maker rights in its lane. So scenarios run in `factory-test`, where the worker has no access: the PR's managed solution is imported, then tested by a separate identity and a separate test user.

**Rough run times per PR (estimates, not measured).** From the Power Platform testing notes ([canvas timings](https://learn.microsoft.com/power-platform/developer/playwright-samples/canvas-application)):

| Step | Estimate |
|---|---|
| Solution import into Test | 3 to 10 minutes |
| Solution checker | 2 to 5 minutes |
| Web API integration tests | 1 to 3 minutes |
| 10 to 20 Playwright scenarios on 2 to 4 workers | 5 to 15 minutes (canvas apps with Dataverse data can take 30 to 60 seconds to load; `directUrl` saves 10 to 20 seconds a test) |
| Flow scenario tests (polling) | 2 to 10 minutes |
| Copilot Studio scripted conversations, 20 to 50 turns, plus judge calls | 3 to 10 minutes |
| Built-in evaluation of 100 cases | "several minutes" or more |
| **Total** | **about 20 to 45 minutes** |

**Flakiness controls.** One UI retry with a trace on the first retry. Unique run tags on all data. Serial execution for tests that share a record type. A three-run majority for generative grades. A nightly sweeper for leftover tagged rows. Rotate a share of held-out cases each month.

### 5.9 The evaluator for Power Platform

Deterministic checks run first. The evaluator runs second, in a fresh session, against the app the PR built. It can block a PR with evidence. It can never pass a PR that a deterministic check failed.

**Canvas and model-driven apps: click-through.** A fresh Copilot CLI session with the read-only `lcp-evaluator` agent and Playwright MCP, loaded with the test user's storage state, against `factory-test`. It gets the spec, `contract.md`, the rubric skills (`rubric-lcp-app`, `rubric-lcp-flow`, `rubric-copilot-agent`), the held-out user stories in plain language, and a time box. It must save a Playwright trace and a screenshot for every claim it makes. Microsoft supports Playwright MCP for authoring tests against a live app with GitHub Copilot and Claude Code ([AI-assisted testing](https://learn.microsoft.com/power-platform/developer/playwright-samples/ai-overview)); using it to grade is our design [inference]. It never sees `learnings.json`, transcripts or session state.

**Flows: scenarios through HTTP or Dataverse triggers.** There is no headless unit-test runner for cloud flows, so test them black-box. Seed data with a unique run tag. Trigger by POST to an HTTP trigger restricted to "Specific users" (the object ID of `getai-<proj>-test`, token audience exactly `https://service.flow.microsoft.com/`) ([OAuth for HTTP triggers](https://learn.microsoft.com/power-automate/oauth-authentication)), or by writing the Dataverse row the trigger watches. Poll Dataverse for the side effect. Check the `FlowRun` row as a secondary signal only: its ingest "isn't transactional, and hence isn't 100 percent lossless" ([flow run history](https://learn.microsoft.com/power-automate/dataverse/cloud-flow-run-metadata)), so a missing row is "unknown", not "fail". Delete everything with the run tag. Point email, Teams and approval connectors at test mailboxes through environment variables. Static results ("beaker" mocks) live in the flow definition ([test cloud flows](https://learn.microsoft.com/power-automate/guidance/coding-guidelines/test-cloud-flows)), so a trusted lint fails any PR that ships them [inference: the JSON key is unconfirmed].

**Plug-ins and business rules.** "Microsoft Dataverse doesn't provide testing framework tools" ([testing tools](https://learn.microsoft.com/power-apps/developer/data-platform/testing-tools-server)). Locked tests are Web API integration tests that create a row, read it back, assert computed fields and query `plugintracelogs` ([debug plug-ins](https://learn.microsoft.com/power-apps/developer/data-platform/debug-plug-in)). Plug-ins target .NET Framework, so unit tests with FakeXrmEasy need a Windows runner and probably a commercial licence [unverified]; or keep business logic in a separate .NET 8 library that runs on Linux. Form-scoped business rules fire only in the UI, so they get a Playwright `FormComponent` test.

**Copilot Studio agents.**

- **Standard harness, primary: a Direct Line runner in the gate.** It sends locked scripted turns, asserts deterministically on text, attachments and tools seen, then calls an LLM judge with a locked rubric, using a three-run majority for generative answers ([Direct Line testing](https://learn.microsoft.com/microsoft-copilot-studio/guidance/conversational-agents-performance-testing-direct-line) [snippet]). Seeing which tools ran may need Dataverse transcripts or Application Insights.
- **Standard harness, secondary: built-in evaluation.** Exact match, Keyword match and Tool use are deterministic; General quality, Compare meaning and Custom are AI-graded ([single response](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-create)). Run with `pac copilot-studio run-maker-evaluation-test-set` (preview) ([pac copilot-studio](https://learn.microsoft.com/power-platform/developer/cli/reference/copilot-studio)) or REST, which needs "A user access token" ([REST API](https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-rest-api)); app tokens are a stage 0 test. No command imports test sets, so the test owner creates them in Test. Results last 89 days; export them. The Agent Kit's deterministic Plan Validation is optional ([Kit tests](https://learn.microsoft.com/microsoft-copilot-studio/guidance/kit-configure-tests)).
- **New GitHub Copilot harness: human.** "Currently, the only available test method is General quality", it supports only "No authentication" or "Authenticate with Microsoft", and no API is documented ([evaluate (preview)](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro)). The Microsoft 365 Agent Evaluations CLI targets declarative agents and assumes Windows ([quickstart](https://learn.microsoft.com/microsoft-365/copilot/extensibility/evaluations-cli-quickstart)), so it is not used.

So the uploaded plan's "5 minutes in the test pane" mostly goes away for standard-harness agents. It becomes a 1 to 2 minute read of a graded transcript bundle, plus the human checks below.

**Accessibility.** Three layers: `pac solution check` canvas accessibility rules in SARIF, failing at Medium or above; a locked Playwright pass running axe-core inside `iframe[name="fullscreen-app-host"]` or the main form, against a baseline of known platform violations; and a keyboard-only journey. The last two are our design, not Microsoft guidance [inference]. The Studio checker is interactive, and colour contrast "is not automatically checked" ([accessibility checker](https://learn.microsoft.com/power-apps/maker/canvas-apps/accessibility-checker)).

**What stays human.**

| Check | Why |
|---|---|
| Behaviour of new-harness Copilot Studio agents | No API and only General quality |
| Agents set to "Authenticate manually" | Not supported by evaluation |
| First-time connector consent | Interactive by design |
| A spot check of the AI grader's reasoning on failures | Graders drift |
| Design approval of mocks | Taste and brand are the client's call |
| One-way doors (drops, security roles, money logic) | Irreversible |
| UAT sign-off | The client owns acceptance |

**Verdicts.**

| Verdict | Action |
|---|---|
| PASS | Merge Danger runs; the PR waits for the morning, or for auto-merge in Phase 4 |
| NEEDS_WORK | `findings.md` (failed criteria with repro steps and evidence paths) goes back. The story re-queues to the next free lane on the same branch, and that lane resets to the branch's own build, not `integration`. Two rounds at most |
| RESTART | Close the PR. Fresh branch, attempt plus 1, `learnings.json` and the spec carried over, nothing else. One per story per night, and only if the budget covers it |

Caps per story: at most 5 fast-check loops inside a session, two evaluator rounds and one RESTART. After that the story PARKs with type `budget`. RESTART fires when the evaluator asks for it, or when one criterion stays below threshold for two passes [talk 23:08 to 23:42; 47:11].

### 5.10 The review agent and Merge Danger

Merge Danger, blast radius and one-way versus two-way doors make a better morning package than V2.1 had. This plan adopts them for every lane. It also changes how the score is made.

**The floor is deterministic.** A trusted script computes it from three inputs (Appendix B):

1. **Changed paths.** For example: docs and handoff files score 0; additive builder inputs 2; any builder, flow logic or Copilot Studio topic change 3; a new connection reference 5; a security role 7; pipeline settings 9; tests, scripts, workflows, hooks or agent instructions 10, and they are protected.
2. **Plan output.** `create_schema.py --plan` and `create_security.py --plan`, run against the Test baseline, flag type changes (6), privilege changes (7 or 8), column drops (8) and table drops (9). That makes one-way-door detection deterministic.
3. **Gate results.** Any checker finding at High, any drift or any held-out failure raises the floor.

**The LLM may only raise it.** The review agent (`lcp-reviewer`, read-only, fresh session) reads the diff, both plans, the evidence, `AGENTS.md` and the spec. It checks builder correspondence, scenario coverage, the architectural decision records and code smells, and out-of-scope changes. It may raise the score, with a written reason. Final score = max(floor, LLM score). Its output is JSON plus a check run and a comment. It never submits a PR review.

**Thresholds** (kept from the uploaded plan):

| Score | Band | Merge |
|---|---|---|
| 0 to 2 | Low | Human in Phases 1 to 3. Phase 4: auto-merge into `integration` if eligible |
| 3 to 5 | Medium | Human, with a blast radius summary |
| 6 to 10 | High | Human, with a blast radius summary and the one-way door called out; a second reviewer for 8 and above on client work |

**Auto-merge rules.**

- Only into `integration`. Never into `main` or anything that deploys to UAT or Prod.
- Only when the final score is 2 or less and every check is green, including `lane/drift`.
- Never when the PR touches tests, scripts, builders, workflows, hooks, `AGENTS.md`, `CLAUDE.md`, agent definitions, skills, pipeline settings or credentials, whatever the score.
- Never on a date. Phase 4 starts per project when all of these hold:
  - 30 days of escaped-defect data from merged factory PRs;
  - evaluator-human agreement at target (80%, an assumption) for four consecutive weeks;
  - zero tampering detections in those 30 days, with the weekly seeded-violation test passing;
  - a held-out pass rate stable within 5 points for four weeks;
  - fewer than 2% of factory PRs reverted within 30 days;
  - the deterministic floor running unchanged for 30 days;
  - Boroon's written sign-off.
- Exit Phase 4 at once on any escaped defect from an auto-merged PR, then re-enter on the same criteria.

**How the rules are enforced without a bypass** [untested; stage 7]. In Phase 4, `integration-gate` drops to 0 required approvals but keeps "Require review from Code Owners". `CODEOWNERS` on `integration` assigns `@factory-reviewers` to every path whose floor is 3 or more, so the native rule forces a human there. For a score raised by a plan or by the LLM, the `merge-policy` step fails with "Human merge required: score N". A reviewer approves, then re-runs that job, which passes once it finds an approving review from `@factory-reviewers` on the head commit. Re-running is needed because ruleset workflows do not trigger on review events. The `factory-merger` App then enqueues the PR. No identity sits in a bypass list.

**The morning package per PR.** What was built, in two lines. Evidence links with SHA-256 hashes from the evaluator's job (Playwright HTML report, JUnit XML, `trace.zip`, screenshots, SARIF, evaluation JSON, `FlowRun` and `plugintracelogs` query results). Score with the floor and LLM parts and their reasons. One-way or two-way door. Blast radius: tables, flows, apps, agents, roles and integrations touched, and who uses them. Held-out pass rate as numbers only. Items that need a human (section 5.9). Cost of the story at list and cash.

### 5.11 The ADO state machine and the PARK protocol

**The orchestrator owns state, not the agent.** GHE.com webhooks go to an Azure Function in `factory-control`, which writes ADO through its REST API as the orchestrator service principal. ADO accepting an Entra service principal is our understanding [unverified; stage 0]. The agent never writes ADO; it writes files the orchestrator reads. Whether the Azure Boards app links work with GHE.com was not researched, so the orchestrator also writes links itself.

| From | To | Trigger | Set by |
|---|---|---|---|
| New | Refining | Spec work starts | Human |
| Refining | Ready to build | Factory Eligible = true (section 6.4) | Human; the orchestrator rejects the change if locked scenarios are missing |
| Ready to build | Queued | Story is in an approved night plan | Orchestrator |
| Queued | Building | Branch `agent/fl<n>/<ado-id>-<attempt>` created | Orchestrator (webhook) |
| Building | Testing | PR opened | Orchestrator (webhook) |
| Testing | Awaiting review | Gate finished with PASS; score written | Orchestrator |
| Testing | Building | NEEDS_WORK or RESTART within caps | Orchestrator |
| Any night state | Awaiting business | PARK | Orchestrator, from `park.json` |
| Awaiting business | Ready to build | Human resolved the PARK | Human |
| Awaiting review | Integrated | PR merged into `integration` | Orchestrator (webhook) |
| Integrated | UAT Ready | Release PR merged into `main` | Orchestrator |
| UAT Ready | In UAT | UAT deployment succeeded | Orchestrator |
| In UAT | Prod Ready | Client UAT sign-off | Human |
| Prod Ready | Done | Production deployment succeeded | Orchestrator |
| Testing or Awaiting review | Needs rework | Caps exhausted, or a human rejects | Orchestrator or human |

**Custom fields** (full list in Appendix D): Factory Eligible (bool, human), Locked Scenarios Ref (path and hash), Merge Danger Score, Merge Danger Floor, One-Way Door, Blocked Reason, PARK Type, Factory Run Id, Factory Attempts, Factory Lane, Factory Verdict, Factory PR URL, Evidence URL, AI Credits, Cost List USD, Cost Cash USD, Human Minutes, Night Id, Residency Tier.

**The PARK protocol.** When the agent reaches a step it may not do, it stops. It does not invent inputs or work around the requirement.

1. It writes `handoff/<ado-id>/park.json`: `type` (portal_step, design_approval, ambiguity, one_way_door, budget), `instruction` (exact steps for a human), `evidence` (paths), `resume_hint`.
2. It prints `PARK: <instruction>` as its last line and ends the session. The driver exits with code 3.
3. The driver commits the work so far and pushes the branch, without opening a PR, so the gate does not run on parked work.
4. The execution workflow reports the PARK to the orchestrator, which sets ADO to "Awaiting business", copies the instruction into Blocked Reason, links the branch, releases the lane and dispatches the next story.
5. In the morning a human does the step, records it in the work item, and sets the story back to "Ready to build". The next night resumes from the branch and the handoff files.

Lane faults are different: a failed preflight marks the lane Offline and raises an ADO bug against the lane, not the story.

### 5.12 Agent instructions

The uploaded plan's prompts become custom agents plus `AGENTS.md` and skills, so Copilot CLI and Claude Code share them. Copilot reads `AGENTS.md` and `CLAUDE.md`, custom agents from `.github/agents/*.agent.md`, and skills from `.github/skills`, `.claude/skills` or `.agents/skills` ([custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration); [cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)). Agent definitions for the evaluator and reviewer load from the gate repo, not the project repo.

| File | Holds |
|---|---|
| `AGENTS.md` (about 100 lines; `CLAUDE.md` points to it) | A map: repo layout, the builder pattern, where scenarios live, the PARK protocol, links to skills. Not a manual |
| `.github/agents/lcp-executor.agent.md` | The execution rules (below) |
| `factory-gates/.github/agents/lcp-evaluator.agent.md` | Harsh grading, evidence for every claim, verdict JSON |
| `factory-gates/.github/agents/lcp-reviewer.agent.md` | Raise-only scoring, builder correspondence, blast radius |
| `.github/skills/` | `builder-pattern`, `dataverse-safe-api` (backoff, batching, run tags), `park-protocol`, `rubric-lcp-app`, `rubric-lcp-flow`, `rubric-copilot-agent`, plus Microsoft's vendored plugins |

The uploaded plan's execution rules all survive in `lcp-executor` (Appendix C.1): code over click-ops with PARK on portal-only steps; never inject identity, rely on `x-ms-object-id`; design first, halting without an approved mock; one branch, now pushed by the driver; and update `state.md` and `docs/lessons-learned.md`. New rules: edit builder inputs, never generated output; never touch protected paths; use the backoff helper; poll Entra changes; stop at the credit cap; PARK on ambiguity and one-way doors. The review prompt's rules survive in `lcp-reviewer` (Appendix C.3).

**Lessons learned are hints, not rules.** The executor reads only the last 50 entries of `docs/lessons-learned.md`. The weekly retro (section 7.3) promotes vetted lessons into `AGENTS.md`, skills or lints by PR. This keeps agent-written text from becoming unreviewed instructions.

**Factory Manifestos.** The uploaded plan's per-practice manifestos become a central `factory-manifestos` repo: per practice, an `AGENTS.md` fragment, skills and a Spec Kit preset, versioned and vendored into project repos. The five practices share the gate.

Appendix C has the full definitions.

### 5.13 Throttling, Entra eventual consistency and backoff

- **Service protection limits are per user, per web server, over 300 seconds:** 6,000 requests, 1,200 seconds of combined execution time, and 52 concurrent requests. "Are limits applied differently for application users? No." Solution imports "can be very demanding" ([API limits](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits)). Per-lane application users therefore give each lane its own budget, so one lane's import cannot throttle another.
- **The daily pool is per tenant.** All application users share the non-licensed pool: 25,000 requests per 24 hours on a Power Apps or Power Automate tenant, or 500,000 plus 5,000 per user licence on Dynamics 365 Enterprise tenants. "Does each application user ... get their own tenant-level limit? No" ([request limits](https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations)). Enforcement is still in a "transition period", but plan for it: preflight reads usage by Caller Type, and a lane pauses its data seeding above 70% of the pool (assumption).
- **The backoff helper (a skill plus a library).** Honour `Retry-After` on HTTP 429. Cap concurrency per identity at 8 to 16, well below 52. Start batches at 10 operations (maximum 1,000). Serialise solution imports per environment. Treat the three error codes (`0x80072322`, `0x80072321`, `0x80072326`) as retryable.
- **Entra eventual consistency.** The uploaded plan says a new group or app role can take 5 to 15 minutes to propagate [unverified]. Scripts that touch Entra poll for the expected state with a deadline before any dependent test runs. A timeout PARKs the story and flags the lane for the morning, rather than failing the test.

### 5.14 Licensing and capacity

- **Application users need no licence, and cannot have one** ([create SP](https://learn.microsoft.com/power-platform/admin/powerplatform-api-create-service-principal)).
- **Managed Environments need premium licences for all active use:** "all active usage requires one of these standalone licenses or pay-as-you-go meters" ([Managed Environment licensing](https://learn.microsoft.com/power-platform/admin/managed-environment-licensing)). Every human who opens apps in a lane, Test, UAT or Prod, and the test user, needs Power Apps Premium or Power Automate Premium. Reviewers who only read GitHub need nothing. From February 2027, users without the right licence "can't open and use the app" ([licensing FAQ](https://learn.microsoft.com/power-platform/admin/powerapps-licensing-faq)).
- **Pipelines** need Managed Environments and premium licences for every target ([pipelines](https://learn.microsoft.com/power-platform/alm/pipelines)). **Code apps** need Power Apps Premium, pay-as-you-go or an App Pass for end users ([code apps](https://learn.microsoft.com/power-apps/developer/code-apps/overview)).
- **Service-principal-owned premium flows** need a Process licence, a flow group, or a designated licensed user with Power Automate Premium, or they can be suspended as "not compliant" ([SP-owned flows](https://learn.microsoft.com/power-automate/service-principal-support)). Use a licensed human as the designated user in lanes and Test, and a Process licence (environment-specific) or flow group in Prod.
- **Capacity.** Each sandbox or production environment needs at least 1 GB of free database capacity to be created, copied or restored ([create environment](https://learn.microsoft.com/power-platform/admin/create-environment)). Six environments need at least 6 GB just to exist, plus real use, against a 10 GB tenant default plus accrual per licence ([licensing FAQ](https://learn.microsoft.com/power-platform/admin/powerapps-flow-licensing-faq#dataverse)). The sources conflict on accrual (250 MB or 50 MB per Premium user); check the admin centre. Auditing uses Log capacity, which defaults low, so keep audit retention short in lanes.
- **Other meters.** Dataverse MCP usage is billed in the environment's tenant. Copilot Studio evaluation and new-harness agents "might consume Copilot Credits". Neither price was researched.
- **Prices.** No Australian dollar prices were gathered. Use the partner price list (section 10.5).

### 5.15 Promotion: Dev to UAT to Prod, with a human at each step

UAT and Prod must be Managed Environments, because pipelines now block unmanaged targets after the grace period (section 1.4). Both run solution checker enforcement at Block, which cancels an import with "highly-critical issues" before any change ([Managed Environment solution checker](https://learn.microsoft.com/power-platform/admin/managed-environment-solution-checker)). That is a second gate the agent cannot skip. To match it in CI, run the checker with no file exclusions or rule overrides.

| | Design A: GitHub Actions does it (default) | Design B: Power Platform pipelines |
|---|---|---|
| Build | Managed zip built from `main` by the trusted builder; `pac solution check` | Same build, then `pac pipeline deploy --wait` ([pac pipeline](https://learn.microsoft.com/power-platform/developer/cli/reference/pipeline)) |
| Approval | GitHub environments `uat` and `prod` with required reviewers and "Prevent self-review" | Delegated deployment: "All delegated deployments are pending until approved" ([delegated deployments](https://learn.microsoft.com/en-us/power-platform/alm/delegated-deployments-setup)), through an `OnApprovalStarted` flow or the admin deployment page ([extend pipelines](https://learn.microsoft.com/en-us/power-platform/alm/extend-pipelines)) |
| Import | `pac solution import --settings-file` as `getai-<proj>-deploy` over OIDC | The pipeline stage deploys as the delegate service principal |
| Secrets | None, if pac federation works on GHE.com | At least one: the approval flow's `UpdateApprovalStatus` must run on a Dataverse connection for the service principal, which "needs a client ID and secret" |
| Strengths | One audit trail in GitHub; works across tenants | The same managed artefact "prohibits any tampering"; the admin deployment hub view |
| Limits | We own the artefact store (Blob, with hashes) | No cross-tenant deploys; personal pipelines cannot be extended; reset lanes break pipeline records |

Use Design A by default. Use Design B when a client wants Power Platform-native governance and accepts one stored secret. Connection references and environment variables come from `pac solution create-settings`, with per-environment values held in `deploy/<env>.settings.json` (protected). A connection reference with no value in the solution or the target "can't be updated during deployment" ([pipelines](https://learn.microsoft.com/power-platform/alm/pipelines)), so preflight checks every reference has a value before promotion.

### 5.16 Residency for the Power Platform lane

Section 9.4 sets the client's tier for the factory engine. Power Platform adds three points:

- **The environments.** The Australia geo keeps "Most customer data ... within Australia, except for Microsoft Entra ID data" ([Microsoft Cloud Australia](https://learn.microsoft.com/power-platform/admin/about-microsoft-cloud-australia)).
- **What the agent sees.** Lanes and Test hold synthetic data only. No client production data enters a factory environment, so the engine sees code, metadata and test data.
- **The deliverable.** A Copilot Studio agent built for a client keeps inference in Australia only with an in-region model and "Move data across regions" off. In Australian environments, GPT models on the standard harness are in-region, while Claude models are "GA (cross-geo)" ([model availability](https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model#model-availability-by-region)). Anthropic models in Microsoft offerings "are currently excluded from the EU Data Boundary, and when applicable, in-country processing commitments" ([Anthropic subprocessor](https://learn.microsoft.com/microsoft-365/copilot/connect-to-ai-subprocessor)). The Power Platform preset records the model and the cross-region setting in the spec.

## 6. The day gate

### 6.1 Spec Kit 1.2 with two presets

Spec Kit replaces a bespoke grill agent. Building our own would be the IKEA trap, and 1.2 answers the ceremony complaint by configuration: presets, a lean preset, custom workflows and bundles [Spec Kit talk 5:35 to 7:02]. Install with `uv tool install specify-cli`, then `specify init --integration copilot` ([Spec Kit README](https://github.com/github/spec-kit)). Pin 1.2.x in the bundle. Overrides layer as built-in, preset, extension, then project ([artifacts reference](https://raw.githubusercontent.com/github/spec-kit/main/docs/reference/artifacts.md)).

| Step | Spec Kit | Output | Who |
|---|---|---|---|
| Idea assessment | `assess` extension: intake, research, shape, define, decide | Verdict `go`, `kill` or `needs-clarification` | Spec owner answers |
| Specify | `/speckit-specify` | `specs/<NNN-feature>/spec.md` | Spec owner |
| Clarify | `/speckit-clarify`, repeated with focus areas until no material gaps | `## Clarifications` and the ten-category coverage table | Spec owner answers |
| Checklist | `/speckit-checklist`, "unit tests for English" | `checklists/*.md` | A reviewer ticks; agents may not self-approve |
| Analyse | `/speckit-analyze`, read-only | Severity report and coverage map | By day on Lane B; at night on Lane A |
| Scenarios | `test-author` agent or a person | Locked scenarios (section 5.8) | `@acceptance-owners` approve |
| Approve | Spec PR, gate script as a CI check and a mandatory `before_implement` hook | Factory Eligible in ADO | `@acceptance-owners` |

Sources: [clarify template](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/clarify.md); [checklist template](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/checklist.md); [analyze template](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/analyze.md).

Rules carried from V2.1: a `kill` verdict is the cheapest outcome in the factory. The GET AI preset raises Spec Kit's question caps (five per clarify session, three markers in specify), and the owner reruns clarify until nothing that matters is Partial or Missing. The deterministic gate script checks the criteria floor, open markers, NFR coverage, approved assumptions and (new) the Power Platform fields below; its hook runs with `optional: false`, because it "must be actually run, not just announced" ([implement template](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/implement.md)). Approval needs every checklist ticked, or implement stops to ask. Skip the experimental MCP server mode [Spec Kit talk 10:38 to 11:17], and turn off `update-agent-context`, which writes to a protected file.

### 6.2 The GET AI preset (unchanged from V2.1)

A constitution (tests and docs for every change, locked acceptance tests, evidence rules); the spec rules in section 6.6; an NFR section, which the core template lacks; raised question caps; the lane field and the ambition setting; and Australian English, since presets can change all artefact output [Spec Kit talk 39:13 to 43:38]. Candidate regulated presets (APRA CPS 234, APRA CPS 230, the ACSC Essential Eight, the Australian Privacy Principles) remain candidates until a qualified reviewer maps them.

### 6.3 The Power Platform preset (`getai-lcp`)

It adds a section to the spec template, a checklist and gate-script rules. Each field must be filled or marked "not applicable" with a reason.

| Field | What the spec records | Why |
|---|---|---|
| Solution boundaries | Target solution, publisher prefix, and whether the story may add a new solution | Stops components leaking into the wrong root solution (`check_root_components.py`) |
| Data model intent | Tables and columns in business terms, and whether any change is destructive | Feeds the `--plan` check; flags one-way doors before the night |
| Connection references | Each connector, its auth type, and whether it needs OAuth consent | OAuth ones must be bootstrapped or listed as a PARK step |
| Environment variables | Name, type, and a value per environment (lane, Test, UAT, Prod) | Feeds `pac solution create-settings` and promotion |
| Security roles | Which roles change, at what privilege depth | Always a floor of 7; a human reviews |
| Design-first mock | Link to the approved mock for any user-facing change: screens, adaptive cards, agent wording | The executor halts without it |
| Testability contract | Control names (`data-control-name`), accessible labels, schema names, flow names, HTTP trigger audience | Locked tests target these |
| Acceptance scenarios | IDs of `run_workflow` scenarios, Playwright specs and Copilot Studio test sets, each mapped to a criterion | Factory Eligible requires them |
| Copilot Studio agent | Harness (standard only for the factory), primary model, "Move data across regions" setting, authentication mode | New-harness and manual-auth agents need human checks (section 5.9) |
| Residency tier | The client's tier (section 9.4) | Decides the engine and whether the factory may run at all |
| Licence impact | Premium connectors, code apps, service-principal-owned premium flows | Avoids flow suspension and surprise licence cost |
| Lane and ambition | `lane: B`, `profile: lcp`, ambition low by default for client work | Routing and scope control |

### 6.4 "Factory Eligible" in ADO

The uploaded plan had a human set Factory Eligible "when acceptance criteria are complete". It now means all of these, and the orchestrator rejects the flag if any is missing:

1. The spec passed the gate script, with no open markers and every checklist ticked.
2. **Locked acceptance scenarios exist,** written by someone other than the worker, merged to the protected paths, with their hash recorded in "Locked Scenarios Ref".
3. A held-out counterpart exists in `factory-holdout`.
4. Any user-facing change has an approved mock linked.
5. Every OAuth or consent prerequisite is bootstrapped, or listed as a PARK step.
6. The residency tier allows factory work.

### 6.5 Intake: the optional Copilot Studio front door

Part A's intake survives as an option for business users. A Copilot Studio intake agent asks clarifying questions, builds `glossary.md`, names the practice, and hands a JSON payload to the Wayfinder planning agent. Wayfinder drafts the Epic and stories in ADO with predecessor links. Then the normal day gate runs: idea assessment, specify and clarify on Spec Kit, scenarios, approval. Wayfinder output is a draft, never a night input.

Two changes from Part A. The "Chief of Staff" orchestrator on Foundry and Microsoft Agent Framework is dropped: Actions, ADO and the agent runtime already do that job, so building it is the IKEA trap. And "Azure AutoGen" is not a product: Microsoft Agent Framework is "the direct successor" to Semantic Kernel and AutoGen, and "focuses on single-process composition today; distributed execution is planned" ([Agent Framework overview](https://learn.microsoft.com/agent-framework/overview/); [AutoGen migration guide](https://learn.microsoft.com/agent-framework/migration-guide/from-autogen/)). Azure AI Foundry is now Microsoft Foundry.

For client PMs, Spec Kit's canvases in the GitHub Copilot app are a second front door [Spec Kit talk 26:40 to 36:11]. They need the app and a seat, and the canvas generator is experimental.

### 6.6 Spec level: what and why, not how

- Stories say what users need and why, plus acceptance scenarios. Spec Kit's split agrees: the spec holds "WHAT users need and WHY" ([specify template](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/specify.md)).
- Wayfinder may write granular, dependency-linked stories. It may not write technical step lists. Granular up-front technical plans cascade errors [talk 24:12 to 24:46].
- Technical design appears only as a hard constraint: stack, identity, data residency, solution boundaries, a client integration.
- The gate script warns when a spec names libraries, schemas or file layouts outside its Constraints section.
- Lane A specs need at least 20 testable criteria. Lane B, both profiles, has no floor, but every criterion needs an executable scenario.
- Clarify happens by day only. A night agent that hits a material ambiguity writes `handoff/<ado-id>/questions.md` and PARKs with type `ambiguity`.

## 7. Handoff files, traces, and the weekly calibration and retro

### 7.1 Handoff files

Every task or story branch carries this set, so a restarted session, a resumed replica, a morning human or a PARK resume can pick up the work [talk 54:08 to 56:04]. It merges V2.1's set with the uploaded plan's `state.md` and `docs/lessons-learned.md`. Lane B stories use `handoff/<ado-id>/`; Lane A builds use `handoff/<task>/`.

| File | Written by | Purpose | Lanes |
|---|---|---|---|
| `specs/<NNN>/spec.md`, `checklists/` | Approved by day | Frozen by the push ruleset and the `locks` job | All |
| `specs/<NNN>/plan.md`, `tasks.md` | Generator at night (A); lean preset by day (B) | The how; converge appends to `tasks.md` | All |
| `handoff/<id>/state.md` | Executor | Every change applied to the lane environment, with the command used. Read by the drift check, the reset and a resuming agent | B Power Platform |
| `handoff/<id>/park.json` | Executor | PARK type, exact instruction, evidence, resume hint (section 5.11) | All |
| `handoff/<id>/questions.md` | Any night agent | Material ambiguities for the morning | All |
| `handoff/<id>/contract.md` | Generator and evaluator | Criteria beyond the locked tests; add or tighten, never remove | A; optional on B |
| `handoff/<id>/learnings.json` | Executor or generator | Timestamped log: tried, evaluator found, fix, worked. JSON because models overwrite it less [talk 12:05 to 14:20] | All |
| `handoff/<id>/findings.md` | Driver, from evaluator output | Latest verdict, scores, failed criteria with repro steps | All |
| `handoff/<id>/evidence/` | Gate and driver | Playwright traces, screenshots, SARIF, evaluation JSON, `FlowRun` and trace-log query results, scores, SHA-256 list | All |
| `docs/architecture.md` | Generator or executor | Living, high-level map of the solution | All |
| `docs/lessons-learned.md` | Executor appends | Gotchas, as hints only; curated weekly (section 5.12) | B Power Platform |

**Spec retention.** Spec Kit's maintainer sees specs as "mostly transient" [Spec Kit talk 14:56 to 15:51], and Spec Kit "names no default" persistence model ([spec persistence](https://raw.githubusercontent.com/github/spec-kit/main/docs/concepts/spec-persistence.md)). Client delivery needs traceability, so archive each feature's assessment, spec, clarifications, checklists, `analyze` and converge reports, scenarios and evidence to Blob, with a traceability matrix: criterion, scenario, story, PR, evidence. Decide per client whether `specs/` stays on `main`.

### 7.2 Traces to Blob, keyed by `run_id`

`run_id = {project}-{yyyymmdd}-{story}-{role}-{attempt}`, for example `p042-20261103-48213-executor-1`. RESTART increments `attempt`.

- **Copilot CLI and SDK runs** (Lane A, the Power Platform executor, every evaluator, the reviewer, the trace reviewer) run with `COPILOT_OTEL_ENABLED=true`, exporting to Application Insights in Australia East ([SDK OpenTelemetry](https://docs.github.com/en/copilot/how-tos/copilot-sdk/observability/opentelemetry); [OTLP ingestion](https://learn.microsoft.com/azure/azure-monitor/containers/opentelemetry-protocol-ingestion)). `OTEL_RESOURCE_ATTRIBUTES` carries `project`, `run_id`, `story_id`, `lane`, `profile` and `role`.
- **Content capture** (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`) is on for factory runs only, never for human sessions.
- **Transcripts.** Each run's `events.jsonl` and `--share` transcript go to Blob ([CLI programmatic reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference)). Lane B code-profile workers on the cloud agent have no OpenTelemetry, so their trace is `gh agent-task view --log` ([cloud agent CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli)).
- **What the night report copies, per story:** PR metadata, checks, review comments, the transcript, the handoff files, the evidence folder with its SHA-256 list, and the ledger rows. One Blob container per project, Australia East. A second copy as an Actions artefact at 400 days.
- **Why now.** Runner disks vanish, retention now deletes checks and runs (section 1.4), the audit log keeps Git events only 7 days ([audit log streaming](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise)), and ACA keeps only the last 100 executions ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs)).
- **The data risk.** Captured content can include client metadata and secrets. Short retention on content tables. Azure RBAC limited to the factory team. In Mode B, one Application Insights resource per client project, in that client's subscription where the contract asks. Every injected secret in `--secret-env-vars`. Check in stage 0 that redaction covers traces.

### 7.3 One weekly routine: calibration plus the Retro Loop

The uploaded plan's Retro Loop (AI Managed Services runs a Retro skill over the logs and turns repeated mistakes into manifesto updates) and V2.1's weekly calibration do the same job. Run them as one 90-minute session, owned by AI Managed Services with the factory owner.

1. **Grade the evaluator.** Sample 10 evaluator verdicts across lanes and all three verdicts. A human grades each one blind. Track agreement on the verdict and the score gap per criterion. Target 80% (assumption). Microsoft's own Copilot Agent Kit guidance suggests iterating rubrics "until alignment is 80-90% or higher" ([rubrics](https://learn.microsoft.com/microsoft-copilot-studio/guidance/kit-rubrics-tests)).
2. **Read the traces behind every disagreement**, and at least one failed trace in full [talk 73:25 to 74:41].
3. **Retro.** The `retro` skill clusters the week's repeated mistakes: NEEDS_WORK findings, PARK reasons, drift detections, human rejections, `lessons-learned.md` entries and trace-review drafts.
4. **Decide.** Each cluster becomes one of: a prompt or rubric change, a new lint or scenario, a skill change, a preset change, or "the model needs this; keep the scaffolding". Raise them as ADO items against `factory-manifestos` or `factory-gates`.
5. **Change by PR only.** Agents and skills load from the default branch, so every change is reviewed. Record `evaluator_version` as the commit SHA of the evaluator agent and its rubric skills. Re-run a new evaluator version on the graded set before merging it.
6. **Seed a violation.** Once a week, seed an edit to a protected path, a fake bypass entry and a weakened scenario. Confirm the gate catches all three. A hook that held for one constructed test but not in natural trials has been reported ([arXiv 2608.23616](https://arxiv.org/pdf/2608.23616) [snippet]).
7. **Update the indicators** in the matrix (section 10.3), and check the Phase 4 entry criteria per project.
8. **Monthly:** the component register review (section 8.2).

This shows engineers that the factory learns from their corrections, which is the trust argument in the uploaded plan.

## 8. Harness parity and the component register

The aim is to use what Microsoft and GitHub already ship, keep glue thin, and invest in IP. The IKEA effect is the risk: over-valuing scaffolding we build when the platform ships it, or soon will. "The harness patterns that work tend to get absorbed back into the tools" [talk 37:58 to 38:52].

### 8.1 Parity for the Power Platform lane

| Workshop requirement | Power Platform equivalent | Status | Our fix |
|---|---|---|---|
| High-level planner, then out of the loop [talk 23:59 to 24:56] | Spec Kit plus the `getai-lcp` preset by day; optional Copilot Studio front door | At parity | Preset fields (section 6.3) |
| One bounded worker per story | Copilot CLI autopilot with the `lcp-executor` agent and Microsoft's skill plugins | At parity | Lane lock, credit cap, 5-loop cap |
| Evaluator that uses the running app [talk 18:42 to 19:31] | Playwright toolkit for Power Platform plus Playwright MCP, against `factory-test` | At parity for canvas and model-driven apps; partial for flows (black-box); gap for new-harness agents | Separate environment and identity; human for new-harness agents |
| Rubrics make taste gradable [talk 21:31 to 22:23] | Skills; Copilot Studio evaluation graders; Agent Kit rubrics | Format at parity; content is ours | `rubric-lcp-app`, `rubric-lcp-flow`, `rubric-copilot-agent` |
| Granular, testable criteria [talk 32:04] | Locked scenarios; built-in evaluation methods; Kit Plan Validation | At parity | Criteria-to-scenario trace in the gate |
| Files as state; structured handoffs [talk 54:08 to 56:04] | Git, the YAML solution format, handoff files | At parity | `state.md`, `park.json` |
| Read the traces [talk 33:51] | OpenTelemetry from Copilot CLI; transcripts | At parity | Trace reviewer; weekly routine |
| Evaluator isolated from the generator [talk 60:03 to 61:04] | Separate session, agent, environment and identity | At parity once wired | Gate repo agents; `preToolUse` deny on `learnings.json` |
| Throw it out and restart [talk 23:08] | Nothing built in | Gap | RESTART: new branch, lane reset |
| Hand back to a human at a stop [talk 46:44] | Nothing built in for Power Platform | Gap | PARK protocol |
| Done decided by someone else | Autopilot ends at `task_complete`, self-declared | Partial | The gate and evaluator decide |
| Deterministic generators | `pac copilot pack`, `pa` codegen, the model-apps App Spec, `pac solution pack` | Shipped | Wrap them; add the manifest check |
| Safe autonomy ("auto mode") | No classifier mode; allow and deny lists, CLI sandboxing, hooks, egress limits, rulesets ([allowing tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools); [local sandboxing](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/understanding-local-sandboxing)) | Gap, rebuilt in layers | Deny `git push`, `pac admin`, `pac auth`; never `--yolo` |
| Delete scaffolding as models improve [talk 34:14] | A process | Process | Register below |

### 8.2 The component register

Review it monthly, in the week after Ignite (17 to 20 November 2026), now for Universe (28 to 29 October 2026), and after each model release.

| Class | Rule | Components |
|---|---|---|
| **Shipped primitive** | Use as is. Do not wrap | V2.1's list (cloud agent, CLI and SDK, custom agents, skills, hooks, Playwright MCP, OpenTelemetry, rulesets, required workflows, merge queue, cost centres, ACA jobs, Key Vault, Blob, Application Insights, Spec Kit core, assess and bug extensions, lean preset). Plus: pac CLI (`solution`, `copilot`, `admin`, `pipeline`, `copilot-studio`); `powerplatform-actions` (`actions-install`); solution checker and Managed Environment enforcement; Power Platform pipelines; the Power Platform Playwright toolkit; Copilot Studio evaluation and the Agent Kit; `power-platform-skills` and `Dataverse-skills`; Dataverse MCP and the Dataverse CLI; the `pa` CLI; Dataverse auditing and Purview; ADO Boards |
| **Thin glue** | Keep small. Expect to delete | V2.1's list. Plus: lane mapping and locks; nightly preflight; per-story reset; the manifest check (until pack fails on missing files); the static-results lint; the Direct Line runner (until evaluation APIs take app tokens and cover the new harness); PARK glue; the ADO state Function (until Boards integration covers GHE.com); the `FlowRun` poller; the merge-policy check (until rulesets can require approval by score) |
| **IP** | Invest | V2.1's list (rubric skills and calibration set, evaluator prompts, trace reviewer and view, ledger and matrix, GET AI preset and bundle, gate script, regression set, gate template). Plus: the `getai-lcp` preset; the environment pool kit; the Power Platform gate workflow and trusted scripts; the Merge Danger rubric and floor; the Playwright kit for Power Platform; Copilot Studio evaluation sets and rubric; deterministic builders where Microsoft has no generator |

For each thin-glue item, ask: does a shipped primitive now do this? If yes, delete it after one regression run.

**The simplification depends on the model.** Anthropic validated the simplified harness on Claude [talk 53:14]. If a role moves to a GPT model (for example through BYOK for an Australian-residency client), re-run the regression set before removing any scaffolding for that role, and re-check rubric weights.

## 9. Credits, billing modes, model choice and data residency

### 9.1 What the designation gives, and the eligibility risk

| Benefit, per year | One Azure-area Solutions Partner designation | Each Azure specialisation (cap of 5) |
|---|---|---|
| Azure bulk credits | USD 10,000 | plus USD 12,000 |
| GitHub Copilot Enterprise (via Azure credits) | USD 5,000 | plus USD 4,680 |
| GitHub Enterprise Metered (via Azure credits) | none | plus USD 2,520 |
| GitHub Enterprise seats or Actions minutes | none | none |

Source: [benefits guide](https://learn.microsoft.com/partner-center/benefits/benefits-at-a-glance). The fee is USD 4,875 a year ([pay the fee](https://learn.microsoft.com/partner-center/membership/mpn-pay-fee-silver-gold-competency)). Credits are yearly, expire with membership, align to the purchase date from 1 November 2026, land on an MCA billing profile with a card attached, and cover first-party Azure only, not Marketplace ([MCA credits](https://learn.microsoft.com/azure/cost-management-billing/benefits/credits/mca-check-azure-credits-balance)). Copilot seats, AI credit overage, Actions and GitHub Enterprise can bill to an Azure subscription connected to the enterprise or a cost centre ([Copilot Azure billing](https://docs.github.com/en/copilot/reference/copilot-billing/azure-billing)). Power Platform licences, Process licences, capacity add-ons and pay-as-you-go meters were not researched against credits.

**The eligibility risk is unchanged and still the biggest.** Microsoft calls partner credits "internal-use-rights credits" ([credits FAQ](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud#azure-credits-faqs-legacy-experience)). Partner Visual Studio subscriptions may not be used to "Develop, test, or maintain applications as part of customer or client projects" ([VS Enterprise for partners](https://learn.microsoft.com/visualstudio/subscriptions/program-mcpp#internal-use-only-restriction)). The binding terms sit in a guide the researchers could not read. Send Partner Center support this question in writing, asking them to cite the Terms of Participation Guide:

> "May GET AI use its Solutions Partner Azure bulk credits and its GitHub Copilot Enterprise (via Azure credits) benefit to pay for GitHub and Azure metered usage that GET AI incurs while delivering a paid client engagement, where the client never receives the credits, the subscription or the GitHub accounts?"

Until the answer arrives, assume no.

### 9.2 Two billing modes, split at the billing boundary

| | Mode A: internal | Mode B: client |
|---|---|---|
| Work | The factory, the accelerator, GET AI IP, internal tools | Client deliverables |
| GitHub | Cost centre `cc-internal-<project>`; for Copilot CLI, the internal organisation or machine account (section 5.2) | Cost centre `cc-<client>-<project>`, tied to the cash subscription; its own organisation or machine account |
| Azure | Subscription on the credited MCA billing profile | Subscription on a separate profile with no credits |
| Power Platform | GET AI's tenant | Usually the client's tenant (section 5.4), so the client pays licences and capacity |
| Funding | Partner credits | Cash, unless the ruling allows credits |
| Ledger | Priced at list for internal ROI | Priced at list; cash equals effective cost |

Subscriptions cannot leave a credited profile while credits are active, so set this split up before the first night.

### 9.3 Model choice

| Path | Billed as | On credits? | Inference region | Use for |
|---|---|---|---|---|
| Claude Sonnet 5.5 or Opus 5.5 through Copilot (CLI, SDK, cloud agent) | GitHub AI credits at the rate table ([rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml)) | Yes, subject to the ruling | Outside Australia (section 9.4) | Default for every role |
| OpenAI models through Copilot | GitHub AI credits | Same | Same | Lane B worker alternative; GPT-6 Luna for chores |
| Copilot CLI or SDK with BYOK to Azure OpenAI, Standard (regional) deployment in Australia East | First-party Azure meter | Yes (Azure credits), subject to the ruling | Australia East | Clients that require in-country inference |
| Azure OpenAI directly (Foundry) | First-party Azure meter ([credit coverage](https://learn.microsoft.com/en-us/microsoft-for-startups/build/foundry-model-sponsorship-coverage)) | Yes | Regional options exist | Calls outside Copilot; the Codex lane |
| Claude in Microsoft Foundry | Marketplace, in Claude Consumption Units; "the credit card will be charged instead of Azure Credits" ([deploy Claude](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-claude)) | No | Global Standard or Data Zone (US); no Australian region ([Claude in Foundry](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models)) | Only on a client mandate, at cash |
| Anthropic API (Claude Code) | Anthropic invoice | No | Offshore | Bake-offs and fallback, at cash |

Pin a model per role. Opus 5.5 for idea assessment and specify. Sonnet 5.5 for the Power Platform executor, with Opus 5.5 for stories marked hard. Sonnet 5.5 for every evaluator, the reviewer and the trace reviewer, so one calibration set covers them. GPT-6 Luna for chores. Microsoft advises "a general-purpose coding model or an advanced reasoning model" for its model-apps skill, not lightweight models ([Learn](https://learn.microsoft.com/power-apps/maker/model-driven-apps/model-driven-app-external-tools)). On credits, get Claude through Copilot, not Foundry: same per-token price, different payer.

### 9.4 Data residency: the facts, and a tier per client

**The facts as of 1 November 2026.**

- **Code and compute can stay in Australia.** GHE.com has an Australia region, with hosted runners in `australiaeast` and `australiacentral` ([GHE.com network details](https://github.com/github/docs/blob/main/content/admin/data-residency/network-details-for-ghecom.md)). Dataverse lanes in the Australia geo keep most customer data in Australia.
- **Copilot inference cannot stay in Australia.** GitHub Copilot with data residency is "currently available in the following regions: United States, European Union", with more "in the near future" and no Australian date. It is enforced by the "Restrict Copilot to data residency compliant models" policy, which changes pricing ([Copilot with data residency](https://raw.githubusercontent.com/github/docs/main/content/admin/data-residency/github-copilot-with-data-residency.md)). The EU list includes Claude Opus 5.5 and Sonnet 5.5. Data-resident requests carry a 10% multiplier ([seats and billing](https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/billing-and-usage/organizations-and-enterprises/seats-and-billing-cycles.md)). Without the policy, Copilot data and logs are "by default stored outside your region" ([data storage](https://github.com/github/docs/blob/main/content/admin/data-residency/about-storage-of-your-data-with-data-residency.md)).
- **Claude has no Australian path.** Claude in Foundry is Global or Data Zone (US) only; the Anthropic API is offshore.
- **BYOK is the only in-country path found.** Copilot CLI and SDK can use your own provider, and user-configured BYOK sends model requests "directly to that provider, rather than through GitHub's Copilot API" ([BYOK](https://github.com/github/docs/blob/main/content/copilot/concepts/models/bring-your-own-key.md)). Point it at an Azure OpenAI Standard (regional) deployment, which is "Processed in the region associated with your deployment"; Global deployments can process anywhere, and Data Zone deployments within US, EU or APAC ([deployment types](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability)). Costs: it bills Azure, not GitHub AI credits; it gives up Claude, so re-run the regression set; enterprise BYOK covers Chat, CLI and IDEs but not the cloud agent. Unknowns: which GPT models are available as Standard in Australia East today, and whether agent metadata or telemetry still goes to GitHub.

**The tier per client.** Record it in the spec (section 6.3) and the project register.

| Tier | Client rule | Engine | Billed | Trade-off |
|---|---|---|---|---|
| **T1** | No inference-location rule for development artefacts; synthetic data only in lanes | Claude through Copilot (default) | AI credits | None beyond the default |
| **T2** | Inference may leave Australia but must stay in the US or EU | Claude through Copilot with the data residency policy on an EU-resident enterprise [unverified: needs a separate EU data-residency enterprise] | AI credits, plus 10% | A second enterprise to run |
| **T3** | Inference must stay in Australia | Copilot CLI with BYOK to Azure OpenAI Standard in Australia East; no cloud agent | Azure (credits in Mode A, cash in Mode B) | GPT only; regression re-run; telemetry path to confirm |
| **T4** | No AI on the client's code or metadata | Not the factory; human-led delivery | n/a | n/a |

Decide the tier before running any client code. The Copilot Studio deliverable has its own rules (section 5.16).

## 10. The cost ledger, profitability matrix and cost envelope

### 10.1 Design principle

Engines report tokens at the client. Billing reports by day and identity, never by run, story or PR ([billing reports](https://docs.github.com/en/billing/reference/billing-reports)). So build the ledger from the client side and reconcile down to each provider's billing grain. Shape it like FOCUS, which carries list, contracted, effective and billed cost on every line ([What is FOCUS](https://learn.microsoft.com/cloud-computing/finops/focus/what-is-focus#benefits)). No FOCUS version has token columns, so map those ourselves.

**What is measured.** Copilot CLI and SDK runs emit `invoke_agent` spans with `github.copilot.nano_aiu` (1 AIU = 1e9 nano AIU), input, output and cache tokens, the agent name (role) and the session ID ([Copilot OpenTelemetry](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)). So the Power Platform lane, Lane A and every evaluator are measured per role per story. Three cautions: `github.copilot.cost` is "Not a monetary value"; confirm `nano_aiu ÷ 1e9` against billing in stage 0; check whether a parent span includes its subagents, so nothing is counted twice. The Lane B cloud agent stays estimated.

### 10.2 Schema

V2.1's tables stay: `dim_project`, `dim_price`, `fact_run`, `fact_usage`, `fact_cost_line`, `fact_human_time`, `fact_outcome`, `fact_spec`, `fact_eval`, `fact_reconciliation`. Store USD and an AUD conversion on every money line. Changes for this plan:

| Table | Change |
|---|---|
| `dim_project` | Add `ado_project`, `residency_tier` (T1 to T4), `platform_tenant` (getai or client), `billing_identity` (org_token or machine_account) |
| `fact_run` | Add `profile` (`code`, `lcp`), `lane_env` (`fl1` to `fl3`, `test`), `ado_id`, `park_type`, `fast_check_loops`, `import_minutes`, `gate_minutes`. Roles add `executor`, `lcp_evaluator`, `lcp_reviewer`, `test_import`, `reset` |
| `fact_outcome` | Add `merge_danger_floor`, `merge_danger_final`, `one_way_door`, `auto_merged`, `drift_detected`, `heldout_pass_rate` |
| New `dim_lane` | Lane code, environment ID, type, tenant, capacity GB, licences assigned, `fixed_monthly_list`, `fixed_monthly_cash` |
| New `fact_fixed_cost` | Monthly Power Platform lines per project: lane and Test licences, test user licence, capacity add-ons, Process licences, Copilot Studio credits, Dataverse MCP usage. Allocated per accepted story |

Category values in `fact_cost_line` add `lcp_licence`, `lcp_capacity`, `lcp_meter` (Copilot Studio credits, Dataverse MCP) and `runner_compute`.

**ADO carries the same numbers.** The orchestrator writes `run_id`, AI credits, list cost, cash cost and human minutes back to each work item (Appendix D), so a project manager sees cost per story without opening Power BI.

### 10.3 Four prices, two rules, one cadence

| Column | Meaning |
|---|---|
| `list_cost` | Published rate, no discounts. **The shadow price.** AI credits at USD 0.01; Actions minutes at USD 0.006 even when included |
| `contracted_cost` | After program discounts, such as Copilot's 10% Auto model discount ([Auto discount](https://raw.githubusercontent.com/github/docs/main/data/reusables/copilot/auto-model-discount.md)) |
| `effective_cost` | After included allowances |
| `cash_cost` | What GET AI pays after partner credits |

- **Each Copilot seat prepays its credits.** Enterprise is USD 39 with 3,900 credits; Business USD 19 with 1,900 ([plan variables](https://raw.githubusercontent.com/github/docs/main/data/variables/copilot.yml)). Post every credit at USD 0.01 and unused included credits as month-end breakage. Never count both.
- **Book partner credits as a funding line, never as a lower cost.** The matrix shows margin twice: at list and at cash.
- **Cadence.** Provisional lines at 05:41 each morning. Reconcile on day 3 per (UTC date, billing identity, model), because Copilot metrics land within two full UTC days ([metrics](https://docs.github.com/en/copilot/concepts/billing-and-usage/copilot-usage-metrics/copilot-metrics)) and Azure tags take up to 24 hours. Pull the provider sum, subtract measured runs, allocate the residual pro rata, and flag a negative residual as measurement drift. Mark lines final at month close. With org-metered CLI runs, nearly everything is measured, so the residual should be small.

**The matrix views** are V2.1's (P&L per accepted unit at list and cash, engine bake-off, night control chart, role cube, credit runway, evaluator health) plus a lane health page: Offline nights, PARKs by type, drift detections, Test queue length and Merge Danger mix.

**Leading indicators to add** for the Power Platform lane (alert levels are assumptions): PARK rate above 25% of stories; drift detections above zero for two nights; Test queue above 5 hours; lane Offline more than once a week; tenant request pool above 70%; evaluator-human agreement below 80%; auto-merged PRs reverted within 30 days above zero.

### 10.4 The Power Platform story model

Everything here is a **model**. Stage 3 calibrates it. Prices from GitHub's [rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml).

**Session sizes, from V2.1.** A heavy 40-minute session reads 6.7M cached and 0.67M uncached input tokens and writes 0.2M output. A light session reads 1.5M input at 80% cache and writes 30K.

- Heavy on Sonnet 5.5 (USD 2.00 in, 0.10 cached, 10.00 out per 1M): 6.7 × 0.10 + 0.67 × 2 + 0.2 × 10 = 0.67 + 1.34 + 2.00 = **USD 4.01**.
- Heavy on Opus 5.5 (USD 4.00, 0.20, 20.00): 1.34 + 2.68 + 4.00 = **USD 8.02**.
- Light on Sonnet 5.5: 1.2 × 0.10 + 0.3 × 2 + 0.03 × 10 = **USD 1.02**.

**One attempt at a story.**

| Line | Assumption | USD at list |
|---|---|---|
| Executor | Heavy session; 80% Sonnet, 20% Opus: 0.8 × 4.01 + 0.2 × 8.02 | 4.81 |
| Evaluator | Half a heavy Sonnet session (click-through plus reading evidence) | 2.00 |
| Review agent | One light Sonnet session | 1.02 |
| LLM judge for Copilot Studio conversations | Small calls, three-run majority | 0.20 |
| Chores (digest, ADO notes) on GPT-6 Luna | | 0.02 |
| **AI credits per attempt** | | **8.05** |
| Runner compute | Execution 60 min plus gate 45 min = 1.75 h at about USD 0.43 an hour for 4 vCPU and 8 GiB (unverified US list rates, from V2.1) | 0.75 |
| **Per attempt** | | **8.80** |

Hosted runner minutes would instead use the 50,000 included minutes on Enterprise ([included usage](https://docs.github.com/en/billing/reference/product-usage-included)), at a shadow value of 105 × 0.006 = USD 0.63.

**One accepted story, fully loaded (model).** Assume 1.3 attempts (about 30% need a NEEDS_WORK round), 70% yield, a loaded human rate of USD 100 an hour (replace it with GET AI's AUD rate), and 50 human minutes per story: 30 for spec and scenarios by day, 15 for morning review, 5 for PARK handling on average. Day-phase AI is three light Opus sessions on the spec owner's seat: 3 × 2.04 = USD 6.12.

| Line | Arithmetic | USD |
|---|---|---|
| Night AI and compute | 8.80 × 1.3 | 11.44 |
| Day AI | 3 × 2.04 | 6.12 |
| Human | 50 ÷ 60 × 100 | 83.33 |
| Subtotal per attempted story | | 100.89 |
| **Per accepted story** | 100.89 ÷ 0.7 | **144** |
| Plus fixed Power Platform costs | Monthly licences and capacity ÷ accepted stories that month | F ÷ n |

Human minutes are 83% of the subtotal.

| Scenario | Change | Per accepted story | Saving |
|---|---|---|---|
| P1: base | As above | USD 144 | |
| P2: token price halved | Night AI 4.02 per attempt; day AI 3.06 | (((4.02 + 0.75) × 1.3) + 3.06 + 83.33) ÷ 0.7 = USD 132 | 8% |
| P3: better evaluator, faster review | 35 human minutes; 85% yield | (11.44 + 6.12 + 58.33) ÷ 0.85 = USD 89 | 38% |

The lesson matches V2.1: evaluator quality and review minutes move margin far more than token price.

### 10.5 The cost envelope and what the credits buy

**Caps.** Per story: `--max-ai-credits 1500` (USD 15; soft, minimum 30, "an in-flight response completes" ([session limit](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit))), plus the driver's 5-loop cap and a wall-clock deadline. Per night: an envelope per project of USD 120 at list (model: 9 stories × 1.3 × 8.80 = USD 103, plus margin). Turn off "AI credits paid usage" or set budgets, because "There is no automatic fallback to lower-cost models" ([organisation billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing)). With an org-metered token, user budgets do not apply, so use cost centre budgets and the dispatcher's own envelope.

**Credit pools (model).** One designation gives USD 10,000 ÷ 12 = 833 of Azure credits plus 5,000 ÷ 12 = 417 of Copilot credits: **USD 1,250 a month**. Assume USD 50 a month of Azure base (Functions, storage, Key Vault, logs, a Burstable PostgreSQL server).

| Scenario | Arithmetic | AI and compute | Total with base | Against 1,250 |
|---|---|---|---|---|
| Power Platform: 1 lane, 3 stories a night, 20 nights | 60 stories × 1.3 = 78 attempts × 8.80 | 686 | 736 | 514 headroom |
| Power Platform: 3 lanes, 3 stories a night, 20 nights | 234 attempts × 8.80 | 2,059 | 2,109 | **859 cash spill** |
| Lane B code: 1 project, 20 light nights (V2.1) | 20 × 45.25 | 905 | 955 | 295 headroom |
| Lane A: 7 builds at USD 150 (V2.1) | 7 × 155 | 1,085 | 1,135 | 115 headroom |
| Mix: 1 Power Platform lane + 6 light Lane B nights | 686 + 6 × 45.25 | 958 | 1,008 | 242 headroom |

So one designation funds about **1.75 Power Platform lanes** at three stories a night (1,200 ÷ 686), or one lane plus a little code work. Three lanes need a specialisation (USD 1,600 a month more, with the GitHub parts earmarked) or cash. These totals exclude seats, the designation fee (USD 406 a month, always cash), and every Power Platform licence, capacity and meter line, which sit in whichever tenant owns the environments.

**Fixed Power Platform lines to price (not researched).** For each project: Power Apps Premium (or Power Automate Premium) for the test user and every human who opens apps in lanes, Test, UAT or Prod; extra database and log capacity beyond the tenant's pool for six environments; Process licences for production service-principal-owned premium flows; Copilot Studio credits for evaluation and for new-harness agents; Dataverse MCP usage. Put the partner price list into `dim_lane` and `fact_fixed_cost` before quoting any client.

**Pricing from the matrix** (unchanged): fixed-price floor = P80 fully loaded list cost ÷ (1 minus target gross margin). Match the commercial model to scope certainty. If margin at list is below target, the project is profitable only through subsidy; do not renew on those terms.

## 11. Staged build plan

The uploaded plan's timeline holds: a safety net on today's human-led work first (verifier before worker), ADO automation second, one night lane before three, and auto-merge only on evidence. V2.1's stages and exit tests fit inside it. Do not start a stage until the one before passes its exit test. Day counts are calendar days from the start. Effort is engineering time; the calendar assumes two engineers.

### 11.1 Stage 0: spikes and money (days 1 to 14, alongside stage 1)

Each spike is one to two days unless noted. A failed spike changes the design before we build on it.

| # | Spike | Exit test | If it fails |
|---|---|---|---|
| 0.1 | **Credit ruling.** Send the question (section 9.1). Set up the Mode A and Mode B billing profiles. Connect the credited subscription to a test cost centre ([connect Azure](https://docs.github.com/en/billing/how-tos/set-up-payment/connect-azure-sub)) | Written answer on file. The next invoice shows "Azure credits applied" against GitHub lines (1 to 3 weeks elapsed) | Client work stays at cash; price from list |
| 0.2 | **GHE.com OIDC with pac.** One job on `getai.ghe.com`: print the `sub` claim, create the credential (Other issuer, `https://token.actions.getai.ghe.com`), run `pac auth create -ghf` then `pac org who` against a sandbox. Repeat inside a ruleset workflow with the `job_workflow_ref` subject | `pac org who` returns the application user in both cases | Certificate in Key Vault, then managed identity, then rotated secrets (section 5.3) |
| 0.3 | **Dataverse MCP with an app-only token.** Local `@microsoft/dataverse mcp` with a federated profile; the remote endpoint with our app ID on the allowed clients list | A read and a create succeed headless | Night stays on pac and trusted Web API scripts |
| 0.4 | **`pac copilot` under federated login.** `clone`, `pull`, `push` and `pack` as `getai-fl1-exec` | All four work; `pack` output imports into Test | Agents are edited as files and deployed by `pack` plus import only |
| 0.5 | **Cloud agent against Dataverse.** OIDC plus `pac auth create -ghf` in `copilot-setup-steps.yml`; allowlist `dynamics.com`, `login.microsoftonline.com`, `api.bap.microsoft.com`, `api.powerapps.com`, `powerplatform.com`; one 45-minute story with an import | The story finishes inside 59 minutes with no firewall blocks | The cloud agent does offline edits only |
| 0.6 | **Copilot CLI on GHE.com.** Org billing policy, `copilot-requests: write`, OpenTelemetry export, custom agents from the gate repo, `--max-ai-credits` behaviour; pick the billing identity (section 5.2) | One executor run measured in Application Insights and billed to the intended identity | Machine account per project |
| 0.7 | **nano AIU against billing.** Sum `nano_aiu ÷ 1e9` for a day of runs | Matches the billing endpoint within 5% (assumed tolerance); subagent spans not double-counted | Treat CLI cost as estimated, reconcile |
| 0.8 | **Container Apps long run and resume** (for Lane A and self-hosted runners). Explicit `replicaTimeout`, Azure Files session state, a killed replica | Runs well past 1,800 seconds (target 7.5 hours); resumes by session ID | Shorter builds; Blob copies of session state |
| 0.9 | **Environment audit.** Find any Type = Developer, Managed = No environment in use | None left in use by 15 December 2026 | Urgent conversion or move to Sandbox |
| 0.10 | **Test environment behaviour.** Managed import with `--stage-and-upgrade` of successive PR versions; measure import time | Upgrades apply and remove dropped components; times recorded | Delete and re-import, or one Test environment per lane |
| 0.11 | **Test user sign-in.** Playwright certificate sign-in under the tenant's Conditional Access | Storage state acquired headless in CI | Work with the client's identity team on a CA exclusion |
| 0.12 | **Copilot Studio evaluation from code.** `pac copilot-studio run-maker-evaluation-test-set` and the REST API with an app token; a Direct Line script | We know which tokens work | Direct Line runner only |
| 0.13 | **ADO and GHE.com.** Orchestrator service principal on the ADO REST API; Azure Boards `AB#` links from GHE.com | State changes and links work | The Function writes links itself |
| 0.14 | **Skills headless.** `model-apps` `/app-builder` and `dv-solution` in `copilot -p` | We know where they stop for approval | PARK at the approval point |
| 0.15 | **Redaction and Universe.** Secrets absent from captured traces; Universe announcements checked against sections 5.2, 8 and 9 | Both done | Capture off until fixed |

### 11.2 Stages 1 to 8

| Stage | Days | Build | Exit test | Effort |
|---|---|---|---|---|
| **1. Safety net** (uploaded Phase 1) | 1 to 14 | `factory-gates` repo with `lcp-gate.yml` (Appendix A) as a required workflow, in Evaluate mode first. The four rulesets and CODEOWNERS. Trusted scripts with a hash manifest. Builder check, pack, manifest check, plan checks, lints, solution checker SARIF. `factory-test` bootstrapped with `getai-<proj>-test` and the test user. Locked scenario conventions and the Playwright kit v0. Spec Kit 1.2.x pinned, GET AI and `getai-lcp` presets v0, gate script as hook and CI check. Humans keep triggering the AI in VS Code; their PRs now pass the gate | A seeded edit to `tests/acceptance/` or `scripts/` is blocked by the push ruleset and, with the ruleset off, by the `locks` job. A component with missing files fails the manifest check. A spec with an open marker or no scenarios cannot become Factory Eligible. A human PR runs the full gate in Test and posts evidence | 3 to 4 weeks (tight in 14 days) |
| **2. ADO automation** (uploaded Phase 2) | 15 to 21 | Orchestrator Function and the state map (section 5.11). Custom fields (Appendix D). `run_id` on every run. Ledger v0: `fact_run`, provisional lines, evidence export to Blob. OpenTelemetry on day sessions through managed settings | Branch, PR and merge events move ADO states correctly for a week of human PRs. Every run has a `run_id` and a cost row. Evidence for each PR is in Blob | 1 week |
| **3. Night shift, one lane** (uploaded Phase 3, first half) | 22 to 30 | `factory-lane-1` bootstrapped (Sandbox, Managed, Australia). Execution workflow with the lane lock, preflight, reset, Copilot CLI executor, fast-check loop, driver push, lane drift check. PARK protocol. Evaluator and review agent with Merge Danger, no auto-merge. 05:41 digest; review 09:00 to 10:00. Trace reviewer. The weekly routine starts | Three nights produce PRs and a digest with nobody awake. A seeded portal-only step PARKs with exact instructions. A seeded environment-only change is caught as drift. The evaluator catches a seeded defect that passes the locked scenarios. Cost per story known from measured rows | 1.5 to 2 weeks |
| **4. Three lanes, calibrated** (uploaded Phase 3, second half) | 31 to 45 | Lanes 2 and 3. Test queue with `queue: max`. NEEDS_WORK re-queue and RESTART. Held-out set in `factory-holdout`. Day-3 reconciliation. Matrix v1 with the Power Platform page. Weekly seeded-violation tests | A night with nine stories across three lanes, no cross-lane interference, no reset mid-check. Ten verdicts graded blind, agreement recorded. Reconciliation variance under 10% per grain key (assumed tolerance). The matrix shows cost per accepted story at list and cash | 2 weeks |
| **5. Lane B for code repos** (V2.1 stages 2 and 3) | 46 to 70 | Cloud agent dispatch, tick and report; gate evaluator; code review at Lite; the `@copilot` loop; held-out suite; Merge Danger rules for code paths | As V2.1: three unattended nights, a seeded defect caught, ten verdicts graded | 3 to 4 weeks |
| **6. Lane A** (V2.1 stage 4) | 60 to 90 | The SDK driver in ACA with generator and evaluator sessions, Spec Kit inside, RESTART, resumable state | One greenfield build merges unattended; cost per role matches billing | 2 to 3 weeks |
| **7. Phase 4: auto-merge into `integration`, on evidence** | Earliest about day 75 per project; never on a date | Phase 4 settings on `integration-gate`, CODEOWNERS by floor, the merge-policy check, the `factory-merger` App | All entry criteria in section 5.10 met and signed off. A seeded score-3 PR is refused auto-merge; a seeded protected-path PR is refused at any score | 1 week, after the evidence |
| **8. Scale, engines, keep healthy** | Ongoing | Second project, second tenant. Claude Code bake-off on 20 stories. A T3 trial with BYOK to Azure OpenAI in Australia East. A long-session trial for a greenfield Power Platform solution. Client PM canvases. Regression set with pass^k. Monthly register reviews. Package the accelerator | Two projects in one night with clean per-project rows. Bake-off results in View 2. Human minutes per accepted story falling. At least one thin-glue item deleted or confirmed. The accelerator deploys into a clean tenant in two days | Ongoing |

Start stage 0 now. The invoice test cannot be rushed, because a month's charges reach the Azure invoice at the start of the next month ([Copilot Azure billing](https://docs.github.com/en/copilot/reference/copilot-billing/azure-billing)). Spike 0.9 has a hard date.

## 12. Risks, most serious first

| # | Risk | Why it matters | Mitigation |
|---|---|---|---|
| 1 | Credits may not fund client delivery | "Internal-use-rights credits" ([credits FAQ](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud#azure-credits-faqs-legacy-experience)) | Written ruling; two modes; price at list (section 9) |
| 2 | Auto-merge lets soft test gaming through | About 80% of agent test patches have weak oracles; about 20% of tests-passing patches are wrong; LLM judges are generous (section 3.4) | Deterministic floor; LLM raise-only; protected paths never; `integration` only; evidence-based entry (section 5.10) |
| 3 | Unmanaged developer environments retire | No new ones from 15 November 2026; suspended 15 December 2026; deleted 15 January 2027 ([important changes](https://learn.microsoft.com/power-platform/important-changes-coming#deprecation-of-unmanaged-developer-environments-and-the-power-apps-developer-plan)) | Lanes are Sandbox plus Managed; spike 0.9 audit now |
| 4 | Client code leaves Australia for inference | Copilot residency covers only the US and EU ([Copilot with data residency](https://raw.githubusercontent.com/github/docs/main/content/admin/data-residency/github-copilot-with-data-residency.md)) | Residency tier per client; BYOK to Azure OpenAI Standard in Australia East for T3; synthetic data only in lanes |
| 5 | The agent edits its own checks, or PR code reaches credentials | The uploaded plan ran PR scripts with `id-token: write` | Required workflow in the gate repo; trusted scripts with hashes; no credentials on PR-code jobs; `job_workflow_ref` subject pin |
| 6 | Evaluator generosity drift | "Done" rests on the evaluator, and Claude starts generous [talk 32:40 to 34:08] | Weekly blind grading; agreement alert; held-out set; evaluator changes by PR with a graded-set re-run |
| 7 | pac federation fails on GHE.com | No source confirms `--githubFederated` on GHE.com | Spike 0.2; certificate, then managed identity, then rotated secrets |
| 8 | Managed Environment licence enforcement | "All active usage requires" premium licences; stricter from February 2027 ([Managed Environment licensing](https://learn.microsoft.com/power-platform/admin/managed-environment-licensing); [licensing FAQ](https://learn.microsoft.com/power-platform/admin/powerapps-licensing-faq)) | Licence the test user and every human who opens apps; price it in `fact_fixed_cost` |
| 9 | Copilot Studio evaluation gaps on the new harness | Preview, General quality only, no API ([evaluate (preview)](https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/analytics-agent-evaluation-intro)) | Factory agents use the standard harness; human check for new-harness agents |
| 10 | Evaluation runs as a user and test sets are visible to makers | Built-in evaluation needs a user token; "Any maker with access to the agent" sees test sets | Separate Test environment and test user; Direct Line runner with locked scripts; held-out set outside Copilot Studio |
| 11 | Pack drops components silently | Exit code 0 with a component missing ([SolutionPackager troubleshooting](https://learn.microsoft.com/power-platform/alm/solution-packager-tool#troubleshooting)) | Manifest check after every pack |
| 12 | Dataverse throttling and the tenant daily pool | 52 concurrent per user; one 25,000-request pool for all application users on Power Apps tenants ([request limits](https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations)) | Per-lane application users; backoff helper; serial imports; pool monitoring in preflight |
| 13 | Test Engine dependency | Deprecated April 2026, repo unmaintained ([deprecations](https://learn.microsoft.com/power-platform/important-changes-coming#deprecation-of-test-engine)) | Playwright toolkit only; no `pac test run` |
| 14 | Preview components change or break | `pa` CLI and `code-apps-preview`, `pac code`, `pac copilot` CLI mode, `pac copilot-studio`, the Dataverse CLI, MCP servers, Git integration, low-code plug-ins, dynamic workflows | Pin versions; vendored plugins; register review monthly; no dependence on preview parts for locked tests |
| 15 | Interactive steps cannot run at night | OAuth consent, first code-app share, agent accounts, canvas authoring | Bootstrap runbook; PARK protocol; route canvas authoring to day work |
| 16 | Agent changes the environment outside the source | MCP or Web API writes that skip builders | Lane drift check blocks the PR |
| 17 | Lane state decays | Expired connections, removed permissions, lost exclusions | Nightly preflight marks the lane Offline and raises a bug |
| 18 | The Test environment becomes the bottleneck | About 30 minutes per PR, serial (section 5.5) | Watch queue length; add a second Test environment |
| 19 | Capacity runs out | Create, copy and restore each need 1 GB free ([backup FAQ](https://learn.microsoft.com/power-platform/admin/backup-restore-environments#faq)) | Capacity check in preflight; short audit retention in lanes |
| 20 | Service-principal-owned premium flows suspended | "Flows owned by service principals are not compliant" without a licence ([SP-owned flows](https://learn.microsoft.com/power-automate/service-principal-support)) | Designated licensed user in lanes and Test; Process licence in Prod |
| 21 | Federated credential subject mismatch | A wrong subject is accepted and "the exchange fails without error" ([FIC considerations](https://learn.microsoft.com/entra/workload-id/workload-identity-federation-considerations)); new repos use immutable subjects | Read the real `sub` first; preflight checks every credential |
| 22 | Captured traces contain client metadata or secrets | Content capture stores prompts and tool data | Short retention; RBAC; resource per client; redaction tested |
| 23 | Bypass list drift | One bypass entry undoes the gate | Nightly audit fails the kickoff |
| 24 | Skills change under us, or phone home | The installer auto-updates; telemetry is on by default ([power-platform-skills](https://github.com/microsoft/power-platform-skills)) | Vendor and pin; telemetry opt-out in CI; review each version |
| 25 | Entra eventual consistency | Reported 5 to 15 minutes [unverified] | Deterministic polling with a deadline; a timeout PARKs the story and flags the lane |
| 26 | The rename | Microsoft is expected to rename Power Platform; Ignite is 17 to 20 November 2026 | Product-neutral identifiers (section 1.1); prose-only change; re-check after Ignite |
| 27 | Over-specified stories cascade errors | Wayfinder writes granular stories [talk 24:12 to 24:46] | What and why only; design-leak warning in the gate script |
| 28 | Credit mechanics or spend controls fail | Unsupported subscription types; paid usage on by default; org tokens ignore user budgets | Stage 0 invoice test; night envelope; per-story caps; cost centre budgets |
| 29 | Operations: incidents, schedule drift, evidence loss, price and FX drift | Late schedules and runner incidents; retention deletes runs; costs in USD, prices in AUD | Idempotent tick and a lost hour budgeted; nightly export to Blob; nightly `dim_price` with an FX column |

## 13. The accelerator and IP

Build these in Mode A, keep client code, data and traces out of them, and record which mode funded each run.

- **The `getai-lcp` preset and bundle.** The Power Platform spec section, checklist and gate-script rules, packaged with the GET AI preset and pinned extensions. It turns a client's Power Platform delivery standard into an installable day process.
- **The environment pool kit.** Bootstrap runbook, lane manifest schema, preflight, reset, lane locks, drift check, backup labels, and the Bicep and pac scripts that stand up three lanes and a Test environment in a client tenant. It answers the consent problem honestly, which is what clients ask about first.
- **The gate repo.** `lcp-gate.yml`, trusted scripts with their hash manifest, ruleset JSON, the identity model and federated-credential templates for GHE.com.
- **The Merge Danger rubric and floor.** Path rules, plan rules and the merge policy (Appendix B). It makes a morning review fast and auditable.
- **The Playwright kit for Power Platform.** Page objects on top of Microsoft's toolkit, the accessible-name selector convention, the axe baseline and the keyboard journey.
- **Copilot Studio evaluation sets and rubric.** The Direct Line runner, locked conversation scripts, rubric and judge prompt. Graded sets improve every week and are hard to copy.
- **The ledger with Power Platform lines.** Cost per accepted story at list and cash, which turns the factory into a pricing tool.

Board lens: these are reusable IP, Power Platform depth strengthens the Microsoft position, and the auditable track record (cost per accepted story at P50 and P80, first-pass rate, escaped defects, evaluator agreement) is what an acquirer values. Auto-merge is the one step that can damage that record, so it waits for evidence.

## 14. Decision log

### 14.1 Against the uploaded plan

| Topic | Uploaded plan said | This plan says | Why |
|---|---|---|---|
| Architecture | Part A: Foundry plus Agent Framework "Chief of Staff", "Azure AutoGen" workers. Part B: Actions dispatcher, headless agent | Part B only. Copilot Studio and Wayfinder as an optional front door | Two architectures conflicted; "Azure AutoGen" is not a product; building an orchestrator is the IKEA trap |
| Ticket state | Agent marks tickets Resolved (Part A); orchestrator owns state (Part B) | Orchestrator owns state; agents write files only | Race-free and auditable |
| Branching | Integration branch per Epic (A); PR per story to `main` (B) | PR per story into `integration`; human release PR to `main` | Auto-merge may never reach anything that deploys |
| Auto-merge | LLM score 0 to 2, including tests, into `main`, from day 45 | Deterministic floor, LLM raise-only, protected paths never, `integration` only, on evidence | Soft test gaming; bypass trap; dates are not evidence |
| Gate | PR checks run the PR's own scripts with `id-token: write` | Required workflow in `factory-gates`; trusted scripts; no credentials on PR code | The agent could edit the checks that judge it |
| Builder protection | (Review fix 2) push-protect `workflows/build/` | Protect the shared builder library and check scripts; per-component builders stay writable with a floor of 3 | The agent must edit builders to change any flow; the builder check only proves determinism |
| Acceptance | Humans refine criteria; the agent writes code and tests (red/green) | Locked scenarios by someone else; held-out set; separate Test environment and identity | Shared blind spots; visible-test overfitting |
| Identity | One "Pipeline App Reg" for execution, verification and review | Four roles; per-lane execution and verification application users | Separation of duties; per-lane throttling budgets |
| Engine | Headless Claude Code with an LLM API key | Copilot CLI with Claude through Copilot by default; Claude Code at cash as secondary | Credit-funded; measured by OpenTelemetry; same skills |
| Money | Iteration cap of 5; no ledger | Cap of 5 plus per-story credit cap, night envelope, `run_id`, cost fields in ADO, the ledger | Cost to build feeds pricing |
| Dev lanes | Three long-lived Dev environments | Three Sandbox plus Managed Environments in Australia | Unmanaged developer environments retire |
| Evaluator | Review agent reads the diff | Fresh evaluator clicks through the app in Test; review agent scores separately | The best catches came from using the app [talk 31:19 to 31:49] |
| Copilot Studio testing | Human spends 5 minutes in the test pane | Automated for standard-harness agents; human for new-harness and manual-auth agents | Built-in evaluation and Direct Line exist now |
| Test environment | Single `FACTORY_ENV_URL` for all lanes | Lane mapping by branch; lane locks; a separate Test environment with its own lock | A reset could land mid-check |
| Runners | Self-hosted "eliminates" timeouts | Self-hosted for images and networking; resumable runs | Self-hosted jobs stop at 5 days; queued jobs drop at 24 hours |
| Retro Loop | Weekly skill over logs | Merged with calibration; transcripts to Blob | Runner disks vanish; retention deletes runs |
| Spec level and one-way doors | Granular Wayfinder stories; doors judged by the review agent | What and why only; doors detected from `--plan` and path rules | Technical plans cascade errors; an LLM must not be the only detector |
| Data residency | Not addressed | Tier per client; BYOK path for in-country inference | No engine keeps inference in Australia by default |
| Small edits | "Section 9.1" reference; pasted chat; restarted numbering | Fixed | Readability |

### 14.2 Against V2.1

| Topic | V2.1 | V3 | Why |
|---|---|---|---|
| First build | Lane B code profile | Lane B Power Platform profile | GET AI's Microsoft focus and the uploaded plan |
| Work queue | GitHub issues and a night plan JSON | ADO Boards as system of record; night plan generated from it | The reader's process |
| Identities | Machine account, factory App, humans | Four roles with per-lane Entra apps for Power Platform; V2.1's model stays for code lanes | Dataverse needs application users |
| Engine for Power Platform | n/a | Copilot CLI on an Actions runner | Cap, OIDC, measurement |
| Merge Danger | Not present | Every lane, with a deterministic floor | Better morning package |
| Auto-merge | Merge queue into `integration` with zero approvals | Human approval into `integration` until Phase 4 | Evidence first |
| Verification | Playwright evaluator | Plus the Power Platform toolkit, flow scenarios, Copilot Studio evaluation, Test environment | New research |
| Handoff files | V2.1 set | Plus `state.md`, `park.json`, `lessons-learned.md` | The uploaded plan |
| Calibration | Weekly calibration | Merged with the Retro Loop and seeded violations | One routine |
| Residency | "Not established" | Facts and a tier table; BYOK option | New research |
| Stages | Eight stages | Stage 0 spikes plus eight stages on the 45-day timeline | The uploaded plan's sequence |

## 15. Open questions and evidence quality

### 15.1 Open questions, by owner

| Question | Owner | Resolved by |
|---|---|---|
| Can partner credits fund client delivery? | Boroon | Spike 0.1 |
| Does `pac --githubFederated` work on GHE.com, including in ruleset workflows with a `job_workflow_ref` subject? | Platform team | Spike 0.2 |
| Which Copilot features work on GHE.com (CLI org billing, OpenTelemetry, cloud agent, code review, Agent HQ)? | Platform team | Spike 0.6 |
| Org-metered `GITHUB_TOKEN` or a machine account for CLI billing? | Boroon and platform team | Spike 0.6 |
| Does the Dataverse MCP server accept an app-only token? | Platform team | Spike 0.3 |
| Do `pac copilot` sync commands and evaluation APIs accept service principals? | Platform team | Spikes 0.4 and 0.12 |
| Which Azure OpenAI models are available as Standard deployments in Australia East, and does BYOK send telemetry to GitHub? | Platform team | Stage 8 T3 trial |
| Lanes in the client's tenant or ours, per client? | Boroon with each client | Before each engagement |
| Power Platform licence, capacity and meter prices in AUD | Commercial | Partner price list |
| Does Purview cover sandbox environments? | Platform team | Stage 1 |
| What did Universe (28 to 29 October 2026) and Ignite (17 to 20 November 2026) change? Is there a rename? | Boroon | Register review in each following week |
| Can an Entra service principal drive the ADO REST API, and do Boards links work with GHE.com? | Platform team | Spike 0.13 |

### 15.2 Evidence quality

| Area | Quality | Note |
|---|---|---|
| Power Platform ALM, environments, limits, licensing, testing, tooling | Strong | Microsoft Learn read in full on 1 November 2026; a few conflicts flagged (two checker rule set GUIDs, 250 MB or 50 MB capacity accrual, action inputs versus the OIDC tutorial) |
| GHE.com specifics | Weak | OIDC issuer format documented; nothing on pac, Copilot feature parity or Boards integration |
| Copilot CLI, SDK, cloud agent, billing | Strong | GitHub Docs source read on 23 October and 1 November 2026; pre-Universe |
| Partner benefits | Medium | Guide and FAQs read; the binding Terms of Participation Guide not read |
| Anthropic harness and workshop | Strong | Primary posts plus the user-supplied transcript |
| Reward-hacking and test-quality rates | Medium | Direction consistent across six papers; figures from snippets and abstracts |
| Run times, story costs, throughput | Model only | Calibrate in stages 3 and 4 |
| Entra propagation delay | Unverified | From the uploaded plan |
| FakeXrmEasy licensing | Unverified | Vendor site blocked |
| Rename | Negative finding | No rename found up to 1 November 2026; blog listing only |

## Appendix A: The gate workflow for the Power Platform profile (untested starting point)

**Status: untested.** The YAML parses, but nobody has run it. Every action version, CLI flag, claim format, path and script name must be checked in stage 0 and stage 1. It assumes this layout in the project repo: per-component builders in `workflows/build/*.py`, the YAML-format solution in `src/`, Copilot Studio workspaces in `agents/<name>/`, locked scenarios in `tests/scenarios/` and `tests/acceptance/{api,ui,agents}/`. Adjust to the real repo.

What it does, job by job:

| Job | Credentials | Runs |
|---|---|---|
| `map` | None | Lane and story from the branch name, validated against `vars.LCP_LANES` |
| `locks` | None | Second lock on protected paths, against the base commit |
| `build` | None | PR builders, `git diff --exit-code`, offline `pac solution pack` and `pac copilot pack` |
| `static` | Read-only gate App token | Trusted manifest check, lints, criteria trace; hashes verified first |
| `verify-in-test` | OIDC for `getai-<proj>-test` only; held-out reader App; Key Vault | Plan against the Test baseline, checker SARIF, import, locked scenarios, Playwright, Copilot Studio conversations, held-out set, evaluator, evidence hashes to Blob |
| `danger` | Job token with `checks: write` | Deterministic floor, raise-only review agent, combined score, merge policy |

Three things to know before using it:

- **The gate reader keys are secrets.** Three jobs hold a GitHub App key that can read `factory-gates`, and one also holds a key for `factory-holdout`. None of them runs PR code. The push ruleset on `.github/**` stops an agent adding a workflow that could read them. Rotate both keys quarterly.
- **The lane lock is not here.** Concurrency groups are per repository, so the lane lock and the lane drift check live in the execution workflow in `factory-control`. That workflow posts `lane/drift` as a check run through the factory App, and `integration-gate` requires it.
- **The Test lock is here.** `verify-in-test` holds `lcp-test-<repo>` for import, tests and the evaluator together, so another PR cannot import between this PR's tests and its evaluation.

```yaml
# lcp-gate.yml
# Required workflow for the Lane B low-code platform profile (Power Platform today).
# Lives in getai/factory-gates on the protected "release" branch. Applied by the
# organisation ruleset "factory-required-workflows" (Require workflows to pass
# before merging) to every repo with custom property factory=enabled.
#
# STATUS: UNTESTED STARTING POINT. Check every action version, CLI flag, claim
# format and path in stage 0 and stage 1 before relying on it.
#
# Rules this file follows:
# - Jobs that run PR code hold no credentials.
# - Jobs that hold credentials run only trusted scripts from this repo, checked
#   against scripts.sha256, and treat PR files as data.
# - Only the verify-in-test job can request an OIDC token, and the Entra
#   federated credential for getai-<proj>-test trusts only this workflow on
#   refs/heads/release (job_workflow_ref in the subject).
# - Ruleset workflows ignore branches, paths and types filters.

name: lcp-gate

on:
  pull_request:
  merge_group:

permissions: {}

env:
  GH_HOST: getai.ghe.com
  PAC_VERSION: "2.4.1"          # pin pac; matches Microsoft's OIDC sample
  PY_VERSION: "3.11"
  GATE_REPO: getai/factory-gates

jobs:
  map:
    name: map lane
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      lane: ${{ steps.lane.outputs.lane }}
      story: ${{ steps.lane.outputs.story }}
    steps:
      - id: lane
        env:
          HEAD_REF: ${{ github.head_ref || github.event.merge_group.head_ref }}
          ALLOWED: ${{ vars.LCP_LANES }}        # for example "fl1 fl2 fl3"
        run: |
          set -euo pipefail
          # Agent branches: agent/<lane>/<ado-id>-<attempt>, for example agent/fl2/48213-1
          if [[ "$HEAD_REF" =~ ^agent/(fl[0-9]+)/([0-9]+)-([0-9]+)$ ]]; then
            lane="${BASH_REMATCH[1]}"
            story="${BASH_REMATCH[2]}"
            if [[ " $ALLOWED " != *" $lane "* ]]; then
              echo "Unknown lane: $lane"
              exit 1
            fi
          else
            lane="none"        # human PR, release PR or merge queue
            story="none"
          fi
          echo "lane=$lane" >> "$GITHUB_OUTPUT"
          echo "story=$story" >> "$GITHUB_OUTPUT"

  locks:
    name: protected paths and locked scenarios
    runs-on: ubuntu-latest
    needs: map
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0
          persist-credentials: false
      - name: Protected paths and locked scenarios unchanged (second lock behind the push ruleset)
        if: needs.map.outputs.lane != 'none'
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
        run: |
          set -euo pipefail
          changed="$(git diff --name-only "$BASE_SHA"...HEAD)"
          protected='^(tests/acceptance/|tests/scenarios/|specs/[^/]+/spec\.md|specs/[^/]+/checklists/|\.specify/|\.github/|\.claude/|\.mcp/|AGENTS\.md|CLAUDE\.md|scripts/|builders/lib/|deploy/)'
          if printf '%s\n' "$changed" | grep -E "$protected"; then
            echo "An agent PR changed a protected path. Failing."
            exit 1
          fi

  build:
    name: builders, drift and pack (PR code, no credentials)
    runs-on: ubuntu-latest
    needs: map
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v5
        with:
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PY_VERSION }}
      - uses: actions/setup-dotnet@v5
        with:
          dotnet-version: 8.0.x
      - name: Install pinned pac
        run: dotnet tool install --global Microsoft.PowerApps.CLI.Tool --version "$PAC_VERSION"
      - name: Run every builder, then fail on any diff
        run: |
          set -euo pipefail
          for builder in workflows/build/*.py; do
            python3 "$builder"
          done
          git diff --exit-code || { echo "Generated files do not match builders"; exit 1; }
      - name: Pack the solution offline (YAML source format)
        run: |
          set -euo pipefail
          mkdir -p out
          pac solution pack --zipfile out/solution_unmanaged.zip --folder src --packagetype Unmanaged
          pac solution pack --zipfile out/solution_managed.zip --folder src --packagetype Managed
      - name: Pack Copilot Studio workspaces offline
        run: |
          set -euo pipefail
          # pac copilot pack is local and needs no sign-in. Confirm its flags in stage 1.
          for ws in agents/*/; do
            [ -d "$ws" ] || continue
            (cd "$ws" && pac copilot pack)
          done
      - uses: actions/upload-artifact@v4
        with:
          name: packed
          path: out/
          retention-days: 30

  static:
    name: trusted manifest check and lints (no Dataverse credentials)
    runs-on: ubuntu-latest
    needs: [map, locks, build]
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v5
        with:
          path: pr
          persist-credentials: false
      - id: gate-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.GATE_READER_APP_ID }}
          private-key: ${{ secrets.GATE_READER_KEY }}
          owner: getai
          repositories: factory-gates
      - uses: actions/checkout@v5
        with:
          repository: ${{ env.GATE_REPO }}
          ref: release
          token: ${{ steps.gate-token.outputs.token }}
          path: gate
          persist-credentials: false
      - name: Verify trusted script hashes
        working-directory: gate
        run: sha256sum --check --strict scripts.sha256
      - uses: actions/download-artifact@v4
        with:
          name: packed
          path: out
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PY_VERSION }}
      - name: Manifest check (pack exits 0 even when it drops a component)
        run: python3 -I gate/lcp/check_manifest.py --source pr/src --zip out/solution_unmanaged.zip
      - name: Lints and limits
        run: |
          set -euo pipefail
          python3 -I gate/lcp/lint_logic_apps.py --root pr          # if() over 8,192 chars, unsafe substrings
          python3 -I gate/lcp/check_root_components.py --root pr    # components in the wrong root solution
          python3 -I gate/lcp/lint_static_results.py --root pr      # no flow static results (mocks) may ship
          python3 -I gate/lcp/lint_canvas_yaml.py --root pr         # .pa.yaml against the published schema
          python3 -I gate/lcp/lint_accessible_labels.py --root pr   # every interactive control has a label
          python3 -I gate/lcp/trace_criteria.py --root pr           # every criterion maps to a locked scenario

  verify-in-test:
    name: import into Test, locked and held-out scenarios, evaluator
    runs-on: ubuntu-latest            # or a self-hosted runner with browsers pre-baked
    needs: [map, locks, build, static]
    environment: lcp-test             # federated credential pinned to this workflow on refs/heads/release
    timeout-minutes: 120
    concurrency:
      group: lcp-test-${{ github.repository }}
      cancel-in-progress: false
      queue: max                      # up to 100 pending; confirm syntax in stage 1
    permissions:
      contents: read
      id-token: write                 # verification identity only
      security-events: write          # upload solution checker SARIF
      copilot-requests: write         # evaluator session; billing identity decided in stage 0
    env:
      TENANT_ID: ${{ vars.TENANT_ID }}
      TEST_APP_ID: ${{ vars.LCP_TEST_APP_ID }}
      TEST_ENV_URL: ${{ vars.LCP_TEST_ENV_URL }}      # https://<org>.crm6.dynamics.com
      PROJECT_ID: ${{ vars.PROJECT_ID }}
      STORY_ID: ${{ needs.map.outputs.story }}
      COPILOT_AUTO_UPDATE: "false"
      COPILOT_OTEL_ENABLED: "true"
    steps:
      - name: Mint run_id and telemetry attributes
        run: |
          set -euo pipefail
          run_id="${PROJECT_ID}-$(date -u +%Y%m%d)-${STORY_ID}-lcp_evaluator-${GITHUB_RUN_ATTEMPT}"
          echo "RUN_ID=$run_id" >> "$GITHUB_ENV"
          echo "OTEL_RESOURCE_ATTRIBUTES=project=${PROJECT_ID},run_id=${run_id},story_id=${STORY_ID},lane=B,profile=lcp,role=lcp_evaluator" >> "$GITHUB_ENV"
      - uses: actions/checkout@v5
        with:
          path: pr
          persist-credentials: false
      - id: gate-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.GATE_READER_APP_ID }}
          private-key: ${{ secrets.GATE_READER_KEY }}
          owner: getai
          repositories: factory-gates
      - uses: actions/checkout@v5
        with:
          repository: ${{ env.GATE_REPO }}
          ref: release
          token: ${{ steps.gate-token.outputs.token }}
          path: gate
          persist-credentials: false
      - name: Verify trusted script hashes
        working-directory: gate
        run: sha256sum --check --strict scripts.sha256
      - uses: actions/download-artifact@v4
        with:
          name: packed
          path: out
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PY_VERSION }}
      - uses: actions/setup-dotnet@v5
        with:
          dotnet-version: 8.0.x
      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
      - name: Install pinned tools
        run: |
          set -euo pipefail
          dotnet tool install --global Microsoft.PowerApps.CLI.Tool --version "$PAC_VERSION"
          npm install --global @github/copilot
      - name: Sign in as the verification identity (OIDC, no secret)
        run: pac auth create --name verify --githubFederated --tenant "$TENANT_ID" --applicationId "$TEST_APP_ID" --environment "$TEST_ENV_URL"
      - uses: azure/login@v2              # for Key Vault (test user certificate, Direct Line secret) and Blob
        with:
          client-id: ${{ vars.LCP_TEST_APP_ID }}
          tenant-id: ${{ vars.TENANT_ID }}
          allow-no-subscriptions: true
      - name: Schema and security plan against the Test baseline (read only, feeds Merge Danger)
        run: |
          set -euo pipefail
          mkdir -p evidence
          python3 -I gate/lcp/create_schema.py --plan --source pr/src --env "$TEST_ENV_URL" --out evidence/schema-plan.json
          python3 -I gate/lcp/create_security.py --plan --source pr/src --env "$TEST_ENV_URL" --out evidence/security-plan.json
      - name: Solution checker, no exclusions or overrides (matches Managed Environment enforcement)
        run: |
          set -euo pipefail
          pac solution check --path out/solution_managed.zip --geo Australia --outputDirectory evidence/checker
          python3 -I gate/lcp/checker_gate.py --dir evidence/checker --fail-on High --sarif-out evidence/checker.sarif
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: evidence/checker.sarif
          category: solution-checker
      - name: Import the managed solution into Test
        run: |
          set -euo pipefail
          pac solution import --path out/solution_managed.zip \
            --settings-file "gate/projects/$PROJECT_ID/test.settings.json" \
            --stage-and-upgrade --async --max-async-wait-time 30
      - name: Locked scenarios (Web API, flows, server logic)
        run: |
          python3 -I gate/lcp/run_workflow.py --suite locked \
            --scenarios pr/tests/scenarios --api-tests pr/tests/acceptance/api \
            --env "$TEST_ENV_URL" --run-tag "$RUN_ID" --out evidence/scenarios.json
      - name: Locked Playwright suite (certificate test user)
        working-directory: gate/playwright
        env:
          MS_AUTH_CREDENTIAL_TYPE: certificate
          MS_AUTH_CREDENTIAL_PROVIDER: azure-keyvault
          KEYVAULT_NAME: ${{ vars.LCP_KEYVAULT }}
          TEST_SPECS_DIR: ${{ github.workspace }}/pr/tests/acceptance/ui
        run: |
          set -euo pipefail
          npm ci
          npx playwright test --config playwright.lcp.config.ts --reporter=html,junit
      - name: Locked Copilot Studio conversations (Direct Line runner)
        run: |
          node gate/lcp/cs-runner/run.mjs --scripts pr/tests/acceptance/agents \
            --rubric gate/rubrics/copilot-agent.md --runs 3 --out evidence/conversations.json
      - id: holdout-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.HOLDOUT_READER_APP_ID }}
          private-key: ${{ secrets.HOLDOUT_READER_KEY }}
          owner: getai
          repositories: factory-holdout
      - uses: actions/checkout@v5
        with:
          repository: getai/factory-holdout
          token: ${{ steps.holdout-token.outputs.token }}
          path: holdout
          persist-credentials: false
      - name: Held-out set (only aggregate scores and failing case IDs leave this step)
        run: |
          set -euo pipefail
          python3 -I gate/lcp/run_holdout.py --root "holdout/$PROJECT_ID" --env "$TEST_ENV_URL" \
            --run-tag "$RUN_ID" --out evidence/holdout-summary.json
          rm -rf holdout
      - name: Evaluator session (fresh, read only, uses the app)
        # Playwright MCP loads the test user's storage state written by the Playwright step.
        # Confirm the --agent flag and the MCP tool pattern for --allow-tool in stage 1.
        working-directory: gate
        env:
          GITHUB_TOKEN: ${{ github.token }}
          STORAGE_STATE: ${{ github.workspace }}/gate/playwright/.auth/mda.json
          TEST_ENV_URL: ${{ vars.LCP_TEST_ENV_URL }}
        run: |
          set -euo pipefail
          copilot -p "$(cat prompts/lcp-evaluate.md)" \
            --agent lcp-evaluator \
            --autopilot --max-autopilot-continues 40 --max-ai-credits 400 \
            --no-ask-user \
            --allow-tool 'playwright/*' --allow-tool 'shell(cat *)' --allow-tool 'shell(ls *)' \
            --deny-tool 'shell(git push*)' --deny-tool 'shell(pac *)' \
            --output-format json --share ../evidence/evaluator-transcript.md \
            > ../evidence/evaluator.jsonl
          python3 -I lcp/parse_verdict.py --in ../evidence/evaluator.jsonl --out ../evidence/verdict.json
      - name: Hash the evidence and write the job summary
        if: always()
        run: |
          set -euo pipefail
          find evidence -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > evidence/SHA256SUMS
          { echo "### Evidence hashes"; echo '```'; cat evidence/SHA256SUMS; echo '```'; } >> "$GITHUB_STEP_SUMMARY"
      - name: Copy evidence to Blob, keyed by run_id
        if: always()
        run: |
          az storage blob upload-batch --auth-mode login \
            --account-name "${{ vars.EVIDENCE_ACCOUNT }}" --destination "$PROJECT_ID" \
            --destination-path "gate/$RUN_ID" --source evidence
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: evidence
          path: evidence/
          retention-days: 400
      - name: Fail on a failing verdict or any failed locked or held-out case
        run: python3 -I gate/lcp/verdict_gate.py --dir evidence

  danger:
    name: merge danger (deterministic floor, review agent may only raise)
    runs-on: ubuntu-latest
    needs: [map, verify-in-test]
    permissions:
      contents: read
      pull-requests: read
      checks: write
      copilot-requests: write
    env:
      COPILOT_AUTO_UPDATE: "false"
      COPILOT_OTEL_ENABLED: "true"
      OTEL_RESOURCE_ATTRIBUTES: project=${{ vars.PROJECT_ID }},story_id=${{ needs.map.outputs.story }},lane=B,profile=lcp,role=lcp_reviewer
    steps:
      - uses: actions/checkout@v5
        with:
          path: pr
          fetch-depth: 0
          persist-credentials: false
      - id: gate-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ vars.GATE_READER_APP_ID }}
          private-key: ${{ secrets.GATE_READER_KEY }}
          owner: getai
          repositories: factory-gates
      - uses: actions/checkout@v5
        with:
          repository: ${{ env.GATE_REPO }}
          ref: release
          token: ${{ steps.gate-token.outputs.token }}
          path: gate
          persist-credentials: false
      - name: Verify trusted script hashes
        working-directory: gate
        run: sha256sum --check --strict scripts.sha256
      - uses: actions/download-artifact@v4
        with:
          name: evidence
          path: evidence
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
      - name: Deterministic floor from paths, plans and gate results
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
        run: |
          python3 -I gate/lcp/merge_danger_floor.py --repo pr --base "$BASE_SHA" \
            --rules gate/lcp/danger-rules.yml \
            --schema-plan evidence/schema-plan.json --security-plan evidence/security-plan.json \
            --gate-dir evidence --out evidence/danger-floor.json
      - name: Review agent (read only; may raise, never lower)
        working-directory: gate
        env:
          GITHUB_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          npm install --global @github/copilot
          copilot -p "$(cat prompts/lcp-review.md)" \
            --agent lcp-reviewer \
            --max-ai-credits 200 --no-ask-user \
            --allow-tool 'shell(git diff*)' --allow-tool 'shell(git log*)' --allow-tool 'shell(cat *)' \
            --deny-tool 'shell(git push*)' \
            --output-format json > ../evidence/review.jsonl
      - name: Combine (final score = max of floor and review) and post the check run
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          python3 -I gate/lcp/merge_danger_combine.py --floor evidence/danger-floor.json \
            --review evidence/review.jsonl --out evidence/danger.json --post-check
      - name: Merge policy (human approval needed above 2, always into main, always for protected paths)
        env:
          GH_TOKEN: ${{ github.token }}
          BASE_REF: ${{ github.base_ref }}
          AUTOMERGE_ENABLED: ${{ vars.LCP_AUTOMERGE_ENABLED }}   # "false" until Phase 4 entry is signed off
        run: |
          # Passes if: base is integration, final score <= 2, no protected path, all checks green,
          # and AUTOMERGE_ENABLED is true; or an approving review from @factory-reviewers exists
          # on the head commit (a reviewer re-runs this job after approving).
          python3 -I gate/lcp/merge_policy.py --danger evidence/danger.json \
            --base "$BASE_REF" --automerge "$AUTOMERGE_ENABLED"
```

## Appendix B: The Merge Danger rubric

The floor comes from `gate/lcp/danger-rules.yml`, run by a trusted script. Final score = max(floor, review agent score). The review agent may raise, with reasons, and may never lower. Each project adds its own sensitive paths (for example allowance or pricing logic) to the rules file through a reviewed PR.

### B.1 Path rules

| Changed path | Floor | Auto-merge eligible in Phase 4? |
|---|---|---|
| `docs/**`, `handoff/**`, `docs/lessons-learned.md` | 0 | Yes |
| Localisation files (for example output of `pac copilot extract-translation`) for wording already approved | 1 | Yes |
| Builder inputs for views, form layout, sitemap entries or new optional columns, where the schema plan is additive only and a locked scenario covers the change | 2 | Yes |
| Generated solution files under `src/**` that match a builder change in the same PR | Inherits the builder input's floor | As the input |
| Per-component builders `workflows/build/*.py` | 3 | No |
| Flow definition inputs that change logic | 3 | No |
| Copilot Studio workspace changes: topics, instructions, tools, knowledge (`agents/**`) | 3 | No |
| Code app source (`apps/**`) | 3 | No |
| Interface changes that need `sync_agent_tools.py` | 4 | No |
| Reference data (`data/reference/**`) | 4 | No |
| New connection reference or environment variable definition | 5 | No |
| Plug-in code (`plugins/**`); dependency or tool version bumps | 5 | No |
| Security roles, field security profiles, business unit or team configuration | 7 | No |
| Money, allowance or pricing logic (paths listed per project) | 8 | No |
| Pipeline and deployment settings (`deploy/**`) | 9 | No, and protected |
| Credentials, secrets, connection secrets | 10 | No, and protected |
| `tests/**` (locked), `scripts/**`, `.github/**` (workflows, hooks, agents, skills, instructions), `AGENTS.md`, `CLAUDE.md`, `.specify/**`, `.claude/**`, `.mcp/**`, `builders/lib/**` | 10 | No, and protected |

### B.2 Plan rules (from `--plan` against the Test baseline)

| Plan finding | Floor | Door |
|---|---|---|
| Additive table, column, view or form | 2 | Two-way |
| Column type change, shorter maximum length, stricter required level | 6 | One-way for existing data |
| Choice value removed | 6 | One-way for existing data |
| Privilege added to a role | 7 | Two-way, but security-relevant |
| Privilege depth widened (for example user to organisation) | 8 | Security-relevant |
| Role removed | 8 | One-way for access |
| Column dropped | 8 | One-way |
| Table dropped | 9 | One-way |

### B.3 Gate result rules

| Result | Effect |
|---|---|
| Any locked or held-out failure, drift, checker High or Critical, accessibility Medium or above | The gate fails; not mergeable at any score |
| Checker Medium findings present | Floor at least 3 |
| PR spans more than one solution | Floor plus 1 |
| More than 25 changed source files (assumption) | Floor plus 1 |
| Evaluator NEEDS_WORK or RESTART | Not mergeable |
| Evaluator finding without evidence | "No verdict": a human looks |

### B.4 What the review agent may raise for

Missing scenario coverage for new logic. Generated output that does not correspond to its builder. A blast radius wider than the paths suggest (a shared flow, a table used by other apps). A breach of an architectural decision record. Code smells that will cost maintenance. Unrequested features. Security-relevant logic in an innocent-looking file. Any doubt it cannot resolve from the evidence. Output:

```json
{
  "raise_to": 4,
  "reasons": ["Flow 'Approve trip' is also triggered by the Expenses app (shared trigger table)"],
  "one_way_door": false,
  "blast_radius": {
    "tables": ["getai_trip"],
    "flows": ["Approve trip"],
    "apps": ["Trips (model-driven)", "Expenses (canvas)"],
    "agents": [],
    "roles": [],
    "integrations": ["Outlook (test mailbox in Test)"]
  },
  "drift_suspected": false,
  "unknowns": ["Could not confirm whether the Expenses app reads the new column"]
}
```

### B.5 Thresholds and merge policy

| Final score | Into `integration`, Phases 1 to 3 | Into `integration`, Phase 4 | Into `main` |
|---|---|---|---|
| 0 to 2 | Human approval | Auto-merge if eligible (B.1) and all checks green | Human approval, always |
| 3 to 5 | Human approval; blast radius shown | Human approval | Human approval |
| 6 to 10 | Human approval; blast radius and door shown; second reviewer at 8 and above on client work | Same | Human approval |

The blast radius summary appears whenever the score is above 2. Drift is always a blocker.

## Appendix C: Custom agents and `AGENTS.md`

Front matter keys follow the custom agents reference: `name`, `description` (required), `tools`, `model`, `mcp-servers` ([custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)). Check tool aliases and model identifiers against the reference before use.

### C.1 `.github/agents/lcp-executor.agent.md` (project repo)

```markdown
---
name: lcp-executor
description: GET AI execution agent for one Power Platform story in one factory lane.
model: claude-sonnet-5.5
tools: ["read", "edit", "search", "shell"]
---
You are the GET AI execution agent. You build one story, in one lane environment,
using builders, pac and the Dataverse Web API. You do not decide when the work is done:
the gate does.

Start of session
1. Read AGENTS.md, specs/<NNN>/spec.md, the locked scenarios for this story,
   handoff/<ado-id>/ (state.md, learnings.json, findings.md if present) and the last
   50 entries of docs/lessons-learned.md. Lessons are hints, not rules.
2. Confirm the work item holds an approved mock if the story changes anything a user
   sees (screens, cards, agent wording). If not, write a Markdown mock to
   handoff/<ado-id>/mock.md and PARK with type design_approval.

Rules
- Code over click-ops. Change builder inputs and per-component builders, then run them.
  Never edit generated files or customizations.xml by hand.
- If a step needs the portal or an interactive consent (OAuth connection, admin consent,
  first share of a code app, agent account), STOP. Write handoff/<ado-id>/park.json with
  type portal_step and exact steps for a human, print "PARK: <instruction>" as your last
  line, and end. Do not invent inputs. Do not work around the requirement.
- If the spec is ambiguous in a way that changes behaviour, write the question to
  handoff/<ado-id>/questions.md and PARK with type ambiguity. Never guess at intent.
- If your change drops or changes existing data, a column, a table or a security role,
  PARK with type one_way_door and attach the plan. Do not apply it.
- Identity: never hardcode or inject identity into tool inputs. Rely on x-ms-object-id.
- Never edit tests/, scripts/, .github/, AGENTS.md, CLAUDE.md, builders/lib/ or deploy/.
  The gate will reject it.
- Never run git push, pac auth, pac admin or pac solution delete. The driver pushes.
- Use the dataverse-safe-api skill for every Web API call: honour Retry-After, keep
  concurrency at 8 or less, batch 10 at a time, tag every test row with the run tag.
- After any Entra change, poll for the expected state with a deadline before testing.
- Stop when the credit cap is reached. Do not ask for more.

Each loop
- Run the builders, git diff, pac solution pack and the fast checks. Fix what fails.
  At most 5 loops. Commit after each loop with the trailer Factory-Run-Id: <run_id>.
- Record every change applied to the lane in handoff/<ado-id>/state.md, with the command.
- Append what you tried to handoff/<ado-id>/learnings.json, and new gotchas to
  docs/lessons-learned.md. Update docs/architecture.md if the structure changed.
```

### C.2 `factory-gates/.github/agents/lcp-evaluator.agent.md` (gate repo)

```markdown
---
name: lcp-evaluator
description: Read-only evaluator that grades a Power Platform PR by using the app in the Test environment.
model: claude-sonnet-5.5
tools: ["read", "search", "playwright/*"]
---
You are a harsh, fair evaluator. You did not build this. Assume it is broken until the
evidence shows otherwise. Plausibility is not correctness.

You get: the spec, contract.md if present, the rubric skills, the held-out user stories in
plain language, the deterministic gate results, and a browser session signed in as the test
user against the Test environment. You do not get the builder's transcript, learnings.json
or session state. Do not look for them.

Method
1. For each acceptance criterion and each held-out story, use the app the way a user would.
   Navigate, enter data, submit, check the result in the UI and, where the criterion says
   so, in the records list.
2. Save a Playwright trace and a screenshot for every claim, pass or fail. A claim without
   evidence does not count.
3. Score each rubric criterion against its threshold. Missing evidence for any criterion is
   NEEDS_WORK.
4. Look beyond the happy path: empty values, long values, the back button, a second record,
   keyboard-only use of the key journey.
5. Do not propose fixes. State what is wrong, how to reproduce it, and where the evidence is.

Output: the first line is exactly PASS, NEEDS_WORK or RESTART. Then JSON:
{"verdict": "...", "scores": {...}, "failed_criteria": [{"id": "...", "repro": "...",
"evidence": ["..."]}], "unknowns": ["..."]}
Ask for RESTART only if the same criterion stays below threshold after the second pass, or
the design is wrong at the root.
```

### C.3 `factory-gates/.github/agents/lcp-reviewer.agent.md` (gate repo)

```markdown
---
name: lcp-reviewer
description: Read-only review agent that may raise, never lower, the Merge Danger score.
model: claude-sonnet-5.5
tools: ["read", "search", "shell"]
---
You are the GET AI code review agent. A trusted script has already computed the Merge
Danger floor. You may raise the score. You may never lower it.

Read: the diff against the base, evidence/danger-floor.json, both plans, the evaluator
verdict, AGENTS.md, the spec and the project's architectural decision records.

Check
1. Generated files correspond to their builder changes.
2. Every new or changed behaviour has a locked scenario. Name any that do not.
3. The blast radius: tables, flows, apps, agents, roles and integrations touched, and who
   else uses them.
4. One-way doors the plan may have missed.
5. Breaches of the decision records, and code smells that will cost maintenance.
6. Changes outside the story's scope. Treat any drift as a blocker.

Verify each finding against the code before you report it. If you cannot verify it, list it
under unknowns. Output the JSON in Appendix B.4. Never submit a pull request review.
```

### C.4 `AGENTS.md` (project repo; `CLAUDE.md` holds one line pointing here)

About 100 lines, and a map, not a manual: the repo layout (`src/` generated, `workflows/build/` editable, `builders/lib/` and `tests/` protected, `agents/`, `apps/`, `plugins/`, `handoff/<ado-id>/`); which skill covers which job (`builder-pattern`, `dataverse-safe-api`, `park-protocol`, the vendored Microsoft plugins); and one line on done: "The gate passes and a human merges. Not before." The `trace-reviewer` agent (V2.1) is unchanged, with parked stories, drift detections and evaluator disagreements added to its reading list.

## Appendix D: ADO fields and state map

Process: inherited "Agile build v1". Reference names are suggestions.

### D.1 Custom fields

| Field | Reference name | Type | Written by | Purpose |
|---|---|---|---|---|
| Factory Eligible | `Custom.FactoryEligible` | Boolean | Human; orchestrator validates | Criteria complete and locked scenarios exist (section 6.4) |
| Locked Scenarios Ref | `Custom.LockedScenariosRef` | String | Orchestrator | Paths and SHA-256 of the locked set at approval |
| Lane Profile | `Custom.LaneProfile` | Picklist: code, lcp | Spec gate | Routing |
| Residency Tier | `Custom.ResidencyTier` | Picklist: T1 to T4 | Spec owner | Engine choice (section 9.4) |
| Factory Lane | `Custom.FactoryLane` | String | Orchestrator | `fl1` to `fl3` |
| Night Id | `Custom.NightId` | Date | Orchestrator | Night the story ran |
| Factory Run Id | `Custom.FactoryRunId` | String | Orchestrator | Latest `run_id` |
| Factory Attempts | `Custom.FactoryAttempts` | Integer | Orchestrator | Attempts including RESTART |
| Factory Verdict | `Custom.FactoryVerdict` | Picklist: PASS, NEEDS_WORK, RESTART, PARKED | Orchestrator | Latest evaluator verdict |
| Merge Danger Floor | `Custom.MergeDangerFloor` | Integer | Orchestrator, from the gate | Deterministic floor |
| Merge Danger Score | `Custom.MergeDangerScore` | Integer | Orchestrator, from the gate | Final score |
| One-Way Door | `Custom.OneWayDoor` | Boolean | Orchestrator, from the plan | Irreversible change flagged |
| Blocked Reason | `Custom.BlockedReason` | Text | Orchestrator, from `park.json` | Exact instruction for a human |
| PARK Type | `Custom.ParkType` | Picklist: portal_step, design_approval, ambiguity, one_way_door, budget | Orchestrator | PARK triage |
| Factory PR URL | `Custom.FactoryPrUrl` | String | Orchestrator | Link to the PR |
| Evidence URL | `Custom.EvidenceUrl` | String | Orchestrator | Blob path of the evidence bundle |
| AI Credits | `Custom.AiCredits` | Decimal | Ledger | Measured credits, all runs on the story |
| Cost List USD | `Custom.CostListUsd` | Decimal | Ledger | Fully loaded at list |
| Cost Cash USD | `Custom.CostCashUsd` | Decimal | Ledger | Cash after credits |
| Human Minutes | `Custom.HumanMinutes` | Decimal | Reviewers, through the digest | Review and PARK minutes |

### D.2 States and categories

| State | Category |
|---|---|
| New, Refining, Ready to build | Proposed |
| Queued, Building, Testing, Awaiting review, Awaiting business, Needs rework | In Progress |
| Integrated, UAT Ready, In UAT, Prod Ready | Resolved |
| Done | Completed |

### D.3 Events

The orchestrator Function maps GHE.com webhook events to the transitions in section 5.11: `create` (agent branch), `pull_request` (opened, merged into `integration` or `main`), `check_run` (gate finished), `workflow_run` (execution finished, including a PARK report) and `deployment_status` (`uat`, `prod`).

## Appendix E: Sources and transcripts used

**Research notes**, under `/tmp/claude-0/-home-user-metro-map-of-music/b195798a-3816-5afd-9b0e-91fd7d5ff91b/scratchpad/research_notes/`: six files in `Overnight AI software factory/` (Anthropic harnesses, evals and gates, harness engineering, orchestration and durable engines, runtime and costs, spec-driven development; read 24 October 2026); eight in `Overnight factory on GitHub and Azure/` (cloud agent and Agent HQ, GitHub control plane, billing and partner benefits, Azure infrastructure, cost ledger, primitives parity, the two transcript notes; read 24 to 25 October 2026); six in `Power Platform factory lane/` (the review of the uploaded plan, the uploaded plan in two forms, ALM and identity, testing and evaluation, agent tooling; read 1 November 2026).

**Earlier reports**, under `.../scratchpad/reports/`: "Grill the Spec, Lock the Tests" (`Overnight AI software factory.md`), V1, V2 and V2.1 ("Two Lanes, One Gate, Priced at List").

**Uploaded plan.** Boroon Mahanta, "End-to-End Specification: The GET AI Microsoft Software Factory" and "Copilot Studio Agents & App Builds", 1 November 2026.

**Transcripts** (both supplied by Boroon):

- Anthropic, "How to Build Agents That Run for Hours (Without Losing the Plot)", AI Engineer, with five slides ([edited transcript](https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript)) **[user-supplied transcript]**.
- GitHub, "Open Source Friday: Spec Kit Part 2", 16 October 2026 ([video](https://www.youtube.com/watch?v=8hHCpNVLhmI)) **[user-supplied transcript]**.

**Primary source families** cited inline: Anthropic engineering and research posts and Claude Code docs; OpenAI and Lopopolo's harness-engineering corpus; GitHub Spec Kit; GitHub Docs (Copilot, Actions, rulesets, billing, OIDC, data residency, source read on 23 October and 1 November 2026); Microsoft Learn (Power Platform ALM, administration, Dataverse, Power Automate, Copilot Studio, code apps, Playwright samples, Entra, Azure Container Apps, Foundry, Partner Center); Microsoft repos `power-platform-skills`, `Dataverse-skills`, `powerplatform-actions`, `vscode-copilotstudio`; npm registry metadata for `@microsoft/dataverse` and `@microsoft/copilot-studio-mcp`.
