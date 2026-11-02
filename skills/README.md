# skills/ (third-party skills, held for review)

This folder is a shelf, not a live install. Nothing here auto-loads. Claude Code only loads skills from `.claude/skills/`. Moving a skill there is the act of adopting it, and plan section 8.3 and rule 19 say that needs Boroon's approval after a full read and a pin.

All 16 skills in the first reading batch were copied unchanged on 2 November 2026 and read in full (every file, including scripts and references). Reading is done.

## Where each came from (pinned)

| Folder | Skills | Source | Commit | Licence |
|---|---|---|---|---|
| `addy/` | `constraint-driven-development`, `doubt-driven-development`, `source-driven-development` | https://github.com/addyosmani/agent-skills, `skills/` | `301b02b12bff98e4688e6984af6556802322bbde` | MIT, Addy Osmani |
| `tan/` | `blast-radius`, `correct`, `create-verification-skill`, `how`, `maintain-verification-skill`, `show-me-your-work`, `why` | https://github.com/cursor/plugins, `pstack/skills/` | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT, Lauren Tan |
| `pocock/` | `ask-matt`, `to-questionnaire`, `triage`, `wizard` | https://github.com/mattpocock/skills, `skills/engineering/` and `skills/productivity/` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT, Matt Pocock |
| `benny/` | `reproduce-and-fix-issues`, `triage-issue-reports` | https://github.com/cursor/plugins, `pstack/automations/benny/skills/` | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT, Lauren Tan |

Files are byte-for-byte copies of the upstream folders. Do not edit them here. A GET AI version is a new skill written in `.claude/skills/`: `getai-*` if it works for any profile, `lcp-*` for Power Platform, `pcp-*` for pro-code, with a note of what it was adapted from.

What we think of each one is in `docs/analysis/skills-reading-notes.md`.

## What happened to each (2 November 2026, Boroon's decision)

Boroon said: adopt the first five, adapt the rest. The shelf copies here stay as the pinned originals. Live versions are in `.claude/skills/`.

| Original | Result | Live skill |
|---|---|---|
| `addy/constraint-driven-development` | Adopted unchanged | `constraint-driven-development` |
| `addy/doubt-driven-development` | Adopted unchanged | `doubt-driven-development` |
| `addy/source-driven-development` | Adopted unchanged | `source-driven-development` |
| `tan/create-verification-skill` | Adopted unchanged. Writes to `.cursor/skills/`, so tell it to use `.claude/skills/` and the name `lcp-verify` | `create-verification-skill` |
| `tan/maintain-verification-skill` | Adopted unchanged. Same path note | `maintain-verification-skill` |
| `tan/blast-radius` | Adapted | `lcp-blast-radius` |
| `tan/show-me-your-work` | Adapted (script and header copied unchanged) | `getai-decision-log` |
| `tan/correct` | Adapted | `getai-correct` |
| `tan/how` | Adapted | `lcp-how` |
| `tan/why` | Adapted | `lcp-why` |
| `pocock/triage` | Adapted | `getai-intake` |
| `pocock/wizard` | Adapted (`template.sh` copied unchanged) | `getai-wizard` |
| `pocock/to-questionnaire` | Adapted | `getai-questionnaire` |
| `pocock/ask-matt` | Adapted | `ask-me` |
| `benny/triage-issue-reports` and `benny/reproduce-and-fix-issues` | Adapted and merged. Fixing and PRs removed | `lcp-triage` |
| `tan/blast-radius`, `tan/how`, `tan/why`, and the two Benny skills again | Second adaptation for the pro-code profile | `pcp-blast-radius`, `pcp-how`, `pcp-why`, `pcp-triage` |

Every adapted skill names its source and pinned commit in its first lines. Adapted skills have not been tested.
