# Teams-first engagement operating model

This is the agreed working convention, not a claim that the tenant is already
configured. Apply the [operating rules](operating-rules.md). The delivery method
is technology-neutral; Teams, SharePoint, ADO and GHE are the selected collaboration
and storage services, not a prescription for the solution's technology stack.

## Who owns what

| Location | Authoritative content | Not a substitute for |
|---|---|---|
| Client Team / engagement channel | Conversations and links to project resources | Approved design versions or ADO delivery records |
| Engagement SharePoint folder | Client background, curated workshop inputs, requirements documents, business-facing designs and approved deliverables | ADO acceptance criteria, work states or risk/decision registers |
| Dedicated engagement ADO project | Actionable requirements, acceptance criteria, Stories/Tasks, assignments, dependencies, states, risks, rulings, deployment and evidence references | A full document library or source repository |
| Engagement GHE build repository | Implementation specification/handoff, build artifacts and tests | Raw workshop/background document copies or the authoritative business-facing design |
| Delivery vault | Reusable skills, blank templates, rules and reviewed patterns | Any project workspace or client record store, including ignored local storage |

Requirements documents explain business context; ADO acceptance criteria define
the actionable approved outcomes to build and verify. Reconcile conflicting
content with the authorized owner rather than choosing a convenient source.

## Structure and names

Use one **internal Team per client**, with its connected SharePoint site.
Use one **standard channel per engagement**, starting in presales and retained
through delivery. Its normal Files experience uses a folder in the parent
site's default document library, not a separate library or site.

```text
Team: Northstar
  General                         Client-wide context
  Document Access                 Engagement conversation
    Files -> SharePoint folder
      Discovery                   Optional navigation folders
      Requirements
      Solution Design
      Client Deliverables
  Service Improvement             Another engagement and folder
```

The names and folders are fictitious examples. Create folders only as useful;
they are not phases, status fields or mandatory empty scaffolding.

| Resource | Naming convention | Example |
|---|---|---|
| Client Team and site display name | Recognizable client name | `Northstar` |
| Standard engagement channel and normal folder | Recognizable opportunity/project name | `Document Access` |
| Default document library | Retain the provisioned library; no project library by default | Channel folders use that library |
| ADO project | Client and engagement name, recognizable outside Teams | `Northstar - Document Access` |
| GHE build repository, when needed | Short platform-compatible client/project slug | `northstar-document-access` |
| Restricted exception Team/site | Meaningful client/project/restriction qualifier | `Northstar - Acquisition - Restricted` |

No redundant GET AI prefix or invented engagement IDs. Add a meaningful
qualifier for ambiguity. Spaces are normal in Teams/SharePoint display and folder
names; URL encoding such as `%20` is not a fault. Avoid leading/trailing spaces,
unsupported characters and unnecessarily long names. Do not create temporary
space-free names and rename them to manipulate URLs. Follow each platform's
actual naming rules and administrator policies. Record actual provisioned
URLs/IDs; never derive resource addresses from display names or promise rename
propagation. Site-address changes are separate administrator operations.

A separate library is an explicit exception for a specific management need,
not the effect of creating a standard channel. It needs provisioning, a Teams
navigation link/tab and an agreed canonical location to prevent split document
storage. Private/shared channels create separate sites and have different
membership behavior; do not use them merely as ordinary project folders.
Separate Teams/sites for access or lifecycle exceptions require admin review.

## Access and workshop inputs

Assigned account/project people participate as Team members. Ordinary internal
documents have governed GET AI-wide read access; restricted contractual or
sensitive material is excluded. Creating a Team does not establish that broad
read policy. An administrator must verify and implement permissions without
accidentally granting write access or exposing restricted content.

Keep the internal working area GET AI-only. Share approved client-facing
derivatives through a separately controlled publication area, not direct access
to internal workshop material. Verify destination, audience and approval before
publishing or linking. Folder names alone do not create security boundaries.

A named engagement owner curates workshop notes, recordings, transcripts and
supporting documents. Check consent, permitted use, access, retention and
completeness before exposing them as inputs. Verify where meeting artifacts
actually land; do not assume Teams automatically files them in the engagement
folder. Use approved references or authorized targeted moves/copies as needed,
not indiscriminate replication. Never bulk-copy them into ADO, GHE or the vault.

## Onboarding and workspaces

1. The engagement owner requests/creates the client Team and standard channel
   through the approved administrative process, reusing suitable existing
   resources. Capture the actual connected site/folder and assigned owners.
2. Request a **dedicated ADO project per engagement/channel**. Do not share a
   client backlog across engagements. Adopt an existing correct project if
   provided; setup does not create projects, teams, processes or permissions.
   Missing resources become an administrator handoff, not automatic provisioning.
3. Open a separate authorized engagement working folder/session from presales.
   Keep local connection metadata there, outside the vault. Explicitly load
   the reusable kit and verify per-interface Teams/SharePoint/ADO access. A
   source repository is not required for discovery or design.
4. Work from relevant authorized SharePoint inputs and ADO records. Draft the
   business-facing design for SharePoint using its approved authoring format.
   Obtain scoped approval for any upload/edit and verify the saved result;
   local drafts outside the vault are not saved SharePoint documents.
5. Once implementation is authorized, request/reuse the engagement GHE repository
   and authorize its source checkout. Default to one repository per engagement,
   with explicit exceptions for an existing product or independently deployed
   components. Do not create unused ADO Repos for project documents.

Creating a Team/channel triggers this **human checklist**, not a workflow engine.
The kit provisions nothing and opens no other sessions automatically. Repository
creation, commits, pushes, access changes and deployment need separate approval.

## Design approval and build contract

SharePoint holds the authoritative business-facing solution design. Verify its
actual versioning/retention capabilities and that the exact approved content
remains readable to the builder. Record document identity/link, exact version
identifier, approver, approval evidence and the relevant ruling on the appropriate
ADO item through an approved batch. Approval through Teams or another review
channel must identify the exact content; an unqualified "looks good" is not
sufficient. Do not invent a version URL or assume a latest-document link is pinned.

The GHE implementation specification/handoff references that exact SharePoint
version and the engagement's actual ADO scope; it adds technical execution detail,
not a competing business design. Version it alongside the build under authorized
Git operations. Before transfer, identify its precise content/revision and verify
audience access; an unpublished local path alone is not a durable shared handoff.

If approved-version access cannot be verified or preserved, the affected handoff
is not-ready: resolve with the document owner rather than using the latest draft.
A later SharePoint edit does not silently change approved scope. Design drift
requires design approval and coverage/backlog review before affected work resumes.
Do not duplicate the full design in Stories/Tasks or synchronize raw inputs into
source. Acceptance criteria and relevant Context/Options/Ruling/Reason stay in ADO.

## Product behavior references

Official references used for this structure; tenant configuration remains to
be verified:

- [Teams and SharePoint integration](https://learn.microsoft.com/en-us/sharepoint/teams-connected-sites)
- [Standard channels](https://learn.microsoft.com/en-us/microsoftteams/standard-channels)
- [Additional document-library tabs](https://learn.microsoft.com/en-us/graph/teams-configuring-builtin-tabs#document-library-tabs)
- [URL path encoding](https://learn.microsoft.com/en-us/graph/onedrive-addressing-driveitems#path-encoding)
- [Separate site-address changes](https://learn.microsoft.com/en-us/sharepoint/change-site-address)
