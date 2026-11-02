---
name: getai-decision-log
description: Keep a reviewable decision trail for any long or unattended run: a TSV with one row per decision, kept in the evidence bundle. Use for night runs, multi-phase day work, or anything a human reviews after stepping away.
disable-model-invocation: true
---

# Decision log (GET AI)

Adapted from `show-me-your-work` by Lauren Tan (MIT, pinned at `cursor/plugins` commit `ae5650febf4320793844c12c4adaa937f417f8da`, original in `skills/tan/show-me-your-work/`). The helper script and the header row are copied unchanged. Changed: Cursor paths removed, the log is tied to `run_id` and the evidence bundle.

## The format

One TSV file, one row per decision. Cells stay on one line. Evidence is a pointer, not prose.

Columns: `ts` (ISO 8601), `phase`, `decision`, `why`, `evidence`, `result`.

- **decision**: what was chosen or done, one line.
- **why**: the reason in plain words.
- **evidence**: a commit SHA, PR number, file and line, or the path to an artifact, trace or screenshot. Never a paragraph.
- **result**: `tests green`, `reverted`, `PARKED`, `INCONCLUSIVE`, `open`.

Add a row with `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`. It stamps the time, writes the header on first use, strips tabs and newlines, and neutralises cells that start with `=`, `+`, `-` or `@` so a spreadsheet cannot run them.

## Where it lives

- Name it `decisions-<run_id>.tsv`. Every run has a `run_id` (rule 13).
- Put it in the evidence bundle. It reaches Blob within the night, tagged with the `run_id` (rule 16).
- Append only. A wrong call gets a new row that supersedes it. Never edit or delete history.

## What to log

Decision points, not every action: a fork chosen, a story step finished with its check, a pivot or revert with the trigger, a PARK with its type (`portal_step`, `design_approval`, `ambiguity`, `one_way_door`, `budget`), a blocker, a gate that was fixed. One row per iteration in a loop. Skip the trivial.

A new run, new chat or replacement agent starts with a row whose phase is `start`. Use `start` for nothing else.

## Audit before you hand back

Walk the log against the run's transcript (the path is in the evidence bundle). Check:

- every row maps to a real decision or action;
- every evidence pointer resolves and shows what the row claims;
- a fork or abandoned approach that shaped the work but is missing is a gap, so add a row.

Correct the log, not the story. Never remove a row, even a wrong one. Add a row that supersedes it.

## Second look by a different model

Before handing back, have a fresh session on a **different model family** read the log and transcript and flag what a casual skim would miss: weak evidence, claims without proof, risky choices, scope creep. Only do this if the client's residency tier allows that model (plan section 9.4). If it does not, write "second look skipped: residency tier" in the reply.

End the reply with an **Attention** section. First line: `reviewed by <model>`. Then each flag with the row or moment it points at. "No flags" is a valid answer.

## Reading it

Top to bottom, follow the evidence, spot-check. `column -s$'\t' -t decisions-<run_id>.tsv` shows it as a table in a terminal.
