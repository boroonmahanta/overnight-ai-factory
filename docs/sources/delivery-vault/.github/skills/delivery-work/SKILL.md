---
name: delivery-work
description: Work on a delivery requirement or ADO item through design approval, coverage-checked backlog proposal and separately authorized build handoff. Use for work on this, solution design, backlog review or resuming delivery.
---

# Work on this

Read the [operating rules](../../../docs/operating-rules.md),
[operating model](../../../docs/operating-model.md),
[ADO guide](../../../docs/ado.md) and relevant
[standards](../../../docs/standards-and-patterns.md).

1. Confirm a separate authorized engagement workspace, not the vault checkout,
   with this kit explicitly readable. Confirm scope, dedicated ADO project and
   item/requirements, Teams/SharePoint connections and audience. Read relevant
   curated SharePoint inputs, the exact approved design if one exists, and
   targeted current source when available. A source repo is optional in presales.
   Assess freshness before requesting a necessary approved read/export refresh.
2. Design first using the [solution design template](../../../templates/solution-design.md).
   Resolve outcomes, boundaries, alternatives, access, failure/recovery and
   verification. The authoritative business-facing design belongs in SharePoint;
   draft outside the vault and obtain scoped approval for uploads/edits, then
   verify saved content/version. Report unsaved drafts explicitly if that
   integration is unavailable. Seek explicit approval for the exact design
   version before backlog creation or implementation. Record its identity,
   version, approver and approval evidence in ADO only through approved changes.
   Existing designs require confirmed version, scope and continued suitability.
3. Search existing Epic/Feature and child work. Present ambiguous parents for
   choice; prefer reuse. Use the
   [coverage review](../../../templates/backlog-coverage-review.md) to map every
   approved outcome to Story/Task coverage and independent verification.
   Include real dependencies and disclose not-ready gaps.
4. Present exact proposed ADO operations/fields/relations and obtain scoped
   batch approval, including any needed new parent. Execute in dependency
   order and read back every mutation. Stop and reconcile partial/uncertain
   results by known IDs and narrow searches; no blanket retries or deletion.
5. Prepare the [implementation specification/handoff](../../../templates/build-handoff.md)
   in the authorized engagement GHE repository, referencing the exact approved
   SharePoint design version and actual ADO IDs. Add execution detail, not a
   competing design or raw background copies. Hand missing repository
   provisioning to its owner; default to one per engagement with explicit
   product/component exceptions. Get explicit authorization for the separate
   source checkout and verify readable handoff revision, design version,
   approval evidence and prerequisites there before building. Git operations
   remain separately authorized; do not create project files in this vault.
6. In that authorized workspace, follow its conventions and the handoff, run
   relevant checks and capture verified evidence. Design drift returns to
   approval and coverage review. Live changes and completion remain explicit
   approvals; use [wrap-up](../delivery-wrap-up/SKILL.md) for closing bookkeeping.

If work resumes after interruption, re-read ADO recovery context, known IDs,
current revisions and unfinished changes before proposing the next operation.
If no approval or ready scope exists, return the precise blocker, not a
success-shaped fallback.
