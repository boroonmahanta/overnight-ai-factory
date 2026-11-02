---
name: lcp-correct
description: Find the mistakes agents keep repeating in a repo and make each one impossible, highest level first. Use for the weekly retro, after a bad week, or when a human keeps correcting the same thing.
disable-model-invocation: true
---

# Correct (GET AI)

Adapted from `correct` by Lauren Tan (MIT, pinned at `cursor/plugins` commit `ae5650febf4320793844c12c4adaa937f417f8da`, original in `skills/tan/correct/`). Changed: sources of mistakes and the ladder now fit Power Platform, and the output is a reviewed PR (rule 17).

Assume every contributor is an agent that sees only the files it opened, copies the nearest example and takes the shortest path that compiles or imports. Change the repo so the next agent cannot make the mistake.

Day work only. This changes prompts, checks and standards, so it ships as a daytime PR a human reviews.

## 1. Find the mistake classes

Read recent commits, reverts, review comments, `AGENTS.md`, comments that explain workarounds, and for the factory: gate failures, `NEEDS_WORK` and `RESTART` verdicts, PARK reasons (`park.json`), escaped defects, and the weekly retro notes. Group them. A class counts once it has happened **twice**.

## 2. Fix each class at the highest level that works

1. **Remove it by design.** One owner for each piece of state, one supported way for each task. In a solution: one place for each environment variable, one connection reference per connector, no copy of a flow to drift. Delete old ways and dead components an agent would copy.
2. **Make the bad state impossible to write.** Solution checker rules, a lint or gate check whose error names the component to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behaviour.** Fix or delete any scenario that still passes when the behaviour breaks, or fails when only internals change. Locked scenarios change only by the people who own them (rule 3).
4. **Write docs or agent rules last.** Only for judgement calls. Nothing fails when an agent skips them.

## 3. Fix and prove

Fix the most frequent classes now, one commit each. Prove each new check **fails on a real past mistake**. Run the same command locally and in the gate. Exceptions go on the offending line with a reason, an expiry date and a human's approval.

## 4. Keep the rule table

Keep a table in `AGENTS.md` that pairs each rule with what enforces it. When a human corrects an agent, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat: fix it at the highest level in the same change. Drop a rule once its mistake cannot happen.

## Reply

Each class, its evidence, the level you picked, and why a higher level did not work. Cost and Merge Danger of the change itself: it touches gate or builder files, so it is at least M.
