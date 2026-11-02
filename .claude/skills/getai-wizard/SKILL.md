---
name: getai-wizard
description: Write an interactive bash script that walks a human through steps only they can do (portal clicks, consent, admin logins, Entra apps, secrets), captures the values and saves them. Use for stage 1 and 2 set-up and for PARK items of type portal_step. Not for steps an agent can do.
disable-model-invocation: true
---

# Wizard (GET AI)

Adapted from `wizard` by Matt Pocock (MIT, pinned at `mattpocock/skills` commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, original in `skills/pocock/wizard/`). `template.sh` in this folder is copied **unchanged**. Never hand-edit the library above its `STAGES` marker. Changed: examples and checks fit GET AI.

This is day work. It needs a person at a terminal. At night an agent that hits one of these steps does not run a wizard, it **PARKs** (rule 8): it writes `park.json` with type `portal_step` and an exact instruction, and the story waits in "Awaiting business". A wizard is how a human then clears it, or how they set up the factory.

If the agent can do the step itself with `pac`, `az`, `gh` or an API, it should. Do not write a wizard for that.

## When it fits

- Creating a Sandbox environment and turning on Managed Environment (day work).
- Entra app registrations and federated credentials: `getai-fl1-exec`, `getai-fl1-verify`, `getai-<proj>-test`, `getai-<proj>-deploy`.
- Granting an application user a security role in an environment.
- Creating connections that need interactive consent.
- Setting GitHub or ADO secrets and variables.
- A one-off cutover or migration with an irreversible step.

## Process

1. **Scope.** Read the repo first, do not ask cold: workflows, `AGENTS.md`, the `park.json` if one exists, environment lists, the plan section for the step. List every stage in order, and for each value: where the human gets it, where it is written (`.env`, GitHub secret, both, or nowhere) and whether it is secret.
2. **Show the list and confirm** with the human. They can add, drop or reorder.
3. **Map each stage's path** to exact clicks and commands. Where you do not know the current portal layout, say so and check the docs. Never invent steps. Power Platform admin screens change, and the product is expected to be renamed (Ignite, 17 to 20 November 2026), so record the date you checked.
4. **Author.** Copy `template.sh` to the target path. One `stage` per step, in dependency order. Open the URL before asking for its value. Use `ask_secret` for secrets. `write_env` every kept value. `set_secret` only what CI needs. `confirm` before any irreversible action. One focused task per stage.
5. **Check and hand over.** `bash -n` and `shellcheck` if present. `chmod +x`. Do not run it yourself, it opens browsers and waits for a person. Trace it by reading: every value from step 1 is captured and lands where step 1 said, and every `set_secret` name matches a `secrets.*` in the workflow.

## GET AI rules

- **Names are product-neutral** (rule 18): `getai-fl1-exec`, `factory-lane-1`, `lcp`.
- **No client production data or credentials** in a wizard (rule 15). Never write a secret into the repo. `.env` stays out of git.
- **Four identity roles stay separate** (rule 6): execute, verify, review, merge. Do not reuse one app for two roles. None in any bypass list.
- **Wizards are ephemeral by default.** Save to a scratch path and delete when done. Commit one only for a repeatable set-up, and then it is a reviewed daytime PR (rule 17).
- Log each wizard run in `decisions-<run_id>.tsv` (`getai-decision-log`) so there is a trail of who did what and when. Never log a secret value.
