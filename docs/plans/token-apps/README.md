# The gate's three token Apps (ADO 2537)

Made in Session 45, 24 November 2026, on the laptop. The gate (`GetAI-IP/factory-gates`, `lcp-gate.yml`) mints a short-lived token from each App in the step that needs it. Each App can only read; none can write anything.

| App | Owner | Permission | Installed on | Used by | Variable and secret |
|---|---|---|---|---|---|
| `ai-factory-gate-reader` | `GetAI-IP` | Repository: Contents, read | `factory-gates` only | `map`, `locks`, `static`, `verify-in-test`, `danger`: check out the gate at `release` | `GATE_READER_CLIENT_ID`, `GATE_READER_KEY` |
| `ai-factory-holdout-reader` | `GetAI-IP` | Repository: Contents, read | `factory-holdout` only | `verify-in-test`, held-out step, only when the project's `gate.json` has a held-out set | `HOLDOUT_READER_CLIENT_ID`, `HOLDOUT_READER_KEY` |
| `ai-factory-team-reader-abs` | `AI-Business-Solutions` | Organisation: Members, read | `AI-Business-Solutions` | `danger`, merge policy: is the approver in `ai-factory-merge-reviewers`? (gate README finding 19) | `TEAM_READER_CLIENT_ID`, `TEAM_READER_KEY` |

Boroon's choices, 24 November 2026:
- **One team reader App per project org**, owned by that org. A leaked key shows only that org's members. When the gate reaches another org, that org gets its own (`ai-factory-team-reader-ams`, and so on). Not an enterprise-owned App.
- **`GetAI-IP/factory-holdout` made now, empty**, so the holdout App can be installed and tested. Private, a README only, ruleset `main-protection` like `factory-gates`'s `release-protection` (pull requests only, 0 approvals until a second approver exists, no force push, no deletion, no bypass). Its tests come at Stage 4. Note: `GetAI-IP`'s base permission is read, so all its members can read it.
- **IDs and keys for selected repos only.** In `AI-Business-Solutions`, all six as organisation variables and secrets with access "selected repositories", none selected yet; each factory project repo is added when it is onboarded. The gate reader's pair also sits on `factory-gates` itself, so the gate's own pull requests test the token.
- **`client-id`, not `app-id`**, in every token step, with the variables renamed to `..._CLIENT_ID`. A gate pull request, and plan Appendix A to match.

The IDs themselves are in ADO 2537, not here (this repo is public).

## Making an App (Boroon, in the browser)

Do this once for each App. Only the parts that differ are in the table at the end.

1. Open the owner org's new-App page:
   - `GetAI-IP`: https://getai.ghe.com/organizations/GetAI-IP/settings/apps/new
   - `AI-Business-Solutions`: https://getai.ghe.com/organizations/AI-Business-Solutions/settings/apps/new
2. **GitHub App name:** from the table. **Description:** from the table. **Homepage URL:** from the table.
3. **Identifying and authorizing users:** leave Callback URL empty. Leave "Request user authorization (OAuth) during installation" and "Enable Device Flow" unticked.
4. **Post installation:** leave Setup URL empty.
5. **Webhook:** untick **Active**.
6. **Permissions:** only the one in the table, set to **Read-only**. Everything else stays **No access**. A repository permission brings Metadata, read-only, with it; that is expected.
7. **Subscribe to events:** none.
8. **Where can this GitHub App be installed?** **Only on this account.**
9. **Create GitHub App.**
10. On the App's page, copy the **Client ID** (starts `Iv`) and send it to Claude. It is not a secret.
11. Under **Private keys**, **Generate a private key**. A `.pem` file downloads. This is the secret: don't paste it into chat.
12. In the left menu, **Install App**, then **Install** next to the owner org.
    - For the two `GetAI-IP` Apps: **Only select repositories**, pick the one repo in the table, **Install**.
    - For the team reader: there is no repository choice (the App asks for no repository permission). **Install**.

| | `ai-factory-gate-reader` | `ai-factory-holdout-reader` | `ai-factory-team-reader-abs` |
|---|---|---|---|
| Owner org | `GetAI-IP` | `GetAI-IP` | `AI-Business-Solutions` |
| Description | Read-only token for the factory gate: reads GetAI-IP/factory-gates. | Read-only token for the factory gate: reads GetAI-IP/factory-holdout. | Read-only token for the factory gate: reads this org's teams for the merge policy. |
| Homepage URL | https://getai.ghe.com/GetAI-IP/factory-gates | https://getai.ghe.com/GetAI-IP/factory-holdout | https://getai.ghe.com/GetAI-IP/factory-gates |
| Permission | Repository permissions, **Contents**: Read-only | Repository permissions, **Contents**: Read-only | Organization permissions, **Members**: Read-only |
| Install on | `factory-gates` only | `factory-holdout` only | the org (no repositories) |

## Storing the keys (Boroon, in the terminal)

Claude does not handle the keys. Run these yourself, from the folder the `.pem` files downloaded to. Each reads the key from the file, so nothing is typed or shown. The file names are the App name, the date and `.private-key.pem`; check them with `ls *.pem` first.

The gate reader, on `factory-gates` itself (for the gate's own pull requests):

```bash
GH_HOST=getai.ghe.com gh secret set GATE_READER_KEY --repo GetAI-IP/factory-gates < ai-factory-gate-reader.*.private-key.pem
```

All three, in `AI-Business-Solutions`, for selected repos, none selected yet:

```bash
GH_HOST=getai.ghe.com gh secret set GATE_READER_KEY --org AI-Business-Solutions --no-repos-selected < ai-factory-gate-reader.*.private-key.pem
```

```bash
GH_HOST=getai.ghe.com gh secret set HOLDOUT_READER_KEY --org AI-Business-Solutions --no-repos-selected < ai-factory-holdout-reader.*.private-key.pem
```

```bash
GH_HOST=getai.ghe.com gh secret set TEAM_READER_KEY --org AI-Business-Solutions --no-repos-selected < ai-factory-team-reader-abs.*.private-key.pem
```

Then delete the three `.pem` files, and empty the Bin if Finder moved them there. Nothing keeps a copy: if a key is lost, make a new one (step 11) and set it again.

Claude sets the three `..._CLIENT_ID` variables the same way, from the client IDs you send.

## Rotating a key (each quarter, with the other keys)

An App can hold up to 25 keys, and GitHub won't delete its last one. So: generate a new key (step 11), set the secret again with the same command, check a gate run, then **Delete** the old key under Private keys on the App's page.

## If a key leaks

- Gate reader: someone can read the gate's scripts, prompts and rubrics. Nothing else.
- Holdout reader: someone can read the held-out tests, which spoils them (rule 4). Rotate the key and rewrite the tests it could reach.
- Team reader: someone can read `AI-Business-Solutions`'s members and teams.

In each case: delete the key on the App's page, then make and set a new one.

## What was checked

To be filled in once the Apps exist.
