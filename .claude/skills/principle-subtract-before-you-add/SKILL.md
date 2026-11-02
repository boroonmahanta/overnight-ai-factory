---
name: principle-subtract-before-you-add
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
disable-model-invocation: true
---

> **GET AI note (2 November 2026).** Removing a component from a managed solution, or dropping data, is a one-way door. Score it size L until proven otherwise. Adopted from `cursor/plugins` `pstack/skills/principle-subtract-before-you-add` at commit `ae5650febf4320793844c12c4adaa937f417f8da`; the text below is otherwise unchanged. Shelf original: `skills/tan/principle-subtract-before-you-add/`.

# Subtract Before You Add

When evolving a system, remove complexity first, then build. Default to subtraction.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

- Sequence removal before construction
- Cut before you polish (get to the minimum before investing in quality)
- Design for observed usage, not speculative edge cases
- No speculative validators, parsers, or guards beyond what the spec demands
- Simplify prompts (remove redundant instructions, excessive templates)
- When a reference has no novel content, delete it rather than leaving a stub
