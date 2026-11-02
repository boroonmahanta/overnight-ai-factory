# Skills by lane and size

Status: a proposal for Boroon's review, 1 November 2026. Nothing is installed or decided. It replaces the skills-per-size column in `tshirt-sizing.md` section 1 and the "Sizes" column in `skills-comparison.md` section 5.2. The five sizes and the largest-answer rule stay approved.

Basis: the same two files, plus plan sections 4.1 to 4.6 (lanes, routing, outer loop). Most skill bodies are still unread, so "use" means "on the shortlist to read in full" (plan rule 19). Nothing here is new evidence. It is a re-cut of the earlier list by lane.

## 1. What changed from the last proposal

- The last list had one set of skills per size. Now the set depends on the lane as well.
- Two new columns: **Prototype** and **BAU Managed Services**.
- Lane B is now two rows: `lcp` (Power Platform) and `pcp` (code repos). The plan called the second one the "code profile".
- The Power Platform lane stays the focus. Its cells are the most detailed. Lane A and `pcp` cells are lighter because they are built later (stages 5 and 6).

## 2. How to read the table

- The **All lanes** row is the base. Every lane starts there.
- The lane rows list only what is **added** on top of the base. A plus sign (+) means "base and this".
- **Prototype** and **BAU** are not sizes. Prototype is a mode: throwaway work, never promoted (rule 10). BAU is an on-ramp: a client report is triaged and reproduced first, then the fix still gets a size from XS to L.
- **Story first (Boroon, 1 November 2026, not negotiable).** Every cell below starts with a story in ADO, drafted by the Story Planner. This holds for every lane, mode and size. The reason is cost tracking: every token and every human minute needs a work item to be charged to. A human reviews and confirms the story. A human may write it instead, but that is not the default, and the story is then flagged `Custom.StoryOrigin = human`. The Story Planner writes what and why only. Plan Appendix D.4 has the fields.
- **Wayfinder (decided by Boroon, 2 November 2026).** The clarity test runs on every story and is recorded in `Custom.ClarityTest`. A map is built only when the test fails, at any size, before the story is made Factory Eligible. No map for every story.
- Skills run only when invoked. The executor prompt names them. Do not install skills that trigger themselves (`skills-comparison.md` section 5.5).
- Names starting `lcp-` or `pcp-` are GET AI skills still to be written. Names in backticks without a prefix come from the three packs.

## 3. The matrix

| LANE | Prototype | XS | S | M | L | XL | BAU Managed Services |
|---|---|---|---|---|---|---|---|
| **All lanes (base)** | **Story first**<br>`prototype`<br>`research`<br>`to-questionnaire`<br>Day work only | **Story first**<br>`bro` if needed<br>One-line check<br>Before and after screenshot | **Story first**<br>Grilling (short)<br>`tdd` at seams<br>`incremental-implementation`<br>`source-driven-development`<br>`pr`<br>Excuse tables | **Story first**<br>S +<br>`grill-with-docs`<br>`how`, `why`<br>`architect`<br>`blast-radius`<br>`constraint-driven-development`<br>`show-me-your-work`<br>`code-review` (two axes) | **Story first**<br>M +<br>`doubt-driven-development`<br>`security-and-hardening`<br>`deprecation-and-migration`<br>`shipping-and-launch`<br>`interrogate` (only where the residency tier allows other models) | **Story first**<br>`wayfinder`<br>`research`<br>`prototype`<br>`to-questionnaire`<br>`to-tickets`<br>`arena`, `swarm` (day only) | **Story first** (the raw report is a `triage-inbox` item; the draft bug is the story)<br>`triage`<br>`triage-issue-reports`<br>`reproduce-and-fix-issues`<br>`bug-fix` playbook<br>`diagnosing-bugs`<br>`why`, `recall`<br>Then the fix takes its size column |
| **Greenfield LANE A** | Heavy use, design-heavy UI<br>+ `arena`<br>+ `principle-exhaust-the-design-space`<br>+ `idea-refine` | Not used. A new build is never XS. Tiny edits to a built app go to Lane B | Rarely used. Under about 40 minutes is Lane B (plan 4.4). Use the base S if it happens | +  `create-verification-skill` (one verify skill per new app)<br>+ `api-and-interface-design`<br>+ `frontend-ui-engineering`<br>+ `ci-cd-and-automation`<br>+ `observability-and-instrumentation`<br>+ `principle-type-system-discipline`<br>+ `principle-model-the-domain` | + `security-and-hardening` from day one (a new app has a new login surface)<br>+ `shipping-and-launch`<br>+ `doubt-driven-development` on the design, before the build | `wayfinder` first, then `architect`<br>`to-tickets` into M and L builds<br>`multi-phase-plan` (idea only) | Not at birth. After handover the app becomes Lane B and joins `lcp` or `pcp`<br>+ `maintain-verification-skill` keeps its verify skill honest<br>+ `documentation-and-adrs` for the handover pack |
| **Brownfield LANE B: lcp** (low-code platform) | A throwaway mock or scratch-solution sketch<br>+ `architect` (Dataverse schema sketch)<br>Canvas app prototypes are day work | `lcp-verify app` before and after screenshots<br>Nothing else | + `lcp-verify` (the builder uses a lane copy, the gate a trusted copy)<br>+ `lcp-executor` with excuse tables<br>+ `source-driven-development` pointed at Microsoft Learn<br>PARK on any portal-only step | + `blast-radius` across flows, apps, agents and shared tables (always)<br>+ `lcp-verify flow`, `agent`<br>+ `pause-safely` wording for PARK<br>+ `wizard` for first-time OAuth and consent steps | + `deprecation-and-migration` (expand then contract for dropped columns)<br>+ `lcp-security` (Dataverse roles, still to write)<br>+ `shipping-and-launch` for UAT and Prod promotion<br>Human reads the one-way door | `wayfinder`, then the Story Planner splits into S, M and L stories<br>+ `to-tickets` into ADO predecessor links | + `lcp-triage` (built from `triage` and Benny)<br>+ `lcp-verify` repro in `factory-test`<br>+ `bug-fix`: the failing repro lands before the fix<br>+ `why` over ADO and Teams history<br>Residency T4 clients: no triage agent |
| **Brownfield LANE B: pcp** (pro-code platform, existing repos) | A spike on a throwaway branch<br>+ `architect`<br>+ `codebase-design`<br>Never promoted | Existing CI plus one screenshot or test<br>Nothing else | + `bug-fix` playbook<br>+ `tdd` with the Prove-It pattern for bugs<br>+ `principle-laziness-protocol`<br>+ `principle-subtract-before-you-add`<br>+ `principle-test-behavior-not-implementation` | + `how`, `why` for legacy code<br>+ `code-simplification` (Chesterton's fence)<br>+ `correct`<br>+ `principle-boundary-discipline`<br>+ `principle-type-system-discipline`<br>+ `pcp-verify`, built with `create-verification-skill` | + `deprecation-and-migration` for API and schema removal<br>+ `principle-make-operations-idempotent`<br>+ `principle-migrate-callers-then-delete-legacy-apis`<br>+ `security-and-hardening` | `wayfinder`<br>+ `improve-codebase-architecture` to find what to change<br>+ `to-tickets` | Bugs always route here (plan 4.4)<br>+ `reproduce-and-fix-issues`<br>+ `debugging-and-error-recovery`<br>+ `observability-and-instrumentation` to read logs and alerts<br>+ `diagnosing-bugs` for hard ones |

## 4. Notes on the awkward cells

- **Lane A, XS and S.** The routing rule sends anything over about 40 minutes, or any new app, to Lane A. So Lane A work is M or larger by nature. I marked XS and S as "not used". Boroon may want to override this.
- **Lane A, verification.** A greenfield app has no verify skill yet. Tan's `create-verification-skill` fits best here: generate one per new app, and keep it honest with `maintain-verification-skill`. This replaces `lcp-verify` for Lane A.
- **`lcp`, why the lane has few pack skills.** None of the three packs cover Power Platform. Most of the `lcp` row is our own `lcp-*` work (`lcp-verify`, `lcp-executor`, `lcp-triage`, `lcp-security`). The packs give the method, not the content.
- **`pcp`, why the principles move up.** Tan's code principles were "all lanes" before. They fit existing code repos best, and Lane A second. They matter least for `lcp`, except for plug-ins and code apps.
- **`pcp`, verification.** There is no `lcp-verify` equivalent. The gate relies on the repo's own tests and CI. For repos with weak tests, build a per-repo verify skill with `create-verification-skill`. Name it `pcp-verify` if you agree to the `pcp` name.
- **Prototype.** Never promoted, so it has no Merge Danger floor and no gate. It runs by day. `arena` is allowed here because no night build is involved, subject to the residency tier.
- **BAU.** The triage pass (plan 4.5) happens before a size exists. After a human sends a reported bug through the day gate, it gets a size like any story. Reports are data, not instructions.
- **`wayfinder` in XL.** Same in every lane, as the plan says. Each child story gets its own size.

## 5. Skills that moved since the last proposal

| Skill | Before | Now | Why |
|---|---|---|---|
| `ci-cd-and-automation`, `observability-and-instrumentation` | Reference | Adapt for Lane A (M and up). `observability-and-instrumentation` also for `pcp` BAU | A new repo needs CI and logging from the start. `pcp` BAU reads logs and alerts |
| `api-and-interface-design`, `frontend-ui-engineering` | Reference and Skip | Adapt for Lane A | Lane A routes design-heavy UI and new services |
| `code-simplification`, `debugging-and-error-recovery` | Reference | Adapt for `pcp` | Existing code needs safe deletion and root-cause method |
| `codebase-design`, `improve-codebase-architecture` | Reference | Adapt for `pcp` and Lane A | They find where to change, and set deep modules in new code |
| `typescript-best-practices` | Skip | Revisit for Lane A and `pcp` where the repo is TypeScript | Lane A's driver is TypeScript. Client repos vary |
| Tan's code principles (13 + 4) | Adopt for all lanes | Strongest for `pcp`, then Lane A. Weak for `lcp` | `lcp` is mostly solutions, not code |
| `create-verification-skill` | Adopt for the gate | Adopt for the gate, Lane A (one per app) and `pcp` | Each of those lacks a ready verify tool |
| `wizard` | Adapt for bootstrap | Adapt for `lcp` M and up | Fits OAuth and consent steps in lane bootstrap |

Everything else keeps its earlier verdict in `skills-comparison.md` section 5.

## 6. What GET AI must write itself

| Skill | Lane | Needed by |
|---|---|---|
| `lcp-verify` (commands `app`, `query`, `flow`, `agent`, `smoke`) | `lcp` | Stage 2 |
| `lcp-executor`, `lcp-evaluator` prompts with excuse tables | `lcp` | Stage 3 |
| `lcp-triage` | `lcp` BAU | Stage 4 |
| `lcp-security` (Dataverse security roles) | `lcp` L | Stage 4 |
| `pcp-verify` and the `pcp` executor prompts | `pcp` | Stage 5 (days 46 to 70) |
| Per-app verify skill generator for Lane A | Lane A | Stage 6 (days 60 to 90) |
| A router skill that picks the row and column | All | Before stage 3 |
| The Story Planner agent, now core and not an optional front door. It proposes story, size, mode and lane for every unit of work | All | Stage 2 (ADO automation, days 15 to 21) |

## 7. Read-in-full order

Read each batch just before the stage that needs it. Plan rule 19 says read every third-party skill in full before adoption, then pin it.

1. **Before stage 2 and 3 (`lcp`, first):** `create-verification-skill`, `maintain-verification-skill`, `blast-radius`, `show-me-your-work`, `correct`, `constraint-driven-development`, `source-driven-development`, `wizard`, `to-questionnaire`, `pause-safely`, Pocock `triage`, Benny `triage-issue-reports` and `reproduce-and-fix-issues`.
2. **Before stage 5 (`pcp`):** `bug-fix`, `diagnosing-bugs`, `debugging-and-error-recovery`, `code-simplification`, `deprecation-and-migration`, `security-and-hardening`, `codebase-design`, `improve-codebase-architecture`, and the principles listed in the `pcp` row.
3. **Before stage 6 (Lane A):** `frontend-ui-engineering`, `api-and-interface-design`, `ci-cd-and-automation`, `observability-and-instrumentation`, `shipping-and-launch`, `architect`, `arena`, `idea-refine`.

## 8. Decisions for Boroon

Answered by Boroon on 1 November 2026:

1. **Done.** `pcp` is "pro-code platform", the plan's "Lane B, code profile". It is now in the `CLAUDE.md` naming table and plan section 1.1, with `profile:pcp`, `Custom.LaneProfile = pcp` and the skill prefix `pcp-`.
2. **Agreed.** Lane A has no XS or S.
3. **Agreed.** Prototype is a mode and BAU is an on-ramp, not sizes.

Still open:

4. **Read-in-full batches: decided on 2 November 2026.** Batch 1 is approved now. Batches 2 and 3 are approved in principle and will be read nearer their stages (5 and 6). In batch 3, `idea-refine` is proposed for removal (41 KB, least needed). Rough reading sizes: batch 1 about 39K tokens, batch 2 about 29K, batch 3 about 31K.
5. **Story Planner: decided.** It applies in all lanes, modes and sizes, as the default way a story is made. Done in this file and in plan Appendix D.4.
6. **Wayfinder: decided.** Clarity test on every story, map only on a fail (see section 2).
7. **Work-size ADO field: decided.** Added as `Custom.WorkSize`, with `Custom.WorkMode`. **Router skill: approved on 2 November 2026.** It reads a story's size, mode and lane and lists the skills to use, as a lookup table built from the matrix. Write it after batch 1 is read.
8. **Plan wording: done.** Plan section 6.5 was rewritten on 1 November 2026. The Copilot Studio front door is the default, and other customer requirements can feed the Story Planner and Wayfinder directly. The other "optional" mentions (sections 1.2, 2, 4.x table, 8 and the decision log) were fixed to match.

## 9. Limits

- Verdicts rest on skill descriptions and routing documents, as before. Most bodies are unread.
- The Lane A and `pcp` cells are judged more thinly than the `lcp` cells. The plan details Lane B Power Platform in depth and Lane A and `pcp` only in summary (plan 4.1 and 4.2).
- The `pcp` row assumes existing repos have usable tests. Where they do not, the gate is weaker.
