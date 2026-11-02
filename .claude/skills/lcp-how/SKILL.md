---
name: lcp-how
description: Explain how a Power Platform solution or a piece of code works, at the level a senior engineer onboarding would need. Use before changing something, or for "how does X work", "where should this live".
disable-model-invocation: true
---

# How (GET AI)

Adapted from `how` by Lauren Tan (MIT, pinned at `cursor/plugins` commit `ae5650febf4320793844c12c4adaa937f417f8da`, original and prompt templates in `skills/tan/how/`). Changed: no Cursor model settings, Power Platform views added. Read only. It changes nothing.

Companion to `lcp-why`. How says what it does. Why says why it is shaped that way. `lcp-blast-radius` says what it breaks elsewhere.

## 1. Size the question

If the scope is vague, say how you read it and carry on. The person can redirect.

- **Simple** (one flow, one table, one function): explore and explain in one pass.
- **Complex** (a whole solution, a cross-app feature): split into 2 to 4 angles, for example data model, flows, UI, security and connections. Use one read-only subagent per angle if the client's residency tier allows it and subagents are available. Otherwise do the angles yourself, one after another.

When unsure, take the simple path.

## 2. Where to look in a Power Platform solution

- Unpacked solution files in the repo (`pac solution unpack`), not just a description.
- Tables, columns, relationships, choices, views and forms.
- Flows: trigger, run-after, child flows, connection references, environment variables, error handling.
- Canvas and model-driven apps: screens, components, formulas, data sources.
- Copilot Studio agents: topics, tools, knowledge, instructions.
- Security roles, column security, sharing, DLP policy that applies.
- Solution layers and dependencies (what must exist in the target environment).
- Run history, traces and logs, only in `factory-test` or with synthetic data.

## 3. Write it up

Sections, dropping any that do not apply:

- **Overview.** What it is, what it does, why it exists. Someone should be able to stop here.
- **Key concepts.** The tables, flows or terms needed to follow the rest. Use words from `glossary.md`.
- **How it works.** The main flow: what triggers it, each step, where data goes, the decision points. Name the real components. Use a small diagram only when it clarifies.
- **Where things live.** A short map of folders and components to start work.
- **Gotchas.** Surprising behaviour, history, traps. Leave out if none.

Concrete words, not abstractions. Say "the `Approve order` flow sets `statuscode` on `Order`", not "the process updates the record". If the explorers or you could not trace something, say so.

## Rules

- Facts are looked up, not guessed (rule 9). If a fact is missing, say it is missing.
- Do not paste client data. Use synthetic examples.
