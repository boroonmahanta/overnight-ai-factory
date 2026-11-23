---
ado_id: "90102"
lane: "B"
profile: "pcp"
ambition: "low"
work_size: "S"
design_document: "n/a: no user interface; the output is a file for another team"
design_version: "n/a: no design document"
prototype: "n/a: no user-facing screen"
---

# Feature Specification: Open orders export

**Feature Branch**: `90102-open-orders-export`

**Created**: 2026-11-24

**Status**: Draft

**Input**: User description: "The warehouse team wants a nightly list of open orders to plan the next day's picking."

## Clarifications

### Session 2026-11-24

- Q: Which orders count as open? → A: Every order not yet shipped and not cancelled.
- Confirmed shared understanding: Spec Owner, 2026-11-24

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get the open orders each morning (Priority: P1)

A warehouse planner starts the day with a list of every open order, oldest first.

**Why this priority**: Picking starts from this list every morning.

**Independent Test**: Run the export with a known set of orders and compare the list.

**Acceptance Scenarios**:

1. **AC-1**: **Given** two open orders and one shipped order, **When** the export runs, **Then** the list holds the two open orders, oldest first.
2. **AC-2**: **Given** no open orders, **When** the export runs, **Then** the list holds only its column headings.

### Edge Cases

- What happens when an order is cancelled after the export runs? It appears in that day's list and drops off the next.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST list every open order once a night, oldest first.
- **FR-002**: The list MUST show each order's number, customer and order date.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The list is ready by 6 am every working day.

## Assumptions

- None.

## Acceptance Scenario Map *(mandatory)*

| Criterion | Locked scenario IDs |
|---|---|
| AC-1 | orders-export-01 |
| AC-2 | `orders-export-02` |

## Non-Functional Requirements *(mandatory)*

- **NFR-001 Performance**: The export finishes in under five minutes for 50,000 open orders.
- **NFR-002 Accessibility**: n/a: no user interface.
- **NFR-003 Security and privacy**: Only the warehouse team can read the list.
- **NFR-004 Reliability and recovery**: A failed run is retried once, then reported to the warehouse team.
- **NFR-005 Observability**: Each run records how many orders it listed.

## Constraints

- Runs in the existing order service and writes `exports/open-orders.csv`, as the warehouse system reads today.
- Uses the service's existing scheduler; no new library.
