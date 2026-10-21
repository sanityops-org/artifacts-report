# prompt-skill — EMPTY (0 cases)

No case in the corpus ships both a loadable System Prompt **and** a loadable Skill.

## Why this folder is empty

`SKILL.md` is a file-based-agent convention. Agents built this way (OpenClaw, nanobot, hermes-agent, openagent, mem0, agency-agents) do ship prompt files, but those prompts are either:

- Jinja/Go template fragments with runtime placeholders and no self-contained output contract, or
- persona/soul files that carry tone rather than a task, or
- role cards whose surrounding runtime supplies the instructions.

The reverse also holds: products that ship a complete, loadable system prompt (contract review, recipe import, bookmark tagging, office assistant, collaboration assistant) do not use `SKILL.md` at all.

## What would fill it

A file-based agent that (a) uses `SKILL.md` for capabilities and (b) also ships a complete, self-contained system message. None found in 205 collected cases across two independent sampling frames.

## Cross-reference

See the agent-case notes in `_archive/agent-suite/README.md` (per-case P/S/T counts) and `../README.md` §3.
