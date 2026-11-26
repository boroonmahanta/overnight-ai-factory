# Spike 0.20: time and tokens on each story, every engine

Plan section 11.1, row 0.20 (ADO 2738). Session 55, Thursday 26 November 2026, laptop track C, a day before its Fri 27 Nov date, after spike 0.6 in the same session (`docs/plans/spike-0.6/README.md`). The story worked was 2738 itself, on the branch `claude/session-55-2738-time-tokens`.

**Result: the exit test passes for every engine but one, and its tolerance needs a correction.**
- **Landed in one place:** Claude Code (terminal CLI, desktop app, VS Code extension), Copilot CLI by day and a night run. One collector on the laptop, merged with the night runner's collector file, and `story_report.py` totals them per story.
- **Labels kept:** the terminal CLI, the VS Code extension and Copilot carried `story_id` from `OTEL_RESOURCE_ATTRIBUTES`.
- **Labels dropped:** the desktop app drops `OTEL_RESOURCE_ATTRIBUTES`. Its sessions join their story through the session's git branch in the local transcript, and every one of them landed on its right story that way.
- **Tokens:** Claude Code's main-loop calls equal `tools/session_usage.py` exactly. Telemetry also counts the app's own side calls, which transcripts never hold, so it reads 0.9% to 7.9% above the tool.
- **The one engine:** VS Code Copilot Chat sent metrics but no token spans in this test (inconclusive).
- **Not tried:** Application Insights, which waits on Azure access, as in spike 0.6 and ADO 3060.

## Exit test (plan 11.1)

| Session that touched story 2738 | Engine | In the one place? | Under its story ID? | Tokens against `session_usage.py` |
|---|---|---|---|---|
| `0bb86652`, `claude -p` in this worktree | Claude Code CLI 2.1.217 (`service.name` `claude-code`, `app.entrypoint` `sdk-cli`) | Yes | Yes, by attribute (`story_id=2738`) and by branch | Transcript 60,696; telemetry 61,232 (+0.9%): a 536-token Haiku side call the transcript does not hold |
| `0c75395b`, one prompt in the Claude Code panel in VS Code, in this worktree | Claude Code VS Code extension, CLI 2.1.332 (`claude-code`, `claude-vscode`) | Yes | Yes, by attribute and by branch | Transcript 68,114; telemetry 69,302 (+1.7%): a Haiku 5.5 side call |
| `b0282934`, a desktop-app session started for this test | Claude Code desktop, CLI 2.1.330 (`claude-code-desktop`, `claude-desktop`) | Yes | **No attribute** (dropped); by branch only, and the app started it on `main` in the main folder, not in this worktree, so it is rightly "unattributed" | Equal: 113,051 both |
| `e43a6f1c` and `c37e1a8c`, two `copilot -p` prompts by day | Copilot CLI on the laptop, Boroon's sign-in (`github-copilot`; 1.0.114, then 1.0.116: it updated itself between the two) | Yes | Yes, by attribute | Not a Claude Code transcript; OTel equals the CLI's usage file (0.139 and 0.332 credits) |
| Two prompts in VS Code Copilot Chat, agent mode, by Boroon | Copilot Chat extension 0.66.0 (`copilot-chat`) | **Metrics only**: one metric, no spans, no token counts | No: its resource holds no `story_id` (VS Code was not started from a shell with the variable) | None to compare |
| Run 41342356, the night leg | Copilot CLI 1.0.114 on a `getai.ghe.com` runner, `probe-executor` agent | Yes (its in-job collector's file, merged) | Yes, by attribute | OTel equals the usage file (4.283 credits); on the bill too: `GetAI-IP`'s total for 26 November, 86.051066 credits, equals every case's usage file with this one |
| `afa29cde`, this session (the story's own work) | Claude Code desktop | **No**: it started before telemetry was turned on, and a running process does not pick the setting up | By branch, from the transcript tool only | The transcript tool alone (the fallback) |

Two sessions that did not touch the story came in as well, because they resumed while the setting was on. **Both landed under their own stories by branch:** `a84c1108` (Session 57, 2739) and `f634c578` (Session 53, 3027). A static `story_id` in the settings would have put both under 2738.

Over 10 minutes of the 2739 session, the telemetry read 12,452,805 tokens and the transcript 11,543,588 (+7.9%). The difference is exactly two calls the app made itself, `query_source` `prompt_suggestion` and `side_question`, each re-reading the whole context (about 454,000 tokens). Without them the two are equal.

The per-story totals from `story_report.py`:
- 2738: 11 model calls, 245,689 tokens processed, 4.754 Copilot AI credits, and USD 0.74 by Claude Code's own estimate (Boroon's plan is Max, so not billed by the token).
- 2739: 19.6 million tokens.
- 3027: 0.48 million tokens.
- Unattributed: the test session only.

## How it was run

Boroon's choices, asked in this session (26 November 2026):
- Claude Code's telemetry by an `env` block in his user settings, for the test only. Claude Code's docs say project and local settings files are ignored for these variables.
- Copilot CLI on the laptop under his own sign-in, on two tiny prompts.
- VS Code Copilot Chat by his own hand.
- One tiny desktop session, started from this session.

1. **A collector on the laptop:** spike 0.6's `probe/otlp_sink.py` on `127.0.0.1:4318`, writing every OTLP/HTTP JSON post to one file in the session scratchpad. Nothing left the laptop. Partway through, the collector learned to read chunked and gzipped bodies. VS Code's Copilot Chat exporter sends chunked bodies, and the first version saved ten of its posts as empty, among them its only traces post.
2. **Claude Code's telemetry on** in `~/.claude/settings.json`, from 04:06 to 04:45 UTC. The file was backed up first; it had no `env` block. Afterwards the backup was restored and checked byte for byte (the same SHA-256). The block:

   ```json
   "env": {
     "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
     "OTEL_METRICS_EXPORTER": "otlp",
     "OTEL_LOGS_EXPORTER": "otlp",
     "OTEL_EXPORTER_OTLP_PROTOCOL": "http/json",
     "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:4318",
     "OTEL_METRIC_EXPORT_INTERVAL": "10000",
     "OTEL_LOGS_EXPORT_INTERVAL": "5000",
     "OTEL_METRICS_INCLUDE_ENTRYPOINT": "true",
     "OTEL_METRICS_INCLUDE_VERSION": "true",
     "OTEL_METRICS_INCLUDE_REPOSITORY": "true",
     "OTEL_RESOURCE_ATTRIBUTES": "project=factory,story_id=2738"
   }
   ```
3. **The desktop app:** a top-level session, "51. Stage 1 - Spike - Desktop telemetry check (2738)", started with a one-word prompt, Sonnet 5.5, effort low.
4. **The terminal CLI:** one `claude -p "Reply with the single word: ready" --model claude-sonnet-5-5` in this worktree, in a clean environment (`env -i`), so it read the user settings and none of the desktop app's own variables.
5. **Copilot CLI by day:** two `copilot -p` prompts in this worktree. They ran with `--no-custom-instructions` so the planning repo's `CLAUDE.md` was not sent, and with `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL=http/json` and `OTEL_RESOURCE_ATTRIBUTES=project=factory,story_id=2738,role=day,engine=copilot-cli`.
6. **VS Code**, by Boroon, in this worktree's folder:
   - in his user settings, `"github.copilot.chat.otel.enabled": true` and `"github.copilot.chat.otel.otlpEndpoint": "http://127.0.0.1:4318"`, then Reload Window;
   - `Reply with the single word: ready` in Copilot Chat (agent mode) and in the Claude Code panel, twice in all, once before the collector's fix and once after;
   - afterwards the two settings were taken out again.
7. **The night leg:** spike 0.6's `probe.yml` in `GetAI-IP/copilot-probe`, mode `executor` (the exit-test mode), with `story_id=2738`. Its in-job collector's file was downloaded and merged with the laptop's.
8. **One place:** the laptop's file and the night's file put together, then `story_report.py` (here), run over all local transcripts. It totals model calls and tokens per story, engine and session. It takes the story from `story_id`, or for Claude Code from the session's git branch in its transcript. It counts Copilot's and Claude Code's tokens the same way.

## Findings

**Claude Code**

1. **The desktop app and the VS Code extension both export** the same metrics and events as the CLI:
   - metrics: `claude_code.token.usage` by `type` and `model`, `claude_code.cost.usage`, `claude_code.active_time.total`, `claude_code.session.count` (with `start_type`);
   - one `claude_code.api_request` event per model call, with its four token counts and `cost_usd`;
   - the desktop app as `service.name` `claude-code-desktop`, `app.entrypoint` `claude-desktop`;
   - the VS Code extension as `claude-code`, `claude-vscode`.

   This answers the plan's open question for both (15.1).
2. **The desktop app drops `OTEL_RESOURCE_ATTRIBUTES`; the CLI and the VS Code extension keep them.**
   - In desktop sessions, neither `project` nor `story_id` reached the resource or the data points. Their resource held the app's own keys instead (`claude.deployment_mode`, `process.owner`, `host.arch`, `os.*`).
   - The CLI (2.1.217) and the VS Code extension (2.1.330 and 2.1.332), reading the same user settings, carried both.
   - The desktop app also starts every session with `CLAUDE_CODE_ENABLE_TELEMETRY=1` and no exporter of its own (seen in this session's environment), so a session sends nothing until an exporter is set.
3. **The branch is not in the telemetry; the repository is.**
   - `OTEL_METRICS_INCLUDE_REPOSITORY=true` adds `vcs.provider.name`, `vcs.owner.name`, `vcs.repository.name` and `vcs.repository.url.full`, but no branch.
   - So a day session's story comes from joining its `session.id` to the transcript's `gitBranch`, which `tools/session_usage.py` already records.
   - That join put every session in this test under its right story: 2738, 2739 and 3027.
4. **A setting in user settings reaches sessions as they start or resume**, not sessions already running.
   - This session never exported. The 2739 and 3027 sessions, started before the change, exported from the moment they resumed (`start_type` `resume`).
   - So a setting turned on for a window catches whatever resumes in that window. To catch every session it must be on before they start: managed settings, always on.
5. **Telemetry counts more than the transcript does.**
   - The main loop's calls (`query_source` `main`) equal the transcript's usage to the token.
   - On top come calls the app makes for itself, which transcripts never hold: Haiku side calls (536 tokens on the CLI, 1,188 on the VS Code extension), and prompt suggestions and side questions. Each of those re-reads the context; together they came to 909,217 tokens over 10 minutes of the 2739 session.
   - So `tools/session_usage.py` is a floor: 0.9% to 7.9% low here, and more in long sessions with many side questions.
6. **Personal data on every point.** `user.email`, `user.account_uuid`, `user.account_id`, `user.id` and `organization.id` come with every metric and event by default, and some cannot be turned off. That is fine for an internal Application Insights, but worth a redaction choice before anything leaves GET AI (spike 0.15).
7. **The bundled system prompt is large.** A one-word prompt in this planning repo cost:
   - 113,045 cache-write tokens on the desktop app;
   - 68,114 tokens on the VS Code extension (45,941 written to the cache, 22,167 read from it);
   - 60,690 on the CLI.

   The app adds its own tools and connectors.

**Copilot**

8. **Copilot CLI by day exports the same as at night**, with `OTEL_RESOURCE_ATTRIBUTES` kept (`story_id=2738`, `role=day`). Its OTel equals its usage file.
9. **The laptop's default model is Auto, and Auto chose `mai-code-2-flash`** for both day prompts. Plan 9.3 says MAI-Code-2 is on neither residency list, so a day session with no model set can break a T2 client's rule. The runner's default (no `--model`) was Claude Sonnet 5.5 (spike 0.6, finding 2).
10. **The laptop's Copilot CLI updated itself between two prompts** (1.0.114 to 1.0.116). With no `COPILOT_AUTO_UPDATE=false` on a laptop, day sessions run whatever version the CLI last fetched, unlike the pinned night.
11. **VS Code Copilot Chat (0.66.0) sent metrics but no spans after the collector's fix.**
    - Its only metric was `copilot_chat.cloud.error.count`, with `operation` `fetchSessionList` and `error.type` `http_404`: it could not list cloud sessions, likely on `getai.ghe.com` [inference].
    - Its resource held only `service.name`, `service.version` and a `session.id`, with no `story_id`.
    - VS Code's docs say chat and `invoke_agent` spans carry `gen_ai.usage.*` with only these two settings, and give no export interval.
    - One traces post did come before the fix, and was lost as an empty chunked body. None came after it, though Boroon's agent-mode prompt was answered.
    - So whether its token spans reach a collector is **not shown** [untested further]. VS Code reads `OTEL_RESOURCE_ATTRIBUTES` only from its own environment, so a story label would have to be set when VS Code starts.
12. **Copilot's input count includes the cache; Claude Code's does not.** Copilot's `gen_ai.usage.input_tokens` is uncached input plus cache reads plus cache writes; Claude Code's `input_tokens` is uncached input only. `story_report.py` subtracts, so both add up the way `session_usage.py` counts.

**The one place**

13. **The join works across engines**: one file, one report, every row with its story, engine and session. With Application Insights the same rows would be one Kusto query keyed by `story_id` [untested].

## What this means for the plan

- **Day sessions need managed settings, always on, not a window.** Telemetry set in user settings misses every session already running (finding 4). Managed settings (`/Library/Application Support/ClaudeCode/managed-settings.json` on macOS, or the MDM domain `com.anthropic.claudecode`) is what the plan already says (10.1). This spike shows why it must be always on.
- **The story key for Claude Code is the branch, joined from the transcript**, not `OTEL_RESOURCE_ATTRIBUTES`. The desktop app drops the label, and a static value in settings would tag every session with one story; it would have put 2739's and 3027's sessions under 2738.
- **The transcript tool is a floor** (finding 5). Keep it as the fallback, but compare on main-loop calls, or accept that telemetry reads higher.
- **VS Code Copilot Chat stays on estimates** until its token spans are seen reaching a collector (finding 11).

## Proposed plan edits (not made; for Boroon)

1. **11.1, row 0.20:** the result, and a new wording for the exit test's tolerance: "the main-loop token totals match `tools/session_usage.py` within 5%; telemetry also counts side calls the transcripts do not hold".
2. **10.1, "Engines with OpenTelemetry send it":**
   - the desktop app (`claude-code-desktop`) and the VS Code extension (`claude-vscode`) export;
   - the desktop app drops `OTEL_RESOURCE_ATTRIBUTES`, so the story comes from joining `session.id` to the transcript's branch;
   - telemetry must be on in managed settings before sessions start;
   - it counts side calls (prompt suggestions, side questions, Haiku calls), so it reads above the transcript tool;
   - VS Code Copilot Chat's token spans are not yet shown.
3. **10.1, "The story key":** Claude Code's telemetry carries the repository (`OTEL_METRICS_INCLUDE_REPOSITORY`) but not the branch. The join is by `session.id`.
4. **10.2, `fact_usage`:** a `query_source` column (`main`, `prompt_suggestion`, `side_question` and so on), so the baseline page can show main-loop work and overhead apart.
5. **9.3 or 9.4:** day sessions pin a model too. The laptop's Copilot CLI default is Auto, which chose MAI-Code-2-Flash, on neither residency list. And laptops set `COPILOT_AUTO_UPDATE=false` if day sessions are to match the night's version.
6. **15.1:** close "Do the Claude Code VS Code extension and desktop app export OpenTelemetry as the CLI does, and does Copilot in VS Code?": both Claude Code ones yes, the desktop app without its labels; Copilot Chat in VS Code not shown.
7. **Section 12 or spike 0.15:** Claude Code's telemetry carries the user's email and account IDs on every point.

## Left to do

1. **Application Insights**, when the CSP subscription's owner gives access (with 3060 and spike 0.6): the same report as a query there.
2. **Managed settings on the laptop**, always on, when Boroon chooses (it needs his admin rights). Then every Claude Code session exports from its start, this kind of session included.
3. **VS Code Copilot Chat, once more:** with `github.copilot.chat.otel.exporterType` `file` and `github.copilot.chat.otel.outfile`, to see whether it writes token spans at all, apart from any network question.
4. **Boroon:** the plan edits.

## Files here

- `story_report.py`: the report. Standard library only. It prints counts and names, never prompt text or account details.
- The collector is spike 0.6's `probe/otlp_sink.py`, now reading chunked and gzipped bodies. The night leg is spike 0.6's `probe.yml`, mode `executor`.

The collected files stay in the session scratchpad. They hold the user's email and account IDs (finding 6), so they are not copied into this public repo.
