# Progress dashboard

The page: **Factory build progress**, https://claude.ai/artifact/DraME5jmLBvouXuH1Kvkk1. It's private and made from the claude.ai Dashboard type. Boroon asked for it on 9 November 2026, and it was built in Session 21.

## What it shows

- One line at the top: scheduled stories done out of all scheduled, the Stage 1 exit test date (ADO 2539) with the days left, and how many stories are past their finish date.
- A **Sync** button.
- Scheduled stories done against the plan, by day: planned by finish date, done by the day each was closed. It has a line for today and one for the exit test.
- Next up: the next six open scheduled stories.
- Past their finish date: open scheduled stories whose finish date has gone.
- Stories per stage: done, in progress and not started, for stages 0 to 9 and Planning.
- Time spent: active minutes per laptop session, with total hours and output tokens.
- Every scheduled story, with its state.

"Today" is the reader's date in Sydney, so the countdown and the late count move each day, even between syncs.

## Where the numbers come from

Claude.ai has no connector to this ADO project or to GitHub (checked 9 November 2026), so the page cannot query either one. The laptop makes a snapshot, and a Claude Code session uploads it.

- **Stories** (`stories.json`): `tools/progress_snapshot.py` reads every Epic, Feature and User Story of `getai-overnight-ai-factory` with `az boards query`, as Boroon's Azure CLI sign-in. It takes each story's stage from its Epic, and the Track from the table in `docs/plans/schedule.md`.
- **Sessions** (`sessions.json`): `tools/session_usage.py --json`, from the local transcripts. Cloud sessions have no local transcript, so they are not counted.

**The Sync button** reloads the newest snapshot uploaded to the page. It can't reach ADO itself, so a change made in ADO shows only after the next snapshot.

Since 11 November 2026, the page shows when the board was read, next to the button. That time comes from `snapshot_at` on every story row. After a click it says either "Newer snapshot loaded" or "No newer snapshot yet". Before then the button gave no sign of what it did, so a click with no new snapshot looked like it did nothing.

The page's Sources panel also shows each snapshot's age, and marks it stale after 72 hours.

## How to sync

Run these steps at the end of every laptop session (`CLAUDE.md`, end step 3), or whenever Boroon asks. Cloud sessions can't do it: they reach neither ADO nor the laptop's transcripts.

1. Run `python3 -I tools/progress_snapshot.py --out <scratchpad>/progress`. It needs the Azure CLI signed in (`az login`) with the `azure-devops` extension.
2. Upload each file to the page with the Artifact tool: `url` the page, `asset: true`, `file_path` the file, one call per file. Each reply gives a `/_blob/<id>` url.
3. With ArtifactData, `get` `datasets/stories` and `datasets/sessions`. Then `update` each one with `if_version`, setting:
   - `source.url` to the new url;
   - `updated` to `{at: <now, UTC>, by: "Claude, from tools/progress_snapshot.py on the laptop"}`;
   - `edit` to `{via: "claude", at: <now, UTC>}`.

   `source` has to be written whole, with its `kind`, `name` and `format` kept.
4. Keep the old file. Boroon stopped the deletes on 10 November 2026 and keeps the old snapshots until he reviews them. Before any delete later on, check that the page doesn't name the old id.

## The daily sync

A scheduled task in the Claude desktop app on the laptop, **"Factory build progress: daily sync"** (`factory-progress-sync`). It was set up on 10 November 2026, at Boroon's word.

- **When:** every day at about 7:30 Sydney time. It runs only while the app is open. If the app was closed at 7:30, it runs the next time the app opens.
- **What it does:** steps 1 to 3 above, and it deletes nothing (changed 11 November 2026). It runs the script from a temporary detached worktree of `origin/main` (or of `origin/claude/session-21-progress-dashboard` until that branch is merged). It never switches the shared folder's branch, and it never writes to the repo or to ADO. Its last line says what it synced, or which step didn't finish.
- **Where it lives:** its prompt is in `~/.claude/scheduled-tasks/factory-progress-sync/SKILL.md`. It's managed from Scheduled in the app's sidebar, where Run now starts a sync at once.
- **Approvals:** the upload to the page and the dataset update each ask for permission until an approval is saved on the task. The 11 November run stopped at that prompt (it was interrupted at 10:03), so the page kept the 10 November data. When a run asks, pick the option that remembers the approval. Later runs then go through on their own.
- **If it fails:** check the run's last line in Scheduled. A sign-in error means running `az login` on the laptop, then Run now. A refused tool means Run now and approving it.

## Not done

- **Live data.** If an Azure DevOps or GitHub connector is added on claude.ai later, the stories could come from a live query instead of a snapshot.
