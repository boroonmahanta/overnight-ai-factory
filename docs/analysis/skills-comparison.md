# Skills comparison: Addy Osmani, Matt Pocock and Lauren Tan

Status: a proposal for Boroon's review, 1 November 2026. Nothing here is installed or decided.

Basis: the three repositories were cloned and read on 1 November 2026, and the two review videos (`docs/sources/transcript-pstack-skills-review.md` and `docs/sources/transcript-skills-comparison-addy-pocock-tan.md`) were read in full. Every skill was listed from the repos. The routing documents and the key skills were read in part. Most skill bodies were not read, so verdicts rest on each skill's description and on how its pack routes to it. Plan section 8.3 says to read a third-party skill in full before adopting it, so "Adopt" means "put on the shortlist to read in full", not "approved".

Companion file: `tshirt-sizing.md` turns this comparison into a T-shirt size approach and says which skills to use at each size.

## 1. Bottom line

- **The three packs answer three different questions.** Matt Pocock: do we agree on what we are building? Lauren Tan: can you prove it works? Addy Osmani: did we follow the whole process? The overlap is large because good engineers converge, as the video says.
- **V3.1 already took a lot.** Grilling rules, glossary and ADRs, Wayfinder, research tickets, prototypes, TDD at seams, two-axis review with named smells, the PR body template, the retro, the verification skill idea, the outer loop and gardening all came from Pocock and Tan. Section 5.3 maps each one.
- **Addy's pack adds what V3.1 lacks most.** That is a written quality bar that watches for a weakened bar (`constraint-driven-development`), excuse tables that stop agents skipping steps, and a release checklist side (`shipping-and-launch`, `deprecation-and-migration`, `security-and-hardening`).
- **Tan's pack adds the best material for the gate.** That is `create-verification-skill`, `maintain-verification-skill`, `blast-radius`, `show-me-your-work` and `correct`.
- **None of the three touch Power Platform.** No Dataverse, pac, solutions, flows or Copilot Studio. They also do not cover lanes, identities, environment pools or a gate repo. Those stay GET AI's own work.
- **Do not install the packs.** A pack is 25 to 58 skills, and every installed skill adds to the context the agent must consider. Take a small set, rewrite it for Power Platform, and name it `lcp-*` (plan section 1.1).
- **Size the ceremony to the work.** The companion file `tshirt-sizing.md` proposes five T-shirt sizes. They line up with the Merge Danger bands the plan already uses, so the size sets how many verifiers run and which skills apply.

## 2. The three packs side by side

| | Addy Osmani | Matt Pocock | Lauren Tan (poteto) |
|---|---|---|---|
| Repo | `addyosmani/agent-skills` | `mattpocock/skills` | `cursor/plugins`, folder `pstack` |
| Version read | commit 301b02b, 1 Nov 2026 | commit 4ae2317, 31 Oct 2026 | commit ae5650f, 31 Oct 2026 |
| Licence | MIT | MIT | MIT |
| Contents, counted | 25 skills, 9 commands, 4 reviewer personas, 7 checklists, hooks | 39 skills: 20 engineering, 7 productivity, 4 misc, 8 in progress | 58 skills (24 are principles), 23 playbooks, 2 agents, 3 automation skills |
| Question it answers | Did we follow the whole process? | Do we agree on what we are building? | Can you prove it works? |
| Planning | Full lifecycle: define, plan, build, verify, review, ship | Effort up front: grill, glossary, ADRs, spec, tickets | No planning skill, by design. "The best spec is the code" |
| Where the weight sits | Breadth. The only one that covers CI/CD, observability, deprecation and shipping | Before coding | After coding: verification and adversarial review |
| Autonomy | `/build auto`: approve the plan once, then every task runs test-first and stops on failure | `implement-spec` runs subagents over a task graph. Pocock rates a scripted loop as more reliable | Playbooks for autonomous runs and autopilot. Tan's agents merge their own PRs once the environment is trusted |
| Self-triggering skills | All 25 can trigger themselves | 15 of 39 can; 24 run only when invoked | 1 of 58 can; 57 run only when invoked |
| Portability (video and Pocock claims, not checked) | Said to install into about 70 agents | Installed with `npx skills` | A Cursor plugin; an unofficial port to other agents is mentioned |
| Cost signal | Addy's own guide says roll out gradually | Small, composable skills | The video's run took about twice as long as a plain run, with many more tokens |
| Power Platform | None | None | None |

The self-triggering row matters for a headless factory. Skills that run only when invoked behave predictably when the executor's prompt names them. Skills that can trigger themselves can fire when nobody wants them. The video warns about accidental triggering.

## 3. Full list of every skill

Generated from the clones, so nothing is retyped by hand. Descriptions are each repo's own `description` line, shortened. Section 5 judges them.

### 3.1 Addy Osmani: `addyosmani/agent-skills`

Version read: commit 301b02b, 1 November 2026

#### Skills (25)

| Name | What it does |
|---|---|
| `api-and-interface-design` | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend … |
| `browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual … |
| `ci-cd-and-automation` | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies. |
| `code-review-and-quality` | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch. … |
| `code-simplification` | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary … |
| `constraint-driven-development` | Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Interviews the user on which dimensions matter, supplies sane default thresholds when they have no number in mind, records everything in … |
| `context-engineering` | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project. |
| `debugging-and-error-recovery` | Guides systematic root-cause debugging. Use when tests fail, builds break, something that worked yesterday broke, behavior doesn't match expectations, or you encounter any unexpected error. Use when you need to figure out what broke and … |
| `deprecation-and-migration` | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when migrating a database schema in production, such as renaming or dropping a column … |
| `documentation-and-adrs` | Records decisions and documentation. Use when you need to document an architecture decision (ADR) or the reasoning behind a design choice, when changing public APIs, shipping features, or when you need to record context that future … |
| `doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when you want every assumption cross-examined before proceeding, when stress-testing a plan for hidden failure modes, when correctness matters … |
| `frontend-ui-engineering` | Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating components, implementing layouts, meeting WCAG accessibility requirements, managing state, or when the output … |
| `git-workflow-and-versioning` | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, splitting uncommitted work in a messy working tree into clean atomic commits, opening or reviewing a pull request … |
| `idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand … |
| `incremental-implementation` | Delivers changes incrementally in thin, verifiable slices. Use when implementing any feature or change that touches more than one file, or when picking up the next task from a plan. Use when rolling a change out behind a feature flag, when … |
| `interview-me` | Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95% confidence about the underlying intent. Use when an ask is underspecified ("build me X" … |
| `observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when shipping any feature that runs in production and you need evidence it works. Use when production issues … |
| `performance-optimization` | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when you suspect performance regressions, when Core Web Vitals or load times need improvement, when N+1 query … |
| `planning-and-task-breakdown` | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible. |
| `security-and-hardening` | Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentication, data storage, or external integrations, or when checking a login flow is safe against the OWASP Top … |
| `shipping-and-launch` | Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or … |
| `source-driven-development` | Grounds every implementation decision in official documentation. Use when you want to verify an approach against the official docs before implementing it, or when you want authoritative, source-cited code free from outdated patterns. Use … |
| `spec-driven-development` | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when drafting a PRD or requirements document with objectives and scope, or when requirements are unclear … |
| `test-driven-development` | Drives development with tests using the red-green-refactor loop. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to … |
| `using-agent-skills` | Discovers and invokes agent skills. Use when starting a session, or when you need to decide which skill or workflow applies to the piece of work at hand. This is the meta-skill that governs how all other skills are discovered and invoked. |

#### Slash commands (9)

| Name | What it does |
|---|---|
| `/build` | Implement tasks incrementally — build, test, verify, commit. Add "auto" to run the whole plan in one approved pass. |
| `/code-simplify` | Simplify code for clarity and maintainability — reduce complexity without changing behavior |
| `/constraints` | Define and enforce this project's quality bar — interview, sane defaults, CONSTRAINTS.md |
| `/planning` | Break work into small verifiable tasks with acceptance criteria and dependency ordering |
| `/review` | Conduct a five-axis code review — correctness, readability, architecture, security, performance |
| `/ship` | Run the pre-launch checklist via parallel fan-out to specialist personas, then synthesize a go/no-go decision |
| `/spec` | Start spec-driven development — write a structured specification before writing code |
| `/test` | Run TDD workflow — write failing tests, implement, verify. For bugs, use the Prove-It pattern. |
| `/webperf` | Run a web performance audit via the web-performance-auditor persona |

#### Reviewer personas (4)

| Name | What it does |
|---|---|
| `code-reviewer` | Senior code reviewer that evaluates changes across five dimensions — correctness, readability, architecture, security, and performance. Use for thorough code review before merge. |
| `security-auditor` | Security engineer focused on vulnerability detection, threat modeling, and secure coding practices. Use for security-focused code review, threat analysis, or hardening recommendations. |
| `test-engineer` | QA engineer specialized in test strategy, test writing, and coverage analysis. Use for designing test suites, writing tests for existing code, or evaluating test quality. |
| `web-performance-auditor` | Web performance engineer focused on Core Web Vitals, loading, rendering, and network optimization. Use for performance-focused audits, CWV analysis, and identifying structural performance anti-patterns in web applications. |

#### Other parts

- **Reference checklists (7):** accessibility-checklist, definition-of-done, observability-checklist, orchestration-patterns, performance-checklist, security-checklist, testing-patterns.
- **Hooks:** sdd-cache-post.sh, sdd-cache-pre.sh, session-start.sh, simplify-ignore.sh (with notes `SDD-CACHE.md` and `SIMPLIFY-IGNORE.md`).

### 3.2 Lauren Tan (poteto): `cursor/plugins`, folder `pstack`

Version read: cursor/plugins commit ae5650f, 31 October 2026

#### Skills other than principles (34)

| Name | What it does |
|---|---|
| `architect` | Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape. |
| `arena` | Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape. |
| `automate-me` | Use for "automate me", "create/update/refresh my -mode skill", "turn/capture my preferences or working style into a skill", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via create-skill + unslop … |
| `benchmark-checklist` | Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you run a benchmark or report a speedup or regression you measured. |
| `blast-radius` | Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a … |
| `bro` | Restate the last message in plain human language, with no jargon. |
| `correct` | Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. … |
| `create-formal-verification-skill` | Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verification tool fits. Use for /create-formal-verification-skill, "model-check this … |
| `create-verification-skill` | Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /create-verification-skill, "make a control skill for this repo", or when a project has no scripted way to … |
| `figure-it-out` | Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for … |
| `how` | Use for "how does X work", code walkthroughs before changing something, and placement / ownership / layering questions ("where should this live", "which package owns this", "is this the right layer"). Explains subsystem architecture … |
| `in-your-own-words` | Restate in your own words what you think the user's goals are and what problem they're trying to solve. Use for /in-your-own-words. |
| `interrogate` | Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this code", "find blind spots", or "tear this apart". Adversaries try to break a change or design, and only findings proven by a run survive. |
| `ketchup` | Catch the user up on what changed in this chat since their last message, in plain words and small visuals. List every item waiting on them with what they need to decide it from the reply alone. Use for /ketchup. |
| `ketchup-video` | Catch the user up like /ketchup, with a short subtitled video of slides for what happened and the waiting calls as text under it. Use for /ketchup-video. |
| `maintain-formal-verification-skill` | Bring a project's formal verification back in line with the code after the code changes: find the commits that touched verified code, update the model, harness, or properties to describe the code as it is now, rerun, and say whether each … |
| `maintain-verification-skill` | Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at most one PR of proven corrections. Use for /maintain-verification-skill or … |
| `make-bot-ui` | Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale. |
| `no-comments` | Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints. |
| `poteto-help` | Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question. |
| `poteto-mode` | poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style. |
| `recall` | Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what … |
| `reflect` | Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect. |
| `setup-pstack` | Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget" … |
| `sharpen` | Make a task deeper, not bigger, then rewrite the prompt. Use for /sharpen. |
| `show-me-your-work` | Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for … |
| `statechart` | Check a TLA+ model of a system that moves between states, such as a product flow, a protocol, or a service, and draw it as a Mermaid statechart. The report gives the shortest path to each state that breaks a rule. Use for /statechart, or … |
| `swarm` | Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration. |
| `tdd` | Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has an obvious cheap local test target. Skip when the test path is unclear, expensive, integration-heavy, or not requested. |
| `teach` | Explain a body of work plainly so a person actually understands it. Runs the `how` and `why` skills and weaves what they find into one clear explanation. Use for 'teach me this', 'help me really understand X', 'explain this change or … |
| `technical-writing` | Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit … |
| `typescript-best-practices` | TypeScript best practices. Use when reading or editing any .ts or .tsx file. |
| `unslop` | Cut AI tells from any writing. |
| `why` | Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and queries each evidence category (source control, issue tracker, long-form docs … |

#### Principles, each a skill (24)

| Name | What it does |
|---|---|
| `principle-attack-the-premise` | Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it. |
| `principle-boundary-discipline` | Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| `principle-build-the-lever` | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the … |
| `principle-encode-lessons-in-structure` | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |
| `principle-exhaust-the-design-space` | Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing. |
| `principle-experience-first` | Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| `principle-explain-the-number` | Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work … |
| `principle-fix-root-causes` | Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. |
| `principle-foundational-thinking` | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| `principle-guard-the-context-window` | Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| `principle-laziness-protocol` | Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem. |
| `principle-make-operations-idempotent` | Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs. |
| `principle-migrate-callers-then-delete-legacy-apis` | Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| `principle-minimize-reader-load` | Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| `principle-model-the-domain` | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. |
| `principle-never-block-on-the-human` | Apply when tempted to ask 'should I do X?' on reversible work. |
| `principle-outcome-oriented-execution` | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| `principle-prove-it-works` | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles. |
| `principle-redesign-from-first-principles` | Apply when integrating a new requirement into an existing design. |
| `principle-separate-before-serializing-shared-state` | Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| `principle-sequence-verifiable-units` | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence … |
| `principle-subtract-before-you-add` | Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base. |
| `principle-test-behavior-not-implementation` | Apply when you write, change, or keep a test. Assert what the code's users can observe, so that the test fails when that behavior breaks and keeps passing when only the internals change. |
| `principle-type-system-discipline` | Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from … |

#### Playbooks, inside `poteto-mode` (23)

| Name | What it does |
|---|---|
| `authoring-a-skill` | Authoring or modifying a skill: You own the skill's voice. |
| `autonomous-run` | Autonomous run: You own the exit condition. Define done, then drive to it without stopping. |
| `autopilot-full` | Autopilot-full: You own the verdicts, never the PRs. One owner carries each PR from build to merge, and nothing merges until your swarm, which never wrote the code, has proven the code that lands. |
| `autopilot-stack` | Autopilot-stack: Reply: |
| `babysit` | Babysit: You own the merge frontier. Declare a mode, clear one PR at a time, stop where the human's call begins. |
| `bug-fix` | Bug fix: You own this task. Plan, review, verify. |
| `eval` | Eval: You own the experiment design. Plan, blind, run, synthesize. |
| `feature` | Feature: You own the design. Plan, review, verify. |
| `hillclimb` | Hillclimb: You own the metric and the experiment's integrity. Supervise and review. Delegate the attempts. |
| `investigation` | Investigation: You own the answer. Plan, route, write. |
| `multi-phase-plan` | Multi-phase or multi-PR plan: You own the plan, not the code. The plan is a checklist an owner runs box by box and the operator audits from the evidence. |
| `opening-a-pr` | Opening a PR: Worktree. |
| `orchestrate` | Orchestrate: You run the program, never the code. Decide which agent does each piece of work, then check what each one produces. |
| `pause-safely` | Pause safely: You own a clean stop. Leave a checkpoint a cold-start agent can resume from. |
| `perf-issue` | Perf issue: You own the measurement story. Plan, review, verify the numbers. |
| `prototype` | Prototype: You own the design decision, not the code. The prototype is a throwaway instrument. The real build follows Feature. |
| `refactoring` | Refactoring: You own the contract. The structure changes. The behavior does not. |
| `runtime-forensics` | Runtime forensics: You own the diagnosis. Instrument the live process, don't theorize from source. |
| `session-pickup` | Session pickup: You own the resume point. Read the prior trail, don't redo it. |
| `shipping` | Shipping: You own what lands. Verify each PR independently, land only the verified run from the root, then keep your hands off the stack. |
| `trace-forensics` | Trace forensics: You own the diagnosis from the artifact. |
| `visual-parity` | Visual parity: You own pixel-exact equivalence. The baseline is the spec. You do not touch it. |
| `worktree-cleanup` | Worktree and simulator cleanup: Reply: |

#### Agents (2)

| Name | What it does |
|---|---|
| `comment-sicko` | A deranged comment-hater that savors deletion and condemns workaround code. |
| `poteto-agent` | Delegate subagent for code-writing and helper tasks spawned during a `/poteto-mode` run. Use for delegates, not as the runner for `/poteto-mode` itself. Spawn a fresh `poteto-agent` for each new task, and resume one only in the strict … |

#### Benny automation skills (3)

| Name | What it does |
|---|---|
| `reproduce-and-fix-issues` | Reproduce triaged Slack bugs through a configured app-control adapter, verify existing fixes, and open a bounded draft pull request only after before-and-after proof. Use only from the configured Benny repro automation. |
| `setup-benny` | Configure Benny and prepare its triage and repro automations. Use when installing Benny or changing its Slack, tracker, repository, routing, control, model, or budget settings. |
| `triage-issue-reports` | Triage Slack issue reports with one thread-only verdict, evidence review, cause-aware routing, tracker dedupe, and fail-closed ticket creation. Use only from the configured Benny triage automation. |

The `poteto-mode` folder also holds a `bugbot-triage` reference, plan-check and worktree scripts, and a ten-part guide under `docs/guide`.

### 3.3 Matt Pocock: `mattpocock/skills`

Version read: commit 4ae2317, 31 October 2026

#### Engineering (20)

| Name | What it does |
|---|---|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked … |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs … |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR. |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `implement` | Implement a piece of work based on a spec or set of tickets. |
| `implement-spec` | Implement the result of /to-spec and /to-tickets in code. |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `pr` | Use when writing a PR body. |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. |
| `research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. |
| `retro` | Conduct a retrospective on a coding session. |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed. |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real … |
| `triage` | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. |
| `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. |
| `wizard` | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off … |

#### Productivity (7)

| Name | What it does |
|---|---|
| `grill-me` | A relentless interview to sharpen a plan or design. |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `teach` | Teach the user a new skill or concept, within this workspace. |
| `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| `wait-what` | Stop. That last message did not land: re-pitch it. |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |

#### Misc (4)

| Name | What it does |
|---|---|
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude … |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. |

#### In progress (not yet released) (8)

| Name | What it does |
|---|---|
| `chief-of-staff` | Pursue a long-running goal in a single session by co-ordinating subagents. |
| `claude-handoff` | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| `loop-me` | Grill me about specs for the workflows I want to build, within this workspace. |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked. |
| `software-factory` | Shared language for designing a software factory: the tasks it runs and the services it plugs into. |
| `writing-beats` | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| `writing-fragments` | Writing, explore: mine raw fragments, no structure yet. |
| `writing-shape` | Writing, exploit: shape raw material into an article, paragraph by paragraph. |

The `deprecated` bucket is empty by design: retired skills are deleted.

## 4. Overlaps

Where two or three packs solve the same job, with the pick for GET AI. The pick is a proposal.

| Job | Addy | Pocock | Tan | Pick for GET AI, and why |
|---|---|---|---|---|
| Clarify the ask by interview | `interview-me`, `idea-refine` | `grill-me`, `grill-with-docs`, `grilling` | `in-your-own-words`, `sharpen` | Pocock's grilling, already in V3.1 section 6.2. It adds facts versus decisions and a confirmation gate, which Addy's version lacks |
| Shared language and decisions | `documentation-and-adrs` | `domain-modeling` (glossary, ADRs) | `principle-model-the-domain`, `why` | Pocock for `glossary.md` and ADRs. Tan's `why` for digging up past decisions from ADO and Teams |
| Write the spec | `spec-driven-development`, `/spec` | `to-spec` | none, deliberately | Spec Kit with the GET AI preset, as the plan already says. Do not run a second spec process |
| Break into tasks | `planning-and-task-breakdown`, `/planning` | `to-tickets` (tracer-bullet tickets with blocking edges) | `multi-phase-plan`, `principle-sequence-verifiable-units` | Pocock's blocking edges map to ADO predecessor links. Use as ideas for the Story Planner |
| Foggy, huge work | none | `wayfinder` | `figure-it-out` | Wayfinder, already in V3.1 section 6.7 |
| Build in thin slices | `incremental-implementation`, `/build` | `implement` | `feature` playbook | Addy's thin-slice rule and Pocock's `implement` for the executor. Tan's playbook for the throughput checkpoint idea |
| Test first | `test-driven-development`, `/test` | `tdd` | `tdd`, `principle-test-behavior-not-implementation` | Pocock's red before green, already in V3.1 section 5.12. Tan's rule to skip when the test path is expensive suits `tests/dev/` only |
| Prove it in the real app | `browser-testing-with-devtools` | none | `create-verification-skill`, `maintain-verification-skill`, `principle-prove-it-works` | Tan. This is the model for `lcp-verify`. Addy's DevTools skill is not needed because the plan uses Playwright |
| Code review | `code-review-and-quality`, `/review`, 4 personas | `code-review` (standards and spec) | `interrogate`, `blast-radius` | Pocock's two axes are already in the gate. Add Tan's `blast-radius` to the spec pass. Borrow Addy's extra axes and personas for size L |
| Adversarial or multi-model review | `doubt-driven-development` | none | `interrogate`, `arena` | Addy's doubt-driven development for size L. Tan's multi-model skills only where the client's residency tier allows other models |
| PR body and evidence | `git-workflow-and-versioning` | `pr` | `opening-a-pr` playbook, `show-me-your-work` | Pocock's `pr`, already the basis of the PR body template |
| Debugging | `debugging-and-error-recovery` | `diagnosing-bugs` | `bug-fix` playbook, `principle-fix-root-causes`, `principle-attack-the-premise` | Pocock's tight feedback loop first, plus Tan's rule that the failing repro lands before the fix |
| Simplify and delete | `code-simplification` | `improve-codebase-architecture` | `principle-laziness-protocol`, `principle-subtract-before-you-add`, `principle-minimize-reader-load` | Tan's principles seed the standards pass. Addy's Chesterton's fence matters for deleting flows and columns |
| Design exploration | `api-and-interface-design` | `codebase-design`, `prototype` | `architect`, `arena`, `principle-exhaust-the-design-space` | Pocock's `prototype`, already in V3.1. Tan's `architect` for Dataverse and solution shape before a build |
| Handoff and resuming | `context-engineering` | `handoff` | `recall`, `ketchup`, `session-pickup` playbook, `pause-safely` playbook | Tan's `recall` and `session-pickup` for resuming. The plan's handoff files and PARK protocol already cover the night |
| Learning loop | none | `retro` | `reflect`, `correct`, `principle-encode-lessons-in-structure` | Pocock's `retro` is in V3.1 as a human-led weekly routine. Tan's `correct` adds a ladder for making a mistake impossible |
| Quality bar and guardrails | `constraint-driven-development`, hooks | `git-guardrails-claude-code`, `setup-pre-commit` | `correct`, `principle-boundary-discipline` | Addy's constraints, as the written contract behind `danger-rules.yml` and `coding-standards.md` |
| Parallel work | `/ship` fan-out to personas | `implement-spec` | `swarm`, `arena`, `orchestrate` playbook, `principle-separate-before-serializing-shared-state` | Plan rule 7: one story, one lane. Use parallelism for day research and gate verifiers, not for night builds |
| Triage reports | none | `triage` | Benny: `triage-issue-reports`, `reproduce-and-fix-issues` | Compare both against the outer loop in plan section 4.5 before building it |
| Release and ship | `shipping-and-launch`, `ci-cd-and-automation`, `deprecation-and-migration`, `observability-and-instrumentation` | none | `shipping` playbook | Addy for the UAT and Prod checklist. Tan's rule that green is not safe |
| Security and performance | `security-and-hardening`, `performance-optimization`, personas | none | `benchmark-checklist`, `principle-explain-the-number` | Addy's security skill for size L. Performance is out of scope for now |
| Explain and restate | none | `teach`, `wait-what` | `teach`, `how`, `why`, `bro`, `ketchup` | Tan's `how` and `why` for understanding an existing solution. `bro` is already installed here |
| Writing style | `documentation-and-adrs` | `writing-for-agents`, 3 writing skills | `unslop`, `technical-writing`, `no-comments` | Adapt Tan's `unslop` and `technical-writing` to GET AI's Australian English and no em-dashes |
| Router for the pack | `using-agent-skills` | `ask-matt` | `poteto-mode`, `poteto-help` | Write a GET AI router that routes by T-shirt size (see `tshirt-sizing.md`). Study all three first |

## 5. What fits GET AI

How verdicts were decided, in order: does it fit a step the plan already has; does it conflict with one of the 19 rules; does it work for story-sized Power Platform change; does it suit the sizes in `tshirt-sizing.md`; is it small enough not to bloat context.

Verdicts:

- **Adopt:** the idea or the skill fits and the plan has a gap. Read it in full, then vendor or rewrite.
- **Adapt:** the idea fits but the skill must be rewritten for Power Platform or for the gate.
- **In V3.1:** the plan already includes it.
- **Reference:** read it for ideas. Do not install.
- **Skip:** not relevant now.

### 5.1 What the three packs do not give you

- Anything about Power Platform, Dataverse, solutions, flows, Copilot Studio or pac.
- The environment pool, lane locks, identities, the gate repo, the ledger or the trust ladder mechanics.
- A way to prove a Power Platform app works. Tan's `create-verification-skill` shows the method. `lcp-verify` is still ours to build (plan section 5.9).

### 5.2 Skills that fit, with where they go

The Sizes column uses the T-shirt sizes defined in `tshirt-sizing.md`: XS, S, M, L and XL.

| Skill or group | Pack | Verdict | Where it fits in GET AI | Sizes | Why |
|---|---|---|---|---|---|
| Excuse tables (a list of excuses an agent uses to skip a step, with a rebuttal) in every skill | Addy | Adopt | `lcp-executor` and `lcp-evaluator` prompts | S to L | Cheap. Targets the failure the plan names first: the worker declaring itself done |
| `constraint-driven-development`, `/constraints` | Addy | Adopt | The written contract behind `danger-rules.yml`, `coding-standards.md` and `trust.yml` | M, L | Records the quality bar with numbers and watches the diff for a lowered bar. Matches rule 2 and the tamper checks |
| `source-driven-development` | Addy | Adopt | Executor and test author | S to L | Grounds work in official docs. Power Platform changes fast, and the plan values primary sources |
| `incremental-implementation` | Addy | Adopt | `lcp-executor` rules | S, M | Thin vertical slices with a check after each. Fits TDD at seams |
| Core operating behaviours in `using-agent-skills` (surface assumptions, stop on confusion, push back, enforce simplicity) | Addy | Adapt | Executor rules and the PARK protocol | S to L | Close to the plan's facts-versus-decisions rule. Stop on confusion becomes a PARK |
| `doubt-driven-development` | Addy | Adapt | Verifier or reviewer when the floor is 6 or more, and before a one-way-door PARK | L | An adversarial pass during the build. Too costly for S and M |
| `code-review-and-quality`, `security-auditor` and `test-engineer` personas | Addy | Adapt | Rubric ideas for size L; `test-engineer` informs the `test-author` agent | L, day gate | The plan already has two review axes. Add axes only where the danger is high |
| `security-and-hardening` | Addy | Adapt | Size L: security roles, API and connector changes | L | Needs Dataverse security content added. Security roles already have floor 7 |
| `deprecation-and-migration` | Addy | Adapt | One-way doors such as dropping or renaming a column | L | Its expand-then-contract method gives a safe route around the plan's floor-8 and floor-9 changes |
| `shipping-and-launch`, `/ship` fan-out | Addy | Adapt | UAT and Prod promotion, plan section 5.15 | M, L | A go or no-go checklist with a rollback plan |
| `/build auto` | Addy | Adapt | Compare with the 17:00 night plan approval | S to M | One approval, then each task test-first, stopping on failure. The stop becomes a PARK or NEEDS_WORK |
| `create-verification-skill`, `maintain-verification-skill` | Tan | Adopt | The method for building and reviewing `lcp-verify` and its verify profiles | S to L | De-risks stage 2. The maintain skill matches the weekly profile coverage check |
| `blast-radius` | Tan | Adopt | Spec pass of the review agent | M, L | Finds what a change could break elsewhere and proves one fact by running real code |
| `show-me-your-work` | Tan | Adopt | A decision trail for unattended and multi-phase runs | M, L | Adds a per-decision log to the plan's handoff files |
| `correct` | Tan | Adopt | The weekly routine, plan section 7.3 | All | Makes a repeated mistake impossible by trying architecture first, then types, then a lint, then a test, then docs last. Each check must fail on a real past mistake |
| `how`, `why` | Tan | Adopt | Day gate and night facts-first lookups | M, L | `why` queries ADO, Teams and Git for past decisions. Fits rule 9: look facts up |
| `recall`, `session-pickup` playbook | Tan | Adopt | Resuming work, mining past sessions | All | Same job as `docs/progress.md` for this project |
| `pause-safely` playbook | Tan | Adapt | PARK protocol wording | M, L | Compare with plan section 5.11 |
| `bug-fix` playbook | Tan | Adapt | The Spec Kit bug workflow and triage repro | S, M | Reproduce on the same surface. Land the failing repro before the fix |
| `trace-forensics` playbook, `reflect` | Tan | Adapt | The `trace-reviewer` agent, weekly routine | All | Keep the retro human-led, as Pocock advises. Do not automate it |
| `shipping` playbook | Tan | Adapt | Merge queue rules, plan section 5.10 | M, L | "Green is not safe": no arming before an independent per-PR verdict |
| `architect` | Tan | Adapt | Data model and solution shape before a build | M, L | Sketch types and structure before code. For Dataverse this means the schema plan |
| `arena`, `swarm` | Tan | Adapt | Day work only: design bake-offs and research coverage | L, XL | Cost and residency limits. Never for night story builds |
| `interrogate` | Tan | Adapt | Contested design at size L | L | Multi-model. Only where the residency tier allows other models |
| 13 principles: `laziness-protocol`, `subtract-before-you-add`, `minimize-reader-load`, `prove-it-works`, `fix-root-causes`, `test-behavior-not-implementation`, `boundary-discipline`, `make-operations-idempotent`, `separate-before-serializing-shared-state`, `sequence-verifiable-units`, `build-the-lever`, `encode-lessons-in-structure`, `guard-the-context-window` | Tan | Adopt | Seed for `coding-standards.md`, read by the standards pass | All | Short and checkable. Idempotency and shared state match retries and lane locks |
| 4 principles: `model-the-domain`, `type-system-discipline`, `foundational-thinking`, `attack-the-premise` | Tan | Adapt | Schema design, code apps and plug-ins; the RESTART rule | M, L | `attack-the-premise` fits the plan's rule: restart when a criterion fails twice |
| `unslop`, `technical-writing` | Tan | Adapt | Client-facing docs, PR text, specs | All | Rewrite to GET AI's Australian English and no em-dashes |
| Benny `triage-issue-reports`, `reproduce-and-fix-issues` | Tan | Adapt | Compare with the outer loop, plan section 4.5 | Outer loop | A built example of triage, repro and a draft PR only after before-and-after proof. The plan's version is untested |
| `ask-matt` | Pocock | Adapt | A GET AI router that routes by size | Day | Shows main flow, on-ramps and phase boundaries on one page |
| `wizard` | Pocock | Adapt | Lane bootstrap and PARK steps that only a human can do | Bootstrap | Generates a guided script for steps only a human can do, such as credentials, CI secrets, unfamiliar dashboards and cutovers. Fits the OAuth connections and consents in lane bootstrap |
| `to-questionnaire` | Pocock | Adapt | Day gate and PARK `ambiguity` questions for clients and PMs | M, L, XL | Turns a decision you cannot answer into a questionnaire |
| `triage` | Pocock | Adapt | The outer loop on-ramp | Outer loop | A state machine of triage roles that ends in an agent-ready brief |
| `diagnosing-bugs` | Pocock | Adapt | Hard bugs, by day | M, L | Builds a tight feedback loop before theorising |
| `to-tickets` | Pocock | Adapt | Story Planner and ADO predecessor links | M, XL | Tracer-bullet tickets with blocking edges |

### 5.3 Already in V3.1

| Skill | Pack | Where the plan uses it |
|---|---|---|
| `grilling`, `grill-me`, `grill-with-docs` | Pocock | Section 6.2: one question at a time, facts versus decisions, confirmation gate |
| `domain-modeling` | Pocock | Section 6.2: `glossary.md` and `docs/adr/` |
| `wayfinder` | Pocock | Section 6.7: discovery maps in ADO |
| `research` | Pocock | Sections 4.6 and 6.7: overnight research tickets |
| `prototype` and the `prototype` playbook | Pocock, Tan | Section 6.7: throwaway prototypes, never promoted |
| `tdd`, `implement` | Pocock | Section 5.12: red before green at the seams |
| `code-review` | Pocock | Section 5.10 and Appendix B.4: standards pass and spec pass, named smells |
| `pr` and the `opening-a-pr` playbook | Pocock, Tan | Appendix C.7: the PR body template. Merge Danger, doors and blast radius came from here |
| `retro` | Pocock | Section 7.3: human-led, on a sample of real sessions |
| `bro` | Tan | Installed in this repo as `.claude/skills/bro` |
| `documentation-and-adrs` | Addy | Covered by `docs/adr/` in section 6.2 |

### 5.4 Reference only, and Skip

| Verdict | Addy | Pocock | Tan |
|---|---|---|---|
| Reference | `api-and-interface-design`, `ci-cd-and-automation`, `code-simplification`, `context-engineering`, `debugging-and-error-recovery`, `git-workflow-and-versioning`, `idea-refine`, `interview-me`, `observability-and-instrumentation`, `planning-and-task-breakdown`, `test-driven-development` (its Prove-It pattern for bugs is the useful part; Pocock's `tdd` covers the rest); commands `/planning`, `/review`, `/test`, `/code-simplify`; persona `code-reviewer`; the seven checklists | `codebase-design`, `improve-codebase-architecture`, `implement-spec`, `to-spec`, `handoff`, `teach`, `wait-what`, `chief-of-staff`, `loop-me`, `software-factory`, `git-guardrails-claude-code`, `writing-for-agents` | `automate-me`, `figure-it-out`, `in-your-own-words`, `ketchup`, `poteto-mode`, `setup-pstack`, `sharpen`, `statechart`, `tdd`, `teach`, `create-formal-verification-skill`, `maintain-formal-verification-skill`, `poteto-agent`; principles `redesign-from-first-principles`, `exhaust-the-design-space`, `experience-first`, `outcome-oriented-execution`, `migrate-callers-then-delete-legacy-apis`, `explain-the-number`; playbooks `autonomous-run`, `feature`, `investigation`, `multi-phase-plan`, `orchestrate`, `refactoring`, `runtime-forensics`, `eval`, `hillclimb`, `authoring-a-skill`, `autopilot-full`, `autopilot-stack` |
| Skip | `browser-testing-with-devtools`, `frontend-ui-engineering`, `performance-optimization`, `spec-driven-development`; commands `/spec`, `/webperf`; persona `web-performance-auditor`; the hooks | `setup-matt-pocock-skills`, `migrate-to-shoehorn`, `scaffold-exercises`, `setup-pre-commit`, `claude-handoff`, `setup-ts-deep-modules`, `writing-beats`, `writing-fragments`, `writing-shape` | `benchmark-checklist`, `ketchup-video`, `make-bot-ui`, `no-comments`, `poteto-help`, `typescript-best-practices`, `comment-sicko`, Benny `setup-benny`; playbooks `babysit`, `perf-issue`, `visual-parity`, `worktree-cleanup` |

Why the notable ones are skipped or kept at reference:

- `spec-driven-development`, `/spec`, `to-spec`: the day gate runs Spec Kit. The plan runs one spec process.
- `browser-testing-with-devtools`: the plan's verifiers use Playwright, which has Power Platform page objects.
- `implement-spec`: it runs subagents on an integration branch. That conflicts with one story, one lane, one PR (section 5.5).
- `statechart` and the formal verification skills: approvals and flows are state machines, so these may matter later. Too heavy for now.
- `frontend-ui-engineering`, `performance-optimization`, `typescript-best-practices`: aimed at web code. Revisit for the code apps profile.

### 5.5 Where the packs conflict with GET AI's rules

| Conflict | Pack and skill | GET AI rule | Proposed resolution |
|---|---|---|---|
| Do not block on the human; mid-run discoveries are yours | Tan: `principle-never-block-on-the-human`, `autonomous-run` | Rule 9 and the PARK protocol: look facts up, ask only for decisions, PARK on decisions and one-way doors | Keep Tan's rule for reversible facts. Decisions and one-way doors still PARK |
| Agents merge their own PRs | Tan: `autopilot-full`, `autopilot-stack` | Rules 1 and 12: humans merge; auto-merge is a rung earned per change class | Reference only until a class reaches L2 |
| No planning; the best spec is the code | Tan: deliberate gap | Day gate: a high-level spec and locked scenarios by someone else | Keep the spec. A night agent cannot ask. Keep Tan's point: when reality breaks an assumption, PARK instead of guessing |
| Subagents on an integration branch | Pocock: `implement-spec` | Rule 7: one story, one lane, one branch, one PR | Use only for code lanes if at all. Pocock himself rates a scripted loop as more reliable |
| Approve once, then run everything | Addy: `/build auto` | The 17:00 night plan approval plus a gate per PR | Compatible if the approval is the night plan and a failure becomes a PARK |
| Two spec processes | Addy `/spec`, Pocock `to-spec` | Spec Kit by day | Pick Spec Kit |
| Multi-model review | Tan: `interrogate`, `arena` | Rule 15 and residency tiers T1 to T4; model pins in section 9.3 | Allow other models only where the client's tier permits |
| Cursor-specific features | Tan: Cursor subagents, `/loop`, model names | Copilot CLI or Claude Code on a runner | Rewrite the playbooks rather than port them |
| Skills that trigger themselves | Addy (all 25), some of Pocock | The executor prompt names the skills it uses | Install only skills that run when invoked, or turn self-triggering off |
| Doing the retro automatically | Tan: `reflect` | Plan section 7.3: do not automate the retro | Keep a human in the loop |

## 6. Limits of this review

- Verdicts rest on skill descriptions, the three routing documents, and the first part of about a dozen skills. Most skill bodies were not read.
- Portability and star counts come from the video and Pocock's transcripts. They were not checked.
- The pick column in section 4 and every verdict in section 5 are proposals.
- The packs change often. Versions are recorded in section 2.

