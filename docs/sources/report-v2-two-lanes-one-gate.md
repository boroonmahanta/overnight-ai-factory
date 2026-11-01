# Two Lanes, One Gate, Priced at List

**Bottom line.** Run the factory in two lanes behind one gate. Lane A takes new apps and feature-sized builds. A planner drafts a high-level spec by day and a human approves it. Overnight, one long Copilot SDK session builds it in an Azure Container Apps job, then a separate evaluator session grades the running app with Playwright and rubric skills. Lane B takes issue-sized changes in existing code through V1's cloud agent flow, which fits the 59-minute cap. Copilot already ships most of the workshop's harness: custom agents, skills, hooks, Playwright MCP, long SDK sessions with compaction, and OpenTelemetry. So build only thin glue we expect to delete, and invest where the platform will not: calibrated rubrics, the evaluator and its calibration set, trace review, and the cost ledger. Lane A cost per agent role is measured from OpenTelemetry. Lane B stays estimated and reconciled to daily billing. On our model a Lane A build costs about USD 100 to 200 in AI credits at list. One Solutions Partner designation gives about USD 1,250 a month in credits. That buys about seven Lane A builds, 26 light Lane B nights, or a mix such as four builds and 12 nights. The biggest risk is still contractual. Microsoft calls partner Azure credits "internal-use-rights" credits, so run client work at cash until a written ruling says otherwise. Get Claude through Copilot, not Foundry. Price every client job from the ledger's list column. Evaluator quality and review minutes move margin more than token price does.

**What changed in V2**

- Two lanes. Feature builds move off the cloud agent to one long SDK session in Container Apps (Lane A). Issue-sized work keeps V1's flow (Lane B). A routing rule decides.
- A harness parity table, and a component register that marks each part as shipped primitive, thin glue or IP.
- Spec rules: high-level specs, a floor of 20 to 30 acceptance criteria, and `contract.md` as a switch.
- Evaluator: isolated and read-only, rubric skills with calibration examples, and a RESTART verdict.
- Traces: OpenTelemetry to Application Insights, a trace-review agent, and weekly human calibration.
- A named handoff file set on every task branch.
- Ledger: measured cost per role on Lane A, new columns, and Lane A and Lane B unit economics reported apart.
- Cost: a Lane A build modelled at USD 100 to 200 at list, with credit coverage per lane and for a mix.
- Stages: new stage 0 tests and a Lane A stage, eight stages in all. Seven new risks. A rewritten transcript section.

**How to read this.** All prices are USD list as read on 24 to 25 October 2026. Figures labelled "model" are arithmetic on stated assumptions, not measurements. A citation with no marker was read in full by the researchers. **[secondary]** means a third-party write-up was read, not the original. **[snippet]** means only a search summary was available, so treat it as unverified. **[talk mm:ss]** cites a timestamp in Anthropic's workshop "How to Build Agents That Run for Hours (Without Losing the Plot)" ([edited transcript](https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript)) **[user-supplied transcript]**. Boroon supplied the transcript and five slides, because the page is blocked from the research environment. This V2 revises V1 at `/tmp/claude-0/-home-user-metro-map-of-music/b195798a-3816-5afd-9b0e-91fd7d5ff91b/scratchpad/reports/Overnight factory on GitHub and Azure.md`, which built on `/tmp/claude-0/-home-user-metro-map-of-music/b195798a-3816-5afd-9b0e-91fd7d5ff91b/scratchpad/reports/Overnight AI software factory.md`. It does not repeat their research.

## 1. The earlier design holds; two lanes change where each part runs

The earlier report's design still stands:

- A daytime gate that questions the spec owner until every acceptance criterion has an executable check.
- Acceptance tests written by a separate author and locked before the night, plus a held-out suite the worker never sees.
- State in files and git, not in the model's context.
- A "done" verdict that never comes from the worker: CI plus a fresh-context evaluator with Playwright evidence.
- Serial integration, a human merge in the morning, and a morning evidence package.

Some Copilot limits enforce this for free: one PR per task, a hard session cap, and a rule that the person who started a task cannot approve its PR ([risks and mitigations](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations)).

One earlier default changes. The earlier report made fresh context per task the safe default. Anthropic dropped context resets on Opus 4.6, because one continuous session with compaction held a two-hour build together [talk 34:14 to 36:08]. So Lane A runs one long session per build. Lane B keeps one bounded task per session.

| Earlier part | GitHub and Azure version | Note |
|---|---|---|
| `/grill` skill plus gate script | `planner` and `grill` custom agents in `.github/agents/`, run by day in VS Code or Copilot CLI. The gate script runs as a required check on the spec PR. | Day use bills to the human's seat. Custom agents fix the prompt, model and tools ([custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)). |
| Separate test author | `test-author` agent by day. `@acceptance-owners` push the tests. | Only that team may change `tests/acceptance/**` ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)). |
| Held-out suite | Private `factory-gates` repo, checked out by the required workflow. | The cloud agent sees only its working repo and no Actions secrets ([Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github); [secrets](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables)). Our inference. |
| Supervisor on a VM | Four short Actions workflows (kickoff, dispatch, tick, report), a ledger Function, and a small driver inside each Lane A job. | No always-on VM. |
| Worker: `claude -p --worktree` | Lane B: a cloud agent task via `POST /agents/repos/{owner}/{repo}/tasks` with `custom_agent`, `model` and `base_ref` ([agent tasks API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api)). Lane A: a Copilot SDK session in an Azure Container Apps (ACA) job. | Section 2. |
| Hooks, budget and turn caps, auto mode | `.github/hooks` ([hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)), SDK hooks ([SDK hooks](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/hooks)), `--max-ai-credits` and `sessionLimits.maxAiCredits` ([CLI session limit](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit); [SDK session limits](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/session-limits)). | Credit caps are soft. The cloud agent has none per session, so use a hard-stop user budget. Section 3. |
| `AGENT_STOP` kill switch | `factory-stop` workflow: stop sessions, cancel ACA executions, remove the repo from the cloud agent's allowed list ([enable cloud agent](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/add-copilot-cloud-agent)). | |
| Evaluator subagent | Fresh SDK session, read-only `evaluator` agent: inside each Lane A job, and as a required gate job in both lanes. | Copilot code review at Lite is a second opinion only. |
| CI gate and serial merge | Organisation ruleset "Require workflows to pass before merging" pointing at `factory-gates`; merge queue on a fixed `integration` branch. | The PR cannot edit the gate. Merge queue cannot use wildcard patterns ([merge queue](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)). |
| Human merge and morning package | One `integration` to `main` PR approved by a human who did not start the tasks. Evidence to Blob, a card to a Teams Workflows webhook. | Teams classic connectors are retiring ([Teams webhooks](https://learn.microsoft.com/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)). |
| DBOS or Temporal; scheduled tasks | Durable Functions on the Durable Task Scheduler ([DTS](https://learn.microsoft.com/azure/durable-task/scheduler/durable-task-scheduler)) when section 9's triggers apply. Copilot automations for chores ([automations](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations)). | Automations bill to their creator. |

## 2. Two lanes: route by size, not by habit

The cloud agent's 59-minute cap suits issue-sized work. It does not suit a new app or a whole feature. So the factory runs two lanes into one gate.

### Lane A: greenfield and feature-sized builds

By day, the `planner` agent (Opus 5.5) turns the brief into a deliberately high-level `spec.md`: outcomes, journeys, constraints, NFRs and acceptance behaviours [talk 23:59 to 24:56]. The `grill` agent questions the spec owner until there are at least 20 testable criteria. The `test-author` agent writes the locked tests. A human approves spec and tests in one PR.

Overnight, in one ACA job execution per build:

1. A small TypeScript driver starts a headless Copilot CLI and one long SDK session with the `generator` agent. Default model: Claude Sonnet 5.5 through Copilot, or Opus 5.5 for hard or design-heavy builds. Sessions we host have no 59-minute cap and no idle timeout by default ([SDK backend services](https://docs.github.com/en/copilot/how-tos/copilot-sdk/setup/backend-services)). The cap point is our reading. `infiniteSessions` compacts in the background ([SDK scaling](https://docs.github.com/en/copilot/how-tos/copilot-sdk/setup/scaling)).
2. The generator commits often and keeps the handoff files current. The driver re-sends `spec.md` on a fixed cadence.
3. When the generator stops, the driver runs fast checks and sends failures back, up to a cap.
4. The driver boots the app and opens a fresh `evaluator` session with Playwright MCP and the rubric skills. It returns PASS, NEEDS_WORK or RESTART with scores. On NEEDS_WORK, `findings.md` goes back to the generator. Plan 2 to 3 passes, more for design-heavy work. Anthropic's frontend-only runs used 5 to 15 [talk 22:32 to 22:49].
5. The output is a PR into `integration` with evidence. The gate and merge queue treat it like any other PR.

### Lane B: brownfield, issue-sized changes

This is V1's night flow. The cloud agent takes a 20 to 40 minute task through the tasks API. `agentStop` runs fast checks. The gate evaluator grades the draft PR. The tick runs at most two `@copilot` review rounds, and the merge queue integrates. It matches the workshop's brownfield SDLC loop: monitoring raises an issue, an agent makes the PR, a review runs, a human reviews before merge [talk 71:28].

### The routing rule

| Lane A, when any is true | Lane B, when all are true |
|---|---|
| Expected agent work is over about 40 minutes | The change is issue-sized, in an existing codebase |
| It is a new app or service | Expected agent work is 20 to 40 minutes |
| The feature spans components (UI, API, data) | It touches files no other task touches |
| Design-heavy UI, where taste matters | Existing tests and CI cover the area |

The grill records the lane in the spec header, and the gate script checks it. A large feature in existing code goes to Lane A, with the evaluator pointed at the codebase and the spec, plus custom rubrics [talk 63:19 to 65:31; 71:00 to 72:06]. Do not split it into a chain of cloud agent tasks.

**Why feature builds stay off the cloud agent.** Fitting a feature into 59-minute sessions would force back what Anthropic removed on Opus 4.6: context resets, sprint decomposition, per-sprint evaluation and sprint contracts (slide "The simplified harness"; [talk 34:14 to 36:08]). That is the IKEA trap in reverse. We would be rebuilding scaffolding the model no longer needs, only because one product has a session cap. The SDK on our own compute is a shipped primitive without that cap.

### Container Apps facts that shape Lane A

- `replicaTimeout` is "the maximum number of seconds a replica is allowed to run". No maximum is documented on the pages read. The Azure Verified Modules job module defaults it to 1,800 seconds, so set it explicitly, for example 27,000 seconds for 7.5 hours ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs#advanced-job-configuration); [AVM job module](https://github.com/Azure/bicep-registry-modules/blob/main/avm/res/app/job/README.md)). Test the longest accepted value in stage 0.
- "Platform maintenance, including routine security updates and upgrades, might interrupt long-running job replicas." Microsoft says to set the retry limit to at least 1 and design for at-least-once processing ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs#advanced-job-configuration)).
- So every build is resumable. Session state (`~/.copilot/session-state/<sessionId>/`, via `COPILOT_HOME`) sits on Azure Files. The generator commits after every pass and every 20 minutes. On retry, the driver resumes the session by id and has the model re-read the handoff files, or starts fresh from them.
- The CLI keeps a SQLite session store, which can lock badly on a network share. Test resume in stage 0, with Blob copies as the fallback (our inference).
- One build per execution. The driver's deadline sits 30 minutes before `replicaTimeout`, so it can always push or park.

## 3. Harness parity: the workshop's primitives on Microsoft

The aim is to use what VS Code, GitHub Enterprise and Copilot already ship, and avoid the IKEA effect: over-valuing scaffolding we build ourselves when the platform ships it, or soon will. The workshop's slide says it: "The harness patterns that work tend to get absorbed back into the tools" [talk 37:58 to 38:52]. Unless a row says otherwise, the Copilot column comes from the [customisation cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet), the [custom agents reference](https://docs.github.com/en/copilot/reference/custom-agents-configuration) and the [hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference).

| Workshop requirement | Microsoft equivalent | Status | Fix |
|---|---|---|---|
| Planner writes a high-level spec, then stays out of the loop [talk 23:59 to 24:56; 49:51] | `planner` custom agent by day, `model` pinned to Opus 5.5 | At parity | Spec rules (section 4). Never runs at night |
| One continuous generator session with compaction [talk 34:14 to 36:08] | SDK session in an ACA job with `infiniteSessions` | At parity on Lane A; gap on the cloud agent | Lane A for feature builds; resumable sessions |
| Adversarial evaluator using the running app [talk 18:42 to 19:31] | Separate SDK session, read-only `evaluator` agent, Playwright MCP. The cloud agent ships a localhost `playwright` server | At parity | Harsh prompt plus calibration (sections 4, 5) |
| Rubrics that make taste gradable [talk 21:31 to 22:23] | Skills in `.github/skills` | Format at parity; content is ours | Rubric skills are IP |
| Sprint contracts and granular criteria [talk 25:12 to 26:46; 32:04] | Nothing built in | Partial | `contract.md`, a 20-criteria floor, negotiation as a switch |
| Files as shared state; structured handoffs over compaction [talk 38:52; 54:08 to 56:04] | Git plus handoff files. `sessionStart` and `postToolUse` hooks can inject context; `preCompact` only notifies | At parity | Handoff file set; the driver re-sends `spec.md` |
| Read the traces [talk 33:51; 62:09] | OpenTelemetry from CLI and SDK with content capture; `events.jsonl`; `--share` ([CLI OpenTelemetry](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#opentelemetry-monitoring)) | At parity on Lane A; gap on the cloud agent (log text only) | Section 5 |
| Evaluator isolated from generator context [talk 60:03 to 61:04] | Separate session, agent and `COPILOT_HOME` | At parity once wired | `preToolUse` deny on progress logs |
| Throw it out and restart [talk 23:08; 47:11] | Nothing built in | Gap | RESTART verdict: reset the worktree (A); close and re-dispatch (B) |
| Auto mode ("safe YOLO") [talk 37:58] | None: no classifier-based approval ([allowing tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools)) | Gap | Layered controls, below |
| Subagents; a critic per sub-builder [talk 57:12 to 59:53] | Yes in VS Code, CLI and SDK (plus fleet mode). Cloud agent docs conflict: the cheat sheet says no, yet an `agent` tool alias and `subagentStart` and `subagentStop` hooks exist | Partial | Do not depend on them on the cloud agent. Trial on Lane A after stage 4 |
| Skills with progressive disclosure [talk 10:41 to 12:05] | `.github/skills`; Copilot also reads `.claude/skills` and `.agents/skills`. The cloud agent and code review load them | At parity | One rubric skill serves Copilot and Claude Code |
| Done decided by someone other than the worker | Autopilot and `/goal` run until the model calls `task_complete`: self-declared, no judge ([CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)) | Partial | Keep `agentStop` and the external evaluator |
| Stop-hook loop with a turn limit [talk 7:55 to 9:43] | `agentStop` with `decision: "block"`; `--max-autopilot-continues`; in the SDK the driver is the stop hook. Subagent stop blocks lapse after eight in a row | At parity | Counter in the hook, cap in the driver. On the cloud agent a blocked stop still burns the 59 minutes |
| Hand back to a human at a stop condition [talk 46:44; 69:11] | Hooks plus glue; dynamic workflow checkpoints; Durable Functions external events; SDK `session_limits_exhausted.requested` | Partial | Park with `needs-human.md` and a Teams card. Fix the harness rather than add a human |
| Chained generator and critic pairs [talk 51:00 to 51:57] | Dynamic workflows: steps plus agents, checkpoints, resume, headless `copilot workflow run` ([dynamic workflows](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/dynamic-workflows); [use them](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-dynamic-workflows)) | Partial: public preview | Trial in stage 4, TypeScript driver as fallback |
| Model per role: Opus to plan, Sonnet to build [talk 52:43 to 53:50] | `model` pinned per custom agent | At parity | Evals per role, model and prompt |
| Delete scaffolding as models improve [talk 34:14; 42:29 to 43:53] | A process, not a product | Process | Component register, below |

**Auto mode, rebuilt in layers.** No single Copilot switch gives "safe YOLO". Stack these:

1. `--available-tools` limits what the model sees.
2. `--allow-tool` and `--deny-tool` patterns, such as allow `shell(npm:*)`, deny `shell(git push)`. Deny beats allow, even with `--allow-all`. Non-interactive runs deny anything not pre-approved, so test allow lists by day ([allowing tools](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools)).
3. CLI local sandboxing: deny-by-default filesystem, OS-confined shell and local MCP. Built-in file tools are checked in software only, and remote MCP is not covered ([local sandboxing](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/understanding-local-sandboxing)). It uses bubblewrap, so test it inside ACA (our inference).
4. `preToolUse` and SDK `onPreToolUse` hooks deny protected paths and risky commands.
5. Egress limits: a VNet behind Azure Firewall or NAT Gateway on Lane A; the cloud agent firewall on Lane B.
6. Rulesets and the required workflow, enforced on GitHub's side.

Never use `--yolo` outside the job container. Inside it, prefer explicit allow lists anyway.

### Component register

Review this list in the week after GitHub Universe (28 to 29 October 2026) and after each model release.

| Class | Rule | Components |
|---|---|---|
| Shipped primitive | Use as is. Do not wrap it | Cloud agent and tasks API; CLI and SDK with compaction and session limits; custom agents, skills, hooks; Playwright MCP; OpenTelemetry; Copilot code review; rulesets, required workflows, merge queue, CODEOWNERS, cost centres, budgets; ACA jobs, Key Vault, Blob, Application Insights, Log Analytics, FOCUS exports, Durable Functions |
| Thin glue | Keep it small. Expect to delete it | The four Actions workflows; the Lane A driver (until dynamic workflows reach GA); RESTART logic; spec re-send; the contract switch; hand-back glue; cloud agent cost estimates (until a per-session cost API ships); session log export (until an export API ships); the routing rule (if the 59-minute cap changes) |
| IP | Invest | Rubric skills and calibration examples; evaluator prompts and calibration set; trace-review agent; trace view; ledger, reconciliation and matrix; grill gate, spec template and gate script; regression task set; `factory-gates` template and Bicep |

Each review asks of each thin-glue item: does a shipped primitive now do this? If yes, delete it after one regression run.

**The simplification depends on the model.** Anthropic validated the simplified harness on Claude. If a role moves to a GPT model, re-run the regression set before removing any scaffolding for that role [talk 53:14]. The same goes for rubric weights.

## 4. The daytime gate: spec, contract, handoff and evaluator rules

### Spec rules

- The grill pins down outcomes, user journeys, constraints, NFRs and acceptance behaviours.
- It leaves technical design to the night, unless it is a hard constraint: stack, identity, data residency or a client integration. Granular up-front plans cascade errors: an early mistake "is going to cascade through every single one of these sprints" [talk 24:12 to 24:46].
- A feature-sized spec needs about 20 to 30 testable acceptance criteria. "If you have vague criteria, you have vague critiques." The talk's example had 27 [talk 32:04 to 32:40]. The gate script fails a Lane A spec with fewer than 20. Lane B has no floor, but every criterion needs an executable check.
- Tests come before code, so the spec carries a short testability contract: routes, accessible names, stable test ids for key elements, health endpoints. Locked Playwright tests target these and visible behaviour, never internal structure.
- Standing NFRs ask the generator to build testability in: a dev-only debug overlay, stable test ids, and `/healthz` and `/readyz`. Anthropic's generator added a debug HUD "to make life easier for the evaluator" [talk 30:37]. A gate lint fails the build if the overlay is on in production config.
- The gate script warns when a spec names libraries, schemas or file layouts outside its Constraints section.

### Contract rules

- The locked acceptance tests stay the human-approved contract. Nothing at night weakens them.
- In `contract.md`, the generator and evaluator may add criteria for anything the locked tests do not cover. They may add or tighten, never remove.
- Contract negotiation is a switch, off by default on Sonnet 5.5 and Opus 5.5. Turn it on when a feature spans sessions (for example two nights), or when a role runs on a model the evidence has not covered. When on, the generator proposes what it will build and how to verify it, the evaluator pushes back in the file, and code starts when both agree [talk 25:12 to 26:46].
- The driver re-sends `spec.md` to generator and evaluator every 25 turns and after each compaction [talk 49:51 to 50:42]. Both numbers are starting assumptions.

### Handoff files

Every task branch carries this set, so a restarted session, a resumed replica or a human can pick up the work [talk 54:08 to 56:04].

| File | Written by | Purpose |
|---|---|---|
| `factory/specs/<feature>/spec.md` | Human-approved by day | Frozen by the push ruleset and a hash check |
| `handoff/<task>/contract.md` | Generator and evaluator | Criteria beyond the locked tests |
| `handoff/<task>/learnings.json` | Generator | Timestamped log: tried, evaluator found, fix, worked. JSON because models overwrite it less [talk 12:05 to 14:20] |
| `handoff/<task>/findings.md` | Driver, from evaluator output | Latest verdict, scores, failed criteria with repro steps |
| `handoff/<task>/evidence/` | Driver | Screenshots, Playwright traces, scores JSON |
| `docs/architecture.md` | Generator | Living, high-level map of the code |

Lane B uses `learnings.json`, `findings.md` and `evidence/`, and `findings.md` doubles as the batched `@copilot` review. The talk says a JSON log plus a structure doc "are more than enough for Claude Code and a human to come in and start iterating" [talk 54:08 to 56:04]. That makes long-lived and brownfield work resumable by a human.

### Evaluator design

- **Isolation.** A separate session with a read-only custom agent. It gets `spec.md`, `contract.md`, the rubric skills, the running app and read-only code. Never `learnings.json`, transcripts or session state [talk 60:03 to 61:04], because "it's very easy for the model to kid itself". Enforce it with the `tools` list, a separate `COPILOT_HOME`, and a `preToolUse` deny on `handoff/*/learnings.json`.
- **Prompt.** Harsh by design. "Tuning a standalone critic to be harsh is actually very tractable, but tuning a builder to be somewhat self-critical is not" [talk 20:05].
- **Rubric skills** in `.github/skills/`:
  - `rubric-product`: design, originality, craft and functionality, weighted towards design and originality, with weights per model [talk 21:31 to 22:23]. Hard thresholds per criterion. Calibration examples of good design and AI slop, such as purple gradients [talk 21:40]. For line-of-business client apps, weight originality down and add brand fit.
  - `rubric-api` for API design and `rubric-code` for code quality [talk 63:19 to 65:31]. Code review loads skills, so `rubric-code` can steer the Lite review ([code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review)).
- **Model.** Start with one evaluator model, Sonnet 5.5, in both lanes, so one calibration set covers it. Trial Opus 5.5 as the Lane A evaluator in stage 4, and keep it if agreement with humans rises enough to pay for it.
- **Output.** JSON: verdict, per-criterion scores, failed criteria, evidence paths.

| Verdict | Lane A | Lane B |
|---|---|---|
| PASS | Open the PR into `integration` | The App marks it ready and enqueues it |
| NEEDS_WORK | `findings.md` back to the generator | One batched `@copilot` review; two rounds at most |
| RESTART | Reset the worktree to the base commit. Keep spec, contract and `learnings.json`. Fresh generator session | Close the PR. Dispatch a fresh task with the findings in the prompt |

RESTART fires when the evaluator asks for it, or when one criterion stays below threshold for two passes [talk 23:08 to 23:42; 47:11]. Allow one per build or task per night, only if the budget covers a fresh attempt, and none after 02:00 on Lane A. It does not count against Lane B's two review rounds or its one timeout re-dispatch, so V1's caps no longer block a restart.

## 5. Traces and the calibration loop

"Read the traces. They're your primary debugging loop" (Takeaways slide, [talk 38:52 to 39:51]).

### What to capture

- Lane A's generator and evaluator, the gate evaluator and the trace reviewer run on CLI or SDK with OpenTelemetry on (`COPILOT_OTEL_ENABLED=true`), exporting to Application Insights ([SDK OpenTelemetry](https://docs.github.com/en/copilot/how-tos/copilot-sdk/observability/opentelemetry); [OTLP ingestion](https://learn.microsoft.com/azure/azure-monitor/containers/opentelemetry-protocol-ingestion)).
- `OTEL_RESOURCE_ATTRIBUTES` carries `project`, `run_id`, `task_id`, `lane` and `role`. Each run emits an `invoke_agent` span with `chat` and `execute_tool` children ([Copilot OpenTelemetry](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)).
- Content capture (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`) is on for factory runs only. It adds full messages, system instructions and tool arguments.
- Each run's `events.jsonl` and `--share` transcript go to Blob ([CLI programmatic reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference)).
- Resource attributes ride on every signal. If metrics are exported too, strip `run_id` from them in an OpenTelemetry Collector (section 10).
- The cloud agent has no transcript export and no OpenTelemetry. Lane B worker traces are the log text from `gh agent-task view --log` ([cloud agent CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli)). The Lane B evaluator runs on the SDK, so it is traced.
- Enterprise managed settings can switch OpenTelemetry on in VS Code too, which measures daytime planner and grill cost per spec. Keep content capture off for human sessions.

### Who reads them

- A `trace-reviewer` agent does the first pass each morning [talk 33:51; 62:09]. It reads RESTARTs, parked builds, tasks at the review cap, PASS verdicts that later failed the held-out suite, and verdicts a human disagreed with. It says where the evaluator's judgement diverged and drafts a prompt or rubric PR.
- Humans read failures in full: "No, you gotta read the whole thing" [talk 73:25 to 74:41]. At least one failed trace each morning.

### Weekly calibration

1. Sample 10 evaluator verdicts across both lanes and all three verdicts.
2. A human grades each one blind: verdict and per-criterion scores.
3. Track evaluator-human agreement on the verdict, and the score gap per criterion. Start with an 80% target (assumption).
4. Read the traces behind each disagreement. Change prompts or rubrics by PR only. Agents and skills load from the default branch, so every change is reviewed.
5. Record `evaluator_version` as the commit SHA of the evaluator agent and rubric skills. Agent profiles are versioned by commit SHA ([custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)).
6. Keep every graded case. Re-run a new evaluator version on the graded set before merging it.

When tuning, run the same spec about 10 times and read the failures [talk 70:02 to 70:25]. Use a small reference spec: 10 full Lane A builds cost about a month of credits.

### The data risk

Captured content can include client code and secrets. So: short retention on content tables; access limited by Azure RBAC to the factory team; in Mode B, one Application Insights resource per client project in that client's subscription, in Australia East; content capture off unless the client contract allows it. Add every injected secret to `--secret-env-vars`, and check in stage 0 that redaction also covers captured traces.

## 6. Credits fund the internal factory; client work waits on one written answer

### What the designation gives you

| Benefit, per year | One Azure-area Solutions Partner designation | Each Azure specialisation (cap of 5) |
|---|---|---|
| Azure bulk credits | USD 10,000 | plus USD 12,000 |
| GitHub Copilot Enterprise (via Azure credits) | USD 5,000 | plus USD 4,680 |
| GitHub Enterprise Metered (via Azure credits) | none | plus USD 2,520 |
| Visual Studio Enterprise | 25 IDE licences, no monthly Azure credit | plus 10 full subscriptions |
| GitHub Enterprise seats or Actions minutes | none | none |

Source: [benefits guide summary](https://learn.microsoft.com/partner-center/benefits/benefits-at-a-glance). The designation fee is USD 4,875 a year ([pay the fee](https://learn.microsoft.com/partner-center/membership/mpn-pay-fee-silver-gold-competency)). The partner FAQ quotes USD 5,320 for the specialisation Copilot retrofit, which conflicts with the guide's USD 4,680 ([benefits FAQ](https://learn.microsoft.com/partner-center/benefits/benefits-faq-new)). Microsoft says GitHub credits from specialisations "can only be used for those purposes".

Other terms that shape the design:

- Credits are yearly, expire with membership, align to the offer purchase date from 1 November 2026, and are revoked if the purchase is cancelled ([use your Azure credits](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud); [August 2026 announcements](https://learn.microsoft.com/partner-center/announcements/2026-august)).
- They land on an MCA billing profile with a card attached, one credit source per profile, and subscriptions cannot leave it while credits are active.
- They cover first-party Azure only: not Marketplace, reserved instances or support ([MCA credits](https://learn.microsoft.com/azure/cost-management-billing/benefits/credits/mca-check-azure-credits-balance)).
- Copilot seats, AI credit overage, Actions and GitHub Enterprise can bill to an Azure subscription connected to the enterprise or a cost centre. Usage lands on the next month's invoice ([Copilot Azure billing](https://docs.github.com/en/copilot/reference/copilot-billing/azure-billing); [Azure subscription reference](https://docs.github.com/en/billing/reference/azure-subscription)).
- No page says in one place that partner credits pay these GitHub meters, though the benefit names show Microsoft intends it. GitHub lists Azure subscription types it will not accept, and a Microsoft Q&A answer contradicts that list, so test it ([supported payment methods](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/supported-payment-methods); [Q&A](https://learn.microsoft.com/answers/a/12897076)).
- Whether credits pay GitHub Enterprise seats is unclear. Another Microsoft program says "Azure cannot pay for Enterprise licenses" ([Startups GitHub Enterprise](https://learn.microsoft.com/startups/investor-network-benefits/technical-benefits/github-enterprise)). The specialisation's metered credit suggests seats are covered there. Probable, not confirmed.

### The eligibility risk

Microsoft's own wording is the warning sign. Partner credits "can't be moved or transferred outside the Billing Account boundary. This guardrail ensures that internal-use-rights credits stay within the partner organization" ([credits FAQ](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud#azure-credits-faqs-legacy-experience)). Partner Visual Studio Enterprise subscriptions "are for internal use only", and may not be used to "Develop, test, or maintain applications as part of customer or client projects" ([VS Enterprise for partners](https://learn.microsoft.com/visualstudio/subscriptions/program-mcpp#internal-use-only-restriction)). The binding rules sit in the AI Cloud Partner Program Terms of Participation Guide ([manage your benefits](https://learn.microsoft.com/partner-center/benefits/manage-your-partner-network-benefits#types-of-benefits)), which the researchers could not read. So nobody knows yet whether the credits can fund client delivery.

**The single check that resolves it.** Send Partner Center support one question in writing, and ask them to cite the Terms of Participation Guide:

> "May Get AI use its Solutions Partner Azure bulk credits and its GitHub Copilot Enterprise (via Azure credits) benefit to pay for GitHub and Azure metered usage that Get AI incurs while delivering a paid client engagement, where the client never receives the credits, the subscription or the GitHub accounts?"

Keep the answer on file. Until it arrives, assume no. A mechanical test belongs in stage 0: connect the credited subscription to a test cost centre and check that the next invoice shows "Azure credits applied" against the GitHub lines ([MCA invoice terms](https://learn.microsoft.com/azure/cost-management-billing/understand/mca-understand-your-invoice#invoice-terms-and-descriptions)).

### Two modes, split at the billing boundary

| | Mode A: internal | Mode B: client |
|---|---|---|
| Work | The factory, the accelerator, Get AI-owned IP, internal tools | Client deliverables |
| GitHub | Cost centre `cc-internal-<project>`, own seated machine account | Cost centre `cc-<client>-<project>`, own seated machine account |
| Azure | Subscription on the credited MCA billing profile | Subscription on a separate profile with no credits, paid by card or invoice |
| Funding | SPD credits | Cash, unless the ruling allows credits |
| Ledger | Priced at list for internal ROI | Priced at list; cash cost equals effective cost |

Each cost centre can connect to a different Azure subscription ([Azure subscription reference](https://docs.github.com/en/billing/reference/azure-subscription)). Subscriptions cannot leave a credited profile, so set this split up before the first night. If the ruling says yes, only Mode B's funding line changes. Either lane can run in either mode.

### What this means for model choice

| Path | Billed as | On credits? | Region | Use it for |
|---|---|---|---|---|
| Claude (Sonnet 5.5, Opus 5.5) through Copilot: cloud agent, SDK, CLI | GitHub AI credits at Anthropic's list rates ([rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml); [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)) | Yes, via the Copilot benefit and Azure-billed GitHub meters, subject to the ruling | Not stated in the notes | Default for every role in both lanes |
| OpenAI models through Copilot (GPT-6.1 Sol, GPT-5.3-Codex, GPT-6 Luna) | GitHub AI credits | Same | Not stated | Lane B worker alternative; Luna for chores. Re-run the regression set before Lane A use |
| Azure OpenAI in Foundry (GPT-5.x, Codex, GPT-6) | First-party Azure meter | Yes: models "sold and billed directly by Azure" ([credit coverage](https://learn.microsoft.com/en-us/microsoft-for-startups/build/foundry-model-sponsorship-coverage)) | Australia East options, for example Global PTU for gpt-5.1-codex ([PTU](https://learn.microsoft.com/azure/foundry/openai/concepts/provisioned-throughput)) | Model calls outside Copilot; the Codex lane; clients who want Azure-contracted inference |
| Claude in Microsoft Foundry | Marketplace, in Claude Consumption Units ([CCU billing](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-billing)) | No: "the credit card will be charged instead of Azure Credits" ([deploy Claude](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-claude)) | US and Sweden Central only ([regions](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-from-partners#region-availability-by-deployment-type)) | Only when a client mandates Claude on its own Azure contract and pays cash |
| Anthropic API direct | Anthropic invoice | No | n/a | Claude Code bake-offs at cash |

Rules that follow:

- On credits, get Claude through Copilot, not Foundry. Same per-token price, different payer.
- Pin a model per role: Opus 5.5 for the planner; Sonnet 5.5 for the generator (Opus 5.5 for hard builds); Sonnet 5.5 or GPT-6.1 Sol for the Lane B worker, with 20% of tasks on Opus 5.5; Sonnet 5.5 for the evaluator and trace reviewer; GPT-6 Luna for chores.
- Use Azure OpenAI for model calls outside Copilot. GitHub Models is retired (section 9).
- Do not plan on Claude in Foundry for Mode A. Its default quota is 40 RPM, 40,000 uncached input TPM and 8,000 output TPM, and Fable has zero ([Claude quotas](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-quotas-limits)).
- Check client data rules before sending client code to Copilot-hosted models. The notes do not establish where Copilot inference runs. Data-resident requests cost 10% more ([seats and billing cycles](https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/billing-and-usage/organizations-and-enterprises/seats-and-billing-cycles.md)).

## 7. GitHub runs the work, Azure keeps the records

GitHub runs anything that touches code: dispatch, the Lane B agent, the gate, the merge. Azure runs anything that must outlive a GitHub retention window or needs a fixed identity: Lane A builds, secrets, evidence, telemetry and the ledger.

| Layer | Runs on | Paid from in Mode A | Notes |
|---|---|---|---|
| Spec gate, test author | Spec owner's VS Code or Copilot CLI, by day | Human's Copilot seat | `planner`, `grill`, `test-author` |
| Kickoff, dispatch, tick, report | Actions on standard Linux runners | Included minutes | `schedule` with an IANA `timezone`, at odd minutes ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)) |
| Lane B worker | Cloud agent on an ephemeral runner with firewall | AI credits on the machine account, plus minutes | Stage 2 |
| Lane A generator and evaluator | SDK sessions in one ACA job execution per build, Australia East, state on Azure Files | AI credits plus Azure credits | Stage 4 |
| Gate evaluator | Job in the required workflow: SDK, `evaluator` agent, Playwright | AI credits plus minutes | Both lanes |
| Second opinion | Copilot code review at Lite | AI credits plus minutes | Severity sits in comment text |
| Trace review | Copilot CLI in a morning Actions job, as the machine account | AI credits plus minutes | `trace-reviewer` |
| Gate | Org required workflow from `factory-gates`; branch and push rulesets | Minutes | Section 8 |
| Integration | Merge queue on `integration` | Minutes | Fed by the factory App |
| Secrets | Key Vault, via Actions OIDC and ACA managed identity | Azure credits | OIDC tokens can carry `repo_property_<name>` claims for per-project scope ([OIDC](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/security/openid-connect)) |
| Evidence | Blob, one container per project; audit log stream | Azure credits | Section 9 |
| Telemetry | Application Insights with OTLP, plus Log Analytics | Azure credits | Content capture for factory runs; daily cap |
| Ledger | Azure Function on a timer, PostgreSQL flexible server (Burstable), Power BI | Azure credits; Power BI licence probably not | Section 10 |

**Identities.** Three kinds, no more:

- One seated machine account per project, for example `getai-p042-bot`, in that project's cost centre with a user-level budget. Its token lives in Key Vault. Lane B dispatch and Lane A sessions both run as it, so both bill to the project. GitHub's terms allow machine accounts with a responsible human owner ([terms of service](https://raw.githubusercontent.com/github/docs/main/content/site-policy/github-terms/github-terms-of-service.md)).
- One factory GitHub App for everything that needs no user token: check runs, labels, marking PRs ready, enqueueing, resetting `integration`, ruleset audits and billing reads ([automate usage reporting](https://docs.github.com/en/billing/tutorials/automate-usage-reporting)).
- The human reviewers.

Neither machine accounts nor the App ever sit in a bypass list. In Lane A the driver pushes, not the model: deny `shell(git push)` and keep tokens in `--secret-env-vars`.

**GitHub Enterprise Cloud is required.** Merge queue on private repos needs it ([merge queue](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)), and so do usage report exports, cost centres and enterprise rulesets ([billing reports](https://docs.github.com/en/billing/reference/billing-reports); [cost centres](https://docs.github.com/en/enterprise-cloud@latest/billing/concepts/cost-centers)). The designation includes no GitHub Enterprise seats, so budget USD 21 per machine account a month unless the specialisation credit covers them.

## 8. Copilot's limits decide task size, identity and the gate

| Constraint | Source | Design response |
|---|---|---|
| Cloud agent sessions stop at 59 minutes. "This limit cannot be extended or bypassed." Setup and test runs count. | [Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github); [setup steps](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment) | Size Lane B tasks to 20 to 40 minutes. Cache dependencies and Playwright browsers in `copilot-setup-steps.yml`. On `timed_out`, re-dispatch once narrower, then park. Route anything bigger to Lane A. |
| One repo, branch and PR per task. Copilot ignores later issue comments. | [use cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github) | One issue per task, disjoint files, issue dependencies for order. Iterate on the PR. |
| The tasks and assignment APIs take only user-to-server tokens, and need a Business or Enterprise seat. | [agent tasks API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api); [OpenAPI](https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json) | A seated machine account per project. Credits go to "the user who triggered" them ([cost centre allocation](https://docs.github.com/en/billing/reference/cost-center-allocation)). GitHub does not state this for API-assigned sessions, so prove it in stage 0. |
| Workflows do not run on Copilot pushes until a writer clicks "Approve and run workflows". | [agent settings](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings) | Turn that off in factory repos, or nothing runs before morning. GitHub warns of exposed write access or secrets, so: gate logic only in required workflows, no secrets in PR jobs, `pull_request` not `pull_request_target`, minimal permissions, Actions policies ([Actions policies](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/about-actions-policies)). |
| On EMU with Entra Conditional Access, "Actions that use a personal access token will likely be blocked". | [CAP support](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/configuring-authentication-for-enterprise-managed-users/about-support-for-your-idps-conditional-access-policy) | Exempt the machine accounts, allow-list Actions ranges, or dispatch from a fixed Azure IP (our inference). A schedule also stops if its last cron editor is deprovisioned ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)). |
| When a ruleset blocks Copilot, the docs suggest adding Copilot as a bypass actor. | [bypass actors](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) | The trap. Fix the rule. Audit rulesets nightly and fail the kickoff if Copilot, the write role, the App or a machine account can bypass. |
| Copilot cannot mark PRs ready, approve or merge. The initiator cannot approve. Unattributed Copilot PRs need an extra approval. | [risks and mitigations](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations) | The App marks PRs ready; a human approves the morning PR. Keep Copilot code review approvals off for `main` ([code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review)). |
| Hooks, custom agents and setup steps load from the default branch at job start. | [use hooks](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks) | Guardrail, agent and rubric changes are daytime PRs behind CODEOWNERS. |
| Scripted dispatch cannot set the reasoning level. | [secondary] [write-up](https://ecorpit.com/copilot-cloud-agent-automations-reasoning-level-config-2026/); [changing the model](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/changing-the-ai-model) | Pin the model per agent. Use Lane A where effort matters. |
| No per-session cost API. Billing "generally cannot trace consumed credits to specific prompts, sessions, or exact features". | [monitor AI usage](https://docs.github.com/en/copilot/how-tos/manage-and-track-spending/monitor-ai-usage) | Lane B: estimate, then reconcile. Lane A: measure with OpenTelemetry (section 10). |
| No documented concurrency cap. A Copilot rate limit stalled all agent work for about an hour on 2 April 2026. | [agent management](https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/agent-management); [snippet] [incident](https://pingoru.io/providers/github/incidents/19872) | Start at four Lane B sessions and two Lane A builds per project. Budget one lost hour a night. |
| Cloud agent and MCP policies are off by default. | [enable cloud agent](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/add-copilot-cloud-agent) | Enable them only for repos with `factory=enabled`. |

### The ruleset stack

No single switch keeps agents off `main` and out of the tests. Four native layers do ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets); [about rulesets](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)):

1. **Branch ruleset `main-gate`**, bypass list empty. Restrict deletions. Block force pushes. Require linear history. Require a PR with 1 approval, stale approvals dismissed, code owner review, approval of the most recent push, conversation resolution, and the default-on extra approval for unattributed Copilot PRs. Required reviewers: `@acceptance-owners` on `tests/acceptance/**`. Strict status checks pinned to their source app. Code scanning results. Merge queue.
2. **Branch ruleset `integration-gate`** on `integration`. A PR with zero approvals, pinned checks (`gate/fast`, `gate/evaluator`) and a merge queue. Zero approvals also switches off the extra Copilot approval there. Leave force pushes allowed so the App can reset `integration` each evening without a bypass entry (our inference: test it).
3. **Push ruleset `protected-paths`**: `tests/acceptance/**`, `factory/**` (including frozen specs), `.github/workflows/**`, `.github/hooks/**`, `.github/agents/**`, `.github/skills/**`, `.github/copilot-instructions.md`, `.github/CODEOWNERS`. Bypass: `@acceptance-owners` and a platform team only. `handoff/**` stays writable.
4. **Organisation ruleset `factory-required-workflows`**, by custom property. "Require workflows to pass before merging", pointing at `factory-gates` pinned to a tag or SHA, with the acceptance and spec hash checks inside as a second lock.

Dry-run all four in Evaluate mode first. The docs do not say whether a push ruleset checks the queue's merge commit. Test that before relying on it.

## 9. A night is short workflows, a 20-minute tick and a few long Lane A jobs

### End to end

Times are Sydney local. In AEDT (UTC+11), 21:47 is 10:47 UTC and 05:41 next morning is 18:41 UTC on the same UTC date. In AEST the window is 11:47 to 19:41 UTC. Either way, **the whole night falls on one UTC date**. GitHub bills by UTC day ([billing reports](https://docs.github.com/en/billing/reference/billing-reports)), so a night-only machine account's daily rows are exactly one night.

| When (Sydney) | Step | Runs on | What happens |
|---|---|---|---|
| Day, by 17:00 | Plan locked | Human, PR | Specs pass the gate. Tests are merged. `factory/nights/<night_id>.json` lists each item's lane, agents, models, size, credit budget, pass and RESTART caps, in-flight caps and cutoffs. An acceptance owner approves it. |
| 21:47 | Kickoff | Actions `schedule`, `timezone: Australia/Sydney` | Preflight: gate script, bypass audit, budgets, PR auto-run, credit runway. The App resets `integration` to `main`. Mint `night_id`. |
| 21:50 | Lane A start | Actions job via OIDC | One ACA execution per build, with `PROJECT_ID`, `RUN_ID`, `NIGHT_ID`, `LANE=A`. Lane A goes first because it runs for hours. |
| 21:55 | Lane B first wave | One Actions job, writes in series | `POST /agents/repos/{owner}/{repo}/tasks` as the machine account, with `custom_agent: worker`, `model`, `base_ref: integration`. Store the task id against the `run_id`. Fill to the cap. |
| 22:00 to 04:45 | Lane A builds | ACA job | Generator session, frequent commits, spec re-sends. Fast checks on each stop, then an evaluator pass. NEEDS_WORK loops; RESTART resets within budget. No RESTART after 02:00, no new pass after 04:00. Ends with a PR, or a parked build. |
| 22:00 to 05:00 | Lane B sessions | Cloud agent | Cached setup, hook denials, `agentStop` fast checks, a draft PR. |
| On each push | Fast gate | Required workflow | Lint, typecheck, unit and acceptance tests, hash checks, hard-rule lints. |
| After the fast gate | Gate evaluator and review | Same workflow | A fresh evaluator re-grades every PR as a required check. Code review at Lite adds findings. |
| :13, :33, :53 | Tick | Actions `schedule` | Lane B: NEEDS_WORK gets one `@copilot` review, two rounds at most, batched with "Start a review" because each comment can start work ([best results](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results)). RESTART re-dispatches once. `timed_out` or `failed`: one narrower re-dispatch, else park. PASS: ready and enqueue. Lane A: enqueue passed PRs. No new dispatch after 04:00. |
| On enqueue | Serial integration | Merge queue | `merge_group` runs the full Playwright and held-out suites, concurrency 1. Ejected PRs re-dispatch (Lane B) or park (Lane A). |
| 05:41 | Morning package | Actions | Summary, Teams card, evidence to Blob, provisional ledger lines, Lane A rubric scores and restarts. |
| 06:00 | Trace review | Actions | `trace-reviewer` reads failed and parked runs and drafts PRs. |
| 07:30 to 09:00 | Human merge | Human | Sample evidence, read one failed trace in full, approve `integration` to `main`, log review minutes. |
| Day 3 | Reconcile | Azure Function | Pull GitHub AI usage, the Actions report and the Azure FOCUS export. Allocate variance. |

Three Actions details matter. Run the full suite only on `merge_group`, or minutes double. Make every dispatch and comment from one paced job, because the secondary limit is 80 content-creating requests a minute and 500 an hour ([rate limits](https://docs.github.com/en/enterprise-cloud@latest/rest/using-the-rest-api/rate-limits-for-the-rest-api)). List issues by label instead of using the search API.

### Why the orchestration stays short

- Hosted jobs stop at 6 hours ([Actions limits](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/limits)). `GITHUB_TOKEN` events start no new workflows except dispatch events ([GITHUB_TOKEN](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/security/github_token)). Polling jobs bill per minute; environment waits are free ([environments](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/deployments-and-environments)).
- `schedule` "can be delayed during periods of high loads" and "some queued jobs may be dropped" ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)). Practitioners report 15 to 30 minute delays [snippet] ([Crontap](https://crontap.com/blog/github-actions-cron-drift-problem)). Hosted runner assignment had multi-hour problems in February, May, August and October 2026 [snippet] ([February](https://github.blog/news-insights/company-news/github-availability-report-february-2026/); [May](https://github.blog/news-insights/company-news/github-availability-report-may-2026/); [August](https://blog.incidenthub.cloud/github-actions-pages-outage-aug-6-2026); [5 October](https://uptimerobot.com/is-it-down/github/2026-10-05/)). A stateless tick and a report that degrades gracefully shrug this off.

The long-running work lives in ACA, where each build is its own resumable execution (section 2).

### Where Container Apps and Durable Functions fit

ACA jobs run every Lane A build. Also use them for a measured Lane B session on fixed-price work, the Codex lane, or self-hosted runners. ACA runner jobs cannot run Docker inside the container ([runner tutorial](https://learn.microsoft.com/azure/container-apps/tutorial-ci-cd-runners-jobs)). Never move the cloud agent to self-hosted runners: its firewall must be off there ([setup steps](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment)). A job's start permission can expose its secrets, so restrict who can start factory jobs ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs)).

Add **Durable Functions** (isolated worker, Durable Task Scheduler Consumption) for a stateful wait such as a mid-run human approval, free on Consumption ([human interaction](https://learn.microsoft.com/azure/durable-task/common/durable-task-human-interaction)); exact start times; a budget shared across projects; or dispatch from a fixed Azure IP. Limits: 1 MB per payload; in-process support ends on 10 November 2026 ([external events](https://learn.microsoft.com/azure/durable-task/common/durable-task-external-events)). Do not use Codespaces (no free organisation quota, 12-hour life) or custom-container dynamic sessions (dedicated E16 instances, [ACA billing](https://learn.microsoft.com/azure/container-apps/billing#dynamic-sessions)).

### GitHub Models is gone

GitHub Models was retired on 30 July 2026 ([GitHub Models](https://docs.github.com/en/enterprise-cloud@latest/github-models); [snippet] [changelog](https://github.blog/changelog/2026-07-30-github-models-is-now-retired/)). For cheap steps like summarising the night, use Copilot CLI in Actions with `permissions: copilot-requests: write`. It meters to the organisation and ignores user budgets ([CLI in Actions](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/copilot-cli-in-github-actions)), so keep it for shared chores, or call a small Azure OpenAI model.

### Export evidence before it expires

- From 1 October 2026, retention also deletes checks, runs and statuses: 90 days by default, 1 to 400 for private repos ([retention](https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository); [snippet] [changelog](https://github.blog/changelog/2026-07-17-actions-retention-will-cover-checks-workflow-runs-and-statuses/)). Per-run timing endpoints are closing ([workflow runs](https://docs.github.com/en/enterprise-cloud@latest/rest/actions/workflow-runs)).
- Cloud agent logs have no REST endpoint and no stated retention. Pull them with `gh agent-task view --log` ([CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli)).
- The audit log keeps web events 180 days and Git events 7. Stream it to Blob or Event Hubs; agent session events can stream too, in preview for EMU ([audit log streaming](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise)).
- ACA keeps only the last 100 executions. Send job logs to Log Analytics ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs)).

So `night-report.yml` copies, per task: PR metadata, checks, review comments, the session log or transcript, the handoff files, Playwright traces and the ledger rows, to a Blob container per project. Keep a second copy as an Actions artifact at 400 days.

## 10. The ledger prices every run four ways and settles on day three

### Design principle

Engines report tokens at the client. Billing reports by day and identity, never by run, task or PR. So build the ledger from the client side and reconcile it down to each provider's billing grain ([billing reports](https://docs.github.com/en/billing/reference/billing-reports); [Agent SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)). Shape it like FOCUS, which carries list, contracted, effective and billed cost on every line ([What is FOCUS](https://learn.microsoft.com/cloud-computing/finops/focus/what-is-focus#benefits)). No FOCUS version has token columns, and neither GitHub nor Anthropic publishes a FOCUS export, so map those yourself ([FOCUS changelog](https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/working_draft/CHANGELOG.md)).

### What OpenTelemetry now measures

Lane A, the gate evaluator and the trace reviewer run on CLI or SDK. Their `invoke_agent` spans carry ([Copilot OpenTelemetry](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)):

- `github.copilot.nano_aiu`: AI units in nano units (1 AIU = 1e9 nano AIU).
- `gen_ai.usage.input_tokens`, `output_tokens`, `cache_read.input_tokens` and `cache_creation.input_tokens`.
- `gen_ai.agent.name` (the role), `gen_ai.conversation.id` (the session) and `gen_ai.request.model`.

So cost per agent role per task is measured on these runs. Three cautions:

- `github.copilot.cost` is a billing multiplier, "Not a monetary value". Never book it as money.
- The ledger maps `nano_aiu / 1e9` to AI credits. Confirm that against billing in stage 0.
- Subagents emit their own `invoke_agent` spans. Check in stage 0 whether a parent span includes them, so nothing is counted twice.

The Lane B cloud agent worker stays estimated. GitHub does not list the cloud agent as an OpenTelemetry client.

### Run identity

`run_id = {project}-{yyyymmdd}-{task}-{role}-{attempt}`, for example `p042-20261027-t017-generator-2`. It is deterministic, so retries and restarts are countable: a RESTART increments `attempt`. Role is metadata (the custom agent's name), not a separate seat.

| Stamp point | Lane B cloud agent | Lane A SDK sessions | Gate evaluator | Claude Code or Codex |
|---|---|---|---|---|
| Engine id kept | Task `id` from the POST | `gen_ai.conversation.id` | SDK `sessionId` | `session_id`; `thread_id` |
| Link to PR | Task `artifacts[]` | Branch name | Event PR number | Branch name |
| Branch | `copilot/...` | `factory/<project>/<night>/<task>-<role>-<attempt>` | n/a | As SDK |
| Commit and PR | Session log link; App comment with `Factory-Run-Id`; labels `night:`, `lane:`, `role:`, `engine:` | Trailer `Factory-Run-Id:`; same labels | Check run output | Trailer; same labels |
| Telemetry | None per session | OpenTelemetry with the resource attributes | Same | `OTEL_RESOURCE_ATTRIBUTES` ([Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage)) |
| Billing identity | Machine account | Machine account | Machine account | Anthropic workspace per project, key per role; Azure OpenAI resource per project |

Keep `run_id` out of metric labels. High-cardinality labels raise storage cost, and APIM's token metric drops data beyond 100 values per dimension ([llm-emit-token-metric](https://learn.microsoft.com/azure/api-management/llm-emit-token-metric-policy)). Put it on spans, events and logs. The PR is the hinge between cost and revenue, because acceptance, review time and rework hang off it.

### Measured versus estimated

| Engine or meter | Measured at run | Billing grain | Ledger status |
|---|---|---|---|
| Cloud agent (Lane B worker) | Tokens show only in the web session view | AI credits per user, model and UTC day, with input, output, cache read and write tokens | Estimated per run; measured per night, project and model |
| Copilot SDK and CLI (Lane A, gate evaluator, trace review) | OpenTelemetry spans; SDK `assistant.usage` and experimental `getMetrics.totalNanoAiu` ([SDK usage](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/usage-and-billing)) | As above | Measured per role per task, cross-checked |
| Copilot code review | Minutes under `dynamic/agents/copilot-pull-request-reviewer` | Credits go to the PR's human co-author, else the organisation; model not disclosed ([models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)) | Estimated |
| Claude Code | `total_cost_usd`, `modelUsage`, `costBasis` | Anthropic Cost API, daily by workspace ([Usage and Cost API](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)) | Measured, reconciled |
| Codex CLI | Tokens per turn, no cost field [snippet] ([JSONL reference](https://codex.danielvaughan.com/2026/04/08/codex-exec-jsonl-reference/)) | Azure meter per resource per day | Tokens measured, priced from `dim_price` |
| Actions minutes; ACA compute | Job times × runner rate; execution time × vCPU and GiB | Detailed report by repo, user, `workflow_path`; FOCUS per tag ([exports](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-improved-exports)) | Measured |
| Telemetry, storage, seats, fee, platform, human time | n/a, or captured per PR | FOCUS, invoice, timesheet | Allocated, or measured for human time |

### Schema

Store USD and an AUD conversion on every money line. V2 adds `lane`, more roles, per-role usage with `nano_aiu`, Lane A outcome columns, and `fact_eval` for calibration.

```sql
create table dim_project (
  project_id text primary key, mode text check (mode in ('internal','client')),
  client text, contract_type text,        -- fixed | tm | subscription | outcome
  github_cost_centre_id text, machine_account text,
  azure_subscription_id text, azure_resource_group text,
  anthropic_workspace_id text, funding_source text  -- spd_credits | cash
);

create table dim_price (                  -- nightly snapshot from SDK models.list and rate tables
  engine text, model text, effective_from date,
  input_per_mtok numeric, cached_per_mtok numeric,
  cache_write_per_mtok numeric, output_per_mtok numeric, source_url text,
  primary key (engine, model, effective_from)
);

create table fact_run (
  run_id text primary key, project_id text, night_id date, night_utc_date date,
  task_id text, feature_id text, lane text check (lane in ('A','B')),
  agent_role text,    -- planner | grill | test_author | generator | worker | evaluator
                      -- | gate_evaluator | reviewer | trace_reviewer | ops
  engine text,        -- copilot-cloud-agent | copilot-sdk | copilot-cli | copilot-review | claude-code | codex-cli
  model text, engine_session_id text, agent_version text,  -- custom agent commit SHA
  pr_number int, head_sha text, started_utc timestamptz, ended_utc timestamptz,
  exit_status text,   -- completed | timed_out | failed | budget_hit | cancelled | restarted | parked
  resumed_count int, round_no int, budget_cap_credits numeric,
  runner_minutes numeric, vcpu_s numeric, gib_s numeric
);

create table fact_usage (
  run_id text, model text, agent_role text,
  input_tok bigint, cached_tok bigint, cache_write_tok bigint, output_tok bigint,
  nano_aiu bigint,      -- summed over invoke_agent spans
  ai_credits numeric,   -- nano_aiu / 1e9, once stage 0 confirms it
  measure_source text,  -- otel_span | engine_reported | billing_allocated | profile_estimate
  primary key (run_id, model)
);

create table fact_cost_line (             -- FOCUS-shaped
  line_id bigserial primary key, charge_date_utc date, project_id text,
  night_id date, lane text, run_id text null,   -- null for shared and fixed costs
  provider text,      -- GitHub | Microsoft | Anthropic | OpenAI | Internal
  category text,      -- ai_tokens | review_agent | ci_minutes | azure_compute | telemetry
                      -- | storage | seats | program_fee | platform | human
  sku_or_meter text, quantity numeric, unit text,
  list_cost numeric, contracted_cost numeric, effective_cost numeric, cash_cost numeric,
  credit_applied numeric,                 -- effective_cost minus cash_cost
  currency text default 'USD', fx_to_aud numeric,
  allocation_method text, -- direct | tokens_share | runtime_share | residual_pro_rata | per_night
  status text             -- provisional | reconciled | final
);

create table fact_human_time (
  project_id text, night_id date, task_id text, pr_number int, person text,
  activity text,  -- spec | triage | review | rework | merge | calibration | trace_read | client_demo
  minutes numeric, loaded_rate_aud numeric
);

create table fact_outcome (
  task_id text, feature_id text, pr_number int, lane text,
  outcome text,   -- merged_first_pass | merged_after_rework | merged_after_restart
                  -- | rejected | abandoned | reverted_30d
  review_rounds int, evaluator_passes int, restart_count int,
  contract_criteria_count int,            -- locked tests plus contract.md additions
  rubric_score_start numeric, rubric_score_end numeric,  -- weighted, first and last pass
  high_findings int, merged_at timestamptz, accepted_by_client_at timestamptz
);

create table fact_eval (                  -- one row per evaluator pass
  run_id text, task_id text, pass_no int, lane text,
  evaluator_version text,                 -- commit SHA of evaluator agent and rubric skills
  model text, verdict text,               -- pass | needs_work | restart
  scores jsonb,                           -- design, originality, craft, functionality, api, code
  criteria_total int, criteria_failed int,
  human_verdict text null, human_scores jsonb null, graded_by text null
);

create table fact_reconciliation (
  provider text,
  grain_key text,   -- GitHub: utc_date|login|model; Azure: utc_date|tag|meter; Anthropic: utc_date|workspace|model
  ledger_sum numeric, measured_sum numeric, provider_sum numeric,
  variance numeric, explained_by text, closed_at timestamptz
);
```

### The four prices, and the shadow price

| Column | Meaning | Examples |
|---|---|---|
| `list_cost` | Published rate, no discounts. **The shadow price.** | AI credits at USD 0.01; tokens at the rate table; Azure at retail (FOCUS `ListCost`); seats at list; Actions minutes at USD 0.006 even when included |
| `contracted_cost` | After negotiated or program discounts | Copilot's 10% Auto model discount ([Auto discount](https://raw.githubusercontent.com/github/docs/main/data/reusables/copilot/auto-model-discount.md)); an Azure private offer |
| `effective_cost` | After included allowances and commitments | Included minutes and Copilot credits |
| `cash_cost` | What Get AI pays after partner credits | Zero for credit-funded Mode A lines |

Two rules keep the numbers honest:

- **Treat each Copilot seat as a prepayment of its credits.** An Enterprise seat costs USD 39 and includes 3,900 credits, exactly USD 39 at USD 0.01. Business is USD 19 for 1,900 ([plan variables](https://raw.githubusercontent.com/github/docs/main/data/variables/copilot.yml)). Post every credit used at USD 0.01, and post unused included credits as month-end "breakage". Never count both the seat fee and its credits.
- **Book partner credits as a funding line, never as a lower cost.** Cost Analysis does not show credits; only the invoice does, as "Azure credits applied" ([reporting](https://learn.microsoft.com/azure/cost-management-billing/costs/reporting-get-started#invoices-and-credits)). So the matrix shows margin twice: at list and at cash.

### Cadence: provisional tonight, reconciled on day three

- **Nightly (05:41).** Provisional lines. OpenTelemetry-measured runs and Claude Code use measured values. Cloud agent and code review use a size-class estimate calibrated from reconciled nights. Azure compute is runtime × list rate.
- **Day 3.** GitHub publishes no billing lag. Copilot metrics land within two full UTC days ([metrics](https://docs.github.com/en/copilot/concepts/billing-and-usage/copilot-usage-metrics/copilot-metrics)), and Azure tags take up to 24 hours ([tags](https://learn.microsoft.com/azure/cost-management-billing/costs/understand-cost-mgt-data#how-tags-are-used-in-cost-and-usage-data)). For each `(UTC date, machine account, model)`:
  1. Pull `provider_sum` from the AI credit usage endpoint or `ai_credit` export ([billing usage](https://docs.github.com/en/billing/tutorials/automate-usage-reporting)).
  2. Subtract `measured_sum`, the OpenTelemetry-measured runs.
  3. Allocate the residual to estimated runs pro rata. Mark them `reconciled`.
  4. A negative residual flags measurement drift. GitHub says `totalNanoAiu / 1e9` matches credits only "as a convenience" ([SDK usage](https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-sdk/features/usage-and-billing.md)).
  Do the same for Actions (per repo and `workflow_path`) and Azure (per tag and meter).
- **Month close.** Compare with the GitHub-on-Azure invoice, including "Azure credits applied". Azure re-rates until the invoice closes and adds late usage up to 72 hours after month end ([exports](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-improved-exports)). Mark lines `final`.

V1's trick of a different evaluator model to split billing rows is no longer needed: the evaluator is measured in both lanes. Keep it on the model its rubric was calibrated on.

## 11. Yield and review minutes set the margin, in both lanes

### Two units, reported apart

- **Lane B: cost per accepted task** = (cost per attempt × attempts + human cost) ÷ yield.
- **Lane A: cost per accepted build** = (cost per build × attempts + human cost) ÷ yield. A RESTART counts towards attempts.

Never average them. A build is a feature or an app; a task is an issue.

Fully loaded cost, at list with cash alongside, covers: AI credits for every run that touched the work, including restarts and retries; code review; CI and agent minutes; Azure compute, storage and telemetry; seats, breakage and the fee; amortised platform hours; human minutes at a loaded rate, including calibration and trace reading; rejected work spread over accepted work; and a warranty reserve for fixed price. This follows Microsoft's FinOps guidance: unit economics are "a derivative of activity-based costing" and include "manual processes and steps outside of the cloud" ([unit economics](https://learn.microsoft.com/cloud-computing/finops/framework/quantify/unit-economics)).

### Worked examples (model)

Assume a loaded human rate of USD 100 an hour. Replace it with Get AI's real rate in AUD.

**Lane B.** An attempt costs USD 5, of which USD 3.50 is tokens.

| Scenario | Attempts | Human minutes | Yield | Cost per accepted task |
|---|---|---|---|---|
| B1: good night | 1.3 | 40 | 80% | (5 × 1.3 + 66.67) ÷ 0.8 = **USD 91** |
| B2: poor night | 1.6 | 60 | 50% | (5 × 1.6 + 100) ÷ 0.5 = **USD 216** |
| B3: B1, token price halved | 1.3 | 40 | 80% | (3.25 × 1.3 + 66.67) ÷ 0.8 = **USD 89** |

Halving the token price saves about 3%. Moving from B2 to B1 saves about 58%.

**Lane A.** A build costs USD 155: USD 150 in AI credits plus about USD 5 of compute and traces (section 12). One build in five restarts, so 1.2 attempts. Human time covers spec approval and morning review.

| Scenario | Cost per attempt | Attempts | Human minutes | Yield | Cost per accepted build |
|---|---|---|---|---|---|
| A1: base | 155 | 1.2 | 90 | 70% | (155 × 1.2 + 150) ÷ 0.7 = **USD 480** |
| A2: better evaluator, faster review | 155 | 1.2 | 60 | 90% | (186 + 100) ÷ 0.9 = **USD 318** |
| A3: A1, token price halved | 80 | 1.2 | 90 | 70% | (96 + 150) ÷ 0.7 = **USD 351** |

On Lane A tokens are about half the cost, so model choice matters more: halving the token price saves about 27%. Better yield and faster review still save more, about 34%. Lane A PRs are large, so review them by evidence, rubric scores and `rubric-code`, not line by line.

The public data agrees. AI PRs merge within 30 days 32.7% of the time against 84.4% for unassisted PRs, and agent PRs wait 17.6 hours for review against 3.4 [snippet] ([LinearB](https://linearb.io/library/engineering-benchmarks-and-research)). Review time rose about 91% on high-adoption teams [secondary] ([Faros summary](https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery)). One feature cost USD 7 to 70 to merge across a dozen models, and the harness alone moved cost about 2.5x [snippet] ([Insight APAC](https://blog.insight-services-apac.dev/2026/07/06/cost-to-a-merged-feature)).

### The matrix

The fact grain is one row per project, night, lane, engine, model and role, rolling up to feature and month.

- **View 1: P&L per accepted build and per accepted task**, on separate pages. Runs, passes, rounds, restarts, outcome; AI credits at list by role, review agent, minutes, Azure, telemetry; seat, fee, platform, human, yield and warranty allocations; **fully loaded at list**, at cash, and the credit subsidy; revenue; **margin at list** and at cash.
- **View 2: engine bake-off.** Per lane, engine, model and harness setting: n, first-pass rate, acceptance, rounds or passes, list cost per accepted unit at P50 and P80, human minutes, timeout rate, 30-day escaped defects.
- **View 3: night control chart.** Per night: dispatched and accepted per lane, cost per accepted unit at P50, review minutes, burn against the envelope, incidents.
- **View 4: role cube.** Cost share by role, now measured on Lane A. Anthropic's DAW build spent about 91% on the builder, 8% on QA and under 0.5% on the planner ([Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
- **View 5: credit runway.** Remaining credits ÷ list burn per night, with expiry dates.
- **View 6: evaluator health.** Agreement by week and `evaluator_version`, rubric score delta, verdict mix.

### Leading indicators

Alert levels are starting assumptions to tune.

| Indicator | Alert |
|---|---|
| First-pass integration rate | Below 60%, the low end of the earlier report's prior |
| Rounds per Lane B task | Above 1.5 |
| Timeout rate against the 59-minute cap | Above 15% (tasks belong in Lane A) |
| Evaluator-human agreement | Below 80% |
| Rubric score delta per build (last pass minus first) | Near zero: the passes are not helping |
| Restarts per build | Above 0.3 |
| Acceptance criteria per Lane A spec | Near the floor of 20 |
| Cost per accepted unit at P50 and P80, by lane and engine | Control chart breach |

Also track eventual acceptance, review and rework minutes per PR, PR size, evaluator false-reject rate, budget hits, cache read share, 30-day reverts and credit runway.

Copilot priors for Lane B: GitHub's `gh-aw` repo merged 76.3% of 1,000 Copilot PRs, then 80.0% of 1,110; fixes at 81.0%, chores at 58.6% ([23 July report](https://github.com/github/gh-aw/discussions/47549); [5 August report](https://github.com/github/gh-aw/discussions/50534)). Academic data shows documentation at 84%, CI 79%, bug fixes 64%, performance 55% [snippet] ([MSR 2026](https://arxiv.org/abs/2601.15195)). One study found 15.4% of merged agent PRs needed reviewer intervention [snippet] ([arXiv 2605.22534](https://arxiv.org/pdf/2605.22534)). Lane A has no public prior beyond Anthropic's own runs.

### Comparing engines and nights fairly

- **Engines.** Replay one regression set (20 to 50 tasks and a few small build specs from your own failures) on each engine and model with the same gate. Compare list cost and human minutes per accepted unit. Always show n. Use pass^k when consistency matters.
- **Nights.** Compare within a lane and size class. Annotate model releases, harness changes and evaluator versions, because any one can move cost 2.5x.

### Pricing from the matrix

- Fixed-price floor = P80 fully loaded list cost ÷ (1 minus target gross margin). P80, because the spread is wide.
- Match the commercial model to scope certainty. Specified items with test oracles suit a fixed price per accepted task or build. Discovery suits a pod day rate. Maintenance suits a monthly capacity subscription. Outcome fees suit only outcomes the client can measure. Forrester says one construct across a portfolio "will misprice most of it" [snippet] ([Forrester](https://www.forrester.com/blogs/for-service-providers-ai-giveth-and-ai-taketh-away/)).
- If margin at list is below target, the project is profitable only through subsidy. Do not renew on those terms.

## 12. What the credits buy: about seven builds or 26 light nights a month

Everything here is a model. Calibrate Lane B in stage 2 and Lane A in stage 4.

### Credit pools

| Pool | Arithmetic | Per month |
|---|---|---|
| Azure bulk credits | 10,000 ÷ 12 | USD 833 |
| Copilot Enterprise via Azure | 5,000 ÷ 12 | USD 417 |
| **Total, one designation** | | **USD 1,250** |
| Each Azure specialisation adds | (12,000 + 4,680 + 2,520) ÷ 12 | USD 1,600 (GitHub parts earmarked) |

The Copilot benefit buys 41,700 credits a month (417 ÷ 0.01), whether it pays seats or overage. Included pools reset at 00:00 UTC on the 1st, with no carry-over. The promotional 7,000-credit allowance ended on 1 September 2026 ([organisation billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing); [snippet] [promotion](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises)).

### Lane B: one session, at Copilot list rates

A **light** session reads 1.5M input tokens with 80% cache hits and writes 30K output. A **heavy** 40-minute session reads 6.7M cached and 0.67M uncached tokens and writes 0.2M. Cache-write charges are excluded.

| Model (USD per 1M: input / cached / output) | Light | Heavy |
|---|---|---|
| GPT-6 Luna (0.10 / 0.01 / 0.50) | USD 0.06 | USD 0.23 |
| Claude Sonnet 5.5 or GPT-6.1 Sol (2.00 / 0.10 / 10.00) | USD 1.02 | USD 4.00 |
| GPT-5.3-Codex (1.75 / 0.175 / 14.00) | USD 1.16 | USD 5.13 |
| Claude Opus 5.5 (4.00 / 0.20 / 20.00) | USD 2.04 | USD 8.00 |

Rates from GitHub's [rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml). Light Sonnet: 1.2M × 0.10 + 0.3M × 2 + 0.03M × 10 = USD 1.02.

Default mix per task: worker 80% on Sonnet 5.5 or GPT-6.1 Sol and 20% on Opus 5.5 (USD 1.22 light, USD 4.80 heavy per session); 1.3 sessions per task, because about 30% need one `@copilot` round; gate evaluator at 25% of a Sonnet session per round; Copilot code review at Lite at USD 0.25 or USD 1.00 per round (Lite runs USD 0.05 to 1, Balanced USD 0.25 to 5: [code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review)); chores on Luna at USD 0.02.

| | Light | Heavy |
|---|---|---|
| Worker | 1.22 × 1.3 = 1.59 | 4.80 × 1.3 = 6.24 |
| Evaluator | 0.255 × 1.3 = 0.33 | 1.00 × 1.3 = 1.30 |
| Code review | 0.25 × 1.3 = 0.33 | 1.00 × 1.3 = 1.30 |
| Chores | 0.02 | 0.02 |
| **Per task** | **USD 2.26** (226 credits) | **USD 8.86** (886 credits) |
| **Per night, 20 tasks** | **USD 45** | **USD 177** |
| **Per month, 20 nights** | **USD 905** | **USD 3,544** |

Totals use unrounded figures. Each RESTART adds about one fresh attempt.

### Lane A: one build

Anthropic published two measured runs. Anthropic lists Opus 4.5 and 4.6 at USD 5 input, 0.50 cache hit and 25 output per million tokens ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)). Copilot bills Claude at GitHub's table rates. Per million (input / cached / cache write / output): Opus 5.5 is USD 4.00 / 0.20 / 5.00 / 20.00; Sonnet 5.5 is USD 2.00 / 0.10 / 2.50 / 10.00 ([rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml)). Claude 4.7 and later produce about 30% more tokens for the same text.

| Line | Arithmetic | USD at list |
|---|---|---|
| DAW build, simplified harness, Opus 4.6, 3 h 50 min ([Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)) | Measured | 124.70 |
| Same work on Opus 5.5 via Copilot | 124.70 × 0.8 (price) × 1.3 (tokens) | about 130 |
| Same work on Sonnet 5.5 via Copilot | 124.70 × 0.4 × 1.3 | about 65 |
| Retro game maker, full harness, Opus 4.5, about six hours | Measured | about 200 |
| Same work on Opus 5.5 | 200 × 0.8 × 1.3 | about 210 |
| **Planning range per build** | | **100 to 200 (10,000 to 20,000 credits); midpoint 150** |
| Compute and traces per build | 4 vCPU × 21,600 s × 0.000024 + 8 GiB × 21,600 s × 0.000003 + 1 GB × 2.30 | about 5 |

Notes:

- Cache hits are cheaper on the 5.5 models (USD 0.20 against 0.50), so the Opus lines are a ceiling. The Sonnet line is a floor: Sonnet may need more passes. The builder took about 91% of the DAW cost, so a RESTART can add up to a full build.
- Compute is about USD 0.20 per worker-hour at 2 vCPU and 4 GiB, on unverified US list rates. GitHub bills its own ACA-based cloud sandbox at the same per-second rates ([sandboxes](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/about-cloud-and-local-sandboxes)). App plus headless browser plus CLI probably needs 4 vCPU and 8 GiB: about USD 0.43 an hour.
- Traces: assume up to 1 GB per build at about USD 2.30 per GB [snippet] ([groundcover](https://www.groundcover.com/guides/reduce-log-ingestion-costs)). Measure in stage 0.

### Other monthly lines for one project

- **Actions minutes.** About 1,500 to 1,900 a Lane B night, so 30,000 to 38,000 for 20 nights. That fits Enterprise's 50,000 included minutes only if nothing else uses them ([included usage](https://docs.github.com/en/billing/reference/product-usage-included)). Shadow value at USD 0.006: USD 180 to 228 ([runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)). Larger runners never use included minutes. Lane A uses few minutes: the gate and the queue.
- **Azure base.** About USD 50 a month (assumption): Functions, Durable Task Scheduler, storage, Key Vault, Azure Files, logs, and a Burstable PostgreSQL server whose price was not retrieved.
- **Machine account GitHub Enterprise seat.** USD 21, funding unclear (section 6).
- **Designation fee.** USD 406 a month (4,875 ÷ 12), always cash.

### How far the credits go

| Scenario | AI credits at list | Other Azure-billable | Total | Cash spill against 1,250 |
|---|---|---|---|---|
| B: 1 project, 20 light nights | 905 | 50 | 955 | 0 (295 headroom) |
| B: 1 project, 20 heavy nights | 3,544 | 50 | 3,594 | **2,344** |
| B: 3 projects, 20 light nights | 2,715 | 70 + 244 Actions overage | 3,029 | **1,779** |
| A: 7 builds at USD 150 | 1,050 | 50 + 7 × 5 = 85 | 1,135 | 0 (115 headroom) |
| A: 7 builds at USD 200 | 1,400 | 85 | 1,485 | **235** |
| Mix: 4 builds + 12 light nights | 600 + 12 × 45.25 = 1,143 | 50 + 4 × 5 = 70 | 1,213 | 0 (37 headroom) |
| B: 20 light nights, if general credits cannot pay GitHub meters | 905 | 50 | 955 | **488** (only 417 covers Copilot) |
| A: if general credits cannot pay GitHub meters | 417 covers 2 builds | Azure credits cover compute | | 0, but 2 builds a month |

Three projects use about 90,600 Actions minutes, so 40,600 run over the included 50,000. Net of the USD 50 base, the credits fund about **26 light or 7 heavy Lane B project-nights** (1,200 ÷ 45 and 1,200 ÷ 177), **about 7 Lane A builds** (1,200 ÷ 155; 6 to 11 across the range), or a mix such as **4 builds and 12 light nights**. Seats and the fee sit outside these totals.

Settings that stop silent spill:

- Overage is USD 0.01 a credit and paid usage is on by default. Turn off "AI credits paid usage", or set budgets ([organisation billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing)). "There is no automatic fallback to lower-cost models", so the dispatcher switches models itself.
- User-level budgets hard-stop, checked before the pool ([budgets](https://docs.github.com/en/billing/how-tos/set-up-budgets)). A hard stop can halt a Lane A build mid-pass, so the dispatcher and driver stop before the budget does. Set each session's `sessionLimits.maxAiCredits` with margin for one overshooting response.
- Set code review to Lite. Balanced on every PR can cost more than the workers.
- Azure billing offers no prepaid usage, and credits cannot buy GitHub Pre-Purchase plans ([payment methods](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/supported-payment-methods); [Pre-Purchase plan](https://learn.microsoft.com/azure/cost-management-billing/reservations/github-pre-purchase)). Pooled developer credits may subsidise a night, but the ledger charges it at list.

## 13. Claude Code and Codex stay as secondary lanes on the same ledger

Copilot is the engine. Other engines earn a lane, mostly for bake-offs.

| Lane | Runs on, billed to | When it is worth it | Ledger |
|---|---|---|---|
| Codex CLI on Azure OpenAI | ACA job, Australia East; Azure credits (first-party meter) | The only long-running CLI agent wholly on general Azure credits. A Lane A build when the Copilot pool is spent but Azure credits remain, and bake-offs. API key only; Responses API; validated with gpt-6-astra, gpt-6-sol and gpt-6-luna ([Codex with Azure OpenAI](https://learn.microsoft.com/azure/foundry/openai/how-to/codex)). Re-run the regression set first. | `codex-cli`; tokens from `turn.completed.usage` [snippet], priced from `dim_price` |
| Claude Code on the Anthropic API | ACA job; Anthropic at cash | Tests the two primitives Copilot lacks: auto mode and a judged `/goal`. The rubric skills carry over via `.claude/skills`. Or a client mandates Anthropic direct. | `claude-code`; `total_cost_usd`, `modelUsage`, OpenTelemetry; daily Cost API reconciliation ([Usage and Cost API](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)) |
| Claude Code on Microsoft Foundry | ACA job in East US 2 or Sweden Central; Marketplace at cash | Only when a client mandates Claude on its own Azure contract. Pin deployments, or `opus` falls back to Opus 4.6 ([Claude Code on Foundry](https://code.claude.com/docs/en/microsoft-foundry)). | As above, monthly against one CCU line ([CCU billing](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-billing)) |
| Agent HQ third-party agents (Claude, Codex) | Inside GitHub, cloud agent sandbox; AI credits plus minutes | Lane B bake-off on low-risk tasks. Public preview, no steering, short model lists: the Claude agent lacks Sonnet 5.5 and Opus 5.5 ([third-party agents](https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-third-party-coding-agents)). Hook and custom agent support is not documented. | As the cloud agent |
| GitHub Agentic Workflows with a Claude or Codex engine | Actions; the provider at your keys | Maintenance agents with read-only tokens and declared `safe-outputs` ([agentic workflows](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows)) | `gh-aw-<engine>` |

Every lane opens PRs through the same rulesets and required workflows, and pushes as the App or the machine account, neither of which can bypass. That is why Agent HQ agents are safe to trial before hook support is confirmed: GitHub enforces the gate, not the agent.

## 14. Build it in eight stages, money first

Each stage has an exit test. Do not start the next until it passes.

| Stage | Build | Exit test | Effort |
|---|---|---|---|
| 0. Prove the money, the identity and the long session | Send the credit question. Credited (Mode A) and cash (Mode B) billing profiles. Connect the credited subscription to a test cost centre ([connect Azure](https://docs.github.com/en/billing/how-tos/set-up-payment/connect-azure-sub)). One seated machine account; one task via the tasks API; CI on for Copilot PRs; EMU check; budgets. One ACA job running an SDK session with explicit `replicaTimeout`, Azure Files state and OpenTelemetry. | A written answer on file. The task's credits sit on the machine account. The invoice shows "Azure credits applied" on GitHub lines. CI ran unattended on a draft PR. The job runs well past 1,800 seconds (target 7.5 hours). A killed replica resumes by id and finishes. Summed `nano_aiu ÷ 1e9` matches the AI usage report within tolerance. Redaction covers traces. | 3 to 4 days of work; 1 to 3 weeks elapsed for the invoice |
| 1. Gate, locks, rubrics and spec rules | `factory-gates` required workflow with hash checks. The four rulesets, Evaluate mode first. CODEOWNERS. All custom agents. Hook deny rules. Cached setup steps. Gate script with the spec rules. Rubric skills v1. `contract.md` and handoff templates. | A seeded agent edit to `tests/acceptance/` or `.github/skills/` is rejected, and the hash check catches it in Evaluate mode. The gate script blocks an open clarification marker and a 12-criteria Lane A spec. Rubric skills load in the CLI and cloud agent. The audit flags a test bypass entry. | 2 to 3 weeks |
| 2. Lane B: one project, one night, Actions only | Kickoff, dispatch, tick and report. Night plan schema with lanes. Morning package. Ledger v0: `fact_run`, provisional estimates, evidence export. | Three nights produce draft PRs and a morning card with nobody awake. Timeout rate and credits per task known from reconciled rows. | 1 to 2 weeks |
| 3. Independent verification and calibration | Gate evaluator (SDK, Playwright, rubric skills, three verdicts, OpenTelemetry) as a required check. RESTART on Lane B. Code review at Lite. The `@copilot` loop. Held-out suite. `trace-reviewer`. Weekly calibration and `fact_eval`. A first trace view. | The evaluator catches a seeded defect that passes the acceptance tests. A seeded RESTART closes and re-dispatches cleanly. 10 verdicts human-graded, agreement recorded. One trace-review PR merged. | 2 weeks |
| 4. Lane A | The SDK driver in ACA: generator and evaluator sessions, 2 to 3 passes, RESTART, spec re-send, handoff files, resumable state, OpenTelemetry per role into the ledger. A dynamic workflows trial of the same loop, with the driver as fallback. | One greenfield build from an approved spec runs unattended overnight and merges through the gate. Score delta and passes recorded. A forced RESTART completes within budget. A small reference spec run about 10 times, every failure read. Measured cost per role matches billing within tolerance. The dynamic workflow matches the driver's verdict flow, or is parked until GA. | 2 to 3 weeks |
| 5. Parallel work, serial integration, full ledger | In-flight caps of 4 to 6 Lane B tasks and 1 to 2 Lane A builds. Disjoint-file check. Merge queue. App marks ready and enqueues. Morning promotion PR. Day-3 reconciliation. Power BI matrix v1. | A night with at least 15 Lane B tasks and one Lane A build, conflicts resolved. Reconciliation variance under 10% per grain key (assumed tolerance). The matrix shows cost per accepted build and per accepted task, separately, at list and cash. | 2 weeks |
| 6. Second project and secondary engines | Second machine account, cost centre and resource group. Durable Functions only if a section 9 trigger applies. Codex and Claude Code lanes. | Two projects in one night with clean per-project rows. A 20-task bake-off on two engines, plus one build spec each. | 2 to 3 weeks |
| 7. Keep healthy, review the register, package | Regression set with pass^k. Maintenance automations. Register reviews after Universe and each model release: remove one component, measure, keep or restore. Package the accelerator (section 16). | 30 days of escaped-defect data. Human minutes per accepted unit falling. Agreement at target for four weeks. At least one thin-glue item deleted or confirmed. The accelerator deploys into a clean tenant in one day. | Ongoing |

Start stage 0 now. A month's charges reach the Azure invoice at the start of the next month ([Copilot Azure billing](https://docs.github.com/en/copilot/reference/copilot-billing/azure-billing)), so the invoice test cannot be rushed. Universe lands during stage 0, so run the first register review then.

## 15. The risks, most serious first

| # | Risk | Why it matters | Mitigation |
|---|---|---|---|
| 1 | Credits may not fund client delivery | "Internal-use-rights credits" ([credits FAQ](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud#azure-credits-faqs-legacy-experience)) | Written ruling; two modes; price at list |
| 2 | Evaluator generosity drift | "Done" rests on the evaluator, and Claude starts as a generous QA agent [talk 32:40 to 34:08]. Drift is silent | Weekly calibration; agreement alert; held-out suite; evaluator changes by PR, re-run on the graded set |
| 3 | Credit mechanics fail | Unsupported subscription types; seats possibly not covered ([payment methods](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/supported-payment-methods)) | Stage 0 invoice test |
| 4 | Captured traces contain client code or secrets | Content capture stores full prompts and tool data ([Copilot OpenTelemetry](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)) | Short retention; RBAC; a resource per client; capture off unless allowed; redaction tested |
| 5 | Auto-run workflows on Copilot PRs | GitHub's own warning ([agent settings](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings)) | Required workflows only; no secrets on PR jobs; Actions policies |
| 6 | Bypass list drift | One Copilot bypass on `main` undoes the gate | Nightly audit fails the kickoff |
| 7 | An over-specified spec cascades errors | Early technical mistakes magnify over hours [talk 24:12 to 24:46] | Technical design only for hard constraints; design-leak warning |
| 8 | Container Apps interrupts or caps long builds | Maintenance interruptions; no documented maximum timeout; 1,800-second AVM default ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs#advanced-job-configuration)) | Explicit timeout; retry at least 1; resumable sessions; stage 0 test |
| 9 | Silent overage or a mid-night hard stop | Paid usage on by default; budgets hard-stop; Lane A spends in big blocks | Envelopes below budget; Lite review; model switching |
| 10 | Cost lands on the wrong identity | Unstated for API-assigned sessions and code review | Stage 0 test; nightly check for human logins |
| 11 | Preview features change | Tasks API, assignment API, session limits, third-party agents, the Copilot approval rule; `getMetrics` experimental | Nightly canary; assignment as fallback; register review after Universe |
| 12 | Dynamic workflows change or stall in preview | Preview; CLI needs `--experimental`; prompts hidden in `workflow run` ([dynamic workflows](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-dynamic-workflows)) | Driver stays default until GA; grant permissions up front |
| 13 | GPT models need re-ablation | Simplified harness validated on Claude [talk 53:14] | Regression set before removing any scaffolding |
| 14 | Cloud agent subagent ambiguity | Docs conflict ([cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)) | No dependence on Lane B; subagents on Lane A only |
| 15 | Firewall gaps | Ignores MCP servers and setup steps ([firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall)) | Push ruleset on `.github/**`; few MCP servers; VNet egress on Lane A |
| 16 | Platform incidents and schedule drift | Late schedules, runner incidents, rate-limit stalls | Idempotent tick; a lost hour budgeted; graceful report |
| 17 | Evidence loss | Retention deletes checks and runs; logs have no API | Nightly export; audit stream |
| 18 | Client data rules | Copilot inference location not established | Check per client; Azure OpenAI in Australia East where needed |
| 19 | Claude in Foundry traps | Cash only, US or Sweden, 40 RPM ([Claude quotas](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-quotas-limits)) | Claude through Copilot in Mode A |
| 20 | Quality decay in agent-built code | Earlier warnings apply, more so for large Lane A PRs | Morning review; `rubric-code`; 30-day defect tracking |
| 21 | Credits expire or are revoked | Expiry moves to the purchase date from 1 November 2026 ([August announcements](https://learn.microsoft.com/partner-center/announcements/2026-august)) | Steady burn; runway view |
| 22 | Price and FX drift | Prices change; costs USD, prices AUD | Nightly `dim_price` snapshot; FX column; fixed-price buffer |

## 16. The factory and its ledger become the deployment accelerator

These become IP:

- **The `factory-gates` template.** Required workflows, ruleset JSON, hooks, custom agents, setup steps and the night plan schema. A client repo adopts it by setting one custom property.
- **The Azure side as Bicep or azd.** ACA jobs, the Lane A driver, the ledger Function, storage, Application Insights, Key Vault and OIDC.
- **The ledger.** Schema, reconciliation and the Power BI matrix. This turns the factory into a pricing tool.
- **The grill gate.** `planner`, `grill` and `test-author`, the spec template and the gate script.
- **Rubric skills with calibration examples.** Anthropic designed its evaluator tuning to be reusable across projects, and found good-design and AI-slop examples "generalize quite well" [talk 40:35 to 41:21]. One calibrated set serves many clients, with per-client weights.
- **The evaluator prompts and the calibration set.** Human-graded verdicts are hard to copy and improve every week.
- **The trace-review agent**, which turns trace reading into a morning routine.
- **A trace view for Copilot agents** in Application Insights or Azure Managed Grafana, starting from Microsoft's guide ([Monitor AI coding agents with Grafana](https://learn.microsoft.com/en-gb/azure/managed-grafana/grafana-opentelemetry-app-insights)). Observability for ultra-long agents is "not fully solved yet" [talk 66:04 to 67:40], so a good view fills a real gap.

After a quarter of nights you will have cost per accepted build and per accepted task at P50 and P80, first-pass rate, review minutes, evaluator-human agreement and escaped defects: an auditable track record a board or buyer can check, which Get AI's board strategy values over billable hours.

The "Agentic DevOps with Microsoft Azure and GitHub" specialisation fits this work and adds credits [snippet] ([specialisation page](https://partner.microsoft.com/en-US/partnership/specialization/agenticdevops-microsoftazure-github)). Cloud Accelerate Factory adds Microsoft-led deployment help ([July 2026 announcements](https://learn.microsoft.com/partner-center/announcements/2026-july#cloud-accelerate-factory-expands)). A fixed-scope Marketplace consulting offer is the natural package.

One hygiene rule: build the accelerator in Mode A, keep client code, data and traces out of it, and record which mode funded each run. Calibration examples from client work need the client's consent, or must be rebuilt from public references.

## Conclusion

The credits make the first months nearly free. They say nothing about price. The ledger's list column keeps pricing honest once credits expire or prove internal-only.

The workshop moved where the engineering effort goes. Copilot and Azure already ship most of the harness, so building more scaffolding is the IKEA trap. The effort belongs in the evaluator: its rubrics, its calibration and the habit of reading traces. That decides yield and review minutes, and those decide margin in both lanes. The question that could change the whole funding model is still a contract clause, not a technical limit. Ask it this week.

## 17. Transcripts: what the workshop changed, and what is still worth getting

Boroon supplied the transcript of Anthropic's workshop "How to Build Agents That Run for Hours" ([edited transcript](https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript)) **[user-supplied transcript]**, plus five slides. V1 rated it low value because the blog post covered the harness shape. That was wrong. The transcript held the operating detail the post does not, and it drove most of V2:

- Feature builds belong in one long session, not the 59-minute cloud agent (section 2).
- The parity table and component register (section 3).
- High-level specs, a criteria floor, contracts as a switch, spec re-sends, handoff files, evaluator isolation, rubric calibration and RESTART (section 4).
- Trace reading and weekly calibration as the main debugging loop (section 5).
- The Lane A cost model (section 12).

**Still worth getting.** GitHub Universe 2026 runs on 28 to 29 October, days away. Its sessions remain the highest-value input.

| Rank | Session | What it would settle |
|---|---|---|
| 1 | Universe: Copilot cloud agent and Agent HQ | Tasks API GA; concurrency limits; who pays for API-assigned sessions; a log export API; cloud agent subagents; any change to the 59-minute cap, which would move the routing rule |
| 2 | Universe: Copilot billing and enterprise admin | A per-session credit export; billing lag; GitHub meters in Azure Cost Management; the nano AIU to credit mapping |
| 3 | Universe: Copilot SDK | Dynamic workflows GA; OpenTelemetry conventions; `getMetrics` leaving experimental; whether SDK cloud sessions share the 59-minute cap |
| 4 | "Open Source Friday: Spec Kit Part 2" (16 October 2026) ([video](https://www.youtube.com/watch?v=8hHCpNVLhmI)) | Whether Spec Kit 1.0 can run the planner and grill steps with Copilot agents. Daytime tooling only |

Re-check sections 2, 3, 8, 10 and 12 against the Universe material once it is posted, and run the first component register review that week.
