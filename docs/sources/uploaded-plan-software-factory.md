**End-to-End Specification: The GET AI Microsoft Software Factory**

This specification defines a secure, governed, "Human-led, Agent-operated" software factory. It marries the continuous, multi-agent workflows of the "Michelin Kitchen" with the strict governance, risk mitigation, and platform realities of enterprise Microsoft environments.

**1. Core Architecture & Topology**

The factory is divided into distinct loops. Azure acts as the central brain, while human experts serve as the initiators, approvers, and final reviewers.

| **Factory Layer**                  | **Microsoft Technology**                           | **Primary Function**                                                                    |
|------------------------------------|----------------------------------------------------|-----------------------------------------------------------------------------------------|
| **Intake (Outer Loop)**            | Microsoft Copilot Studio                           | Human-initiated chat interface to capture initial requirements and gather context.      |
| **Orchestration (Chief of Staff)** | Azure AI Foundry + Microsoft Agent Framework (MAF) | Manages state, routes tasks to specialized agents, and oversees the ADO integration.    |
| **Planning (Wayfinder)**           | Azure AI Agent (Planning Spec)                     | Translates raw requirements into ADO Epics, Features, and strictly scoped User Stories. |
| **Execution (Inner Loop)**         | Azure AutoGen Workers + Dev Sandboxes              | Specialized coding agents executing tasks in isolated non-prod Dev environments.        |
| **Verification & PR**              | GitHub Actions / ADO Pipelines                     | Automated testing, code smell checks, and PR generation with Blast Radius assessments.  |

**2. The Step-by-Step Factory Workflow**

**Phase 1: Intake & Context Gathering (The Front Door)**

Currently configured for human initiation, paving the way for future ITSM automation.

- **Trigger:** A human engineer, consultant, or lead initiates a chat in a Microsoft Copilot Studio agent (e.g., "We need to build a new Power App for vendor onboarding based on this uploaded policy document").

- **Context Assembly:** The Copilot Studio agent asks clarifying questions to build the initial glossary.md and requirement spec. It identifies the target Practice (e.g., AI Business Solutions) and packages this into a JSON payload.

- **Handoff:** The payload is securely passed to the Azure-based "Chief of Staff" orchestrator.

**Phase 2: Wayfinder Planning & The Sign-Off Seam**

Agents map the work, but humans approve the blueprint before execution begins.

- **Ticket Generation:** The Azure Wayfinder agent parses the payload and interfaces with the Azure DevOps (ADO) REST API. It generates a comprehensive Epic (The Spec) and breaks it down into granular User Stories (The Tickets).

- **Dependency Mapping:** The agent applies predecessor/successor links in ADO to ensure the execution agents follow a strict logical path (e.g., "Define Dataverse schema" must precede "Build Canvas App UI").

- **The Sign-Off Seam:** **Execution pauses here.** Project Managers, Architects, or Tech Leads review the ADO Epic and mapped tickets. They adjust scope, refine acceptance criteria, and manually change the Epic state to "Approved for Factory."

**Phase 3: The Overnight "Dark Factory" (Inner Loop Execution)**

Triggered by the ADO approval, the Azure orchestrator spins up the specialized workforce.

- **Worker Spawn:** Azure AutoGen reads the unblocked ADO tickets and provisions ephemeral agent workers.

- **The Sandbox:** Agents deploy their work directly into the respective **Dev (non-production) environment** for that project:

  - *Power Platform:* Agent uses Power Platform CLI to unpack/pack solutions and push to a dedicated Dev Environment.

  - *Cloud & Data (Fabric/Azure):* Agent pushes PySpark notebooks to a Fabric Dev Workspace or deploys Bicep to an Azure Dev Sandbox.

  - *Security:* Agent deploys KQL queries and Sentinel policies to an isolated Azure Audit-Only subscription.

- **Red/Green Implementation:** The agent writes the code/configuration, runs localized verification checks within the Dev sandbox, and commits the work to an integration branch tied to the ADO Epic. It marks the ticket "Resolved" and grabs the next unblocked task.

**Phase 4: Verification, PR Generation & Human Review (The Morning Expo)**

The overnight work is prepared for human tasting.

- **Automated Review:** When the Epic is complete, ADO Pipelines or GitHub Actions trigger the Code Review agent. This agent checks the integration branch against the company's architectural decision records (ADRs) and looks for Martin Fowler-style code smells.

- **Evidence Collection:** The pipeline runs automated UI tests (Playwright) or unit tests in the Dev sandbox, attaching the logs to the PR.

- **PR Creation:** The agent generates a comprehensive Pull Request body detailing:

  - **Summary & Evidence:** What was built and the test logs proving it works.

  - **Merge Danger:** Assessed as a "Two-Way Door" (easily revertible UI change) or "One-Way Door" (destructive schema change).

  - **Blast Radius:** The scope of impacted systems.

- **Human Accountability:** In the morning, GET AI engineers review the PR, examine the blast radius, and click "Merge" to push the code from Dev toward UAT/Prod.

**3. Guardrails & Change Management (The Company Brain)**

Because this represents a fundamental shift from traditional human-led development to an agent-operated factory, the environment and the humans operating it must be meticulously aligned.

**Documenting the "New Way of Working"**

The first step of the factory implementation is using AI to help draft the new baseline documentation.

- **Factory Manifestos:** Create highly structured Markdown files detailing coding standards, naming conventions, and specific constraints for each of the 5 Practices. These files live in a central repository that the Azure Code Review agent reads dynamically during Phase 4.

- **Constraint by Design:** The Dev sandboxes will be pre-configured with strict Bicep policies, branch protection rules, and SonarQube gates. The agents will find it physically impossible to push unlinted or highly vulnerable code to the integration branch.

**Human Engineering Adoption**

To ensure rapid and easy adoption by the engineering team:

- **"Executive Chef" Enablement:** Engineers must be retrained to view themselves as Michelin chefs reviewing the work of sous-chefs. Training will focus on how to write effective Copilot Studio intake prompts, how to properly review Wayfinder ADO tickets, and how to read the "Merge Danger" assessments in PRs.

- **The Retro Loop:** The AI Managed Services practice will run a weekly Retro skill against the factory's logs. When engineers notice the agent making repeated mistakes, the Retro process will generate tickets to update the central Factory Manifestos (updating the agent's system prompt or linting rules). This proves to the human engineers that the system learns from their corrections, building deep trust in the factory over time.

**Copilot Studio Agents & App Builds**

This is a blueprint for transitioning the GET AI Copilot Agent from a human-led, AI-executed model into a strictly governed, overnight "dark factory." It is designed around the constraints of GitHub Enterprise data residency, Azure DevOps Boards, and the specific quirks of Power Platform APIs.

**1. Target Architecture & Identity Mapping**

The factory relies on strict separation of duties between the orchestrator (GitHub Actions), the planner/tracker (ADO), and the worker (the AI agent).

| **Component**                 | **Location**                | **Execution/Identity**           | **Role**                                                                                                                        |
|-------------------------------|-----------------------------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| **Work Queue**                | ADO Boards (getai org)      | ADO REST API                     | Holds "Ready to build" stories tagged factory-eligible.                                                                         |
| **Dispatcher & Orchestrator** | GitHub Actions (scheduled)  | token.actions.getai.ghe.com OIDC | Wakes up, checks preflight health, pulls the ADO queue, and assigns a single story to an isolated environment lane.             |
| **Execution Agent**           | GitHub-hosted ubuntu-latest | OIDC -\> Pipeline App Reg        | Headless Claude Code (or custom Python wrapper). Reads CLAUDE.md, branches, edits code, applies to Dataverse, and opens the PR. |
| **Factory Environments**      | Power Platform              | Dataverse Workflow App Reg       | A pool of 3 long-lived Dev environments (e.g., factory-1). Holds the manual Teams/Secret connections.                           |
| **Verification & PR Checks**  | GitHub Actions              | OIDC -\> Pipeline App Reg        | Runs --plan, builder diffs, and run_workflow.py scenarios.                                                                      |
| **Review Agent**              | GitHub Actions              | Pipeline App Reg (LLM API key)   | A secondary LLM step that evaluates the diff against CLAUDE.md, scores Merge Danger, and auto-merges if safe.                   |

**2. PR Check Suite (GitHub Actions YAML)**

This workflow forms the automated safety net. It runs on pull_request and executes the idempotent scripts to prove the agent's work is deployable.

YAML

name: Factory PR Checks

on:

pull_request:

branches: \[ main \]

permissions:

contents: read

id-token: write

pull-requests: write

env:

GH_HOST: getai.ghe.com

APP_ID: \${{ vars.PIPELINE_APP_ID }}

TENANT_ID: \${{ vars.TENANT_ID }}

\# Environment dynamically assigned based on the PR label or branch prefix

DEV_URL: \${{ vars.FACTORY_ENV_URL }}

jobs:

validate-and-test:

runs-on: ubuntu-latest

environment: factory-pool \# Mapped to immutable OIDC subject in Entra

steps:

\- uses: actions/checkout@v5

\- name: Setup Python & Dependencies

uses: actions/setup-python@v5

with:

python-version: '3.11'

\- name: Setup pac CLI

uses: actions/setup-dotnet@v5

with:

dotnet-version: 8.0.x

\- run: dotnet tool install --global Microsoft.PowerApps.CLI.Tool

\- name: Authenticate via OIDC

run: pac auth create --githubFederated --applicationId "\$APP_ID" --tenant "\$TENANT_ID" --environment "\$DEV_URL"

\- name: 1. Builder Check (No manual edits to generated files)

working-directory: scripts

run: \|

for builder in ../workflows/build/\*.py; do

python3 "\$builder"

done

git diff --exit-code \|\| { echo "Generated files do not match builders"; exit 1; }

\- name: 2. Schema & Security Plan (Read-only check)

working-directory: scripts

run: \|

python3 create_schema.py --plan

python3 create_security.py --plan

\- name: 3. Lints & Limits

run: \|

\# Fails if an if() expression exceeds 8192 chars or uses unsafe substrings

python3 scripts/lint_logic_apps.py

\# Fails if components leaked into wrong root solution

python3 scripts/check_root_components.py

\- name: 4. Scenario Tests

working-directory: scripts

run: python3 run_workflow.py --suite all

**3. ADO State Machine Automation**

The orchestrator owns state, not the agent. This resolves the race conditions identified in Section 9.1.\\

- **Trigger:** GitHub events webhook sent to an Azure Function or a central GitHub Action in GetAI-Project-Setup.

- **State Mapping:**

  - branch created matching a work item ID -\> Moves ADO state to **Building**.

  - pull_request opened -\> Moves ADO state to **Testing**.

  - pull_request merged -\> Moves ADO state to **UAT Ready** (or PROD Ready based on environment).

- **Custom Fields Required in "Agile build v1":**

  - Factory Eligible (Boolean): Human toggles this when acceptance criteria are complete.

  - Merge Danger Score (Integer): Written by the Review Agent.

  - Blocked Reason (Text): Written by the Execution Agent if it hits a portal-only task.

- **Parking Mechanism:** If the execution agent hits a human-only step (e.g., admin consent required), it exits with a specific code. The GitHub Actions orchestrator catches this, moves the ADO state to **Awaiting business**, writes the agent's question into the Blocked Reason field, and immediately pulls the next story for the next factory lane.

**4. Merge Danger Scoring**

The Review Agent calculates a score from 0 to 10.

**Thresholds:**

- **0-2 (Low Danger - Auto-Merge):** Edits to docs/, state.md, tests, or generated JSON/XML that perfectly matches its Python builder. Test suite passes 100%.

- **3-5 (Medium Danger - Human Merge):** Interface changes requiring sync_agent_tools.py, edits to workflow builders, additions to reference data.

- **6-10 (High Danger - Human Merge):** Security role modifications, schema changes (one-way column drops), logic affecting allowances/money, changes to pipeline YAML or credentials.

**Auto-Merge Gate:** If the calculated score is $\leq 2$ AND all GitHub Action PR checks are green AND a drift check (sync_solutions.py) shows 0 unintended changes, the GitHub Action automatically merges the PR using the gh CLI.

**5. System Prompts**

**Execution Agent Prompt:**

You are the GET AI execution agent. You build strictly within the Microsoft Power Platform using Python builders, JSON, and scripts.

1.  **Code over click ops:** Always use scripts or APIs. If a task requires a human portal click (e.g., Teams connection consent, Dataverse hierarchy exclusion), STOP. Output exactly: "PARK: \[Exact instruction for human\]" and exit. Do not invent inputs or bypass the requirement.

2.  **Identity:** Never hardcode or inject identity into tool inputs. Rely strictly on x-ms-object-id headers.

3.  **Design First:** For user-facing changes (cards, agent wording), you must output a markdown mock design and halt. Only proceed to build if the work item explicitly contains an approved mock.

4.  **One Branch:** Make all changes on the current branch. Do not push to a branch if a PR is already open and under review.

5.  **Documentation:** Update state.md with your Dev changes and append any new gotchas to docs/lessons-learned.md.

**Review Agent Prompt:**

You are the GET AI code review agent. Your job is to score Merge Danger and verify compliance with CLAUDE.md.

1.  Evaluate the git diff. Calculate the Merge Danger score (0-10) using the strict rubric.

2.  Verify that generated XML/JSON changes correspond to changes in their Python builders.

3.  Verify that test scenarios (run_workflow.py) cover the new logic.

4.  If the score is \> 2, output a concise summary of the blast radius for the human reviewer. If you detect drift (changes outside the PR scope), flag it as a blocker.

**6. Environment Isolation Strategy (The Pool)**

Creating a new environment per run is impossible without halting for human API consent (Teams/Hierarchy exclusions).

**The Pooled Approach:** Maintain a pool of 3 long-lived Dev environments (factory-lane-1, factory-lane-2, factory-lane-3).

1.  **Bootstrap (Human - Once):** A human creates the environment, configures the security group, performs the Teams OAuth sign-in, creates the Dataverse connection with the secret, and excludes tables from hierarchy security.

2.  **Preflight (Automated - Nightly):** Before accepting a job, the lane runs a health check: pac connection list (validates credentials), reads hierarchysecurityconfiguration, and checks Entra App permissions against the manifest. If a check fails, the lane is marked "Offline" and a bug is raised in ADO.

3.  **Reset (Automated - Per Story):** Before an agent begins a story, a reset_environment.py script runs. It deletes transactional test data (e.g., trips created in the last run) and runs a clean import of the main branch solution XML to overwrite any unmerged experiments from the previous night.

**6b. Agent Testing Gap Strategy:** Until Microsoft opens the Copilot Studio conversation API for the new harness, separate the workflow from the conversational agent. The overnight factory guarantees that the underlying *workflows* execute perfectly via run_workflow.py. The "Morning Digest" will explicitly list PRs that altered agent tools or instructions, prompting the human to spend 5 minutes in the Copilot Studio test pane verifying the NLP routing before hitting merge.

**7. Phased Rollout**

- **Phase 1: The Safety Net (Days 1-14):** Deploy the GitHub Actions PR Check Suite (Section 2) on the existing human-led process. Humans continue to trigger the AI in VS Code, but the pipeline now blocks bad generated code, expression limits, and solution drift.

- **Phase 2: ADO Automation (Days 15-21):** Deploy the GitHub-to-ADO state machine. The human still reviews and merges, but project reporting becomes instantly accurate based on Git events.

- **Phase 3: The Night Shift (Days 22-45):** Activate the Dispatcher and Execution Agent on pooled environments. Humans queue stories tagged factory-eligible at 5 PM. The factory runs overnight, parks blockers, and prepares PRs. Humans spend 9 AM - 10 AM reviewing Merge Danger scores and clicking merge.

- **Phase 4: Dark Factory (Day 45+):** Enable auto-merge for PRs that score 0-2 on the Merge Danger rubric.

**8. Unseen Risks & Failure Modes**

1.  **Entra ID Eventual Consistency:** Creating an Entra group or assigning an app role via API can take 5 –15 minutes to propagate across Microsoft's backend. If an agent script creates a security context and immediately tests a workflow relying on it, the test will falsely fail. ***Mitigation**:* Scripts touching Entra must build in deterministic polling/wait loops before proceeding to tests.

2.  **LLM Runaway Cost Loops:** An unattended headless agent dealing with a persistent script failure may attempt to fix it 50 times in a row, burning massive API credits. ***Mitigation**:* The orchestrator must enforce a strict token budget or iteration cap (e.g., max 5 execution loops per ADO ticket) before forcefully parking the story.

3.  **Dataverse API Throttling:** If all 3 factory lanes attempt to run sync_solutions.py or massive data seeds simultaneously, the shared tenant API limits may trigger 429 Too Many Requests. ***Mitigation**:* Implement exponential backoff in all custom Python scripts accessing the Dataverse API.

4.  **GitHub Actions Runner Compute & Timeouts** In your current check-pac.yml, you are using ubuntu-latest GitHub-hosted runners. These are fine for deterministic PR checks, but your overnight **Execution Agent** runs will be long-lived, multi-turn AI loops that could easily run for 30–60 minutes per ticket. GitHub-hosted runners bill per minute and have a hard 6-hour timeout limit. ***Mitigation**:* For the Dispatcher & Execution phase, deploy self-hosted GitHub runners backed by Azure Container Apps or Azure VMs. This gives you predictable cost control, eliminates the GitHub-imposed timeouts, and allows you to pre-bake the pac CLI, Python 3.11, and the Microsoft Agent Framework (MAF) binaries into the runner image, shaving minutes off every job start.

5.  **Distinct AI Identity for Auditing** Make sure the OIDC federated credential your pipeline uses maps to a dedicated Entra ID Service Principal specifically named for the AI (e.g., ai-factory-execution-agent-dev). Since this identity will be moving ADO tickets and pushing code, you want your audit logs to clearly distinguish between when the Director of AI Services acted, and when the AI acted on their behalf.
