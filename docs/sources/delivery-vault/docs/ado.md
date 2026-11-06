# ADO integration and bookkeeping

Apply the [operating rules](operating-rules.md). This guide defines an integration
contract, not an assumed connector or custom ADO process.

Use one dedicated ADO project per engagement, mapped to its Teams channel and
SharePoint folder. Do not mix engagements into a client-wide backlog or create
ADO Repos to hold workshop documents. Project provisioning is an explicit
administrator handoff; setup only verifies existing resources.

## Discover before proposing changes

Use the engagement's explicit organization URL and project on every operation.
Verify current ADO identity, project/team visibility, areas and iterations,
work item types, actual backlog hierarchy, fields, allowed values, required and
conditional rules, relation types and state transitions. Discover existing
tags and sections before introducing labels. If rules cannot be inspected,
mark that capability unknown and resolve the prerequisite before writing.

Search narrowly for existing Epics/Features by approved scope and identifiers;
also inspect linked and matching Stories/Tasks to avoid duplicates. Show
ambiguous matches to the user. Reuse an existing appropriate parent; propose a
new Epic/Feature only when needed or explicitly chosen, then obtain approval.
Tasks go under Stories, Stories under Features, where the discovered process
supports that hierarchy. Adapt actual type names (for example User Story);
do not impose those names on another process.

Use existing fields, sections and suitable tags. Do not create custom work item
types. No universal Decision type or state progression is assumed. Do not
mislabel a Review as a Decision. Conditional field values, defaults and state
names are not business policy.

## Read and write tools

Use only a locally verified integration. The Windows app's ADO CLI read path
has been verified; writes and VS Code remain unverified. A dedicated ADO MCP
is not assumed. If the approved Azure CLI path is available, check local help
and extension capabilities before using it. Read examples with placeholders:

```powershell
az boards work-item show --id <confirmed-id> --org <organization-url>
az boards query --org <organization-url> --project <project> --wiql <approved-query>
```

These are illustrative, not commands to run verbatim. Where a command lacks
`--project`, resolve its ID to the confirmed project and verify the returned
`System.TeamProject`. Always check the returned scope. Some metadata may require
approved REST reads or administrator input instead of the boards command.

Do not print credentials, use token-bearing URLs, change shared CLI defaults,
log out shared users or broaden scopes for convenience. Authentication/access
failure is not an empty query. Ask for the appropriate interface's supported
sign-in path; do not assume Windows app and VS Code authentication is shared.
Never probe writes by creating unsolicited test records.

## Scoped mutation contract

Before approval, present a [coverage review](../templates/backlog-coverage-review.md)
and a batch with operation, existing ID or proposed title, type, project, parent,
fields/relations, expected revision, readiness and verification method.
Identify and record dependencies and ordering first; the batch stays conditional
until existing parents and child work have been searched.
Include only authorized state changes and assignments. Unresolved prerequisites
are not-ready; do not start their dependent implementation. Any proposal to
create blocked planning items must disclose those gaps for explicit approval.

After approval, execute prerequisite operations first. Capture returned IDs;
read back each created/changed item, parent/dependency relations, fields, state
and revision. Verify effects rather than trusting an exit code. Use supported
revision preconditions for updates; if unavailable, re-read immediately before
writing and stop on differences. Do not claim atomicity across a batch.

On timeout or partial success, use known IDs and a narrow duplicate search to
determine what happened. Do not retry an uncertain create until resolved.
Stop on conflict, scope change, auth or hook failure. Report verified successes,
failed/unknown operations and the next safe action. Resume missing work only
if the original approval still covers it; otherwise seek revised approval.

## Decisions, risks and evidence

Record a decision on its relevant work item using **Context / Options / Ruling /
Reason**, identifying the authorized decision maker. A proposal is not a ruling.
Use a separate linked suitable Issue only if an independent lifecycle is needed
and approved. Discover the actual Risk type and fields when applicable; do not
invent likelihood scales, ratings, defaults or risk acceptance.

Keep actionable requirements, acceptance criteria and delivery state in ADO.
Supporting requirements documents and business-facing designs remain in SharePoint.
Record the exact approved SharePoint document identity/version, approver and
approval-evidence reference on the relevant item; a latest-document link alone
is not a pinned design. Do not paste the whole design into Stories/Tasks.
The implementation specification/handoff lives in the engagement GHE repository
and references the approved version and ADO scope. Check drift between these
sources before writing or building. Evidence identifies what ran,
where, against which source/environment revision, the observed result and any
limitations. Use authorized evidence locations and audiences; do not paste raw
logs or private vault paths into client-visible items. Deployment and acceptance
records stay in ADO; a passing test does not itself authorize deployment or Done.
