## GET AI rules for this command

These rules come from the GET AI preset (plan 6.2). Where they differ from the command below, these rules win.

1. **Facts versus decisions.** Look up every fact yourself before you write: the repo, `glossary.md`, `docs/adr/`, the ADO work item and its history, and the platform's own metadata where you can read it. Never guess a fact, and never ask the owner for one. Mark only a *decision* the owner has not made, as `[NEEDS CLARIFICATION: <the decision>]`.
2. **No cap on markers.** Ignore the command's limit of three markers and its instruction to make informed guesses for the rest. Mark every open decision. Ask the owner at most five of them in this session, the most blocking first, numbered Q1 to Q5, each with one sentence on what it decides and your recommended answer worded so "yes" accepts it. Leave the rest marked for clarify. An open marker fails the spec check, so nothing is silently assumed.
3. **Assumptions need approval.** End each line under Assumptions with `(approved: <who>, <YYYY-MM-DD>)` once the owner approves it, or `(not yet approved)` until then. An assumption that is not approved fails the spec check.
4. **Acceptance criterion IDs.** Start every acceptance scenario with an ID, numbered across the whole spec: `1. **AC-1**: **Given** ...`. Add each ID to the Acceptance Scenario Map, with `[to be written by the scenario author]` as its scenario IDs. The worker never writes its own locked scenarios.
5. **ADO ID first, before anything else.** Every spec belongs to one ADO work item, and its ID names everything.
   - Take the ID from the user input. If none is given, search the engagement's ADO project for the story by its title and description, and confirm the match with the owner. Ask the owner only if you cannot search ADO.
   - If no work item exists, create one before you write anything: a User Story in the engagement's ADO project, titled from the feature description. Find the project from the repo (its project manifest, or the ADO project its existing specs and pull requests name); ask the owner only if the repo does not say. Show the owner the project and title, create it once they agree (through the Azure DevOps tools you have, or `az boards work-item create`), and use the new ID.
   - If no ID can be found or created, **stop**. Never fall back to Spec Kit's own numbering (`001-`, `002-` or a timestamp), and never write a spec without an ID.
6. **Story fields.** Fill the YAML header at the top of the spec:
   - `ado_id` is the ID from rule 5, digits only.
   - `ambition` stays `low` for client work unless the owner says otherwise.
   - `work_size` is the largest answer across reversibility, blast radius, clarity, verifiability, effort and residency, not an average.
   - `design_document` and `design_version` take the SharePoint document identity and the exact approved version identifier. A link to a Teams channel, a folder or "the latest version" is not accepted.
   - Any field that does not apply: `n/a: <reason>`.
7. **Folder name.** Always set `SPECIFY_FEATURE_DIRECTORY` to `specs/<ado-id>-<short-name>` yourself, so the command never auto-generates a numbered or timestamped folder. The spec, the day branch (`<ado-id>-<slug>`) and the story share the ID.
8. **What and why, not how.** Put the stack, identity, residency, solution boundaries and client integrations only under Constraints.
9. **GET AI checklist.** After the core quality checklist, run `.specify/scripts/bash/resolve-template.sh getai-checklist --json` (or the PowerShell or Python script beside it), write its `TEMPLATE_CONTENT` to `checklists/getai.md` in the feature folder and fill its header. Do not tick its items: a reviewer ticks them.
10. **Next step.** Hand off to clarify, not plan. Plan waits for the owner's written confirmation at the end of clarify.

{CORE_TEMPLATE}
