# Staging

Drafts of the Stage 1 day-gate files (D1, Boroon, 7 November 2026). They are built here so cloud sessions can build them: cloud sessions cannot reach `getai.ghe.com`. Plan: `docs/plans/stage-1-day-gate-plan.md`.

## Where each part moves

On Friday 4 December 2026, one laptop session (DG8) moves everything here to `GetAI-IP` on `getai.ghe.com`. A pull request here then deletes `staging/` and leaves a pointer in `CLAUDE.md`.

| Folder | Moves to | How |
|---|---|---|
| `factory-manifestos/` | `GetAI-IP/factory-manifestos` (private, created 13 November 2026). This folder is its root | With its history (a subtree split), merged by pull request beside the coding standards from DG3. The repo's starter README is replaced by this folder's |
| `factory-gates/` (not created yet; DG5 and DG7) | `GetAI-IP/factory-gates`. This folder mirrors its root | By pull request there: `spec/`, its tests and fixtures, and `playwright/` |

## Rules

- Nothing here may name a client, a person or an engagement. This repo is public, and the staged files stay in its history after the move (accepted in D1).
- The low-code coding standards never come here. They are only on GHE, in `GetAI-IP/factory-manifestos` at `practices/lcp/coding-standards.md` (DG3, its pull request 1).
- Machine-read names stay product-neutral (rule 18).
- Python is standard library only, run with `python3 -I`, tested with `unittest`, as in `factory-gates`.
- The `glossary.md` and ADR templates are copies of the formats in `.claude/skills/getai-domain-modeling/`. When one changes, change both in the same pull request. After the move they sit in two repos, so DG8 settles how they stay the same.
