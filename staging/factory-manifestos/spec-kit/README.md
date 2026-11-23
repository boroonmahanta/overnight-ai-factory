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
| `extensions/getai-spec-check/` | The mandatory `before_implement` hook (`optional: false`). Its command runs `scripts/check_spec.py`, a byte-identical copy of `factory-gates` `spec/check_spec.py` (D3). **The script comes in DG5** (Wednesday 25 November) |
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

Not tested: running the commands with an agent; the bundle install (needs the catalog, DG8); the spec check script (DG5).

## Findings

- **Spec Kit's three-marker cap** lives in the core `specify` command (Outline step 6.3, step 8c and "For AI Generation"), not in a template. Clarify's caps (five per session, one at a time) are in its Outline steps 4 and 5.
- **`update-agent-context` is now the opt-in `agent-context` extension.** `specify init` does not install it, so it is off unless someone adds it. Do not add it (plan 6.1: it writes to a protected file).
- **`specify init` no longer installs the `git` extension** by default, so no hook creates branches. Name the day branch `<ado-id>-<slug>` by hand (plan 6.4); the GET AI rules name the spec folder the same way.
- **The hook is a prompt, not a lock.** A mandatory hook asks the agent to run the command; an agent can still skip it. The gate's CI check, running its trusted copy of the script, is the lock (D3, 2538).

## Prototypes (plan 6.7)

The spec header's `prototype` field links the approved mock or throwaway prototype for any user-facing change (rule 10). For low-code, a prototype:

- is a throwaway canvas app, code app or flow sketch, built in a maker sandbox or a free lane by day;
- uses its own solution with the publisher prefix `proto`;
- is never promoted. Preflight fails a lane that still holds one, and a trusted lint fails any pull request that contains one (2538);
- goes onto the ADO item as screenshots or a short screen recording, which is the design-first approval. The real build starts from the spec.

## Third-party pieces

Spec Kit (MIT, `github/spec-kit`) and the skills it generates into `.github/skills/`. Its row is in the planning repo's `docs/component-register.md`. Our presets copy no Spec Kit file; the composed skills hold Spec Kit's text below ours.
