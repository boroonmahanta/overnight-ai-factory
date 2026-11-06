# Implementation specification / build handoff: `<approved scope>`

This transfers authorized context, not blanket permission. Do not begin build
until the design revision and ADO records are readable and authorized from the
destination workspace.

Complete this outline in the engagement GHE repository under authorized Git
operations, never in the vault. Default to one repository per engagement, with
explicit product/component exceptions. It contains execution detail, not copies
of workshop inputs or the authoritative business-facing design.

## Contract

- Client/engagement; authorized builder and audience:
- Handoff identity/revision: `<repository, path and precise reviewed content; immutable revision for transfer>`
- SharePoint design: `<document identity/link and exact approved version, not latest only>`
- Exact design approval: `<ADO reference, approver and verifiable approval evidence>`
- Approved-version access: `<verified readable and preserved for the builder; otherwise not-ready>`
- Coverage review: `<revision and path, if retained>`
- ADO organization/dedicated engagement project and scoped Story/Task IDs:
- Current acceptance criteria, dependencies and readiness: `<read in ADO; do not copy status>`
- Build authorization: `<scope, authorized source repository/workspace, approval reference>`
- Source baseline: `<repository and revision; private local mappings kept local>`
- Relevant shared instructions: `<readable revision-pinned resources>`

## Execution and verification

- Environments, purposes and credential-store references: `<no secrets>`
- Relevant constraints, interfaces and approved technology guidance:
- Technical execution detail: `<components, contracts and task mapping; consistent with the approved design>`
- Targeted SharePoint/source freshness checks or approved refresh required:
- Checks to run and observable outcomes:
- Authorized evidence location/audience; ADO records to update:
- Deployment prerequisites and separate live-change approval:
- Stop conditions: `<design drift, unreadable revision, conflict, failed prerequisite>`

## Resume entry

- Durable ADO recovery reference and known IDs, if resuming:
- Re-read design, current ADO records/relations and local unfinished changes:
- Compare the approved SharePoint version with later drafts: `<do not silently adopt new scope>`
- Verify uncertain writes before retry; execute only missing still-approved operations:
- If drift, ambiguity or missing access remains: `<not-ready; approval/admin action needed>`

Keep curated background documents and the authoritative business-facing design
in SharePoint; do not bulk-copy them into source. Check audience access before
adding any internal reference to a client-visible destination. If necessary,
request an approved readable derivative without silently changing the approved
design/version. Keep subsequent state, decisions and evidence in ADO.
