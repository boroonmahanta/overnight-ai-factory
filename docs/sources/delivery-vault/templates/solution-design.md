# Solution design: `<title>`

Use this reusable outline in the approved SharePoint authoring format. Project
drafts belong in the engagement workspace until saved through an approved
document operation, never in the vault. Do not duplicate the whole design in ADO
or the build repository.

- Client/engagement and audience approval:
- SharePoint document identity/link and exact version: `<verify actual version access>`
- Requirement references: `<ADO IDs/links; acceptance criteria remain there>`
- Source/doc references: `<targeted paths/revisions, freshness and access checked>`

## Outcomes and boundaries

Describe independently verifiable outcomes, in/out of scope, constraints,
ownership and trust boundaries. Distinguish confirmed requirements from
assumptions requiring a business ruling.

## Proposed solution

Describe components, interfaces, data flow, access model, environments,
credential references and source mapping. No secrets or raw data.
Explain alternatives, tradeoffs, failure behavior, recovery and compatibility.
Include technology-specific guidance only where relevant.

## Verification and release approach

Map outcomes to observable checks, including negative paths, permissions and
recovery as relevant. Describe test environments, authorized evidence location,
deployment prerequisites, rollback feasibility and required documentation.
Live-system changes and completion remain separately approved.

## Prerequisites and design approval

- Unresolved prerequisites and affected outcomes: `<not-ready; relevant ADO links>`
- Decision/risk references: `<ADO only, not a duplicate register>`
- Design approval: `<authorized approver, date, exact SharePoint version and evidence>`
- ADO approval/ruling reference: `<relevant engagement item; authorized update verified>`
- Coverage review reference: `<bounded review; no copied delivery state>`

Approval attaches to the exact reviewed SharePoint content/version, not the
latest-document link. Verify the approved version remains readable by the builder.
The fields above identify the approval context; keep the authoritative approval
record in ADO. Do not edit an approved document merely to stamp its approval,
thereby creating an unreviewed new version.
The GHE implementation specification/handoff references it and adds execution
detail without becoming a competing design. Material changes return to approval
and backlog coverage review; a new draft does not silently replace approved scope.
