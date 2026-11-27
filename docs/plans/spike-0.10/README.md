# Spike 0.10: Test environment behaviour, by "export both"

Plan section 11.1, row 0.10 (ADO 2459). Session 54, Thursday 26 November 2026, on the laptop (desktop app), laptop track B. It was due Wednesday 25 November. It was kept to what the Stage 1 exit test (2539, Friday 27 November) needs. The result is also in `docs/progress.md` (Session 54).

**Result: the exit test passes, and the "export both" route works** (runs 41298256 to 41338391, 26 November 2026, 02:13 to 04:06 UTC). The scratch is deleted and read back gone.

- **Export both works.** As `getai-fl1-exec`, on a runner with no secret, the solution exported unmanaged and managed and unpacked into one tree with `--packagetype Both`. A second export was **byte-identical**, within each run (six times) and across two runs 13 minutes apart. The managed export adds about 8 to 10 seconds.
- **Both packs work offline.** The gate's own `pack_offline.py`, in a sandbox with no network, packed that tree `Unmanaged` and `Managed` on pac 2.4.1 and 2.15.1, every time. The managed zip says `Managed` 1 and has the managed export's members and root components. Unpacking it gives the export's files byte for byte. Both pac versions packed identical members.
- **Upgrades apply and remove dropped parts.** As `getai-nwt-test`, Test took the 2.4.1-packed managed zip with the gate's flags over each version. An additive version applied, and a changed flow took its new text. Then a version that dropped a column, a table, an environment variable and a flow removed all four, even with data in the dropped table and column. The data in kept columns stayed. Times are below: 35 to 132 seconds per upgrade for this small solution.

**Two things will stop tomorrow's exit test (2539) unless the gate changes first.** Neither is in this spike's exit test, and neither is changed here (only Session 53 may change `factory-gates`):

1. **`--stage-and-upgrade` fails on a first install** (finding 5). It needs the solution already in Test ("Cannot create a holding solution for missing base"). Northwind is not in `factory-test`, so the gate's import step, as written, fails on the first gate run for `ai-factory-nwt`. A plain managed import (the same flags without `--stage-and-upgrade`) installed it.
2. **pac 2.4.1's solution checker writes no report file** (finding 11). It exits 0 and prints its counts, but `--outputDirectory` stays empty (two runs). pac 2.15.1 writes the report zip there. The gate pins 2.4.1 and `checker_gate.py` fails when there is no report, so `verify-in-test` stops at the checker on every PR, clean or not.

Exit test (plan 11.1): a managed import with `--stage-and-upgrade` of successive PR versions, measuring import time. Pass if upgrades apply and remove dropped components, and times are recorded. If it fails: delete and re-import, or one Test environment per lane.

The route tried is the one Boroon chose on 23 November 2026 (ADO 2459's body), because `pac solution pack --packagetype Managed` stops on an unmanaged-only export (gate finding 11):

1. the driver exports the lane solution twice, unmanaged and managed, as the lane identity;
2. it unpacks both into one tree with `pac solution unpack --packagetype Both`; that tree is `src/`;
3. the gate packs offline from that tree, `Unmanaged` then `Managed` (pac 2.4.1, the gate's pin, and 2.15.1);
4. Test imports the managed zip, upgrading over the last one.

The fallback, for the gate to import the unmanaged zip into Test, is **not needed**. It would not have worked well anyway [from Microsoft's docs, not run]: once Test holds a solution as managed, an unmanaged import of the same solution fails (error 80048041), and an unmanaged import never removes a dropped component.

## What runs where

| Thing | Where | State |
|---|---|---|
| `probe.yml` (copy here) | `GetAI-IP/import-probe` (private, scratch, repo 5468676), `.github/workflows/probe.yml` | Pushed 26 November 2026 (`c696b18`, last `1600c33`). **Deleted** |
| `import_probe.py` and `check_vars.sh` (copies here) | Same repo, `probe/` | Probe-only, not gate scripts. **Deleted** with the repo |
| `pack_offline.py` | Same repo, `probe/pack_offline.py`: **the gate's own script**, copied unchanged from `GetAI-IP/factory-gates` at `release` `5ba13be`; its SHA-256 (`ff017c10…`) matches the gate's `scripts.sha256`. Not copied here: the gate holds it | **Deleted** with the repo |
| Repository variables `TENANT_ID`, `LANE_APP_ID`, `LANE_URL`, `TEST_APP_ID`, `TEST_URL` | Same repo. Not secret; kept there so the IDs stay out of this public repo | **Deleted** with the repo |
| GitHub environments `fl1-exec` and `lcp-test` | Same repo, made by the first run, no protection rules | **Deleted** with the repo |
| Federated credential `import-probe-fl1-exec` | On `getai-fl1-exec`, subject `repo:GetAI-IP@801576/import-probe@5468676:environment:fl1-exec` | Made 26 November 2026 by `az`, at Boroon's word in the brief. **Deleted** |
| Federated credential `import-probe-lcp-test` | On `getai-nwt-test`, subject `repo:GetAI-IP@801576/import-probe@5468676:environment:lcp-test` | Made the same way. **Deleted** |
| Solution `FactoryImportSpike` (publisher `factoryspike`, prefix `fspk`) and its parts | `factory-lane-1`, unmanaged, made by the probe as the lane identity | **Deleted** |
| The same solution, managed | `factory-test`, imported by the probe as the Test identity | **Uninstalled** |
| The checker's two reports | Microsoft's checker service storage, reached by a signed link valid for 24 hours | Not deletable by us; they expire. Scratch content only |

Northwind was not used: it reaches `factory-test` only through the gate (Boroon, 24 November 2026).

## How the probe works

`workflow_dispatch` only. Every job that signs in refuses any ref but `main` and checks out only its own repo (rule 5). No secrets. Actions are pinned to the gate's commit SHAs. pac is installed at a pinned version with `dotnet tool install` on .NET `10.0.x`, telemetry off. The Web API calls use an app-only token with the GitHub OIDC token as the client assertion, as in spikes 0.18 and 0.19. One concurrency group, so one run at a time.

Each identity has its own job and GitHub environment, as plan 5.3 has it. The lane identity (`getai-fl1-exec`, environment `fl1-exec`) never reaches Test. The Test identity (`getai-nwt-test`, environment `lcp-test`) never reaches the lane. The pack job holds no credentials at all (no `id-token`).

Modes:

1. **`check`** (read-only): each identity prints its OIDC claims (never the token), signs in to the Web API and lists every scratch part in its environment.
2. **`cycle`**, with an input `state` (1 to 5), three jobs in a row:
   - **`export`** (lane identity, pac 2.15.1): sets the scratch solution in `factory-lane-1` to the state through the Web API and publishes. Then it exports the solution unmanaged and managed, **twice**, and unpacks each pair with `--packagetype Both`. It also unpacks the first pair `Unmanaged` only and `Managed` only, to see what `Both` adds. Trees are compared byte for byte, then in a canonical form.
   - **`pack`** (no credentials; pac 2.4.1 and 2.15.1): runs **the gate's own `pack_offline.py solution`** on the `Both` tree inside `sudo unshare --net`. That is a sandbox with no network, checked first: `curl` to the sign-in host must fail there. It checks each zip's `Managed` flag, version, member names and root components against the export's. Then it unpacks each packed zip and compares it with the export's own unpack.
   - **`import`** (Test identity, pac 2.4.1, the gate's pin): may run the solution checker first (input `checker`). It makes a settings file and imports the **2.4.1-packed managed zip**. With `import_mode: gate` it uses the gate's flags (`--settings-file … --stage-and-upgrade --async --max-async-wait-time 30`); with `plain`, the same without `--stage-and-upgrade`. It times the import. Then it reads every scratch part in Test, the solution's version, any `_Upgrade` holding solution and the platform's solution history (`msdyn_solutionhistories`). With `seed`, it adds a row to each scratch table, so later drops are tested on a table and a column that hold data.
3. **`observe`** (read-only): reads the scratch solution in Test, with its whole solution history.
4. **`teardown`**: uninstalls the solution from Test, then deletes every scratch part from the lane, and lists what is left in each. It fails if anything is.

The settings file is `fresh` (from `pac solution create-settings` on the zip, with a value for each environment variable), `stale` (it names `fspk_ImportSetting` whatever the zip holds, as a static project file in the gate would after a PR drops the variable) or `none`.

The states of the scratch solution:

| State | Version | What changes |
|---|---|---|
| 1 | 1.0.0.1 | Table `fspk_importitem` (columns `fspk_kept`, `fspk_dropped`), table `fspk_importextra`, global choice `fspk_importstage`, environment variable `fspk_ImportSetting` (text, default `lane-default`), security role "Factory import spike role", cloud flow "Factory import spike flow" (manual trigger, one Compose step, no connector, left off; text `import spike v1`) |
| 2 | 1.0.0.2 | Adds column `fspk_added`; the flow's text becomes `import spike v2` |
| 3 | 1.0.0.3 | **Drops** column `fspk_dropped`, table `fspk_importextra`, the environment variable and the flow |
| 4 | 1.0.0.3 (the same) | Adds column `fspk_sameversion`, with no version change |
| 5 | 1.0.0.3 (the same) | **Drops** column `fspk_sameversion`, with no version change |

## Runs

Runs start with `GH_HOST=getai.ghe.com gh workflow run probe.yml -R GetAI-IP/import-probe --ref main -f mode=<mode> …`. Times are UTC, 26 November 2026.

| Run | ID | Mode and inputs | Result |
|---|---|---|---|
| 1 | 41297271 | `check` | Pass. Both identities signed in by OIDC with the subjects above; neither environment held any scratch |
| 2 | 41298256 | `cycle`, state 1, gate flags, checker, seed | Export and both packs pass. Checker (2.4.1): exit 0, no report file. **Import fails in 27.3 s**: "Cannot create a holding solution for missing base FactoryImportSpike" (finding 5). Test unchanged |
| 3 | 41301746 | `cycle`, state 1, **plain**, checker, seed | Checker: 2.4.1 33.7 s, no report; 2.15.1 34.2 s, report written (finding 11). **Import (first install) 145.5 s**; all parts there, managed, 1.0.0.1. Rows seeded |
| 4 | 41304331 | `cycle`, state 2, gate flags | **Upgrade 59.5 s.** The probe then failed on a Web API read of the new column (finding 13); run 5 read the result |
| 5 | 41332381 | `observe` | Test at 1.0.0.2, all as expected: the new column, the flow's v2 text, the settings value, the seeded rows |
| 6 | 41332541 | `cycle`, state 3, gate flags, **stale** settings | **Upgrade 132.2 s.** All four dropped parts removed; kept data stayed; the stale settings entry caused no error |
| 7 | 41334836 | `cycle`, state 4, gate flags | **Same version, 39.2 s.** The new column applied |
| 8 | 41336921 | `cycle`, state 5, gate flags | **Same version, 34.9 s.** The dropped column removed |
| 9 | 41338391 | `teardown` | Pass. Test: uninstalled in 131.7 s. Lane: the role, the table, the global choice, the solution and the publisher deleted. Both listings empty |

The scripts never print a token (the `check` mode prints claims only). No token-shaped string (`eyJ`) is in any of the 1,063 files saved from the runs (the step logs the probe wrote, and every artifact). The full job logs went with the repo. The checker's log does carry a signed link to its report (finding 12).

### Times

Export, for this small solution (24 to 42 unpacked files), in seconds. The first export on a fresh runner was 18 to 19 seconds; later ones 8 to 10.

| Run | State | Unmanaged export, rounds 1 and 2 | Managed export, rounds 1 and 2 | Unpack `Both` | Unpack `Unmanaged` only |
|---|---|---|---|---|---|
| 41298256 | 1 | 18.2, 8.6 | 10.5, 8.8 | 1.1, 1.1 | 1.0 |
| 41301746 | 1 | 8.9, 8.9 | 9.1, 8.5 | 1.2, 1.1 | 1.0 |
| 41304331 | 2 | 10.7, 8.8 | 8.3, 8.6 | 1.1, 1.1 | 1.1 |
| 41332541 | 3 | 18.8, 9.1 | 10.0, 9.3 | 1.1, 1.0 | 1.0 |
| 41334836 | 4 | 9.2, 9.5 | 8.1, 7.4 | 1.1, 1.2 | 1.3 |
| 41336921 | 5 | 9.6, 9.8 | 8.7, 8.5 | 1.5, 1.1 | 1.1 |

The gate's `pack_offline.py` (both kinds) took 1.9 s on pac 2.4.1 and 2.4 s on 2.15.1 (run 41298256).

Import into Test, as the Test identity, in seconds. "pac" is the wall time of `pac solution import`; "server" is the platform's own `msdyn_totaltime`.

| Run | Version in Test before, then the zip's | Kind (from the solution history) | pac | Server |
|---|---|---|---|---|
| 41298256 | none, then 1.0.0.1 | Import, failed (gate flags) | 27.3 | 5 |
| 41301746 | none, then 1.0.0.1 | Import, New (plain) | 145.5 | 131 |
| 41304331 | 1.0.0.1, then 1.0.0.2 | InlineUpgrade (additive) | 59.5 | 42 |
| 41332541 | 1.0.0.2, then 1.0.0.3 | InlineUpgrade (four drops) | 132.2 | 120 |
| 41334836 | 1.0.0.3, then 1.0.0.3 | InlineUpgrade (one column added) | 39.2 | 30 |
| 41336921 | 1.0.0.3, then 1.0.0.3 | InlineUpgrade (one column dropped) | 34.9 | 21 |

The uninstall (teardown) took 131.7 s. The solution checker took 33.7 to 34.2 s. Plan 5.8 budgets 3 to 10 minutes for the import into Test. This small solution took 0.6 to 2.5 minutes; Northwind is far larger (its unmanaged import into `factory-lane-1` took 4 min 24 s, Session 48).

## Findings

1. **Export both works as the lane identity, headless.** `pac solution export --managed` ran as `getai-fl1-exec` with no secret, every time, and `pac solution unpack --packagetype Both` took the pair (the unmanaged zip `<name>.zip` with `<name>_managed.zip` beside it).
2. **What `Both` writes beyond an `Unmanaged` unpack:**
   - one `_managed.xml` beside each form: card, main and quick, so three per table here (six at state 1, three after table `fspk_importextra` was dropped). Session 48 saw the same beside Northwind's app and site map;
   - `Other/Solution.xml` says `<Managed>2</Managed>` (both) where an unmanaged unpack says `0`;
   - nothing missing.
   - **The managed form halves hold empty cell labels** (`<label description="" …>`) where the unmanaged halves hold "Name" and "Owner".
   - What the gate already knows (read from `release` `5ba13be`, not run here): `check_manifest.py` accepts `_managed.xml` beside forms, apps and site maps (gate PR 29); `lint_accessible_labels.py` reads the managed halves too and passed on Northwind's `Both` tree (gate PR 30, Session 50). `plan_from_export.py` keys forms by form ID, and both halves carry the same ID, so whichever half it reads last stands for the form [inference from the code, not run]. That is harmless while both halves change together, but worth a test there.
3. **A second export stays byte-identical with `Both`.** In all six export jobs the second round's `Both` tree equalled the first byte for byte (42 files at states 1 and 2, 24 at states 3 to 5), and both zips' members were identical. Across runs too: the two state-1 exports, 13 minutes apart in different runs, gave identical trees (`diff -r`). So the lane drift check and the reset proof still hold with `Both`.
4. **The managed export adds about 8 to 10 seconds** per export for this size (7.4 to 10.5 s, against 8.6 to 10.7 s for the unmanaged one after the first). `Both` adds about 0.1 s to the unpack. So the driver's export step roughly doubles, from about 10 to about 20 seconds here. It will grow with the solution.
5. **`--stage-and-upgrade` fails when the solution is not yet in Test.** The import job's message: "ImportAsHolding failed with exception: Solution manifest import: FAILURE: Cannot create a holding solution for missing base FactoryImportSpike". pac exited 1 and Test was unchanged. The same zip imported with the same flags minus `--stage-and-upgrade` installed it (145.5 s). **For 2539:** Northwind is not in `factory-test` (it reaches Test only through the gate), so the gate's import step, as written, fails on its first run there. The step needs to install when the solution is absent and upgrade when it is present (proposal 3).
6. **Upgrades apply.** 1.0.0.1 to 1.0.0.2 added the column and gave the flow its v2 text. The settings file's new value (`test-value-s2`) replaced the old one, and the seeded rows stayed. Every upgrade was recorded as an **InlineUpgrade**, the platform's single-step upgrade. No `<name>_Upgrade` holding solution was there after any import. Microsoft notes the single-step upgrade "no longer use[s] a temporary `_Upgrade` solution". So the "stage" in `--stage-and-upgrade` leaves nothing to apply later.
7. **Dropped components are removed (the exit test).** 1.0.0.2 to 1.0.0.3 removed column `fspk_dropped` (it held a seeded value), table `fspk_importextra` (it held a row), environment variable `fspk_ImportSetting` (its definition and its value) and the flow. The kept row and its `fspk_kept` value stayed. A managed upgrade is a one-way door for data in what it drops, in Test as in UAT and Prod.
8. **The version need not change for Test.** 1.0.0.3 imported over 1.0.0.3 twice with the gate's flags. Both were InlineUpgrades: the first added a column, the second removed it. Microsoft's page says "An update must have a higher major, minor, build, or revision number". That did not block an upgrade at the same version. So the driver can keep the version the lane has; plan 5.6 already gives it the version stamp. Not tested: a lower version than Test's, which happens if two PRs import out of order.
9. **A stale settings file did no harm.** At 1.0.0.3 the settings file still named `fspk_ImportSetting`, which the zip no longer had. The import gave no error or warning and made no orphan value. So the project's static `test.settings.json` in the gate need not change in the same PR that drops a variable [one case].
10. **Settings values land as unmanaged rows.** The value that `--settings-file` set in Test has `ismanaged` false: an unmanaged row on top of the managed definition. It went when the definition was dropped (finding 7). Plan 7.4 lists unmanaged layers in `factory-test` as a gardening finding, so that scan should expect environment variable values.
11. **pac 2.4.1's checker writes no report file; pac 2.15.1 does.** As the Test identity, on the same zip and in the same job, `pac solution check --geo Australia --outputDirectory <folder>`:
    - on **2.4.1** printed "Downloading 1 files to <folder>" and "Finished downloading 1 files", then its counts (all 0), and exited 0. **The folder was empty**, and no report was anywhere under the runner's temp, workspace or home folders. Seen in runs 41298256 and 41301746;
    - on **2.15.1** wrote `<timestamp>_FactoryImportSpike_<4 hex>.zip` into the folder (run 41301746). That is the shape `checker_gate.py` reads.
    
    **For 2539:** the gate pins pac 2.4.1, and `checker_gate.py` fails with "no SARIF report" when the folder is empty. So `verify-in-test` fails at the checker step on every PR, even a clean one, before the import. Also settled: the checker works as the Test identity with **no API permission** (`getai-nwt-test` has none), so `factory-test` README finding 3 stands, and plan 5.3's "PowerApps-Advisor `Analysis.All`" is not needed. It took about 34 seconds for this solution.
12. **pac prints the checker report's signed link in the job log.** The link to Microsoft's storage carries its signature and is valid for 24 hours. Anyone who can read the gate's run log could fetch the report in that time. The report holds checker findings, not data. It is minor, but the evidence step could note it.
13. **The Web API can lag behind an upgrade.** Seconds after the 1.0.0.2 upgrade (run 41304331), a Web API read that named the new column `fspk_added` failed with 0x80060888, "Could not find a property named 'fspk_added'". The column's metadata already read back. A read in run 41332381, about an hour later, worked. Later cycles waited for it, and their first reads worked with no error. So it was seen once in four upgrades. **For 3027 (`run_workflow.py`) and the Playwright kit:** retry the first queries after the import for a short while on that error, before failing a scenario.
14. **Teardown in Test is one uninstall.** Deleting the managed solution removed every part and the seeded data in 131.7 s, and no publisher was left for the probe to delete. Nothing was left by name or prefix (read back by the probe as the Test identity, then again by Boroon's own sign-in).

## Proposed plan edits (not made; Boroon decides)

Each is a proposal only. The two marked **for 2539** are gate changes, which only Session 53 may make today; the plan edit would follow at Boroon's word.

1. **5.6, the driver's export** (and 14.4, a row). The driver exports the lane solution twice, unmanaged and then managed (`pac solution export`, then again with `--managed`), and unpacks the pair with `pac solution unpack --packagetype Both`; that tree is `src/`. For a small solution it adds about 8 to 10 seconds, and a second export stays byte-identical (spike 0.10). The tree gains a `_managed.xml` beside each form, app and site map, and `Other/Solution.xml` says `<Managed>2</Managed>`. Line 600's "`pac solution export` then `pac solution unpack`" becomes "an unmanaged and a managed export, then `pac solution unpack --packagetype Both`". Session 48 proposed the `Both` unpack for Northwind; this makes it the rule.
2. **5.7 and Appendix A, `build`.** No change to `pack_offline.py` or its flags: from the `Both` tree it packs both kinds offline on pac 2.4.1 and 2.15.1. Only its docstring's "[untested]" for the managed call is out of date (a gate change; not needed for 2539).
3. **Done in the gate as gate PR 35** (https://getai.ghe.com/GetAI-IP/factory-gates/pull/35, 27 November 2026, Session 61, at Boroon's word; the plan edit still waits on his word). **For 2539. Appendix A, `verify-in-test`, "Import the managed solution into Test"** (and 5.7). Install when the solution is absent, upgrade when present. For example, a trusted step reads the solution's unique name from the zip's `solution.xml`, asks Test by the Web API (`solutions?$filter=uniquename eq '<name>'`) as the Test identity, and then runs `pac solution import` with `--stage-and-upgrade` only if it is there. The rest of the flags stay. A first install also happens after anyone deletes the solution from Test.
4. **For 2539. The gate's pac pin, `PAC_VERSION`, from 2.4.1 to 2.15.1** (or the newest, 2.16.1 on NuGet today, once A1 reads its release notes). At least `verify-in-test` needs it for the checker's report. Evidence that the move is safe: 2.15.1 and 2.4.1 packed identical members here, and spike 0.18 found 2.14.1 and 2.4.1 exported identical files. Plan 5.7's pin line and Appendix A's `env` would match. The other way out is a second pac install for the checker step alone, as this probe did.
5. **11.1, row 0.10:** "**Run 26 November 2026** (Session 54): passed. Upgrades applied and removed a dropped column, table, environment variable and flow, with data in them. Times 35 to 132 seconds for a small solution. `--stage-and-upgrade` fails on a first install (`docs/plans/spike-0.10/README.md`)." And the fallback cell: "Not needed. Install when absent, upgrade when present."
6. **5.3, the Test identity's row.** Drop "App permissions: Dynamics CRM and PowerApps-Advisor `Analysis.All`". The checker ran as `getai-nwt-test`, which has no API permission (finding 11, with `factory-test` README finding 3).
7. **5.8, the run-time table** ("Solution import into Test, 3 to 10 minutes"; "Solution checker, 2 to 5 minutes"; both estimates). Keep them, and add the first measures: for a small solution the import took 0.6 to 2.5 minutes, longest when it dropped a table (finding 7's run, 2.2 minutes), and the checker about 34 seconds.
8. **5.8 or 5.9, locked scenarios after the import.** The runner retries its first Web API reads for a short while on 0x80060888 after an import (finding 13), so the platform's lag is not read as a failed scenario.
9. **7.4, gardening.** The scan for unmanaged layers in `factory-test` expects environment variable values set by the settings file (finding 10).
10. **12, a risk or a line in risk 17's neighbourhood**, if Boroon wants one: a managed upgrade in Test drops data in removed columns and tables. That is expected and is why removals are listed in the PR body (5.6). Test data is seeded by scenarios, so nothing real is lost.

Left for the gate (not plan edits): `plan_from_export.py`'s handling of the two form halves (finding 2), with Session 48's note on the app and site map halves; and the checker's signed link in the log (finding 12).

## Scratch

Everything this spike made is deleted, and each deletion was read back (26 November 2026):

| Thing | Where | Deleted | Read back |
|---|---|---|---|
| Solution `FactoryImportSpike` (managed), with its tables, columns, global choice, role, the seeded rows and the publisher `factoryspike` | `factory-test` | Uninstalled by the probe as the Test identity (run 41338391, 04:02 to 04:04 UTC, 131.7 s) | The probe's listing (solutions, publishers, `fspk_` tables, choices, environment variables and their values, roles, flows, connection references): none. Again as Boroon by the Web API at 04:09 UTC: none |
| Solution `FactoryImportSpike` (unmanaged), its role, table `fspk_importitem`, global choice `fspk_importstage`, and the publisher `factoryspike` (the other parts were dropped by states 3 and 5) | `factory-lane-1` | By the probe as the lane identity (run 41338391, 04:05 UTC) | The same listing, by the probe and again as Boroon: none |
| Federated credential `import-probe-fl1-exec` | `getai-fl1-exec` in Entra | `az ad app federated-credential delete`, 04:09 UTC | `az ad app federated-credential list`: none. The app has no secret or certificate |
| Federated credential `import-probe-lcp-test` | `getai-nwt-test` in Entra | The same | Only `ai-factory-nwt-lcp-test` is left (Session 48's, kept). No secret or certificate |
| Repo `GetAI-IP/import-probe`, with its environments, variables, runs and artifacts | `getai.ghe.com` | `gh repo delete`, 04:09 UTC | `gh api repos/GetAI-IP/import-probe`: HTTP 404 |

Kept, as before: `factory-lane-1` (with Northwind), `factory-test`, `getai-fl1-exec`, `getai-nwt-test` and their application users. The copies here (`probe.yml`, `import_probe.py`, `check_vars.sh`) are the only record of the probe.
