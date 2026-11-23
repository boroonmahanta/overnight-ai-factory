---
ado_id: "90101"
lane: "B"
profile: "lcp"
ambition: "low"
work_size: "S"
design_document: "SharePoint site factory-samples, library Designs, item ID 1042"
design_version: "3.0"
prototype: "n/a: one new column on an existing form and view, with no new screen"
---

<!-- Fixture for check_spec.py, stage 1 exit clause (plan 11.2): a spec with no scenarios cannot become Factory Eligible. The good lcp spec with its Acceptance Scenario Map as specify leaves it, before the scenario author writes the locked scenarios; everything else passes. -->

# Feature Specification: Order follow-up date

**Feature Branch**: `90101-order-follow-up`

**Created**: 2026-11-24

**Status**: Draft

**Input**: User description: "Sales staff want each open order to show when they should next contact the customer about it."

## Clarifications

### Session 2026-11-24

- Q: How many days after the order date is the follow-up due? → A: Seven days.
- Q: Does a shipped order keep its follow-up date? → A: No, it is cleared when the order ships.
- Confirmed shared understanding: Spec Owner, 2026-11-24

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  This comment is left from the template, as specify leaves it. The check ignores
  comments: [a bracketed placeholder] and - [ ] an unticked box here do not count.
-->

### User Story 1 - See when to follow up an order (Priority: P1)

A salesperson opens an open order and sees the date by which they should contact the customer.

**Why this priority**: Orders go quiet without a reminder, and a late order costs repeat business.

**Independent Test**: Create an open order and check the follow-up date shown on it.

**Acceptance Scenarios**:

1. **AC-1**: **Given** a new open order dated 1 March, **When** it is saved, **Then** its follow-up date is 8 March.
2. **AC-2**: **Given** an open order with a follow-up date, **When** it is marked shipped, **Then** its follow-up date is cleared.

---

### User Story 2 - Find the orders due for follow-up (Priority: P2)

A salesperson lists the open orders whose follow-up date has passed.

**Why this priority**: It turns the date into a daily work list.

**Independent Test**: Create three open orders, one past its follow-up date, and open the list.

**Acceptance Scenarios**:

1. **AC-3**: **Given** three open orders, one past its follow-up date, **When** the salesperson opens the orders due for follow-up, **Then** only that one is listed.

---

### Edge Cases

- What happens when an order has no order date? It gets no follow-up date.
- How does the system handle an order shipped on the day it is created? Its follow-up date is cleared.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST set an open order's follow-up date to seven days after its order date.
- **FR-002**: The system MUST clear the follow-up date when the order ships.
- **FR-003**: Salespeople MUST be able to list the open orders whose follow-up date has passed.

### Key Entities

- **Order**: a customer's order, with its order date, its shipped date and the new follow-up date.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every open order saved after release shows a follow-up date.
- **SC-002**: A salesperson finds the orders due for follow-up in under 30 seconds.

## Assumptions

- Salespeople can already read every order they work on (approved: Spec Owner, 2026-11-24)
- Weekends and public holidays count as days
  when the follow-up date is worked out (approved: Spec Owner, 2026-11-24)

## Acceptance Scenario Map *(mandatory)*

<!--
  GET AI. Every acceptance scenario above starts with an ID: "1. **AC-1**: **Given** ...".
  A criterion with no scenario ID fails the spec check.
-->

| Criterion | Locked scenario IDs |
|---|---|
| AC-1 | [to be written by the scenario author] |
| AC-2 | [to be written by the scenario author] |
| AC-3 | [to be written by the scenario author] |

## Non-Functional Requirements *(mandatory)*

<!--
  GET AI. Give each line a testable target, or write "n/a: <reason>".
  An empty section fails the spec check.
-->

- **NFR-001 Performance**: The follow-up date is set within one minute of saving the order.
- **NFR-002 Accessibility**: WCAG 2.2 AA on the changed form and view; the journey works by keyboard alone.
- **NFR-003 Security and privacy**: Only people who can read an order see its follow-up date; no client production data in factory lanes.
- **NFR-004 Reliability and recovery**: If setting the date fails, the order still saves, and the failed run waits for a person to run it again.
- **NFR-005 Observability**: n/a: the platform's own run history shows each failed run, and nothing more is needed.

## Constraints

<!--
  GET AI (plan 6.6). The only place for technical design.
-->

- The change stays inside the Sample Orders solution, publisher prefix `smpl`, in `src/Entities/smpl_order/`.
- A cloud flow sets the column, not a plug-in.

## Low-Code Fields *(mandatory for profile lcp)*

<!--
  GET AI low-code (plan 6.3). Fill every field, or write "Not applicable: <reason>".
  An empty field or a bracketed placeholder fails the spec check.
-->

### Solution boundaries

Sample Orders solution, publisher prefix `smpl`. This story adds no new solution.

### Data model intent

One new date column on the Order table, the follow-up date. Additive: no existing data changes, so it is a two-way door.

### Connection references

One, `smpl_DataverseOrders`: the Dataverse connector, with the lane's existing service principal connection. No OAuth consent.

### Environment variables and values per environment

| Name | Type | Lane | Test | UAT | Prod |
|---|---|---|---|---|---|
| smpl_FollowUpDays | Number | 7 | 7 | 7 | 7 |
| smpl_DataverseOrders (connection reference) | Dataverse | lane connection | Test connection | UAT connection | Prod connection |

The number of days is the same everywhere, so its default value is 7.

### Names

- Column `smpl_followupdate`, display name "Follow-up date" (standard NM-03)
- Flow "Set order follow-up date" (standard FL-01)
- View "Orders due for follow-up" (standard NM-07)
- Environment variable `smpl_FollowUpDays` (standard EV-02)

### Reference components

The existing flow "Set order status" in the same solution, for its trigger and error handling.

### Inventory check

Read the solution inventory on 2026-11-24: no existing column, flow or view holds a follow-up date.

### Open questions

**We can answer** (facts the team looks up): none

**Ask the client** (decisions): none; both were answered in Clarifications.

### Security roles

None change.

### Design-first mock or prototype

Not applicable: one new column on an existing form and view, with no new screen.

### Testability contract

Column `smpl_followupdate`; flow "Set order follow-up date"; view "Orders due for follow-up"; form label "Follow-up date".

### Verify profile change

Add the view "Orders due for follow-up" as a journey.

### Glossary terms

Follow-up date: `smpl_followupdate` on Order.

### Copilot Studio agent

Not applicable: no agent changes.

### Residency tier

T2.

### Licence impact

One premium flow (the Dataverse connector), owned by the lane identity, which already holds the licence.

### Kind of change to a model-driven app

An additive change to an existing app: a column on an existing table, shown on an existing form and view.
