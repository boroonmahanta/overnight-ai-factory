# Stage 1 build plan: the day gate

Written 7 November 2026 (Session 17, a cloud session, planning only). ADO story 2543, brought forward from 12 November. Decisions D1 to D6 are Boroon's, made in this session.

This covers the day-gate parts of Stage 1 (plan section 11.2, stage 1 row), the way `stage-1-gate-build-plan.md` covered the gate builds:

| ADO | Story |
|---|---|
| 2545 | `glossary.md`, `docs/adr/` templates and the coding standards seed |
| 2544 | Pin Spec Kit; GET AI and `getai-lcp` presets v0 |
| 2546 | Locked scenario conventions and the Playwright kit v0 |
| 2548 | Mine at least 20 human-led sessions, with spike 0.17 (2466) |

Left out: the gate scripts (2538). Their order waits on spike 0.18 (2462, Monday 9 November). Where a day-gate piece needs a gate script, this plan says so and leaves it to 2538.

## Where things stand

- None of these pieces existed when this plan was written. The plan describes them in 6.1 to 6.4, 5.8 and 7.3. The DG1 templates exist since 7 November (Session 18).
- Two live skills already hold the formats we need: `getai-domain-modeling` (the `glossary.md` and ADR formats, adapted 2 November 2026) and `getai-grilling` (the grilling rules). Use them; do not write new formats.
- The Get AI Engineer's material is the default where the plan does not settle a point (plan 14.4). From the delivery vault copy (`docs/sources/delivery-vault/`): the solution design, build handoff and backlog coverage templates, and the rule that business designs stay in SharePoint, approved by exact version. From the older ADO vault (laptop only): the 46 standards, the retro and "suggest patterns and skills" workflows, the design template and the per-story build brief.
- `GetAI-IP/factory-manifestos` exists since 13 November 2026 (DG3, Session 23): private, default branch `main`, with the repo ruleset `main-protection`.

## Decisions (Boroon, 7 November 2026)

**D1. Where the files are built: draft here, move later.** The templates, the two presets, the spec check, the scenario rules and the Playwright kit draft are built in a staging folder in this repo, so cloud sessions can build them. One laptop session (DG8, Friday 4 December) moves them to `GetAI-IP` on `getai.ghe.com`. The 46 standards go only to GHE, never to this repo. The catch, accepted: this repo is public, so the staged presets stay in its public history.

**D2. Spec Kit pin: the newest 1.3.x.** Not 1.2.x as the plan says. On build day (DG4), pin the newest 1.3.x release after reading its release notes. Boroon also asked for an action to keep Spec Kit and the other kits current: A1 below. (My suggestion of waiting until a release is two weeks old is not part of his answer; DG4 reads the notes and pins.)

**D3. The spec check script is built in 2544, with the presets.** It enforces the presets' rules, needs no tenant and does not wait on spike 0.18. Wiring it into `lcp-gate.yml` as a job joins the factory-gates list for 2538.

**D4. Locked Web API tests are YAML, in the same shape as workflow scenarios.** `tests/acceptance/api/*.yaml` uses the schema of `tests/scenarios/*.yaml`: seed rows with a run tag, act, assert fields and plug-in trace logs, clean up. The trusted runner reads both, so no extra test code runs in the job that holds the Test credentials, and people who do not code can write them.

**D5. Mining: engineers' sessions first, Boroon's top up.** Engineers' delivery sessions count first. If fewer than 20 have arrived by Friday 4 December, Boroon's own laptop Claude Code sessions fill the gap, up to 10 of the 20. The mix is recorded.

**D6. Test target: Microsoft's Northwind Traders sample solution.** Microsoft's Playwright samples already test it (canvas, model-driven and custom page). It holds no client data, so notes about it can be public. It is the solution for the kit test (DG9) and the human PR in the Stage 1 exit test (2539).

**A1. Keep pinned kits current (Boroon's action, for later).** Spec Kit moved three releases in five days (1.3.0 to 1.3.2). Proposed shape, not built:
1. One pin register listing every third-party kit we pin: Spec Kit, Microsoft's Playwright samples, `power-platform-skills`, the Dataverse skills, pac, Copilot CLI, Playwright, axe-core and the actions. For each: the pin, where it is pinned, how it is watched.
2. Dependabot wherever the ecosystem allows. It already watches the actions in `factory-gates`; it can also watch npm, pip and NuGet pins.
3. A manual pass for the rest at the monthly component register review (plan 8.2), and after each Microsoft or GitHub event (Ignite, Build, Universe). The first pass goes with the Ignite re-check on Monday 23 November.
4. Every update is read in full and moved by PR (plan 8.3, rule 3).

The next laptop session creates an ADO story for it (see `docs/progress.md`, Session 17).

## Where the files are built (D1)

```
staging/
  README.md                    what this is, where each part moves, the move date
  factory-manifestos/          moves to GetAI-IP/factory-manifestos (this folder is its root)
    README.md
    templates/project/         copied into each project repo at these paths
      glossary.md
      docs/adr/README.md
      coding-standards.md      how the file is read; the standards themselves are only on GHE
    spec-kit/
      presets/getai/           the GET AI preset
      presets/getai-lcp/       the low-code preset
      extensions/getai-spec-check/   the before_implement hook
      bundles/getai-lcp/bundle.yml   lean + getai + getai-lcp + assess + bug + spec check
    conventions/
      locked-scenarios.md
      scenario.schema.json
  factory-gates/               files added to GetAI-IP/factory-gates by PR (this folder mirrors its root)
    spec/check_spec.py
    tests/test_check_spec.py
    tests/fixtures/specs/
    playwright/                the kit v0 (the gate runs it as gate/playwright)
```

Rules for the staging folder:
- Nothing in it may name a client, a person or an engagement (public repo).
- Machine-read names stay product-neutral (rule 18).
- Python is standard library only, run with `python3 -I`, tested with `unittest`, as in `factory-gates`.
- The `glossary.md` and ADR templates are copies of the formats in `.claude/skills/getai-domain-modeling/`. When one changes, change both in the same PR.

## How to start each build session

1. Read `CLAUDE.md`, `docs/progress.md`, `docs/plans/schedule.md`, then this file.
2. Read only the plan lines named for that session. Line numbers are as at Session 16; if the plan has changed, run `grep -n '^## \|^### ' docs/sources/plan-v3.1.md`.
3. Start a branch from `main` that carries the ADO ID, for example `claude/session-<n>-2545-templates`.
4. Cloud sessions cannot reach `getai.ghe.com`, the tenant or ADO. Write ADO updates into the progress entry for the next laptop session.
5. End as usual: progress entry, time and tokens (or "cloud session, not recorded"), commit, push, no pull request unless asked.

## The build sessions, in order

### DG1. Templates (2545, part 1). Saturday 7 November (brought forward from Thursday 12 November). Cloud

**Done 7 November 2026** (Session 18, branch `claude/session-18-2545-templates`): `staging/README.md`, `staging/factory-manifestos/README.md` and the three files in `staging/factory-manifestos/templates/project/`.

Read: plan 6.2 (lines 959 to 973), 5.10 standards pass (line 782), 5.12 (lines 870 to 897), the two format files in `.claude/skills/getai-domain-modeling/`.

1. Create `staging/README.md` and `staging/factory-manifestos/README.md`.
2. `templates/project/glossary.md`: the glossary format, with the `_Schema_` line for both profiles (Dataverse table and column, flow or app for low-code; code symbol for pro-code). One synthetic example term.
3. `templates/project/docs/adr/README.md`: the ADR format and the three tests for when to write one (hard to reverse, surprising, a real trade-off). No fake `0000` record: records start at `0001` and are created lazily.
4. `templates/project/coding-standards.md`: a short header only. What the file is, that the reviewer's standards pass reads it, that "rule" items become gate lints that can raise the floor and "judgement" items go to the reviewer, and that it changes only by a reviewed daytime PR (rule 17). Do not invent an entry format: DG3 takes the Get AI Engineer's format as it is.
5. A note in the manifestos README on how a project repo takes the templates: copied in by a reviewed daytime PR, into protected paths (`glossary.md`, `docs/adr/**`, `coding-standards.md`).

Done when: the three templates match the skill's formats, and nothing in them is client-specific.

### DG2. Spike 0.17, session export (2466). Wednesday 18 November. Laptop, apps only, no tenant

Read: plan 7.3 (lines 1136 to 1142), spike 0.17 (line 1435).

1. On the laptop, export one session by hand from each tool an engineer uses: VS Code Copilot Chat, the Copilot app if there is one, Copilot CLI, and Claude Code (`/export <file>` writes plain text; the raw transcript is `~/.claude/projects/<project>/<session>.jsonl`). Record the command, the format, and whether tool calls and file edits are included. This session could not check the VS Code or GitHub docs (their hosts did not resolve), so this is the first check.
2. Write `docs/plans/spike-0.17/README.md`: the how-to for engineers, one short section per tool, plus a checklist for removing client data (names, tenant URLs, record values, screenshots) before sending.
3. Set up where exports go: a restricted folder in GET AI's SharePoint, readable by Boroon and each sender (the delivery vault keeps inputs in SharePoint). Raw exports never enter any repo.
4. Check whether a cloud session can read that folder through the Microsoft 365 connector. If yes, mining batches can run in the cloud; if not, they run on the laptop.

Done when: a readable transcript without client data exists for each tool, and the how-to is ready for the checkpoint on Friday 20 November.

### DG3. The coding standards seed and the older vault's methods (2545, part 2). Friday 20 November. Laptop

**Run 13 November 2026** (Session 23, brought forward from 20 November): `GetAI-IP/factory-manifestos` created, with `main-protection` (pull request required, 0 approvals until a second approver, no deletion, no force push), at Boroon's word. Pull request 1 there adds `practices/lcp/coding-standards.md`: 50 standards, not 46, because Boroon kept the vault's four client-token standards (`TOK`). **Merged by Boroon on 13 November 2026** (merge commit `fd2e268`), so 2545 is done. The notes for DG4 and DG6 are in `docs/progress.md`, Session 23. Step 5 waits for DG2. The eight flow patterns were not read in full (their names are noted); read them when `lcp-flow-patterns` is built.

Read: plan 5.10 (line 782), 5.12 (lines 881 and 894); assessment rows 10, 11, 14, 18, 19 and 20 (`docs/analysis/delivery-vault-assessment.md`).

1. Through Boroon's Azure CLI sign-in, read from the older ADO vault (`getai` organisation, project `GETAI-PowerPlatform`, repo `vault`): the 46 standards and their index, the eight flow patterns, the retro workflow, the "suggest patterns and skills" workflow, the design (SDD) template and the per-story build brief. Read only; change nothing there.
2. Create `GetAI-IP/factory-manifestos` on `getai.ghe.com`: private, default branch `main`, protected like the other `GetAI-IP` repos.
3. By PR there: `coding-standards.md` for the low-code profile, from the 46 standards in their own format and IDs, anonymised (no client, person or engagement names; synthetic examples). Each keeps its "rule" or "judgement" mark. Boroon merges. Ask the Get AI Engineer to review it (assessment section 6, question 2); their review does not block the merge.
4. Write into the progress entry, for DG4 and DG6: the design template's sections (for the `getai-lcp` plan template), the build brief's sections (for `handoff/`), and the retro workflow's rules (for mining), each anonymised.
5. Checkpoint, same day: send the engineers the DG2 how-to and ask for their exports.

Done when: `coding-standards.md` is merged in `factory-manifestos` with all 50 standards (the 46 plus the four `TOK`, Boroon, 13 November 2026) and none names a client. The "rule" lints are not written here: they are gate scripts (plan 5.7), for 2538 or a later slice.

### DG4. Spec Kit pin and the two presets (2544, part 1). Monday 23 and Tuesday 24 November. Cloud

Read: plan 6.1 to 6.3 (lines 940 to 998), 6.6 and 6.7 (lines 1035 to 1066), 8.3 (lines 1202 to 1211); the delivery vault's `templates/solution-design.md` and `templates/build-handoff.md`; DG3's notes in the progress log; the Ignite re-check from the same morning.

1. Pick the pin (D2): the newest 1.3.x, after reading its release notes. Install in the scratchpad with `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.3.<n>`. Check whether the PyPI `specify-cli` versions match the tags; if they do, a hashed requirements pin lets Dependabot watch it (A1).
2. Run `specify init --integration copilot` in a scratch folder. Read in full every template and command we override (plan 8.3). Check two things the docs did not show: where specify's three-marker cap lives, and whether an `update-agent-context` step still exists (plan 6.1 turns it off).
3. `presets/getai/` (plan 6.2):
   - `preset.yml`.
   - The constitution: tests and docs for every change, locked acceptance tests, evidence rules, Australian English.
   - The spec template: header fields for lane, profile, ambition (low by default for client work), ADO ID and work size; the SharePoint design's identity and exact approved version (delivery vault); acceptance criteria with IDs (`AC-<n>`) so scenarios can point at them; an NFR section; a Constraints section (plan 6.6).
   - The `specify` and `clarify` command overrides: raised question caps and the grilling rules from `getai-grilling` (at most five questions a round, facts versus decisions, the confirmation gate), and capture of glossary terms and decision records in the DG1 formats.
   - A GET AI checklist.
   - The prototype option (plan 6.7): a spec field for the mock or prototype link, and a short guide (the `proto` publisher prefix; never promoted). The prototype lint is a gate script, for 2538.
4. `presets/getai-lcp/` (plan 6.3):
   - A spec section with every field in the 6.3 table; each must be filled or marked "not applicable" with a reason. Names point at `coding-standards.md` by standard ID.
   - The plan template from the delivery vault's solution design and build handoff, with the least change: alternatives, failure and recovery, access, verification and release approach.
   - An lcp checklist.
5. `extensions/getai-spec-check/`: an `extension.yml` that declares a `before_implement` hook with `optional: false`, which runs its copy of `check_spec.py` (DG5). Hooks live in extensions, not presets.
6. `bundles/getai-lcp/bundle.yml`: the lean preset, `getai`, `getai-lcp` (in that priority order), the `assess` and `bug` extensions and `getai-spec-check`.
7. Record each vendored or generated third-party piece (Spec Kit, its generated skills) with its source and licence, for the component register (plan 8.2) and the A1 pin register.

Done when: in a scratch folder, `specify init`, then installing the bundle from the staging folder (`specify bundle install <path>/bundle.yml`, or `specify preset add --dev` for each), gives a project whose spec template shows every GET AI and lcp field.

### DG5. The spec check script (2544, part 2). Wednesday 25 November. Cloud

Read: plan 6.1 rules (line 957), 6.4 (lines 1000 to 1011), 6.6 (lines 1035 to 1042).

1. `staging/factory-gates/spec/check_spec.py --spec <spec.md> --profile lcp [--repo <root>]`. It fails on:
   - an open `[NEEDS CLARIFICATION]` marker;
   - an unticked item in any of the spec's checklists;
   - a missing or empty NFR section;
   - an assumption not marked approved;
   - a missing or invalid lane, profile or ambition field;
   - for `lcp`, any 6.3 field neither filled nor "not applicable" with a reason;
   - no acceptance scenario IDs, or a criterion with no scenario ID.
   It warns (does not fail) when a spec names libraries, schemas or file layouts outside Constraints (plan 6.6). With `--repo`, it also checks each listed scenario ID resolves to a file under `tests/`. The full criterion-to-scenario trace stays with `trace_criteria.py` (2538).
2. Tests and fixtures: a good lcp spec passes; one fixture fails for each rule above; the design-leak case warns only.
3. The extension's copy of the script is byte-identical to the gate's; a test checks the two hashes match, so they cannot drift.
4. Check that the 2538 list in `docs/progress.md` (Open items, the `factory-gates` follow-ups, item 8) still matches the script as built (D3): a job in `lcp-gate.yml` that runs the gate's trusted copy on spec PRs and checks the hash of the copy vendored under `.specify/`.

Done when: all tests pass, and the stage 1 exit clause "a spec with an open marker or no scenarios cannot become Factory Eligible" is shown by two fixtures failing. (In stage 1 there is no orchestrator yet, so "cannot become Factory Eligible" means the check fails. Stage 2's orchestrator reads the same result.)

### DG6. Mining 20 human-led sessions (2548). Thursday 26 November to Friday 11 December. Documents, or laptop per DG2

Read: plan 7.3 (lines 1106 to 1142), the retro rules from DG3's notes, the 11.2 stage 1 exit test (line 1444).

Human-led by design: do not automate the retro (plan 7.3). Four batches:

| Date | Batch |
|---|---|
| Thu 26 Nov | 1: whatever has arrived. If nothing has, try the method on two of Boroon's sessions (they count under D5's cap) |
| Thu 3 Dec | 2 |
| Fri 4 Dec | Cut-off (D5): count engineers' sessions; if under 20, choose up to 10 of Boroon's to top up |
| Tue 8 Dec | 3 |
| Fri 11 Dec | 4, then close |

Each batch:
1. Read each session with Boroon. Note every place the human corrected the agent, using the 7.3 checklist. Give each session an anonymous code (for example `S07`); never its owner, client or engagement.
2. Cluster the corrections across sessions.
3. For each repeated correction, raise one of: a skill change, a lint, a coding standard, or a glossary entry, by PR. Or record "no action" with a reason. Use the older vault's bar for new skills (only after three manual repeats) unless DG3 finds otherwise.
4. Record findings in `docs/analysis/session-mining.md` (public, anonymised): the correction, the session codes, the count, the action and its PR or ADO item.
5. Where each PR goes: lane skills and standards to `factory-manifestos` (laptop after DG8), lints to `factory-gates` (laptop), skills for this repo's own work to `.claude/skills/` here.

Before batch 1: raise Claude Code's transcript retention on the laptop. Transcripts are deleted after `cleanupPeriodDays`, 30 days by default, so the sessions from 4 November go on about 4 December. Set it in the next laptop session, at Boroon's word.

Done when (stage 1 exit, 11.2): at least 20 sessions mined, with the mix recorded (D5), and every repeated correction is a PR or a recorded "no action".

### DG7. Scenario conventions and the Playwright kit draft (2546, part 1). Monday 30 November to Wednesday 2 December. Cloud

Read: plan 5.8 (lines 665 to 698), 5.9 accessibility (line 735), Appendix A `verify-in-test` (lines 1999 to 2015), 13 (line 1502); Microsoft's Playwright samples docs (overview, get started, configuration, sample tests, authentication guide).

1. `conventions/locked-scenarios.md`, one section per type in the 5.8 table:
   - where each type lives;
   - IDs: every scenario has an `id` and a `criteria` list of spec `AC-<n>` IDs; Playwright tests carry the same IDs as tags (`@AC-1`), so `trace_criteria.py` can read every type;
   - run tags on every seeded row, in a fixed place the nightly sweeper can find;
   - the selector rule: accessible name first, `data-control-name` second, never CSS paths;
   - serial runs for tests that share a record type;
   - who writes them: a person who is not the worker, approved by `@acceptance-owners`. The `test-author` agent is not in stage 1;
   - the held-out set uses the same formats, in `factory-holdout`.
2. `conventions/scenario.schema.json`: one JSON Schema for workflow and Web API scenarios (D4): seed, trigger (HTTP, row create or update, or none), expected rows and fields, flow run status, plug-in trace log checks, timeout, cleanup by run tag. The runner (`run_workflow.py`) and a schema lint are gate scripts, for 2538.
3. `staging/factory-gates/playwright/`, the kit v0 (plan 13):
   - Microsoft's toolkit (`power-platform-playwright-toolkit` in `microsoft/power-platform-playwright-samples`) vendored at a pinned commit. Microsoft ships it as source to reference locally, not as an npm package. Read it in full first (plan 8.3) and record its source and licence.
   - `playwright.lcp.config.ts`: specs from `TEST_SPECS_DIR` (`*.spec.ts`, as plan 5.8 says; also `*.test.ts`, Microsoft's naming); one worker and no full parallel to start, as Microsoft advises for a shared environment; one retry in CI; trace on first retry; HTML and JUnit reporters; canvas and model-driven projects with their storage states; the sign-in variables Appendix A already uses.
   - Helpers: the accessible-name selector, the run tag, an axe-core pass against a baseline of known platform violations, and a keyboard-only journey.
   - Northwind example specs (D6), adapted from Microsoft's samples to our conventions.
4. Checks the cloud can run: `npm ci`, a type check, and `npx playwright test --list`. Nothing signs in.

Done when: the conventions, the schema, the example scenarios and the kit's example specs agree with each other, and the kit type-checks and lists its tests.

### DG8. Move the staged files to GHE (D1). Friday 4 December. Laptop

Read: Session 9's entry in `docs/progress.md` (how `factory-gates` moved).

1. In the clone, delete Finder's `.DS_Store` files first.
2. `staging/factory-manifestos/` into `GetAI-IP/factory-manifestos` with its history (a subtree split, merged by PR beside DG3's standards).
3. `staging/factory-gates/` into `GetAI-IP/factory-gates` by PR: `spec/`, its tests and fixtures, and `playwright/`. Regenerate `scripts.sha256`; run every test; check `self-test` is green.
4. A PR here deleting `staging/`, leaving a pointer in `CLAUDE.md`.
5. Settle how the two copies of the glossary and ADR formats stay the same (added Session 18). After the move, the skill (`.claude/skills/getai-domain-modeling/`) stays here and the templates are in `factory-manifestos`, so the staging rule "change both in the same PR" no longer works. Agree a way with Boroon, for example two PRs that link each other, and write it into the `factory-manifestos` README and `CLAUDE.md`.
6. Boroon merges all three.

Done when: both GHE repos hold the files with tests passing, `staging/` is gone from `main` here, and the way the two format copies stay the same is written down.

### DG9. Test the kit against `factory-test` (2546, part 2). Monday 14 and Tuesday 15 December. Laptop

Needs first: 2541 (`factory-test` bootstrapped), 2447 (spike 0.11, test user sign-in), 2538 (`run_workflow.py`, for the YAML scenarios).

1. Import the Northwind Traders sample solution into `factory-test`, if 2541 has not.
2. Run the kit's Northwind specs as the certificate test user, headless.
3. Run the example workflow and Web API scenarios through `run_workflow.py`.
4. Record run times against plan 5.8's estimates, and any flaky step.
5. Fix the kit by PR in `factory-gates`.

Done when: the Northwind specs and scenarios pass headless in `factory-test`, and the times are recorded. Then 2539 (Friday 18 December) can run the full gate on a human PR to the Northwind solution.

## How the stage 1 exit test is met

| Exit clause (plan 11.2) | Met by |
|---|---|
| A spec with an open marker or no scenarios cannot become Factory Eligible | DG5's fixtures; then 2539 on a real spec PR |
| A human PR runs the full gate in Test and posts evidence | DG7 and DG9, on Northwind (D6); with 2538, 2541, 2447 |
| At least 20 human-led sessions mined; each repeated correction a PR or a recorded "no action" | DG6 (D5) |
| Spec Kit pinned, presets v0 with the grilling rules, templates and the prototype option, gate script as hook and CI check (build column) | DG1, DG4, DG5; the CI job via 2538 (D3) |

## Facts checked this session (7 November 2026)

- **Spec Kit releases** (https://github.com/github/spec-kit/releases and `/tags`): 1.2.0 on 13 October to 1.2.6 on 2 November; 1.3.0 on 3 November, 1.3.1 on 5 November, 1.3.2 on 6 November (latest). 1.3.0 removed `/speckit.taskstoissues` in favour of the `github` extension.
- **Pinning** (Spec Kit `docs/installation.md`): `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z`. `specify-cli` is also on PyPI; whether its versions match the tags was not checked.
- **Presets** (`docs/presets/overview.md`, `api.md`): `preset.yml`; they override templates, commands and scripts; install with `specify preset add --dev <folder>` or `--from <archive URL>`; a bundled `lean` preset exists.
- **Extensions and hooks** (`docs/extensions/api.md`): hooks are declared in an extension's `extension.yml` and registered in `.specify/extensions.yml`; `before_implement` exists; `optional: false` makes the hook automatic. `assess` and `bug` are first-party.
- **Bundles** (`docs/bundles/overview.md`): `bundle.yml`, installed with `specify bundle install <name or path>`.
- **Copilot integration** (`docs/integrations/copilot.md`): skills land in `.github/skills/speckit-<command>/SKILL.md`, a protected path.
- **Not found in the docs read**: the three-marker cap in specify, and `update-agent-context`. DG4 checks the templates.
- **Microsoft's Playwright samples** (https://learn.microsoft.com/power-platform/developer/playwright-samples/overview and its get started, sample tests and configuration pages): a Rush monorepo with `power-platform-playwright-toolkit` ("Reference this package locally") and `e2e-tests`, whose samples "target the Northwind Traders solution". Advice for a shared Dataverse environment: `workers: 1`, `fullyParallel: false`; `retries: 1` in CI; trace on first retry. Tests named `<feature>.test.ts`. Node 20 or later.
- **Claude Code** (https://code.claude.com/docs/en/commands and `/claude-directory`): `/export [filename]` writes plain text; transcripts are `~/.claude/projects/<project>/<session>.jsonl`, deleted after `cleanupPeriodDays`, 30 days by default.
- **Not checked**: VS Code chat export, Copilot CLI session logs and any Copilot app export. `code.visualstudio.com` and `docs.github.com` did not resolve from this session. DG2 checks them by hand.

## Risks

- **Spec Kit moves fast.** Our command overrides are copies of upstream templates, so each update can conflict. Keep overrides small, and read the diff of every update (A1).
- **Microsoft's toolkit is samples, not a supported package.** It can change without notice. Vendor at a commit; watch it under A1.
- **One worker in Test.** Microsoft's advice for a shared environment can make the Test queue longer than plan 5.8's 20 to 55 minutes. DG9 measures it.
- **Mining depends on other people.** D5's top-up keeps the exit date, at the cost of fewer lane lessons.
- **Transcript retention.** 30 days by default on the laptop. Raise it before batch 1.
- **Public history (D1).** The staged presets and conventions stay readable in this repo's history after the move, unless the repo is made private.
- **Ignite (17 to 20 November)** may rename products or change tools. DG4 starts after the Monday 23 November re-check.
- **DG9 waits on 2538.** If the gate scripts slip, the YAML scenarios cannot run on 14 December; the Playwright half can.

## Plan edits made for these decisions

Made in `docs/sources/plan-v3.1.md` in this session, at Boroon's word ("Yes, edit now"):
1. 6.1: pin the newest 1.3.x (D2); the hook comes from a GET AI extension and the script's source is `factory-gates` `spec/` (D3).
2. 11.2, stage 1 build: Spec Kit 1.3.x (D2) and the Northwind test solution (D6).
3. 5.8, server logic row: YAML in the workflow scenario schema, read by the trusted runner (D4).
4. 5.12, Factory Manifestos: `GetAI-IP/factory-manifestos`, private, staged here until 4 December (D1).
5. 14.4: one row for D1 to D6.

Not edited: plan 8.2 for A1, which is an action for later. Older mentions of "Spec Kit 1.2" (the bottom line, section 3, the 5.1 day gate row and the 6.1 heading) name the generation the research described and are left as they are.

## Not in these sessions

- The gate scripts (2538), including `run_workflow.py`, `trace_criteria.py`, the standards lint, the schema lint, the prototype lint and wiring `check_spec.py` into `lcp-gate.yml`.
- The `test-author` agent, verify profiles (stage 2) and the held-out set (stage 4).
- Pro-code standards and a `pcp` preset (stage 5).
- Mining past engagements (stage 9).
