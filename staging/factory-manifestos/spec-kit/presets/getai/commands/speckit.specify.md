## GET AI rules for this command

These rules come from the GET AI preset (plan 6.2). Where they differ from the command below, these rules win.

1. **Facts versus decisions.** Look up every fact yourself before you write: the repo, `glossary.md`, `docs/adr/`, the ADO work item and its history, and the platform's own metadata where you can read it. Never guess a fact, and never ask the owner for one. Mark only a *decision* the owner has not made, as `[NEEDS CLARIFICATION: <the decision>]`.
2. **No cap on markers.** Ignore the command's limit of three markers and its instruction to make informed guesses for the rest. Mark every open decision. Ask the owner at most five of them in this session, the most blocking first, numbered Q1 to Q5, each with one sentence on what it decides and your recommended answer worded so "yes" accepts it. Leave the rest marked for clarify. An open marker fails the spec check, so nothing is silently assumed.
3. **Assumptions need approval.** End each line under Assumptions with `(approved: <who>, <YYYY-MM-DD>)` once the owner approves it, or `(not yet approved)` until then. An assumption that is not approved fails the spec check.
4. **Acceptance criterion IDs.** Start every acceptance scenario with an ID, numbered across the whole spec: `1. **AC-1**: **Given** ...`. Add each ID to the Acceptance Scenario Map, with `[to be written by the scenario author]` as its scenario IDs. The worker never writes its own locked scenarios.
5. **Story fields.** Fill the YAML header at the top of the spec:
   - `ado_id` from the user input or the work item; ask if neither gives it.
   - `ambition` stays `low` for client work unless the owner says otherwise.
   - `work_size` is the largest answer across reversibility, blast radius, clarity, verifiability, effort and residency, not an average.
   - `design_document` and `design_version` take the SharePoint document identity and the exact approved version identifier. A link to a Teams channel, a folder or "the latest version" is not accepted.
   - Any field that does not apply: `n/a: <reason>`.
6. **Folder name.** When the ADO ID is known, set `SPECIFY_FEATURE_DIRECTORY` to `specs/<ado-id>-<short-name>`, so the spec, the day branch and the story share the ID.
7. **What and why, not how.** Put the stack, identity, residency, solution boundaries and client integrations only under Constraints.
8. **GET AI checklist.** After the core quality checklist, run `.specify/scripts/bash/resolve-template.sh getai-checklist --json` (or the PowerShell or Python script beside it), write its `TEMPLATE_CONTENT` to `checklists/getai.md` in the feature folder and fill its header. Do not tick its items: a reviewer ticks them.
9. **Next step.** Hand off to clarify, not plan. Plan waits for the owner's written confirmation at the end of clarify.

{CORE_TEMPLATE}
