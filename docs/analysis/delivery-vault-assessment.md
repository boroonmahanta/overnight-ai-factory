# Delivery vault assessment: what lane B (low-code) should take

Session 14, 6 November 2026. A fresh look at the Get AI Engineer's material and the 5 November call, against plan V3.1 for lane B, Power Platform profile.
Everything here is a proposal. The plan is not changed.

**Public repo.** No client, staff or engagement names. Engagements are "the current engagement" and "the past engagement"; people are "the Get AI Engineer" and "the engagement team". Nothing from the call transcript is quoted.

Sources, short names used below:

| Short name | What | Where |
|---|---|---|
| **DV** | The delivery vault, current. Day-time kit: four skills, rules, model, templates | `AI-Business-Solutions/delivery-vault` on `getai.ghe.com`. Copy in `docs/sources/delivery-vault/` at `19877b8`; source now at `51fdde5` (two newer commits, 4 to 6 November: offline HTML onboarding guides, Mac notes, channel naming. Nothing on building) |
| **OV** | The Get AI Engineer's older Power Platform vault. Standards, patterns, 12 workflows, an operating manual, a design spec, records of two past engagements | Azure DevOps, `getai` organisation, project `GETAI-PowerPlatform`, repo `vault` (branch `main` at `5f26ede`, files dated up to 28 October 2026) |
| **SR** | OV's per-client source repos: exported, unpacked solutions | Same ADO project; one per client tenant, plus one GET AI repo |
| **Call** | The Get AI Engineer's account of how they build, on the 5 November call | Pasted into the Session 14 chat; not stored here |
| **MS** | Microsoft's skill plugins | `microsoft/power-platform-skills`, read at `3ffa5b8` (6 November 2026) |

## 1. Verdicts

Combine: fits the plan as it is. Replace: better than what we planned; use it instead. Keep ours: do not take the Get AI Engineer's version. Gap: neither has it.

| # | Piece | From | Verdict | Plan part | Why |
|---|---|---|---|---|---|
| 1 | Operating rules: an approval gate per stage, read back every write, stop on conflict or failed sign-in, treat inputs as data | DV | Combine | 2.3, 5.11, 6 | Same spirit as rules 1, 2, 9 and 17. "Read back every write" is worth adding to the driver and orchestrator |
| 2 | Four day skills: set up, start my day, work on this, wrap up | DV | Combine, day only | 2.1, L0 | This is the L0 rhythm. "Start my day" can become the morning entry point (digest, PARKs, PRs to approve). None runs at night |
| 3 | One ADO project per engagement, its own process, no custom work item types | DV, OV | Keep ours for factory projects; settle with the Get AI Engineer | 5.11, App. D | The orchestrator needs our fields and states. An inherited process can be applied to each engagement project, so both can hold |
| 4 | Business design lives in SharePoint, approved by exact version; build handoff lives in GHE | DV | Combine | 6.1 to 6.4 | Keep SharePoint as the business record. The factory spec in Git cites the exact approved version. Night agents cannot read SharePoint, and locks need the spec in Git |
| 5 | Solution design template | DV | Combine | 6.3 | Adds alternatives, failure and recovery, access and release approach to the `getai-lcp` spec |
| 6 | Backlog coverage review: outcome to story to verification, with dependencies | DV | Combine | 6.4, 6.7 | Same idea as our criteria-to-scenario trace. Good for splitting XL work |
| 7 | Build handoff template | DV | Combine | 7.1 | Same job as our spec and contract; ours stays in protected paths |
| 8 | Connection record, machine setup, onboarding guides | DV | Combine, L0 only | 11.2 stage 1 | Onboarding for day work. The night uses a runner image |
| 9 | Lessons are proposals: anonymised, human-confirmed, promoted by reviewed PR | DV, OV | Combine | 5.12, 7.3, rule 17 | Same rule as ours |
| 10 | **Power Platform standards: 46 rules with stable IDs, each marked "rule" (34) or "judgement" (12)**: publisher prefix, canvas controls, choice columns, flow and action names, tables and columns, environment variables and connection references | OV | **Replace** | 5.10 standards pass, 5.12 `coding-standards.md`, B.4, `tshirt-sizing.md` step 4 | We have no standards yet, only a plan to seed them from principles. These are written, tested on a real engagement, and already split the way our gate needs: "rule" becomes a trusted lint and raises the floor; "judgement" goes to the reviewer's standards pass |
| 11 | Eight Power Automate patterns (secrets fetched at point of use, try/catch and the swallowed-failure rule, empty-string-safe environment variables, identifier versus label, and more) | OV | Combine | 5.12 skills, C.3 smells | Executor skill references and reviewer smells |
| 12 | **Export and unpack procedure**: fixed solution scope, no delete option by default, canvas app folder names normalised, ZIP timestamp churn is not drift, orphaned files reported not deleted, failures stop the run | OV | **Replace the procedure; keep our YAML format** | 5.4 reset step 4, 5.6 format and lane drift check | Hard-won detail our plan lacks. It uses the older XML layout and a separate canvas unpack; new factory repos stay on YAML (Microsoft's advice for new projects) |
| 13 | Generated inventories: components, environment variables, connection references; values redacted | OV | Combine (new to the plan) | 5.10 blast radius, 5.11 facts first, C.1 | Cheap facts for the executor and reviewer: "read the inventory before the source" |
| 14 | Standards check reports violations (rule) and observations (judgement); never auto-corrects | OV | Combine | 5.10, B.4 | Same as our deterministic floor plus raise-only review |
| 15 | ADO item type and state as the program counter; one "work" verb routes by state | OV | Combine by day; keep ours at night | 5.11 | At night the orchestrator owns state; agents never write ADO |
| 16 | No tenant writes from the vault; builds run in a separate session with the builder's own sign-in | OV | Combine the separation; keep our identities | 5.3, rules 5 and 6 | A personal sign-in with MFA cannot run at night. Per-lane service principals over OIDC are proven (spikes 0.2, 0.3) |
| 17 | **Build live in the environment (Studio or Microsoft's plugins), then export and unpack as the record** | OV, Call | **Replace, for most component types** | 5.6 builders and drift gate, 5.7 `build` job, B.1 | Microsoft supports this loop and does not support hand edits to extracted files. Keep builders only where Microsoft ships a generator. Section 3 |
| 18 | Design (SDD) template | OV | Combine | 6.3 | Adds: an environment variable and connection reference table with values per environment; names decided at design time; open questions split into "we can answer" and "ask the client"; check the inventory before proposing a new component |
| 19 | Per-story brief: a snapshot of the approved design for the build session | OV | Combine | 7.1 | Same idea as `handoff/<ado-id>/`; ours is in Git |
| 20 | Retro workflow: a skill only after three manual repeats; candidates go to a backlog; nothing auto-created | OV | Combine | 7.3, 7.4 | A good threshold for new skills |
| 21 | Microsoft plugins installed per user, auto-updating, never vendored | OV, MS | Keep ours for the night | 5.6, 8.3, rule 19 | The night vendors, reads and pins. Engineers' laptops by day are their own kit |
| 22 | Telemetry off for every plugin; scoped allow-list; never skip permissions while signed in to a client | OV | Combine | 5.2, 5.6 | Already our rule; theirs lists the variable names |
| 23 | Decisions, risks and deployments as Markdown registers (OV) or in ADO only (DV) | OV, DV | Keep ours | 6.2 `docs/adr/`, rule 9 | Night agents look facts up in the repo. Decision records stay in Git; the ruling is also on the ADO item |
| 24 | Client-side pre-push hook and file classes for shared files | OV | Keep ours as the lock | 5.7 rulesets | A local hook can be skipped; server-side rulesets cannot |
| 25 | Past engagement records: 14 decisions, 10 risks, 14 deployment records, 8 designs, 3 standards reviews | OV | Combine, kept private | 7.3 mining, stage 1 exit | The first mining set and a source of seeded test cases. Only anonymised findings leave ADO |
| 26 | Past engagement source repo: six exported solutions, XML layout, canvas apps unpacked apart, plug-in source | SR | Combine, kept private | 5.7, spike 0.10 | A real test input for pack, the manifest check and the checker before any client trial |
| 27 | Build self-test: the agent seeds data, runs the flow, checks the run, cleans up | Call; not found written down | Keep ours | 5.9 `lcp-verify` | `lcp-verify flow` does this with run tags. Their practice shows it works. Ask them for the prompt |
| 28 | End-of-build "learn from this conversation" step | Call; not found as a skill step | Combine | 7.3, trace reviewer | Fine by day with human confirmation. At night the trace reviewer drafts and humans promote |
| 29 | Managed and unmanaged zips snapshotted after each build | Call; only unmanaged zips found | Keep ours | 5.15 | The managed artefact is packed from `main` by trusted tooling |
| 30 | Reference-first building: hand-build the first app and flows so agents copy their conventions | Call | Gap: add | 6.3 | Neither the plan nor the vault names reference components. Add "reference components" to the spec |
| 31 | Microsoft canvas plugin | MS | Keep ours: day only | 5.6 | Needs an open Studio tab for the whole session |
| 32 | Microsoft Power Automate plugin (FlowAgent MCP, 50+ tools, validates before every create or update) | MS | Combine by day; night only after a spike | 5.6 MCP table | Signs in with `az login` and MSAL as a user. App-only sign-in untested. Night fallback: write the flow's `workflows` row through the Dataverse Web API, which Microsoft documents |
| 33 | Microsoft model-apps plugin: App Spec, lint, dry-run plan, idempotent apply, verify, download back to a spec | MS | Combine | 5.6 point 4 | A real builder input with a way back; keep as planned |
| 34 | A lane reset that removes components left by an earlier story | none | Gap | 5.4 | An unmanaged import does not delete components. Under live build a leftover would be exported into the next PR |
| 35 | Night access to client systems (connections needing client credentials) | none | Gap | 5.4 "which tenant", 9.4 | Neither solves it. Client-tenant lanes are a later stage (Boroon, Session 13) |
| 36 | A context budget per session (keep a session under about a third of the window) | Call (Boroon) | Gap | 5.2, 5.12 | The plan caps credits and loops, not context |
| 37 | Teams, SharePoint and ADO setup from the CRM entry; the project setup app | DV, `GetAI-IP/getai-project-setup` | Out of lane scope | none | Organisation setup, not the low-code lane. Only its file list was read |

## 2. Inventory

### 2.1 In the delivery vault (DV)

Read in full at `19877b8` (19 files), plus the Markdown changes and the text of the two HTML guides added since.

- Four skills: set up an engagement, start my day, work on an item (design, approved backlog batch, authorised build handoff), wrap up (evidence to ADO).
- Operating rules (seven approval gates), an operating model (who owns what across Teams, SharePoint, ADO, GHE), an ADO guide (discover the process, scoped write batches, read back), a stack-neutral standards baseline, a worked example.
- Four templates: engagement connection, solution design, build handoff, backlog coverage review.
- Machine setup and onboarding (Windows first; Mac and VS Code unverified), and since 5 November two offline HTML guides.
- **No Power Platform content.** No standards, no build skill, no export step, nothing on Microsoft's plugins.

### 2.2 Described on the call but not found

- A build skill that loads Microsoft's plugins, builds from an approved brief, then tests itself with seeded data and cleans up.
- An end-of-build step that rereads the session and proposes lessons.
- Snapshotting both managed and unmanaged zips after each build (only unmanaged exports were found).
- The "four slides" deck.
- Wrap-up raising pattern PRs automatically (the vaults only propose lessons for a human to confirm, which is the safer version).

### 2.3 Found elsewhere

- **OV, the older vault in Azure DevOps.** This holds most of what the call described: the six GET AI Power Platform standards documents turned into 46 rules with IDs; eight flow patterns; an export-and-unpack workflow with inventories; a standards-check workflow; a retro workflow with a skills and patterns backlog; a design template; a per-story build brief; an operating manual and a 1,065-line design spec, provider-neutral with Claude Code and Copilot adapters; telemetry and permission decisions for Microsoft's plugins; full records of the past engagement.
- **OV's design spec** confirms the build method: Microsoft's plugins or Studio write to the client's development environment in a separate session under the builder's own account; the vault never writes to a tenant; the next export brings the source back. It also lists the constraint that matters most for us: no unattended tenant access without a service principal the client's admin consents to.
- **SR, the per-client source repos.** The past engagement's repo holds six exported solutions in the XML layout, their zips, two canvas apps unpacked separately, and hand-written plug-in source. One deployment record shows a change made "in Studio, no import", then found by the next export. A GET AI repo holds solution zips and an architecture pack for the current engagement (seen by folder names only, not read), which suggests some of that work is already built in GET AI's tenant.
- **Nothing else of the Get AI Engineer's on `getai.ghe.com`.** The only other relevant repo is the project setup app in `GetAI-IP` (row 37). The handbook repo has no low-code standards.

## 3. How agents should build

**Recommendation: build live in the lane, export as the record.** Keep builders only where Microsoft ships a generator.

### 3.1 The evidence

- **Microsoft's supported loop is live edit, export, extract.** Its source control page says to edit components "through existing means", export and extract again, and that manual editing of extracted component files and zips is not supported, outside the few `customizations.xml` sections it lists. The plan already uses this to forbid hand edits; per-component builders that write flow JSON or table XML are the same thing done by a script.
- **The Get AI Engineer built this way for six months** on the past engagement, with Microsoft's plugins and Studio, then exported. The records show it worked for tables, columns, security roles, environment variables and connection references; canvas apps from scratch went badly without a hand-built reference.
- **Spikes 0.2 and 0.3 proved the lane can act headless.** `getai-fl1-exec` signs in by GitHub OIDC with no secret (pac and the Dataverse CLI), reads and creates through the Dataverse MCP server and the Web API, and its writes are recorded against the lane's application user.
- **Microsoft documents code paths for most components.** Solution-aware cloud flows are rows in the `workflows` table and can be created and updated through the Dataverse Web API. The model-apps App Spec applies tables, forms, views, roles and the sitemap. `pac copilot` and the `pa` CLI cover agents and code apps.
- **Builders are the plan's biggest unbuilt piece.** Per-component builders, `create_schema.py --plan`, `create_security.py --plan` and `sync_solutions.py` are among the gate's 20 unwritten scripts.

### 3.2 How it would work

1. **Reset** the lane to the head of `integration` (plan 5.4), then prove it: a fresh export must equal `integration` exactly, or the lane goes Offline. This needs leftover components removed (row 34).
2. **The agent changes the lane through supported tools only**: pac, the Web API (including `workflows` rows for flows), Dataverse MCP, the App Spec apply, and FlowAgent only if it works as the lane identity. It never edits exported files.
3. **The driver exports**, not the agent. After the session ends, a trusted step exports and unpacks the solution (YAML) into a clean tree, using the Get AI Engineer's procedure (row 12), throws away any agent edits under the solution folders, and commits. The PR's solution files come from trusted tooling, not from the model.
4. **The lane drift check keeps a job, with a new meaning**: a second export at lane close must equal the PR head (nothing changed after the export), and a query finds any component the lane identity created that is not in the solution.
5. **Generator-backed parts keep the plan's builder pattern** (5.6 point 4): App Spec, `pac copilot` agents, code apps, PCF and plug-in source live in Git as inputs and are drift-checked.
6. **Canvas apps stay day work** in Studio, as the plan says.
7. **The gate barely changes.** `build` packs the exported source offline with no credentials; `static`, `verify-in-test`, the verifiers and Merge Danger run as planned. Two edits: the B.1 path rules move from builder paths to the exported component folders (`entities/`, `workflows/`, roles, environment variables, connection references), and the `--plan` checks become a diff of exported table and role definitions against the Test baseline.
8. **One-way doors**: the lane is disposable, so a destructive change there is reversible. Keep the PARK before applying one at L1 anyway; the floor of 6 or more and a human still catch it at merge.

### 3.3 What it costs

- Reviewers read exported YAML diffs instead of builder inputs. Microsoft calls these diffs minimal and readable; the standards (row 10) and inventories (row 13) give the reviewer something to check them against.
- Exports re-serialise, so the drift check compares canonical files (the plan already says this) and ignores ZIP timestamp churn (the Get AI Engineer's procedure).
- Reset fidelity becomes critical (row 34).

### 3.4 What is not proven yet

| Item | Why it matters | Where to test |
|---|---|---|
| Headless YAML export as the lane identity | Microsoft's pages disagree: the YAML reference says `pac solution clone` and `sync` produce YAML; the Git integration FAQ says `unpack`, `clone` and `sync` do not support it yet | New spike |
| Reset fidelity: after reset, an export equals `integration` | Leftovers would ride into the next PR | New spike, with 0.10 |
| A solution flow created and updated through the Web API as `getai-fl1-exec`, then exported | The night's main way to build flows | Widen 0.14 |
| FlowAgent and the App Spec apply signed in as the lane identity (`az login` with a federated token) | Decides whether Microsoft's plugins run at night or only by day | Widen 0.14 |
| Where Microsoft's plugins stop for approval when run with `--no-ask-user` | Decides PARK points | 0.14, as planned |

If headless YAML export fails, fall back to the XML layout for flows and tables (what the Get AI Engineer used) and keep canvas apps out of the night, until Microsoft's tooling catches up.

### 3.5 Live build against builders, side by side

Added 7 November 2026. 🟢 wins that row, 🔴 loses it, ⚪ a tie.

**Score: live build 10, builders 5, ties 3.**

| Factor | Live build, export as the record | Builders (plan 5.6) | Wins |
|---|---|---|---|
| Microsoft support | 🟢 The supported loop: change through tools, export, extract | 🔴 Writes extracted files by script, which Microsoft does not support | 🟢 Live |
| Build effort left | 🟢 A driver export step and three spikes; reuses the Get AI Engineer's procedure | 🔴 Every per-component builder and both plan checks still unwritten | 🟢 Live |
| Components covered | 🟢 Tables, columns, roles, environment variables, connection references, views, forms and flows through Microsoft's APIs | 🔴 One builder per component type, written and kept by us | 🟢 Live |
| Proven in practice | 🟢 Six months on the past engagement; lane sign-in proven by spikes 0.2 and 0.3 | 🔴 Never run anywhere | 🟢 Live |
| Keeping up with Microsoft | 🟢 Microsoft's tools own the file format through renames and new component types | 🔴 We chase every format change | 🟢 Live |
| Fits L0 day work | 🟢 Humans in Studio and agents at night both produce an export | 🔴 A human Studio edit counts as drift; engineers must learn builders | 🟢 Live |
| Use of Microsoft's skills | 🟢 App Spec, Web API and MCP used directly | 🔴 Each generator must be wrapped and drift-checked | 🟢 Live |
| Agent's build loop | 🟢 Sees the change in the lane at once | 🔴 Pack and import each loop, 5 to 10 minutes | 🟢 Live |
| Time to L1 | 🟢 About a week earlier (section 5.2) | 🔴 The Session 13 baseline | 🟢 Live |
| Unproven parts | 🟢 Three spikes: YAML export, reset fidelity, flows by Web API (section 3.4) | 🔴 The whole builder library, plus the support risk | 🟢 Live |
| Reviewer sees intent | 🔴 Reads exported YAML: the result, not the intent | 🟢 Reads small builder-input diffs that state intent | 🟢 Builders |
| Clean diffs | 🔴 Exports re-serialise; needs a canonical compare | 🟢 Stable output by design | 🟢 Builders |
| One-way doors | 🔴 Applied in the lane first; caught at the gate | 🟢 The plan check flags a drop before anything applies | 🟢 Builders |
| Leftovers and side changes | 🔴 Needs a reset-fidelity proof and a query for components outside the solution | 🟢 The lane drift check flags anything not in the repo | 🟢 Builders |
| Edits with no lane | 🔴 Needs a live lane per story | 🟢 The cloud agent can edit inputs, checked by an offline pack | 🟢 Builders |
| Rule 5, credentials | ⚪ The trusted driver exports; the gate packs offline | ⚪ Builders run in the no-credential job | ⚪ Tie |
| Canvas apps | ⚪ Day work in Studio | ⚪ Day work in Studio | ⚪ Tie |
| Generator-backed parts | ⚪ App Spec, agents, code apps, PCF and plug-ins kept as inputs | ⚪ The same | ⚪ Tie |

Live build wins on cost, Microsoft support, proof in practice and speed to L1. The builders' five wins are about review and safety, and each has a fix that works with a live build:

- **Reviewer sees intent:** the standards (row 10) and the generated inventories (row 13) give the reviewer something to check the exported YAML against.
- **Clean diffs:** compare canonical files and ignore ZIP timestamp churn, as the Get AI Engineer's procedure already does.
- **One-way doors:** at L1 the agent still PARKs before a destructive change, and a floor of 6 or more brings in a human at merge.
- **Leftovers and side changes:** prove after each reset that the lane equals `integration`, and query for any component the lane identity made outside the solution.
- **Edits with no lane:** this mainly helps the cloud agent, which is not part of the low-code night plan.

## 4. Day-time skills versus the night lane

The vaults assume a person approves each step. At night nobody does. What changes:

| By day (vault) | At night (lane) | Why |
|---|---|---|
| A human approves each write batch, scoped and named | Approval moves earlier and later: Factory Eligible, locked scenarios and the approved night plan cover the story's writes to its own lane; the morning PR approval covers the result | Rules 1, 2, 3 |
| The agent writes to ADO and SharePoint after approval | The agent writes only files and its lane. The orchestrator writes ADO. Nobody writes SharePoint | 5.11 |
| Reads the approved design from SharePoint by exact version | Reads the spec in Git, which cites that version. No Microsoft 365 identity in the lane | Rule 5, 6.4 |
| Asks one question at a time | Looks facts up, then PARKs on a decision with `questions.md` | Rule 9 |
| Signs in as the person, with MFA | Signs in as the lane's service principal over OIDC; a failed sign-in marks the lane Offline, not the story | 5.3, spikes 0.2 and 0.3 |
| Builds in the client's development environment | Builds only in a GET AI lane at L1; client-tenant lanes later | 5.4, 9.4 |
| Microsoft's plugins ask before acting | `--no-ask-user` with explicit allow and deny lists; a plugin approval point becomes a PARK unless the night plan pre-approved it | 5.2, 0.14 |
| Plugins installed per user and auto-updated | Vendored, read in full, pinned; auto-update off | Rule 19 |
| Learns from the session at wrap-up, a human confirms | The trace reviewer drafts at 06:00; lessons are hints (last 50); the weekly retro promotes by PR | 7.3, rule 17 |
| Snapshots zips by hand | The driver exports; the gate packs; promotion packs managed from `main` | 5.15 |
| One person decides when a story is done | The gate and fresh verifiers decide | Rule 2 |
| Sessions can run long; context grows | One story per session, a credit cap, a loop cap, and (proposed) a context cap | Row 36 |
| "Start my day" reads assigned work | Becomes the morning entry point: the digest, PARKs, PRs to approve, one failed trace to read | 2.1 |

## 5. Timeline for the low-code lane

### 5.1 Assumptions

- Today is Friday 6 November 2026. The plan's own targets: Stage 1 exit by day 14 (15 November) and Stage 3 exit, with L1 possible, by day 30 (30 November).
- Baseline (Session 13, one person, Boroon near full time on the factory): **L0 trial early December 2026; L1 night-shift trial second half of January 2027.**
- GET AI is assumed to be closed from Monday 21 December to Friday 1 January, back Monday 4 January 2027. Ignite is 17 to 20 November.
- L0 here means: engineers on an engagement build with agents by day, export, and their PRs pass the gate (static checks, pack, checker, import into `factory-test`). L1 means Stage 3's exit test passed, then night PRs on real stories with a human approving each.
- **Any trial on a live engagement needs someone from that engagement** to own the spec, write or check scenarios, and approve PRs. Boroon may not approve alone a client release he started (plan 2.2). Without the Get AI Engineer's time, trials run on GET AI's own work.

### 5.2 Effect of the Get AI Engineer's material

Saves about 6 to 8 person-days: standards and lints are written (row 10), the export procedure is known (row 12), the builders and their plan checks are dropped (section 3), and the first mining set exists (row 25). Costs about 2 to 3 days in new spikes (section 3.4). **Net: about one week earlier than the baseline.**

### 5.3 Dates

| Scenario | L0 trial | Stage 3 exit (three unattended nights, internal stories) | L1 trial | Against the plan |
|---|---|---|---|---|
| Baseline (Session 13): one person | Early December | Mid January | Second half of January | 3 and 7 weeks late |
| **A. One person, the Get AI Engineer's material, no Get AI Engineer time** | Week of 30 November, GET AI work only | About 11 to 15 January | From about 18 January, GET AI work only. A live engagement waits for its team | 2 and 7 weeks late |
| **B. One person plus the Get AI Engineer's time** (half a day a week until the trial, then 30 to 60 minutes each morning) | Week of 30 November, on the current engagement, limited to work with no client connections | About 11 to 15 January | From about 18 January, on the current engagement | As A, but on real work |
| **C. A second engineer full time, plus the Get AI Engineer's time** | About 23 to 27 November, on the current engagement | About 14 to 18 December | One week before the break is possible (14 to 18 December) only if the exit passes the week before. Recommended start: 11 January | About 2 weeks late for L1 |

The Get AI Engineer's time does not make the build much faster. It makes a live trial possible: a spec owner and test author who is not the builder (rule 3), a morning reviewer, and real stories.

**Boroon's goal from the call** (done by end of November, a couple of projects started by mid-December): L0 by end of November is reachable in scenario C and nearly in A and B. A night shift on one project by mid-December needs scenario C. A couple of projects at once needs three lanes (Stage 4), not before late January in any scenario.

### 5.4 What each date depends on

| Dependency | Needed for | Owner |
|---|---|---|
| Rulesets applied (move step 12) and a private caller repo in the engagement's org; checks (a) and (d) of the caller design | L0 | Boroon |
| `factory-test` with `getai-<proj>-test`, a test user and its premium licence; spike 0.11 (test user under Conditional Access) | L0 import; verifiers at L1 | Boroon, platform |
| Minimal gate scripts for L0: pack, manifest check, checker SARIF, Test import, lints from row 10 | L0 | Boroon |
| `getai-lcp` preset v0 from the plan's fields plus rows 5 and 18 | L0 | Boroon, Get AI Engineer |
| Current engagement: residency tier T1 or T2, the client's agreement, and stories with no client connections that can be built in GET AI's tenant | Any live trial | Get AI Engineer, engagement lead |
| New spikes: YAML export headless; reset fidelity; flows by Web API as the lane identity (section 3.4) | Stage 3 | Boroon |
| Spike 0.6 (Copilot CLI on GHE.com, billing identity) and 0.13 (ADO service principal) | Stage 2 and 3 | Boroon, platform |
| Stage 2: orchestrator, ADO fields, ledger v0, `lcp-verify` v0 and the first verify profile | L1 | Boroon |
| Spike 0.1's invoice check (one to three weeks elapsed) | Pricing, not the trial | Boroon |
| Ignite renames (17 to 20 November) | Names and tooling | Boroon |

## 6. Questions for the Get AI Engineer

Ask:

1. Is the ADO vault retired, or still in use beside the delivery vault? Which one holds the standards from now on, and who owns them?
2. Will you agree to the 46 standards becoming the lane's coding standards, reviewed by PR, with "rule" items enforced by the gate?
3. On the past engagement, roughly what share of changes was made in Studio by hand, by Microsoft's plugins live, or by editing unpacked files then packing and importing? Which component types went well and badly?
4. The flow update that stripped a connection's client ID and secret: which tool and which operation did it? We want a lint for it.
5. Did you ever run Microsoft's plugins signed in as a service principal, or only as yourself? Which plugins stopped to ask for approval mid-build?
6. How does your build test itself: seeded data, flow runs, run history, clean-up? Is that prompt written down?
7. What exactly does your end-of-build "learn from this session" step ask the agent?
8. Do you keep managed zips anywhere? Have you tried the YAML source format?
9. On the current engagement, which stories in the next six weeks need no client-system connections? Can they be built in GET AI's tenant and delivered as a solution? What is the client's residency tier, and does the contract allow agents?
10. Will you, or a teammate, own the spec and the scenarios for five to ten stories, and approve PRs each morning during a trial? How much time per week until Christmas?
11. Which existing app and flows would you name as reference components for agents to copy?
12. How should your delivery-setup step and the project setup app fit together? (A separate conversation; not the lane.)

Ask them to send:

- The build prompt or skill they use with Microsoft's plugins (not in either vault).
- The self-test prompt and the end-of-build learning prompt, word for word.
- Two or three anonymised build sessions (Claude Code or Copilot exports) for mining.
- The list of Microsoft plugins and versions they use, and their telemetry settings.
- The "four slides" deck.
- A short list of candidate stories from the current engagement that need no client connections.
- Confirmation that the six original standards documents have no newer versions than the ones distilled into the ADO vault.

## 7. Plan edits I would propose (not made)

1. **5.6, "Builders and the drift gate"**: make "build live in the lane, export as the record" the default; keep builders only for generator-backed parts (App Spec, `pac copilot`, code apps, PCF, plug-in source); the driver exports, not the agent.
2. **5.6, lane drift check**: redefine as "a second export equals the PR head" plus "no component created by the lane identity outside the solution".
3. **5.6, solution format**: record that Microsoft's pages disagree on YAML support in `unpack`, `clone` and `sync`; add the spike; name the XML fallback.
4. **5.4, per-story reset**: add the reset-fidelity check, leftover removal, and Offline on mismatch.
5. **5.7 and Appendix A**: drop the per-component builders, `create_schema.py --plan`, `create_security.py --plan` and `sync_solutions.py` from the trusted scripts; add an export-diff plan check and lints from the "rule" standards.
6. **Appendix B.1**: remap path rules to the exported component folders.
7. **5.12 and Appendix C.1 (`lcp-executor`)**: "never edit exported solution files; change the lane through pac, the Web API, MCP or the App Spec; the driver exports"; read inventories before source; add the flow patterns as a skill; add a context cap.
8. **5.10, 5.12**: seed the lane's `coding-standards.md` from the Get AI Engineer's 46 standards: "rule" to lints and the floor, "judgement" to the reviewer.
9. **6.3, `getai-lcp` preset**: add environment variables and connection references with values per environment (no default for a value that differs by environment), names decided at design, reference components, open questions split by who answers, and an inventory check before proposing a new component.
10. **6.4 and Appendix D**: one ADO project per engagement, with the factory's inherited process and fields applied to it.
11. **5.6, Microsoft plugins**: canvas plugin by day only; Power Automate plugin signs in as a user, so night use waits on a spike, with the Web API `workflows` route as the fallback.
12. **7.3 mining**: name the past engagement's records and the Get AI Engineer's sessions as the first mining set, kept private, anonymised findings only.
13. **11.1**: add spikes for headless YAML export and reset fidelity; widen 0.14 to flows by Web API, FlowAgent and the App Spec apply as the lane identity.
14. **2.1, morning**: name "start my day" as the reviewer's entry point.
15. **5.10**: add generated inventories as an input to blast radius and the reviewer.

**Status, 7 November 2026 (Session 15).** Boroon decided:
- **Items 1 to 7, 11 and 13:** made, as live build in the lane.
- **Item 8:** agreed for low-code; made in plan 5.10 and 5.12.
- **Item 9:** agreed for low-code; made in plan 6.3.
- **Item 10:** agreed for every lane; made in plan 6.4, Appendix D and 14.4:
  - ADO is GET AI's and holds Kanban boards only;
  - repos sit on GET AI's GitHub Enterprise, with pipelines and tests on GitHub Actions;
  - the vault's engagement projects take our process;
  - there is one internal project for the factory.
- **Item 12:** moved out of the current stages into a new last stage 9, with a mining agent of its own for every engagement type.
- **Item 14:** agreed for low-code; made in plan 2.1.
- **Item 15:** assessed for both profiles in section 10, for Boroon to decide.
- **Overall rule:** our plan wins on design, and the Get AI Engineer's material is the default source for anything it does not settle (plan 14.4).
- **Anonymising:** anything from the older ADO vault comes over anonymised, by a reviewed PR.

## 8. Where this differs from Session 13's quick take

Sections 1 to 7 were drafted before reading `docs/analysis/delivery-vault-fast-track.md`. Compared afterwards:

**Agree.** The vault is a stack-neutral day kit that fits the day gate and L0. At night, Factory Eligible plus the approved handoff must be the whole authorisation, and anything else PARKs. The pilot should be limited to work with no client connections, built in `factory-lane-1`, on a T1 engagement. The lane's own sign-in removes the Get AI Engineer's lost-session problem.

**Differ:**

| Topic | Session 13 | This assessment | Why |
|---|---|---|---|
| Where the Power Platform material is | Not in the vault; probably elsewhere; ask the Get AI Engineer for it | Found in the older ADO vault: 46 standards, 8 patterns, the export procedure, inventories, a design template, and the past engagement's records and source | Session 13 could not see Azure DevOps. The ask to the Get AI Engineer is now much narrower (section 6) |
| How agents build | A difference to settle before Stage 3 | Decide now: build live, export as the record, builders only where Microsoft ships a generator (section 3) | Microsoft's source control page does not support editing extracted files; the builders are the plan's largest unbuilt piece; the lane identity is proven |
| "Update inventory" | Exports managed and unmanaged and unpacks to YAML (from the call) | The written procedure exports unmanaged only and unpacks to the XML layout, with canvas apps apart. Headless YAML export is unproven, and Microsoft's pages disagree | Read the workflow and the source repo, not the call |
| Spikes 0.6 and 0.14 together | Microsoft's skills may not prompt once the lane is signed in | The Power Automate plugin signs in as a user (`az login` plus MSAL) and the canvas plugin needs an open Studio tab, so neither is a safe night assumption. Add the Web API route for flows, a YAML export spike and a reset-fidelity spike | Read Microsoft's plugin docs |
| Dates | Day trial early December credible; night trial towards early to mid January if the Get AI Engineer has time | Day trial week of 30 November; night trial from about 18 January with one person; mid-December only with a second engineer. The Get AI Engineer's time enables a live trial rather than speeding the build | The new spikes cost 2 to 3 days and the break sits in the middle |
| ADO | Tags fit both | Keep our custom fields too, by applying the factory's inherited process to each engagement project | The orchestrator needs the fields (Appendix D) |
| Session mining | Start now with the engagement team's wrap-up lessons | Also mine the past engagement's records, which already exist. They are records, not chat sessions, so they add to the 20 sessions rather than replace them | Found in the ADO vault |
| Missing from Session 13 | | Reset fidelity (row 34), reference components (row 30), a context cap (row 36), inventories as reviewer input (row 13) | |

## 9. What was read, and limits

- **DV**: all 19 files at `19877b8`; the Markdown changes in `19877b8...51fdde5`; the text of the two new HTML guides (onboarding only).
- **OV**: the README, `AGENTS.md`, the operating manual, the workflows `work`, `update-from-client`, `repair-inventory`, `check-standards` and `suggest-patterns-and-skills`; the design spec's sections 4, 5, 9 to 12 and 14.4 to 14.5; the Claude Code adapter; the plugin usage notes; six of the seven standards files and their index; two of the eight patterns; the design template; one deployment record. **Not read**: the other seven workflows, the spec's other sections, six patterns, the client-token standard, scripts and hooks, the dashboard, timesheets, and most past engagement records.
- **SR**: the past engagement repo's README and folder layout; the GET AI repo's file list. No solution content was read.
- **MS**: the top README, the Power Automate plugin's README, `AGENTS.md` and setup skill, and searches of the model-apps README and canvas `AGENTS.md`.
- **Microsoft Learn**: source control with solution files; the YAML format reference; the `pac solution` reference; the Git integration FAQ; working with cloud flows using code.
- Read-only throughout. Nothing changed on `getai.ghe.com`, in Azure DevOps or in the tenant.
- Effort and dates are my estimates from the plan's stage contents and the Session 13 baseline, not measurements.

## 10. Inventories for low-code and pro-code: decision matrix (item 15)

Added 7 November 2026 (Session 15), at Boroon's request. A proposal; nothing here is in the plan yet beyond what Session 15 already made.

**The idea.** A generated, deterministic list of the things a diff does not show: what else uses a changed component, and which settings and connections it touches. People and agents read the list before the source. It should be cheaper and steadier than asking an LLM to work out the blast radius from the diff alone.

### 10.1 What each profile's inventory would hold

| | Low-code (lane B, `lcp`) | Pro-code (lane B code profile, `pcp`, and Lane A) |
|---|---|---|
| What it lists | Components and what uses them (tables, columns, flows, apps, agents, roles), environment variables, connection references. Names and types only; values redacted | Config keys and secret references (names only); infrastructure resources; database tables from migrations; public routes or contracts where a spec file exists; the internal import graph of changed files [inference] |
| Source | The driver's export (YAML), following the Get AI Engineer's inventory procedure, with the least change (the precedence rule) | The PR's own files, parsed without running them |
| Who makes it | The driver, after each export; trusted | A trusted gate step, in a job with no credentials (rule 5); the agent wrote the code, so it must not write the inventory |
| Where it lives | Committed beside `src/` by the driver; the gate regenerates it and fails on a mismatch | Gate evidence only, never committed |
| Effort | Small: parse the export the driver already makes | Medium: one parser per stack (TypeScript, Python, .NET), plus infrastructure files and migrations [inference] |
| When | Stage 3, with the driver | Stage 5 (code profile), Stage 6 (Lane A) |

### 10.2 Decision matrix against our plan

Markers: 🟢 better than our plan now, ⚪ no real change, 🔴 worse or a new risk.

| Use | Our plan now (after Session 15) | Low-code with inventories | Pro-code with inventories | Proposed decision |
|---|---|---|---|---|
| Reviewer's blast radius (B.4 spec pass) | Low-code: the reviewer reads the inventories (C.3) and judges. Pro-code: the reviewer judges from the diff | ⚪ Already done | 🟢 The reviewer sees who else imports a changed file, and which config and migrations it touches | Low-code: keep. Pro-code: adopt at Stage 5 |
| Deterministic floor (rule 11) | Paths (B.1) and the export-diff plan (B.2). Nothing about shared use | 🟢 New rule: a change to a component the inventory shows another app, flow or agent uses has a floor of at least 3. This matches size M, "shared table" | 🟢 Same pattern: a change to a file other packages import, a public contract, a config key, a migration or an infrastructure resource has a floor of at least 3 | Adopt for both. Low-code at Stage 3; pro-code with its Stage 5 path rules |
| Verifier count (B.6) | "3 when the blast radius names another app or flow", fed by the export-diff plan | 🟢 The "used by" links make that test deterministic | ⚪ Pro-code has one evaluator, not one to three verifiers. The inventory sets its regression focus instead | Low-code: adopt. Pro-code: use for regression focus only |
| Executor facts first (rule 9) | Low-code: read the inventories before the source (C.1). Pro-code: the agent searches the code | ⚪ Already done | ⚪ The cloud agent and the SDK session search code well. A gate-made inventory reaches them only after the PR | Low-code: keep. Pro-code: skip for now |
| Day spec: check before proposing a new component | Low-code: the `getai-lcp` preset's inventory check (6.3, item 9) | ⚪ Already done | 🟢 Stops a duplicate service, table or config key being specified | Pro-code: add to the GET AI preset at Stage 5 |
| Triage (outer loop, 4.5) | The triage agent finds components by search | 🟢 Maps a client report to the components and flows it touches | 🟢 Maps a report to the routes and services it touches | Adopt for both at the Stage 4 outer-loop pilot |
| Gardening (7.4) | Scans for smells | 🟢 Finds orphans: unused environment variables and connection references | 🟢 Finds unused config keys and dead routes | Adopt for both with gardening at Stage 4 |
| Data exposure | No inventories for pro-code | 🔴 Values could leak. Names and types only; never values | 🔴 Same: config key names only, never values or secrets | A lint fails any inventory that holds a value |
| Trust | n/a | 🔴 An agent commit could alter a committed inventory. The gate regenerates it and fails on any difference | ⚪ Gate-made, so the agent cannot touch it | Low-code: the gate regenerates and compares. Pro-code: never committed |
| Build effort | None | ⚪ Small; the procedure exists | 🔴 A parser per stack | Pro-code: start with config keys, infrastructure and migrations, plus the import graph for the main stack |

**Counts.** Low-code: 4 better, 4 no change, 2 new risks, each with its answer. Pro-code: 5 better, 3 no change, 2 new risks, each with its answer.

**What it means.** For low-code, Session 15 already did most of item 15. What is left is one floor rule, the verifier test, and the gate's regeneration check. For pro-code, inventories pay off in review, the floor, triage and gardening. They do not help the agent while it builds. Start small at Stage 5.

**Decided (Boroon, 7 November 2026), and made in plan 5.6, 5.10, 11.2, Appendices A and B, and 14.4:**
1. The two floor rules (shared use raises the floor to at least 3), one per profile: agreed.
2. Pro-code inventories made by the gate and never committed: agreed.
3. A lint that fails any inventory holding a value: agreed, "with reasons". The plan reads this as a lint whose failure gives its reasons: the entry, why values are barred, and the fix.
