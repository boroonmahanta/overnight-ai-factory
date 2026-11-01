# **GET AI** Overnight Factory

For GET AI engineers. One-page summary of plan V3.1, focused on Lane B for Power Platform. 1 November 2026.

GET AI

We own the spec and the merge. Agents build and verify overnight.

How a day and a night run: triage -> spec -> build -> verify -> merge

1\. Triage

Outer loop, business hours

- Client reports from service desk, Teams, alerts and ADO
- Triage agent groups related reports first
- Reproduces each group in `factory-test` with `lcp-verify`
- Draft ADO bug with repro steps and evidence
- A human decides what goes to the gate

2\. Day

Spec gate on Spec Kit 1.2

- Foggy work starts as a Wayfinder map
- Agents look up facts and ask only for decisions, one at a time
- `glossary.md` and decision records updated
- Scenarios written by someone else, then locked
- Mock or throwaway prototype approved
- A human sets Factory Eligible

3\. Night

One story per lane

- Copilot CLI, headless, on an Actions runner in Australia
- Reset, build, verify in the lane with `lcp-verify`
- Red before green at the agreed seams
- Portal steps and decisions PARK
- Research tickets run on their own runners

4\. Verify

The gate decides

- Required workflow in `factory-gates`, trusted scripts only
- Managed import into `factory-test`
- Locked and held-out scenarios
- 1 to 3 verifiers, scaled by Merge Danger
- Two-axis review: standards and spec

5\. Morning

A human merges

- 05:41 digest, 09:00 to 10:00 review
- PR body: diagram, before and after, Merge Danger, blast radius
- Resolve PARKs and answer questions
- Approve PRs into `integration`
- Human release PR to `main`, then UAT

Lane B, Power Platform profile (`lcp`): built first

Work Queue

ADO Boards; only the orchestrator changes state

Dispatcher

Scheduled Actions plus an Azure Function; a deterministic loop

Executor

Copilot CLI with pac and Microsoft's skill plugins; Claude via Copilot

Three Lanes

Sandbox Managed Environments in Australia; one story each, under a lock

Lane Care

Bootstrap once by hand, preflight nightly, reset per story

Test Environment

`factory-test`: managed import of each PR, certificate test user

Four Identities

Execute, verify, review, merge; per lane; OIDC, no secrets

Story Planner

Optional Copilot Studio front door; drafts Epics and stories

Other lanes

Lane A

Greenfield code builds: one long Copilot SDK session in Container Apps

Lane B, Code

Issue-sized code changes on the cloud agent, 59-minute cap

Human-led by Day

Canvas authoring, new-harness agents, tenant settings

Routing: a story-sized change in a Power Platform solution, with scenarios locked and every consent already bootstrapped -> **Lane B, Power Platform**. Nobody can name the stories yet -> **a Wayfinder map first**.

`lcp-verify`: the agent's hands and eyes

| Command | Does |
| --- | --- |
| `app <route>` | Opens a canvas or model-driven app as the test user, runs a journey, saves a screenshot and trace |
| `query <table>` | Reads rows and computed fields through the Web API, with backoff |
| `flow <name>` | Seeds tagged data, triggers the flow, checks the side effect, reads FlowRun |
| `agent <set>` | Runs a locked Direct Line script or a Copilot Studio test set |
| `smoke` | Runs the solution's key journeys once |

- **Two copies.** The executor uses the lane copy; its results are claims. Verifiers and triage use the trusted copy from `factory-gates`; theirs is the verdict.
- **One verify profile per solution,** kept by the test author and protected, so an agent cannot shrink what gets checked.

Merge Danger and the trust ladder

| Score | Verifiers | Merge into `integration` |
| --- | --- | --- |
| 0 to 2 | 1 | Human at L0 and L1. Auto-merge at L2 if the change class is eligible |
| 3 to 5 | 2 or 3 | Human, with blast radius |
| 6 to 10 | 2 or 3, plus a human | Human, door called out; second reviewer at 8 and above on client work |

- **The floor comes from a script:** changed paths, schema and security plans, gate results. The reviewer may raise it, never lower it.
- **Rungs per project and change class:** L0 humans run agents by day; L1 night shift, humans approve every PR; L2 auto-merge for eligible classes, with a sampled review; L3 is a proposal only.
- **Climb on evidence, never on a date.** Any escaped defect drops the class back to L1. `main` is always human.

Rules we do not break

- **Agents never merge to `main`.** No agent, App or identity sits on a bypass list.
- **The worker never decides it is done.** The gate and isolated verifiers decide.
- **Scenarios come from someone else,** locked before the night. The held-out set stays hidden.
- **Credentials and untrusted code never share a job.**
- **One story, one lane, one branch, one PR,** under a lane lock.
- **Facts are looked up, decisions are asked.** Portal steps and decisions PARK.
- **Design first.** An approved mock or prototype. Prototypes are never promoted.
- **Every run has a `run_id`,** a credit cap and a loop cap.
- **Agents, skills, `lcp-verify`, glossary, decision records and coding standards** change only by a reviewed daytime PR.
- **Read every third-party skill in full,** then pin it.

Files on every story branch

| File | Holds |
| --- | --- |
| `spec.md` | What and why; frozen once approved |
| `state.md` | Every change applied to the lane, with the command |
| `park.json` | PARK type, exact instruction, resume hint |
| `learnings.json` | Tried, found, fixed, worked |
| `findings.md` | Verdict, scores, failed criteria |
| `evidence/` | Traces, screenshots, SARIF, evaluation JSON |
| `pr.md` | Summary, diagram, before and after |
| `tests/dev/` | The worker's own red-green checks |
| `glossary.md`, `docs/adr/` | Domain terms and decisions; day gate only |
| `lessons-learned.md` | Hints only; curated weekly |

Machine names stay product-neutral (`lcp`, `fl1`, `factory-lane-1`), because Microsoft may rename Power Platform.

Every run is priced

- **Measured per agent role** from Copilot CLI telemetry: tokens and AI units per span.
- **One machine account and cost centre** per project runs the night.
- **Triage, research and gardening** get their own ledger rows.
- **Posted tonight,** reconciled to billing on day three, priced at list.

USD 11.82per story attempt, AI and compute at list (model)

USD 150per accepted story, fully loaded; human minutes are most of it (model)

About 1.3 lanesfunded by one partner designation's credits (model)

Shipped: use as is

- Copilot CLI, SDK and cloud agent
- Custom agents, skills and hooks
- pac CLI and `powerplatform-actions`
- Microsoft's Playwright toolkit for Power Platform
- Copilot Studio evaluation and the Agent Kit
- Microsoft's Power Platform and Dataverse skills, Dataverse MCP
- Rulesets, required workflows, merge queue
- Spec Kit 1.2, presets and workflows

Thin glue: expect to delete

- Lane mapping and locks
- Preflight and per-story reset
- Manifest check after pack
- Direct Line runner
- ADO state Function and FlowRun poller
- Triage intake Function
- Merge policy and the trust file check

Reviewed monthly, after Ignite (17 to 20 November) and after each model release.

Our IP: invest here

- `lcp-verify` and the verify profiles
- The `getai-lcp` preset and bundle
- Gate workflow and trusted scripts
- Merge Danger rubric and the trust ladder
- Coding standards and the smell list
- Rubric skills and the evaluator calibration set
- Triage agent and the Wayfinder pattern
- Cost ledger and profitability matrix

What engineers do

- **By day:** run the Spec Kit gate with the spec owner. Write or review scenarios, then lock them. Check triage evidence before a bug goes to the gate.
- **Each morning:** read the evidence, resolve PARKs, approve PRs into `integration`, and review the L2 sample once a class has climbed.
- **Each week:** grade 10 verifier verdicts and read failed traces in full. Run the retro on a sample of sessions and work the gardening findings list. Change prompts, rubrics and lints by PR.
- **Before the night shift starts:** export your own human-led sessions so the retro can mine your corrections.
- **Each model release:** remove one piece of glue, measure, then keep it out or put it back.

Build stages and key dates

1. 0Spikes and money: credit ruling, pac sign-in on GHE.com, environment auditNow
2. 1Safety net: gate repo on today's human-led workDays 1 to 14
3. 2ADO automation and `lcp-verify` v015 to 21
4. 3Night shift, one lane (rung L1)22 to 30
5. 4Three lanes, calibrated; triage pilot31 to 45
6. 5Lane B for code repos
7. 6Lane A
8. 7Rung L2 per class, on evidence
9. 8Scale, engines, keep healthy

- **15 Nov 2026**No new unmanaged developer environments. Lanes are Sandbox plus Managed
- **17 to 20 Nov**Ignite: re-check names and Copilot Studio evaluation APIs
- **15 Dec 2026**Unmanaged developer environments suspended
- **15 Jan 2027**Unmanaged developer environments deleted
- **Feb 2027**Stricter premium licence checks in Managed Environments

We build the gate first. Models change every release. The gate is what we own.

Summary of plan V3.1 (plan.md), 1 November 2026. Figures marked model are arithmetic on list prices, not measurements. Client work runs at cash until Microsoft confirms in writing that partner credits can fund it.