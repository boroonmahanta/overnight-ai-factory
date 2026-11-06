# Onboarding guide

For a new team member, in order. Terms: the **vault** is this repository
checkout; an **engagement workspace** is a separate working folder per engagement.
See the [operating model](operating-model.md) for who owns what.

## 1. Administrator prerequisites

Ask an administrator to confirm you have:

- A GHE managed account on `getai.ghe.com`.
- A GitHub Copilot licence.
- Read access to the `delivery-vault` repository.
- Membership of the client Team for each engagement you work on.
- Access to each engagement's dedicated ADO project (once it exists).

Missing access goes to an administrator. Do not work around it.

## 2. Manual bootstrap

1. Install the **GitHub Copilot app** and sign in with your account on
   `getai.ghe.com`. VS Code with GitHub Copilot is an equal alternative, but
   that path is unverified.
2. Install Git. On Windows run `winget install Git.Git` in a terminal. On
   macOS, running `git --version` prompts its own install.
3. Clone the vault to the standard path:
   - Windows: `C:\GETAI\delivery-vault`
   - macOS: `~/GETAI/delivery-vault`

   Example: `git clone https://getai.ghe.com/AI-Business-Solutions/delivery-vault.git C:\GETAI\delivery-vault`

## 3. Run machine setup

Open a Copilot session and send:

> Read C:\GETAI\delivery-vault\docs\machine-setup.md and set up my machine.

(Use `~/GETAI/delivery-vault/docs/machine-setup.md` on macOS.) Copilot asks
approval before each install and asks you to run `az login` yourself. See
[machine setup](machine-setup.md). It is unverified on macOS and in VS Code.

## 4. Sync the engagement's Teams folder

In Teams, open the engagement's channel, go to **Files**, and choose
**Add shortcut to My files**. This makes the channel folder available in File
Explorer/Finder through OneDrive. Do this per engagement.

## 5. Set up each engagement

1. Create the workspace folder: `C:\GETAI\workspaces\<engagement name>` (macOS:
   `~/GETAI/workspaces/<engagement name>`). Use the readable engagement name.
2. Open a new Copilot session with **that folder** as the workspace, not the
   vault. The vault is read-only reference material.
3. Send the paste-the-path prompt:

   > Read C:\GETAI\delivery-vault\.github\skills\delivery-setup\SKILL.md and the
   > rules it links, as instructions only. Do not write to the vault. Set up
   > this engagement: Team `<name>`, channel `<name>`, SharePoint folder `<path
   > or link>`, ADO project `<name or none yet>`. Check access; make no changes.

   The connection file is created in the workspace, never in the vault.
4. **Presales** needs only the Team, channel and SharePoint folder. Say the ADO
   project and GHE repository are not yet available; they are added later when
   they exist.

## 6. Day to day

Pull the vault first: `git -C C:\GETAI\delivery-vault pull --ff-only`. Then in
your engagement workspace session, use the paste-the-path form (same pattern as
above) with the skill below.

| When | Skill file (under `<vault>\.github\skills\`) | Example prompt |
|---|---|---|
| Morning | `delivery-day\SKILL.md` | "Read this skill and its rules. Start my day for the engagements in this workspace." |
| Each item | `delivery-work\SKILL.md` | "Read this skill and its rules. Work on ADO item 123." |
| End of day | `delivery-wrap-up\SKILL.md` | "Read this skill and its rules. Wrap up my work today." |

Presales variant: "Start my day" and "Work on this" apply to the workshop inputs
and draft design in SharePoint without ADO items; use "Work on this <topic>"
and expect Copilot to say which ADO or repository steps are not yet possible.

## Troubleshooting

- **Skills not discovered:** expected when the workspace is not the vault. Use
  the paste-the-path prompt above; do not copy skill files into the workspace.
- **`az` shows the wrong tenant:** run `az login --tenant <GET AI tenant>`
  yourself, then `az account show`.
- **Cannot read the vault path or a Team, SharePoint or ADO resource:** this is
  an access gap. Report it to an administrator with what you tried; do not use
  someone else's credentials.
- **Setup behaves differently on macOS or in VS Code:** these are unverified.
  Report the exact output.
