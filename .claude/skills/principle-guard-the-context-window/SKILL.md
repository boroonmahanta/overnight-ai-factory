---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

> **GET AI note (2 November 2026).** Boroon likes this one. In this repo it means: sessions stay under about 200K tokens, `CLAUDE.md` is a map, and sources are read by line range, not whole. Adopted from `cursor/plugins` `pstack/skills/principle-guard-the-context-window` at commit `ae5650febf4320793844c12c4adaa937f417f8da`; the text below is otherwise unchanged. Shelf original: `skills/tan/principle-guard-the-context-window/`.

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
