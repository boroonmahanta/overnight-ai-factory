# Reusable standards and patterns

Apply [operating rules](operating-rules.md); this document is a small baseline,
not a mandate for a particular vendor or architecture. Shared additions require
human review. Engagement-specific constraints are confirmed during design.

## Baseline design and build guidance

| Concern | Expected design treatment |
|---|---|
| Boundaries | Identify owners, inputs, outputs, trust boundaries and external contracts |
| Data and access | Minimize data; confirm classification, authorized roles, retention and credential handling |
| Reliability | Define meaningful failures, safe retry/idempotency boundaries and recovery; no success-shaped fallbacks |
| Change safety | Consider compatibility, migration, rollback feasibility and environment separation |
| Verification | Make each approved outcome observable; include negative paths, permissions and failure recovery where relevant |
| Operability | Define diagnostics without sensitive payloads, ownership and actionable failure signals |
| Maintainability | Reuse existing supported conventions; prefer the simplest complete implementation |

Choose technology-specific guidance only after the actual stack, versions and
environment are known. Check authoritative current documentation and existing
source conventions with targeted reads. Do not install dependencies, add
frameworks or introduce infrastructure merely to satisfy this kit.

## Patterns to consider, not automatic prescriptions

| Pattern | Useful when | Limitation to resolve in design |
|---|---|---|
| Version-pinned design and handoff | SharePoint design feeds a GHE implementation specification | Verify the exact approved SharePoint version and ADO approval; latest links and local paths alone are insufficient |
| Read-back after mutation | An external system can partially succeed | Read consistency/latency and duplicate detection must be understood |
| Outcome-based coverage | One requirement spans several technical tasks | A task list is not proof of acceptance or readiness |
| Scoped refresh | Existing source/docs may be stale | Export may have side effects and needs an approved operation |

To propose a lesson, state the anonymized problem, context, approach, verified
benefit, limitations and when not to use it. Remove client identifiers and
source fragments; seek confirmation before saving. Only a reviewed PR can
promote a candidate into shared guidance or a mandatory rule. Do not create a
lesson register or import trial history.

No project-specific examples or context are saved in the vault, even locally.
Use synthetic illustrations here. Curated project inputs stay in SharePoint;
only implementation-relevant specifications and artifacts go in project source.
