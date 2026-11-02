---
name: getai-grilling
description: Grill the user about a plan, decision, or idea in tranches of at most five questions. Day work only. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
disable-model-invocation: true
---

> **GET AI version (2 November 2026).** Adapted from Matt Pocock's `grilling` (`mattpocock/skills`, commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`; original on the shelf at `skills/pocock/grilling/`). Changes: at most five questions per round (Boroon's decision); day only, never at night (rule 9: night agents PARK on decisions); runs only when called; the facts-then-decisions and confirmation-gate rules are kept. Feeds the Spec Kit clarify step (plan 6.2). Untested.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask **at most five** frontier questions per round, most blocking first (the ones that unblock the most other questions). If the frontier holds more than five, keep the rest for the next round and say how many are waiting. Number each question and give your recommended answer. Then wait for the user's answers before the next round. A grilling can run to dozens of questions. Never dump them all at once.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round (again at most five). A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding. The owner confirms in writing before specify or plan runs. Record the settled decisions in the spec's `## Clarifications` section, new terms through `getai-domain-modeling`, and hard-to-reverse choices as ADRs.
