
<!--
  GET AI low-code. This replaces the core source-tree section. The solution source is
  the driver's export in the XML layout, and the build never edits exported files, so
  there is no source tree to design. The sections below are the delivery vault's
  solution design and build handoff, with the least change. Write so someone who was
  not in the requirement conversation could build from it. Delete a subsection that
  truly does not apply rather than leave it empty.
-->

### Scope

| Component | New or existing | Notes |
|---|---|---|
| [table, column, flow, app, environment variable, connection reference, role] | [new or existing] | [notes] |

Check the inventory first: never propose a new table, flow or screen without confirming nothing already does the job.

### Design

[For a flow: the trigger, the actions in order, error handling, what it calls and what calls it. For an app: screens, controls, data sources, the change in behaviour. Name every new component now, to the coding standards, citing each standard ID]

### Alternatives and trade-offs

[The options considered, and why this one. A fork found while writing is a decision for the owner, not buried here]

### Failure and recovery

[What happens when each step fails, how it recovers, and whether the change can be rolled back (a one-way or two-way door)]

### Access

[Security roles and privilege depth; who can see and change what; the identities that run it. No secrets]

### Environment variables and connection references

[From the spec's values table. A new child-flow call needs its URI variable, with a value per environment and no default]

### Data model changes

[Tables and columns added or changed, by schema name]

### Verification and release approach

[Map each `AC-<n>` to the observable check that proves it, including negative paths, permissions and recovery. Test environment, evidence location, deployment prerequisites, rollback]

### Build handoff

- Solutions touched: [names]
- ADO story: [ID and link]
- Design: [SharePoint document identity and exact approved version, from the spec header]
- For the build session: [one or two sentences]
- Stop conditions: [design drift, an unreadable design version, a failed prerequisite, a decision the spec does not settle; a night agent parks on any of them]

### Status

- Design complete, with no open client questions: [yes or no]
- Reviewed against the coding standards: [yes or no]
- Ready for build: [yes or no]

