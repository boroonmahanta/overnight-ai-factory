## GET AI rules for this command (grilling)

These rules come from the GET AI preset (plan 6.2, the `getai-grilling` skill). Where they differ from the command below, these rules win.

1. **Rounds of up to five.** Ignore "present exactly one question at a time" and the cap of five questions for the whole session. Ask in rounds. A round holds at most five questions, the most blocking first: those whose answers unblock the most others. If more are waiting, say how many. Wait for the owner's answers, write them into the spec, rescan, then ask the next round. A question that depends on another question still open belongs to a later round.
2. **Question format.** Number the questions in a round Q1 to Q5. Each has a full question ending in `?`, one sentence on what it decides, and your recommended answer, worded so "yes" accepts it. Keep the core command's option table for multiple choice.
3. **Facts versus decisions.** Before you ask, look up every fact yourself: the repo, `glossary.md`, `docs/adr/`, the ADO work item and its history, and the platform's own metadata where you can read it. Ask the owner only for decisions. A question you could answer with real data is not a question.
4. **When to stop.** Keep going until no category that matters is Partial or Missing and no `[NEEDS CLARIFICATION]` marker is left, or the owner stops. If the owner stops early, list what is still open under Deferred: the spec check fails on any open marker.
5. **Assumptions.** When the owner approves an assumption, end its line with `(approved: <who>, <YYYY-MM-DD>)`.
6. **Glossary terms.** Add each new or changed business term to `glossary.md` in its format: the term, a one or two sentence definition, one `_Schema_` line (the Dataverse table and column, flow or app for low-code; the code symbol for pro-code) and the words to avoid. Create the file from the project template if it does not exist.
7. **Decision records.** For each answer that is hard to reverse, surprising without context and the result of a real trade-off, add a record to `docs/adr/` in its format, numbered after the highest existing record.
8. **Reviewed by day.** `glossary.md` and `docs/adr/` change here only on the spec's day branch. They reach `main` through the reviewed spec pull request, never another way (rule 17).
9. **Confirmation gate.** When nothing is left to ask, ask the owner to confirm in writing that you have reached a shared understanding. Record it as the last bullet of today's Clarifications session: `- Confirmed shared understanding: <owner>, <YYYY-MM-DD>`. Do not suggest plan until the owner has confirmed.

{CORE_TEMPLATE}
