---
name: lcp-blast-radius
description: Find what a change to a Power Platform solution could break somewhere else, then prove the one fact it is safe because of by running something real. Use for "blast radius of X", "what could this break", or any M or L change.
disable-model-invocation: true
---

# Blast radius (GET AI)

Adapted from `blast-radius` by Lauren Tan (MIT, pinned at `cursor/plugins` commit `ae5650febf4320793844c12c4adaa937f417f8da`, original in `skills/tan/blast-radius/`). Changed: Cursor-only references removed, Power Platform places to look added, Merge Danger tied in.

Listing what uses a thing is easy. The job is the breakage a search will not show.

## The rule that matters (rule 11)

Your writeup can **raise** the Merge Danger score. It can never lower the deterministic floor. A writeup that sounds right is not proof, so find the one or two facts the safety depends on and prove them by running something.

## How sure are you

For each fact, get it as far down as is cheap, and say where it stopped.

1. You said so. Worthless alone.
2. You pointed at it. A real file and line, a solution component name, or the product docs for that version.
3. You walked the failure step by step and it cannot reach.
4. You ran it. A query, a flow run, a solution check or an `lcp-verify` call that fails loudly if you are wrong.
5. You reproduced it in the running app in `factory-test`.

## Steps

1. **Read the change.** The diff or solution export, what it adds, changes and deletes, including what it now does differently that the diff does not say.
2. **Find the one fact it is safe because of.** Most risky-looking changes are safe for one reason, for example "this column is only read by the view being changed". Find it first.
3. **Look where a search stops.** In Power Platform, check:
   - Other flows, apps, agents and Copilot Studio topics or tools that use the same table, column, choice value, connection reference, environment variable or child flow.
   - Solution layers: is an unmanaged layer or another solution sitting on top of what you change?
   - Security roles and column security that change who can see or do something.
   - Triggers and run-after settings, plug-ins and business rules that fire on the same table.
   - Anything outside the solution: reports, exports, integrations, the client's ITSM tool, another tenant.
   - Data already in the table that the new logic has never seen (nulls, old choice values).
   - Connector limits and throttling (plan section 5.12).
4. **Be honest about each risk.** Give it a real chance and a real cost. Keep confirmed risks apart from the ones you checked and cleared. Cite a real component or line. A search that finds nothing is still an answer. Never make up a caller.
5. **Prove the one fact.** Run it in `factory-test` or against the solution export. Paste what happened. Use `lcp-verify` when it exists (stage 2). Until then use a Dataverse query, a flow run history, or `pac solution check`.
6. **Never test in UAT or Prod.** Synthetic data and the test user only (rule 15).

## What to hand back

- **What it does.** Including the part that is not obvious.
- **The one safety fact.** Say which of the five levels you reached, and show the proof. If you could not prove it, write **unproven**.
- **Risks.** Each: how it breaks, where, how likely, how bad, how to check.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test that would catch the real bug.
- **Merge Danger.** The size of the blast radius, and whether you are asking to raise the score. Never ask to lower it.

Plain words. Keep client names and data out of anything that leaves the repo.
