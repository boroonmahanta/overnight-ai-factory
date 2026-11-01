# T-shirt sizing for GET AI

Status: a proposal for Boroon's review, 1 November 2026. Nothing here is decided or built.

Purpose: match the ceremony to the stakes. This takes the effort-level idea from the video (`docs/sources/transcript-skills-comparison-addy-pocock-tan.md`) and the skills worth using from the three packs, and fits them to the GET AI plan (`docs/sources/plan-v3.1.md`).

Companion file: `skills-comparison.md` lists every skill in the three packs, the overlaps, and which skills fit GET AI.

## 1. The sizes

The video's advice is that ceremony should match the stakes. It gives four tiers: a small tweak, a small feature, a big or fuzzy feature, and production or irreversible work. It also says its author keeps light, medium and heavy versions of his skill set. GET AI already scales effort this way: the number of verifiers depends on Merge Danger, and the plan assumes a mix of 40% low, 45% medium and 15% high (section 10.4). The proposal below puts a name on that.

| Size | Looks like | Upfront work | GET AI route | Merge Danger and verifiers | Skills to use | Human gate |
|---|---|---|---|---|---|---|
| **XS** | A wording, label, colour or view-column tweak. No logic. Visual | None. One-line check | Day work with AI, or batched into the night as an S | Floor 0 to 1. 1 verifier | `bro` if needed. `lcp-verify app` for a before and after screenshot | A glance at the screenshots |
| **S** | One additive change in one app or flow. Outcome is clear. Scenarios take minutes to write | Spec Kit lean preset, 1 to 3 clarify questions, locked scenarios | Night story, Lane B Power Platform profile | Floor 0 to 2. 1 verifier | Pocock grilling rules, `tdd` at seams, Addy `incremental-implementation` and `source-driven-development`, `pr`, Tan principles seed | Morning approval at L1. Eligible for L2 only for named classes |
| **M** | Flow logic, a Copilot Studio topic or tool, a shared table, a new connection reference, code app source. Or any UI a user sees | Full GET AI preset: assess, specify, clarify, checklist. Glossary and ADR updates. Mock or prototype. Test author writes scenarios and the held-out set | Night story, Lane B Power Platform profile. Lane A if over about 40 minutes | Floor 3 to 5. 2 verifiers, 3 if another app or flow is in the blast radius | S plus `grill-with-docs`, `how`, `why`, `architect`, `blast-radius`, Addy `constraint-driven-development`, `show-me-your-work`, two-axis review | Human approves every PR with the blast radius shown |
| **L** | A one-way door: dropped column or table, a security role, money or pricing logic, deploy settings. Anything touching production data | M, plus an expand-then-contract plan for schema changes and a security check | Night story if the spec is locked. Otherwise day work | Floor 6 to 10. 2 to 3 verifiers plus a human check | M plus `doubt-driven-development`, `interrogate` where the tier allows, Addy `security-and-hardening` and `deprecation-and-migration`, `shipping-and-launch` for promotion | Human reads the one-way door. A second reviewer at floor 8 or more on client work. Never auto-merged |
| **XL** | Too big or foggy for one session: a new app, a big migration, an unclear destination | A Wayfinder map in ADO with research, grilling, prototype and task children | Not a night unit. The map closes into a spec, which is split into S, M and L stories with predecessor links | Each child story gets its own size | `wayfinder`, `research`, `prototype`, `to-questionnaire`, `arena` and `swarm` by day, `to-tickets` | Acceptance owners approve the split before any story is queued |

## 2. How to pick the size

Ask these questions in order. The size is the largest answer, not the average. This follows the plan's own rule that the deterministic floor can be raised, never lowered (rule 11).

1. **Reversibility.** Is any part a one-way door? Dropped data, a security role, money logic, deploy settings, anything sent outside. If yes, L.
2. **Blast radius.** Does it touch another app, flow, agent or shared table? If yes, at least M.
3. **Clarity.** Can every behaviour be written as a locked scenario today? If no, M with a grilling session, or XL if nobody can yet say what the stories are.
4. **Verifiability.** Can `lcp-verify` prove it? If not, raise a size and add a human check. New-harness Copilot Studio agents are the known example.
5. **Effort.** Is it more than about 40 minutes of agent work? If yes, it is probably not a single night story.
6. **Residency and data.** What is the client's tier? T3 limits models. T4 rules out the factory.

Who sets it: the spec owner proposes the size at intake. The gate's pre-floor can raise it, never lower it. A proposed ADO field could hold it, for example `Custom.WorkSize`. That field does not exist in plan Appendix D yet, so it needs a decision.

## 3. What the sizes cost

Cost comes mostly from verifiers and human minutes, not from the executor. In the plan's model a verifier session costs about USD 2 at list, and human minutes are about 80% of a story's loaded cost. So the saving from XS and S is mainly human time: no clarify rounds, one verifier, a quick morning look. The video reports that a pstack run took about twice as long as a plain run for a more hardened result. That supports keeping the heavy skills for M and L.

## 4. Proposed next steps

1. **Decide the sizes.** Agree on XS, S, M, L and XL and the rule that the largest answer wins.
2. **Read the shortlist in full**, as plan section 8.3 requires. Suggested first batch: Addy `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`; Tan `create-verification-skill`, `maintain-verification-skill`, `blast-radius`, `show-me-your-work`, `correct`, `how`, `why`; Pocock `triage`, `wizard`, `to-questionnaire`, `ask-matt`; plus the Benny triage and repro skills.
3. **Write the GET AI set**, named `lcp-*`, adapted for Power Platform. Keep it small. A router skill that routes by size comes first.
4. **Seed `coding-standards.md`** from the 13 adopted principles.
5. **Update the plan.** Add the size field to Appendix D and a short sizing section to plan section 5, if you approve.
6. **Review again after Ignite and each model release.** Delete skills the model no longer needs (plan section 8.3).

## 5. Limits

- The sizes and the sizing rule are proposals. The rule extends the plan's Merge Danger design. The plan does not say it today.
- The skills named for each size are the shortlist from `skills-comparison.md` section 5. Most were judged from their descriptions and have not been read in full.
- The cost figures are the plan's modelled figures (section 10.4), not measurements.
- The Merge Danger floors quoted come from plan Appendix B.
