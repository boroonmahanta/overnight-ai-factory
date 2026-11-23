## Low-Code Fields *(mandatory for profile lcp)*

<!--
  GET AI low-code (plan 6.3). Fill every field, or write "Not applicable: <reason>".
  An empty field or a bracketed placeholder fails the spec check. New names follow
  coding-standards.md: cite the standard ID beside each one. Lane and ambition are in
  the YAML header; acceptance scenarios are in the Acceptance Scenario Map.
-->

### Solution boundaries

[Target solution, publisher prefix, and whether this story may add a new solution]

### Data model intent

[Tables and columns in business terms, and whether any change is destructive: one that drops or changes existing data is a one-way door]

### Connection references

[Each connector, its authentication type, and whether it needs OAuth consent. An OAuth one is set up by day or listed as a PARK step]

### Environment variables and values per environment

| Name | Type | Lane | Test | UAT | Prod |
|---|---|---|---|---|---|
| [schema name] | [type] | [value] | [value] | [value] | [value] |

[Connection references' connections go in this table too. No default value for a value that differs between environments]

### Names

[Every new table, column, flow, app, environment variable and connection reference, each with the standard ID it follows]

### Reference components

[The hand-built app, flow or table the build copies for its conventions]

### Inventory check

[Which inventory was read, and why no existing component already does this job]

### Open questions

**We can answer** (facts the team looks up): [question, or none]

**Ask the client** (decisions): [question, or none]

### Security roles

[Roles that change, and at what privilege depth. Any change sets the Merge Danger floor at 7, and a person reviews it]

### Design-first mock or prototype

[Which screens, adaptive cards or agent wording the `prototype` header field covers. A prototype uses its own solution with the publisher prefix `proto` and is never promoted]

### Testability contract

[Control names (`data-control-name`), accessible labels, schema names, flow names, HTTP trigger audience. The locked tests target these]

### Verify profile change

[New routes, journeys, key flows or test sets for the solution's verify profile, or "none"]

### Glossary terms

[New or changed terms, each with its table, column, flow or app name]

### Copilot Studio agent

[Harness (only the standard harness runs at night), primary model, the "Move data across regions" setting, authentication mode]

### Residency tier

[T1 to T4 (plan 9.4). It decides the engine and whether the factory may run this story at all]

### Licence impact

[Premium connectors, code apps, premium flows owned by a service principal]

### Kind of change to a model-driven app

[New app; an additive change to an existing app (a column on an existing table, shown on an existing form and view); or another change to an existing app, which parks at night (plan 5.6)]
