---
name: principle-laziness-protocol
description: "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem."
disable-model-invocation: true
---

> **GET AI note (2 November 2026).** Pro-code (`pcp`) repos. For Power Platform work, read it as background only. Adopted from `cursor/plugins` `pstack/skills/principle-laziness-protocol` at commit `ae5650febf4320793844c12c4adaa937f417f8da`; the text below is otherwise unchanged. Shelf original: `skills/tan/principle-laziness-protocol/`.

# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
