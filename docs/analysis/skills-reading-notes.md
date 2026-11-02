# Reading notes: the first 16 skills

Date: 2 November 2026. Status: notes from reading, so everything here is a proposal until Boroon approves it.

What was read: all 16 skills in `skills/`, every file in each folder, including the four scripts (`floor-guard` in the Addy reference, `quality-gate.mjs`, `log.sh`, `template.sh`). This is the "read in full" step from plan section 8.3 and rule 19. It is the same batch as `tshirt-sizing.md` section 4, step 2.

Companion files: `skills-comparison.md` (every skill in the three packs), `tshirt-sizing.md` (which size uses which skill).

## Safety read (rule 19)

- No hidden network calls, no data sent out, no instructions aimed at the model beyond the skill's own job.
- The only code that runs is small. `floor-guard` (in the Addy reference) uses `git` only. `quality-gate.mjs` reads a JSON report. `log.sh` appends a row to a file. `wizard/template.sh` writes `.env` and runs `gh secret set` on a human's machine.
- Careful points worth keeping: `log.sh` blocks spreadsheet formula injection. `source-driven-development` treats fetched docs as data. `doubt-driven-development` never calls an outside model CLI without a yes from the user, and tells the agent to pipe the prompt through a file, not a shell argument. The Benny skills forbid any Slack write by child agents.
- Nearly all of the Tan, Pocock and Benny skills are marked `disable-model-invocation`. They run only when someone calls them. That fits rule 17.
- Verdict: nothing found that blocks adoption. Pinning is done in `skills/README.md`.

## Things the skills assume that GET AI does not have

Most need adapting, not just copying.

- **Cursor tools.** The Tan skills and Benny use Cursor's `Task` subagents, a `pstack-models.mdc` rule, the `poteto-mode` skill, `unslop`, the `principle-*` skills, and the `.cursor/skills/` path. None of those exist here. `how`, `why`, `blast-radius` and `show-me-your-work` all point at them.
- **Other trackers.** `why` searches Linear, Notion, Slack, Datadog, Sentry and Databricks. `triage-issue-reports` and `reproduce-and-fix-issues` run on Slack. GET AI uses Azure DevOps (ADO) and an ITSM tool still to be named.
- **Other Pocock skills.** `triage` and `ask-matt` call skills that are not in the batch: `grilling`, `domain-modeling`, `setup-matt-pocock-skills`, `implement`, `to-spec`, `to-tickets` and more.
- **A web app to drive.** The verification skills assume a browser, a CLI or a TUI. Power Platform needs `lcp-verify` to play that part.

## One line on each, and where it fits

| Skill | What it does | Fit for GET AI | Adapt how |
|---|---|---|---|
| `constraint-driven-development` | Writes the quality bar into `CONSTRAINTS.md`. A diff check stops the agent lowering it (new suppressions, skipped tests, thresholds moved down, new exceptions). Exit codes 0, 1, 2 | Strong. Same idea as rule 11 and the seed for `coding-standards.md`. The floor guard is a ready pattern for the gate | The interview needs a live human, so run it by day only. Replace the JS and TS patterns with Power Platform ones: solution XML, flow JSON, test files |
| `doubt-driven-development` | A fresh reviewer that sees the artifact and contract but not the claim, told to find faults. Up to 3 cycles, then stop and escalate | Strong. Matches our verifiers (fresh session, no builder context). Gives the reconcile step and a "doubt theatre" warning sign | Cannot run inside a subagent. The night gate runs it from the top level. Skip the cross-model offer at night, and say so |
| `source-driven-development` | Fetch official docs for the exact version, cite them, flag anything unverified | Good for L and M work. The Microsoft Learn tool is already connected | Add a rule to prefer Microsoft Learn. Power Platform docs move fast, so record the doc date |
| `create-verification-skill` | Builds a project verification skill: launch, doctor, drive, evidence, cleanup, plus a feature map with four fixed headings | Very strong. This is close to a blueprint for `lcp-verify` and its feature map | Swap browser and PTY recipes for Playwright against the model-driven app, Dataverse queries, flow run history. Keep the proof standards and "never weaken the journey" |
| `maintain-verification-skill` | Keeps the feature map honest. One reader per feature, one live pass, at most one PR | Strong, for the weekly routine (plan section 7) | Run by day. Output is a reviewed PR, as rule 17 needs |
| `blast-radius` | Finds what else breaks, then proves the one fact the change is safe because of by running real code. Five levels of how sure you are | Strong for M and L. Feeds the blast-radius part of Merge Danger | An LLM writeup may raise the score only (rule 11). Add Power Platform lookups: other flows on the same table, connection references, solution layers |
| `show-me-your-work` | One TSV row per decision with evidence, append only, audit against the transcript, and a different-model review | Strong. Fits rule 16 and the PR evidence | Point the audit at our transcript files in Blob, not Cursor paths. Commit the log into the evidence bundle |
| `correct` | Find repeat mistakes, then fix them at the highest level: design, then types, then lint, then tests, docs last. Prove each check fails on a real past mistake | Good for the weekly retro and for `lcp-verify` checks | Run by day after a bad week. Output goes to a reviewed PR |
| `how` | Explains how a subsystem works, using explorers and one explainer | Useful by day, to read a client solution before changing it | Rewrite the subagent lines for Claude Code. Add Power Platform views (solution layers, dependencies) |
| `why` | Explains why code is shaped as it is, with a confidence scale and honest gaps | Useful for the Story Planner and for client solutions with no history | Replace Linear, Notion and Slack with ADO, SharePoint and Teams. The confidence tiers in `epistemics.md` are worth keeping as they are |
| `triage` (Pocock) | Moves issues through states. Verify the claim, grill, then write a durable agent brief. Records rejected requests in `.out-of-scope/` | Strong match for the outer loop (plan section 4.5) and for Factory Eligible. `ready-for-agent` is close to our flag | Map states to ADO. Keep the AI disclaimer on every post and the rule "verify before you grill". The agent brief template is a good base for the night story spec |
| `wizard` | Writes an interactive script that walks a human through steps only they can do, then saves the values | Good for the PARK path (rule 8) and for the portal-only steps in stage 1 and 2 | Needs a human at a terminal, so it is day work. Add Entra, Power Platform admin and ADO steps |
| `to-questionnaire` | Turns "I need an answer from someone else" into a short questionnaire | Good for the day gate: acceptance owners, client IT, Partner Center (spike 0.1) | Little change. Suits the credit ruling question in plan section 9.1 |
| `ask-matt` | A router that says which skill fits. Includes the rule for what to do at the end of a phase: continue, clear, hand off, subagent, compact | The router idea matches the size router we want. The phase rule matches our short sessions | Write a GET AI router by size (T-shirt sizing). Borrow the phase-boundary order |
| `triage-issue-reports` (Benny) | One verdict per report, thread only, dedupe, create a ticket only for a clear new bug, ends with a marker line | The best built example of the outer loop. Fail-closed rules match rules 5 and 6 | Replace Slack and Linear with the ITSM tool and ADO. Keep the marker handshake and "prefer no ticket over a guessed one" |
| `reproduce-and-fix-issues` (Benny) | Waits for a trusted marker, reproduces twice through the real UI, fixes only after a confirmed repro, opens a draft PR only after before and after proof | The best example of "no confirmed repro, no fix", and of verify mode when a fix already exists | Needs a control adapter, which is `lcp-verify`. Never merge, as in rule 1. This is the closest match to the night shift's proof rule |

## Findings worth acting on

1. **`create-verification-skill` plus `maintain-verification-skill` is the template for `lcp-verify`.** Four fixed headings per feature, real selectors, proof standards, and a check that evidence survives cleanup. Use it for stage 2.
2. **`constraint-driven-development` and the Benny skills both support rule 11.** The floor is deterministic and written down. Tightening is quiet and loosening is loud.
3. **Fresh context for the checker is a shared idea.** `doubt-driven-development`, the Benny media reviewer and our verifiers all follow it. Do not pass the claim to the checker.
4. **Benny's "twice through the real UI" is a good proof standard.** It could be added to the verifier rubric (plan Appendix B).
5. **The most reusable pieces are patterns, not files.** The marker handshake, the floor guard exit codes, the TSV decision log, the agent brief template and the confidence tiers.
6. **Dropped from this batch:** nothing is rejected. `how` and `why` are the lowest priority because they are explainers for people by day.

## Decisions waiting on Boroon

- Which of the 16 to adopt as is (move to `.claude/skills/`), which to adapt into `lcp-*` skills, and which to leave on the shelf.
- Whether the dependencies in the table above (`unslop`, the `principle-*` skills, `poteto-mode`, `grilling`, `domain-modeling`) are worth reading next. Several of the 16 lean on them.
- Whether to write the router skill by size first, as `tshirt-sizing.md` step 3 suggests.
