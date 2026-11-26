# Spike 0.6: Copilot CLI on GHE.com

Plan section 11.1, row 0.6 (ADO 2451). Session 55, Thursday 26 November 2026, laptop track C, a day after its Wed 25 Nov date. Spike 0.14's run 39346986 had already shown that Copilot CLI 1.0.113 runs on a `getai.ghe.com` runner with the job's own `GITHUB_TOKEN` and `copilot-requests: write` (`docs/plans/spike-0.14/README.md`). This spike answers the rest: which model answered and where it was billed, OpenTelemetry, custom agents laid out as the gate lays them out, and `--max-ai-credits`.

**Result: the exit test passes, measured in a collector in the job. Application Insights waits on Azure access**, as ADO 3060 does: Boroon has no role on the CSP subscription that can make the resource (checked 26 November 2026). One executor run, with a custom agent and the night's flags, was measured by OpenTelemetry under its `project`, `story_id`, `run_id` and `role`, and billed to the organisation `GetAI-IP`, repository `copilot-probe`, model Claude Sonnet 5.5. The bill, the CLI's usage file and the OpenTelemetry spans agree to six decimal places.

**The billing identity: the job's own token, Boroon's pick on 26 November 2026** (below). A machine account is not tried.

## Exit test (plan 11.1)

| Item | Result |
|---|---|
| One executor run | Run 41333481: `copilot -p` with `--agent probe-executor` (a custom agent in the repo's `.github/agents/`, laid out as `lcp-executor`), `--autopilot`, `--max-autopilot-continues 5`, `--max-ai-credits 60`, `--no-ask-user`, allow and deny rules, `--secret-env-vars GITHUB_TOKEN`, `--output-format json`, `--share`, `--disable-builtin-mcps`. It wrote its handoff file and ended with `task_complete`, exit 0, 5.8 s, 3 model calls, 2.568 credits |
| Measured | **In a collector in the job** (`probe/otlp_sink.py`, OTLP/HTTP JSON on `127.0.0.1:4318`): one `invoke_agent probe-executor` span (`gen_ai.agent.name` `probe-executor`, `github.copilot.agent.type` `custom`) over three `chat claude-sonnet-5.5` spans and three `execute_tool` spans, with the resource attributes `project=probe`, `story_id=2451`, `run_id=probe-20261126-2451-41333481-1`, `lane=B`, `profile=lcp`, `role=executor`. `github.copilot.nano_aiu` on the root span is 2,568,070,000, the same as `--usage-output-file`. **Application Insights is not tried**: it waits on access to the CSP subscription (as 3060) |
| Billed to the intended identity | Yes: `GetAI-IP`, repository `copilot-probe`, "Copilot AI Credits", model "Claude Sonnet 5.5", USD 0.01 a credit, no discount (`GET /organizations/GetAI-IP/settings/billing/ai_credit/usage`, and `.../billing/usage` for the repository). It was on the bill within a minute of the run |

## What ADO 2451 asked, answered

| Question | Answer |
|---|---|
| Org billing policy | On for `GetAI-IP` (spike 0.14, run 39346986) and still on. All five orgs have the CLI turned on (`GET /orgs/<org>/copilot/billing`: `cli: enabled`); only `AI-Business-Solutions` has seats (3). GitHub's docs: the policy "Allow use of Copilot CLI billed to the organization" is on by default where the CLI is on |
| `copilot-requests: write` | Works with the job's own `GITHUB_TOKEN`, `GH_HOST=getai.ghe.com`, no seat, no secret, on CLI 1.0.113 (spike 0.14) and 1.0.114, the gate's pin (this spike) |
| Which model answered | With no `--model`: **Claude Sonnet 5.5** on the runner (1.0.113 on 18 November and 1.0.114 now). The bill names the model per day. `--model auto` chose GPT-6 Luna for a one-word prompt, billed as "Fusion (Standard): GPT-6 Luna". An agent file's `model:` sets the model, and `--model` beats it (findings 6 and 7) |
| Where it was billed | The organisation that owns the repository the job runs in, by day, repository and model. Spike 0.14's two days are there too: 18 November 5.38755 and 21 November 84.5554 credits, repository `export-probe`, all Claude Sonnet 5.5; the 21 November figure equals that day's usage files (part 4 47.30, part 4b 16.77 and 20.49) |
| OpenTelemetry export | Works to a file and to OTLP/HTTP JSON. **Setting only `COPILOT_OTEL_ENABLED=true`, as `lcp-gate.yml` does today, sends to `http://localhost:4318`; with nothing listening the run still exits 0 and every span is lost**, with one warning in the process log only (finding 9) |
| Custom agents from the gate repo | With the gate's layout (the repo checked out at `gate/`, `working-directory: gate`), `--agent <name>` finds `gate/.github/agents/<name>.agent.md` with no trust flag. The agent's `tools:` list limits the tools: an agent without `shell` cannot run any command, whatever `--allow-tool` says (findings 4 to 8) |
| `--max-ai-credits` | Minimum 30. A soft cap: warnings at 50%, 75% and 90%; at 90% the tools are turned off; the session ends with `session.error` `ai_credit_soft_cap_exhausted` and exit 1, slightly over the cap (30.40 of 30). The agent cannot write a handoff after 90% (finding 11) |
| Billing identity | The job's own token (option 1 in plan 5.2), Boroon's pick on 26 November 2026 (below) |

## Method

A private scratch repo, `GetAI-IP/copilot-probe`, made for this session and deleted at its end. One workflow, `probe.yml` (copy here), started by hand with a `mode` input. Every case is one tiny `copilot -p` call with the job's own `GITHUB_TOKEN` (`copilot-requests: write`): no tenant, no OIDC, no secrets. Copilot CLI is **the gate's pin**: `tools/copilot/package.json` and `package-lock.json` copied from `GetAI-IP/factory-gates` at `release` `5ba13be` (1.0.114, ten packages with their integrity values), installed the gate's way, `npm ci --ignore-scripts`. `factory-gates` was read in a separate clone and not changed.

- `probe/case.py` runs one case with a fresh `COPILOT_HOME` (no saved trust, agents or sessions from another case), its own `--usage-output-file` and `--log-dir`, and JSON output, and writes a summary (`case.json`) of the events, the usage file and any telemetry.
- `probe/otlp_sink.py` is the collector in the job: a standard-library OTLP/HTTP receiver on `127.0.0.1` that writes each POST to a JSON line. The copy here also reads chunked and gzipped bodies, added for spike 0.20 on the laptop (VS Code's Copilot Chat exporter sends chunked bodies); the runs in this spike used the first version, which Copilot CLI's exporter did not need.
- `probe/scrub.py` removes token-shaped strings from every file before upload. It found none in any run.
- `agents/` holds the three agent files: `probe-evaluator` (`tools: ["read"]`, `model:` set by the run), `probe-shell` (`tools: ["read", "shell"]`, no model) and `probe-executor` (`model: claude-sonnet-5.5`, `tools: ["read", "edit", "search", "shell"]`).

Before the first run, the three scripts were checked on the laptop against a stand-in `copilot` (no Copilot call): the sink got a span with its resource attributes, and the scrubber removed a planted token from both files that held it.

The bill was read with Boroon's own `gh` sign-in on `getai.ghe.com` (read only): `GET /organizations/<org>/settings/billing/usage`, `.../usage/summary`, `.../ai_credit/usage` (by model, with `day=`), and `GET /enterprises/GetAI/settings/billing/usage`. The enterprise has no cost centres (`GET /enterprises/GetAI/settings/billing/cost-centers`: none).

## Findings

**The model and the bill**

1. **The bill names the organisation, the repository and the model, by day, at USD 0.01 a credit, within a minute.** `.../billing/usage` gives one "Copilot AI Credits" row per organisation, repository and day; `.../billing/ai_credit/usage` gives the same credits by model (`model`, `grossQuantity`, `discountQuantity`, `netQuantity`). `GetAI-IP` has no seats, so nothing is included: every credit is paid usage (`discountQuantity` 0). Today's 81.768446 credits over 9 runs and 26 cases equal the sum of the cases' usage files to six decimal places, model by model (Claude Sonnet 5.5 81.18519; GPT-6 Luna 0.472057; Fusion GPT-6 Luna 0.1111985), and the last run was on the bill a minute after it ended. Plan 10.1 says billing reports "by day and identity, never by run, story or PR": it is by day, organisation, repository and model, and still never by run, story or PR.
2. **With no `--model`, the runner's default is Claude Sonnet 5.5.** `session.model_change` at startup says so, and the bill names it, on 1.0.113 (18 November) and 1.0.114 (today). On the laptop the default can differ: the gate's review fixture (23 November, Boroon's own sign-in, no `--model`) ran on `mai-code-2-flash` through Auto. The default follows the account, so a factory session should never rely on it.
3. **`--model auto` picked GPT-6 Luna** for a one-word prompt (`session.auto_mode_resolved`: "Copilot Fusion selected GPT-6 Luna since the task has low complexity"), 0.11 credits against Sonnet's 5.39. The bill shows it as "Fusion (Standard): GPT-6 Luna", separate from GPT-6 Luna asked for by name, and with no discount line (plan 10.3 cites a 10% Auto discount; none shows here, so it may be in the price, not a discount). **A bad model name** fails at once, at no cost: `session.error` "Model ... is not available", exit 1.

**Custom agents** (runs 41301741 and 41334566, the same results both times)

4. **The gate's layout works with no trust flag.** With the repo checked out at `gate/` and the session in `gate/`, `--agent no-such-agent` fails with "No such agent: no-such-agent, available: probe-evaluator, probe-executor, probe-shell", and `--agent probe-evaluator` loads `gate/.github/agents/probe-evaluator.agent.md`. `--trust-folder` changed nothing (it covers workspace MCP servers and hooks, the CLI's help says).
5. **An agent's `tools:` list limits the session's tools, whatever `--allow-tool` says.** `probe-evaluator` (`tools: ["read"]`) did not get the shell with `--allow-tool 'shell(echo:*)'`: it answered "shell: no". `probe-shell` (`tools: ["read", "shell"]`) ran `echo`. **So plan C.2's `lcp-evaluator` (`tools: ["read", "search", "playwright/*"]`) could not run `lcp-verify`, `cat` or `ls`**, which the gate's verifier step allows with `--allow-tool`. The `skill` tool stayed: `probe-evaluator` loaded a skill that ships inside the CLI, `customize-cloud-agent`.
6. **An agent's `model:` replaces the session's default model.** `probe-evaluator` with `model: gpt-6-luna` ran on GPT-6 Luna; `probe-shell`, with none, on Claude Sonnet 5.5.
7. **`--model` on the command line beats the agent's `model:`.** With `--agent probe-evaluator --model claude-sonnet-5.5`, the agent loaded (its marker), its tool limit held, and the model was Claude Sonnet 5.5.
8. **Which copy of an agent wins**, for one name in three places:
   - a copy in `$COPILOT_HOME/agents/` beats the repo's `.github/agents/` copy (the home copy's marker came back);
   - the working folder's `.github/agents/` copy beats one in a folder added with `--add-dir` (the gate's marker, not the PR's);
   - `GetAI-IP` has no `.github-private` repo, so no organisation agents exist to load. The CLI has a setting, `customAgents.defaultLocalOnly`, to use local agents only [untested].

   So a driver that puts the trusted agent files in a fresh `COPILOT_HOME/agents/` is sure they win over any copy in the checkout.

**OpenTelemetry** (run 41304176; 41302666 stopped early, the probe's own fault)

9. **`COPILOT_OTEL_ENABLED=true` alone exports OTLP/HTTP JSON to `http://localhost:4318`.** The sink on 4318 got `/v1/traces` and `/v1/metrics` with nothing else set. With nothing listening, the run exits 0, prints nothing, and loses everything: the only sign is one `[WARNING] [rust:otel] OTel provider shutdown failed ... HTTP export failed: network error` in the process log. `lcp-gate.yml` sets only `COPILOT_OTEL_ENABLED: "true"` in `verify-in-test` and `danger`, so **every gate session's telemetry is lost today**.
10. **What arrives**, from the file exporter (`COPILOT_OTEL_FILE_EXPORTER_PATH`, one JSON line per span or metric) and OTLP alike:
    - resource attributes: everything in `OTEL_RESOURCE_ATTRIBUTES` (`project`, `story_id`, `run_id`, `lane`, `profile`, `role`), with `service.name`, `service.version` (1.0.114) and, over OTLP, `service.instance.id`;
    - one root `invoke_agent` span per session: `gen_ai.agent.name` and `github.copilot.agent.type` (`custom` with `--agent`, `builtin` without), input and output tokens, `github.copilot.turn_count`, `github.copilot.cost` (premium-request units, not money) and `github.copilot.nano_aiu`;
    - one `chat <model>` span per model call: `gen_ai.request.model` (`claude-sonnet-5.5`), `gen_ai.response.model` (`claude-sonnet-5-5`), input, output, cache-read and cache-write tokens, and `github.copilot.nano_aiu`;
    - `execute_tool <tool>` spans with the tool's name and exit code, no arguments; and a `permission` span for each refusal, with `github.copilot.permission.result` (`denied-no-approval-rule-and-could-not-request-from-user`);
    - 19 metrics, among them the token counters by kind.

    **The root span's `nano_aiu` is the sum of its `chat` spans'**, and equals the usage file's `totalNanoAiu` exactly, in every case. Sum one level, never both. Subagents were not tried (spike 0.7). No prompt text is in any span (content capture is off by default).

**`--max-ai-credits`** (runs 41304926 and 41306186)

11. **A soft cap that ends the session with exit 1.** Below 30 it is refused before any call ("Use at least 30 AI credits"). With a cap of 30 on a task needing more:
    - the session gets `session.info` at 50%, 75% and 90% ("Session limits: 27.34/30 AI credits used. If this session continues, the next model call is final; tools will be disabled."), and each tool result carries the budget ("[cost: 89% used · $0.03 left]");
    - **at 90% the tools are off**: the agent could not make more files, nor any handoff file;
    - autopilot then sent five "You have not yet marked the task as complete" turns, text only, which spent the last 10% (5 premium requests in all);
    - the session ended with `session.warning` and `session.error` `errorType: session_limits`, `errorCode: ai_credit_soft_cap_exhausted`, "Session limit reached (30.4/30 AI credits used)", **exit 1**, 30.40 credits (1.3% over), 30 of 40 files made;
    - the model's last answer said plainly that the task was not finished and what was left.

    So the driver must read that error code, write the PARK `budget` itself, and keep the last answer as the handoff; and the usable budget is 90% of the cap.

**Other**

12. **Prompt caching crosses sessions.** A one-word prompt cost 5.39 credits on a cold cache (21,555 tokens written) and a two-call prompt 2.25 credits minutes later (its first call read 14,399 cached tokens written by an earlier session in the same job). A run's cost depends on what ran just before it, so compare stories by their totals over many runs, not one run each.
13. **In `-p`, a command no rule allows is refused, and the write tool makes no folders.** The first exit-test run (41332621) asked for `handoff/2451/state.md`: `mkdir` was refused (no rule), `create` said the parent folder did not exist, and the agent stopped with "Blocked: ... state.md was not written". The driver should make `handoff/<ado-id>/` before the session (run 41333481 did).
14. **The built-in GitHub MCP server starts with the job's token** (5 tools) unless `--disable-builtin-mcps` is passed. The gate's verifier and review steps do not pass it.
15. **`actions/setup-node` with `node-version: lts/*` failed on a GHE.com runner** (run 41331761): it reads Node's version list from github.com without signing in, and the runner's shared address was over github.com's rate limit ("API rate limit exceeded for" the runner's address). `22.x` comes from the runner's own cache with no lookup. `lcp-gate.yml` uses `lts/*` in `verify-in-test` and `danger`, so a gate run can fail the same way.
16. **No token-shaped string** in any job log, artifact or `--share` transcript (the scrubber found none in 9 runs). With `--secret-env-vars GITHUB_TOKEN` the executor still worked: the CLI keeps its own copy.

## The billing identity: the job's own token (Boroon, 26 November 2026)

**Proposed, and picked by Boroon: option 1 of plan 5.2, the job's own `GITHUB_TOKEN` with `permissions: copilot-requests: write`**, billed to the organisation that owns the repository the job runs in.

- **Why:** it works (spikes 0.14 and 0.6); it needs no seat, no secret and no personal token, so no Conditional Access problem; the bill names the organisation, repository and model each day and matches the CLI's own count to six decimal places; user budgets do not apply (GitHub's docs).
- **Option 2, a seated machine account per project, is not tried.** It needs a seat and a personal token per project, and GitHub's docs say a personal token on EMU with Conditional Access "will likely be blocked".
- **What follows for Mode A and Mode B (plan 9.2)** [inference, from GitHub's docs, untested here]: a cost centre can hold repositories (and users, organisations and enterprise teams), can be tied to its own Azure subscription, and can carry a budget that stops usage ("Stop usage when budget limit is reached", off by default). So each client's cost centre holds that client's repositories, tied to the cash subscription. **This only splits by client if every Copilot session for a client runs in a repository in that client's cost centre.** The gate's sessions do: the required workflow runs in the project repository (to be confirmed by 2539's first real run). The night execution job, planned in one `factory-control`, does not: all its usage would land on `factory-control`. So the execution workflow should run in, or be called from, a repository inside each client's cost centre (for example a reusable execution workflow called from the project repository, as the gate is).
- **Not tried:** a budget that stops an organisation's or cost centre's Copilot usage (creating one changes billing settings, Boroon's call); whether `AI-Business-Solutions`' 3 seats' included credits absorb gate usage there.

**Boroon's pick (26 November 2026, asked in Session 55): the job token**, option 1 above, with client splits by cost centres made of repositories. Not yet in the plan: the edits below wait on his word.

## Proposed plan edits (not made; for Boroon)

1. **11.1, row 0.6:** the result: passed in a collector in the job, billed to `GetAI-IP` per repository and model, matching to six decimals; Application Insights waits on Azure access (3060).
2. **5.2, "Billing identity":** the pick, and the finding that the bill names organisation, repository and model; for client work, the execution workflow runs in a repository in the client's cost centre.
3. **5.2, the engine bullets:** always pass `--model` (the default follows the account); pass `--disable-builtin-mcps` in every session; put the trusted agent files in a fresh `COPILOT_HOME/agents/` (they win over the checkout's); the driver makes `handoff/<ado-id>/`; `--max-ai-credits` turns tools off at 90% and ends with exit 1 and `ai_credit_soft_cap_exhausted`, which the driver maps to PARK `budget` (5.11), keeping the last answer.
4. **5.2 and 10.1, telemetry:** never `COPILOT_OTEL_ENABLED=true` alone. Until Application Insights exists, `COPILOT_OTEL_FILE_EXPORTER_PATH=evidence/otel-<role>.jsonl`, so the spans travel in the evidence bundle to Blob (rule 16) and a trusted loader takes them in; later an OTLP endpoint with its auth header. Sum `nano_aiu` from the root `invoke_agent` span or from the `chat` spans, never both.
5. **10.1:** "Billing reports by day and identity" becomes "by day, organisation, repository and model"; reconciliation can run per (UTC date, organisation, repository, model), and the bill appears within minutes, not two days (the two-day note in 10.3 is for Copilot metrics, not the bill).
6. **10.3:** no Auto discount line was seen on 26 November ("Fusion (Standard)" is billed with `discountQuantity` 0); check before `contracted_cost` counts one.
7. **Appendix C.2, `lcp-evaluator`:** add `shell` to `tools:`, so `lcp-verify` can run; the command rules stay in `--allow-tool` and `--deny-tool`.
8. **Appendix A, `verify-in-test` and `danger`:** the telemetry exporter (edit 4), `--disable-builtin-mcps`, `--model`, and `node-version: 22.x` (or an exact version) instead of `lts/*`. These touch `factory-gates`, so they go there by its own pull request (Session 53 owns `factory-gates` today).
9. **15.1:** close "Which Copilot features work on GHE.com, and which billing identity for the CLI?" for the CLI, keeping code review and the cloud agent open.

## For the gate (not changed here)

For whoever next changes `lcp-gate.yml` (2539, 3027), from findings 5, 9, 14 and 15: the verifier and review sessions' telemetry is lost today; their agent files, when written, need `shell` in `tools:` for the evaluator; neither step passes `--disable-builtin-mcps` or `--model`; and `setup-node` with `lts/*` can fail on github.com's rate limit.

## Runs

Started with `GH_HOST=getai.ghe.com gh workflow run probe.yml -R GetAI-IP/copilot-probe --ref main -f mode=<mode>`. Credits are the cases' usage files; the bill for 26 November matched their sum.

| Run | Mode | Result | Credits |
|---|---|---|---|
| 41300916 | model | Default Claude Sonnet 5.5 ("ready", 5.39); bad name refused at no cost; `auto` chose GPT-6 Luna (0.11); `--max-ai-credits 29` refused | 5.50 |
| 41301741 | agents (`agent_model=gpt-6-luna`) | Agents found from `gate/`; `tools:` limits; `model:` applies; home beats repo, repo beats `--add-dir` | 3.11 |
| 41302666 | otel | Cases 1 to 3 ran; the step then stopped (the probe's `wait` on the killed sink returned 143 under `bash -e`) | 6.76 |
| 41304176 | otel | All four cases: file, enabled only (to `localhost:4318`), explicit endpoint, nothing listening (exit 0, data lost) | 9.01 |
| 41304926 | credits (12 files) | Finished under the cap of 30, warm cache | 14.99 |
| 41306186 | credits (40 files) | Cap reached: tools off at 90%, exit 1, `ai_credit_soft_cap_exhausted`, 30 of 40 files | 30.40 |
| 41331761 | executor | Failed before Copilot: `setup-node` `lts/*` hit github.com's rate limit | 0 |
| 41332621 | executor | Ran; `mkdir` refused (no rule), handoff not written, agent stopped and said why | 4.50 |
| 41333481 | executor | **The exit test: passed**; handoff written; measured in the sink; billed to `GetAI-IP` / `copilot-probe` | 2.57 |
| 41334566 | agents | As 41301741, plus `--model` beats the agent's `model:` | 4.93 |

**The spike's cost: 81.77 AI credits, about USD 0.82 at list**, all paid usage on `GetAI-IP`. Actions: 11 Linux minutes on the bill by the last read (each job rounded up to the minute; the Actions minutes were discounted to nil, like the rest of `GetAI-IP`'s).

## Left to do

1. ~~**Boroon:** pick the billing identity~~: the job token (26 November 2026). **Boroon:** the plan edits.
2. **Application Insights**, when the CSP subscription's owner gives access (with 3060): one executor run with an OTLP endpoint and its auth header, or the file exporter's spans loaded by a trusted step. Until then the exit test stands on the collector in the job.
3. Not tried, could follow: a budget that stops Copilot usage at the organisation or a cost centre; a subagent's spans (does the parent's `nano_aiu` include them? spike 0.7); `customAgents.defaultLocalOnly`; whether included seat credits absorb usage in `AI-Business-Solutions`.

## Scratch

| Thing | Where | State |
|---|---|---|
| The repo `GetAI-IP/copilot-probe` (private), with `probe.yml`, the scripts, the agents, the copied lockfile, its runs and their artifacts (3-day retention) | `getai.ghe.com` | Made 26 November 2026; **deleted at the end of Session 55, 26 November 2026, about 04:50 UTC**, as Boroon allowed in the session's brief, after every file was checked against its copy here (all identical; the collector here is the later, fixed one). Read back: `gh repo view` cannot resolve it and `GET /repos/GetAI-IP/copilot-probe` answers 404 |

Nothing was made in any tenant, no credential, no secret, and nothing in `factory-gates`. The copies here are the only record of the probe; the lockfile is `factory-gates`' `tools/copilot/` at `release` `5ba13be`.
