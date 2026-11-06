# Machine setup

Instructions Copilot follows when a person says: **"Read `<vault>/docs/machine-setup.md`
and set up my machine."** There are no scripts; Copilot runs the listed commands
one at a time with the person's approval. `<vault>` is the standard vault
location below.

This flow is **unverified on macOS and in VS Code**. Windows with the Copilot
app is the expected first path. Report any step that behaves differently; do
not improvise around it.

## Rules for Copilot

- Ask approval before every install. Show the exact command first.
- Never use admin/elevated rights or `sudo` silently. If a step needs them, say
  so and let the person decide how to proceed.
- Change nothing else: no global Git/`az` defaults, no PATH edits, no settings,
  no other software.
- Never print or store credentials or tokens.
- Check each tool with its version command; skip installs for tools already present.
- Finish with a short report: **installed**, **already present**, **failed**
  (with the exact error and what the person can do next).

## Standard locations

| Item | Windows | macOS |
|---|---|---|
| Delivery vault checkout | `C:\GETAI\delivery-vault` | `~/GETAI/delivery-vault` |
| Engagement workspaces | `C:\GETAI\workspaces\<engagement name>` | `~/GETAI/workspaces/<engagement name>` |

The vault is read-only reference material for everyone but kit maintainers.
Engagement workspaces hold connection records and project work, never the vault.

## 1. Detect the operating system

Determine whether this is Windows or macOS. For anything else, stop and tell the
person this guide does not cover it.

## 2. Install tools

### Windows

1. Git: `git --version`. If missing, with approval: `winget install --id Git.Git -e`.
2. Azure CLI: `az --version`. If missing, with approval:
   `winget install --id Microsoft.AzureCLI -e`.
3. If `winget` is unavailable, stop and tell the person to install App Installer
   from the Microsoft Store or ask an administrator.
4. New installs may need a fresh terminal/session before the command is found.
   Ask the person to restart the app or terminal, then re-check.

### macOS

1. Homebrew: `brew --version`. If missing, **stop**. Tell the person to install
   it themselves from <https://brew.sh> and then rerun this guide. Do not run
   the installer script on their behalf.
2. Git: `git --version`. If missing, with approval: `brew install git`.
3. Azure CLI: `az --version`. If missing, with approval: `brew install azure-cli`.

### Both

1. Azure DevOps extension: `az extension list --query "[?name=='azure-devops'].version" -o tsv`.
   If empty, with approval: `az extension add --name azure-devops`.

## 3. Sign in (the person does this)

Ask the person to run `az login` themselves in a terminal. It is interactive
(browser and MFA) and must use their GET AI account/tenant. Copilot must not
handle credentials. When they confirm, run `az account show` and check that the
signed-in user and tenant are the expected GET AI ones. If the tenant is wrong,
see [troubleshooting](onboarding.md#troubleshooting). Do not change `az`
defaults or run `az logout`.

## 4. Vault location and daily pull

1. If the vault is not at the standard path and the person has read access,
   confirm the exact path, then with approval run
   `git clone https://getai.ghe.com/AI-Business-Solutions/delivery-vault.git <standard path>`.
   Create the parent folder only with approval.
2. If it already exists, confirm it is the right repository
   (`git -C <path> remote -v`) and that the working tree is clean
   (`git -C <path> status --short`). Do not modify unexpected local changes.
3. **At the start of each day**, update the vault:
   `git -C <vault> pull --ff-only`. If it fails, report the error rather than
   forcing it.

## 5. Report

List what was installed, already present and failed, the verified `az` account
and tenant (not tokens), the vault path and its latest commit, and what was not
checked (macOS and VS Code remain unverified). Then point the person to
[onboarding](onboarding.md) for the next step.
