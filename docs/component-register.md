# Component register: third-party sources

Made 11 November 2026 (Session 21, ADO 2549), at Boroon's word. Plan 8.3 point 4 says to record each third-party skill's source and licence in the component register (plan 8.2). Until now the register was only the class table in the plan. This file holds the rows.

- **What goes here:** one row per third-party source we copy or pin, at its pin. Today that is the three skill sources. A1 (ADO 2740, keep pinned kits current) adds the kits as rows: Spec Kit, pac, Copilot CLI, Playwright, axe-core, Microsoft's Playwright samples, Microsoft's skill plugins and the actions. One file serves both plan 8.3 and A1.
- **What does not:** the class of each part of the factory (shipped primitive, thin glue, IP) stays in plan 8.2's table. The detail of each skill (what it became, where its notes are) stays in `skills/README.md`. Nothing here may name a client, a person or an engagement (public repo).
- **Review:** monthly, with the plan 8.2 review, and after each Microsoft or GitHub event. The first pass is on Monday 23 November 2026, with the Ignite re-check (`docs/plans/schedule.md`). At each pass: check each source for changes since its pin, and update "Last checked".

## Rows

| Source | What we take | Pin | Licence | Copied to | Read in full | Watched by | Last checked |
|---|---|---|---|---|---|---|---|
| [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills), folders `skills/` and `references/` | 10 skills and 4 shared reference files. Live: 3, adopted unchanged with a source line (`constraint-driven-development`, `doubt-driven-development`, `source-driven-development`). Shelf only: 7. Not copied: `ci-cd-and-automation`, `shipping-and-launch` (dropped, not read) | commit `301b02b12bff98e4688e6984af6556802322bbde` (1 November 2026, UTC) | MIT, Copyright (c) 2025 Addy Osmani. Text at `skills/addy/LICENSE` | `skills/addy/`, `skills/references/`, and the 3 live skills in `.claude/skills/` | Yes, every file: `docs/analysis/skills-reading-notes.md` (3), `skills-reading-notes-skill-batches.md` (7 and 3 references), `docs/analysis/skills-policy-check.md` (`orchestration-patterns.md`) | Manual pass at the monthly review. Dependabot cannot watch copied files | 11 November 2026: upstream head is still the pin |
| [`mattpocock/skills`](https://github.com/mattpocock/skills), folders `skills/engineering/` and `skills/productivity/` | 9 skills. Live: 6, all adapted (`ask-me`, `getai-intake`, `getai-wizard`, `getai-questionnaire`, `getai-grilling`, `getai-domain-modeling`). Shelf only: 3 | commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` (31 October 2026, UTC) | MIT, Copyright (c) 2026 Matt Pocock. Text at `skills/pocock/LICENSE` | `skills/pocock/`, and the 6 live skills built from them in `.claude/skills/` | Yes, every file: `skills-reading-notes.md` (4), `skills-reading-notes-batch2.md` (2), `skills-reading-notes-skill-batches.md` (3) | Manual pass at the monthly review | 11 November 2026: upstream head is still the pin |
| [`cursor/plugins`](https://github.com/cursor/plugins), folders `pstack/skills/` and `pstack/automations/benny/skills/` (Lauren Tan's pstack) | 37 skills: 35 from `pstack/skills/`, 2 Benny skills. Live: 25 adopted (`bro`, `unslop`, the two verification skills, 21 principles), each with a source line, and 10 adaptations (`getai-correct`, `getai-decision-log`, `lcp-` and `pcp-` `blast-radius`, `how`, `why`, `triage`). `ask-me` also lifts four habits from `poteto-mode`. Shelf only: 5 (`poteto-mode`, `architect`, 3 principles). Not copied: `arena` (dropped, not read) | commit `ae5650febf4320793844c12c4adaa937f417f8da` (1 November 2026, UTC) | MIT, Copyright (c) 2026 Lauren Tan (`pstack/LICENSE`, which covers the Benny skills too). Text at `skills/tan/LICENSE` and `skills/benny/LICENSE` | `skills/tan/`, `skills/benny/`, and the 35 live skills built from them in `.claude/skills/` | Yes, except `poteto-mode` (shelf only): its `watch-pr` code and two scripts were not read line by line. Records: `skills-reading-notes.md`, `skills-reading-notes-batch2.md`, `skills-reading-notes-skill-batches.md`, and `skills-policy-check.md` (`bro`) | Manual pass at the monthly review | 11 November 2026: upstream head is `63912a9`, with no change under `pstack/` since the pin |

## How to check a source for changes

From any folder outside the repo:

```bash
git clone --filter=blob:none --no-checkout https://github.com/cursor/plugins.git
```

```bash
git -C plugins diff --stat ae5650febf4320793844c12c4adaa937f417f8da origin/HEAD -- pstack/skills pstack/automations/benny/skills pstack/LICENSE
```

Use the source's own pin and folders for the other two. If a folder we copy has changed, the update follows plan 8.3: read the diff in full, then move the pin by a reviewed pull request that updates the shelf copies, every live skill built from them, this row and `skills/README.md` together (rule 17).

## Not in the register yet

- **Microsoft's skill plugins** (`power-platform-skills`, `Dataverse-skills`). The policy covers them, but nothing is copied or pinned yet. They get a row when first pinned (A1).
- **The delivery vault's four skills** (`docs/sources/delivery-vault/.github/skills/`). A GET AI engineer's own work, not third-party. A read-only source copy that does not load.
- **Skills and plugins installed on the claude.ai account,** outside the repo. They load in day sessions, and nothing in this repo pins them. For the first review to decide whether they belong here.
