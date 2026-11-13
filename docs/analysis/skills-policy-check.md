# The third-party skills policy, checked against every vendored skill

Date: 11 November 2026 (Session 21, a cloud session). ADO 2549. Plan 8.3, points 1 to 5, checked against every third-party skill in the repo: the shelf in `skills/` and the live skills in `.claude/skills/` built from it. Point 6 is a note at the end.

## How it was checked

- **Pins and copies.** Each source was cloned at its pin. Every shelf file was compared with the upstream file at the pin by git blob hash: 56 skill folders, 4 reference files and 4 licence files. All are byte-identical.
- **Live skills.** Each live skill was compared with its shelf original. Each adopted skill differs only by its GET AI note and the edits that note names. Each copied script (`quality-gate.mjs`, `log.sh`, `template.sh`) and template matches its original. All 44 live skills now name their source commit in their first lines.
- **Loaded files.** Every link that leaves a skill's own folder was listed, on the shelf and live. One file a live skill points to had never been copied or read (see `doubt-driven-development`).
- **Updates.** `git ls-remote` on each source, and a diff of the copied folders from the pin to today's head.
- **Auto-update and telemetry.** The repo has no `.claude/settings.json` and installs no plugin or marketplace. Skills are plain files in Git, so nothing updates them on its own. No script in `skills/` or `.claude/skills/` calls the network. `poteto-mode`'s `bootstrap.ts` installs from npm, but it is shelf only and never run.
- **Licences.** Read from each upstream licence file at the pin.

## Gaps common to every row, now fixed

| Point | Gap | Fix (11 November 2026) |
|---|---|---|
| 4. Source and licence in the register | No register file. Source and licence were only in `skills/README.md` | `docs/component-register.md`, one row per source (Boroon's choice) |
| 4. Licence | All three sources are MIT, which asks that the notice go with every copy. The repo is public and held no licence text | Each upstream licence file copied unchanged to `skills/addy/`, `skills/pocock/`, `skills/tan/` and `skills/benny/` (Boroon's choice). The live skills built from them are covered by those files |
| 3. Updates reviewed as a PR | No update has happened yet, but nothing watched the sources | The register's "Watched by" column: a manual pass at the monthly review, first on 23 November. Checked today: nothing to take |
| 2. Pin; auto-update and telemetry off | None | Met by copying files at a commit |

## The table

Key to the reading records, all in `docs/analysis/`: **N1** `skills-reading-notes.md` (the first 16, every file including scripts), **N2** `skills-reading-notes-batch2.md`, **N3** `skills-reading-notes-skill-batches.md`, **this** this file. Commits in full are in `docs/component-register.md`. Licence is MIT for every row. "Source line" means the dated GET AI note at the top of a live skill that names its source and commit.

| Skill | Source | Commit | Licence | Read in full (where recorded) | Status | Gaps | Fix |
|---|---|---|---|---|---|---|---|
| `constraint-driven-development` | Addy, `skills/` | `301b02b` | MIT | Yes, 3 files with the script (N1) | Live, adopted unchanged | No source line | Line added (Boroon, 11 November) |
| `doubt-driven-development` | Addy, `skills/` | `301b02b` | MIT | Yes (N1); its linked `references/orchestration-patterns.md` only today (this) | Live, adopted unchanged | No source line. It points twice at `references/orchestration-patterns.md`, which was never copied or recorded as read, and the link does not resolve from `.claude/skills/` | File copied to `skills/references/` and read in full: no scripts, no network, nothing aimed at a reviewer, and the skill quotes the one rule it takes. Line added, naming the broken link |
| `source-driven-development` | Addy, `skills/` | `301b02b` | MIT | Yes (N1) | Live, adopted unchanged | No source line | Line added |
| `code-simplification` | Addy, `skills/` | `301b02b` | MIT | Yes (N3) | Shelf | None | None |
| `deprecation-and-migration` | Addy, `skills/` | `301b02b` | MIT | Yes (N3) | Shelf | None | None |
| `security-and-hardening` | Addy, `skills/` | `301b02b` | MIT | Yes, with `hardening-patterns.md` and the shared security checklist (N3) | Shelf | None | None |
| `debugging-and-error-recovery` | Addy, `skills/` | `301b02b` | MIT | Yes (N3) | Shelf | None | None |
| `frontend-ui-engineering` | Addy, `skills/` | `301b02b` | MIT | Yes, with the accessibility checklist (N3) | Shelf | None | None |
| `api-and-interface-design` | Addy, `skills/` | `301b02b` | MIT | Yes (N3) | Shelf | None | None |
| `observability-and-instrumentation` | Addy, `skills/` | `301b02b` | MIT | Yes, with the observability checklist (N3) | Shelf | None | None |
| `ask-matt` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes (N1) | Live, adapted as `ask-me` | None | None |
| `triage` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes (N1) | Live, adapted as `getai-intake` | None | None |
| `wizard` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes, with `template.sh` (N1) | Live, adapted as `getai-wizard` (`template.sh` unchanged) | None | None |
| `to-questionnaire` | Pocock, `skills/productivity/` | `4ae2317` | MIT | Yes (N1) | Live, adapted as `getai-questionnaire` | None | None |
| `grilling` | Pocock, `skills/productivity/` | `4ae2317` | MIT | Yes (N2) | Live, adapted as `getai-grilling` | None | None |
| `domain-modeling` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes, 4 files (N2) | Live, adapted as `getai-domain-modeling` (`adr-format.md` unchanged) | None | None |
| `diagnosing-bugs` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes, with the script (N3) | Shelf | None | None |
| `codebase-design` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes (N3) | Shelf | None | None |
| `improve-codebase-architecture` | Pocock, `skills/engineering/` | `4ae2317` | MIT | Yes (N3) | Shelf | None | None |
| `bro` | Tan, `pstack/skills/` | `ae5650f` | MIT | Not recorded until today; 7 lines, read (this) | Live, adopted unchanged on 1 November, before the policy | No shelf copy, no pin, no licence recorded. Its source was only in the commit message and the Session 1 log. No source line | Shelf copy at `skills/tan/bro/`; rows in `skills/README.md` and the register; line added |
| `blast-radius` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N1) | Live, adapted as `lcp-blast-radius` and `pcp-blast-radius` | None | None |
| `correct` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N1) | Live, adapted as `getai-correct` | None | None |
| `create-verification-skill` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes, 4 files (N1) | Live, adopted with two path edits | None | None |
| `how` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N1) | Live, adapted as `lcp-how` and `pcp-how` | None | None |
| `maintain-verification-skill` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N1) | Live, adopted with one path edit | None | None |
| `show-me-your-work` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes, with the script and template (N1, N3) | Live, adapted as `getai-decision-log` (script and template unchanged) | None | None |
| `why` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes, 13 files (N1) | Live, adapted as `lcp-why` and `pcp-why` | None | None |
| `unslop` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N2) | Live, adopted with rule 34 added | None | None |
| 13 principles: `attack-the-premise`, `boundary-discipline`, `exhaust-the-design-space`, `foundational-thinking`, `guard-the-context-window`, `laziness-protocol`, `make-operations-idempotent`, `minimize-reader-load`, `model-the-domain`, `prove-it-works`, `separate-before-serializing-shared-state`, `sequence-verifiable-units`, `subtract-before-you-add` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N2) | Live, adopted with a GET AI note | None | None |
| `principle-explain-the-number` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N2); its link to `benchmark-checklist` not read | Live, adopted with a GET AI note | Points at `benchmark-checklist`, not copied or adopted. The live note already says so | None needed while it stays a pointer |
| `principle-type-system-discipline` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N2); `typescript-best-practices` not read | Live, adopted with a GET AI note | Names `typescript-best-practices`, not copied or adopted. The live note already says so | None needed while it stays a pointer |
| 6 principles: `build-the-lever`, `encode-lessons-in-structure`, `experience-first`, `fix-root-causes`, `redesign-from-first-principles`, `test-behavior-not-implementation` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N2) | Live, adopted unchanged | No source line, though `skills/README.md` and N2 said every adopted principle had one | Line added (Boroon, 11 November); the two records are now true |
| 3 principles: `never-block-on-the-human`, `outcome-oriented-execution`, `migrate-callers-then-delete-legacy-apis` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes (N2) | Shelf, left there by Boroon | None | None |
| `poteto-mode` | Tan, `pstack/skills/` | `ae5650f` | MIT | **Partly** (N2): `watch-pr` code and tests (about 3,800 lines), and most of `check-plan.mjs` and `worktree-audit.sh`, not read line by line | Shelf; four habits lifted into `ask-me` | Not read in full. Allowed while it stays on the shelf | Read the rest in full before any adoption (rule 19) |
| `architect` | Tan, `pstack/skills/` | `ae5650f` | MIT | Yes, with 3 reference files (N3) | Shelf | Links to `arena`, dropped and not read | None while shelved |
| `triage-issue-reports` | Benny, `pstack/automations/benny/skills/` | `ae5650f` | MIT | Yes (N1) | Live, adapted and merged into `lcp-triage` and `pcp-triage` | None | None |
| `reproduce-and-fix-issues` | Benny, `pstack/automations/benny/skills/` | `ae5650f` | MIT | Yes (N1) | Live, adapted and merged into `lcp-triage` and `pcp-triage` | None | None |

Not in the table, because nothing was copied: `ci-cd-and-automation` and `shipping-and-launch` (Addy), and `arena` (Tan). They were dropped on 2 November without a full read by us, so each must be read in full if it is ever reconsidered (N3).

## Point 5: prefer our own adaptations

Of the 44 live skills, 16 are our adaptations and 28 are adopted: 4 unchanged apart from a source line (the 3 Addy skills and `bro`), 3 with small edits (the two verification skills and `unslop`), and 21 principles with a source line (15 with GET AI guidance too). Boroon chose to adopt these on 1 and 2 November 2026. The policy says "prefer", not "must", so this is a note, not a gap. The register review (point 6) is the place to adapt or drop any that do not earn their keep.

## Point 6: shrink skills as models improve (note)

No register review has run yet. The first is on Monday 23 November 2026, with the Ignite re-check. Things to look at then:
- the five principle fragments (N2 "Things to know before adopting", item 2);
- whether the adopted Addy skills still need their full length;
- skills and plugins installed on the claude.ai account, which load in day sessions but are pinned nowhere in this repo (`docs/component-register.md`, "Not in the register yet").

## Out of scope today

- **Microsoft's skill plugins** (`power-platform-skills`, `Dataverse-skills`): named by the policy, not copied or pinned yet. They get a register row when first pinned (A1, ADO 2740).
- **The delivery vault's four skills**: a GET AI engineer's own work, not third-party, and a read-only source copy that does not load.

## Decisions by Boroon (11 November 2026)

1. The register is a new file in this repo, `docs/component-register.md`, with one row per third-party source at a pin. A1 adds the kits to it later.
2. Each source's licence file is copied unchanged to the shelf. The live skills are covered by those files; no licence file goes in a live skill folder.
3. The 10 live skills with no source line get one, in the form the other 34 use.
