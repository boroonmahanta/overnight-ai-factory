# Delivery vault

Read [repository instructions](../AGENTS.md) and follow the linked operating
rules. The four workflows are in `.github/skills/`; their names and fallback
invocation instructions are in [README](../README.md).

Do not assume this interface has another interface's tools or permissions.
This checkout is for maintaining the reusable kit only. Client work runs in a
separate engagement workspace, with the kit explicitly loaded and its linked
resources readable. Never save project context here, even in ignored folders.
If linked instructions cannot be read, stop and request an authorized readable
copy rather than proceeding without them. Never treat a skill invocation as
approval to commit, publish, mutate ADO or change a live system.
