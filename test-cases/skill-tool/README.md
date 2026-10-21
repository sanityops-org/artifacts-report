# skill-tool — EMPTY (0 cases)

No case in the corpus ships both a loadable Skill **and** a loadable Tool Schema.

## Why this folder is empty

The two conventions come from different ecosystems and different eras:

| | Skill (`SKILL.md`) | Tool Schema (MCP / function calling) |
|---|---|---|
| Origin | File-based agent / Claude Skills ecosystem | MCP and provider function-calling APIs |
| What it describes | A capability procedure in prose | A callable interface in JSON Schema |
| Who ships it | Individual skill authors, role libraries | MCP server projects, platform vendors |

Skill authors publish prose procedures; MCP authors publish JSON interfaces. A skill that also declares a formal JSON tool schema would have to be authored against both conventions at once. None of the 205 collected cases does.

## What would fill it

A skill package whose `SKILL.md` is accompanied by a machine-readable tool definition (for example a skill that wraps an MCP server and documents its `inputSchema`). None found.
