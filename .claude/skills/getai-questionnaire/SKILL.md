---
name: getai-questionnaire
description: Turn a decision or fact you cannot get alone into a short questionnaire for someone else to fill in. Use for acceptance owners, client IT, Microsoft or Partner Center, or any PARK that needs an answer from another person.
disable-model-invocation: true
---

# Questionnaire (GET AI)

Adapted from `to-questionnaire` by Matt Pocock (MIT, pinned at `mattpocock/skills` commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, original in `skills/pocock/to-questionnaire/`). Changed: GET AI uses and rules added. Day work. At night, an agent that needs an answer PARKs (type `ambiguity`) instead.

Grill the **send**, not the subject. The person asking can always answer questions about who it goes to and what they need back. Then aim the questions at the gap between what the recipient knows and what is needed.

## Steps

1. **Who is it going to?** One exchange: their role, what they know, and how they relate to us. This sets the tone and how much context to carry.
2. **What do you need back?** One exchange: the exact decisions or facts to walk away with. A concrete list.
3. **Write it.** Save to `docs/questionnaires/<slug>.md` and say the path. Every item from step 2 must be covered by a question.

## Structure

- **Title.**
- **Purpose.** Why it exists and what decision rides on it.
- **From, To, How your answers will be used.**
- **Context.** One short paragraph for someone who was not in the room.
- **How to answer.** Deadline and rough effort. Partial answers and "I do not know" are useful.
- **Themes.** One `##` per theme, most important question first. One idea per question, never two. A blank answer line under each. A one-line "why this matters" only where the question could be misread.
- **Anything else?** A closing catch-all.

## Where it fits in GET AI

- **Acceptance owners and the person who writes the locked scenarios** (rule 3): what must be true, what edge cases, what is out.
- **Client IT:** residency tier, tenant, who owns the environments, which ITSM tool, who approves the admin steps.
- **Microsoft or Partner Center:** the credit ruling (spike 0.1). The question text is in plan section 9.1. Start from it.
- **Design approval** (rule 10): what the mock needs to show.
- **A PARK with `Custom.BlockedReason`:** turn the exact instruction into a short list a business owner can answer.

## Rules

- **No client production data** in the questionnaire. Use synthetic examples (rule 15).
- Plain language, no jargon. The reader may not know our terms.
- Whatever comes back goes to `getai-intake` or the Spec Kit step. Record the decision and who made it.
- A human sends it. The agent does not email a client.
