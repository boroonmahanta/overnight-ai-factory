---
name: ask-me
description: Ask which GET AI flow fits the work in front of you. Picks the T-shirt size first, then routes to the right day or night path, skills and human gate. Use at intake, when unsure what to do next, or when starting a session.
disable-model-invocation: true
---

# Ask me

Adapted from `ask-matt` by Matt Pocock (MIT, commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, copy in `skills/pocock/ask-matt/`). Matt's router sends one person from idea to ship. This one sends GET AI work by size and by day or night, under the 19 rules in `CLAUDE.md`.

Plain language. Australian English. No em-dashes. Ask Boroon at most one question at a time.

Before you say what a skill does, check the status tag below. Do not point at a skill that is not live. Say it is on the shelf or planned, and give the manual step instead.

Status tags: **live** (in `.claude/skills/`), **shelf** (in `skills/`, read, not adopted), **planned** (named in the plan or `tshirt-sizing.md`, not written). `lcp-*` skills are GET AI versions adapted from the shelf originals.

## Step 1. Where are we?

Read `docs/progress.md`. It says what was decided and what is next. Then work out which of these you are in:

1. **New work arriving** (a story, a change, a client report). Go to step 2.
2. **Blocked on a person** (an answer, a login, a decision). Go to "When you are stuck".
3. **Checking or reviewing something built.** Go to "Checking work".
4. **Improving the factory itself** (skills, rubrics, gate, standards). Go to "Changing the factory".

## Step 2. Pick the size

Ask these in order. The size is the **largest** answer, never the average. The spec owner proposes it. The gate can raise it, never lower it.

1. **Reversibility.** Any one-way door (dropped data, security role, money logic, deploy settings, anything sent outside)? Then L.
2. **Blast radius.** Touches another app, flow, agent or shared table? At least M.
3. **Clarity.** Can every behaviour be a locked scenario today? If not, M with a grilling session, or XL if nobody can say what the stories are.
4. **Verifiability.** Can `lcp-verify` prove it? If not, go up one size and add a human check. New-harness Copilot Studio agents are the known case.
5. **Effort.** More than about 40 minutes of agent work? Probably not one night story.
6. **Residency.** What is the client's tier? T3 limits models. T4 rules out the factory.

If any answer is "I do not know", that is a fact to look up or a decision to ask by day (rule 9). It is never a guess.

## Step 3. Route by size

| Size | Merge Danger floor | Verifiers | Path | Human gate |
|---|---|---|---|---|
| **XS** | 0 to 1 | 1 | Day work with AI, or batch into a night S | A glance at before and after screenshots |
| **S** | 0 to 2 | 1 | Lean preset, 1 to 3 clarify questions, locked scenarios. Night story, Lane B Power Platform profile | Morning approval at L1 |
| **M** | 3 to 5 | 2 (3 if another app or flow is in the blast radius) | Full `getai-lcp` preset. Mock or throwaway prototype. A different person writes the scenarios and the held-out set. Night story, or Lane A past about 40 minutes | Human approves every PR with the blast radius shown |
| **L** | 6 to 10 | 2 to 3, plus a human check | M plus an expand-then-contract plan for schema changes. Night story only if the spec is locked, otherwise day work | Human reads the one-way door. A second reviewer at 8 or more on client work. Never auto-merged |
| **XL** | each child gets its own | | Not a night unit. Wayfinder map in ADO first, then split into S, M and L stories with predecessor links | Acceptance owners approve the split before any story is queued |

Then: write the size on the story, get **Factory Eligible** set by a human only when spec, locked scenarios, held-out set, mocks and prerequisites exist, and let the night shift pick it up.

## The day flow (idea to Factory Eligible)

0. **Intake.** A raw request or draft bug: `lcp-intake` (live) verifies the claim, proposes the size and writes the brief.
1. **Grill the idea.** Facts are looked up. Decisions are asked. Clarify by day only. Status: planned as a GET AI grilling skill; until then follow the grilling rules in plan section 6.
2. **Need to see it?** User-facing change needs an approved mock or throwaway prototype (rule 10). Prototypes are never promoted. Keep the answer, not the code.
3. **Write and lock the scenarios.** Someone other than the builder (rule 3). Put the held-out set where the worker cannot read it (rule 4).
4. **Set the size and Merge Danger floor.** Section above.
5. **Set Factory Eligible in ADO.** A human does this.

## The night flow

Do not try to run this from a day session. The night shift follows the plan: one story per lane under a lock, builder uses the lane copy of `lcp-verify`, the required workflow in the gate repo runs the trusted checks, fresh verifiers click through the app, and Merge Danger is scored by the deterministic floor. If the agent hits a portal-only step or a decision it **PARKs**: it writes `park.json` and the story waits in "Awaiting business". Humans merge in the morning. `main` is always human.

## When you are stuck

- **Need an answer from someone else** (acceptance owner, client IT, Partner Center for spike 0.1): `lcp-questionnaire` (live). It writes a short questionnaire.
- **Only a human can do the step** (portal click, consent, admin login, Entra app, secrets): this is a PARK at night. By day use `lcp-wizard` (live) to script it for a person.
- **Foggy and too big for one session:** Wayfinder map in ADO (plan section 6). Pocock's `wayfinder` skill is not on the shelf yet, so run the map by hand from the plan.
- **Lost the thread of a client solution:** `lcp-how` for what it does and `lcp-why` for why it is shaped that way (both live).

## Checking work

- **Is the change safe?** `lcp-blast-radius` (live). Prove the one fact it is safe because of by running something. An AI writeup can raise the Merge Danger score, never lower it (rule 11).
- **Is my reasoning sound?** `doubt-driven-development` (live, adopted as is). A fresh reviewer sees the artifact and the contract, not your claim. Stop after 3 cycles. It cannot run from inside a subagent.
- **Is the quality bar being lowered?** `constraint-driven-development` (live, adopted as is), especially its diff check for new suppressions, skipped tests, moved thresholds and new exceptions.
- **Does a feature really work?** `lcp-verify` (planned, stage 2). Use `create-verification-skill` and `maintain-verification-skill` (live, adopted as is) as the pattern. Both write to `.cursor/skills/`; tell them to use `.claude/skills/` and the name `lcp-verify`.
- **Is it grounded in current docs?** `source-driven-development` (live, adopted as is). Prefer Microsoft Learn and note the doc date.
- **Where is the trail?** `lcp-decision-log` (live). One decision per row, evidence is a pointer. Transcripts and traces reach Blob within the night, tagged with `run_id` (rule 16).

## Client reports (the outer loop)

AI Managed Services reports arrive raw. Triage first, never build straight from a report. `lcp-triage` (live, untested) groups, dedupes and reproduces in `factory-test`, then writes `triage.json`. It never fixes. A human then uses `lcp-intake` (live) to set the size and write the story brief. Which ITSM tools clients use is still an open question.

## Changing the factory

Prompts, rubrics, agents, skills, hooks, gate scripts, `lcp-verify`, `glossary.md`, decision records and coding standards change **only by a reviewed daytime PR** (rule 17).

- **Same mistake keeps happening:** `lcp-correct` (live). Fix it as high as it goes: design, then types, then lint, then tests, docs last.
- **Adopting a third-party skill:** read every file, pin the commit, record it in `skills/README.md` (rule 19). Then Boroon approves. Then it moves to `.claude/skills/`, adapted and renamed `lcp-*` where it touches Power Platform.
- **Machine-read names** stay product-neutral (rule 18). Use `lcp`, `fl1`, `factory-test` and so on, never `pp` or `powerplatform`.

## Where the session ends

At a phase boundary (grilling done, build done, review done), take the first yes:

1. **Does the next phase need this one word for word?** Carry on in the same session. Grilling into scenarios is the usual case.
2. **Is nothing here needed next?** Clear it.
3. **Is it moving to another harness, folder, repo or person?** Write a handoff file. In this repo that means a `docs/progress.md` entry.
4. **Can it run with nobody watching?** Give it to a subagent, or to the night shift.
5. **Otherwise** compact, with an instruction that says what the next phase needs.

Never rely on chat memory. Write the decision down in `docs/progress.md` before the session ends, and commit and push to the session branch.

## Always true

- Humans own intent, spec approval and every merge to `main`.
- The worker never decides it is done. The gate and fresh verifiers do.
- Price from the list column, never from credits. Client work runs at cash until spike 0.1 is answered.
- No client production data in factory lanes. Client code follows the client's residency tier.
