---
ado_id: "[ADO work item ID, digits only]"
lane: "[A | B]"
profile: "[lcp | pcp]"
ambition: "low"
work_size: "[XS | S | M | L | XL]"
design_document: "[SharePoint document identity: site, library and item ID; or n/a: reason]"
design_version: "[exact approved version identifier, never latest; or n/a: reason]"
prototype: "[link to the approved mock or prototype on the ADO item; or n/a: reason]"
---

{CORE_TEMPLATE}

## Acceptance Scenario Map *(mandatory)*

<!--
  GET AI. Every acceptance scenario above starts with an ID: "1. **AC-1**: **Given** ...".
  IDs run AC-1, AC-2 and so on across the whole spec. Map each one to the IDs of its
  locked scenarios (workflow scenarios, Playwright specs, Copilot Studio test sets).
  Someone other than the worker writes the locked scenarios, and @acceptance-owners
  approve them (rule 3). A criterion with no scenario ID fails the spec check.
-->

| Criterion | Locked scenario IDs |
|---|---|
| AC-1 | [to be written by the scenario author] |

## Non-Functional Requirements *(mandatory)*

<!--
  GET AI. Give each line a testable target, or write "n/a: <reason>".
  An empty section fails the spec check.
-->

- **NFR-001 Performance**: [target, or n/a: reason]
- **NFR-002 Accessibility**: [e.g. WCAG 2.2 AA on every changed screen; the journey works by keyboard alone]
- **NFR-003 Security and privacy**: [who may see and change what; no client production data in factory lanes]
- **NFR-004 Reliability and recovery**: [what happens when it fails, and how it recovers]
- **NFR-005 Observability**: [what a person must be able to see when it fails]

## Constraints

<!--
  GET AI (plan 6.6). The only place for technical design: hard constraints such as the
  stack, identity, data residency, solution boundaries or a client integration. The rest
  of this spec says what users need and why, not how. The spec check warns when a
  library, schema or file layout appears outside this section.
-->

- [Constraint, or "None"]
