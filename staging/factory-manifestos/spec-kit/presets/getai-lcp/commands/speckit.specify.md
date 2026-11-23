## GET AI low-code rules for this command

These rules come from the getai-lcp preset (plan 6.3). They add to the GET AI rules below.

1. **Header.** Set `profile: lcp` and `lane: B`.
2. **Low-code fields.** Fill every field under Low-Code Fields, or write `Not applicable: <reason>`. Look up the facts yourself: the existing tables, columns, flows, apps, environment variables and connection references are in the solution's export in the repo and in the inventory, and in the environment's metadata where you can read it. Choices among them are decisions for the owner.
3. **Names.** Name every new component to `coding-standards.md` and cite the standard ID beside it.
4. **Open questions.** Split them into "We can answer" (facts the team looks up) and "Ask the client" (decisions). Client questions go out by day.
5. **Low-code checklist.** After the GET AI checklist, run `.specify/scripts/bash/resolve-template.sh getai-lcp-checklist --json` (or the PowerShell or Python script beside it), write its `TEMPLATE_CONTENT` to `checklists/lcp.md` in the feature folder and fill its header. Do not tick its items: a reviewer ticks them.

{CORE_TEMPLATE}
