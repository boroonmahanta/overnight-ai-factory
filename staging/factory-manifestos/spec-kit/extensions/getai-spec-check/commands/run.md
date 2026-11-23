---
description: "Run the GET AI spec check on the current feature's spec. A failed check stops the command that called it."
---

# GET AI spec check

This command runs as a mandatory hook before implement (`before_implement`, `optional: false`). It runs a deterministic script. You report its result and obey it.

## Steps

1. From the repository root, run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` (PowerShell: `.specify/scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly`) and read `FEATURE_SPEC`.
2. Read `profile` from the YAML header at the top of `FEATURE_SPEC`.
3. Run, with the values from steps 1 and 2:

   ```bash
   python3 -I .specify/extensions/getai-spec-check/scripts/check_spec.py --spec "<FEATURE_SPEC>" --profile "<profile>" --repo .
   ```

4. Show the script's output to the user unchanged.
5. If the exit code is not 0, **stop**. Tell the user the spec is not ready and that implement must not go on. Do not run implement's remaining steps.
6. If the exit code is 0, say the spec check passed, and continue.

## Never

- Never edit the spec, a checklist, the scenario map or the script to make the check pass.
- Never tick a checklist item, approve an assumption or remove a `[NEEDS CLARIFICATION]` marker yourself.

## Notes

- The script is a byte-identical copy of `spec/check_spec.py` in `GetAI-IP/factory-gates` (D3). The gate runs its own trusted copy on every spec pull request and checks this copy's hash, so a hook that was skipped or edited is caught there.
