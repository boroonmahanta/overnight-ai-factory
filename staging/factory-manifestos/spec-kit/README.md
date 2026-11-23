# Spec Kit: the GET AI presets, spec check and bundle

Built 23 November 2026 (DG4, ADO 2544; `docs/plans/stage-1-day-gate-plan.md` in the planning repo). Plan sections 6.1 to 6.3, 6.6 and 6.7.

## The pin

**Spec Kit 1.4.3** (tag `v1.4.3`, commit `980b3d027f4bd7958c35f97f618d854b41320e3f`, 19 November 2026). Boroon, 23 November 2026: D2 said "the newest 1.3.x", but 1.4.0 to 1.4.3 had shipped since, with nothing marked as breaking, and 1.4.3 added section replacement for presets. Release notes for 1.3.0 to 1.4.3 were read before pinning.

Install it the documented way, pinned to the commit:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@980b3d027f4bd7958c35f97f618d854b41320e3f
```

The PyPI package `specify-cli` carries the same versions, published by Spec Kit's own `publish-pypi.yml` from each tag (trusted publishing, no provenance attestations). So a hashed requirements pin of `specify-cli==1.4.3` would let Dependabot watch it (A1); its dependencies need hashes too.

**Prerequisite:** the system `python3` needs PyYAML. Spec Kit's shell resolver composes preset layers with it, and without it `specify` stops with "PyYAML is required to resolve preset template composition".

## What is here

| Path | What it does |
|---|---|
| `presets/getai/` | Every profile. Wraps the core spec template: a YAML header (ADO ID, lane, profile, ambition, work size, design document and exact version, prototype) before it; an Acceptance Scenario Map, Non-Functional Requirements and Constraints after it. Wraps `specify` and `clarify` with the GET AI rules. Replaces the constitution template. Adds the `getai-checklist` template |
| `presets/getai-lcp/` | Low-code, on top of `getai`. Appends the Low-Code Fields (plan 6.3) to the spec template. Replaces the plan template's source-tree section with the delivery vault's design and handoff sections. Wraps `specify` with the low-code rules. Adds the `getai-lcp-checklist` template |
| `extensions/getai-spec-check/` | The mandatory `before_implement` hook (`optional: false`). Its command runs `scripts/check_spec.py`, a byte-identical copy of `factory-gates` `spec/check_spec.py` (D3; built in DG5, 23 November 2026). Never edit the copy: change `factory-gates` and copy it again. While both are staged, a test there fails if the hashes differ |
| `bundles/getai-lcp/` | Spec Kit's `assess` and `bug` extensions, the spec check and both presets, `getai-lcp` on top |

### How the overrides are made

A preset may contribute once per template or command. Each override here is one composition step over Spec Kit's own file, never a copy of it, so Spec Kit's updates flow through:

| Artefact | `getai` | `getai-lcp` (wins) |
|---|---|---|
| `spec-template` | `wrap`: header before, three sections after | `append`: Low-Code Fields |
| `plan-template` | | `replace-section`, selector `project-structure` |
| `constitution-template` | `replace` (the core file is a skeleton) | |
| `speckit.specify` | `wrap`: GET AI rules before the core command | `wrap`: low-code rules before both |
| `speckit.clarify` | `wrap`: the grilling rules before the core command | |
| `getai-checklist`, `getai-lcp-checklist` | new templates | |

The core commands still say "at most three markers" and "one question at a time". The GET AI rules above them say they win where they differ. That keeps each override a few lines long; the cost is that the agent reads both.

## Install today (staging)

In a project repo, after `specify init --here --integration copilot`:

```bash
specify preset add --dev <path>/spec-kit/presets/getai --priority 10
specify preset add --dev <path>/spec-kit/presets/getai-lcp --priority 5
specify extension add --dev <path>/spec-kit/extensions/getai-spec-check
specify extension add assess
specify extension add bug
```

Lower priority wins, so `getai-lcp` composes on top of `getai`. `assess` and `bug` ship inside Spec Kit and install offline. Commit the resulting `.specify/` and `.github/skills/` by a reviewed daytime pull request: both are protected paths.

**Why not `specify bundle install`:** in 1.4.3 a bundle takes its presets and extensions only from Spec Kit's packaged set or from a catalog, never from folders beside `bundle.yml`. The bundle names a private catalog `getai` for the three GET AI parts. That catalog is made in the move (DG8): a catalog JSON and release archives in `GetAI-IP/factory-manifestos`, read with `~/.specify/auth.json` set to the `github-cli` provider for `getai.ghe.com` and `api.getai.ghe.com` (Spec Kit's authentication reference covers GHE.com).

**Why no lean preset:** the day-gate plan put Spec Kit's `lean` preset in the bundle. Its `implement` has no hook step and no checklist gate, so with it the mandatory spec check would never run. It is left out.

## Tested (23 November 2026, Spec Kit 1.4.3, macOS)

In a scratch folder: `specify init t1 --integration copilot --non-interactive`, then the five commands above. Results:

- The composed spec template holds the YAML header, every core section, the Acceptance Scenario Map, Non-Functional Requirements, Constraints and all 17 Low-Code Fields. The composed plan template holds the ten low-code sections in place of Project Structure, with the core Summary, Technical Context, Constitution Check and Complexity Tracking kept.
- `.github/skills/speckit-specify/SKILL.md` starts with the low-code rules, then the GET AI rules, then the core command; `speckit-clarify` starts with the grilling rules. Each skill's `metadata.source` names the preset that changed it (`preset:getai-lcp`, `preset:getai`).
- `.specify/extensions.yml` registers `speckit.getai-spec-check.run` under `before_implement` with `optional: false`. The core `implement` skill reads `before_implement` hooks.
- `specify bundle validate --offline` passes the bundle, with a warning for each of the three `getai` catalog parts it cannot check offline.

Not tested: running the commands with an agent; the bundle install (needs the catalog, DG8).

## The spec check (DG5, 23 November 2026)

`scripts/check_spec.py --spec <spec.md> --profile lcp|pcp [--repo <root>]`, Python standard library only, run with `python3 -I`. It reads the format above and fails on, by rule name: `header`, `ado-id`, `design`, `marker`, `checklist`, `nfr`, `assumption`, `criteria`, `lcp-field`, `scenario` (with `--repo`) and `spec` (no such file). It warns, without failing, on `design-leak`: a library, schema or file layout named outside Constraints (plan 6.6); the Low-Code Fields and the Acceptance Scenario Map are exempt, because plan 6.3 asks for names there. The script's docstring lists each rule in full. Its tests and fixtures are in `factory-gates` (`tests/test_check_spec.py`, `tests/fixtures/specs/`).

What a spec needs, beyond what the templates say:

- **Checklists:** `checklists/getai.md` always, and `checklists/lcp.md` for profile lcp, each with at least one item. Every `- [ ]` item in any file under `checklists/` fails, Spec Kit's own `requirements.md` included. Items inside HTML comments do not count.
- **Markers count everywhere,** inside HTML comments too. Everything else ignores comments, so the templates' guidance comments can stay.
- **Assumptions:** each line ends `(approved: <who>, <YYYY-MM-DD>)`, with a real date. A line that says only `None.` needs no approval.
- **Criteria:** every list item that starts with **Given** needs an `AC-<n>` ID; an ID may be defined once; every map row names a defined ID; lane A needs at least 20 (plan 6.6). In the map, the second column holds the scenario IDs, separated by commas.
- **Scenario IDs (with `--repo`):** an ID resolves to a file under `tests/` whose name is the ID plus its extensions (`tests/scenarios/<id>.yaml`, `tests/acceptance/ui/<id>.spec.ts`), or, if the ID holds a slash, to that path under `tests/`. DG7 (2546) sets the scenario conventions and may change this.
- **Header:** `ambition` is `low` or `high` (the two values the plan names); `profile: lcp` needs `lane: B` (plan 6.3); the header ends with `---` before the spec's title.

Tested the same day, on Spec Kit 1.4.3 in a scratch project: `specify extension add --dev` copies `scripts/check_spec.py` to `.specify/extensions/getai-spec-check/scripts/`, byte for byte, which is the path the hook's command runs. With `.specify/feature.json` pointing at a copy of the good low-code fixture, the hook's own steps (`check-prerequisites.sh --json --paths-only`, then the command in `commands/run.md`) passed it. A spec and both checklists composed by Spec Kit's own resolver straight from the templates failed on every rule, 42 failures. The script runs on Python 3.9, 3.14 and 3.15.

## Findings

- **Spec Kit's three-marker cap** lives in the core `specify` command (Outline step 6.3, step 8c and "For AI Generation"), not in a template. Clarify's caps (five per session, one at a time) are in its Outline steps 4 and 5.
- **`update-agent-context` is now the opt-in `agent-context` extension.** `specify init` does not install it, so it is off unless someone adds it. Do not add it (plan 6.1: it writes to a protected file).
- **`specify init` no longer installs the `git` extension** by default, so no hook creates branches. Name the day branch `<ado-id>-<slug>` by hand (plan 6.4).
- **No Spec Kit numbering (Boroon, 23 November 2026).** Every spec needs an ADO work item ID. The GET AI specify rules find the story in ADO, or create it (after the owner agrees the project and title) when none exists, and always set the folder to `specs/<ado-id>-<short-name>`. If no ID can be found or created, specify stops. Spec Kit's own `001-` or timestamp folders are never used.
- **The hook is a prompt, not a lock.** A mandatory hook asks the agent to run the command; an agent can still skip it. The gate's CI check, running its trusted copy of the script, is the lock (D3, 2538).

## Prototypes (plan 6.7)

The spec header's `prototype` field links the approved mock or throwaway prototype for any user-facing change (rule 10). For low-code, a prototype:

- is a throwaway canvas app, code app or flow sketch, built in a maker sandbox or a free lane by day;
- uses its own solution with the publisher prefix `proto`;
- is never promoted. Preflight fails a lane that still holds one, and a trusted lint fails any pull request that contains one (2538);
- goes onto the ADO item as screenshots or a short screen recording, which is the design-first approval. The real build starts from the spec.

## Third-party pieces

Spec Kit (MIT, `github/spec-kit`) and the skills it generates into `.github/skills/`. Its row is in the planning repo's `docs/component-register.md`. Our presets copy no Spec Kit file; the composed skills hold Spec Kit's text below ours.
