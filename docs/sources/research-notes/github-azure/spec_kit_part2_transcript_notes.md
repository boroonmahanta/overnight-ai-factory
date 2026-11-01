# Spec Kit Part 2 transcript notes: "Open Source Friday: Spec Kit Part 2"

Source: transcript supplied by the reader on 25 October 2026. Video: https://www.youtube.com/watch?v=8hHCpNVLhmI (Open Source Friday, GitHub, 16 October 2026, per the earlier research). Host: Sarah Kaiser (GitHub). Guests: Manfred (principal software engineer at GitHub, Spec Kit maintainer) and Nicole Hogan (principal software engineer at GitHub). Cite as [Spec Kit talk mm:ss] with the video URL, marked [user-supplied transcript]. The earlier Spec Kit research is in research_notes/Overnight AI software factory/spec_driven_development_requirements.md; this transcript adds to it and does not replace it.

## Releases and growth (4:47 to 5:28)
- 1.0 released on the project's birthday; now at 1.2 (the earlier research lists 1.0.0 on 21 August 2026 and 1.2.3 on 22 October 2026).
- Since May 2026: stars almost doubled; community extensions doubled; presets growing the same way.

## New primitives (5:35 to 7:02)
- Presets: "if you're using it in a team... you can actually layer in your own stuff". Presets are where you encode "standardized ways of working" (36:44 to 37:04).
- Bundles: "a vetted set of things": a valid set of extensions, presets or workflows packaged together (6:02 to 6:23).
- Workflows: "we had one workflow now we have five" (6:23). Workflow steps can now be hosted like other primitives; 13 core steps, and you can add your own steps (6:37 to 7:02).

## Before and after spec-driven development (7:07 to 8:52)
- Before SDD, a core extension assesses an idea "on the merit of how does it fit the project". Verdicts: go, kill, or needs more clarification (7:29 to 7:54). Canvas pipeline: intake, research, shape, define, decide (31:10, 34:47). It asks clarifying questions using the Copilot app's tool for asking the user (31:40 to 31:58). "Did you consider this? Did you consider that?" (54:16). The host calls it "a pocket PM" (55:02); Manfred: if you are a PM, use it and make it your own with presets.
- It also lets you push back on a filed issue: "is it something that actually fits the code base or is it something that I should push back on" (54:47).
- After SDD, a bug fix workflow: assess the bug (verdict: valid bug or not), fix, then test that the fix fixed the bug (8:12 to 8:32, 32:34 to 33:13). Bug fixing is "not normally a whole SDD flow".
- "Create your own process" through a capability list. "It's more kit than spec" (8:52); "it really is now become a process kit" (56:24).

## Converge (9:29 to 12:30)
- New core command after implement: "implemented but did it actually adhere to the spec? If it didn't, converge will actually create new tasks that implement needs to go do to converge onto the spec."
- It reads the spec, the plan, the tasks and the code base and asks: "Did I overreach? Did I under-deliver? Did I break something?"
- Append-only to tasks.md, "like a loop where you go... make that tighter and tighter... or a funnel": an asymptotic approach.
- It came out of community extensions; some community extensions do it differently and are not obsolete.
- The earlier research found converge audits by reading code and does not run tests, so it is a traceability sweep, not a behaviour check.

## Experimental MCP server mode (10:38 to 11:17)
- The specify CLI can run in MCP mode, slowly gaining the same functionality. Not intended for running the commands, "because obviously the commands are still the prompts that the agent needs to execute". Highly experimental and not in the capability list.

## Agent-agnostic core (24:54 to 26:32)
- `specify init` takes the coding agent (Copilot, Claude, Codex and so on) and generates the matching skills for that agent. A project can use multiple agents, switching with "use".
- Extensions are delivered agent-agnostically; on install they create a skill file for the chosen coding agent. So teams on different agents share the same core instructions.
- Layering: core Spec Kit (agnostic), then the Copilot plugin, then the canvases.

## spec-kit-copilot sibling repo (13:20 to 14:17, 17:38 to 18:19)
- A separate, open-source repository keeps Copilot-specific pieces out of the agnostic core.
- Five plugins: `speckit-copilot` (drive Spec Kit in natural language; skills call the specify CLI underneath) and four canvas plugins.
- Demo in the GitHub Copilot app (released about June to July 2026, "geared towards agent first development", multiple repos and sessions side by side): "initialize my project" in plain words loads the init skill; it scaffolds per-phase skills (constitution through implement); artefacts land in `.specify/`; it then prompts for a constitution. Demo constitution: "for every single change I want docs and tests added" (19:07 to 24:10).

## Canvases (26:40 to 36:11, 39:13 to 43:38)
- Canvases are web apps inside the GitHub Copilot app. They need the Copilot app; the core artefacts can be produced from the plain CLI without them (32:09).
- Three workflow canvases: SDD (badges per state, view the constitution, run specify with a feature id, view and rerun each phase's artefact), idea assess (intake to decide, with a verdict and clarifying questions to answer before rerunning a stage), and bug fix (assess, fix, test).
- Wizard canvas: browse presets and extensions across catalogues (built-in, Copilot-specific, community), install them, and build a pipeline on a phases tab (for example idea assessment commands followed by specify), then run it.
- Experimental, not yet checked in: a "generate canvas" button opens a canvas designer that generates a canvas app from the pipeline metadata, with title, description, badges and logo; presets can further customise the generated app (example: vertical layout and autopilot mode, so a bug can be entered and the pipeline runs on its own).
- Example preset "Pirate Speak" shows presets can change all artefact output.

## Specs as transient: "flow forward" (14:56 to 15:51)
- "I view specs as mostly transient." Flow forward: once delivered, create a new spec for the new work.
- Do not create specs for small changes ("a different color for a toggle button, that's not really a spec").
- The maintainer asks contributors to scrub spec artefacts from PRs to keep the Spec Kit repo clean.
- The earlier research found persistence models are an open topic (issue #4944: flow-back, flow-forward, flow-always "living").

## Token cost and the lean preset (47:24 to 50:10)
- The core SDD flow "delivers a lot of files": API contracts, research, spec, implementation plan, task list.
- A "lean" preset "only creates three files" and "consumes a whole lot less tokens", but is less specified: no API contracts, no research files. Use it for small features. "It all depends on how much you need and how much your organization requires of you to specify."
- You can write your own preset to override the core, for example dropping API contracts but keeping everything else.

## Regulated industries (56:29 to 57:51)
- Host: medical device software had "a binder of all the things you had to check" for every code change; a preset could enforce that.
- Manfred built a preset for the US VA's NIEM information-exchange model in a personal repo, as a community member.

## Architecture notes (50:35 to 52:23)
- The CLI is Python. When commands run, Python is not in play: the agent reasons over the prompt and calls whatever tools the command specifies (Python, bash or PowerShell scripts). Fully decoupled.

## Community (38:15 to 38:55)
- The Spec Kit docs site has a community tab by area (extensions, presets, workflows) and a "friends" page for projects built on Spec Kit (for example a terminal UI).
