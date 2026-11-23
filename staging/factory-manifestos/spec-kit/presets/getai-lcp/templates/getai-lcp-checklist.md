# Low-Code Checklist: [FEATURE NAME]

**Purpose**: Check the low-code fields before the spec can be Factory Eligible (plan 6.3)
**Created**: [DATE]
**Feature**: [Link to spec.md]

**Review Ownership**: A reviewer ticks these items, never the agent that wrote the spec (plan 6.1). Mark an item `[x]` only when the reviewer finds it satisfied.
**Marker Semantics**: `[x]` means reviewed and satisfied. It does not mean the build is done. An unticked item fails the spec check.

## Boundaries and data

- [ ] CHK001 The target solution and publisher prefix are named, and whether a new solution is allowed
- [ ] CHK002 Every destructive data change is named as a one-way door
- [ ] CHK003 The inventory was read, and no existing component already does the job

## Names and values

- [ ] CHK004 Every new name follows `coding-standards.md` and cites its standard ID
- [ ] CHK005 Every environment variable has a value per environment, and none that differs by environment has a default
- [ ] CHK006 Every OAuth connection is set up by day or listed as a PARK step

## Risk

- [ ] CHK007 Every security role change is named, with its privilege depth
- [ ] CHK008 The licence impact is stated: premium connectors, code apps, service-principal-owned premium flows
- [ ] CHK009 The residency tier allows factory work
- [ ] CHK010 The kind of change to a model-driven app is stated, and "another change to an existing app" is planned as day work or a PARK

## Build and test

- [ ] CHK011 A reference component is named for the build to copy
- [ ] CHK012 The testability contract names the controls, labels, schema names and flows the locked tests target
- [ ] CHK013 The verify profile change is stated, or "none"
- [ ] CHK014 A Copilot Studio agent change uses the standard harness, or is day work
- [ ] CHK015 Open questions are split into "we can answer" and "ask the client", and every client question is answered

## Notes

- `__SPECKIT_COMMAND_IMPLEMENT__` reads checklist state as a gate and must not change markers
- Add findings inline under the item
