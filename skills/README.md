# skills/ (third-party skills, held for review)

This folder is a shelf, not a live install. Nothing here auto-loads. Claude Code only loads skills from `.claude/skills/`. Moving a skill there is the act of adopting it, and plan section 8.3 and rule 19 say that needs Boroon's approval after a full read and a pin.

All 16 skills in the first reading batch were copied unchanged on 2 November 2026 and read in full (every file, including scripts and references). Reading is done. Adoption is not approved for any of them yet.

## Where each came from (pinned)

| Folder | Skills | Source | Commit | Licence |
|---|---|---|---|---|
| `addy/` | `constraint-driven-development`, `doubt-driven-development`, `source-driven-development` | https://github.com/addyosmani/agent-skills, `skills/` | `301b02b12bff98e4688e6984af6556802322bbde` | MIT, Addy Osmani |
| `tan/` | `blast-radius`, `correct`, `create-verification-skill`, `how`, `maintain-verification-skill`, `show-me-your-work`, `why` | https://github.com/cursor/plugins, `pstack/skills/` | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT, Lauren Tan |
| `pocock/` | `ask-matt`, `to-questionnaire`, `triage`, `wizard` | https://github.com/mattpocock/skills, `skills/engineering/` and `skills/productivity/` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT, Matt Pocock |
| `benny/` | `reproduce-and-fix-issues`, `triage-issue-reports` | https://github.com/cursor/plugins, `pstack/automations/benny/skills/` | `ae5650febf4320793844c12c4adaa937f417f8da` | MIT, Lauren Tan |

Files are byte-for-byte copies of the upstream folders. Do not edit them here. A GET AI version is a new skill (named `lcp-*`) written in `.claude/skills/`, with a note of what it was adapted from.

What we think of each one is in `docs/analysis/skills-reading-notes.md`.
