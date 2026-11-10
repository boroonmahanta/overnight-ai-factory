# Spike 0.19: reset fidelity

Plan section 11.1, row 0.19 (ADO 2463). Session 20, 9 and 10 November 2026 (Sydney time). The result is in `docs/progress.md` (Session 20).

**Result: pass** (run 37559661, 10 November 2026). On a runner, signed in as `getai-fl1-exec` with no secret, a probe-only stand-in for `reset_environment.py` ran plan 5.4's reset steps 2 to 5 on a lane left dirty by an earlier run:

- it imported the reset commit with overwrite and publish;
- it set the lane's environment variable value;
- it found three leftovers by query alone and deleted them: a flow and a column inside the solution, and a flow outside it;
- a fresh export, unpacked, then equalled the reset commit **byte for byte**, all 23 files, not only in canonical form.

The import also undid a change to the main flow's definition. The way to find what the lane identity made outside the solution is not the one Microsoft's table reference suggests (finding 3). Findings below.

Exit test (plan 11.1): in `factory-lane-1`, plant a leftover component in the lane's solution and one outside it, run `reset_environment.py` to the head of `integration`, then export. Pass if both leftovers are removed and the export equals `integration` exactly (canonical compare). Boroon added a third mess, a change to a component the reset commit holds, and chose (9 November 2026) to plant two leftovers inside the solution, a flow and a column, in the same run.

**Run alone, not with 0.10.** The 0.19 row says "run with 0.10", but 0.10 needs `factory-test` (2541, 8 December). This spike ran in `factory-lane-1` only. Nothing here depends on the Test environment.

**One pac version, 2.14.1.** Spike 0.18 found 2.14.1 and the gate's pin 2.4.1 wrote identical files, and no result here looked version-dependent.

## What runs where

| Thing | Where | State |
|---|---|---|
| `reset.yml` (copy here) | `GetAI-IP/export-probe` (private, scratch), `.github/workflows/reset.yml`, next to 0.18's `probe.yml` | Pushed 9 November 2026 (`c0cbf48`, last `28a0654`). Scratch |
| `reset_probe.py` (copy here) | Same repo, `probe/reset_probe.py` | Scratch. Probe-only: **not a gate script** and not `reset_environment.py` |
| `lane-fl1.json` (copy here) | Same repo, `lane/fl1.json`: a stand-in for the lane manifest | Scratch |
| The reset commit | Same repo, `reset-commit/FactorySpike/` at `0c6e2d5`: the XML export of `FactorySpike`, unpacked by run 37558641. A stand-in for the head of `integration`. `.gitattributes` marks it `-text`, so Git never changes its line endings | Scratch |
| GitHub environment `fl1-exec`, federated credential `export-probe-fl1-exec` | From spike 0.18 | Reused. Scratch |
| Solution `FactorySpike` and its parts | `factory-lane-1`, from spike 0.18 | Reused as the baseline. Scratch |
| Environment variable value for `fspk_SpikeSetting` (`fl1-lane-value`) | `factory-lane-1`, outside the solution, made by the reset's step 3 | **New in 0.19.** Scratch |

Nothing new in Entra. The planted parts are gone (the reset deleted them; checked by name).

## How the probe works

`workflow_dispatch` only, refuses any ref but `main`, checks out its own repo, never pull request code (rule 5). Permissions `id-token: write` and `contents: read`. No secrets: the tenant ID, app ID and Dataverse URL come in as inputs. The job runs in the GitHub environment `fl1-exec`, on pac 2.14.1 under .NET `10.0.x`, signed in with `pac auth create --githubFederated`. The Web API calls use an app-only token with the GitHub OIDC token as the client assertion, as in 0.18. It shares 0.18's concurrency group, so only one run at a time touches the lane.

Modes:

1. **`baseline`** (read-only): export and unpack `FactorySpike`, then run the leftover finder on the clean lane. This calibrates the finder: on a clean lane it must find nothing. Its export became the reset commit.
2. **`plant`**: leave a night's mess, then export and show it against the reset commit, and run the finder:
   - a cloud flow, "Factory spike leftover flow", made with the `MSCRM.SolutionUniqueName` header (inside the solution);
   - a text column `fspk_Leftover` on the spike table, made with the header (inside the solution);
   - a cloud flow, "Factory spike stray flow", made with no header (outside the solution);
   - the main flow's definition changed (`$top` 1 to 7).
3. **`reset`**: the stand-in for `reset_environment.py`. It knows nothing of what `plant` made. Plan 5.4's steps:
   - Step 1, transactional test data: **not in this spike**.
   - Step 2: `pac solution pack` of the reset commit, then `pac solution import --force-overwrite --publish-changes`.
   - Step 3: the lane manifest's environment variable values, through the Web API **without** the solution header; then a check that the value has not joined the solution (it would be taken out of it if it had).
   - Step 4: find leftovers by query (below), plan, and only then delete. Brakes: any component the probe cannot judge, any managed component, anything inside the solution the lane identity did not make, any metadata outside the solution, or more than 10 deletes, and it deletes nothing (the lane would go Offline).
   - Step 5, the proof: export, unpack, compare every file with the reset commit, raw bytes first, then the canonical form 0.18 used; run the finder again; read the environment variable value back.

   Then a separate step looks up the planted parts by name: the probe checks the reset, not the reset itself.
4. **`unplant`**: delete the planted parts by name. A safety net. Not run.

**The leftover finder** (step 4), as it stands after the calibration runs:

- *Inside the solution:* every root component of `FactorySpike` that the reset commit does not hold. What the commit holds is read from the whole tree: tables from `Entities/`, flows and roles by ID, environment variables from their folder, connection references from `Other/Customizations.xml` (finding 2). Then every unmanaged custom column of a table the solution holds whole that the commit's `Entity.xml` does not list.
- *Outside the solution, rows with a maker:* every component row whose own `createdby` is the lane identity and that the solution does not cover. The probe asks each component table in turn: 21 classic tables (`workflows`, `roles`, `savedqueries`, `webresourceset` and the rest) and the 220 that `solutioncomponentdefinitions` names in this org. "Covered" means in the lane solution, or a part of a table it holds whole: columns, relationships, keys, choices, forms, views, charts, privileges, and rows that extend the table (finding 5). The values the lane manifest sets are allowed.
- *Outside the solution, metadata:* every unmanaged custom table or column that neither the lane solution nor the lane manifest's bootstrap list holds. One read of all tables with their columns.

Local checks before any run (9 November 2026, scratch harness, not committed):

- the reset commit reader on 0.18's export;
- the compare on a copy, a line-ending change and a version change;
- the finder and the removal against a fake lane after planting: the right three deletes, in the right order;
- the two brakes: an item it cannot judge, and a column not on the bootstrap list.

Repeated after each change to the finder.

## Found before any run (read-only)

- **`Other/Solution.xml` does not list every root component.** In 0.18's export its `RootComponents` named the table, the role and the flow, but not the environment variable or the connection reference. Those are only in `environmentvariabledefinitions/` and in `Other/Customizations.xml`. So "what the reset commit holds" has to be read from the whole tree. 0.18's note that the manifest check "reads the declared root components from `Other/Solution.xml`" is incomplete.
- **What Microsoft's pages say about finding components:** the `solutioncomponent` table has `createdby` and `createdon`; the Default Solution "contains all components in the system"; and a component made without a solution context "will only be added to the default solution". This suggested looking for Default Solution rows the lane identity created. Run 1 showed that does not work (finding 3).
- **`pac solution import --force-overwrite`** is documented as "Force an overwrite of unmanaged customizations"; `--publish-changes` publishes after a successful import.

## Findings (runs 1 to 5, 9 and 10 November 2026)

1. **The reset passes the exit test, and more.** After the reset, the export equalled the reset commit byte for byte (23 files, none added, none missing, none different). All three leftovers were gone, and the flow change was undone. Looked up by name afterwards: no leftover flow, no stray flow, no leftover column, `$top` back to 1. The environment variable value was set and stayed out of the solution and out of the export.
2. **Import with overwrite undoes changes but removes nothing**, as the plan says. After the import alone, the finder still saw all three leftovers, while the main flow's definition was already back to the commit's. So step 4 is needed for leftovers, and step 2 is enough for changes to what the commit holds.
3. **`solutioncomponent.createdby` cannot find what the lane identity made.** The Default Solution's rows are written by SYSTEM, whoever made the component. In `FactorySpike`, the rows for the flow, role, environment variable and connection reference are by SYSTEM too; only the table's row named the lane identity. Run 1's finder, built on the docs, found one row by the lane identity in the whole org. The maker is on the component's own row instead (`workflows`, `roles`, `connectionreferences` and so on). So the finder asks each component table for rows the lane identity created. `solutioncomponentdefinitions` names the table for 220 newer types, the org-specific codes among them: 10167 is the connection reference and 10260 the allowed MCP client. Of 241 types asked, 29 have no `createdby` to ask: mostly link tables, plus `systemform` and `canvasapp`. One pass of the finder takes about 20 seconds.
4. **Tables, columns and other metadata keep no maker at all**, and the `entity` and `attribute` tables have no `createdby`. So metadata outside the solution is found by state. One read of all 874 tables with their columns takes about 6 seconds and 7 MB. The lane already holds 14 unmanaged custom columns outside any solution, all Microsoft's own on system tables (image and file ID columns and the like). So the lane needs a bootstrap list of them, which fits bootstrap step 7, "save the baseline". If Microsoft adds more, the reset sees something it cannot judge and the lane goes Offline until a human adds them to the list.
5. **Dataverse makes parts of a new table outside the solution.** When the lane identity made the spike table in 0.18, Dataverse also made a `recyclebinconfig` row for it, made by the lane identity, in no solution but `Basic`, pointing at the table through `extensionofrecordid`. Run 2's finder could not judge it. The finder now treats rows that extend a covered table as parts of that table (run 3: clean).
6. **The platform keeps adding Default-only rows by SYSTEM:** for example 93 table rows on 5 November for tables that no longer exist, and SDK message steps. A search by time ("everything made since bootstrap") cannot tell them from the lane's work, so it was dropped.
7. **A column made with the solution header, on a table the solution holds whole, gets no `solutioncomponent` row at all**, neither in `FactorySpike` nor in the Default Solution. The export still carries it in `Entity.xml`. Only a comparison of the table's columns with the commit's `Entity.xml` finds it.
8. **A flow made with no solution header lands only in the Default Solution and is invisible to the export.** Only the query found it. This is risk 17's case.
9. **The lane's own environment variable value counts as "made by the lane identity outside the solution".** Unless the lane manifest allows it, the reset would delete in step 4 what step 3 just set. The value made by the Web API without the header did not join the solution.
10. **Timings on a hosted runner,** for this small solution:

    | Step | Time |
    |---|---|
    | pack | 1 second |
    | import with overwrite and publish | 90 seconds |
    | value | 1 second |
    | each finder pass | about 20 seconds |
    | removal and publish | 22 seconds |
    | export and unpack | 11 seconds |
    | whole reset job, pac install included | 3.5 minutes |

    The real reset needs one finder pass, not the probe's three. The import will grow with the solution.
11. **Deletes are planned before any is made.** Item by item:
    - Inside the solution: a flow, role, environment variable or connection reference is deleted only if the lane identity made it. A table or column is deleted only if it is unmanaged and custom. Anything else would have to be taken out of the solution by hand.
    - Outside the solution: only rows the lane identity made are deleted.
    - Metadata outside the solution is never deleted, because no maker is kept.

    One refusal stops every delete. On the real lane only the path that deletes ran; the refusals ran against the fake lane.
12. **The OIDC subject is the immutable form again**, as in 0.18: `repo:GetAI-IP@801576/export-probe@5352096:environment:fl1-exec`. No token-shaped string (`eyJ`) in any of the five run logs.

Not tested:

- step 1 (transactional test data);
- a story that resumes from its own branch head, not `integration`;
- a connection reference bound to a connection in the lane;
- the refusal paths and a metadata stray on the real lane (only against the fake lane);
- an environment variable value already inside the solution (the take-out step did not run);
- forms and canvas apps, which have no maker column;
- running with 0.10 in `factory-test`;
- a second pac version.

## Run order and results

Runs start with `GH_HOST=getai.ghe.com gh workflow run reset.yml -R GetAI-IP/export-probe --ref main -f mode=<mode> -f tenant_id=... -f app_id=... -f env_url=https://factory-lane-1.crm6.dynamics.com/`.

| Run | ID | Mode | Result |
|---|---|---|---|
| 1 | 37428706 | baseline | Clean, but only because the finder was blind: it found one row by the lane identity in the whole org (finding 3). Export 29 seconds on a fresh runner |
| 2 | 37558056 | baseline | Finder rebuilt on each component's own maker, and metadata by state. One item it could not judge: the table's `recyclebinconfig` row (finding 5) |
| 3 | 37558641 | baseline | Clean. Its export, byte for byte the same as 0.18's from 8 November, became the reset commit (`0c6e2d5`) |
| 4 | 37559106 | plant | Three leftovers and one change made. The export showed the leftover flow (two files and a root component), the leftover column (`Entity.xml`) and `$top` 7. The stray flow was not in it. The finder saw all three, and nothing it could not judge |
| 5 | 37559661 | reset | **Pass.** Export equal to the reset commit, byte for byte. Finder clean afterwards. Value set. The planted parts gone by name |

Each run took 1 to 3.5 minutes, install included.

## What this means for the plan

Proposals only. The plan is not edited (Boroon's word decides, as in 0.18):

- **Plan 5.4, step 4:** say how leftovers outside the solution are found:
  - rows with a maker, by asking each component table, including those `solutioncomponentdefinitions` names;
  - tables and columns by state, against a bootstrap list in the lane manifest;
  - parts of a held table, including rows that extend it, count as covered;
  - columns on held tables are compared with the commit's `Entity.xml`.

  Add the brakes, and say the lane manifest's own values are allowed.
- **Plan 5.4, bootstrap step 7:** save the bootstrap list in `lanes.json`: the unmanaged custom tables and columns outside any lane solution.
- **Plan 5.4, step 5:** the proof can ask for byte equality, which held here; the canonical form then only explains a failure. If Microsoft's server version stamp changes the files (0.18 finding 9), the canonical form may need to ignore it.
- **Plan 5.6 and the `factory-gates` follow-up list (item 9):** the manifest check must read the root components from the whole XML tree, not only `Other/Solution.xml`.
- **Plan 11.1, row 0.19, and risk 17:** the result. Risk 17's answer works for the types tested; it stays open for forms, canvas apps and metadata made outside the solution.
- **A decision for Boroon:** what the reset does with a table or column made outside the solution. No maker is kept on metadata. The probe refuses it, and the lane goes Offline until a human looks. The other way is to delete what appeared since the last proven reset.

## Scratch to delete (only at Boroon's word)

**Kept for spike 0.14** (Boroon, 10 November 2026): 0.14 makes and updates a flow by the Web API as the lane identity and exports it, which this scratch makes quicker. Delete all of 0.18's and 0.19's scratch together after 0.14, at his word.

Spike 0.18's list (`docs/plans/spike-0.18/README.md`) still holds and covers almost everything. 0.18's `teardown` mode deletes environment variable values before the definition, so it also takes the value 0.19 made.

| Thing | Where | How |
|---|---|---|
| Environment variable value `fspk_SpikeSetting` (`fl1-lane-value`), outside the solution | `factory-lane-1` | 0.18's `mode=teardown` (values first) |
| `reset.yml`, `reset_probe.py`, `lane/fl1.json`, `.gitattributes`, `reset-commit/` and runs 37428706, 37558056, 37558641, 37559106, 37559661 (artifacts expire after three days) | `GetAI-IP/export-probe` | Go with the repo (0.18's list) |
| Solution `FactorySpike`, publisher `factoryspike`, repo `GetAI-IP/export-probe`, credential `export-probe-fl1-exec` | As in 0.18's list | As in 0.18's list: teardown first, then the repo, then the credential |

Kept for Stage 3, as before: `getai-fl1-exec`, its application user, `factory-lane-1` and the allowed MCP client `new_getaifl1exec`.
