---
name: delivery-day
description: Start the delivery day by reading connected engagements, the current person's assigned ADO work and unfinished local changes. Use for start my day or choosing the next focus.
---

# Start my day

Run outside the vault checkout, with the kit explicitly readable. Read the
[operating rules](../../../docs/operating-rules.md) and configured connection
records in authorized engagement workspaces, never stored in the vault. Use the
[ADO guide](../../../docs/ado.md) for queries.

1. Confirm the current person's ADO identity and configured connected
   engagements and their dedicated ADO projects; do not search every accessible
   project or assume one roster. Cross-engagement reads need explicit configured
   scope; a single engagement workspace does not imply access to all others.
2. Read current assigned work, relevant parents, acceptance criteria,
   dependencies, blockers and next actions using each project's actual process.
   Refresh stale context with targeted reads; separate denied/unavailable
   scopes from successful empty queries.
3. Inspect unfinished engagement drafts and relevant source changes only in
   confirmed authorized workspaces; a source repo may not exist during presales.
   Check relevant SharePoint design/approval references when needed. Work
   without switching branches, stashing or discarding changes.
   Relate changes to ADO items where evidence supports it; label unknown
   associations.
4. Suggest a focus based on readiness, dependencies, explicit priorities and
   unfinished work. Explain uncertainty and ask the user to choose if ambiguous.
   Do not silently reprioritize, assign, transition or create records.

Return a concise current view with ADO references and one suggested next action.
Keep it conversational, not a Markdown daily register. A selected item enters
[delivery-work](../delivery-work/SKILL.md); selecting focus is not write approval.
