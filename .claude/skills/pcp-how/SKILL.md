---
name: pcp-how
description: Explain how a subsystem in a pro-code repo works, at the level a senior engineer onboarding would need. Use before changing something, for "how does X work", or for "where should this live". Pro-code profile.
disable-model-invocation: true
---

# How, pro-code (GET AI)

Adapted from `how` by Lauren Tan (MIT, pinned at `cursor/plugins` commit `ae5650febf4320793844c12c4adaa937f417f8da`, original and prompt templates in `skills/tan/how/`). The Power Platform version is `lcp-how`. Read only. It changes nothing. Untested.

Companion to `pcp-why` (why it is shaped this way) and `pcp-blast-radius` (what it breaks elsewhere).

## 1. Size the question

If the scope is vague, say how you read it and carry on. The person can redirect.

- **Simple** (one module, one function, a narrow question): explore and explain in one pass.
- **Complex** (a subsystem across files or services, a cross-cutting feature): split into 2 to 4 angles, for example request path, data model, background work, auth and config. Use one read-only subagent per angle if the client's residency tier allows it and subagents are available. Otherwise take the angles one after another.

When unsure, take the simple path.

## 2. Where to look

- Entry points: routes, handlers, CLI commands, queue consumers, scheduled jobs.
- Types, schemas, migrations and the data model.
- Config, environment variables, feature flags and secrets handling (names only, never values).
- Tests: their names and assertions show intended behaviour.
- CI, build and deploy files: how it is built, tested and shipped.
- `glossary.md`, decision records, `AGENTS.md` and READMEs in the area.
- Each explorer lists every file it read, so the explainer can reference them.

## 3. Write it up

Sections, dropping any that do not apply:

- **Overview.** What it is, what it does, why it exists. Someone should be able to stop here.
- **Key concepts.** The types, services or terms needed to follow the rest. Use words from `glossary.md`.
- **How it works.** The core and the longest part. What triggers it, each step, where data goes, the decision points. Name real files and functions. Use prose, not pseudocode. Add a small diagram only when it clarifies.
- **Where things live.** A short map of folders and files to start work.
- **Gotchas.** Surprising behaviour, history, traps. Leave out if none.

Say "`UserService` calls `AuthClient.refresh()`", not "the service delegates to the client". If something is complex, say why. If it is simple, do not pad. Where explorers could not trace something, say so.

## Rules

- Facts are looked up, not guessed (rule 9). A fact you could not find is marked missing.
- Do not paste secrets or client data. Describe their shape only.
