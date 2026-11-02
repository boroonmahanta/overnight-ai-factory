---
name: pcp-blast-radius
description: Find what a change to a pro-code repo could break somewhere else, then prove the one fact it is safe because of by running real code. Use for "blast radius of X", "what could this break", or reviewing a small diff you do not trust. Pro-code profile.
disable-model-invocation: true
---

# Blast radius, pro-code (GET AI)

Adapted from `blast-radius` by Lauren Tan (MIT, pinned at `cursor/plugins` commit `ae5650febf4320793844c12c4adaa937f417f8da`, original in `skills/tan/blast-radius/`). The Power Platform version is `lcp-blast-radius`. Same method, different places to look. Untested.

Listing callers is easy. A search does that in a second. The job is the breakage a search will not show.

## The rule that matters (rule 11)

Your writeup can **raise** the Merge Danger score. It can never lower the deterministic floor. A writeup that sounds right proves nothing, so find the one or two facts the safety depends on and prove them by running code.

## How sure are you

For each fact, get it as far down as is cheap, and say where it stopped.

1. You said so. Worthless alone.
2. You pointed at the line: a real `file:line`, or the library's own source at the pinned version.
3. You walked the failure step by step and it cannot reach.
4. You ran it: a script or test that imports the same library the app ships and calls the exact function you worry about. It fails loudly if you are wrong.
5. You reproduced it in the running app.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes and deletes, and what it now does differently, including the part the diff does not spell out. Use `pcp-why` to pull the PR and commits.
2. **Find the one fact it is safe because of.** Most risky-looking changes are safe for one reason, for example "this call only drops already-dead cache entries". Find it first. Spend time here, not on a long list of maybes.
3. **Look where a search stops.**
   - The source and pinned version of the library you call, and any local patch.
   - When things run: startup, teardown, async ordering, retries, timeouts, transactions.
   - What a symbol search misses: JSON an API returns, database columns and migrations, a wire format another language reads, message queues and events, feature flags, config and environment variables, scheduled jobs, code three hops downstream.
   - Other services, repos and clients that call this one. Public API and contract changes.
   - Build and deploy: lockfile, generated code, container image, infrastructure files, CI.
   - Data already in the system that the new code has never seen.
4. **Be honest about each risk.** Give it a real chance and a real cost. Keep confirmed risks apart from the ones you checked and cleared. Cite a real `file:line`. A search that finds nothing is still an answer. Never make up a caller or an API.
5. **Prove the one fact.** Write a small script or test that runs the real code, run it, and paste what happened. Run it in the sandbox only, never against production or client data (rule 15).

## What to hand back

- **What it does.** Including the part that is not obvious.
- **The one safety fact.** Say which of the five levels you reached and show the proof. If you could not prove it, write **unproven**.
- **Risks.** Each: how it breaks, `file:line`, how likely, how bad, how to check.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test that would catch the real bug, including the script you wrote.
- **Merge Danger.** The size of the blast radius, and whether you are asking to raise the score. Never ask to lower it.

Plain words. Strip client names and data from anything that leaves the repo.
