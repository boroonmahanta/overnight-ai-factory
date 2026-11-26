# Locked scenarios: conventions

How a low-code project writes the tests the gate runs against each pull request, one section for each type in plan 5.8. Draft v0, ADO 2546 (DG7), 25 November 2026. Untested until DG9 runs the Northwind examples in `factory-test`.

Files here:
- `scenario.schema.json`: the format of workflow scenarios and Web API tests (one schema, decision D4).
- `examples/northwind/tests/`: one example of each, on Microsoft's Northwind Traders sample solution (decision D6). Both test behaviour Northwind already has, so they pass on an unchanged import.

Who reads this: the people who write locked tests (acceptance owners, spec owners, business owners of Copilot Studio agents), and whoever builds the gate scripts that run them: `run_workflow.py` (ADO 3027), `trace_criteria.py` and the Direct Line runner.

## Rules for every type

**Who writes them.** A person who is not the worker (rule 3). In stage 1 there is no `test-author` agent. The spec owner checks they match the intent. `@ai-factory-acceptance-owners` approve them, and the approver is not the person who wrote them. For a Copilot Studio agent, its business owner writes the conversations.

**When.** By day, before the story is marked Factory Eligible, by a reviewed pull request. The paths `tests/acceptance/**` and `tests/scenarios/**` are locked: the push ruleset lets only that review change them, CODEOWNERS sends them to the acceptance owners, and the gate's `locks` job fails a night pull request that touches them.

**IDs.** Every locked test has an ID, and its file is named after it: `tests/scenarios/wf-order-status-shipped-01.yaml`, `tests/acceptance/ui/ui-order-form-01.spec.ts`. The spec check finds a test by that name. An ID is lower case: a type prefix, a short slug, and a two-digit number, at most 40 characters.

| Prefix | Type | Folder |
|---|---|---|
| `wf-` | Workflow scenario | `tests/scenarios/` |
| `api-` | Web API test (server logic) | `tests/acceptance/api/` |
| `ui-` | Playwright test | `tests/acceptance/ui/` |
| `agent-` | Copilot Studio conversation | `tests/acceptance/agents/` |
| `set-` | Copilot Studio built-in test set | `tests/acceptance/agents/sets/` |
| `ho-` before any of these | Held-out case | `GetAI-IP/factory-holdout` only |

**Criteria.** Every test names the spec's acceptance criteria it covers, as `AC-<n>`: a `criteria` list in YAML, a Playwright tag `@AC-<n>` in a spec file. The spec's Acceptance Scenario Map lists the test's ID against the same criteria. The spec check fails a criterion with no test; `trace_criteria.py` (not written yet) will check that the two lists agree.

**Run tags.** Every row a test creates carries a run tag, so it can be found and deleted. The tag is `lcp-run:<run ID>/<test ID>`, for example `lcp-run:nwt-20261125-3059-lcp_evaluator-1/wf-order-status-shipped-01`. It goes in one text column of each table, named in the test as `tag_column`: a column of at least 100 characters that can be filtered. Northwind's tables each have `nwind_sampledataoriginalid` (100 characters), which the app does not use. The primary name column often does not fit: Northwind's order number holds 8 characters.

**Clean-up.** The runner deletes every row it created, pass or fail, and the rows a flow made that a test found by filter. A nightly sweeper (plan 5.8, not built) deletes rows whose tag column starts with `lcp-run:` and that are more than a day old, in every table and column a locked test names.

**One at a time.** Tests that touch the same table never run at the same time. The runner works this out from the tables each scenario names. To start, everything runs one after another: one Playwright worker, as Microsoft advises for a shared environment, and the gate runs the scenarios before the Playwright suite.

**No real data.** Made-up values only. No client data and no production data (rule 15). These files can be read by anyone with access to the project repo.

**The held-out set.** Same formats, same rules, in the private repo `GetAI-IP/factory-holdout`, at `projects/<project>/tests/...` (the same paths as a project repo). IDs start with `ho-`, for example `ho-wf-order-status-shipped-02`. A held-out ID never appears in the spec's map, because the worker reads the spec. Only counts and failing IDs come back to the pull request (rule 4).

## Workflow scenarios

`tests/scenarios/<id>.yaml`, `kind: workflow`. For cloud flows and classic workflows. A flow is tested from the outside: it cannot be started on demand by an app identity (plan 5.9, spike 0.14), so the scenario fires its own trigger.

The runner, as the Test identity (`getai-<project>-test`) over the Web API:
1. Checks the file (the schema, then the rules under "What the schema cannot check"). A file that fails is a failed case; the others still run.
2. Notes the time, then creates the `seed` rows in order, writing the run tag into each `tag_column`.
3. Does the `trigger`: creates, updates or deletes one row, or posts to the flow's HTTP trigger.
4. Reads Dataverse every `poll_seconds` until every expectation under `rows` and `plugin_trace` holds. If they do not all hold within `timeout_seconds` (default 300), the case fails.
5. If the scenario has `run`: looks for a run of that flow or workflow that started after step 2. A run with another status fails the case. A run that is not there is "unknown" and does not decide anything, because the run history is not complete (plan 5.9).
6. Cleans up (above). A clean-up that fails does not change the result; it is listed in the evidence, and the sweeper finds the rows later.

Example: `examples/northwind/tests/scenarios/wf-order-status-shipped-01.yaml`. Northwind's classic workflow sets an order's status from its sample-data status text when the order is created.

A scenario must point email, Teams and approval steps at test mailboxes, through environment variables set in the project's `test.settings.json` in the gate repo. It must never message a real person.

## Web API tests (server logic)

`tests/acceptance/api/<id>.yaml`, `kind: api`. For plug-ins, low-code plug-ins, entity-scoped business rules and columns the server fills in. Same schema and runner as workflow scenarios, so no test code of our own runs beside the Test credentials (D4). The differences:
- the trigger is always one row create, update or delete;
- there is no `run` check;
- the default timeout is 60 seconds, because the logic runs when the row is saved;
- `plugin_trace` checks the plug-in trace logs written after the trigger, by plug-in type name. This needs plug-in trace logging on in `factory-test`.

Form-scoped business rules fire only in the browser, so they get a Playwright test instead.

Example: `examples/northwind/tests/acceptance/api/api-order-number-01.yaml`. Northwind has no plug-ins, so it checks the order number the server fills in. A plug-in test looks like this under `expect`:

```yaml
expect:
  rows:
    - ref: order
      fields:
        smpl_followupdate:
          equals: "2026-03-08"
  plugin_trace:
    - type_name: "Smpl.Plugins.SetFollowUpDate"
      message_name: Create
      no_exception: true
```

## The file format, for both

The schema is the full reference. In short:

| Key | What it holds |
|---|---|
| `schema_version` | `1` |
| `id`, `kind`, `title`, `criteria` | The ID (same as the file name), `workflow` or `api`, one line in plain words, the `AC-<n>` list |
| `timeout_seconds`, `poll_seconds` | How long to wait (10 to 900), how often to look (2 to 60) |
| `seed` | Rows to create first: `alias`, `table`, `tag_column`, `fields`. A seed row must not fire the logic under test |
| `trigger` | One act. `kind: row` with `action: create` (`alias`, `table`, `tag_column`, `fields`), `update` (`ref`, `fields`) or `delete` (`ref`); or `kind: http` with `workflow_id` and an optional `body` |
| `expect.rows` | Either `ref: <alias>`, a row this test made; or `table` and `filter` (an OData filter), with `count` (default 1; 0 means none) and `cleanup` (default true). Then `fields`, the checks |
| `expect.plugin_trace` | `type_name`, and optionally `message_name`, `min_count` (default 1), `no_exception` (default true), `message_contains` |
| `expect.run` | `workflow_id`, `status` (`succeeded` or `failed`). A secondary signal only |

Names are Dataverse logical names: lower case, with the publisher prefix (`nwind_orders`, `nwind_customerid`). The runner looks up each table's Web API name and each lookup's link from Dataverse itself. That matters: Northwind's orders table is `nwind_orderses` in the Web API.

**Values** in `fields`: text, numbers, `true` or `false`, `null` to clear a column, or a lookup to a row this test made:

```yaml
fields:
  nwind_customerid:
    ref: customer
```

A choice takes its number. A date takes quoted text: `"2026-03-01"` for a date-only column, `"2026-03-01T09:00:00Z"` for date and time, in UTC.

**Placeholders**, in any text value, in a filter and in an HTTP body:

| Placeholder | Becomes |
|---|---|
| `${run_tag}` | The run tag |
| `${<alias>.id}` | The ID of a row this test made, once it exists |
| `${today}`, `${today+N}`, `${today-N}` | A date, `YYYY-MM-DD`, in UTC, at the start of the run |

**Checks** on a column, one or more, all of which must hold:

| Check | Holds when |
|---|---|
| `equals` | The value is exactly this. For a choice, its number; for a lookup, the row's ID, such as `"${customer.id}"`; for a date, the text the Web API returns |
| `empty` | `true`: the column has no value. `false`: it has one |
| `contains` | The text holds this |
| `matches` | The text matches this regular expression (Python's), anywhere unless anchored with `^` and `$` |

**Writing the YAML.** The gate reads YAML with its own small reader, so keep to the plain part of YAML: no `{ }` mappings, no `|` or `>` text, no anchors. Quote dates, `yes`, `no`, `on` and `off`, and anything that starts with a symbol. Quoting every text value is the easy rule. The reader names the line it refuses. A first line like `# yaml-language-server: $schema=<path to scenario.schema.json>` makes VS Code's YAML extension check the file as you type.

## What the schema cannot check

For the runner (3027), and for a lint if one is written:
- the `id` equals the file name, and the folder matches the `kind`;
- aliases are unique in the file, and every `ref` and `${<alias>.id}` names a row made earlier in the file;
- every placeholder is one of those above;
- no `fields` sets its row's `tag_column`;
- each `tag_column` is a text column of at least 100 characters, and each table and column exists in Test;
- each criterion is listed for this ID in the spec's map (`trace_criteria.py`).

## UI tests (Playwright)

`tests/acceptance/ui/<id>.spec.ts`, IDs `ui-<slug>-<nn>`. Playwright in TypeScript on Microsoft's toolkit (model-driven: `ModelDrivenAppPage`, `GridComponent`, `FormComponent`; canvas: `CanvasAppRuntimePage`, for a published app; `CanvasAppPage` drives Power Apps Studio, for authoring only), signed in as the certificate test user. The kit is built in its own session (ADO 2546, "45. Stage 1 - Build - Playwright kit v0") in `staging/factory-gates/playwright/`; the gate runs it with the project's specs.
- One file is one ID. It may hold several tests; each is tagged with the criteria it covers, `test('...', { tag: ['@AC-3'] }, ...)`, so `--grep @AC-3` runs one criterion.
- A canvas test also carries the tag `@canvas`, which puts it in the kit's canvas project. Every other UI test runs in the model-driven project.
- **Selectors** (plan 5.8): accessible name first (`getByRole`, `getByLabel`); `data-control-name` second, for a canvas control with no accessible name; never CSS paths or positions. The names come from the spec's Testability contract. A renamed control then breaks the test, as it should.
- Data the test makes carries the run tag, through the kit's helper, and is deleted at the end.
- Tests that change the same table run in one serial group.
- Each changed form or screen gets an axe-core pass against the kit's baseline of known platform faults, and a keyboard-only journey (plan 5.9).
- Northwind as the factory imports it has no canvas apps (they were left out), so its examples are model-driven.

## Copilot Studio conversations

`tests/acceptance/agents/<id>.yaml`, IDs `agent-<slug>-<nn>`, with `schema_version: 1`, `id` and `criteria` like the other YAML files. Each holds scripted turns, the expected words, attachments and tools, and a rubric reference (plan 5.8). The full format is set when the Direct Line runner is built; no project has agents yet (Northwind's `gate.json` says `agents: false`). The runner reads only the `.yaml` files at the top of `agents/`.

## Copilot Studio built-in test sets

`tests/acceptance/agents/sets/<id>.csv`, IDs `set-<slug>-<nn>`: columns Question and Expected response, up to 100 single-response cases or 20 conversations of up to 12 messages. Kept in the repo, and created in `factory-test` by the test owner, because no command imports them. A CSV has no place for criteria, so the spec's map alone links a set to its criteria.

## Open points

Untested until DG9 and 3027:
1. **The HTTP trigger's address.** The scenario names the flow by its ID; how the runner gets the trigger's address as the Test identity is not tried. The flow service refused the lane identity's `run` call (spike 0.14). A row trigger needs no address, so prefer one.
2. **Where run records are.** A cloud flow's runs are in `flowrun`; a classic workflow's in `asyncoperation`. Northwind's workflow deletes its own succeeded jobs, so its example expects "unknown".
3. **Plug-in trace logging** must be on in `factory-test` before any `plugin_trace` check can pass (2541 or 2459).
4. **Rows a flow makes** carry no run tag. A test finds them by filter and deletes them; if the run dies first, the sweeper cannot find them.
5. **Which copy of the schema the gate trusts.** This one moves to `GetAI-IP/factory-manifestos` with the other conventions (D1). The runner in `factory-gates` must enforce the same rules: 3027 decides whether it keeps a hashed copy beside the runner, as the spec check does.
6. **The Northwind spec.** The examples' `AC-1` and `AC-2` are stand-ins. The spec written for the Stage 1 exit test (2539) maps the real criteria to these IDs, and the files move to `AI-Business-Solutions/ai-factory-nwt` by pull request.
