# factory-manifestos (staged)

This folder becomes the root of `GetAI-IP/factory-manifestos`, a private repo on `getai.ghe.com`, on Friday 4 December 2026 (DG8). Until then it is drafted here, so cloud sessions can build it (D1, Boroon, 7 November 2026). Plan: `docs/plans/stage-1-day-gate-plan.md`.

The repo holds, per practice: a `coding-standards.md`, an `AGENTS.md` fragment, skills and a Spec Kit preset, versioned and vendored into project repos (plan 5.12). It also holds the templates every project repo takes.

## What is here

| Path | What it is | Built in |
|---|---|---|
| `templates/project/glossary.md` | The glossary format, with the `_Schema_` line for both profiles and one example term | DG1 (2545), done |
| `templates/project/docs/adr/README.md` | The decision record (ADR) format and the three tests for writing one | DG1 (2545), done |
| `templates/project/coding-standards.md` | The header only: who reads the file, "rule" and "judgement", how it changes | DG1 (2545), done |
| `spec-kit/` | The `getai` and `getai-lcp` presets, the `getai-spec-check` extension and the `getai-lcp` bundle | DG4 and DG5 (2544), not started |
| `conventions/` | `locked-scenarios.md` and `scenario.schema.json` | DG7 (2546), not started |
| `practices/lcp/coding-standards.md` | The low-code standards, 50 with their own IDs, anonymised. **On GHE only, never here** | DG3 (2545), done: pull request 1 in `GetAI-IP/factory-manifestos`, merged 13 November 2026 |

The coding standards themselves are not here. The low-code standards went straight to the GHE repo (DG3, 2545, 13 November 2026), never to this public repo.

## How a project repo takes the templates

- Each file under `templates/project/` is copied into the project repo at the same path: `glossary.md` and `coding-standards.md` at the root, `docs/adr/README.md` in `docs/adr/`.
- The copy is made by a reviewed daytime pull request. A night agent never adds or edits these files.
- All three paths are protected in the project repo: the `protected-paths` push ruleset and the gate's `locks` job cover `glossary.md`, `docs/adr/**` and `coding-standards.md` (plan 5.7 and Appendix B.1).
- When to copy each one:
  - `glossary.md` when the first term is resolved, usually in the first spec's clarify step. Files are created lazily, as `getai-domain-modeling` says.
  - `docs/adr/README.md` with the first decision record, `0001`. There is no `0000` example.
  - `coding-standards.md` when the project is set up, with its practice's standards below the header, because the reviewer reads it on every pull request.
- In the copy: delete the template notes (the HTML comments at the top), set the glossary's heading and description, and replace its example term with the first real one.

## Rules for this folder

- Nothing here may name a client, a person or an engagement. This repo is public, and the files stay in its history after the move (accepted in D1).
- Machine-read names stay product-neutral (rule 18).
- The glossary and ADR templates are copies of the formats in `.claude/skills/getai-domain-modeling/` (`glossary-format.md` and `adr-format.md`). When one changes, change both in the same pull request. That works only while both sit in the planning repo; after the move they are in two repos, and DG8 settles how they stay the same.
