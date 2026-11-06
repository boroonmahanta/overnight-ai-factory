# Delivery vault

Internal, technology-neutral delivery skills and documentation. GitHub Copilot
in the Windows app and in VS Code are equally supported interfaces; neither is
the primary workflow. Other assistants can follow the same operating rules.

**This repository is the reusable operating kit, not a project workspace.**
It holds skills, templates, rules and reviewed patterns only. No project-specific
connections, designs, handoffs, client material or project scratch files belong
here, even in ignored folders. Fictitious examples demonstrate the workflow.

| System | Authoritative purpose |
|---|---|
| Teams | Client and engagement conversations; onboarding front door |
| SharePoint | Background documents, curated workshop inputs and business-facing solution designs |
| ADO Boards | One project per engagement; actionable requirements, acceptance criteria, work, decisions, risks and evidence |
| Engagement GHE repository | Implementation specification/handoff, build artifacts and tests |
| Delivery vault | Reusable guidance only |

See the [agreed operating model](docs/operating-model.md) for naming, access,
provisioning handoffs and document ownership.

## Quick start

New to the team? Follow the [onboarding guide](docs/onboarding.md); it uses
[machine setup](docs/machine-setup.md) to prepare your computer.

1. Start with the approved client Team and engagement standard channel.
   Request missing resources through the administrator; channel creation is
   not an infrastructure automation trigger.
2. Open a **separate engagement working folder/session** in either interface,
   from presales onward. Load this kit explicitly as described below, then ask
   **"Set up this engagement"** with the Teams/SharePoint and dedicated ADO
   project references. Keep the [connection record](templates/engagement-connection.md)
   in that engagement workspace, never this checkout. A source repository is
   optional during presales.
3. Use **"Start my day"**, **"Work on this <ADO reference>"**, or **"Wrap up"**.
   Design comes before backlog creation or implementation.
4. Approve the exact SharePoint design version, then a coverage-checked, scoped
   ADO batch. Before implementation, authorize a separate GHE source checkout
   and its implementation specification/handoff referencing that design version.
   Each mutation is verified; approvals are not blanket permission.

| Conversation | Skill adapter | Result |
|---|---|---|
| Setup / onboard | [delivery-setup](.github/skills/delivery-setup/SKILL.md) | Confirmed connections, identity and capability limits |
| Start my day | [delivery-day](.github/skills/delivery-day/SKILL.md) | Current assigned work and suggested next focus |
| Work on this | [delivery-work](.github/skills/delivery-work/SKILL.md) | Design, approved backlog scope, then authorized build |
| Wrap up | [delivery-wrap-up](.github/skills/delivery-wrap-up/SKILL.md) | Verified ADO evidence and explicit next action |

## Loading skills in either interface

Project adapters use `.github/skills/<name>/SKILL.md` with `name` and
`description` YAML frontmatter. `AGENTS.md` points to the common rules;
`.github/copilot-instructions.md` is the Copilot repository-instructions bridge.
These files do not grant permissions or install integrations.

**Current supported workflow: explicit manual loading.** A Windows app dry run
from a separate engagement folder did not discover the four skills; manual
reading worked. In VS Code, discovery from a separate folder is unverified. No
automatic discovery is promised from any other folder in either interface.

For project work, open the **engagement folder**, not the vault checkout.
Explicitly attach/open the intended `SKILL.md` from a readable, authorized kit
checkout and ask Copilot to read its linked rules and templates. Use an
interface-supported skill-loading mechanism only after reviewing and verifying
it. Confirm the session
can read those resources without changing its working folder to the vault.
If cross-folder reads are unavailable, request an approved readable distribution
of the reusable kit that preserves its resource links. Do not assume an
installation mechanism exists or silently change global settings.

Use the available skill picker/invocation mechanism, or ask by name. Do not
assume slash commands or automatic phrase-based discovery in every version.
Copying an adapter alone breaks its relative references. Opening an engagement
folder or source repository does not automatically load this vault's skills.
The source session also needs the approved handoff and relevant readable rules;
it does not inherit another conversation. Never copy client context into the
vault or internal material into client source just to make discovery work.

### Capability checks, not assumed parity

For **each interface and engagement**, verify skill loading, Teams/SharePoint
reads and exact document-version access, ADO identity/read access, and GHE/source
and technology tools when needed. Record capability, scope, date, evidence
reference and limitations in the connection record outside the vault. SharePoint
document writes and ADO writes require scoped approval and read-back; test only
through approved real operations, not unsolicited probe changes.

Current foundation baseline: Windows app GHE and ADO CLI reads were verified
during onboarding; ADO writes are untested. VS Code verification is deferred to
a teammate and does not block authoring this kit. Skill discovery for these new
adapters has not been verified across all four skills/interfaces; explicit
loading of `delivery-work` in the authoring session does not prove automatic
selection in an engagement session. Teams/SharePoint integrations, document
write/version access and the tenant access model remain unverified. No dedicated
ADO MCP is assumed. Inherited organization rules remain unverified due to token
scope; do not broaden permissions merely to inspect them.

## Reference map

- [ADO integration and bookkeeping](docs/ado.md)
- [Teams, SharePoint and project workspace model](docs/operating-model.md)
- [Reusable standards and candidate patterns](docs/standards-and-patterns.md)
- [Fictitious walkthrough, coverage matrix and resume example](docs/walkthrough.md)
- Templates: [connection](templates/engagement-connection.md),
  [solution design](templates/solution-design.md),
  [build handoff](templates/build-handoff.md),
  [backlog coverage review](templates/backlog-coverage-review.md)

Templates are blank reusable outlines, not permission to create project records
here. Use the solution-design outline in the approved SharePoint authoring
format; use the build-handoff outline in the engagement build repository. A
bounded coverage proposal belongs in the engagement conversation or approved
project location, not the vault. Do not create Markdown status, risk, decision,
deployment, worklog or timesheet registers. ADO remains the delivery tracker.

## Maintaining the kit

Propose shared rule or standard changes through a human-reviewed PR; an agent
cannot approve its own change. An observed lesson is only a candidate until
reviewed. Publication, commits and pushes require explicit authorization; this
initial kit is local and unpublished. Verify actual repository rules before
publication; admin capability is not policy approval.

No dependencies, scripts or CI are required. Review all changed and untracked
documents, resolve relative links, inspect skill frontmatter, and run
`git diff --check` (also check new files) before handing changes back.

Official references consulted 2026-10-30:
[agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills),
[creating skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills),
[repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions),
[app customization](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app).
Documented support is not proof of local integration behavior.
