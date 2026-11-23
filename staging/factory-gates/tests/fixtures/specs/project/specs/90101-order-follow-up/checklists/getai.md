# GET AI Checklist: Order follow-up date

**Purpose**: Check the spec meets the GET AI day gate before it can be Factory Eligible
**Created**: 2026-11-24
**Feature**: [spec.md](../spec.md)

**Review Ownership**: A reviewer ticks these items, never the agent that wrote the spec (plan 6.1). Mark an item `[x]` only when the reviewer finds it satisfied.
**Marker Semantics**: `[x]` means reviewed and satisfied. It does not mean the build is done. An unticked item fails the spec check.

## Decisions and facts

- [x] CHK001 No `[NEEDS CLARIFICATION]` marker is left; every decision is answered by the owner in Clarifications
- [x] CHK002 Every assumption is marked `(approved: <who>, <date>)`
- [x] CHK003 Nothing in the spec is a guessed fact: facts were looked up, and their sources are named
- [x] CHK004 The owner confirmed a shared understanding in writing (the last bullet of a Clarifications session)

## Acceptance

- [x] CHK005 Every acceptance scenario has an `AC-<n>` ID
- [x] CHK006 Every `AC-<n>` maps to at least one locked scenario ID in the Acceptance Scenario Map
- [x] CHK007 The locked scenarios are written by someone other than the worker and approved by `@acceptance-owners`

## Quality and scope

- [x] CHK008 Every NFR line has a testable target or "n/a" with a reason
- [x] CHK009 Technical design appears only in Constraints (plan 6.6)
- [x] CHK010 Ambition is low for client work, or the owner chose otherwise in writing
- [x] CHK011 The work size is the largest answer across reversibility, blast radius, clarity, verifiability, effort and residency

## Design and records

- [x] CHK012 The design fields give the SharePoint document identity and the exact approved version, not a channel link or the latest version
- [x] CHK013 A user-facing change links an approved mock or throwaway prototype (rule 10), and nothing from a prototype is promoted
- [x] CHK014 New business terms are in `glossary.md`, each with its `_Schema_` line
- [x] CHK015 Each decision that is hard to reverse, surprising and a real trade-off has a record in `docs/adr/`

## Data

- [x] CHK016 No client production data, secret or personal detail appears in the spec, its examples or its scenarios

## Traceability

- [x] CHK017 The spec's `ado_id`, its folder (`specs/<ado-id>-<short-name>`) and its day branch carry the same ADO work item ID; no Spec Kit numbered or timestamped folder

## Notes

- `__SPECKIT_COMMAND_IMPLEMENT__` reads checklist state as a gate and must not change markers
- Add findings inline under the item
