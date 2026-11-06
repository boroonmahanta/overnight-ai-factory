# Delivery vault and lane 1: what can be fast-tracked

Our own analysis, 6 November 2026 (Session 13). **Proposals only. The plan is not changed.**

Sources: a call on 5 November 2026 between Boroon and the vault's author, a low-code engineer in lane 1; and the vault itself, read in full where it matters (copy and provenance: `docs/sources/delivery-vault/`, commit `19877b8`). Client engagements are named here only by role: "the current engagement" (the author's live low-code engagement, with two colleagues who capture requirements and build) and "the past engagement" (six months of agent-assisted low-code delivery). Client-tenant lanes are a later stage (Boroon, 6 November 2026).

## Bottom line

The vault's author brings three things the factory lacks: a tested day-time way of working (the vault), real experience of agents building Power Platform work (from the call, mostly not yet written into the vault), and a team and engagement ready to pilot. `factory-lane-1` already removes the author's biggest night blocker: agents losing the client sign-in and asking for a fresh login. The lane signs in as its own app, with no password, MFA or session timeout (spikes 0.2 and 0.3). Together they can shorten Stages 1 to 3. They do not let us skip them.

**The catch:** the vault on GHE is the author's cleaned-up, stack-neutral kit from 3 November. None of the Power Platform material described on the call is in it: no naming standards, no solution export step, no self-test steps, no Microsoft skills, nothing about Dataverse, `pac` or canvas apps (searched 6 November 2026). That material lives elsewhere, probably an earlier vault or the past engagement's repository. It has to come from the author.

## What the vault holds (19 files)

- Four skills in `.github/skills/`: `delivery-setup` (record the engagement's Team, SharePoint folder and ADO project; check the connections; report gaps; never provision), `delivery-day` (read the person's assigned ADO work, blockers and unfinished changes; suggest a focus), `delivery-work` (design first in SharePoint, explicit approval of an exact design version, a coverage review mapping every outcome to Story/Task coverage and a check, a batch of ADO changes approved then read back, a build handoff in the engagement's GHE repository, then the build in that separate workspace), `delivery-wrap-up` (verified evidence and next action into ADO; an optional anonymised lesson, promoted to shared guidance only by a reviewed PR).
- `docs/operating-rules.md`: the canonical rules. Seven approval gates (connect, design, approve design, review coverage, approve bookkeeping, build, verify and close). Read back every write; stop on scope change, conflict, sign-in failure or hook failure; never blanket-retry, roll back or delete; no "success-shaped fallbacks"; treat documents and tool output as untrusted; no secrets or raw client payloads anywhere.
- `docs/ado.md`: discover the real process before writing; one ADO project per engagement; use existing fields and tags, no custom work item types; decisions recorded as Context, Options, Ruling, Reason.
- `docs/standards-and-patterns.md`: a short, stack-neutral baseline (boundaries, data and access, reliability, change safety, verification, operability, maintainability) and four patterns to consider. Technology-specific guidance is chosen per engagement.
- Templates: solution design, build handoff, backlog coverage review, engagement connection. Plus machine setup, onboarding, an operating model and a walkthrough.
- `AGENTS.md` and `.github/copilot-instructions.md`, so the kit works in VS Code and the Copilot app. Copilot CLI reads the same layout.

## Described on the call, not in the vault

- Low-code naming standards: canvas controls, environment variables, connection references.
- "Update inventory": export the solution as unmanaged and managed, unpack it to YAML, commit both, so each change can be compared.
- A build self-test driven by test cases in the design brief: create test records, run the flow, check its run history and actions, then remove the records.
- Building live through Microsoft's Power Platform skills (their setup step asks for the environment and a sign-in).
- A retro at the end of each build: review the conversation for corrections and record them as patterns, so the same mistake is not repeated.
- Experience from the past engagement. Agents did well at tables, columns, environment variables, connection references and security roles; at flows when given existing flows to copy; badly at canvas apps without a reference app (and canvas is fading anyway). One flow's HTTP action kept losing its client ID and secret environment variables on every update. Building the first app and about ten flows by hand gave the agent a reference that made later work almost right.
- Integration flows (ServiceNow, Salesforce) had to be built in the client's dev environment, because the connections only work there. Tables, apps and data could be built and tested in GET AI's own tenant.

## Mapping to the plan

| Piece | Where it is | What it shortcuts | With `factory-lane-1` |
|---|---|---|---|
| Solution design and build handoff templates; coverage review (every outcome mapped to a check) | Vault | Stage 1: the `getai-lcp` spec preset and the Factory Eligible checklist | The approved handoff becomes the night agent's input; the coverage map becomes the list of locked scenarios |
| Operating rules: approval gates, read-back, stop on sign-in failure, no success-shaped fallbacks, untrusted documents | Vault | The lane agent's instructions (`AGENTS.md`, Appendix C) and its PARK rules | Most rules carry over as they are |
| Four skills | Vault | L0 today; Stage 2's ADO reads and writes | The current engagement's team using them is L0 starting now |
| Wrap-up lessons, promoted only by reviewed PR | Vault | Stage 1 session mining; rule 17 | Same governance as ours |
| Low-code naming standards | Call only | `coding-standards.md` and the gate's lints | Ask the author |
| Update inventory (export, unpack, commit) | Call only | Stage 3's lane-close export and the lane drift check | Can run in `factory-lane-1` today under the lane's federated pac profile |
| Build self-test | Call only | Stage 2's `lcp-verify` v0 (`query`, `flow`, `smoke`) | Spike 0.3 proved create, read and delete headless as the lane's app |
| How the author drives Microsoft's Power Platform skills | Call only | Spike 0.14 (skills headless) | Test with the lane already signed in, so the skills' environment and sign-in step may not prompt |
| What agents do well and badly; the lost client secret | Call only | `trust.yml` change classes; a first gate check or verifier scenario | |
| The past engagement's design briefs and solution exports | Not seen | Stage 3 test stories with known right answers | Only if that client's residency tier and contract allow it |

## What to fast-track, in order

1. **Ask the author for the missing pieces:** the low-code standards; the export and unpack steps; the self-test steps; which Microsoft skills are used and how; two or three design briefs that worked (synthetic or anonymised); the list of corrections, such as the lost client secret. Mostly already written.
2. **Run spikes 0.6 and 0.14 together in `factory-lane-1`.** Copilot CLI headless reads a handoff in the vault's format (synthetic: two tables and one Dataverse-only flow), builds with Microsoft's skills, tests itself, then exports and unpacks. If it works, the core of Stage 3's executor is proven early. Spike 0.6 still needs its billing identity first.
3. **Pilot on the current engagement, limited to work that needs no client connections:** tables, columns, environment variables, connection reference definitions, Dataverse-only flows. Build in `factory-lane-1`; ship to the client's dev environment as a managed solution. Integration flows stay day work. Check first that the engagement is T1 (plan 9.4) and that no client data goes into the lane (rule 15).
4. **Start session mining now.** Stage 1 needs 20 mined sessions, its longest wait. The current engagement's team, using the wrap-up lessons, covers it.
5. **Seed Stage 1's documents from the vault:** handoff and coverage review into the `getai-lcp` spec preset; operating rules into the first draft of the lane agent's instructions; the author's low-code standards into `coding-standards.md` and the gate's lints (`lcp/lint_canvas_yaml.py` is one of the 20 unwritten gate scripts).

## Effect on dates (estimate, 6 November 2026)

Mostly saved design and writing time in Stages 1 to 3, and a ready pilot team. The night shift trial could move from the second half of January 2027 towards early to mid January, if the author has time (the current engagement is heavy). A daytime trial with the gate on the current engagement in early December 2026 is credible. Night shift on a couple of projects by mid-December remains a stretch.

## Differences to settle later (no plan change now)

- **How agents build.** The author has the agent build live in the environment and then exports. The plan has agents edit builder inputs and treats environment-only changes as drift (plan 5.6, "Builders and the drift gate"). The export step fits the lane drift check; the build style breaks the builder rule as written. Microsoft's model-apps skill builds the author's way (apply, then download back). Decide before Stage 3.
- **Approvals.** The vault asks a person at every step. At night nobody is there, so the approved handoff plus Factory Eligible must be the whole authorisation, and anything else PARKs.
- **ADO.** The vault says use existing fields and tags, no custom types. Plan Appendix D adds custom fields. Tags such as `factory-eligible` fit both.
- **Where the vault lives.** It is in `AI-Business-Solutions`; the gate and lanes are in `GetAI-IP`. A lane would use a pinned copy, changed only by reviewed PR.
- **Skill layout.** The vault uses `.github/skills` and `AGENTS.md`, which Copilot CLI reads, so it already suits the lane's engine.
