# Copilot and Azure primitives checked against the workshop harness

Checked on 24 to 25 October 2026 against the GitHub Docs source (github/docs, main, read from a local clone) and Microsoft Learn. URLs below are the published docs.github.com pages that correspond to each source file.

## Support matrix (Copilot customisation cheat sheet)
Source: https://docs.github.com/en/copilot/reference/customization-cheat-sheet

| Feature | VS Code | Visual Studio | JetBrains | GitHub.com (cloud agent) | Copilot CLI |
|---|---|---|---|---|---|
| Custom instructions | yes | yes | preview | yes | yes |
| Custom agents | yes | yes | preview | yes | yes |
| Subagents | yes | no | preview | **no** | yes |
| Agent skills | yes | yes | preview | yes | yes |
| Hooks | preview | no | no | yes | yes |
| MCP servers | yes | yes | yes | yes | yes |

- Skills locations: `.github/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md` (project), plus `~/.copilot/skills/` and `~/.agents/skills/` (personal). So one rubric skill can serve both Copilot and Claude Code.
- Subagents are "a separate agent spawned by the main agent to handle delegated work in an isolated context".
- Conflict to flag: the matrix says subagents are not supported on GitHub.com, but the custom agents configuration reference lists an `agent` tool alias ("Allows a different custom agent to be invoked to accomplish a task") and the hooks reference says `subagentStart` and `subagentStop` fire under the cloud agent. Treat cloud agent subagents as partial and do not depend on them. Sources: https://docs.github.com/en/copilot/reference/custom-agents-configuration and https://docs.github.com/en/copilot/reference/hooks-reference
- VS Code custom agent `handoffs` and `argument-hint` are ignored by the cloud agent (custom agents configuration reference). VS Code handoffs are useful by day only.
- Custom agents can pin `model` and `tools`; profiles are versioned by commit SHA, and PR follow-ups use the same version as the task that created the PR (custom agents configuration reference). Use this to record evaluator version.

## Playwright MCP
- The cloud agent ships two out-of-the-box MCP servers: `github` (read-only by default) and `playwright` (localhost only). The app must boot inside the session (via `copilot-setup-steps.yml`). Source: custom agents configuration reference (see copilot_coding_agent_and_agent_hq.md line on out-of-the-box MCP servers).
- The cloud agent firewall does not cover MCP server processes or setup steps (customize-the-firewall page, in the Copilot agent notes).
- CLI and SDK sessions add Playwright MCP through normal MCP configuration.

## Auto mode equivalent: none
Source: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools
- Copilot CLI has no classifier-based approval mode. Controls are: `--available-tools` and `--excluded-tools` (what the model can see), `--allow-tool` and `--deny-tool` with patterns such as `shell(git:*)` and `shell(git push)`, and permissive `--allow-all-tools`, `--allow-all` or `--yolo`. Deny rules always beat allow rules, even with `--allow-all`.
- In non-interactive mode, any action not pre-approved is denied automatically (autopilot docs, in the Copilot agent notes).
- GitHub's own caution: use allow-all only in an isolated environment; consider local or cloud sandboxing first.
- Cloud agent: all tools pre-approved inside the sandbox; `permissionRequest` hooks have no effect; use `preToolUse` to deny (hooks reference).

## CLI local sandboxing
Source: https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/understanding-local-sandboxing
- Deny-by-default filesystem policy. Shell commands, built-in searches and local MCP and LSP processes run as sandboxed child processes, enforced by the operating system. Built-in file read and edit tools check the same policy in software only, with no OS backstop. Remote MCP servers are not constrained by the filesystem policy.
- Working directory read/write by default; whole git repo readable; writes limited to the working directory and `.git`. Enterprise admins can lock settings.

## Autopilot and /goal
Source: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
- `/autopilot [OBJECTIVE]` and `/goal [OBJECTIVE]` start or refocus autopilot mode. Autopilot keeps working until the model calls `task_complete` (self-declared done). There is no separate judge model, unlike Claude Code's `/goal`. So the `agentStop` hook and an external evaluator are still needed.
- `--max-autopilot-continues`, `--max-ai-credits` (soft, per response), `--plan --mode autopilot` (plan then run with no approval), `--resume`, `--session-id`, `--worktree`, `--no-ask-user`.

## Dynamic workflows (public preview)
Sources: https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/dynamic-workflows and https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-dynamic-workflows
- "A program that defines how a task is carried out", combining deterministic steps with one or more agents, sequential or parallel. Can pass results between stages, "have subagents verify each other's findings", ask agents for results in a set format, pause at a checkpoint for review and resume.
- Defined in Copilot extensions (session, personal or project). Run from chat, or headless with `copilot workflow run WORKFLOW-NAME --args '<json>'`, which waits for completion and suits CI. Permission prompts are not shown in `workflow run`, so grant permissions up front.
- Limits such as an AI credit limit per run are optional but recommended. Runs can be paused, cancelled, or resumed after hitting a limit, reusing saved results from completed steps. Cancelled runs cannot resume.
- With OpenTelemetry on, each run or resume creates an `invoke_workflow` span with agent activity linked.
- Available in Copilot CLI (needs `--experimental`), the GitHub Copilot app and the SDK; all plans except Copilot Pro tiers. `/workflows` needs a token-based billing plan.
- Fits the planner, generator and evaluator loop, and chained generator and critic pairs. Preview, so keep a fallback.

## OpenTelemetry from Copilot CLI and SDK (ledger and trace reading)
Sources: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#opentelemetry-monitoring, https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry, https://docs.github.com/en/copilot/how-tos/copilot-sdk/observability/opentelemetry
- Enable with `COPILOT_OTEL_ENABLED=true` or by setting `OTEL_EXPORTER_OTLP_ENDPOINT`; file exporter via `COPILOT_OTEL_FILE_EXPORTER_PATH` (JSON lines). `OTEL_RESOURCE_ATTRIBUTES` adds custom resource attributes (for example project, run_id, task_id, lane, role).
- Span tree per agent interaction: `invoke_agent` root, with `chat` (one per LLM request) and `execute_tool` children. Top-level sessions and subagent invocations both emit `invoke_agent`.
- `invoke_agent` attributes include: `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.version`, `gen_ai.conversation.id` (session id), `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_creation.input_tokens`, `github.copilot.turn_count`, `github.copilot.cost` (a billing multiplier, "Not a monetary value"), `github.copilot.nano_aiu` (AI units in nano units, 1 AIU = 1e9 nano AIU), `error.type`.
- Content capture (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`, or enterprise capture classes for prompts, responses, tool arguments, tool output) adds full messages, system instructions and tool definitions. Off by default; may contain source code and secrets.
- Enterprise managed settings can enforce OTel config across clients. Supported clients: Copilot CLI, the GitHub Copilot app, VS Code, and the SDK. The cloud agent is not listed.
- GitHub's docs point to a Microsoft guide for Azure: "Monitor AI coding agents with Grafana" using Azure Managed Grafana and Application Insights: https://learn.microsoft.com/en-gb/azure/managed-grafana/grafana-opentelemetry-app-insights
- Ledger implication: for CLI and SDK lanes, cost per agent role per task becomes measured (`nano_aiu` per `invoke_agent` span, keyed by `gen_ai.agent.name` and resource attributes). The ledger research maps `totalNanoAiu / 1e9` to AI credits; confirm the unit mapping against billing in stage 0. The cloud agent lane stays estimated.

## Compaction and hooks
- SDK `infiniteSessions` with `backgroundCompactionThreshold` for long runs; session state lives in `~/.copilot/session-state/<sessionId>/` (events.jsonl), which must be on shared storage to resume elsewhere (SDK scaling page, in the Copilot agent notes).
- `preCompact` hook fires before compaction (notification only, output not processed, but the command runs). `sessionStart` and `postToolUse` can inject additional context. `subagentStart` can prepend context to every subagent's first message. `agentStop` with `decision: "block"` forces another turn. Subagent scoped stop blocks are ignored after eight in a row (hooks reference).

## Azure Container Apps jobs (Lane A runtime)
Sources: https://learn.microsoft.com/azure/container-apps/jobs#advanced-job-configuration and the Azure Verified Modules job module README https://github.com/Azure/bicep-registry-modules/blob/main/avm/res/app/job/README.md
- `replicaTimeout` is "the maximum number of seconds a replica is allowed to run". No maximum value is documented on the pages read. The AVM module default is 1,800 seconds, so it must be set explicitly for multi-hour runs.
- Microsoft: "Platform maintenance, including routine security updates and upgrades, might interrupt long-running job replicas. Set the replica retry limit to at least 1, and design your workload for at-least-once processing so that retries can safely complete the work."
- Implication: the long generator session must be resumable. Keep Copilot session state and the working tree on Azure Files or commit to the task branch often; on retry, resume the session by id and re-read the handoff files. Test the longest replicaTimeout the subscription accepts in stage 0.
