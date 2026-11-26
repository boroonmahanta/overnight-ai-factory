# Spike 0.17: session export for mining

Plan section 11.1, row 0.17 (ADO 2466), and DG2 of `docs/plans/stage-1-day-gate-plan.md`. Session 31, 21 November 2026, on the laptop, apps only, no tenant. A day after its Friday 20 November date. Part of the Copilot app check ran in a side session Boroon opened the same day.

**Result: the exit test passes for all four tools.** Each tool gave a readable transcript of a test session with no client data. Copilot CLI's `--share` writes the fullest export. It also covers the GitHub Copilot app and VS Code's Copilot Chat, because all three keep their sessions in one shared store on disk (`~/.copilot/session-state/`). Claude Code's `/export` writes plain text, but only in a live terminal session. The how-to for engineers and the checklist for removing client data are below. A cloud session can read the exports folder through the Microsoft 365 connector, so mining batches can run in the cloud ("Where exports go").

Exit test (plan 11.1): export a VS Code and a Copilot app chat session by hand; pass if the transcript is readable and holds no client data. If it fails, engineers write short correction notes instead. DG2 widened it to every tool an engineer uses: VS Code Copilot Chat, the Copilot app, Copilot CLI and Claude Code.

## What was tested

Every test used a fresh session in a scratch folder with the same prompt: "Create a file hello.py that prints 'hello from the export test', then run it with python3 and tell me the output in one line." So each session has a prompt, a file edit, a shell command with output, and an answer, and no client data. Raw exports stayed in the session scratchpad and are not in this repo.

| Tool | Version on the laptop | Export tried | Readable? | What it holds |
|---|---|---|---|---|
| Copilot CLI | 1.0.113 (spike 0.14's pin, installed in the scratchpad only, `npm ci --ignore-scripts`) | `copilot -p ... --share <file>` | Yes, Markdown | Prompt, each tool call, the file edit as a patch, shell commands with output, a refused call, the answer, the model chosen |
| GitHub Copilot app | 1.2.0 (bundles the Copilot CLI runtime 1.0.106-8) | No export in the app. Copilot CLI on a copy of the session | Yes, Markdown | The same as the CLI |
| VS Code Copilot Chat | 1.138.0 (chat ran on the Copilot CLI engine, model id `agent-host-copilotcli:auto`) | "Chat: Export Chat...", right-click "Copy All", and Copilot CLI on a copy of the session | Copy All and the CLI export, yes. Export Chat is JSON | Copy All: prompt, tool names, the command line, answer, but no command output or file content. Export Chat: everything, including command output, but as JSON. The CLI export: the same as the CLI |
| Claude Code | CLI 2.1.217 (Homebrew); desktop app 6.28899.2 | `/export <name>` in a live session; `/export` headless; the desktop app's Export | `/export` in a live session, yes, plain text | Prompt, file writes with content, the answer. Shell commands show only as "Ran 2 shell commands". The opening box shows the account email and organisation |

## Findings

1. **One store for three Copilot tools.** The Copilot app, Copilot CLI and VS Code's chat (when it runs on the Copilot CLI engine) each keep a session as `~/.copilot/session-state/<id>/events.jsonl`. The session's `workspace.yaml` names the tool in `client_name`: `github/cli` for the CLI, `github/autopilot` for the app, `vscode-agent-host` for VS Code. So Copilot CLI can export a session made in any of them.
2. **Copilot CLI's export is the fullest.** `--share <file>` in non-interactive mode writes Markdown after the run: a header with the session ID, start, duration and export time, then each turn in order, with tool arguments, results and shell output in code blocks. A past session is exported by resuming it with one small prompt: `--resume <id> -p "Reply with the single word OK." --share <file>`. The added turn goes into the export too.
3. **Export a copy, never the original.** Resuming adds a turn to the session, and a session open in another Copilot process is refused ("Session ... is in use by another Copilot process", seen with VS Code's window open). Copying the session folder into a throwaway Copilot home folder (`COPILOT_HOME`) and resuming it there solves both. The original stayed unchanged (22 events before and after), and the sign-in still worked from the system keychain.
4. **Pin the model and deny tools on the export turn.** Resumed with the session's own model, the app session's export turn failed: "Model "claude-sonnet-5.5" is not available". Copilot CLI still wrote the export and exited 1. With `--model auto` the turn answered "OK" and exited 0. `--deny-tool shell --deny-tool write` keeps that turn from running commands or changing files.
5. **The export turn costs little.** The CLI's closing "AI Credits" line is the session's running total, not the export's. The app session showed 15.97, then 16.05 after one more export turn, so that turn cost 0.08 AI credits (USD 0.0008 at the CLI's 1 credit = USD 0.01, spike 0.14). The fresh CLI test session cost 0.29 in all.
6. **The Copilot app has no file export.** Its right-click menu on a session offers Rename, Pin, Mark as unread, Show in Finder, Share as secret gist, Copy (the session ID only), Open in..., Create nested session, Archive and Delete (Boroon's side session). "Share as secret gist" uploads the session to GitHub, so it must never be used for a real session. "Copy" gives the session ID the CLI route needs. GitHub's docs have no page for the app.
7. **Copilot exports start with a warning line.** "Remote sessions are not enabled. Contact your organization administrator to enable remote sessions." It is harmless.
8. **VS Code's own export is complete but not readable.** "Chat: Export Chat..." saves JSON with each request's prompt, tool calls, command lines, command output (`terminalCommandOutput`), model and timings. "Copy All" gives short readable text but drops command output and file contents. Older VS Code sessions that did not run on the Copilot CLI engine are only in VS Code's own store, so only these two commands reach them.
9. **Claude Code's `/export` works only in a live terminal session.** Headless (`claude -p`, with or without the desktop app's environment) it answers "/export isn't available in this environment". Typed in a terminal session, `/export <name>` wrote the file into the current folder. It writes what the terminal shows, wrapped at the terminal's width: the opening box (with the account email, plan and organisation), each prompt, file writes with their content, and the answers. Shell commands are folded to a count ("Ran 2 shell commands (ctrl+o to expand)"). Resuming a session to export it adds no paid turn, but the `/export` line itself is recorded in the session.
10. **The desktop app's Export is the raw files.** In the Claude desktop app, Export writes a zip to Downloads: the session's JSONL transcript (twice, once as `transcript.jsonl`), the subagent transcripts and metadata. Complete, but not readable without a converter. For Boroon's own sessions (D5's top-up), mining can read the JSONL on the laptop directly; `tools/session_usage.py` already reads it.
11. **Every export shows full file paths.** Copilot exports name the absolute path of each file touched; Claude Code's opening box shows the folder. Folder and repo names can carry a client's name, so the checklist covers paths.
12. **Not tested:** Copilot CLI's interactive `/share file` (documented by GitHub; it would not run under a scripted terminal, `expect`); Windows (every test ran on macOS); the Claude Code VS Code extension (it keeps sessions in the same `~/.claude/projects/` store as the CLI, so `claude --resume` in a terminal should reach them, but this was not tried); Claude Code's `/export` after expanding the folded commands with ctrl+o.

## How-to for engineers

This is what goes to the engineers (DG3's checkpoint). It assumes macOS. Windows notes are at the end of each section, untested.

### Which sessions to send

- Day-time delivery sessions where you led an AI agent, from the last few weeks. Some that went wrong and some that looked fine (plan 7.3, step 3).
- Two to five sessions each. One session per file.
- Mining looks for where you corrected the agent, so a session with a few corrections in it is the most useful.

### Copilot CLI, the GitHub Copilot app, and VS Code Copilot Chat

These three keep sessions in one place, and Copilot CLI exports any of them. You need Copilot CLI installed (`npm install --global @github/copilot`) and signed in once (`copilot login`). The export works on a copy, so your real session never changes, and it adds one small turn that costs well under one AI credit.

1. Find the session ID.
   - **Copilot app:** right-click the session, then Copy, then Session ID.
   - **Copilot CLI:** the last lines of a run show `copilot --resume=<id>`; in a running session, `/session info` shows it.
   - **VS Code:** this lists the VS Code sessions Copilot CLI can reach, with their first prompt:

     ```bash
     grep -l 'client_name: vscode-agent-host' ~/.copilot/session-state/*/workspace.yaml | xargs grep -H '^name:'
     ```

     The ID is the folder name in each line. If your session is not listed, use "VS Code's own commands" below.
2. Copy the session into a throwaway Copilot home folder (put your ID in place of `<id>`):

   ```bash
   mkdir -p ~/copilot-export/session-state && rsync -a --exclude 'inuse.*' --exclude '*.lock' --exclude '*.hold' ~/.copilot/session-state/<id> ~/copilot-export/session-state/
   ```

3. From the folder you worked in, export the copy:

   ```bash
   COPILOT_HOME=~/copilot-export copilot --resume <id> --model auto --deny-tool shell --deny-tool write -p "Reply with the single word OK." --share ~/copilot-export/<id>.md
   ```

   It prints `Session exported to: ...`. The last turn in the file, "Reply with the single word OK.", is from this step; leave it in. An error line such as `Model "..." is not available` can appear for a turn that failed before; the export is still complete.
4. Clean the file (checklist below), rename it, and send it.
5. Delete the copy: `rm -rf ~/copilot-export`.

Never use "Share as secret gist" in the app, or `/share gist`, `/share link` or `--share-gist` in the CLI: they upload the session to GitHub.

Windows (untested): the store is `%USERPROFILE%\.copilot\session-state`. In PowerShell, copy with `robocopy "$env:USERPROFILE\.copilot\session-state\<id>" "$env:USERPROFILE\copilot-export\session-state\<id>" /E /XF inuse.* *.lock *.hold`, then set `$env:COPILOT_HOME="$env:USERPROFILE\copilot-export"` and run step 3 without the `COPILOT_HOME=~/copilot-export` part.

### VS Code's own commands

For a VS Code session the list above does not show:

1. Open the session in the Chat view (sessions list, or change the filter to Archived to find a closed one).
2. Right-click in the chat, choose **Copy All**, paste into a new text file and save it as Markdown (`.md`). This is the readable copy.
3. If you are asked for more detail, also run **Chat: Export Chat...** from the Command Palette (⇧⌘P) and save the JSON file. It holds command output too, so it needs more cleaning.

### Claude Code (terminal, VS Code extension, desktop app)

1. In a terminal, go to the folder you worked in and run `claude --resume`. Pick the session from the list.
2. Type `/export <name>.txt` with a plain file name, not a full path, and press Enter. It says "Conversation exported to:" and the path, in the current folder.
3. Type `/exit`.
4. Delete the opening box at the top of the file (it shows your email and organisation), then clean the rest with the checklist.

`/export` does not work in `claude -p`. The desktop app's Export gives a zip of raw files; do not send that.

### If you cannot clean a session

Write a short correction note instead (the plan's fallback). One note per session:

```
Tool and date:
What I asked the agent to do (one line, no client names):
Each place I corrected it: what it did, what I told it, why:
What would have saved the correction (a standard, a check, a glossary term, information it lacked):
```

### Remove client data before you send

Go through the whole file. Replace, do not just delete, so the shape stays: `<client>`, `<person-1>`, `<env-url>`, `<id>`, `<value>`.

- [ ] Client, project, engagement and people's names: in prompts, answers, file and folder paths, repo and branch names, ADO project names, solution, table and publisher names and prefixes.
- [ ] Tenant and environment addresses: `*.dynamics.com`, `*.sharepoint.com`, `*.ghe.com` org names, tenant IDs, app and client IDs.
- [ ] Record values: rows, names, emails, phone numbers and IDs in query results, Web API answers and flow run output.
- [ ] Secrets: tokens, keys, passwords, connection strings. If you find a real one, do not send the file; tell Boroon, because the secret must be changed.
- [ ] Screenshots and images: remove them and any links to them.
- [ ] Your own details: the Claude Code opening box, and your user name in paths if you prefer.
- [ ] Read it once more from top to bottom.

If a session is too full of client detail to clean, send a correction note instead.

### Name and send

- File name: `<tool>-<yyyymmdd>-<n>.md`, for example `copilot-cli-20261124-1.md` or `claude-code-20261124-2.txt`. No client, engagement or person names in the file name.
- Upload it through the "Request files" link Boroon sends you. You cannot see the folder or other people's files.
- Never put a raw or cleaned export in a repo, a Teams chat or an email.
- If you want to keep the raw export, put it in that engagement's own channel folder in Teams (GET AI only), not in Downloads, and never in a channel shared with the client. If it holds a secret, delete it instead.

### A message Boroon can send (draft)

> We're starting to learn from real AI-assisted delivery sessions, to find where agents needed correcting and turn the repeats into standards, checks and skills. Could you send two to five of your recent sessions by Friday 4 December? The how-to is attached: one command per session for Copilot (app, CLI or VS Code) and `/export` for Claude Code, then a checklist to remove client data. Upload through this link: <Request files link>. If a session can't be cleaned, a four-line correction note is just as useful.

## Where exports go

- **Folder:** `Factory session exports` in Boroon's OneDrive (made 21 November 2026 through the Mac's OneDrive sync folder). Private to Boroon: a new OneDrive folder is shared with no one.
- **How engineers send:** a "Request files" link on that folder, which Boroon makes in OneDrive in the browser (folder menu, Request files). Senders can upload but cannot open the folder or see other files. Request files shows in the folder's command bar (checked 21 November 2026, Session 32), so it works here with no admin change. **The link is not made yet.**
- **The Microsoft 365 connector is read only.** It has `Files.Read.All` and `Sites.Read.All` and no write scope, so it could not make the folder (`FORBIDDEN: Missing scope 'Files.ReadWrite.All'`). Granting write consent is a tenant security change and is not needed: mining only reads. The laptop session read the test file through the connector.
- **Cloud read check: a cloud session can read the folder** (21 November 2026, at Boroon's word). A cloud session, asked only to read, had the same Microsoft 365 connector as the laptop and read the test file `spike-0.17-cloud-read-test.md` by its path, token and all. So mining batches (2548, DG6) can run in a cloud session.
- **List the folder by its ID, not its path.** The cloud session's listing by path failed (`INTERNAL_ERROR: Failed to fetch OneDrive metadata caused by: Invalid request`, Graph 400): the connector reads a folder path's last part as an item ID, with or without a trailing slash. From the laptop, `sharepoint_folder_search` for "Factory session exports" gives the folder's item ID, and reading `file:///<driveId>/<itemId>` lists it. A file reads by path. The cloud session has the same search tool; the listing by ID was tried on the laptop only.
- **Its lasting home** (Boroon, 21 November 2026; plan 7.3): a private channel for session exports in an internal Factory Team. It outlives any one account, only its members can read it, and the "Request files" link works there too if "Anyone" links are allowed on that one site. A private channel is its own SharePoint site, so the vault's operating model treats it as an access exception that needs admin review. The OneDrive folder is the stopgap until then. Moving gives the folder a new drive ID and item ID, so the connector read check runs again after the move (ADO 3019, which also holds the "Anyone" links check below). Boroon kept "Request files" for it, renewed quarterly (Session 32): see "The Factory Team's home" below.
- **Raw exports.** An engineer who wants to keep a raw, uncleaned export keeps it in that engagement's own channel folder, which is GET AI only, not in Downloads, and never in a channel shared with the client. Ordinary internal folders are readable across GET AI (vault operating model), so an export that holds a secret is deleted, not kept. Only the cleaned copy goes to the factory folder.
- **Keeping:** proposed, for Boroon to decide: delete each batch's files once its findings are in `docs/analysis/session-mining.md`, and all of them when DG6 closes (Friday 11 December).

## The Factory Team's home (ADO 3019)

Session 32, 21 November 2026. Boroon kept "Request files" for the private channel, **renewed quarterly**: the link expires after 90 days, and he makes a new one each quarter and sends it to the engineers. Three SharePoint and Teams admins, named in ADO 3019, review the private channel and make the settings.

What was checked:

- **OneDrive passes.** "Request files" shows in the OneDrive command bar when `Factory session exports` is selected (in the built-in browser, under Boroon's sign-in; the link was not made). So the tenant allows "Anyone" links for OneDrive, and the stopgap needs no admin change. OneDrive's own switch is `OneDriveRequestFilesLinkEnabled`; `CoreRequestFilesLinkEnabled` is SharePoint's, which the channel needs.
- **The folder is empty.** Session 31 deleted its test file with the rest of the scratch (below); the web view, the connector's listing by ID and the Mac's sync folder all show no files. Nothing needs moving yet.
- **A channel's site and its Team's site** (Microsoft's pages, untested). "Private channels in Microsoft Teams" says a private channel's site inherits guest access from its parent Team's site and cannot be shared separately. "Change the sharing settings for a site" shows an admin picking a channel site from the Channel sites column to set its sharing. They may not agree, so the admins try the channel's site alone first.
- **Microsoft advises against "Anyone" links** ("Secure external access to Microsoft Teams, SharePoint, and OneDrive"), and says to set an expiry if they are used. The quarterly renewal is that expiry. The link only uploads: whoever holds it cannot open, list or download anything.

Steps:

1. **Boroon:** create the internal Factory Team (private, GET AI only) and a private channel for session exports. Channel members: Boroon and the mining reviewers. Make a folder in the channel's Files, since new private channels have none. **Done on 21 November 2026:** the Factory Team and a private channel, "Cleaned AI Factory Sessions Exports", which the connector shows as private (IDs in ADO 3019). The Team's standard channel is General, and its folder in the Team's own library is readable by every Team member, so no export goes there. The channel's own site exists (a Teams channel site, from the URL Boroon gave). The connector lists its document library from the laptop by the site's Graph ID (host name, site ID and web ID, read from the page in the browser; all in ADO 3019), but not by the site's path (404, twice). The exports folder is `Uploads`, which Boroon made in the channel's Files; the connector lists it by its item ID from the laptop (empty, no error; the ID is in ADO 3019). That is the laptop half of the read check in step 4; a cloud session still has to list it by the same ID. The channel's members are not checked: the connector cannot list them.
2. **The admins:**
   - review the private channel as an access exception (delivery vault operating model);
   - tenant: `CoreRequestFilesLinkEnabled` true (`Get-SPOTenant`, then `Set-SPOTenant -CoreRequestFilesLinkEnabled $true` if needed); "Anyone" links for folders allow "View, edit, and upload" or "View and upload"; note any tenant expiry on "Anyone" links;
   - the channel's site (SharePoint admin center, Active sites, the Factory Team, the Channel sites column, the channel's site, Settings, More sharing settings): external sharing "Anyone". If it will not hold, the Factory Team's own site too. The default link type stays "People in your organization" on both, so nobody makes "Anyone" links by default;
   - `Set-SPOSite -Identity <channel site URL> -RequestFilesLinkEnabled $true -RequestFilesLinkExpirationInDays 90`.
3. **Boroon:** make the "Request files" link on the channel's folder, send it to the engineers, and set a quarterly reminder to make the next one.
4. Move anything in `Factory session exports`, record the new site, drive and folder IDs, run the connector read check again (laptop and cloud, by ID), and update this README and the message to the engineers.

A message Boroon can send the admins (draft):

> I'm setting up a restricted place for the factory's session exports: a private channel in a new internal Factory Team, readable only by its members. Engineers will upload through a "Request files" link (upload only; they can't see the folder). Could you please: (1) review the private channel as an access exception; (2) confirm `CoreRequestFilesLinkEnabled` is true for the tenant; (3) set the channel's site to allow "Anyone" links (and the Team's site too, if the channel's site won't take it alone), keeping the default link type to people in GET AI; (4) set its Request files links to expire after 90 days (`Set-SPOSite -RequestFilesLinkEnabled $true -RequestFilesLinkExpirationInDays 90`). I'll renew the link each quarter.

## What can fail

1. **"Request files" may be off in GET AI's tenant.** Checked for OneDrive in Session 32: it shows, so the stopgap works. Still to check for the channel's site (ADO 3019). Microsoft's page "Enable file requests in SharePoint or OneDrive" says it works only if "Anyone" links are allowed for the organisation and on the folder, and "Allow only specific security groups" is off. Whoever holds the link can then upload without signing in. Check that the folder's menu in the browser shows Request files. If it does not: one subfolder per engineer, shared with that engineer alone, or the tenant admin's call.
2. **Finding the folder by search.** The folder search matches part of a name across every site Boroon can read. With one Team per client it can return several folders, and a new folder takes a while to appear. Pick the result by its drive ID, then work by item ID; the vault's rule is the same ("Record actual provisioned URLs/IDs; never derive resource addresses from display names").
3. **Long exports come in pages.** The read tool returns about 200,000 characters a call and ends a longer file with a "re-call with startPage" note. A mining session must follow it, or it reads only part of the session.
4. **The connector reads as Boroon.** If his sign-in lapses or the tenant changes the connector's consent, reads fail on the laptop and in the cloud alike.
5. **Uploaders' names in file names** (unverified). The upload page may ask for the sender's name and add it to the file name. Check the first upload; mining records only codes such as `S07`.
6. **Client names in paths.** With one channel per engagement, a synced channel folder puts the client's name in every path an export shows. Cleaning paths is a step on nearly every export.
7. **Tested once:** one small file, one cloud session. Not tried: listing by ID in the cloud, many files, large files, VS Code's JSON.

## What this means for the plan and for 2548

- The exit test passes, so the fallback is not needed as the main route; correction notes stay for sessions that cannot be cleaned.
- Mining (DG6) reads Markdown and plain text, plus the raw JSONL of Boroon's own Claude Code sessions on the laptop (D5). Engineers' exports can be mined in a cloud session, which reads the folder through the connector; Boroon's own JSONL can be mined only on the laptop.
- The checkpoint (send the how-to and ask for exports) is due now: it was set for Friday 20 November.
- Possible plan edit, for Boroon to decide: in 11.1, row 0.17, record the result (passes for all four tools; Copilot CLI's `--share` exports Copilot app, CLI and VS Code sessions; Claude Code's `/export` in a live session) and point to this file.

## Scratch (deleted 21 November 2026, at Boroon's word)

All of it was deleted on 21 November 2026, at Boroon's word, after he merged pull request 41. The Copilot app session went through the app's own Delete. The VS Code session's folder went to the Mac's Trash once its window was closed: a leftover lock file remained, but no process had it open. The other sessions also went to the Trash, the OneDrive test file to OneDrive's recycle bin, and the scratchpad was removed. The `Factory session exports` folder stays, empty, for the engineers. What there was:

| What | Where |
|---|---|
| Copilot CLI 1.0.113, the copies of sessions, the raw exports and the run logs | The session scratchpad (`s017/`); goes with the scratchpad |
| Four Copilot test sessions: `792105df` (CLI), `f1ad0a3c` (app), `23fe9fee` (VS Code), `44ee8e7e` (empty, opened by `copilot app`) | `~/.copilot/session-state/`; the app and VS Code list theirs. Delete in the app (right-click, Delete) or remove the folders |
| One Claude Code test session, `17e559b6` | `~/.claude/projects/`, under the scratchpad's path |
| The VS Code window on the scratch folder `vsc-test` | VS Code |
| The test file `spike-0.17-cloud-read-test.md` (keep the folder) | `Factory session exports` in Boroon's OneDrive |
