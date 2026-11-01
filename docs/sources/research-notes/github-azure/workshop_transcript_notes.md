# Workshop transcript notes: "How to Build Agents That Run for Hours (Without Losing the Plot)"

Source: transcript supplied by the reader on 24 October 2026, from https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript (the page itself is blocked from this environment). Speakers: Ash and Andrew, Applied AI team, Anthropic. Delivered at AI Engineer (Europe), first session. The talk follows Anthropic's March 2026 harness design post. The reader also supplied five slides: "Sprint contracts", "The debugging loop", "The simplified harness, end to end", "Build this loop yourself, today", "Takeaways".

Cite as [talk mm:ss] with the page URL above, marked [user-supplied transcript].

## Problem framing (Andrew)
- Three buckets of failure (2:42 to 4:04): context (finite window, amnesia across sessions, "context rot", "context anxiety" where the model hurries to finish near the end of the window); planning (one-shots everything, builds half a feature and stops); self-judgement ("models are really bad at judging their own output"; a button with no back end "looks done").
- Two fixes: the model weights, and the harness (4:14 to 5:39). METR chart: about 1 hour at 50% task completion for Sonnet 3.7, about 12 hours for Opus 4.6 with a minimal scaffold (4:24, 14:51).
- Model and harness "co-evolve"; harness parts are added to fill model gaps, then removed (5:54, 16:35).

## History of primitives (Andrew)
- Ralph loop (7:55 to 9:43): fresh context per task; "deterministically bad in an undeterministic world"; Anthropic's plugin version runs inside one session with compaction, a max iteration count, a "safe word", and a Stop hook that blocks stopping until done.
- Sonnet 4.5: context-aware token tracking; Claude Code 2.0 checkpoints; Agent SDK renamed from Claude Code SDK (9:59 to 10:41).
- Opus 4.5 for planning plus Sonnet 4.5 as the workhorse; Haiku made many subagents economical; Skills with progressive disclosure (only front matter loaded until used); programmatic tool calling to save context (10:41 to 12:05).
- November 2025 harness (12:05 to 14:20): initializer writes feature_list.json (JSON because models overwrite Markdown more), progress file, git repo, init script; loop: get bearings, smoke test, pick ONE failing feature, implement, verify with Puppeteer, commit, flip to passes, repeat in fresh context.
- Opus 4.6 and Sonnet 4.6: agent teams (subagents can talk to each other), server-side compaction, 1M context GA (14:20 to 15:53). Typical full app builds now 3 to 5 hours (16:25).

## The GAN-style harness (Ash)
- Generator builds, evaluator grades, separate context windows and system prompts. The evaluator "isn't just reading diffs" but uses Playwright to open live pages and click around, then hands critique back (18:42 to 19:31). Contrast with one session told to check its own work (19:31).
- Why it works: "tuning a standalone critic to be harsh is actually very tractable, but tuning a builder to be somewhat self-critical is not" (20:05).

## Rubrics for subjective quality (21:31 to 22:23)
- "Most people say you can't grade taste, but we think you can if you have a strong enough opinion on it, and you just kind of write it down."
- Four criteria: design, originality, craft, functionality. Weighted towards design and originality. Weights shift with the model in play (Opus 4.6 already strong on functionality).
- Calibrated with few-shot examples of reference sites so "the evaluator's taste converges on our own"; target is avoiding "purple gradients" and "AI slop" aesthetics.
- Frontend-only example: about four hours, 5 to 15 rounds of generator then evaluator (Playwright navigate, screenshot, score on four criteria, write critique) (22:32 to 22:49).
- Pivots: if the generator keeps scoring low on one criterion, the harness "will just throw the whole thing out and try again from scratch"; a single loop "keeps trying to patch the same thing" (23:08 to 23:42). Q&A (47:11): the 4.6 models were "extremely willing to throw away everything" even after 10 passes; the evaluator sometimes asks to "delete everything and restart".
- Q&A (40:35 to 41:21): the evaluator tuning was designed to be reusable across projects, not per project; good-design versus AI-slop examples "generalize quite well".
- Q&A (63:19 to 65:31): rubrics are set "in extreme detail" at the generator and evaluator level, for design, API design, code quality and so on. Quality signal is where a run started and ended on those criteria; "not super comparable across different products and runs" but useful within one. Brownfield: point the evaluator at the codebase plus the spec and start the loop from there. The pattern is opinionated (React, Postgres, Node) and needs tailoring.

## Planner (23:59 to 24:56)
- Turns a one-line prompt into "a very deliberately high-level kind of spec", split into sprints (in the older version).
- It does NOT plan granular technical details, because an early error "is going to cascade through every single one of these sprints" and "magnify errors over a multi-hour time horizon".
- Org analogy: PM, IC, QA, each with its own context window.
- Q&A (49:51 to 50:42): the main spec is inserted into the generator and evaluator sessions "regularly" as a reference point. The planner is deliberately NOT part of the loop; it sets "the hard outer lines of what this product could be".

## Sprint contracts (25:12 to 26:46, slide "Sprint contracts")
- Before code, generator and evaluator negotiate what "done" means for the chunk. Generator proposes "I'm gonna build X feature and you should verify it by testing Y". Evaluator may push back: scope too big, tests too weak, missed edge cases. Back and forth via Markdown files on disk until both agree. Then build.
- The evaluator grades against the contract, not the original spec.
- Purpose: bridge user stories (spec) to "tangible, testable assertions" without the planner over-specifying up front. "The key innovation that the Ralph loop never really had": nobody on the other side arguing with the main loop.
- Granularity (32:04 to 32:40): the retro game maker had 27 contract criteria. "If you have vague criteria, you have vague critiques... Whereas if you have granular criteria, the agent knows, okay, I need to fix this exact line."
- Slide "The simplified harness": sprint contracts are listed as REMOVED ON OPUS 4.6, together with context resets, sprint decomposition and the per-sprint eval loop.

## Results (27:03 to 31:49)
- Prompt "Build a retro game maker". Solo loop: looks fine, play mode broken (arrow keys and space do nothing); the agent "didn't have any idea how to test itself".
- Full harness: about USD 200 and six hours. Planner added product features nobody asked for (new project dialogue, an AI level assistant from one vague line). The app added a debug HUD "to make life easier for the evaluator" (30:37). Play mode works.
- Evaluator catches: FastAPI route ordering that "passes every unit test but might actually break in prod"; a delete key Boolean logic bug. "Only caught because the evaluator's actually using the app" (31:19 to 31:49).
- Simplified harness on a newer model (DAW example): "roughly like half the cost of the previous runs", still a very extended run, "a couple rounds" (36:39 to 37:48).

## Evaluator honesty and the debugging loop (32:40 to 34:08, slide "The debugging loop")
- "Out the box, Claude is a really, really bad just general QA agent." Same sycophancy and generosity bias as LLM-as-judge. Early runs: finds a bug, says "fix it later".
- "The primary debugging loop was this, and not necessarily running more experiments. It was reading what the agent actually did, finding where its judgment diverged from ours as humans, and then tuning the prompt for that."
- Tooling tip: pipe agent transcripts into files, have another agent go through them and update the prompts.
- Q&A (61:57 to 62:45): mostly reading traces by hand; Claude pointed at traces with custom prompts as a first pass; "by far and away the best approach is just reading the traces by hand".
- Q&A (73:25 to 74:41): "No, you gotta read the whole thing." Empathise with the model.
- Q&A (70:02 to 70:25): run the harness many times (for example ten generations, three succeed, seven fail), read the seven, adjust the harness prompting, repeat until happy to leave it fully autonomous.

## Evaluator isolation (60:03 to 61:04)
- A critic that gets the generator's context or traces: "I would be very hesitant of that... muddying of thoughts between the two model streams." Better to "just let it judge the output". The evaluator states the issue; the generator reflects on its own work and fixes it. Otherwise "it's very easy for the model to kid itself".

## Adjusting the harness as models improve (34:14 to 36:08)
- Find each model's "spiky behaviours" and fill the gaps.
- Context resets dropped: Opus 4.5 had bad context anxiety, Opus 4.6 did not; one continuous session plus compaction was enough.
- Sprint decomposition: critical for Opus 4.5; Opus 4.6 held "a two-hour continuous build coherently".
- Evaluator cadence: was every sprint, now once at the end of a one-shot generation, then pass back.
- "The lesson isn't necessarily our harness was wrong, but rather it was right for 4.5, the frontier moved."
- Q&A (42:29 to 43:53): fresh sessions versus one long session "is probably still up to your use case and your evals"; context rot is "a temporary problem"; "I'd be hunting for the model release where I can kind of strip it out."
- Q&A (52:43 to 53:50): model selection informs harness design. Common pattern: Opus for planning, Sonnet for coding. Build evaluations per subagent, model and prompt.

## Build it yourself (37:58 to 38:52, slide "Build this loop yourself, today")
- Auto mode: "safe YOLO" instead of --dangerously-skip-permissions.
- Custom subagents for the evaluator and QA role: "give it a harsh system prompt and a very detailed rubric".
- Playwright MCP or Claude for Chrome MCP; computer use for native apps.
- Skills to package grading rubrics.
- Slide: "The harness patterns that work tend to get absorbed back into the tools."

## Takeaways slide (38:52 to 39:51)
1. Self-evaluation is a trap. Use an adversarial evaluator.
2. Compaction doesn't cure coherence drift. Structured handoffs do. ("Lossy summaries really drift.")
3. Make subjective quality gradable with rubrics the model can apply.
4. Read the traces. They're your primary debugging loop.
5. Delete scaffolding when the model catches up. The frontier moves.

## Other Q&A points
- Human in the loop (46:44, 69:11): use hooks at a stop condition to hand back to a human, allow a developer message, continue. Their goal is no human in the loop; they prefer to fix the harness rather than insert a human.
- Long-lived products and handoff to humans (54:08 to 56:04): file system as state; embed prompting that writes learnings and state to a JSON file (models overwrite JSON less): a timestamped log of "tried this, evaluator found this bug, implemented this fix, this fix worked, yes". Plus a live, high-level doc of the file structure. "Those two files are more than enough for Claude Code and a human to come in and start iterating."
- Agent teams versus generator and critic (57:12 to 59:53): compatible. Front end, back end and integrator subagents "each probably deserve their own critic". The Agent SDK runs in a cloud sandbox for long periods; Claude Code on a laptop needs the machine awake.
- Multi-step workflows (51:00 to 51:57): the generator and evaluator pair can be repeated across a workflow (planner, generator plus QA, integrator plus QA, and so on).
- Collaboration on harnesses (66:04 to 67:40): bottom-up adoption, an owner maintains and generalises it; observability for ultra-long agents is "a thing which is not fully solved yet"; use version control, PRs and git worktrees.
- Brownfield (71:00 to 72:06): the pattern suits greenfield; brownfield needs more control and custom rubrics. Brownfield SDLC automation: monitoring raises an issue, an agent makes the PR, a review runs, a human reviews before merge.
- Learnings go into prompt templates, CLAUDE.md or skills (74:44).
