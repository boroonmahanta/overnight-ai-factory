# Fund Nights on Credits, Price at List

**Bottom line.** Keep the factory design from the earlier report and change its engine and plumbing. The Copilot cloud agent becomes the night worker for tasks that fit its 59-minute session cap. Copilot SDK workers on Azure Container Apps take the longer tasks. Short event-driven GitHub Actions workflows and a 20-minute reconciler replace the always-on supervisor. Rulesets and an organisation-level required workflow become a gate the agent cannot edit. Azure holds the secrets, the evidence, the telemetry and a cost ledger that prices every run at list, contracted, effective and cash cost. One Solutions Partner designation gives about USD 1,250 a month in credits (USD 833 Azure, USD 417 Copilot). On our model, that funds one project at 20 light nights a month, or about seven heavy nights. The biggest risk is contractual, not technical. Microsoft calls partner Azure credits "internal-use-rights" credits, and nobody has confirmed they can fund client delivery. So run two modes from day one: internal work on credits, and client work that can run at cash cost. On credits, get Claude through Copilot or use Azure OpenAI. Claude in Microsoft Foundry bills a card, not credits, and has no Australian region. Price every client job from the ledger's list column. Merge rate and review minutes move cost per accepted feature far more than token price does.

**How to read this.** All prices are USD list as read on 24 October 2026. Figures labelled "model" are arithmetic on stated assumptions, not measurements. A citation with no marker was read in full by the researchers. **[secondary]** means a third-party write-up was read, not the original. **[snippet]** means only a search summary was available, so treat it as unverified. This plan builds on the earlier report at `/tmp/claude-0/-home-user-metro-map-of-music/b195798a-3816-5afd-9b0e-91fd7d5ff91b/scratchpad/reports/Overnight AI software factory.md` and does not repeat its research.

## 1. The earlier design holds; only where each part runs changes

The earlier report's design still stands. Its core parts are:

- A daytime "grill" gate that questions the spec owner until every acceptance criterion has an executable check.
- Acceptance tests written by a separate author and locked before the night starts, plus a held-out suite the worker never sees.
- One bounded task per agent session, with state in files and git, not in the model's context.
- A "done" verdict that never comes from the worker: CI plus a fresh-context evaluator that shows Playwright evidence.
- Serial integration, a human merge in the morning, and a morning evidence package.

Nothing in the GitHub and Azure research weakens any of this. Some Copilot limits even enforce it for free: one PR per task, a hard session cap, and a rule that the person who started a task cannot approve its PR ([risks and mitigations](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations)). The table maps each earlier part onto its new home.

| Earlier part | GitHub and Azure version | What changes |
|---|---|---|
| `/grill` skill plus gate script | A `grill` custom agent in `.github/agents/`, run by the spec owner in VS Code or Copilot CLI by day. The same TypeScript gate script runs as a required check on the spec PR. | Daytime use bills to the human's own seat, so it stays out of the night ledger. Custom agents fix the prompt, model and tool list ([custom agents](https://docs.github.com/en/copilot/reference/custom-agents-configuration)). |
| Separate test-author session | A `test-author` custom agent, run by day under a human seat. A member of `@acceptance-owners` reviews and pushes the tests. | A push ruleset lets only that team change `tests/acceptance/**`, so a night agent cannot even commit there ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)). |
| Held-out suite in `tests/holdout/` | Moves to a private `factory-gates` repo that the required workflow checks out. | The cloud agent's GitHub MCP server sees only its working repo by default, and it cannot read Actions secrets ([Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github); [secrets](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables)). So the worker cannot see the held-out tests. This is our inference. |
| TypeScript supervisor on a systemd VM | Four short Actions workflows (kickoff, dispatch, tick, report) plus one small Azure Function for the ledger. Durable Functions only when section 5's triggers apply. | No always-on VM. State lives in issues, PRs, a night plan file and the ledger. |
| Worker: `claude -p --worktree ...` | A cloud agent task via `POST /agents/repos/{owner}/{repo}/tasks` with `custom_agent`, `model` and `base_ref` ([agent tasks API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api)). Longer tasks run as a Copilot SDK session in an Azure Container Apps (ACA) job. | 59-minute cap. One repo, one branch, one draft PR per task ([Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github)). |
| Claude Code hooks (`PreToolUse`, `Stop`) | `.github/hooks/*.json`. `preToolUse` denies writes to protected paths and risky commands, and `ask` is treated as `deny`. `agentStop` returns `decision: "block"` until fast checks pass ([hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)). SDK workers use `onPreToolUse` ([SDK hooks](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/hooks)). | Hooks load only from the default branch ([use hooks](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks)). A blocked stop still burns the 59 minutes. |
| `--max-budget-usd` | CLI `--max-ai-credits` (soft, minimum 30) or SDK `sessionLimits.maxAiCredits` ([CLI session limit](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit); [SDK session limits](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/session-limits)). The cloud agent has no per-session cap, so use a hard-stop user budget on the machine account plus the dispatcher's night envelope. | Both caps are soft. The SDK checks after each model call returns, so one response can overshoot. |
| `--max-turns` | CLI `--max-autopilot-continues`; the cloud agent's 59-minute cap ([CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)). | |
| Auto permission mode and bubblewrap sandbox | Cloud agent: all tools pre-granted, trimmed by the custom agent's `tools` list and hooks, on an ephemeral runner with a default-on firewall. ACA workers: VNet egress through Azure Firewall or a NAT Gateway. | The cloud agent firewall covers only processes the agent starts with its Bash tool. It does not cover MCP servers or setup steps ([firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall)). |
| `AGENT_STOP` kill switch | A `factory-stop` workflow: stop running sessions, cancel ACA executions, and remove the repo from the cloud agent's allowed repos through the management API ([enable cloud agent](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/add-copilot-cloud-agent)). | |
| Evaluator subagent with Playwright MCP | A fresh Copilot SDK session with a read-only `evaluator` custom agent, run as a job inside the required gate workflow. Its PASS or NEEDS_WORK is a required check. | Copilot code review at Lite effort is a second opinion. It is never the verdict. |
| CI gate on each draft PR | An organisation ruleset "Require workflows to pass before merging" that points at `factory-gates`, with checks pinned to the expected source app. | The PR cannot edit the gate, because the gate file lives in another repo ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)). |
| Serial merge into `overnight/<date>` | A merge queue on a fixed `integration` branch, fed by a factory GitHub App. | Merge queue cannot be used with wildcard branch-protection patterns, so a fixed branch name is the safe choice ([merge queue](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)). |
| Human merge in the morning | One `integration` to `main` PR, approved by a human who did not start the tasks. | Copilot cannot approve or merge, and the initiator cannot approve ([risks and mitigations](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations)). |
| Morning package in Slack or an issue | `night-report.yml`: a job summary, JSON evidence and session logs to Azure Blob, and an Adaptive Card posted to a Teams Workflows webhook. | Teams classic connectors are being retired ([Teams webhooks](https://learn.microsoft.com/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)). |
| Telemetry and evals | SDK `assistant.usage` and `getMetrics`, GitHub billing APIs, the audit log streamed to Azure, Application Insights. | The cloud agent has no per-session cost API. |
| DBOS or Temporal (stage 4 option) | Durable Functions on the Durable Task Scheduler, Consumption tier ([DTS](https://learn.microsoft.com/azure/durable-task/scheduler/durable-task-scheduler)). | |
| Claude cloud scheduled tasks | Copilot automations, for maintenance chores only. | Hourly, daily or weekly. One repo each. Billed to the creator ([automations](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations)). |

## 2. Credits fund the internal factory; client work waits on one written answer

### What the designation actually gives you

| Benefit, per year | One Azure-area Solutions Partner designation | Each Azure specialisation (cap of 5) |
|---|---|---|
| Azure bulk credits | USD 10,000 | plus USD 12,000 |
| GitHub Copilot Enterprise (via Azure credits) | USD 5,000 | plus USD 4,680 |
| GitHub Enterprise Metered (via Azure credits) | none | plus USD 2,520 |
| Visual Studio Enterprise | 25 IDE licences, no monthly Azure credit | plus 10 full subscriptions |
| GitHub Enterprise seats or Actions minutes | none | none |

Source: [benefits guide summary](https://learn.microsoft.com/partner-center/benefits/benefits-at-a-glance). The designation fee is USD 4,875 a year ([pay the fee](https://learn.microsoft.com/partner-center/membership/mpn-pay-fee-silver-gold-competency)). The partner FAQ quotes USD 5,320 for the specialisation Copilot retrofit, which conflicts with the guide's USD 4,680 ([benefits FAQ](https://learn.microsoft.com/partner-center/benefits/benefits-faq-new)). Microsoft says GitHub credits from specialisations "can only be used for those purposes".

Other terms that shape the design:

- Credits are yearly and must be used before membership ends. From 1 November 2026 their expiry aligns to the offer purchase date. They are revoked if the purchase is cancelled ([use your Azure credits](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud); [August 2026 announcements](https://learn.microsoft.com/partner-center/announcements/2026-august)).
- Credits now land on an MCA billing profile (standard or premier) that has a card attached. A profile holds one credit source at a time. Subscriptions cannot leave the profile while credits are active ([use your Azure credits](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud)).
- Credits cover first-party Azure use only. They do not cover Marketplace products, reserved instances or support plans ([MCA credits](https://learn.microsoft.com/azure/cost-management-billing/benefits/credits/mca-check-azure-credits-balance)).
- Copilot seats, AI credit overage, Actions and GitHub Enterprise can all be billed to an Azure subscription connected to the enterprise or to a cost centre. Usage goes to Azure daily and lands on the next month's invoice ([Copilot Azure billing](https://docs.github.com/en/copilot/reference/copilot-billing/azure-billing); [Azure subscription reference](https://docs.github.com/en/billing/reference/azure-subscription)).
- No page says in one place that partner credits pay these GitHub meters. The benefit names ("via Azure credits") show Microsoft intends it. GitHub also lists some Azure subscription types it will not accept, and a Microsoft Q&A answer contradicts that list, so test the connection ([supported payment methods](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/supported-payment-methods); [Q&A](https://learn.microsoft.com/answers/a/12897076)).
- Whether credits can pay GitHub Enterprise seat licences is unclear. A different Microsoft program says "Azure cannot pay for Enterprise licenses" ([Startups GitHub Enterprise](https://learn.microsoft.com/startups/investor-network-benefits/technical-benefits/github-enterprise)). The specialisation's "GitHub Enterprise Metered" credit suggests metered seats are covered there. Treat this as probable, not confirmed.

### The eligibility risk

Microsoft's own wording is the warning sign. Partner credits "can't be moved or transferred outside the Billing Account boundary. This guardrail ensures that internal-use-rights credits stay within the partner organization" ([credits FAQ](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud#azure-credits-faqs-legacy-experience)). Partner Visual Studio Enterprise subscriptions "are for internal use only". Partners may not use them to "Develop, test, or maintain applications as part of customer or client projects" ([VS Enterprise for partners](https://learn.microsoft.com/visualstudio/subscriptions/program-mcpp#internal-use-only-restriction)). The binding rules sit in the AI Cloud Partner Program Terms of Participation Guide ([manage your benefits](https://learn.microsoft.com/partner-center/benefits/manage-your-partner-network-benefits#types-of-benefits)). The researchers could not read it. So nobody knows yet whether the Azure and Copilot credits can fund client delivery.

**The single check that resolves it.** Send Microsoft Partner Center support one question in writing, and ask them to cite the Terms of Participation Guide in the answer:

> "May Get AI use its Solutions Partner Azure bulk credits and its GitHub Copilot Enterprise (via Azure credits) benefit to pay for GitHub and Azure metered usage that Get AI incurs while delivering a paid client engagement, where the client never receives the credits, the subscription or the GitHub accounts?"

Keep the answer on file. Until it arrives, assume the answer is no. A second, mechanical test belongs in stage 0: connect the credited subscription to a test cost centre and check that the next invoice shows "Azure credits applied" against the GitHub lines ([MCA invoice terms](https://learn.microsoft.com/azure/cost-management-billing/understand/mca-understand-your-invoice#invoice-terms-and-descriptions)).

### Two modes, split at the billing boundary

| | Mode A: internal | Mode B: client |
|---|---|---|
| Work | The factory itself, the deployment accelerator, Get AI-owned IP, internal tools | Client deliverables |
| GitHub | Cost centre `cc-internal-<project>` with its own seated machine account | Cost centre `cc-<client>-<project>` with its own seated machine account |
| Azure | Subscription on the credited MCA billing profile | Subscription on a separate billing profile with no credits, paid by card or invoice |
| Funding | SPD credits | Cash, unless the written ruling allows credits |
| Ledger | Priced at list for internal ROI | Priced at list; cash cost equals effective cost |

GitHub lets each cost centre connect to a different Azure subscription ([Azure subscription reference](https://docs.github.com/en/billing/reference/azure-subscription)). Because subscriptions cannot leave a credited profile, set this split up before the first night. If the ruling says yes, Mode B only changes its funding line. Nothing else moves.

### What this means for model choice

| Path | Billed as | On credits? | Region | Use it for |
|---|---|---|---|---|
| Claude (Sonnet 5.5, Opus 5.5) through Copilot: cloud agent, SDK, CLI | GitHub AI credits at Anthropic's list rates ([rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml); [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)) | Yes, through the Copilot benefit and Azure-billed GitHub meters, subject to the ruling | Not stated in the notes | Default worker and evaluator models |
| OpenAI models through Copilot (GPT-6.1 Sol, GPT-5.3-Codex, GPT-6 Luna) | GitHub AI credits | Same as above | Not stated | Alternate default; Luna for cheap chores |
| Azure OpenAI in Foundry (GPT-5.x, Codex, GPT-6) | First-party Azure meter | Yes, models "sold and billed directly by Azure" are covered ([credit coverage](https://learn.microsoft.com/en-us/microsoft-for-startups/build/foundry-model-sponsorship-coverage)) | Australia East options, for example Global provisioned throughput for gpt-5.1-codex ([PTU](https://learn.microsoft.com/azure/foundry/openai/concepts/provisioned-throughput)) | Factory model calls outside Copilot; the Codex lane; clients who want Azure-contracted inference |
| Claude in Microsoft Foundry | Marketplace, in Claude Consumption Units ([CCU billing](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-billing)) | No: "the credit card will be charged instead of Azure Credits" ([deploy Claude](https://learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-claude)) | US regions and Sweden Central only; none in Asia Pacific ([regions](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-from-partners#region-availability-by-deployment-type)) | Only when a client mandates Claude on its own Azure contract and pays cash |
| Anthropic API direct | Anthropic invoice | No | Not applicable | Claude Code bake-offs at cash |

Four rules follow:

- On credits, get Claude through Copilot, not Foundry. The per-token price is the same. Only the payer changes.
- Use Azure OpenAI for any model call the factory makes outside Copilot. GitHub Models is retired (section 5).
- Do not plan on Claude in Foundry for Mode A. Its default pay-as-you-go quota is 40 RPM, 40,000 uncached input TPM and 8,000 output TPM, and Fable has zero ([Claude quotas](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-quotas-limits)).
- Check client data rules before you send client code to Copilot-hosted models. The notes do not establish where Copilot inference runs. Data-resident requests cost 10% more ([seats and billing cycles](https://raw.githubusercontent.com/github/docs/main/content/copilot/concepts/billing-and-usage/organizations-and-enterprises/seats-and-billing-cycles.md)).

## 3. GitHub runs the work, Azure keeps the records

The split is simple. GitHub runs anything that touches code: dispatch, the agent, the gate, the merge. Azure runs anything that must outlive a GitHub retention window or needs a fixed identity: secrets, evidence, telemetry, the ledger, and long or measured workers.

| Layer | Runs on | Paid from in Mode A | Notes |
|---|---|---|---|
| Spec gate, test author | Spec owner's VS Code or Copilot CLI, by day | Human's Copilot seat | Custom agents `grill` and `test-author` |
| Night plan approval | PR adding `factory/nights/<night_id>.json` | None | Approved by `@acceptance-owners` |
| Kickoff, dispatch, tick, report | Actions on standard Linux runners | Included Actions minutes | `schedule` with an IANA `timezone`, at odd minutes ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)) |
| Worker, tasks under about 40 minutes | Copilot cloud agent on an ephemeral Actions runner with firewall | AI credits on the project machine account, plus minutes | Default |
| Worker, long or must-be-measured tasks | Copilot SDK session in an ACA job (Australia East) | AI credits plus Azure credits for compute | Stage 5 |
| Evaluator | Job in the required gate workflow on a standard runner, running the SDK with the `evaluator` agent and Playwright | AI credits plus minutes | Fresh context, read-only tools |
| Second opinion | Copilot code review at Lite effort | AI credits plus minutes | Severity sits in comment text, not a structured field |
| Gate | Org ruleset required workflow from `factory-gates`; branch and push rulesets | Minutes | Section 4 lists the exact rules |
| Integration | Merge queue on `integration` | Minutes | Fed by the factory GitHub App |
| Secrets | Azure Key Vault, reached through Actions OIDC | Azure credits | OIDC tokens can carry `repo_property_<name>` claims, so access can be scoped per project ([OIDC](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/security/openid-connect)) |
| Evidence | Azure Blob, one container per project; audit log stream | Azure credits | Section 5 |
| Telemetry | Application Insights with OTLP on, plus Log Analytics ([OTLP ingestion](https://learn.microsoft.com/azure/azure-monitor/containers/opentelemetry-protocol-ingestion)) | Azure credits | Set a daily cap |
| Ledger | Azure Function on a timer, Azure Database for PostgreSQL flexible server (Burstable), Power BI | Azure credits; a Power BI licence is probably not credit-eligible | Section 6 |
| Optional orchestrator | Durable Functions, isolated worker, Durable Task Scheduler Consumption | Azure credits | Section 5 triggers |
| Secondary engines | ACA jobs: Codex CLI on Azure OpenAI; Claude Code on the Anthropic API | Azure credits; Anthropic at cash | Section 9 |
| Morning card | Teams Workflows webhook | None | |

**Identities.** Three kinds, no more:

- One seated machine account per project, for example `getai-p042-bot`. It sits in that project's cost centre and has a user-level budget. Its user-to-server token lives in Key Vault. GitHub's terms allow machine accounts run by a responsible human owner ([terms of service](https://raw.githubusercontent.com/github/docs/main/content/site-policy/github-terms/github-terms-of-service.md)).
- One factory GitHub App for everything that does not need a user token: check runs, labels, marking PRs ready, enqueueing, resetting `integration`, ruleset audits and billing reads. Billing endpoints accept an enterprise-installed App with billing read ([automate usage reporting](https://docs.github.com/en/billing/tutorials/automate-usage-reporting)).
- The human reviewers.

Neither the machine accounts nor the App ever sit in a ruleset bypass list.

**GitHub Enterprise Cloud is required.** Merge queue on private repos needs it ([merge queue](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)). So do usage report exports, cost centres and enterprise rulesets ([billing reports](https://docs.github.com/en/billing/reference/billing-reports); [cost centres](https://docs.github.com/en/enterprise-cloud@latest/billing/concepts/cost-centers)). The designation does not include GitHub Enterprise seats, so budget USD 21 per user per month for the machine accounts unless the specialisation's metered credit covers them.

## 4. Copilot's limits decide task size, identity and the gate

| Constraint | Source | Design response |
|---|---|---|
| Each session stops at 59 minutes. "This limit cannot be extended or bypassed." Setup steps and test runs count. | [Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github); [setup steps](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment) | Size tasks to 20 to 40 minutes of agent work. Cache dependencies and Playwright browsers in `copilot-setup-steps.yml`. Treat `timed_out` as a normal state: re-dispatch once with a narrower prompt, then park it for the morning. Send anything bigger to an SDK worker on ACA. |
| One repo, one branch, one PR per task. Copilot ignores later comments on the issue. | [Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github); [use cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github) | One issue per task. Disjoint file ownership. Order dependent tasks with issue dependencies. Iterate on the PR, not the issue. |
| The tasks and assignment APIs accept only user-to-server tokens. App installation tokens are refused. Task creation needs a Business or Enterprise seat. | [agent tasks API](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-via-the-api); [OpenAPI](https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json) | A seated machine account per project. AI credits are charged to "the user who triggered" them, so the machine account's billing rows are the project's rows ([cost centre allocation](https://docs.github.com/en/billing/reference/cost-center-allocation)). GitHub does not state this for API-assigned cloud agent sessions, so prove it in stage 0. |
| Actions workflows do not run on Copilot pushes until a writer clicks "Approve and run workflows". | [agent settings](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings) | Turn off "Require approval for workflow runs" in each factory repo, or nothing runs before morning. GitHub warns that unreviewed Copilot code could then gain write access or reach secrets. So: gate logic only in required workflows from `factory-gates`, no secrets in PR-triggered jobs, `pull_request` not `pull_request_target`, minimal token permissions, and Actions policies that limit which actors and events can start workflows ([Actions policies](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/about-actions-policies)). |
| On an EMU enterprise with Entra Conditional Access, "Actions that use a personal access token will likely be blocked". App installation calls are exempt. | [CAP support](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/configuring-authentication-for-enterprise-managed-users/about-support-for-your-idps-conditional-access-policy) | Only dispatch and `@copilot` follow-ups need the user token. Either exempt the machine accounts from IP rules, allow-list Actions IP ranges, or dispatch from an Azure Function whose fixed egress IP sits in a trusted location. The last option is our inference. Also note: on EMU, a schedule stops if the last person to edit its cron line is deprovisioned ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)). |
| When a ruleset blocks Copilot, GitHub's docs suggest adding Copilot as a bypass actor. | [Copilot on GitHub](https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github); [bypass actors](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) | This is the trap. A bypass on `main` or on protected paths lets the agent skip the gate. Fix the rule instead. Audit every factory repo nightly with `GET /repos/{owner}/{repo}/rulesets` and fail the kickoff if Copilot, the write role, the App or a machine account appears in any bypass list. |
| Copilot opens drafts, cannot mark them ready, approve or merge. The initiator cannot approve. Unattributed Copilot PRs need one extra approval by default. | [risks and mitigations](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations) | The App marks PRs ready for the `integration` queue. A human, never the machine account, approves the morning PR. Keep Copilot code review approvals (preview, off by default) off for `main` ([code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review)). |
| Hooks, custom agents and `copilot-setup-steps.yml` load from the default branch at job start. | [use hooks](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks) | Guardrail changes are daytime PRs behind CODEOWNERS. The agent cannot weaken its own hooks mid-run. |
| Scripted dispatch cannot set the reasoning level. Only the automations API takes `reasoning_effort`. | [secondary] [write-up](https://ecorpit.com/copilot-cloud-agent-automations-reasoning-level-config-2026/); [changing the model](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/changing-the-ai-model) | Pin the model in each custom agent. Use SDK workers where effort matters. |
| No per-session cost API. Billing "generally cannot trace consumed credits to specific prompts, sessions, or exact features". | [monitor AI usage](https://docs.github.com/en/copilot/how-tos/manage-and-track-spending/monitor-ai-usage) | Estimate per run, then reconcile to the daily per-user, per-model billing row (section 6). |
| No documented concurrency cap. An internal Copilot rate limit suspended all agent work for about an hour on 2 April 2026. | [agent management](https://docs.github.com/en/copilot/concepts/agent-capabilities/choosing-and-delegating-agent-work/agent-management); [snippet] [incident](https://pingoru.io/providers/github/incidents/19872) | Cap in-flight sessions in the dispatcher. Start at four per project. Budget one lost hour a night. |
| Cloud agent and MCP server policies are off by default on Business and Enterprise. | [enable cloud agent](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-organization/add-copilot-cloud-agent) | Enable them only for repos with the `factory=enabled` custom property. |

### The ruleset stack

No single switch keeps the agent off `main` and out of the tests. Four native layers do, all from the control plane notes ([available rules](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets); [about rulesets](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)):

1. **Branch ruleset `main-gate`** on the default branch, bypass list empty. Restrict deletions. Block force pushes. Require linear history. Require a PR with 1 approval, stale approvals dismissed, code owner review, approval of the most recent push, conversation resolution, and the default-on extra approval for unattributed Copilot PRs. Add a Required reviewers entry: `@acceptance-owners` on `tests/acceptance/**`. Require status checks (strict) pinned to their source app. Require code scanning results. Require merge queue.
2. **Branch ruleset `integration-gate`** on `integration`. Require a PR with zero approvals, pinned checks (`gate/fast`, `gate/evaluator`) and a merge queue. Zero approvals also switches off the unattributed-Copilot extra approval there. Leave force pushes allowed so the App can reset `integration` to `main` each evening without a bypass entry. That last choice is our inference: test it.
3. **Push ruleset `protected-paths`.** Restrict file paths: `tests/acceptance/**`, `factory/**`, `.github/workflows/**`, `.github/hooks/**`, `.github/agents/**`, `.github/copilot-instructions.md`, `.github/CODEOWNERS`. Bypass: `@acceptance-owners` and a platform team only. The agent's commit is rejected even on its own branch.
4. **Organisation ruleset `factory-required-workflows`**, targeting repos by custom property. "Require workflows to pass before merging", pointing at `factory-gates` pinned to a tag or SHA. Keep the acceptance-directory hash check inside it as a second lock.

Dry-run all four in Evaluate mode first. One gap: the docs do not say whether a push ruleset checks the merge commit the queue creates. Test that before relying on it.

## 5. A night is short workflows plus a 20-minute tick, not one long job

### End to end

Times are Sydney local. In daylight saving time (AEDT, UTC+11), 21:47 is 10:47 UTC and 05:41 the next morning is 18:41 UTC on the same UTC date. In standard time (AEST) the window is 11:47 to 19:41 UTC. Either way, **the whole night falls on one UTC date**. GitHub bills by UTC day ([billing reports](https://docs.github.com/en/billing/reference/billing-reports)), so a night-only machine account's daily rows are exactly one night.

| When (Sydney) | Step | Runs on | What happens |
|---|---|---|---|
| Day, by 17:00 | Plan locked | Human, PR | Specs pass the gate script. Acceptance tests are merged. A night plan `factory/nights/<night_id>.json` lists each task with its custom agent, model, size class, expected credits, the in-flight cap and the cutoff. An acceptance owner approves it. |
| 21:47 | Kickoff | Actions `schedule` with `timezone: Australia/Sydney` | Preflight: gate script, ruleset bypass audit, budgets in place, Copilot PR auto-run on, credit runway check. The App resets `integration` to `main`. Mint `night_id`. Write the night row to the ledger. |
| 21:52 | First wave | One Actions job that makes its writes in series | For each ready task, call `POST /agents/repos/{owner}/{repo}/tasks` as the project machine account, with `custom_agent: worker`, `model` and `base_ref: integration`. Long tasks start an ACA job instead. Store the returned task id against the `run_id`. Fill up to the in-flight cap. |
| 22:00 to 05:00 | Sessions | Cloud agent, or ACA | Setup steps restore caches. Hooks deny protected paths. `agentStop` runs fast checks. A draft PR appears on a `copilot/` branch. |
| On each push | Fast gate | Required workflow from `factory-gates` | Lint, typecheck, unit tests, acceptance tests, acceptance hash check, hard-rule lints. |
| After the fast gate | Evaluator and review | Same workflow; Copilot code review | The evaluator session returns PASS or NEEDS_WORK as a required check. Copilot code review at Lite adds findings. |
| :13, :33, :53 | Tick | Actions `schedule` | Read task states and checks. NEEDS_WORK: the machine account posts one batched `@copilot` review, at most two rounds. Batch with "Start a review", because each submitted comment can start work ([best results](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results)). `timed_out` or `failed`: one narrower re-dispatch, else park. PASS: the App marks the PR ready and enqueues it. Fill free slots from the ready queue while the night budget lasts. No new dispatch after 04:00. |
| On enqueue | Serial integration | Merge queue on `integration` | `merge_group` runs the full Playwright suite and the held-out suite. Build concurrency 1. A failure ejects the PR, and the next tick re-dispatches it as a conflict task. |
| 05:41 | Morning package | Actions | Job summary, Teams card, evidence and session logs to Blob, provisional ledger lines. |
| 07:30 to 09:00 | Human merge | Human | Sample the evidence. A code owner who is not a machine account approves the `integration` to `main` PR. Log review minutes per task. |
| Day 3 | Reconcile | Azure Function on a timer | Pull GitHub AI usage, the Actions detailed report and the Azure FOCUS export. Allocate the variance. Mark lines reconciled. |

Three Actions details matter here. Run the full suite only on `merge_group`, because running it on both `pull_request` and `merge_group` doubles the minutes. Make every dispatch and comment from one job with pacing, because GitHub's secondary limit is 80 content-creating requests a minute and 500 an hour ([rate limits](https://docs.github.com/en/enterprise-cloud@latest/rest/using-the-rest-api/rate-limits-for-the-rest-api)). Avoid the search API in the tick. List issues by label instead.

### Why not one long supervisor job

- GitHub-hosted jobs stop at 6 hours, and that cannot be raised ([Actions limits](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/limits)).
- Events caused by `GITHUB_TOKEN` do not start new workflows, apart from `workflow_dispatch` and `repository_dispatch` ([GITHUB_TOKEN](https://docs.github.com/en/enterprise-cloud@latest/actions/concepts/security/github_token)). `workflow_run` chains stop at three levels ([events](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)).
- A job that sleeps while polling is billed per minute. Environment wait timers and approval waits are free ([environments](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/deployments-and-environments)).
- `schedule` is best effort. It "can be delayed during periods of high loads", worst at the top of the hour, and "some queued jobs may be dropped" ([schedule](https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflows-and-actions/events-that-trigger-workflows)). Practitioners report 15 to 30 minute delays [snippet] ([Crontap](https://crontap.com/blog/github-actions-cron-drift-problem)). A stateless tick shrugs off a late or missing run. A single supervisor does not.
- Hosted runner assignment had multi-hour problems in February, May, August and October 2026 [snippet] ([February report](https://github.blog/news-insights/company-news/github-availability-report-february-2026/); [May report](https://github.blog/news-insights/company-news/github-availability-report-may-2026/); [August write-up](https://blog.incidenthub.cloud/github-actions-pages-outage-aug-6-2026); [5 October](https://uptimerobot.com/is-it-down/github/2026-10-05/)). The morning report must degrade gracefully when the night ran short.

### When Azure Container Apps or Durable Functions earn their place

Add **ACA jobs** when one of these is true:

- A task cannot be split to fit 59 minutes.
- Fixed-price client work needs a measured cost per session. SDK sessions give `assistant.usage` and `getMetrics` ([SDK usage](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/usage-and-billing)).
- You run the Codex-on-Azure-OpenAI lane (section 9).
- You want self-hosted runners to escape hosted-runner incidents, the 6-hour cap, or to reach private Azure resources. ACA event jobs support a GitHub Actions scale rule, but cannot run Docker inside the container ([runner tutorial](https://learn.microsoft.com/azure/container-apps/tutorial-ci-cd-runners-jobs)). Do not move the cloud agent itself to self-hosted runners: you must switch off its firewall there ([setup steps](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-environment)).

Run each task as its own job execution. Platform maintenance can interrupt long replicas, the default `replicaTimeout` is 1,800 seconds with no documented maximum, and a job's start permission can expose its secrets ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs)).

Add **Durable Functions** (isolated worker, Durable Task Scheduler Consumption) when one of these is true:

- The night needs a stateful wait, for example a human approval mid-run for a risky migration. On the Consumption plan, waiting for an external event costs nothing ([human interaction](https://learn.microsoft.com/azure/durable-task/common/durable-task-human-interaction)).
- Start times must be exact. Call `workflow_dispatch` from Azure instead of trusting `schedule`.
- Several projects share one budget and need priorities across repos.
- Dispatch must come from a fixed Azure IP to satisfy Conditional Access.

Known limits: 1 MB per orchestration payload, and in-process model support ends on 10 November 2026 ([DTS](https://learn.microsoft.com/azure/durable-task/scheduler/durable-task-scheduler); [external events](https://learn.microsoft.com/azure/durable-task/common/durable-task-external-events)). Do not use Codespaces as workers: organisations get no free quota and a codespace dies after 12 hours. Do not use custom-container dynamic sessions at this size, because each pool runs on dedicated E16 instances ([ACA billing](https://learn.microsoft.com/azure/container-apps/billing#dynamic-sessions)).

### GitHub Models is gone

GitHub Models was fully retired on 30 July 2026: playground, catalogue, inference API and BYOK ([GitHub Models](https://docs.github.com/en/enterprise-cloud@latest/github-models); [snippet] [changelog](https://github.blog/changelog/2026-07-30-github-models-is-now-retired/)). Do not use `permissions: models: read`. For cheap steps like summarising the night, use Copilot CLI in Actions with `permissions: copilot-requests: write`. That path meters to the organisation and ignores user budgets ([CLI in Actions](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/copilot-cli-in-github-actions)), so keep it for shared chores. Alternatively, call a small Azure OpenAI model on credits.

### Export evidence before it expires

- From 1 October 2026, retention also deletes checks, workflow runs and commit statuses. The default is 90 days. Private repos can set 1 to 400 days ([retention](https://docs.github.com/en/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository); [snippet] [changelog](https://github.blog/changelog/2026-07-17-actions-retention-will-cover-checks-workflow-runs-and-statuses/)).
- The per-run timing endpoints are closing down ([workflow runs](https://docs.github.com/en/enterprise-cloud@latest/rest/actions/workflow-runs)).
- Cloud agent session logs have no REST endpoint and no stated retention. Pull them with `gh agent-task view --log` ([CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli)).
- The audit log keeps web events for 180 days and Git events for 7. Stream it to Azure Blob or Event Hubs. Copilot agent session events can stream too, in preview for EMU and data-residency enterprises ([audit log streaming](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/streaming-the-audit-log-for-your-enterprise)).
- ACA keeps only the last 100 job executions. Send job logs to Log Analytics ([ACA jobs](https://learn.microsoft.com/azure/container-apps/jobs)).

So `night-report.yml` copies, per task: PR metadata, check runs and annotations, review comments, the session log, Playwright traces and screenshots, and the ledger rows. They go to a Blob container per project. Keep a second copy as an Actions artifact at 400 days.

## 6. The ledger prices every run four ways and settles on day three

### Design principle

Every engine reports tokens at the client. Billing reports by day and identity, never by run, task or PR. So build the ledger from the client side and reconcile it down to each provider's billing grain ([billing reports](https://docs.github.com/en/billing/reference/billing-reports); [Agent SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)). Shape it like FOCUS so it sits next to the Azure FOCUS export. FOCUS carries list, contracted, effective and billed cost on every line ([What is FOCUS](https://learn.microsoft.com/cloud-computing/finops/focus/what-is-focus#benefits)). No FOCUS version has token columns, and neither GitHub nor Anthropic publishes a FOCUS export, so you map those sources yourself ([FOCUS changelog](https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/working_draft/CHANGELOG.md)).

### Run identity

`run_id = {project}-{yyyymmdd}-{task}-{role}-{attempt}`, for example `p042-20261027-t017-worker-2`. It is deterministic, so retries are countable. Role is metadata (the custom agent's name), not a separate seat. Separate accounts per role would multiply seat fees.

| Stamp point | Cloud agent | SDK worker on ACA | Evaluator job | Claude Code or Codex |
|---|---|---|---|---|
| Engine id kept | Task `id` from the POST response | `sessionId`; the CLI also accepts `--session-id` | SDK `sessionId` | Claude `session_id`; Codex `thread_id` |
| Link to PR | Task `artifacts[]` gives the PR | Branch name | PR number from the event | Branch name |
| Branch | `copilot/...` (the agent picks it) | `factory/<project>/<night>/<task>-<role>-<attempt>` | Not applicable | Same pattern as SDK |
| Commit | Copilot commits link to the session log | Trailer `Factory-Run-Id:` | Not applicable | Trailer |
| On the PR | App comment with `Factory-Run-Id`; labels `night:`, `role:`, `engine:` | Same | Check run output | Same |
| Telemetry | None per session | SDK OpenTelemetry export plus `assistant.usage` | Same | `OTEL_RESOURCE_ATTRIBUTES="project.id=...,night.id=...,run.id=...,agent.role=..."` ([Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage)) |
| Azure | None | Job execution env vars `PROJECT_ID`, `RUN_ID`, `NIGHT_ID`; resource group tag `project=` | Key Vault via OIDC | Same as SDK |
| Billing identity | Project machine account | Project machine account token | Project machine account token | Anthropic workspace per project with a key per role; one Azure OpenAI resource per project |

Keep `run_id` out of metric labels. High-cardinality labels raise storage cost, and APIM's token metric drops data beyond 100 values per dimension ([Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage); [llm-emit-token-metric](https://learn.microsoft.com/azure/api-management/llm-emit-token-metric-policy)). Put it on events and logs only. The PR is the hinge between cost and revenue, because acceptance, review time and rework all hang off it.

### Measured versus estimated

| Engine or meter | Measured at run | Billing grain | Ledger status |
|---|---|---|---|
| Copilot cloud agent | Token use shows only in the web session view | AI credits per user, model and UTC day, with input, output, cache read and cache write tokens ([billing reports](https://docs.github.com/en/billing/reference/billing-reports)) | Estimated per run. Measured per night, project and model, thanks to the night-only machine account. |
| Copilot code review | Actions minutes under `dynamic/agents/copilot-pull-request-reviewer` | Credits go to the PR's human co-author, else the organisation; the model is not disclosed ([models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)) | Estimated |
| Copilot SDK | `assistant.usage` per model call, delivered live and not replayed on resume; `getMetrics.totalNanoAiu`, marked experimental ([SDK usage](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/usage-and-billing)) | As above | Measured, then cross-checked |
| Copilot CLI `-p` | No documented JSON usage schema ([CLI programmatic reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference)) | As above | Drive it through the SDK instead |
| Claude Code | `total_cost_usd`, `modelUsage` and `costBasis`, all client-side estimates ([Agent SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking)) | Anthropic Cost API, daily by workspace; usage within about 5 minutes ([Usage and Cost API](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)) | Measured, reconciled |
| Codex CLI | Tokens per turn, no cost field [snippet] ([JSONL reference](https://codex.danielvaughan.com/2026/04/08/codex-exec-jsonl-reference/)) | Azure meter per resource per day | Tokens measured, priced from the price table |
| Actions minutes | Job start and end times multiplied by the runner rate | Detailed report by repo, user and `workflow_path` per day | Measured |
| ACA compute | Execution start and end, multiplied by allocated vCPU and GiB | FOCUS export per tag per day ([exports](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-improved-exports)) | Measured |
| Telemetry, storage, Functions, Key Vault | Not applicable | FOCUS per tag | Allocated by event volume or runtime |
| Seats, program fee, platform work | Not applicable | Invoice | Allocated per night |
| Human time | Captured per PR | Timesheet code | Measured |

### Schema

Store source currency (USD) and an AUD conversion on every money line.

```sql
create table dim_project (
  project_id text primary key,            -- 'p042'
  mode text check (mode in ('internal','client')),
  client text, contract_type text,        -- fixed | tm | subscription | outcome
  github_cost_centre_id text, machine_account text,
  azure_subscription_id text, azure_resource_group text,
  anthropic_workspace_id text, funding_source text  -- spd_credits | cash
);

create table dim_price (                  -- snapshot nightly from SDK models.list and rate tables
  engine text, model text, effective_from date,
  input_per_mtok numeric, cached_per_mtok numeric,
  cache_write_per_mtok numeric, output_per_mtok numeric,
  source_url text,
  primary key (engine, model, effective_from)
);

create table fact_run (
  run_id text primary key,                -- p042-20261027-t017-worker-2
  project_id text, night_id date, night_utc_date date,
  task_id text, feature_id text,
  agent_role text,    -- planner | test_author | worker | evaluator | reviewer | ops
  engine text,        -- copilot-cloud-agent | copilot-sdk | copilot-review | claude-code | codex-cli
  model text, engine_session_id text,
  pr_number int, head_sha text,
  started_utc timestamptz, ended_utc timestamptz,
  exit_status text,   -- completed | timed_out | failed | budget_hit | cancelled
  round_no int, budget_cap_credits numeric,
  runner_minutes numeric, vcpu_s numeric, gib_s numeric
);

create table fact_usage (
  run_id text, model text,
  input_tok bigint, cached_tok bigint, cache_write_tok bigint, output_tok bigint,
  ai_credits numeric,
  measure_source text,  -- engine_reported | otel | billing_allocated | profile_estimate
  primary key (run_id, model)
);

create table fact_cost_line (             -- FOCUS-shaped
  line_id bigserial primary key,
  charge_date_utc date, project_id text, night_id date,
  run_id text null,                       -- null for shared and fixed costs
  provider text,      -- GitHub | Microsoft | Anthropic | OpenAI | Internal
  category text,      -- ai_tokens | review_agent | ci_minutes | azure_compute | telemetry
                      -- | storage | seats | program_fee | platform | human
  sku_or_meter text, quantity numeric, unit text,
  list_cost numeric, contracted_cost numeric,
  effective_cost numeric, cash_cost numeric,
  credit_applied numeric,                 -- effective_cost minus cash_cost
  currency text default 'USD', fx_to_aud numeric,
  allocation_method text, -- direct | tokens_share | runtime_share | residual_pro_rata | per_night
  status text             -- provisional | reconciled | final
);

create table fact_human_time (
  project_id text, night_id date, task_id text, pr_number int,
  person text, activity text,             -- spec | triage | review | rework | merge | client_demo
  minutes numeric, loaded_rate_aud numeric
);

create table fact_outcome (
  task_id text, feature_id text, pr_number int,
  outcome text,   -- merged_first_pass | merged_after_rework | rejected | abandoned | reverted_30d
  review_rounds int, high_findings int,
  merged_at timestamptz, accepted_by_client_at timestamptz
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
| `list_cost` | Published rate, no discounts. **This is the shadow price.** | AI credits at USD 0.01 each; tokens at the rate table; Azure at retail pay-as-you-go (the FOCUS `ListCost`); seats at list; Actions minutes at USD 0.006 even when included |
| `contracted_cost` | After negotiated or program discounts | Copilot's 10% discount for Auto model selection ([Auto discount](https://raw.githubusercontent.com/github/docs/main/data/reusables/copilot/auto-model-discount.md)); an Azure private offer |
| `effective_cost` | After included allowances and commitments | Included Actions minutes; included Copilot credits |
| `cash_cost` | What Get AI actually pays after partner credits | Zero for credit-funded Mode A lines |

Two rules keep the numbers honest:

- **Treat each Copilot seat as a prepayment of its credits.** An Enterprise seat costs USD 39 and includes 3,900 credits, which is exactly USD 39 at USD 0.01. Business is USD 19 for 1,900 credits ([plan variables](https://raw.githubusercontent.com/github/docs/main/data/variables/copilot.yml)). So post every credit used at USD 0.01. At month end, post unused included credits as "breakage" on the seat holder's cost centre. Never count the seat fee and the included credits both, or you double count.
- **Book partner credits as a funding line, never as a lower cost.** Azure Cost Analysis does not show credits at all; they appear only on the invoice as "Azure credits applied" ([reporting](https://learn.microsoft.com/azure/cost-management-billing/costs/reporting-get-started#invoices-and-credits)). So the ledger posts list, effective and cash on each line, and the matrix shows margin twice: at list and at cash.

### Cadence: provisional tonight, reconciled on day three

- **Nightly (05:41).** Post provisional lines. SDK and Claude Code runs use measured values. Cloud agent and code review runs use a size-class estimate, calibrated from past reconciled nights. Azure compute is runtime multiplied by the list rate. Status is `provisional`.
- **Day 3.** GitHub publishes no billing lag. Copilot metrics land within two full UTC days ([metrics](https://docs.github.com/en/copilot/concepts/billing-and-usage/copilot-usage-metrics/copilot-metrics)). Azure tags take up to 24 hours ([tags](https://learn.microsoft.com/azure/cost-management-billing/costs/understand-cost-mgt-data#how-tags-are-used-in-cost-and-usage-data)). For each `(UTC date, machine account, model)`:
  1. Pull `provider_sum` from the AI credit usage endpoint or `ai_credit` report export ([billing usage](https://docs.github.com/en/billing/tutorials/automate-usage-reporting)).
  2. Subtract `measured_sum`, the SDK runs for that key.
  3. Allocate the residual to the estimated runs (cloud agent, code review) pro rata to their provisional estimates. Mark them `reconciled`.
  4. If the residual is negative, flag measurement drift. GitHub says `totalNanoAiu / 1e9` matches credits only "as a convenience" and to confirm it against billing ([SDK usage](https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/copilot-sdk/features/usage-and-billing.md)).
  Do the same for Actions (per repo and `workflow_path`) and Azure (per tag and meter).
- **Month close.** Compare with the GitHub-on-Azure invoice, including "Azure credits applied". Azure re-rates current-month charges until the invoice closes and adds late usage up to 72 hours after month end ([exports](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-improved-exports)). Mark lines `final`.

One trick helps attribution. If the evaluator uses a different model from the worker (for example a worker on Sonnet 5.5 and an evaluator on GPT-6.1 Sol), the billing row splits the two roles for free. A second model also gives the evaluator an independent reading. This is our inference.

## 7. Yield and review minutes set the margin, not token price

### The formula

Cost per accepted feature = (cost per attempt × attempts per task + human cost per task) ÷ yield.

Fully loaded cost per accepted feature includes, each at list with cash alongside:

1. AI credits or tokens for every run that touched the feature: planner, test author, worker, evaluator, reviewer, failed attempts and retries.
2. Copilot code review credits and its Actions minutes.
3. CI minutes, cloud agent minutes and setup steps.
4. Azure: ACA compute, storage for evidence, Key Vault, Functions, orchestration share.
5. Telemetry ingestion, split by event volume.
6. Seat amortisation: machine account Copilot and GitHub Enterprise seats, breakage, the designation fee.
7. Platform engineering hours on the harness, amortised per accepted feature.
8. Human minutes at a loaded rate: spec, triage, review, rework, merge, client acceptance.
9. Yield adjustment: the cost of that night's rejected and abandoned tasks, spread over its accepted features.
10. A warranty reserve for fixed-price work, sized from the revert-within-30-days rate.

This follows Microsoft's FinOps guidance: unit economics are "a derivative of activity-based costing" and should include "manual processes and steps outside of the cloud" ([unit economics](https://learn.microsoft.com/cloud-computing/finops/framework/quantify/unit-economics)).

### Worked example (model)

Assume an attempt costs USD 5 in tokens, minutes and infra, of which USD 3.50 is tokens. Assume a loaded human rate of USD 100 an hour. Replace that with Get AI's real loaded rate in AUD.

| Scenario | Attempts per task | Human minutes per task | Yield | Cost per accepted feature |
|---|---|---|---|---|
| A: good night | 1.3 | 40 | 80% | (5 × 1.3 + 66.67) ÷ 0.8 = **USD 91** |
| B: poor night | 1.6 | 60 | 50% | (5 × 1.6 + 100) ÷ 0.5 = **USD 216** |
| C: A with token price halved | 1.3 | 40 | 80% | (3.25 × 1.3 + 66.67) ÷ 0.8 = **USD 89** |

Halving the token price saves about 3%. Moving from B to A saves about 58%. The public data points the same way. AI PRs merge within 30 days 32.7% of the time against 84.4% for unassisted PRs, and agent PRs wait 17.6 hours for review against 3.4 hours [snippet] ([LinearB](https://linearb.io/library/engineering-benchmarks-and-research)). Review time rose about 91% on high-adoption teams [secondary] ([Faros summary](https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery)). One feature cost USD 7 to 70 to merge across a dozen models, and the harness alone moved cost about 2.5x [snippet] ([Insight APAC](https://blog.insight-services-apac.dev/2026/07/06/cost-to-a-merged-feature)).

### The matrix

The fact grain is one row per project, night, engine, model and agent role. It rolls up to project by feature and project by month.

**View 1: feature P&L.** One row per accepted feature, grouped by project and night.

| Columns |
|---|
| Runs, rounds, outcome |
| AI credits or tokens at list (all roles) · review agent · Actions minutes · Azure infra · telemetry |
| Seat and fee allocation · platform allocation · human minutes × loaded rate · yield allocation · warranty reserve |
| **Fully loaded at list** · fully loaded at cash · credit subsidy (list minus cash) |
| Revenue (price per feature, or allocated T&M or subscription revenue) |
| **Margin at list** · margin at cash |

**View 2: engine bake-off.** One row per engine, model and harness setting. Columns: tasks (n), first-pass rate, eventual acceptance, rounds, list cost per attempt, list cost per accepted feature at P50 and P80, human minutes per accepted feature, timeout rate, escaped defects at 30 days.

**View 3: night control chart.** One row per night. Columns: tasks dispatched, accepted, cost per accepted at P50, review minutes, credit burn against the night envelope, platform incidents.

**View 4: role cube.** Cost share by planner, test author, worker, evaluator and reviewer. The one public example, Anthropic's DAW build, spent about 91% on the builder, about 8% on QA and under 0.5% on the planner ([Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps)).

**View 5: credit runway.** Remaining partner and included Copilot credits, divided by list burn per night, with expiry dates.

### Leading indicators

Track these nightly. The alert levels are starting assumptions to tune.

- First-pass integration rate. Alert below 60%, the low end of the earlier report's 60 to 80% prior.
- Eventual acceptance rate.
- Rounds per task. Alert above 1.5.
- Timeout rate against the 59-minute cap. Alert above 15%.
- Review minutes and rework minutes per PR.
- PR size in lines changed.
- Evaluator reject rate and its false-reject rate.
- Budget hits: SDK `session_limits_exhausted` events and user-budget blocks.
- Cache read share.
- Cost per accepted feature at P50 and P80, by engine.
- Revert within 30 days.
- Credit runway in nights.

For priors on Copilot specifically: GitHub's own `gh-aw` repo merged 76.3% of 1,000 Copilot PRs, and 80.0% of 1,110 in a later window. Fixes merged at 81.0% and chores at 58.6% ([23 July report](https://github.com/github/gh-aw/discussions/47549); [5 August report](https://github.com/github/gh-aw/discussions/50534)). Academic data shows documentation at 84%, CI at 79%, bug fixes at 64% and performance at 55% [snippet] ([MSR 2026](https://arxiv.org/abs/2601.15195)). One study found 15.4% of merged agent PRs needed reviewer intervention and argues merge rate alone is a weak quality measure [snippet] ([arXiv 2605.22534](https://arxiv.org/pdf/2605.22534)).

### Comparing engines and nights fairly

- **Engines.** Replay the same regression set (20 to 50 tasks drawn from your own past failures) on each engine and model, with the same gate and harness settings. Compare list cost per accepted feature and human minutes per accepted feature. Always show n. Use pass^k when consistency matters, as the earlier report set out.
- **Nights.** Compare within a task size class only. Plot cost per accepted feature at P50 on a control chart. Annotate model releases and harness changes, because either one can move cost 2.5x on its own.

### Pricing from the matrix

- Price floor for a fixed-price feature = P80 fully loaded list cost ÷ (1 minus target gross margin). Use P80, not the mean, because the spread is wide.
- Match the commercial model to scope certainty. Specified backlog items with test oracles suit a fixed price per accepted feature. Discovery suits time and materials, repackaged as a pod day rate. Steady maintenance suits a monthly capacity subscription. Outcome fees suit only outcomes the client can measure. Forrester says three archetypes now coexist and one construct across a portfolio "will misprice most of it" [snippet] ([Forrester](https://www.forrester.com/blogs/for-service-providers-ai-giveth-and-ai-taketh-away/)).
- If a project's margin at list is below target, it is profitable only because of subsidy. Do not renew its price on those terms.

## 8. SPD credits cover about one project at 20 light nights a month

Everything in this section is a model, not a measurement. Calibrate it in stage 2.

### Credit pools

| Pool | Arithmetic | Per month |
|---|---|---|
| Azure bulk credits | 10,000 ÷ 12 | USD 833 |
| Copilot Enterprise via Azure | 5,000 ÷ 12 | USD 417 |
| **Total, one designation** | | **USD 1,250** |
| Each Azure specialisation adds | (12,000 + 4,680 + 2,520) ÷ 12 | USD 1,600 (GitHub parts earmarked) |

Because an Enterprise seat's included credits equal its price, the Copilot benefit buys 41,700 credits a month (417 ÷ 0.01) whether it pays seats or overage. Included pools reset at 00:00 UTC on the 1st, with no carry-over. The promotional 7,000-credit Enterprise allowance ended on 1 September 2026 ([organisation billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing); [snippet] [promotion](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-organizations-and-enterprises)).

### Cost of one session, at Copilot list rates

Assumptions: a **light** session reads 1.5M input tokens with 80% cache hits and writes 30K output, as in the billing research. A **heavy** 40-minute session reads 6.7M cached and 0.67M uncached tokens and writes 0.2M output, scaled from the Azure research's heavy worker-hour. Cache-write charges are excluded.

| Model (USD per 1M: input / cached / output) | Light session | Heavy session |
|---|---|---|
| GPT-6 Luna (0.10 / 0.01 / 0.50) | USD 0.06 | USD 0.23 |
| Claude Sonnet 5.5 or GPT-6.1 Sol (2.00 / 0.10 / 10.00) | USD 1.02 | USD 4.00 |
| GPT-5.3-Codex (1.75 / 0.175 / 14.00) | USD 1.16 | USD 5.13 |
| Claude Opus 5.5 (4.00 / 0.20 / 20.00) | USD 2.04 | USD 8.00 |

Rates come from GitHub's table ([rate table](https://raw.githubusercontent.com/github/docs/main/data/tables/copilot/models-and-pricing.yml)). Light Sonnet arithmetic: 1.2M × 0.10 + 0.3M × 2 + 0.03M × 10 = 0.12 + 0.60 + 0.30 = USD 1.02.

### A sensible default mix, per task

- Worker: 80% of tasks on Sonnet 5.5 or GPT-6.1 Sol, 20% on Opus 5.5. That averages USD 1.22 (light) or USD 4.80 (heavy) per session.
- 1.3 worker sessions per task, because about 30% need one `@copilot` round.
- Evaluator: one run per round at 25% of a Sonnet-class session, so USD 0.255 (light) or USD 1.00 (heavy).
- Copilot code review at Lite: USD 0.25 (light) or USD 1.00 (heavy) per round. GitHub's Lite range is USD 0.05 to 1 per review. Balanced, the default, is USD 0.25 to 5 ([code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review)).
- Chores on GPT-6 Luna: about USD 0.02 per task.

| | Light | Heavy |
|---|---|---|
| Worker | 1.22 × 1.3 = 1.59 | 4.80 × 1.3 = 6.24 |
| Evaluator | 0.255 × 1.3 = 0.33 | 1.00 × 1.3 = 1.30 |
| Code review | 0.25 × 1.3 = 0.33 | 1.00 × 1.3 = 1.30 |
| Chores | 0.02 | 0.02 |
| **Per task** | **USD 2.26** (226 credits) | **USD 8.86** (886 credits) |
| **Per night, 20 tasks** | **USD 45** | **USD 177** |
| **Per month, 20 nights** | **USD 905** | **USD 3,544** |

Totals use unrounded figures. That is lower than the earlier report's USD 150 to 600 a night for four always-busy Claude workers on the API. Copilot sessions are bounded at 59 minutes, and this mix leans on USD 2 / USD 10 models.

Other monthly lines for one project:

- **Actions minutes.** About 1,500 to 1,900 standard minutes a night (agent sessions, fast checks, evaluator, the merge-queue suite, review and orchestration), so 30,000 to 38,000 a month. That fits the 50,000 included minutes on Enterprise only if nothing else uses them ([included usage](https://docs.github.com/en/billing/reference/product-usage-included)). Shadow value at USD 0.006 a minute: USD 180 to 228 ([runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)). Larger runners never use included minutes.
- **Azure base infrastructure.** About USD 50 a month. This is an assumption: Functions, Durable Task Scheduler, storage, Key Vault, under 1 GB of logs at about USD 2.30 per GB [snippet] ([groundcover](https://www.groundcover.com/guides/reduce-log-ingestion-costs)), and a Burstable PostgreSQL server whose price was not retrieved. SDK workers on ACA add about USD 0.20 per worker-hour, using unverified US list rates.
- **Machine account GitHub Enterprise seat.** USD 21, funding unclear (section 2).
- **Designation fee.** USD 406 a month (4,875 ÷ 12), always cash.

### How far the credits go

| Scenario | AI credits at list | Other Azure-billable | Total billable | Credits | Cash spill |
|---|---|---|---|---|---|
| 1 project, light | 905 | 50 | 955 | 1,250 | 0 (USD 295 headroom) |
| 1 project, heavy | 3,544 | 50 | 3,594 | 1,250 | **2,344** |
| 3 projects, light | 2,715 | 70 infra + 244 Actions overage | 3,029 | 1,250 | **1,779** |
| 1 project, light, if general credits cannot pay GitHub meters | 905 | 50 | 955 | 417 for Copilot; 833 for Azure only | **488** |

Three projects use about 90,600 Actions minutes, so 40,600 run over the included 50,000 at USD 0.006. Net of the USD 50 base, the credits fund about **26 light project-nights or 7 heavy project-nights a month** (1,200 ÷ 45 and 1,200 ÷ 177). Seats and the designation fee sit outside these totals.

What spills, and the settings that stop it spilling silently:

- Every credit beyond the included pool is overage at USD 0.01. Paid usage is on by default. Turn off the "AI credits paid usage" policy, or set budgets ([organisation billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing)).
- User-level budgets always hard-stop, and are checked before the pool. Alerts fire at 75%, 90% and 100% ([budgets](https://docs.github.com/en/billing/how-tos/set-up-budgets)). A hard stop halts agents mid-night, so the dispatcher must stop dispatching before the budget does.
- "There is no automatic fallback to lower-cost models when a budget is exhausted" ([organisation billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing)). The dispatcher must switch models itself.
- Code review at Balanced on every PR can cost more than the night's workers. Set Lite.
- Prepaid usage is not available through Azure billing, and credits cannot buy GitHub Pre-Purchase plans ([payment methods](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/supported-payment-methods); [Pre-Purchase plan](https://learn.microsoft.com/azure/cost-management-billing/reservations/github-pre-purchase)).
- If Get AI's developers already hold Copilot seats, their unused pooled credits subsidise the night. The ledger still charges the night at list.

## 9. Claude Code and Codex stay as secondary lanes on the same ledger

Copilot is the engine. Two other engines still earn a lane.

| Lane | Where it runs | Billed to | When it is worth it | How it enters the ledger |
|---|---|---|---|---|
| Codex CLI on Azure OpenAI | ACA job, Australia East | Azure credits (first-party meter) | The only long-running CLI agent that runs wholly on general Azure credits. Use it when a task exceeds 59 minutes and the Copilot pool is spent but Azure credits remain, and for bake-offs. API key only, no Entra; Responses API; validated with gpt-6-astra, gpt-6-sol and gpt-6-luna ([Codex with Azure OpenAI](https://learn.microsoft.com/azure/foundry/openai/how-to/codex)). | `engine = codex-cli`. Tokens from `turn.completed.usage` [snippet], priced from `dim_price`. One Azure OpenAI resource per project, so FOCUS rows split by tag. |
| Claude Code on the Anthropic API | ACA job, or a self-hosted runner on ACA | Anthropic, at cash | You want Claude Code's harness: the validated hook set, `/goal`, and Agent SDK cost fields with `costBasis`. Or a client mandates Anthropic direct. | `engine = claude-code`. `total_cost_usd` and `modelUsage` per run; OTel `api_request` events with the run attributes. Reconcile daily against the Cost API by workspace (one per project, one key per role) ([Usage and Cost API](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)). |
| Claude Code on Microsoft Foundry | ACA job in East US 2 or Sweden Central | Marketplace, at cash | Only when a client mandates Claude on its own Azure contract. Pin model deployments, or the `opus` alias falls back to Opus 4.6 ([Claude Code on Foundry](https://code.claude.com/docs/en/microsoft-foundry)). Request quota before the first night. | As above, but reconcile monthly against the single CCU line. Per-model detail lives only in the Foundry portal ([CCU billing](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-billing)). |
| Agent HQ third-party agents (Claude, Codex) | Inside GitHub, same sandbox and PR flow as the cloud agent | GitHub AI credits by model and tokens, plus Actions minutes | A bake-off lane on low-risk tasks. Still public preview. No steering. Short model lists: the Claude agent offers Sonnet 4.6, Sonnet 5, Opus 4.8, Opus 5 and Fable 5.1, but not Sonnet 5.5 or Opus 5.5 ([third-party agents](https://docs.github.com/en/copilot/concepts/agent-capabilities/about-agents/about-third-party-coding-agents)). The docs do not say whether they honour `.github/hooks`, custom agents or setup steps. | Same as the cloud agent: estimated per run, measured per machine account, model and day. Their hidden GitHub Apps show in the audit log. |
| GitHub Agentic Workflows with a Claude or Codex engine | Actions | The provider, at your own keys | Maintenance agents with read-only tokens and declared `safe-outputs` ([agentic workflows](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows)) | `engine = gh-aw-<engine>`, priced from provider usage |

Two rules apply to every lane. Each one opens PRs through the same rulesets and required workflows, so the gate holds whatever the engine. And each one pushes as the factory App or the project machine account, neither of which sits in a bypass list. That is why Agent HQ agents are safe to trial before hook support is confirmed: the push ruleset and the required workflow are enforced on GitHub's side, not inside the agent.

## 10. Build it in six stages, money first

Each stage has an exit test. Do not start the next stage until it passes.

| Stage | Build | Exit test | Effort |
|---|---|---|---|
| 0. Prove the money and the identity | Send the written credit question. Set up two billing profiles: credited (Mode A) and cash (Mode B). Connect the credited subscription to a test cost centre via "Metered billing via Azure" ([connect Azure](https://docs.github.com/en/billing/how-tos/set-up-payment/connect-azure-sub)). Create one machine account with a Copilot Enterprise seat. Dispatch one task through the tasks API. Turn on CI for Copilot PRs. Check EMU Conditional Access. Set budgets. | A written answer on file. The AI usage report shows the task's credits on the machine account, not on a human. The next invoice shows "Azure credits applied" against GitHub lines. One draft PR whose CI ran unattended. | 2 to 3 days of work; 1 to 3 weeks elapsed for the invoice |
| 1. Gate and locks | `factory-gates` repo: required workflow (fast, evaluator placeholder, full, held-out, hash check). The four rulesets, in Evaluate mode first. CODEOWNERS. Custom agents `grill`, `test-author`, `worker`, `evaluator`. `.github/hooks` deny rules. `copilot-setup-steps.yml` with caching. Gate script. | A seeded cloud-agent edit to `tests/acceptance/` is rejected by the push ruleset. With that ruleset in Evaluate, the hash check fails the PR. The gate script blocks a spec with an open clarification marker. The nightly audit flags a test bypass entry. | 1 to 2 weeks |
| 2. One project, one night, Actions only | Kickoff, dispatch, tick and report workflows. Night plan schema. Morning package to Teams and Blob. Ledger v0: `fact_run`, provisional estimates, nightly evidence export. | Three nights produce draft PRs and a morning card with nobody awake. Timeout rate and credits per task known from reconciled billing rows. | 1 to 2 weeks |
| 3. Independent verification | Evaluator job (SDK, `evaluator` agent, Playwright) as a required check. Copilot code review at Lite. The `@copilot` loop, two rounds at most. Held-out suite in `factory-gates`. | The evaluator catches a seeded defect that passes the acceptance tests. False-reject rate recorded. Review severity counted from comment text. | 1 to 2 weeks |
| 4. Parallel work, serial integration, full ledger | In-flight cap of 4 to 6. Disjoint-file check. Merge queue on `integration`. App marks ready and enqueues. Morning promotion PR. Day-3 reconciliation. Power BI matrix v1 with list and cash. | One night of at least 15 tasks with conflicts resolved by re-dispatch. Reconciliation variance under 10% per grain key (an assumed tolerance). The matrix shows cost per accepted feature at list and at cash. | 2 weeks |
| 5. Second project and Azure workers | Second machine account, cost centre and resource group. ACA job running a Copilot SDK worker with `maxAiCredits` for long tasks. Durable Functions only if a section 5 trigger applies. Codex lane for a bake-off. | Two projects in one night with clean per-project rows. SDK `getMetrics` totals match billing within tolerance. A 20-task bake-off on two engines. | 2 to 3 weeks |
| 6. Keep healthy and package | Regression set of 20 to 50 tasks with pass^k tracking. Maintenance automations. Re-simplify on each model release: remove one component, measure, keep or restore. Package the accelerator (section 12). | 30 days of escaped-defect data. Human minutes per accepted PR falling. The accelerator deploys into a clean tenant in one day. | Ongoing |

Start stage 0 now. Charges for a calendar month reach the Azure invoice at the start of the next month ([Copilot Azure billing](https://docs.github.com/en/copilot/reference/copilot-billing/azure-billing)), so the invoice test cannot be rushed.

## 11. The risks, most serious first

| # | Risk | Why it matters | Mitigation |
|---|---|---|---|
| 1 | Credits may not fund client delivery | Microsoft calls them "internal-use-rights credits" ([credits FAQ](https://learn.microsoft.com/partner-center/benefits/mpn-benefits-azure-cloud#azure-credits-faqs-legacy-experience)). Pricing client work on credits could breach program terms. | The written ruling. Two modes split at the billing boundary. Price at list. |
| 2 | Credit mechanics fail | Unsupported subscription types; GitHub Enterprise seats possibly not covered ([payment methods](https://docs.github.com/en/enterprise-cloud@latest/billing/reference/supported-payment-methods)) | Stage 0 invoice test on an MCA subscription |
| 3 | Credits expire or are revoked | Yearly; expiry moves to the offer purchase date from 1 November 2026; revoked on cancellation ([August announcements](https://learn.microsoft.com/partner-center/announcements/2026-august)) | Steady burn through the year; runway view |
| 4 | Preview features change | Tasks API, issue assignment API, session limits, third-party agents and the unattributed-Copilot approval rule are preview; `getMetrics` is experimental | A nightly canary task; issue assignment as a fallback dispatch path; re-check after Universe |
| 5 | Cost attribution lands on the wrong identity | GitHub does not state who pays for API-assigned sessions or code review on them | Stage 0 test; a nightly check that no human login shows night-time credits |
| 6 | Silent overage or a mid-night hard stop | Paid usage is on by default; budgets hard-stop | Dispatcher envelope below the budget; Lite review; model switching in the dispatcher |
| 7 | Auto-run workflows on Copilot PRs open a security hole | GitHub's own warning ([agent settings](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings)) | Required workflows only; no secrets on PR jobs; Actions policies |
| 8 | Bypass list drift | One Copilot bypass entry on `main` undoes the gate | Nightly ruleset audit fails the kickoff |
| 9 | Firewall gaps | It ignores MCP servers and setup steps ([firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall)) | Push ruleset on `.github/**`; few MCP servers |
| 10 | Platform incidents and schedule drift | Late or dropped schedules; runner incidents; the Copilot rate-limit stall | Idempotent tick; one lost hour budgeted; graceful morning report; optional ACA runners |
| 11 | Evidence loss | Retention now deletes checks and runs; session logs have no API | Nightly export to Blob; audit log stream |
| 12 | Claude in Foundry traps | Cash only, US or Sweden only, 40 RPM default ([Claude quotas](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/claude-models-quotas-limits)) | Use Claude through Copilot in Mode A |
| 13 | Client data rules | The notes do not establish where Copilot inference runs | Check per client; Azure OpenAI in Australia East where residency is required |
| 14 | Quality decay in an agent-built codebase | The earlier report's warnings on lights-off factories still apply | A human reads the morning package; escaped defects tracked for 30 days |
| 15 | Price and FX drift | Model prices change; costs are in USD and prices in AUD | Nightly `models.list` snapshot into `dim_price`; FX column; a buffer in fixed prices |

## 12. The factory and its ledger become the deployment accelerator

Keep this practical. Four things become IP:

- **The `factory-gates` template.** Required workflows, ruleset JSON, hooks, custom agents, setup steps and the night plan schema. Any client repo can adopt it by setting one custom property.
- **The Azure side as Bicep or azd.** ACA jobs, the ledger Function, storage, Application Insights, Key Vault and the OIDC wiring.
- **The ledger.** The schema, the reconciliation Function and the Power BI matrix. This is the piece that turns the factory into a pricing tool.
- **The grill gate.** The `grill` and `test-author` agents plus the gate script.

What it proves: after a quarter of nights you will have cost per accepted feature at P50 and P80 at list, first-pass rate, review minutes and escaped defects. That is production track record and auditable unit economics, which a board or a buyer can check. It is the kind of asset Get AI's board strategy values over billable hours.

Two practical levers on the Microsoft side. The "Agentic DevOps with Microsoft Azure and GitHub" specialisation fits this work exactly and adds its own credits [snippet] ([specialisation page](https://partner.microsoft.com/en-US/partnership/specialization/agenticdevops-microsoftazure-github)). Cloud Accelerate Factory gives partners with that specialisation Microsoft-led deployment help ([July 2026 announcements](https://learn.microsoft.com/partner-center/announcements/2026-july#cloud-accelerate-factory-expands)). A fixed-scope Marketplace consulting offer is the natural package.

One hygiene rule: build the accelerator in Mode A, keep client code and data out of it, and record which mode funded each run in the ledger. That keeps the IP clean if anyone later asks who paid for it.

## Conclusion

The credits make the first months nearly free. They say nothing about price. The ledger's list column is what keeps Get AI's pricing honest once credits expire or turn out to be internal-only. That is why the ledger matters more than the choice of agent.

The matrix also changes where to spend engineering effort. Token price barely moves cost per accepted feature. Yield and review minutes do. So the main cost levers are the evaluator's evidence and the morning package, not cheaper models: every minute the morning reviewer saves by trusting the evidence is worth more than a model downgrade. And the one question that could change the whole funding model is a contract clause, not a technical limit. Ask it this week.

## Would video transcripts help?

Yes, but only a few, and the most useful ones do not exist yet. Microsoft's credit terms are the biggest open question, and no talk will settle them. That needs the written ruling in section 2.

**Worth getting, ranked:**

| Rank | Session | What it would settle |
|---|---|---|
| 1 | GitHub Universe 2026 (28 to 29 October 2026) sessions on the Copilot cloud agent and Agent HQ | Whether the tasks API goes GA; concurrency limits; whether API-assigned sessions bill to the assigning account; any session-log export API or retention period; whether third-party agents honour hooks and custom agents; any change to the 59-minute cap. These are the biggest gaps in the agent research. |
| 2 | Universe 2026 sessions on Copilot billing, AI credits and enterprise admin | A per-session credit export; the billing data lag; how GitHub meters appear in Azure Cost Management; any change to included credits or Azure billing for partners. |
| 3 | Universe 2026 sessions on the Copilot SDK | Whether `getMetrics` leaves experimental status; caller-chosen session ids; whether SDK cloud sessions share the 59-minute cap; OpenTelemetry conventions for tokens and credits. |
| 4 | "Open Source Friday: Spec Kit Part 2" (16 October 2026, Spec Kit 1.0) ([video](https://www.youtube.com/watch?v=8hHCpNVLhmI)) | How Spec Kit 1.0 runs with Copilot agents, and whether `clarify` and `implement` can run unattended. This affects only the daytime gate tooling. |
| 5 | FinOps X 2026 day 1 keynote [secondary] ([recap](https://www.nops.io/blog/finops-x-2026-day-1-keynote/)) | The "nine distinct layers" of AI cost, as a cross-check on the ledger's cost categories. Minor. |

GitHub announced Agent HQ at Universe 2025 [snippet] ([announcement](https://github.blog/news-insights/company-news/welcome-home-agents/)), so expect the 2026 event to carry the next round of agent and billing changes. Those transcripts will likely be the highest-value input once they are posted. Re-check sections 4, 6 and 8 against them.

**Little value, because primary sources already confirm the mechanism:**

- "Build Agents That Run for Hours" (Prabaker and Wilson) [snippet] ([recap](https://digg.com/ai/wtakhm1b)). The planner, generator and evaluator shape is confirmed by Anthropic's March 2026 post and the Code with Claude repo. A transcript would only settle the conflicting run-length claims.
- Lopopolo's harness engineering talk [snippet] ([talk page](https://ai.engineer/talks/harness-engineering)). His own published corpus is the primary source for every mechanism used.
- Brennan's OpenHands talk [snippet] ([talk page](https://ai.engineer/talks/software-development-agents-what-works-and-what-doesn-t)). OpenHands' own blog states its current position.
- Herrera, "Your agents should be durable" (Temporal) ([notes](https://summify.io/discover/ai-dev-26-x-sf-melissa-herrera-your-agents-should-be-durable-T-E5YF/)). This plan uses Durable Functions, whose limits come from Microsoft's docs.
- The video summary of "The Verification Horizon". Read the paper instead.
- "Open Source Friday with Spec Kit" part 1 (8 May 2026) ([video](https://www.youtube.com/watch?v=2IArMAhkJcE)). Part 2 supersedes it.

One non-video source is worth pasting in if you can open it: Insight APAC's "Token Price Is the Wrong Number" post [snippet] ([blog](https://blog.insight-services-apac.dev/2026/07/06/cost-to-a-merged-feature)). Its per-model table would give the engine bake-off a real external benchmark.
