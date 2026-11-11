# Schedule: the rest of stages 0 and 1, then into stage 2

Made 7 November 2026 (Session 16), at Boroon's word, starting Monday 9 November 2026. The order comes from what each story needs first (plan sections 11.1 and 11.2, and the ADO backlog). ADO holds the same dates on each story as Start Date and Finish Date, and the "needs first" column as predecessor links (project `getai-overnight-ai-factory`).

## How to use it

- Dates are targets, not promises. When a story slips, move the stories after it too, here and in ADO.
- At the end of each session, mark the stories it finished as done in the Status column, and move them to Done in ADO.
- The plan's rule holds: do not start a stage until the one before passes its exit test. Stage 2 starts only after 2539.

## Assumptions

- One person (Boroon) with Claude, about one story per working day, Monday to Friday.
- Two tracks at once:
  - **Laptop:** work on `getai.ghe.com` and in the tenant. Cloud sessions cannot reach `getai.ghe.com`.
  - **Documents:** repo work only, which can run in a cloud session.
- 21 December 2026 to 8 January 2027 is left as buffer and holidays. If you work then, pull the January stories forward.
- Two things depend on other people:
  - a second approver and the three CODEOWNERS teams, needed by 17 December;
  - engineers sending their session exports, needed for 2548.

## The order

| Start | Finish | ADO | Story | Track | Needs first | Status |
|---|---|---|---|---|---|---|
| Sun 8 Nov | Sun 8 Nov | 2462 | Spike 0.18: headless YAML export as the lane identity (brought forward from Mon 9 to Tue 10 Nov) | Laptop | | **Done 8 Nov** (Session 19; `docs/plans/spike-0.18/`: YAML fails, the XML fallback passes) |
| Mon 9 Nov | Tue 10 Nov | 2463 | Spike 0.19: reset fidelity (moved from Wed 11 to Thu 12 Nov; reuses 0.18's scratch solution and repo) | Laptop | 2462 | **Done 10 Nov** (Session 20; `docs/plans/spike-0.19/`: the reset passes, export equal byte for byte) |
| Sat 7 Nov | Sat 7 Nov | 2543 | Plan the rest of Stage 1 in its own planning session (brought forward; the gate scripts left for after 2462) | Documents | | **Done 7 Nov** (Session 17; `docs/plans/stage-1-day-gate-plan.md`) |
| Sat 7 Nov | Sat 7 Nov | 2545 | Templates: `glossary.md`, `docs/adr/`, `coding-standards.md` header (day-gate DG1, in `staging/`; brought forward from Thu 12 Nov) | Documents | 2543 | **Done 7 Nov** (Session 18; `staging/`) |
| Thu 12 Nov | Fri 13 Nov | 2549 | Apply the third-party skills policy to every vendored skill (moved from Thu 19 to Fri 20 Nov) | Documents | | |
| Fri 13 Nov | Fri 13 Nov | 2433 | Check Dataverse MCP billing for `factory-lane-1` | Laptop (portal) | | |
| Fri 13 Nov | Fri 13 Nov | 2505 | Review and merge Dependabot PRs #9, #10 and #11 | Laptop | | |
| Mon 16 Nov | Tue 17 Nov | 2461 | Spike 0.14: skills and lane tools headless, as the lane identity | Laptop | 2462 | |
| Wed 18 Nov | Thu 19 Nov | 2511 | Bring `factory-gates` in line with the live-build plan | Laptop | 2462 | |
| Wed 18 Nov | Wed 18 Nov | 2466 | Spike 0.17: session export for mining (DG2; the export how-to and the SharePoint folder) | Laptop (apps only, no tenant) | | |
| Fri 20 Nov | Fri 20 Nov | 2509 | Pin the Copilot CLI install in `verify-in-test` | Laptop | | |
| Fri 20 Nov | Fri 20 Nov | 2545 | The 46 standards, anonymised, into a new private `GetAI-IP/factory-manifestos`; read the older vault's retro workflow and design template (DG3). 2545 finishes here, not on Tue 17 Nov | Laptop | 2545 templates (done 7 Nov) | |
| Mon 23 Nov | Fri 27 Nov | 2538 | Write the remaining Stage 1 gate scripts (now also the `check_spec.py` job, D3) | Laptop | 2511, 2543 | |
| Mon 23 Nov | Wed 25 Nov | 2544 | Pin Spec Kit 1.3.x (D2); GET AI and `getai-lcp` presets v0; the spec check script (D3) (DG4, DG5) | Documents | 2543, 2545, the Ignite re-check | |
| Thu 26 Nov | Fri 11 Dec | 2548 | Mine at least 20 human-led sessions, in four batches: 26 Nov, 3 Dec, 8 Dec, 11 Dec (DG6) | Documents, or laptop if a cloud session cannot read the exports | 2543, 2466, engineers' exports | |
| Mon 30 Nov | Mon 30 Nov | 2537 | Create the gate reader and holdout reader token Apps | Laptop | | |
| Mon 30 Nov | Tue 15 Dec | 2546 | Locked scenario conventions and the Playwright kit v0 (draft 30 Nov to 2 Dec, DG7; test against `factory-test` on Northwind 14 to 15 Dec, DG9) | Documents, then laptop | 2543, 2447, 2541, 2538 (the YAML runner) | |
| Tue 1 Dec | Wed 2 Dec | 2451 | Spike 0.6: Copilot CLI on GHE.com | Laptop | | |
| Thu 3 Dec | Thu 3 Dec | 2738 | Spike 0.20: time and tokens on each story, every engine | Laptop | 2451 | |
| Fri 4 Dec | Fri 4 Dec | 2432 | Spike 0.7: nano AIU against billing | Laptop | 2451 (a day of runs) | |
| Fri 4 Dec | Fri 4 Dec | 2739 | Move `staging/` to `GetAI-IP/factory-manifestos` and `factory-gates` (DG8, D1) | Laptop | 2544, 2546 draft | |
| Mon 7 Dec | Mon 7 Dec | 2465 | Spike 0.15: redaction and Universe | Laptop | 2451 | |
| Mon 7 Dec | Mon 7 Dec | 2427 | Spike 0.1: credit ruling, the invoice check | Boroon | The credited subscription connected to a cost centre | |
| Tue 8 Dec | Tue 8 Dec | 2541 | Bootstrap `factory-test` with its test identity and test user | Laptop | | |
| Wed 9 Dec | Thu 10 Dec | 2459 | Spike 0.10: Test environment behaviour | Laptop | 2541 | |
| Fri 11 Dec | Fri 11 Dec | 2447 | Spike 0.11: test user sign-in | Laptop | 2541 | |
| Mon 14 Dec | Mon 14 Dec | 2455 | Spike 0.16: parallel sessions in one gate job | Laptop | 2451, 2447 | |
| Tue 15 Dec | Wed 16 Dec | 2531 | Callers build: reusable gate workflow, private caller repos | Laptop | 2511 | |
| Thu 17 Dec | Thu 17 Dec | 2520 | Undo the second-approver stopgaps | Laptop | The second approver | |
| Thu 17 Dec | Thu 17 Dec | 2529 | Make `self-test` a required status check | Laptop | The second approver | |
| Thu 17 Dec | Thu 17 Dec | 2521 | Apply the four rulesets (move step 12), Evaluate mode | Laptop | 2520, 2531, the three teams | |
| Fri 18 Dec | Fri 18 Dec | 2539 | Run the full gate on a human PR in Test, on the Northwind sample solution (D6): **Stage 1 exit test** | Laptop | 2521, 2537, 2538, 2451, 2459, 2544, 2546, 2548, the move | |
| Mon 11 Jan | Tue 12 Jan | 2448 | Spike 0.13: ADO and GHE.com (**Stage 2 starts**) | Laptop | 2539 | |
| Wed 13 Jan | Thu 14 Jan | 2457 | Spike 0.4: `pac copilot` under federated login | Laptop | The Ignite re-check | |
| Fri 15 Jan | Mon 18 Jan | 2460 | Spike 0.12: Copilot Studio evaluation from code | Laptop | The Ignite re-check | |

## Checkpoints (not ADO stories)

| Date | What | Who |
|---|---|---|
| Mon 9 Nov | Raise Claude Code's transcript retention on the laptop (`cleanupPeriodDays`, 30 days by default), so sessions from 4 November survive for mining and time records. **Done 8 Nov** (Session 19): 365 days, in `~/.claude/settings.json` | Boroon, in the laptop session |
| Fri 20 Nov | Ask the engineers for their session exports, using what spike 0.17 shows | Boroon |
| Mon 23 Nov | Ignite re-check, after 17 to 20 November: product names, Copilot Studio evaluation APIs, Git integration (`CLAUDE.md`, dates). Also the first pass of A1: check every pinned kit for updates | Boroon with Claude |
| Fri 4 Dec | A second approver named, and the three CODEOWNERS teams created. Without them, 2520, 2521 and the Stage 1 exit test cannot happen | Boroon |
| Fri 4 Dec | Mining cut-off (D5): if fewer than 20 engineers' sessions have arrived, pick up to 10 of Boroon's own to top up | Boroon |

## Not dated yet

- 2450, spike 0.5 (cloud agent against Dataverse): Stage 5.
- 2454, spike 0.8 (Container Apps long run and resume): Stage 6.

Date them when Stage 4 ends.

- A1, keep pinned kits current (Boroon, 7 November 2026; `docs/plans/stage-1-day-gate-plan.md`): a pin register, Dependabot where it can, and a monthly manual pass. Only its first pass is dated (23 November). ADO 2740, created 8 November 2026 (Session 19), Proposed, no dates.

## Changes

- **7 November 2026 (Session 17, cloud).** 2543 done early. 2545 split: templates move into the freed slot (Thu 12 Nov); the standards seed moves to Fri 20 Nov, so 2545 finishes on 20 Nov, not 17 Nov. 2466 is on the laptop (it needs the apps). 2544 pins 1.3.x. 2546 now also needs 2541 and 2538. New: the move on Fri 4 Dec, the retention checkpoint on Mon 9 Nov, and the mining cut-off on Fri 4 Dec. 2539 now also needs the move. The detail is in `docs/plans/stage-1-day-gate-plan.md`. ADO is not yet updated (cloud session); the next laptop session does it.
- **7 November 2026 (Session 18, cloud).** DG1, the templates half of 2545, done on Sat 7 Nov, brought forward from Thu 12 Nov. 2545 now starts Sat 7 Nov, not Thu 12 Nov, and still finishes Fri 20 Nov (DG3). Thu 12 Nov's documents slot is now free. ADO is not yet updated (cloud session); the next laptop session does it.
- **7 November 2026 (Session 18, later, at Boroon's word).** 2549 moves into the free slot: Thu 12 to Fri 13 Nov, from Thu 19 to Fri 20 Nov, still two days. It needs nothing first and nothing waits on it. Fri 20 Nov now holds only laptop work (2509 and 2545's DG3). ADO not yet updated.
- **8 November 2026 (Session 19, laptop).** ADO now matches this file: Sessions 17 and 18's updates are made, the DG8 move is 2739 and A1 is 2740, and the schedule-order query gives every date above. 2462 (spike 0.18) done on Sun 8 Nov, two days early, which unblocks 2463, 2461 and 2511. At Boroon's word, 2463 (spike 0.19) moves forward to Mon 9 to Tue 10 Nov, from Wed 11 to Thu 12 Nov. Wed 11 and Thu 12 Nov are now free on the laptop track; nothing else moves. The retention checkpoint is done (365 days).
- **10 November 2026 (Session 20, laptop).** 2463 (spike 0.19) done on Tue 10 Nov, on its target date. Nothing moves. Wed 11 and Thu 12 Nov stay free on the laptop track. ADO: 2463 Done.
