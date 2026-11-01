# Anthropic's published engineering work on harnesses for long-running autonomous coding agents (as of 24 October 2026)

Provenance key used throughout: **[Anthropic]** = primary Anthropic source (engineering blog, research post, Claude Code docs, or an `anthropics/` GitHub repo). **[Third party]** = summary or commentary by someone else. **[Search snippet only]** = the page could not be fetched from this environment (DNS blocked), so the claim rests on a search-result summary and is unverified.

Sources read in full (primary):
- "Effective harnesses for long-running agents", Anthropic Engineering, 26 Nov 2025. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- "Harness design for long-running application development", Anthropic Engineering, 24 Mar 2026. Fetched at https://www.anthropic.com/research/harness-design-long-running-apps (the engineering index links the same slug; note the slug is `harness-design-long-running-apps`, not the long title).
- "Building a C compiler with a team of parallel Claudes", Nicholas Carlini, Anthropic Engineering, 5 Feb 2026. https://www.anthropic.com/engineering/building-c-compiler
- `anthropics/claude-quickstarts/autonomous-coding` (sample harness for the Nov 2025 post). https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding, with raw prompts at https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/initializer_prompt.md and .../coding_prompt.md
- `anthropics/claudes-c-compiler` (output of the Feb 2026 run). https://github.com/anthropics/claudes-c-compiler and https://github.com/anthropics/claudes-c-compiler/tree/main/current_tasks
- `anthropics/cwc-long-running-agents` (Code with Claude 2026 take-home for the Long-Running Agents station). https://github.com/anthropics/cwc-long-running-agents, with raw files at https://raw.githubusercontent.com/anthropics/cwc-long-running-agents/main/README.md, .../claude-code-config/.claude/CLAUDE.md, .../claude-code-config/.claude/agents/evaluator.md
- Claude Code docs: "Keep Claude working toward a goal" (/goal). https://code.claude.com/docs/en/goal
- Claude Code docs: "Orchestrate teams of Claude Code sessions" (agent teams). https://code.claude.com/docs/en/agent-teams
- Claude Code docs: "Manage costs effectively". https://code.claude.com/docs/en/costs
- "Measuring AI agent autonomy in practice", Anthropic, 18 Feb 2026. https://www.anthropic.com/research/measuring-agent-autonomy
- "Scaling Managed Agents: Decoupling the brain from the hands", Anthropic Engineering, 8 Apr 2026. https://www.anthropic.com/research/managed-agents
- "Redesigning source control at Anthropic", Nick G. and the source control team, Anthropic Engineering, 13 Oct 2026 (updated 15 Oct). https://www.anthropic.com/research/redesigning-source-control
- Anthropic engineering index (for dates and slugs). https://www.anthropic.com/engineering

Not fetchable from this environment (DNS refused): the workshop recording and every recap page for it, Simon Willison's blog, InfoQ, daily.dev, digg, podwise, sozai, intentlayer, aibuilderclub, sean-weldon.com. Workshop findings below are therefore search-snippet only.

---

## Key question 1: What exact loop structure does each article recommend (one session per feature? fresh context per task? how is state handed over)?

### Takeaway
Anthropic's recommendation evolved across three generations. Nov 2025: an outer loop over many fresh-context sessions, one "initializer" session then N "coding" sessions, each doing exactly one feature and handing over through files plus git. Mar 2026: a planner, generator and evaluator with sprint contracts and full context resets (V1 on Sonnet 4.5 and Opus 4.5), then simplified on Opus 4.6 to one continuous generator session with auto-compaction, a planner up front, and a single evaluator pass at the end (V2). Feb 2026 (C compiler): a dumb bash `while` loop that re-launches `claude -p` with the same prompt file as soon as the previous session exits, 16 of these in parallel against a shared bare git repo.

### Cited Findings

**Nov 2025 "Effective harnesses" [Anthropic]**
- The harness runs the Claude Agent SDK in a loop across many context windows; each session starts with no memory of earlier sessions, and compaction alone was not enough for multi-session work. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Two agent roles, "initializer" and "coding", differ only in their initial user prompt; system prompt, tools and harness are identical. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- The initializer runs once (session 1) and produces `init.sh`, `claude-progress.txt`, an initial git commit, and the feature list JSON (over 200 features for the claude.ai-clone example). [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Every later session follows a fixed sequence: get oriented (`pwd`, read git log and progress file, read feature list, pick the highest-priority unfinished feature); start the environment (`init.sh`, then a basic end-to-end check such as starting a chat, sending a message, receiving a response, to catch bugs left by the previous session); work on one feature; leave a clean state (descriptive git commit plus progress-file update, code that "could be merged to a main branch"). [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- "The team found that restricting each session to a single feature was critical." [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- A typical session opens with tool calls `pwd`, read `claude-progress.txt`, read `feature_list.json`, `git log --oneline -20`, start the server. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Sample code: the `autonomous-coding` quickstart. In that repo the entry point is `autonomous_agent_demo.py` (flags `--project-dir`, `--max-iterations`, `--model`, default model `claude-sonnet-4-5-20250929`), with `agent.py` (session logic), `client.py` (SDK client), `security.py` (bash allowlist `ALLOWED_COMMANDS`), `progress.py`, `prompts.py`, `prompts/app_spec.txt`, `prompts/initializer_prompt.md`, `prompts/coding_prompt.md`. The loop auto-continues after a 3-second delay; Ctrl+C pauses and re-running the same command resumes; `--max-iterations` caps iterations (unlimited by default). [Source](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- Bash allowlist in the quickstart: `ls cat head tail wc grep npm node git ps lsof sleep pkill` (dev processes only); file operations limited to the project directory; OS-level sandbox. [Source](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
- Expected timings from the quickstart README: first session takes several minutes with no visible output; each coding iteration takes about 5 to 15 minutes; a full 200-feature build "takes many hours". [Source](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)

**Mar 2026 "Harness design" V1 (Sonnet 4.5, Opus 4.5) [Anthropic]**
- Three roles. Planner: expands a 1 to 4 sentence prompt into a full product spec, told to be ambitious on scope, avoid granular technical detail, and weave in AI features; given the frontend-design skill to create a visual design language. Generator: works in sprints, one feature at a time, stack React + Vite + FastAPI + SQLite (later PostgreSQL), self-evaluates at sprint end, has git, hands off to QA. Evaluator: uses Playwright MCP to click through the running app, testing UI, API endpoints and database state. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Sprint contracts: before each sprint the generator and evaluator negotiate what "done" means and how it will be verified; communication is file-based (one agent writes a file, the other reads and replies). Sprint 3 alone had 27 contract criteria for the level editor. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Context handling in V1: Sonnet 4.5 showed strong "context anxiety" (wrapping up work prematurely as the window fills), so the harness used full context resets with structured handoffs rather than compaction; compaction "doesn't give the agent a clean slate". The article does not name the handoff files. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Loop built on the Claude Agent SDK. In the frontend-only experiment, the generator produced HTML/CSS/JS, the evaluator used Playwright MCP to navigate the live page, screenshot it, score each criterion and write a critique; 5 to 15 iterations per generation, runs up to four hours; after each evaluation the generator chose to refine or pivot. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

**Mar 2026 "Harness design" V2 (Opus 4.6) [Anthropic]**
- Removed the sprint construct and per-sprint evaluation; the evaluator moved to a single pass at the end. Kept the planner ("without it, the generator under-scoped") and the evaluator ("worth the cost when the task sits beyond what the current model does reliably solo"). [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Context resets dropped entirely: Opus 4.5 "largely removed that behavior on its own"; agents ran as one continuous session with automatic compaction handling context growth. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Added prompting so the generator builds AI agents that drive the app's own functionality through tools. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Method for simplifying: remove components one at a time and measure the impact; an earlier attempt to cut radically failed to match performance. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Actual DAW run shape under V2: Planner, then three Build/QA rounds (Build R1, QA R1, Build R2, QA R2, Build R3, QA R3). [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

**Feb 2026 C compiler [Anthropic]**
- Each agent runs in a bash loop invoking `claude --dangerously-skip-permissions -p "$(cat AGENT_PROMPT.md)"`, with logs written to `agent_logs/agent_${COMMIT}.log` where `${COMMIT}` is the short commit hash. The loop starts a new session as soon as one finishes. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- The agent prompt asks Claude to break problems into small pieces, track its work, choose the next task, and "keep going until it's perfect". [Source](https://www.anthropic.com/engineering/building-c-compiler)
- No orchestration agent and no inter-agent communication other than git; agents chose their own work, usually "the next most obvious" problem. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- A human wrote test cases Claude was told to pass but "never interactively pair-programmed with Claude to debug or to provide feedback on code quality" (repo README, the one human-written paragraph). [Source](https://github.com/anthropics/claudes-c-compiler)

**Code with Claude 2026 take-home (`cwc-long-running-agents`) [Anthropic]**
- Headless wrapper loop from the README (paraphrased from the fetched page, structure preserved):
  ```bash
  while grep -q '"passes": false' test-results.json; do
    claude -p "Read PROGRESS.md and build the next unfinished feature per CLAUDE.md."
    VERDICT=$(claude --agent evaluator -p "Review the most recent commit against its spec.")
    [ "$(echo "$VERDICT" | head -1)" = "PASS" ] || echo "$VERDICT" > NEXT_FINDINGS.md
  done
  ```
  Each pass starts a fresh context. Suggested exit conditions: nothing left failing, a cycle makes no changes, or a budget is hit; `touch AGENT_STOP` stops early. The sample script implements only the first condition. [Source](https://github.com/anthropics/cwc-long-running-agents)
- Alternative in-product loop: `/goal every feature in PROGRESS.md is implemented, committed, and its tests pass`. [Source](https://github.com/anthropics/cwc-long-running-agents)
- Third alternative: a `Stop` hook in Claude Code, or `PreToolUse`/`Stop` callbacks in the Agent SDK, which "translate one-to-one" from the shell hooks. [Source](https://github.com/anthropics/cwc-long-running-agents)
- "Going further" patterns listed but not shipped: unattended loop (cap session length, outer script starts the next session); planner agent (first session expands a one-line ask into `BUILD_PLAN.md`); sprint contracts; grading rubrics; browser-verified evaluator; re-simplify on model upgrades; hosted runtime. [Source](https://github.com/anthropics/cwc-long-running-agents)

**Claude Code `/goal` (docs, current) [Anthropic]**
- `/goal` is "a wrapper around a session-scoped prompt-based Stop hook". After each turn Claude Code sends the condition and the conversation so far to the configured small fast model, which returns Not yet met (Claude keeps working and takes the reason as guidance), Met (goal cleared, achieved entry recorded), or Impossible (goal cleared, failed entry recorded). [Source](https://code.claude.com/docs/en/goal)
- Runs non-interactively: `claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"` runs the loop to completion in one invocation; add `--output-format stream-json --verbose` to see progress. [Source](https://code.claude.com/docs/en/goal)
- Loop guard: if Claude keeps answering the evaluator without tool use for several turns in a row, Claude Code stops the loop, prints a warning and returns control with the goal still set. [Source](https://code.claude.com/docs/en/goal)
- Bounding: include a clause such as `or stop after 20 turns` in the condition; conditions up to 4,000 characters. [Source](https://code.claude.com/docs/en/goal)
- Comparison table: `/goal` (next turn when previous finishes; stops on Met/Impossible/unrecoverable error/`/goal clear`), `/loop` (time interval), Stop hook (your own script or prompt decides). Auto mode "approves tool calls within a single turn but doesn't start a new one"; `/goal` and auto mode are "complementary". [Source](https://code.claude.com/docs/en/goal)
- Resume: an active goal is restored on every resume route, with turn count, timer and token baseline reset. [Source](https://code.claude.com/docs/en/goal)

**Workshop "Build Agents That Run for Hours" [Search snippet only, third party]**
- Roughly 75-minute AI Engineer talk by Anthropic's Ash Prabaker and Andrew Wilson; YouTube id `mR-WAvEPRwE`; proposed architecture planner, generator, evaluator; "before building, the generator and evaluator negotiate testable sprint contracts"; takeaways include "using file-system state for long-running agents". No official Anthropic page was found for it. [Source (search result summary, pages unreachable)](https://digg.com/ai/wtakhm1b); recap pages at https://daily.dev/posts/build-agents-that-run-for-hours-without-losing-the-plot-ash-prabaker-andrew-wilson-anthropic-n3dvnyjtj and https://sozai.app/transcript/anthropic-workshop-build-long-running-agents/ (both unreachable from here).

### Inferences
- The three Anthropic designs converge on the same skeleton for an overnight run: a one-off planning/initialising step that writes a machine-readable checklist, then a loop whose unit of work is one feature, then a verification step that is separate from the worker. What changed between Nov 2025 and Mar 2026 is only how often the context is thrown away (every feature, then every sprint, then never) and how often the evaluator runs (never, then every sprint, then once).
- Anthropic's own newest primitive (`/goal`) is the Nov 2025 outer loop re-implemented inside the product: a fresh small model judges completion after every turn, exactly the "separate judge" role the Mar 2026 post argued for, but with the judge reading only the transcript.
- For a run on a current Opus model, the Mar 2026 V2 shape (planner, one long generator session with compaction, evaluator at the end) is the cheapest configuration Anthropic has published that still reached a working app; the Nov 2025 fresh-context-per-feature shape remains the safer default when the model is weaker or the run is longer than one context window can tolerate.

### Gaps
- The Mar 2026 post does not name the V1 handoff files or quote the planner, generator or evaluator prompts.
- The `AGENT_PROMPT.md` used in the C compiler run is not in the public repo (the `current_tasks/` directory and README are there, but no prompt file), and the article only paraphrases it.
- The workshop could not be watched or read from this environment; its exact loop advice is unverified.

---

## Key question 2: What files or artefacts carry state between sessions, and what goes in them?

### Takeaway
State lives in a handful of plain files in the repo plus git itself: a machine-readable checklist of features/tests that only ever flips from failing to passing (`feature_list.json` / `test-results.json`), a human-readable handoff note (`claude-progress.txt` / `PROGRESS.md`), a bootstrap script (`init.sh`), the git log, and (for parallel agents) one lock file per claimed task in `current_tasks/`. Claude Code's own agent-teams feature keeps equivalent state under `~/.claude/teams/` and `~/.claude/tasks/`.

### Cited Findings

**Nov 2025 harness and quickstart [Anthropic]**
- `feature_list.json`: each entry has `category`, `description`, `steps`, `passes`. Example: `"description": "New chat button creates a fresh conversation"` with five verification steps and `"passes": false`. All features start failing. Coding agents may only change `passes`; the prompt says "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." JSON was chosen over Markdown because "models are less likely to overwrite JSON inappropriately". [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Quickstart initializer prompt (paraphrased from the raw file): read `app_spec.txt`; write at least 200 end-to-end test cases; `category` is `functional` or `style`; mix narrow tests (2 to 5 steps) with comprehensive ones, at least 25 with 10+ steps; order by priority with fundamental features first; all `passes: false`; entries must never be removed or edited, only `passes` may flip false to true. [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/initializer_prompt.md)
- `init.sh`: installs dependencies, starts servers/services, prints access instructions, matching the stack named in the spec. [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/initializer_prompt.md)
- Initial git commit contains `feature_list.json`, `init.sh`, `README.md`, with message "Initial setup: feature_list.json, init.sh, and project structure." [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/initializer_prompt.md)
- `claude-progress.txt`: written at the end of every session with what was done, what was tested, open issues, next steps and the completion count (coding prompt, step 9). [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/coding_prompt.md)
- Git commits must be descriptive and list the changes, the testing done and the updated tests; the session must end with no uncommitted changes and the app in a working state. [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/coding_prompt.md)
- Git also lets agents revert bad changes. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- A generated project also contains `.claude_settings.json` ("Security settings"), contents not shown. [Source](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)

**Code with Claude 2026 take-home [Anthropic]**
- `test-results.json` with shape `{ "feature-1": { "passes": false }, "feature-2": { "passes": false } }`; every criterion starts `false`. [Source](https://github.com/anthropics/cwc-long-running-agents)
- `PROGRESS.md` with four sections: Done, In progress, Next, Notes. Read first on every session ("the handoff note from the previous session"); created with empty sections if absent; after each completed item, check it off, record what was learned and what is next, because "future sessions read the file cold". [Source](https://raw.githubusercontent.com/anthropics/cwc-long-running-agents/main/claude-code-config/.claude/CLAUDE.md)
- Other state files: `STEER.md` (operator message shown once by `steer.sh` then cleared; messages arrive prefixed `OPERATOR STEERING:` and take priority over the current plan), `AGENT_STOP` (kill switch: `kill-switch.sh` halts every tool call while this file exists), `.claude/.evidence-reads` (written by `track-read.sh` to record which evidence files the agent has opened), `NEXT_FINDINGS.md` (evaluator's findings for the next pass, written by the wrapper loop), `screenshots/` (evidence location the evaluator opens). [Source](https://github.com/anthropics/cwc-long-running-agents); [Source](https://raw.githubusercontent.com/anthropics/cwc-long-running-agents/main/claude-code-config/.claude/agents/evaluator.md)
- `commit-on-stop.sh` (`Stop` hook) commits tracked changes at session end as a backstop; new files must be added and committed manually at meaningful checkpoints with descriptive messages; `git log` is "a second record". [Source](https://github.com/anthropics/cwc-long-running-agents); [Source](https://raw.githubusercontent.com/anthropics/cwc-long-running-agents/main/claude-code-config/.claude/CLAUDE.md)
- Operator monitoring suggested: `watch -n 2 'tail -20 PROGRESS.md'` and `watch -n 5 'git log --oneline -8'`. [Source](https://github.com/anthropics/cwc-long-running-agents)

**C compiler [Anthropic]**
- Shared state is a bare git repo mounted at `/upstream` in each agent's Docker container; each agent clones to `/workspace` and pushes upstream when done. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Task claims are text files in `current_tasks/`, e.g. `current_tasks/parse_if_statement.txt`. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- The public repo's `current_tasks/` currently holds a `.keep` plus 13 snake_case `.txt` files such as `fix_arm_asm_caspal_instruction.txt`, `fix_pcre2_stack_frame_bloat.txt`, `fix_x86_standalone_kernel_link_errors.txt`, `implement_string_literal_deduplication.txt` (pattern `<action>_<component>_<description>.txt`). [Source](https://github.com/anthropics/claudes-c-compiler/tree/main/current_tasks)
- Agents were instructed to maintain extensive READMEs and progress files; the repo has `DESIGN_DOC.md`, `BUILDING_LINUX.txt`, `ideas/`, and a README in each `src/` subdirectory. [Source](https://www.anthropic.com/engineering/building-c-compiler); [Source](https://github.com/anthropics/claudes-c-compiler)
- Per-session logs at `agent_logs/agent_${COMMIT}.log`. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Context hygiene baked into the harness: tools print only a few lines and log details to files; errors are written as `ERROR` with the reason on the same line so `grep` finds them; aggregate statistics are precomputed. [Source](https://www.anthropic.com/engineering/building-c-compiler)

**Mar 2026 harness [Anthropic]**
- Communication between generator and evaluator was file-based ("one agent writing a file and the other reading and replying"); the sprint contract is the shared artefact; handoff artefacts for context resets were "structured" but unnamed. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

**Claude Code agent teams (docs) [Anthropic]**
- Team config: `~/.claude/teams/{team-name}/config.json` (removed when the session ends; holds a `members` array with name, agent ID and agent type, lead is `team-lead`; contains runtime state such as session IDs and tmux pane IDs, do not hand-edit). Task list: `~/.claude/tasks/{team-name}/` (persists after the session, cleaned per `cleanupPeriodDays`). Mailboxes: `~/.claude/teams/{team-name}/inboxes/{agent-name}.json` (validated on read; malformed entries removed). Team name is `session-` plus the first eight characters of the session ID. [Source](https://code.claude.com/docs/en/agent-teams)

**Managed Agents (Apr 2026) [Anthropic]**
- In Anthropic's hosted runtime, durable state is an append-only session event log stored outside both the harness and Claude's context window; the harness writes with `emitEvent(id, event)`, reads positional slices with `getEvents()`, and a crashed harness restarts with `wake(sessionId)` and `getSession(id)` and resumes from the last event. Compaction, memory-tool files and context trimming remain options but the session keeps the full record. [Source](https://www.anthropic.com/research/managed-agents)

### Inferences
- Anthropic consistently separates two kinds of state: an append-or-flip-only machine-readable contract (JSON, never edited except `passes`) and a free-form human-readable narrative (progress file). The JSON is the thing that prevents "declared done too early"; the narrative is what prevents "re-learns the codebase every session".
- The `.evidence-reads` plus `verify-gate` pattern shows Anthropic's latest thinking: state files should be guarded by hooks, not only by prompt instructions, because the model will otherwise flip `passes` without proof.
- For an overnight run on one machine, the C compiler's `current_tasks/` lock-file convention and the agent-teams `~/.claude/tasks/` queue solve the same problem; the former is portable to any harness, the latter only works in interactive Claude Code.

### Gaps
- Exact format of `claude-progress.txt` is not documented anywhere (the quickstart README calls it "session progress notes" only).
- Contents of the C compiler lock files and of `DESIGN_DOC.md` were not readable from the directory listing.
- The Mar 2026 post's V1 handoff file names remain unknown.

---

## Key question 3: How is "done" decided: self-report, tests, a separate evaluator agent, or a human?

### Takeaway
Never by self-report alone. Nov 2025: the worker marks a feature passing only after driving the UI through browser automation, and the harness forbids editing tests. Mar 2026: a separate evaluator agent with hard per-criterion thresholds decides sprint pass/fail, after Anthropic found the model "a poor QA agent" out of the box and tuned its prompt over several rounds. Feb 2026: near-perfect external verifiers (compiler test suites, build scripts for real projects, CI). The current product answer (`/goal`) is a fresh small model judging the transcript after every turn, and the Code with Claude sample adds a read-only evaluator subagent returning `PASS` or `NEEDS_WORK`.

### Cited Findings

**Nov 2025 [Anthropic]**
- A feature is marked done only after self-verification; the prompt asks the agent to test "as a human user would". [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Browser automation through the Puppeteer MCP server "gave the largest improvement"; without explicit prompting Claude relied on unit tests or `curl` and missed end-to-end failures. Known gap: Claude cannot see browser-native alert modals through Puppeteer, so features relying on them were buggier. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Quickstart coding prompt prohibitions: testing only with curl or backend-only methods; using JavaScript evaluation to bypass the UI; using the puppeteer "active tab" tool; skipping visual verification or marking tests passing without thorough checks; removing, editing, combining or reordering tests or changing their descriptions or steps; changing any field other than `"passes"`. Quality bar: zero console errors, UI matching the spec, all features working end to end. [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/coding_prompt.md)
- Coding prompt step 3: before new work, re-test one or two core features already marked passing; any bug, including visual problems, means marking the feature failing and fixing it first. Step 7: change only `"passes"`, and only after screenshot-backed verification. [Source](https://raw.githubusercontent.com/anthropics/claude-quickstarts/main/autonomous-coding/prompts/coding_prompt.md)
- Open question stated by Anthropic: whether one general-purpose coding agent beats a multi-agent setup with specialised testing, QA or cleanup agents. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Mar 2026 [Anthropic]**
- Motivation: two failure modes, coherence loss as the context fills, and self-evaluation bias, where agents "confidently prais[e] the work" even when mediocre. A separate evaluator was "far more tractable" to tune than a self-critical generator. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Frontend experiment grading criteria (given to both generator and evaluator): design quality (does it "feel like a coherent whole rather than a collection of parts"), originality (custom decisions versus template layouts, library defaults and "AI slop" patterns), craft (typography, spacing, colour harmony, contrast), functionality (can users find primary actions and complete tasks). Design quality and originality were weighted above craft and functionality because Claude already handled the latter by default. Evaluator calibrated with few-shot examples with detailed score breakdowns to reduce score drift. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- V1 full-stack evaluator graded each sprint on bugs found plus criteria covering product depth, functionality, visual design and code quality; "each criterion had a hard threshold. If any fell below it, the sprint failed." [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Example evaluator findings: rectangle fill tool placed tiles only at drag start and end points (FAIL); delete handler at `LevelEditor.tsx:892` required a condition the click did not set (FAIL); `PUT /frames/reorder` defined after `/{frame_id}` so FastAPI returned 422 (FAIL). [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Out of the box Claude was "a poor QA agent": it identified real issues then talked itself into approving the work, and tested superficially. The team read evaluator logs, found where its judgement diverged from theirs, and edited the QA prompt over several rounds. The evaluator is still "inclined to be generous". [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- V2: one QA pass at the end of the build (then two further build/QA rounds in the DAW example). No pass rates or threshold values published. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

**C compiler [Anthropic]**
- Carlini "emphasized near-perfect verifiers": high-quality compiler test suites, plus verifiers and build scripts he wrote for open-source packages. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Late in the project Claude frequently broke existing features when adding new ones, so a CI pipeline and stricter enforcement were added so commits could not break existing code. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Repo test layout: `tests/<name>/main.c`, `expected.stdout`, `expected.ret`, optional `expected.skip.arm`; tests run by compiling `main.c` with `ccc`, executing, and comparing stdout and exit code; unit tests via `cargo test --release`. [Source](https://github.com/anthropics/claudes-c-compiler)
- Time-blindness fix: a `--fast` option runs a 1% or 10% random sample of tests, deterministic per agent but random across VMs so all files get covered. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- "Oracle" when all agents were stuck on one kernel bug: compile most kernel files with GCC and the rest with Claude's compiler at random, then delta-debug to find file pairs that failed together but worked independently. [Source](https://www.anthropic.com/engineering/building-c-compiler)

**Code with Claude 2026 take-home [Anthropic]**
- Default-FAIL contract: "Every criterion starts `false`; the agent can't mark it passing without opening evidence first." `verify-gate.sh` (`PreToolUse`) denies writes to the results file unless the agent has first read an evidence file (screenshots, console logs, result files; patterns set in `track-read.sh`). CLAUDE.md: a test counts as passing only after it runs against the live app (e.g. a Playwright screenshot), the evidence is opened and inspected, and it shows the expected result; "do not work around" the gate. [Source](https://github.com/anthropics/cwc-long-running-agents); [Source](https://raw.githubusercontent.com/anthropics/cwc-long-running-agents/main/claude-code-config/.claude/CLAUDE.md)
- Evaluator subagent (`agents/evaluator.md`): name `evaluator`; tools Read, Glob, Grep, Bash (Bash limited to `git diff`, `git log`, `ls`/`cat`; not a hard read-only boundary); cannot edit, write or run the app; must not offer to fix anything. Procedure: read the spec/acceptance criteria; `git diff` against baseline; open every screenshot or console log in `screenshots/` and judge what they show, not what filenames imply (a file that fails to open counts as missing evidence); decide. "Plausibility is not correctness." "Missing evidence for any acceptance criterion is NEEDS_WORK." Output: bare `PASS` or `NEEDS_WORK` on the first line so a wrapper can parse it; PASS gets one line on what evidence convinced it; NEEDS_WORK gets a bulleted list of specific fixable findings. Invoked as `claude --agent evaluator -p "<review prompt>"`. [Source](https://raw.githubusercontent.com/anthropics/cwc-long-running-agents/main/claude-code-config/.claude/agents/evaluator.md); [Source](https://github.com/anthropics/cwc-long-running-agents)
- Shipped evaluation is binary; numeric rubrics (functionality, design, craft, originality with few-shot examples) are a "Going further" item, not shipped. [Source](https://github.com/anthropics/cwc-long-running-agents)

**Claude Code `/goal` and agent-team hooks [Anthropic]**
- `/goal`'s evaluator "doesn't run commands or read files independently", so the condition must be something Claude's own output demonstrates (e.g. "`npm test` exits 0", "`git status` is clean"). A good condition has one measurable end state, a stated check, and constraints that must not change. Evaluation tokens are billed on the small fast model and are "typically negligible". [Source](https://code.claude.com/docs/en/goal)
- Agent-team quality gates: `TeammateIdle` (exit code 2 sends feedback and keeps the teammate working), `TaskCreated` (exit 2 prevents creation), `TaskCompleted` (exit 2 prevents completion and sends feedback). [Source](https://code.claude.com/docs/en/agent-teams)

**Workshop [Search snippet only, third party]**
- One summary says the evaluator "uses Playwright to test live apps and grade subjective output via rubrics", and that speakers named "poor self-evaluation" as a core challenge. [Source (search summary)](https://digg.com/ai/wtakhm1b)

### Inferences
- Anthropic's position hardened over time from "tell the model to verify" (Nov 2025) to "make verification a separate agent with its own context" (Mar 2026) to "enforce evidence with hooks so the model physically cannot flip the flag" (CwC 2026). A reader designing an overnight run should treat prompt-only verification as the weakest tier.
- The reliability ranking implied by the three posts: deterministic test suites and build scripts (C compiler) > browser-driven evaluator agent with hard thresholds (Mar 2026) > browser-driven self-verification (Nov 2025) > transcript-only judge (`/goal`). The `/goal` judge is cheap but only as good as what the worker chose to surface.
- The "re-test one or two passing features first" step in the Nov 2025 coding prompt is the mechanism that converts a single-agent loop into something with regression protection, in the absence of CI.

### Gaps
- No Anthropic post publishes false-positive or false-negative rates for the evaluator agent, or threshold values for the hard per-criterion gates.
- The actual QA prompt tuned over "several rounds" in the Mar 2026 work is not published.

---

## Key question 4: What coordination mechanisms were used for parallel agents (locks, task queues, branch per task, merge rules)?

### Takeaway
The C compiler run used the simplest possible scheme: a shared bare git repo, git itself as the lock (a text file per task in `current_tasks/`, with push conflicts forcing the loser to pick another task), work-pull-merge-push-unlock cycles, no orchestrator, and a few agents given standing specialist roles. Claude Code's agent teams productise a similar idea (shared task list with file-locked claiming, dependencies, and JSON mailboxes) but only for interactive sessions. Anthropic's internal source control redesign (Oct 2026) shows the limit case: 30,000+ agent merges per day with lock-free commits and no merge-queue lock, relying on post-merge testing and on Claude resolving conflicts.

### Cited Findings

**C compiler [Anthropic]**
- 16 parallel Claude instances; a bare git repo as shared upstream mounted at `/upstream` in each agent's Docker container; each agent clones to `/workspace` and pushes when done. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Task locking: an agent claims a task by writing a text file to `current_tasks/` (e.g. `current_tasks/parse_if_statement.txt`); "if two agents try to claim the same task, git's synchronization forces the second to pick another." [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Cycle per task: work on the task, pull and merge upstream changes, push, then remove the lock. Merge conflicts were frequent but Claude resolved them. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- No orchestration agent and no other inter-agent communication; agents chose their own work. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Specialised standing roles: one agent consolidated duplicate code, one improved compiler performance, one worked on efficient output code, one critiqued the design from a Rust developer's perspective, one maintained documentation. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Once the kernel compiled, agents were each pointed at a different open-source project (SQLite, Redis, libjpeg, MQuickJS, Lua) to spread the work. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- A CI pipeline was added late so commits could not break existing code. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Context hygiene for shared logs: `ERROR` lines grep-able, precomputed aggregate stats, `--fast` sampling deterministic per agent and random across VMs. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Third-party summary agrees: "Agents claimed work with lockfiles and synced through git, with no orchestration agent." [Third party, search summary](https://simonwillison.net/2026/Feb/22/ccc/)

**Claude Code agent teams (docs) [Anthropic]**
- Enabled with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; experimental and off by default. One session is the lead; teammates are separate Claude Code instances with their own context windows. [Source](https://code.claude.com/docs/en/agent-teams)
- Shared task list with three states (pending, in progress, completed) and dependencies; a pending task with unresolved dependencies cannot be claimed; completing a task auto-unblocks dependents. Lead assigns, or teammates self-claim the next unassigned unblocked task. "Task claiming uses file locking to prevent race conditions." [Source](https://code.claude.com/docs/en/agent-teams)
- Messaging: each agent's mailbox is a JSON file at `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`; messages are delivered automatically; idle teammates notify the lead with their final answer; a teammate whose turn ends on an API error notifies the lead with the error text. Messages between agents are marked as coming from another Claude session, cannot approve permissions, and in auto mode are screened by the classifier. [Source](https://code.claude.com/docs/en/agent-teams)
- Important for unattended use: "Spawning teammates also requires an interactive session. In non-interactive mode with the `-p` flag, including Agent SDK sessions, Claude doesn't spawn teammates." [Source](https://code.claude.com/docs/en/agent-teams)
- Best practice: "Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files." Start with 3 to 5 teammates; 5 to 6 tasks per teammate; "Three focused teammates often outperform five scattered ones." [Source](https://code.claude.com/docs/en/agent-teams)
- Limitations: no session resumption with in-process teammates; task status can lag (teammates fail to mark tasks complete, blocking dependents); shutdown slow; one team per session; no nested teams; lead is fixed; "The lead can stop early too, deciding the team is finished before all tasks are actually complete." [Source](https://code.claude.com/docs/en/agent-teams)
- Alternatives named: subagents (results return to caller), cross-session messaging, and git worktrees for "manual parallel sessions ... without automated team coordination". [Source](https://code.claude.com/docs/en/agent-teams)

**Anthropic internal source control (Oct 2026) [Anthropic]**
- Anthropic's clients are "almost all agents and jobs that are always online"; the monorepo main history is almost 100 GB. Merges grew from about 2,500 per day (May 2026) to over 30,000 per day (Sept 2026); about 25 million checkouts per day for CI. [Source](https://www.anthropic.com/research/redesigning-source-control)
- The new system (Scion) makes commits, rebases and merges lock-free; moving a ref is a compare-and-swap on a single database row; refs other than main and release branches are discouraged. Anthropic could not replicate a global merge-queue lock and relies on post-merge and pre-deploy automated testing instead; concurrent changes can conflict because changes merge while tests run, and "Claude typically resolves these conflicts faster than humans can identify them." [Source](https://www.anthropic.com/research/redesigning-source-control)
- Code review (Antique) uses semantic approval rules so engineers review intent rather than every line. [Source](https://www.anthropic.com/research/redesigning-source-control)

**Mar 2026 harness [Anthropic]**
- Coordination between the two roles was sequential and file-based, not parallel. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

### Inferences
- Anthropic's parallel designs avoid branch-per-task entirely: both the C compiler run and the internal monorepo push straight to a shared mainline and let tests catch breakage after the fact. Branch isolation is offered only as a manual option (worktrees) in the Claude Code docs.
- The lock-file-in-git pattern needs no infrastructure and survives agent crashes (a stale lock is just a file to delete), which is why it suits an overnight run on one box; the agent-teams task list is the better fit when a human is at the terminal.
- Anthropic's experience that the lead "can stop early" and that teammates "fail to mark tasks completed" mirrors the Nov 2025 single-agent failure modes, so the same external contract (a results file that only tests may flip) is still needed in a team.

### Gaps
- The C compiler post does not describe how stale locks were cleaned up if an agent died mid-task, nor how `current_tasks/` files were named or what they contained beyond the task name.
- No Anthropic source gives merge-conflict frequency or resolution failure rates for the compiler run.

---

## Key question 5: What failed or needed human intervention, and what did Anthropic conclude about the limits?

### Takeaway
Recurring failures across all three posts: declaring done too early, marking features passing without real verification, leaving the environment broken for the next session, context anxiety (wrapping up as the window fills), self-praise bias in evaluation, and regressions when adding features. Human effort went into harness and verifier design, reading traces and re-tuning prompts, not into pair programming. Anthropic's stated limits: the harness is a snapshot of current model weaknesses and should be re-simplified on each model release; the full harness costs 20x a solo run; the C compiler is "not yet a drop-in replacement"; and agent teams left "unattended for too long" waste effort.

### Cited Findings

**Nov 2025 [Anthropic]**
- Failure-to-fix table: declares project done too early (fix: feature list, work one feature); leaves bugs or undocumented progress (fix: git repo and progress notes, basic test at start, commit and notes at end); marks features done prematurely (fix: verify and mark passing only after careful testing); wastes time working out how to run the app (fix: `init.sh`). A further failure: a later agent sees progress and wrongly declares the job finished. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Without explicit prompting Claude tested via unit tests or `curl` and missed end-to-end failures; alert modals invisible via Puppeteer. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Open questions: single agent vs specialised agents; generalisation beyond full-stack web development. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Mar 2026 [Anthropic]**
- Context anxiety: models "begin wrapping up work prematurely" as the window fills; Sonnet 4.5 strongly, Opus 4.5 "largely removed that behavior on its own". [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Self-evaluation bias; evaluator leniency; shallow testing (evaluator missed deeper bugs and subtle interactions); generator stubbing features or missing details; product-intuition gaps (workflow did not guide users to build sprites and entities before levels); physics rough edges and an AI-built level with an unjumpable wall. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Solo baseline on the retro game maker: entities appeared but nothing responded to input; wiring between entity definitions and the runtime was broken. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- DAW: QA found clips could not be moved or resized, instrument and effect UIs missing (synth knobs, EQ curves), recording stub-only; result "not professional quality"; Claude "can't actually hear", weakening musical-taste feedback. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Human role: reading evaluator logs and editing the QA prompt over several rounds; removing harness components one at a time to measure impact (a radical cut failed). Cost: the full harness was "over 20x more expensive" than solo. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Prompt wording visibly shaped output (e.g. "the best designs are museum quality"); scores improved then plateaued; complexity tended to grow. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

**C compiler [Anthropic]**
- Claude once ran `pkill -9 bash` by accident, which killed its own loop. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Late in the project new features and bug fixes frequently broke existing functionality; CI and stricter enforcement were added; the author "tried to fix the limitations but was not fully successful". [Source](https://www.anthropic.com/engineering/building-c-compiler)
- All 16 agents got stuck on the same kernel bug; the human built the GCC-mix oracle plus delta debugging to unblock them. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Limits at publication: cannot generate 16-bit x86 real-mode code within Linux's 32k limit (output exceeded 60kb, so x86 calls out to GCC for that phase; ARM and RISC-V compile fully); no native assembler or linker (demo used GCC's); not a drop-in replacement, does not build every project; generated code less efficient than GCC at `-O0`; Rust quality "reasonable but not at expert level". [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Later repo state conflicts with the Feb 2026 article on one point: the current README says "the frontend, SSA-based IR, optimizer, code generator, peephole optimizers, assembler, linker, and DWARF debug info generation are all implemented from scratch" and that it "produces ELF executables without any external toolchain", so the assembler/linker gap was closed after the post. The README also states "None of it has been validated for correctness." [Source](https://github.com/anthropics/claudes-c-compiler); contrast [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Model-capability framing: Opus 4 models "were barely capable of producing a functional compiler"; Opus 4.5 could pass large test suites but not compile real large projects; Opus 4.6 did. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Human involvement was mainly designing the harness, tests and feedback and watching for failure modes; the article describes no mid-run interactive debugging, and the repo README confirms no pair programming. [Source](https://www.anthropic.com/engineering/building-c-compiler); [Source](https://github.com/anthropics/claudes-c-compiler)

**Code with Claude 2026 take-home [Anthropic]**
- "Re-simplify on model upgrades": re-check how much of `CLAUDE.md` you still need after each model release; newer models drift less and self-scope better. The shipped hook is intentionally simple and `verify-gate.sh` comments list gaps a production version must close. Hooks do not load from subdirectories. [Source](https://github.com/anthropics/cwc-long-running-agents)

**Claude Code docs [Anthropic]**
- Agent teams: "Letting a team run unattended for too long increases the risk of wasted effort"; teammates "may stop after encountering errors instead of recovering"; the lead may start implementing instead of waiting, or stop early. [Source](https://code.claude.com/docs/en/agent-teams)
- `/goal` clears itself on four unrecoverable errors (auth failure where Claude Code manages credentials, exhausted credit balance, context overflow auto-compaction cannot clear, model unavailable); other errors retry three times then pause; rate limits and usage limits pause the goal. Background work defers evaluation; check-ins start at 30 minutes and double up to 4x; at most three idle check-ins per goal between prompts. [Source](https://code.claude.com/docs/en/goal)

**Measuring agent autonomy (Feb 2026) [Anthropic]**
- Why humans interrupt Claude Code: missing technical context or corrections 32%, Claude slow/hanging/excessive 17%, user had enough help 7%, user wants the next step 7%, changed requirements 5%. Why Claude stops itself: presenting a choice between approaches 35%, gathering diagnostic or test information 21%, clarifying vague requests 13%, requesting credentials or access 12%, seeking approval 11%. On the most complex tasks Claude asks for clarification more than twice as often as on minimal-complexity tasks. [Source](https://www.anthropic.com/research/measuring-agent-autonomy)
- Internally, average human interventions per Claude Code session fell from 5.4 to 3.3 between August and December 2025 while success on the hardest tasks doubled. [Source](https://www.anthropic.com/research/measuring-agent-autonomy)

**Workshop [Search snippet only, third party]**
- Challenges named by the speakers per recaps: "context rot, context anxiety, poor self-evaluation, and planning failures"; takeaways: "reading traces as the primary debug loop, deleting harness components as models improve". [Source (search summary)](https://digg.com/ai/wtakhm1b)

### Inferences
- The human job in every Anthropic run was the same: write the verifier, read the traces, tighten the gate. None of the posts describe a human steering the agent's code decisions during the run, which supports treating an overnight run as "verifier design before bed, log review in the morning".
- The autonomy research's top interruption reason (missing technical context, 32%) and top self-stop reason (presenting a choice, 35%) are exactly what an unattended run cannot service; the planner/spec step and the "one feature at a time" rule exist to pre-empt both.
- Anthropic's repeated advice to delete harness pieces on each model release means any overnight design should keep context resets, sprint contracts and per-sprint evaluation as toggles rather than fixed architecture.

### Gaps
- No Anthropic source quantifies how often an evaluator pass fails, how many sprints were retried, or how many sessions in the compiler run ended without a useful commit.
- The workshop's specific failure anecdotes could not be verified.

---

## Key question 6: Any numbers: tokens, dollars, hours, pass rates, number of sessions

### Takeaway
Hard figures exist for the C compiler run (16 agents, ~2,000 sessions, two weeks, ~2B input and 140M output tokens, just under $20,000, ~100k lines of Rust, 99% on most test suites) and the Mar 2026 app builds (solo 20 min/$9 vs full harness 6 h/$200; simplified V2 DAW 3 h 50 min/$124.70). The Nov 2025 post gives feature counts only (200+). Claude Code autonomy data: the 99.9th-percentile unattended turn went from under 25 to over 45 minutes between Oct 2025 and Jan 2026.

### Cited Findings

**C compiler (Opus 4.6, published 5 Feb 2026) [Anthropic]**
- 16 parallel Claude instances; nearly 2,000 Claude Code sessions; two weeks; about 2 billion input and 140 million output tokens; just under $20,000 API cost. [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Output: roughly 100,000-line C compiler in Rust depending only on the Rust standard library; builds Linux 6.9 on x86, ARM and RISC-V; compiles QEMU, FFmpeg, SQLite, PostgreSQL, Redis; runs Doom; 99% pass rate on most compiler test suites including the GCC torture suite; clean-room (no internet during development). [Source](https://www.anthropic.com/engineering/building-c-compiler)
- Repo README: PostgreSQL all 237 regression tests; FFmpeg all 7,331 FATE checkasm tests on x86-64 and AArch64; targets x86-64, i686, AArch64, RISC-V 64. [Source](https://github.com/anthropics/claudes-c-compiler)

**Mar 2026 harness [Anthropic]**
- Frontend experiment: 4 criteria; 5 to 15 iterations per generation; runs up to 4 hours; the Dutch art museum site pivoted to a 3D gallery at iteration 10. [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Retro game maker (V1, Opus 4.5): planner produced 16 features across 10 sprints; Sprint 3 had 27 contract criteria. Solo agent: 20 minutes, $9, broken core functionality. Full harness: about 6 hours, about $200, playable. "Over 20x more expensive." [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Browser DAW (V2, Opus 4.6), per-phase: Planner 4.7 min, $0.46; Build R1 2 h 7 min, $71.08; QA R1 8.8 min, $3.24; Build R2 1 h 2 min, $36.89; QA R2 6.8 min, $3.09; Build R3 10.9 min, $5.88; QA R3 9.6 min, $4.06; total 3 h 50 min, $124.70 (body text rounds to "about 4 hours and $124"). [Source](https://www.anthropic.com/research/harness-design-long-running-apps)
- Models: Sonnet 4.5 (context anxiety), Opus 4.5 (V1), Opus 4.6 (V2). [Source](https://www.anthropic.com/research/harness-design-long-running-apps)

**Nov 2025 harness and quickstart [Anthropic]**
- Over 200 features in the claude.ai clone; model named is Opus 4.5; no hours, token or session counts given. [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Quickstart: 200 features by default (20 to 50 suggested for demos); 5 to 15 minutes per coding iteration; "many hours" for a full build; default model `claude-sonnet-4-5-20250929`. [Source](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)

**Claude Code autonomy and cost [Anthropic]**
- 99.9th-percentile turn duration nearly doubled from under 25 minutes to over 45 minutes between October 2025 and January 2026; median turn about 45 seconds (40 to 55 s range); the extreme tail declined somewhat after mid-January. Full auto-approve used in about 20% of sessions for new users (<50 sessions), over 40% by about 750 sessions; interrupt rate about 5% of turns at ~10 sessions vs about 9% for experienced users. Internal interventions per session 5.4 to 3.3 (Aug to Dec 2025). Public API: about 80% of tool calls from agents with at least one safeguard, about 73% with a human in the loop (upper bound), about 0.8% of actions irreversible. Published 18 Feb 2026. [Source](https://www.anthropic.com/research/measuring-agent-autonomy)
- Agent teams "use approximately 7x more tokens than standard sessions when teammates run in plan mode"; token use roughly proportional to team size; recommendation to use Sonnet for teammates and shut them down when done. Enterprise averages: about $13 per developer per active day, $150 to $250 per month, under $30 per active day for 90% of users. A `--max-budget-usd` CLI flag exists and counts the 1.1x data-residency multiplier. Background token use typically under $0.04 per session. [Source](https://code.claude.com/docs/en/costs)
- Managed Agents: p50 time-to-first-token dropped roughly 60% and p95 over 90% after decoupling harness from container (8 Apr 2026). [Source](https://www.anthropic.com/research/managed-agents)
- Source control: about 2,500 merges/day (May 2026) to over 30,000/day (Sept 2026); ~25 million checkouts/day for CI; cache hit rates above 99%; migration took five months with a seven-person team (13 Oct 2026). [Source](https://www.anthropic.com/research/redesigning-source-control)

**Workshop run-length claims [Search snippet only, third party, conflicting]**
- One recap cites a jump "from 1 hour on Opus 3.7 to 12 hours on Opus 4.6 with minimal scaffolding"; another says "about 30 hours for Opus 4.5 and Sonnet 4.5"; a third says "days". These figures disagree and none could be checked against the recording. ("Opus 3.7" is not a model name Anthropic shipped; the recap likely means Claude 3.7 Sonnet.) [Source (search summary)](https://digg.com/ai/wtakhm1b); [Source (search summary)](https://daily.dev/posts/build-agents-that-run-for-hours-without-losing-the-plot-ash-prabaker-andrew-wilson-anthropic-n3dvnyjtj)

### Inferences
- Per-session economics from the C compiler run: ~$10 and ~1 M input tokens per session on average (20,000 / 2,000 and 2 B / 2,000), with roughly 70,000 output tokens per session, which is consistent with each session being one bounded task. (Arithmetic on Anthropic's figures, not a published number.)
- The V2 DAW numbers imply QA is cheap relative to build (about $10 of $125, about 25 of 230 minutes), so running the evaluator more often than once at the end is unlikely to be the cost driver; the build phases are.

### Gaps
- No Anthropic source gives tokens per session, cost per feature, or pass/fail rates for the Nov 2025 harness.
- No verified Anthropic figure for maximum unattended run length per model; the only official duration data is the Claude Code 99.9th-percentile turn (45+ minutes), which measures one turn, not a looped run.

---

## Key question 7 (added): What newer Anthropic material from 2026 supersedes or extends the three articles?

### Takeaway
Three things are newer than the March 2026 post and directly relevant: the Code with Claude 2026 take-home repo (hooks-based default-FAIL contract, read-only evaluator subagent, `PROGRESS.md` handoff, kill switch and steer file), the Claude Code `/goal` command (a product-native completion-judge loop that works with `claude -p`), and agent teams (experimental shared task list and mailboxes, interactive only). Managed Agents (April 2026) and the source control redesign (October 2026) describe Anthropic's internal infrastructure for the same problem at scale.

### Cited Findings
- `cwc-long-running-agents` cites both earlier posts as its sources, is "the take-home for the Long-Running Agents station at Code with Claude 2026", and is described as "example ingredients, not a turnkey harness. Event demo; not maintained and not accepting contributions." Apache-2.0; 3 commits on main. [Source](https://github.com/anthropics/cwc-long-running-agents)
- Its hook set: `track-read.sh` (records evidence reads), `verify-gate.sh` (`PreToolUse`, blocks results-file writes until evidence read), `commit-on-stop.sh` (`Stop`, commits leftovers), `kill-switch.sh` (halts tool calls while `AGENT_STOP` exists), `steer.sh` (shows `STEER.md` once then clears). Setup: `cp -r claude-code-config/.claude /path/to/your/project/` then `chmod +x .claude/hooks/*.sh`; set `RESULTS_FILE` and the evidence pattern. [Source](https://github.com/anthropics/cwc-long-running-agents)
- `/goal` requirements and knobs: `CLAUDE_CODE_GOAL_CHECKIN_MINUTES` (0 disables check-ins and retries), `ANTHROPIC_DEFAULT_HAIKU_MODEL` to change the judge model, works in `-p`, desktop and Remote Control; check-ins need v2.1.234+, idle check-in cap v2.1.246+; unavailable when `disableAllHooks` is true. [Source](https://code.claude.com/docs/en/goal)
- Agent teams: enable via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`; a named subagent launches as a teammate while enabled; teammates inherit the lead's permission mode (and `--dangerously-skip-permissions`) but not `dontAsk`; `TeammateIdle`, `TaskCreated`, `TaskCompleted` hooks; subagent definitions in `.claude/agents/` can define reusable teammate roles. [Source](https://code.claude.com/docs/en/agent-teams)
- Managed Agents separates session (append-only log), harness (loop) and sandbox (execution) behind `execute(name, input) -> string`; containers are disposable and reprovisioned via `provision({resources})`; container failure is returned to Claude as a tool error so it can retry on a new container; credentials stay out of the sandbox (git tokens wired at init, MCP via proxy and vault). [Source](https://www.anthropic.com/research/managed-agents)
- Other 2026 engineering posts on the index that may be relevant but were not read: "How we built Claude Code auto mode: a safer way to skip permissions" (25 Mar 2026), "Demystifying evals for AI agents" (9 Jan 2026), "Quantifying infrastructure noise in agentic coding evals" (5 Feb 2026), "An update on recent Claude Code quality reports" (23 Apr 2026), "How we contain Claude across products" (25 May 2026). [Source](https://www.anthropic.com/engineering)

### Inferences
- The CwC repo is the most directly reusable Anthropic artefact for an overnight run on Claude Code: it is the Nov 2025 pattern ported from the Agent SDK to Claude Code hooks, with the Mar 2026 evaluator added as a subagent.
- Because agent teams do not spawn in `-p` mode, a truly unattended parallel run on Claude Code today still needs the C compiler's approach (N independent `claude -p` loops plus git locks) or the Agent SDK.

### Gaps
- The auto-mode post (25 Mar 2026) likely matters for unattended permission handling but was not fetched within the tool budget.
- No Anthropic page for the "Build Agents That Run for Hours" workshop was found; the Code with Claude 2026 event date and the talk date are unconfirmed (one recap was dated 23 May 2026, suggesting the talk is from around then).
