# Schedule: the rest of stages 0 and 1, then into stage 2

Made 7 November 2026 (Session 16), at Boroon's word, starting Monday 9 November 2026. The order comes from what each story needs first (plan sections 11.1 and 11.2, and the ADO backlog). ADO holds the same dates on each story as Start Date and Finish Date, and the "needs first" column as predecessor links (project `getai-overnight-ai-factory`).

## How to use it

- Dates are targets, not promises. When a story slips, move the stories after it too, here and in ADO.
- At the end of each session, mark the stories it finished as done in the Status column, and move them to Done in ADO.
- The plan's rule holds: do not start a stage until the one before passes its exit test. Stage 2 starts only after 2539.

## Assumptions

- One person (Boroon) with Claude, about one story per working day, Monday to Friday.
- **From Tue 24 Nov (Boroon, 23 November 2026): finish Stage 1 by Fri 27 Nov**, with Sat 28 and Sun 29 Nov as buffer. That needs up to three laptop sessions at once, each in its own worktree: **A** gate scripts and rulesets, **B** the tenant (`factory-test`, one story at a time, since each needs the one before), **C** other getai.ghe.com work. Two sessions in `factory-gates` at once will clash in `scripts.sha256` and `pending-scripts.txt`; merge one pull request before the other rebuilds the manifest. Stage 0 spikes that 2539 does not need move to the week after, except 2738 (spike 0.20), which is in the Stage 1 epic and runs Fri 27 Nov.
- Two tracks at once:
  - **Laptop:** work on `getai.ghe.com` and in the tenant. Cloud sessions cannot reach `getai.ghe.com`.
  - **Documents:** repo work only, which can run in a cloud session.
- 21 December 2026 to 8 January 2027 is left as buffer and holidays. If you work then, pull the January stories forward.
- Two things depend on other people:
  - a second approver and the three CODEOWNERS teams, needed by Wed 25 Nov (was 17 December);
  - engineers sending their session exports, needed for 2548 from Wed 25 Nov.

## The order

| Start | Finish | ADO | Story | Track | Needs first | Status |
|---|---|---|---|---|---|---|
| Sun 8 Nov | Sun 8 Nov | 2462 | Spike 0.18: headless YAML export as the lane identity (brought forward from Mon 9 to Tue 10 Nov) | Laptop | | **Done 8 Nov** (Session 19; `docs/plans/spike-0.18/`: YAML fails, the XML fallback passes) |
| Mon 9 Nov | Tue 10 Nov | 2463 | Spike 0.19: reset fidelity (moved from Wed 11 to Thu 12 Nov; reuses 0.18's scratch solution and repo) | Laptop | 2462 | **Done 10 Nov** (Session 20; `docs/plans/spike-0.19/`: the reset passes, export equal byte for byte) |
| Sat 7 Nov | Sat 7 Nov | 2543 | Plan the rest of Stage 1 in its own planning session (brought forward; the gate scripts left for after 2462) | Documents | | **Done 7 Nov** (Session 17; `docs/plans/stage-1-day-gate-plan.md`) |
| Sat 7 Nov | Sat 7 Nov | 2545 | Templates: `glossary.md`, `docs/adr/`, `coding-standards.md` header (day-gate DG1, in `staging/`; brought forward from Thu 12 Nov) | Documents | 2543 | **Done 7 Nov** (Session 18; `staging/`) |
| Wed 11 Nov | Wed 11 Nov | 2549 | Apply the third-party skills policy to every vendored skill (moved from Thu 19 to Fri 20 Nov, then brought forward from Thu 12 to Fri 13 Nov) | Documents | | **Done 11 Nov** (Session 21; `docs/analysis/skills-policy-check.md`, `docs/component-register.md`) |
| Fri 13 Nov | Fri 13 Nov | 2433 | Check Dataverse MCP billing for `factory-lane-1` | Laptop (portal) | | **Done 13 Nov** (Session 22; `docs/plans/spike-0.3/README.md`, "Billing check": metered, 0.1 Copilot Credit a call, from the tenant's prepaid pool) |
| Fri 13 Nov | Fri 13 Nov | 2505 | Review and merge Dependabot PRs #9, #10 and #11 | Laptop | | **Done 13 Nov** (Session 24; #10 and #11 were superseded on 9 Nov by #14 and #13; Boroon merged #9, #13 and #14) |
| Wed 18 Nov | Thu 19 Nov | 2461 | Spike 0.14: skills and lane tools headless, as the lane identity (moved from Mon 16 to Tue 17 Nov) | Laptop | 2462 | **Done 21 Nov**, two days after its finish date (Sessions 25 to 29; `docs/plans/spike-0.14/`: passed, with the fallback where it applies; the plan edited at Boroon's word) |
| Thu 19 Nov | Fri 20 Nov | 2511 | Bring `factory-gates` in line with the live-build plan (moved from Wed 18 to Thu 19 Nov) | Laptop | 2462 | **Done 21 Nov**, a day after its finish date (Session 30; gate PR 15 merged by Boroon; task 2517 moved to 2538) |
| Fri 20 Nov | Fri 20 Nov | 2466 | Spike 0.17: session export for mining (DG2; the export how-to and the SharePoint folder; brought forward from Wed 18 to Mon 16 Nov on 13 Nov, missed, set to Fri 20 Nov on 18 Nov, at Boroon's word) | Laptop (apps only, no tenant) | | **Done 21 Nov**, a day after its date (Session 31; `docs/plans/spike-0.17/`: passes for all four tools; a cloud session can read the exports folder; Done in ADO at Boroon's word) |
| Fri 20 Nov | Fri 20 Nov | 2545 | The standards (50, with the four `TOK`), anonymised, into a new private `GetAI-IP/factory-manifestos`; read the older vault's retro workflow and design template (DG3). 2545 finishes here, not on Tue 17 Nov | Laptop | 2545 templates (done 7 Nov) | **Done 13 Nov** (Session 23; `GetAI-IP/factory-manifestos` pull request 1, 50 standards, merged by Boroon) |
| Mon 23 Nov | Mon 23 Nov | 2509 | Pin the Copilot CLI install in `verify-in-test` (moved from Fri 20 Nov) | Laptop | | **Done 23 Nov** (Session 34; gate PR 16; Done in ADO) |
| Mon 23 Nov | Wed 25 Nov | 2544 | Pin Spec Kit 1.4.3 (D2, Boroon, 23 Nov; was 1.3.x); GET AI and `getai-lcp` presets v0; the spec check script (D3) (DG4, DG5) | Documents | 2543, 2545, the Ignite re-check | DG4 **done 23 Nov** (Session 35; `staging/factory-manifestos/spec-kit/`). DG5 **done 23 Nov** (Session 36; `staging/factory-gates/spec/check_spec.py`, 98 tests passing). All built, two days early; Done in ADO at Boroon's word |
| Tue 24 Nov | Thu 26 Nov | 2538 | Write the remaining Stage 1 gate scripts (now also the `check_spec.py` job, D3) (was Tue 24 to Mon 30 Nov; three days, not five, to finish Stage 1 this week) | Laptop A | 2511, 2543 | |
| Tue 24 Nov | Tue 24 Nov | 2537 | Create the gate reader and holdout reader token Apps (was Tue 1 Dec) | Laptop C | | |
| Tue 24 Nov | Fri 27 Nov | 2546 | Locked scenario conventions and the Playwright kit v0 (draft Tue 24 to Wed 25 Nov, DG7; test against `factory-test` on Northwind Fri 27 Nov, DG9) (was 30 Nov to 15 Dec) | Documents, then laptop B | 2543, 2447, 2541, 2538 (the YAML runner) | |
| Tue 24 Nov | Tue 24 Nov | 2541 | Bootstrap `factory-test` with its test identity and test user (was Tue 8 Dec) | Laptop B | | |
| Tue 24 Nov | Tue 24 Nov | 3019 | A restricted Factory home for session exports: the folder in the private channel's Files and its "Request files" link, so the engineers' exports land there before 2548 starts (was not dated) | Laptop C (Microsoft 365) | The admins' part, if still needed | Building since 21 Nov |
| Wed 25 Nov | Wed 25 Nov | 2740 | A1, keep pinned kits current: its first pass (missed on 23 Nov), each pinned kit checked for updates and added to `docs/component-register.md`, before 2739 moves the kits (was not dated) | Documents | 2544 | |
| Wed 25 Nov | Fri 27 Nov | 2548 | Mine at least 20 human-led sessions, in three batches: 25, 26 and 27 Nov (DG6) (was four batches, 26 Nov to 11 Dec) | Documents (a cloud session can read the exports, spike 0.17); Boroon's own sessions on the laptop | 2543, 2466, engineers' exports | |
| Wed 25 Nov | Wed 25 Nov | 2451 | Spike 0.6: Copilot CLI on GHE.com (one day, not two: spike 0.14's run 39346986 already showed the CLI runs on a getai.ghe.com runner with the job's own token) (was Wed 2 Dec) | Laptop C | | |
| Wed 25 Nov | Wed 25 Nov | 2459 | Spike 0.10: Test environment behaviour (was Wed 9 to Thu 10 Dec; one day, not two) | Laptop B | 2541 | |
| Wed 25 Nov | Thu 26 Nov | 2531 | Callers build: reusable gate workflow, private caller repos (was Tue 15 to Wed 16 Dec) | Laptop C | 2511 | |
| Thu 26 Nov | Thu 26 Nov | 2739 | Move `staging/` to `GetAI-IP/factory-manifestos` and `factory-gates` (DG8, D1) (was Fri 4 Dec). First on Thu, merged before 2538's spec-check job | Laptop C | 2544, 2546 draft, 2740 | |
| Thu 26 Nov | Thu 26 Nov | 2447 | Spike 0.11: test user sign-in (was Fri 11 Dec) | Laptop B | 2541 | |
| Fri 27 Nov | Fri 27 Nov | 2520 | Undo the second-approver stopgaps (was Thu 17 Dec) | Laptop A | The second approver | |
| Fri 27 Nov | Fri 27 Nov | 2529 | Make `self-test` a required status check (was Thu 17 Dec) | Laptop A | The second approver | |
| Fri 27 Nov | Fri 27 Nov | 2521 | Apply the four rulesets (move step 12), Evaluate mode (was Thu 17 Dec) | Laptop A | 2520, 2531, the three teams | |
| Fri 27 Nov | Fri 27 Nov | 2539 | Run the full gate on a human PR in Test, on the Northwind sample solution (D6): **Stage 1 exit test** (was Fri 18 Dec; Sat 28 and Sun 29 Nov are buffer) | Laptop A | 2521, 2537, 2538, 2451, 2459, 2544, 2546, 2548, the move | |
| Fri 27 Nov | Fri 27 Nov | 2738 | Spike 0.20: time and tokens on each story, every engine (not needed by 2539, but it is in the Stage 1 epic, so Stage 1 closes with it; was Mon 30 Nov) | Laptop C | 2451 | |
| Tue 1 Dec | Tue 1 Dec | 2432 | Spike 0.7: nano AIU against billing (was Fri 4 Dec; not needed by 2539) | Laptop | 2451 (a day of runs) | |
| Wed 2 Dec | Wed 2 Dec | 2465 | Spike 0.15: redaction and Universe (was Mon 7 Dec; not needed by 2539) | Laptop | 2451 | |
| Thu 3 Dec | Thu 3 Dec | 2455 | Spike 0.16: parallel sessions in one gate job (was Mon 14 Dec; not needed by 2539) | Laptop | 2451, 2447 | |
| Mon 7 Dec | Mon 7 Dec | 2427 | Spike 0.1: credit ruling, the invoice check (not needed by 2539; date unchanged, it waits on the subscription) | Boroon | The credited subscription connected to a cost centre | |
| Mon 11 Jan | Tue 12 Jan | 2448 | Spike 0.13: ADO and GHE.com (**Stage 2 starts**) | Laptop | 2539 | |
| Wed 13 Jan | Thu 14 Jan | 2457 | Spike 0.4: `pac copilot` under federated login | Laptop | The Ignite re-check | |
| Fri 15 Jan | Mon 18 Jan | 2460 | Spike 0.12: Copilot Studio evaluation from code | Laptop | The Ignite re-check | |

### This week, in order (Stage 1's 14 open stories, plus the three Stage 0 spikes 2539 needs)

Start each one only when what it needs is done. Within a day, go top to bottom.

| Day | Laptop A (gate scripts, rulesets) | Laptop B (the tenant) | Laptop C (other getai.ghe.com, Microsoft 365) | Documents |
|---|---|---|---|---|
| Tue 24 | 2538 day 1 | 2541 | 3019, then 2537 | 2546 draft (DG7) day 1 |
| Wed 25 | 2538 day 2 | 2459 (spike 0.10) | 2451 (spike 0.6), then 2531 day 1 | 2546 draft day 2, 2740, 2548 batch 1 |
| Thu 26 | 2538 day 3: the spec-check job last, after 2739 merges | 2447 (spike 0.11) | 2739 first, then 2531 day 2 | 2548 batch 2 |
| Fri 27 | 2520, 2529, 2521, then **2539, the exit test, last** | 2546 test on `factory-test` (DG9), before 2539 | 2738 (spike 0.20) | 2548 batch 3, before 2539 |

## Checkpoints (not ADO stories)

| Date | What | Who |
|---|---|---|
| Mon 9 Nov | Raise Claude Code's transcript retention on the laptop (`cleanupPeriodDays`, 30 days by default), so sessions from 4 November survive for mining and time records. **Done 8 Nov** (Session 19): 365 days, in `~/.claude/settings.json` | Boroon, in the laptop session |
| Fri 20 Nov | Ask the engineers for their session exports, using what spike 0.17 shows | Boroon |
| Mon 23 Nov | Ignite re-check, after 17 to 20 November: product names, Copilot Studio evaluation APIs, Git integration (`CLAUDE.md`, dates). Also the first pass of A1: check every pinned kit for updates | Boroon with Claude. **Re-check done 23 Nov** (Session 33; `docs/analysis/ignite-2026-recheck.md`; ADO 3024). A1's first pass and the register review not done |
| Wed 25 Nov | A second approver named, and the three CODEOWNERS teams created (was Fri 4 Dec). Without them, 2520, 2521 and the Stage 1 exit test cannot happen | Boroon |
| Thu 26 Nov | Mining cut-off (D5): if fewer than 20 engineers' sessions have arrived, pick up to 10 of Boroon's own to top up (was Fri 4 Dec) | Boroon |
| Tue 24 Nov | Chase the engineers' session exports, so 2548's first batch has some on Wed 25 Nov | Boroon |

## Not dated yet

- 2450, spike 0.5 (cloud agent against Dataverse): Stage 5.
- 2454, spike 0.8 (Container Apps long run and resume): Stage 6.

Date them when Stage 4 ends.

- 3019 and 2740 (A1) are dated since Session 37 (Tue 24 and Wed 25 Nov). A1's monthly pass after the first stays a checkpoint, with the component register review.

## Changes

- **7 November 2026 (Session 17, cloud).** 2543 done early. 2545 split: templates move into the freed slot (Thu 12 Nov); the standards seed moves to Fri 20 Nov, so 2545 finishes on 20 Nov, not 17 Nov. 2466 is on the laptop (it needs the apps). 2544 pins 1.3.x. 2546 now also needs 2541 and 2538. New: the move on Fri 4 Dec, the retention checkpoint on Mon 9 Nov, and the mining cut-off on Fri 4 Dec. 2539 now also needs the move. The detail is in `docs/plans/stage-1-day-gate-plan.md`. ADO is not yet updated (cloud session); the next laptop session does it.
- **7 November 2026 (Session 18, cloud).** DG1, the templates half of 2545, done on Sat 7 Nov, brought forward from Thu 12 Nov. 2545 now starts Sat 7 Nov, not Thu 12 Nov, and still finishes Fri 20 Nov (DG3). Thu 12 Nov's documents slot is now free. ADO is not yet updated (cloud session); the next laptop session does it.
- **7 November 2026 (Session 18, later, at Boroon's word).** 2549 moves into the free slot: Thu 12 to Fri 13 Nov, from Thu 19 to Fri 20 Nov, still two days. It needs nothing first and nothing waits on it. Fri 20 Nov now holds only laptop work (2509 and 2545's DG3). ADO not yet updated.
- **8 November 2026 (Session 19, laptop).** ADO now matches this file: Sessions 17 and 18's updates are made, the DG8 move is 2739 and A1 is 2740, and the schedule-order query gives every date above. 2462 (spike 0.18) done on Sun 8 Nov, two days early, which unblocks 2463, 2461 and 2511. At Boroon's word, 2463 (spike 0.19) moves forward to Mon 9 to Tue 10 Nov, from Wed 11 to Thu 12 Nov. Wed 11 and Thu 12 Nov are now free on the laptop track; nothing else moves. The retention checkpoint is done (365 days).
- **10 November 2026 (Session 20, laptop).** 2463 (spike 0.19) done on Tue 10 Nov, on its target date. Nothing moves. Wed 11 and Thu 12 Nov stay free on the laptop track. ADO: 2463 Done.
- **11 November 2026 (Session 21, cloud).** 2549 done on Wed 11 Nov, in one day, a day before its Thu 12 to Fri 13 Nov slot. Nothing waits on it, so nothing moves. Thu 12 and Fri 13 Nov are now free on the documents track; Fri 13 Nov keeps 2433 and 2505 on the laptop. ADO is not yet updated (cloud session): the next laptop session moves 2549 to Done, dates it Wed 11 Nov, and adds Session 21's time and tokens to its body.
- **13 November 2026 (Session 22, laptop).** 2433 done on Fri 13 Nov, on its target date. Nothing moves. ADO: 2433 Done. 2549's ADO updates were made the same day by another laptop session.
- **13 November 2026 (Session 23, laptop).** 2545's DG3 run on Fri 13 Nov, a week before its Fri 20 Nov slot, at Boroon's word. Boroon merged pull request 1 in `GetAI-IP/factory-manifestos` the same day, so 2545 is done; ADO: 2545 Done, dated Fri 13 Nov. The DG3 checkpoint (send the engineers the DG2 how-to) stays on Fri 20 Nov, after DG2 on Wed 18 Nov. Fri 20 Nov now holds only 2509 on the laptop track. Nothing else moves.
- **13 November 2026 (Session 24, laptop).** 2505 done on Fri 13 Nov, on its target date. Nothing moves. ADO: 2505 Done, its three tasks Closed, and 2507 and 2508 renamed for #14 and #13.
- **13 November 2026 (daily sync, laptop; committed by Session 25).** At Boroon's word, 2466 (DG2) brought forward from Wed 18 Nov to Mon 16 Nov, here and in ADO. It did not run on Mon 16 Nov; ADO still says Proposed.
- **18 November 2026 (Session 25, laptop).** 2461 started on Wed 18 Nov, two days late: part 1 of 4 passes (a flow by the Web API as the lane identity), and Copilot CLI works on a getai.ghe.com runner. It needs about one more session. Mon 16 and Tue 17 Nov passed with no session, so 2466 and 2511 slipped too. Dates not moved yet: Boroon to say how. ADO: 2461 Building.
- **18 November 2026 (Session 25, later, at Boroon's word: "Thu 19, shift a day").** 2461 finishes Thu 19 Nov. The laptop stories behind it move one working day: 2511 to Thu 19 to Fri 20 Nov, 2509 to Mon 23 Nov, 2538 to Tue 24 to Mon 30 Nov, 2537 to Tue 1 Dec. 2451 (spike 0.6) shrinks to one day, Wed 2 Dec, because 2461's Copilot check already did part of it; so nothing from Thu 3 Dec on moves, and the Stage 1 exit test stays Fri 18 Dec. 2466 (DG2) goes to Fri 20 Nov, so the checkpoint (ask the engineers for their exports) stays Fri 20 Nov. The documents track does not move. ADO matches.
- **21 November 2026 (Sessions 28 and 29, laptop).** 2461 done on Sat 21 Nov, two days after its Thu 19 Nov finish date, and moved to Done in ADO at Boroon's word. Its Start and Finish Dates are not changed. The stories behind it (2511 first) slip by the same; their dates move only at Boroon's word and are not moved here.
- **21 November 2026 (Session 30, laptop).** 2511 built on Sat 21 Nov, a weekend day, so the next working day, Mon 23 Nov, is still free for 2509 as planned: nothing after it needs to move. Boroon merged gate PR 15 the same day, and ADO 2511 is Done, its tasks Closed. Task 2517 (`danger-rules.yml`) moved under 2538 at Boroon's word. Dates not changed.
- **21 November 2026 (Session 31, laptop).** 2466 (DG2) run on Sat 21 Nov, a day after its Fri 20 Nov date, also a weekend day, so nothing after it moves. 2548's first batch (Thu 26 Nov) needs the engineers' exports, so the checkpoint (send the how-to, ask for exports) is due now; its date is not changed. ADO: 2466 Done at Boroon's word; its Start and Finish Dates are not changed. New: 3019 (a restricted Factory home for session exports), not dated.
- **21 November 2026 (Session 32, laptop).** 3019 started: "Request files" works in Boroon's OneDrive, so the checkpoint (send the how-to, ask for exports) is unblocked and still due. Boroon kept "Request files" for the channel, renewed quarterly; the admins' part is in ADO 3019. Still not dated. ADO: 3019's body updated, and 3019 moved to Building. Later the same day Boroon made the Factory Team and its private channel (3019 step 2), and Feature 2464 moved to In Progress at his word.
- **23 November 2026 (Session 33, laptop).** The Ignite re-check done on Mon 23 Nov, its checkpoint date, as ADO 3024 (new, under Feature 2711, Done). So 2544, 2457 (spike 0.4) and 2460 (spike 0.12), which list it as "needs first", are no longer waiting on it; nothing in it changes their scope. A1's first pass and the component register review, due the same day, were not done. Nothing moves.
- **23 November 2026 (Session 35, laptop).** 2544's DG4 done on Mon 23 Nov, its start date, in one session rather than two, with Spec Kit pinned at 1.4.3 at Boroon's word. DG5 (the spec check script) is next, on Tue 24 or Wed 25 Nov; 2544 still finishes Wed 25 Nov. Nothing moves. ADO: 2544 Building.
- **23 November 2026 (Session 36, laptop, started from Session 35).** DG5 done on Mon 23 Nov too, so all of 2544 is built two days before its Wed 25 Nov finish date. Tue 24 and Wed 25 Nov are free on the documents track; 2548's first batch stays Thu 26 Nov. Nothing else moves. ADO: 2544 stays Building, with DG5's result in its body, until Boroon says Done.
- **23 November 2026 (Session 37, laptop, at Boroon's word: finish Stage 1 this week).** Every story 2539 needs moves into Tue 24 to Fri 27 Nov, with Sat 28 and Sun 29 Nov as buffer, over up to three laptop sessions at once (A, B and C, see Assumptions) and the documents track. 2538 shrinks from five days to three, 2459 from two to one, and 2548 to three batches. The second approver and the three teams are now due Wed 25 Nov, and the mining cut-off Thu 26 Nov. Stage 0 spikes 2539 does not need (2738, 2432, 2465, 2455) move to Mon 30 Nov to Thu 3 Dec; 2427 stays Mon 7 Dec. 2509 and 2544 are Done in ADO. The January stories (Stage 2) are not moved; if 2539 passes on Fri 27 Nov, they can come forward at Boroon's word. ADO matches since the same evening, at Boroon's word ("Yes, update ADO"): the Start and Finish Dates of the 18 moved stories, read back and checked. Predecessor links not changed. Later the same evening, at Boroon's word, the plan (11.1, 14.4) says when Stage 0 spikes run: each before the first build that depends on it, not all in days 1 to 14. The dates above already follow it.
- **23 November 2026 (Session 37, later, at Boroon's word: "reorder the stories … move all proposed stories to the right sequence").** All 14 open Stage 1 stories now sit in this week, with a day-by-day order ("This week, in order"). New dates: 3019 Tue 24 Nov (before 2548), 2740 (A1's first pass) Wed 25 Nov (before 2739 moves the kits), and 2738 (spike 0.20) Fri 27 Nov, from Mon 30 Nov, since it is in the Stage 1 epic. 2739 now also needs 2740, and goes first on Thu so 2538's spec-check job follows it. Nothing else moves. ADO: the Start and Finish Dates of 3019, 2740 and 2738, and predecessor links 3019 before 2548 and 2740 before 2739.
