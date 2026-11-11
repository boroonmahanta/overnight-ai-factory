---
name: principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design."
disable-model-invocation: true
---

> **GET AI note (11 November 2026).** Adopted unchanged on 2 November 2026 from `cursor/plugins` `pstack/skills/principle-redesign-from-first-principles` at commit `ae5650febf4320793844c12c4adaa937f417f8da` (MIT, licence text at `skills/tan/LICENSE`); the text below is unchanged. Shelf original: `skills/tan/principle-redesign-from-first-principles/`.

# Redesign From First Principles

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been a foundational assumption from the start.

- Read all affected files and understand the current design
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections
- Think about the whole redesign, then deliver it incrementally

This is the method for preserving option value when integrating changes into an existing design.
