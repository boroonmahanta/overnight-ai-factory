---
name: getai-domain-modeling
description: Build and sharpen a project's domain model. Day work only. Use when discussing codebase terminology, writing or editing glossary.md, or recording or editing an ADR.
disable-model-invocation: true
---

> **GET AI version (2 November 2026).** Adapted from Matt Pocock's `domain-modeling` (`mattpocock/skills`, commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; originals on the shelf at `skills/pocock/domain-modeling/`). Changes, decided by Boroon: the files are lowercase (`glossary.md`, `glossary-map.md`) because the protected-paths pattern in plan Appendix A matches lowercase only; each term carries a **Schema** line (plan 6.2); this skill runs by day, and both files change only by a reviewed daytime PR (rule 17). `docs/adr/` is unchanged. Untested.

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `glossary.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── glossary.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `glossary-map.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── glossary-map.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── glossary.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── glossary.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `glossary.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `glossary.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update glossary.md inline

When a term is resolved, update `glossary.md` right there, on the working branch. Don't batch these up: capture them as they happen. The file is protected, so it reaches `main` only through a reviewed daytime PR. A night agent never edits it. Use the format in [glossary-format.md](./glossary-format.md).

`glossary.md` holds the meaning of each term, plus one **Schema** line that names where the term lives (Dataverse table and column, flow, app, or code symbol). It holds no design, no how-it-works and no implementation decisions. Do not treat it as a spec or a scratch pad. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [adr-format.md](./adr-format.md).
