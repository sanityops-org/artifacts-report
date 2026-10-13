# TC-032: Hermes Agent - File-Based Multi-Agent Suite

## Metadata
- **Source Project**: NousResearch/hermes-agent
- **GitHub**: https://github.com/NousResearch/hermes-agent
- **Commit SHA**: 3569e8461ea721623fa16e6f01fb636157989fe6
- **License**: MIT
- **Artifact Type**: File-based logical artifacts
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API retrieval via `gh api`

---

## Project Overview

Hermes Agent is a **personal AI assistant** framework built by Nous Research that runs the same agent core across multiple surfaces: CLI, messaging gateway (Telegram, Discord, Slack, ~20 platforms), TUI, and Electron desktop app. It features **prompt-caching invariants**, a **narrow-waist core with edge capability**, and extensive skill/plugin ecosystem.

### Key Features
- **Multi-surface deployment**: Same agent core across CLI, messaging platforms, TUI, desktop
- **Prompt caching invariant**: System prompt is byte-stable for conversation lifetime
- **AGENTS.md routing**: Context-aware routing to area-specific documentation
- **Skill ecosystem**: 200+ skills across productivity, communication, and automation
- **Plugin architecture**: Extensible via plugins, MCP servers, and custom skills
- **Tool search/defer**: Progressive tool disclosure for large tool surfaces

---

## Logical Artifact Inventory

### 1. SOUL.md - Core Personality

```markdown
You are Hermes Agent, built by Nous Research. Be direct: match the length of your reply to the weight of the ask — a one-line question gets a one-line answer, and finished work gets a short report of what changed, what's verified, and what's left, never a replay of the process. No filler ("Great question," "I'd be happy to"), no restating the request back, no re-summarizing what you already said, no narrating tool calls the user can see. Plain claims over adjectives; when unsure, say so plainly. Agree because it's right, not because the user said it. Depth is earned — give it when the user asks for detail, teaches, or the stakes demand it, not by default.
```

### 2. Root AGENTS.md - Development Guide

```markdown
# Hermes Agent - Development Guide

For AI coding assistants and developers working on hermes-agent. This root file is a hub: what
applies everywhere, then a routing table. Each area's `AGENTS.md` loads automatically when you work
in that directory; read it before editing there.

**Never give up on the right solution.**

## What Hermes Is

Hermes is a personal AI agent that runs the same agent core across a CLI, a messaging
gateway (Telegram, Discord, Slack, ~20 platforms), a TUI, and an Electron desktop app. It
learns across sessions (memory + skills), delegates to subagents, runs scheduled jobs, and
drives a real terminal and browser. It is extended primarily through **plugins and skills**,
not by growing the core.

Two invariants shape almost every design decision and are the lens for reviewing any change:

- **Per-conversation prompt caching is sacred.** Mutating past context, swapping toolsets,
  reloading memories or rebuilding the system prompt mid-conversation breaks the cached prefix and
  multiplies the user's cost; the ONE exception is context compression.

- **The core is a narrow waist; capability lives at the edges.** Every model tool is sent on
  every API call, so the bar for a new *core* tool is high. New capability should arrive as a
  CLI command + skill, a service-gated tool, or a plugin — not as core surface.

## Project Structure

*(Excerpt — the upstream tree additionally includes hermes_state.py, hermes_constants.py, apps/desktop/, cron/, pm/, hermes_platform/, scripts/, and website/, and the ui-tui row reads "…JSON-RPC backend (also serves Desktop)".)*

```
hermes-agent/
├── run_agent.py          # AIAgent facade; the turn loop lives in agent/turn_*.py
├── model_tools.py        # Tool orchestration, discover_builtin_tools(), handle_function_call()
├── toolsets.py           # TOOLSETS dict, _HERMES_CORE_TOOLS
├── cli.py                # HermesCLI (REPL, slash dispatch) + hermes_cli/cli_*_mixin.py
├── agent/                # turn loop phases, providers, memory, compression, prompt builder
├── tools/                # Tool implementations (tools/registry.py) + environments/ backends
├── gateway/              # run.py facade + run_*.py phases + session*.py + platforms/
├── plugins/              # memory/, context_engine/, model-providers/, kanban/, image_gen/, ...
├── skills/               # Built-in skills (by category)   optional-skills/: shipped, not active
├── ui-tui/, tui_gateway/ # Ink terminal UI + its Python JSON-RPC backend
└── tests/                # Pytest suite, mirrors the source tree
```

## Routing Table — working in X → read X/AGENTS.md

*(Excerpt — the upstream table has 15 rows; 8 are omitted (gateway/platforms/, plugin-catalog/, tui_gateway/, ui-tui/, web/, apps/desktop/, tests/, pm/, hermes_platform/) and several "Covers" cells carry additional entries such as compression, model/aux resolution, skins, profiles/multiplex, token locks, kanban.)*

| Area | Read | Covers |
|---|---|---|
| `run_agent.py`, `agent/` | `agent/AGENTS.md` | turn phases, caching and message-flow invariants |
| `cli.py`, `hermes_cli/` | `hermes_cli/AGENTS.md` | CLI mixins, slash registry, config system |
| `gateway/` | `gateway/AGENTS.md` | adapters, message guards, streaming, notifications |
| `tools/`, `toolsets.py` | `tools/AGENTS.md` | adding tools, registry, toolsets, delegation |
| `plugins/` | `plugins/AGENTS.md` | plugin kinds, native compat contract |
| `skills/` | `skills/AGENTS.md` | frontmatter, authoring standards, curator |
| `cron/` | `cron/AGENTS.md` | scheduler invariants, job fields |
```

### 3. agent/AGENTS.md - Turn Loop Architecture

```markdown
# agent/ — AIAgent, turn loop, prompt, compression

## Shape

`run_agent.py` is the public facade: `AIAgent` is assembled from mixins. A turn is
`agent/conversation_loop.py::run_conversation`. `AIAgent.__init__` takes ~60 parameters
(credentials, routing, callbacks, session context, budget, credential pool, ...).

## Agent loop

```python
while (api_call_count < self.max_iterations and self.iteration_budget.remaining > 0) \
        or self._budget_grace_call:
    if self._interrupt_requested: break
    response = client.chat.completions.create(model=model, messages=messages, tools=tool_schemas)
    if response.tool_calls:
        for tc in response.tool_calls:
            messages.append(tool_result_message(handle_function_call(tc.name, tc.args, task_id)))
        api_call_count += 1
    else:
        return response.content
```

## Message-flow invariants (every change is reviewed against these)

- **Prompt caching must not break.** Never alter past context, change toolsets, reload memories,
  or rebuild the system prompt mid-conversation.
- **Strict role alternation.** Never two same-role messages in a row; never a synthetic user
  message injected mid-loop.
- **Context files** load from the CWD only at startup and are capped.
```

---

## Tool Definitions (Python)

### Skill Tools (skills_list / skill_view / skill_manage)

*(Note — hermes-agent has no `SkillManagerTool` class. Skill discovery and management are exposed through the model tools `skills_list`, `skill_view`, and `skill_manage`, registered in `toolsets.py` and dispatched in `model_tools.py` (`"skills_tools": ["skills_list", "skill_view", "skill_manage"]`). Skill install/uninstall is CLI-side via `hermes skills` in `hermes_cli/skills_hub.py`.)*

### Tool Search System

```python
"""Progressive tool disclosure: MCP/plugin tools are replaced by bridge tools."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class ToolSearchConfig:
    """Resolved, validated tool-search configuration for a single assembly."""
    enabled: str  # "auto" | "on" | "off"
    threshold_pct: float  # 0..100
    search_default_limit: int
    max_search_limit: int
    listing: str = "auto"  # "auto"/"on" = embed the manifest when it fits
    listing_max_tokens: int = 4000
    defer_tools: Optional[frozenset] = None

    @property
    def effective_defer_tools(self) -> frozenset:
        return _DEFAULT_DEFERRED_TOOLS if self.defer_tools is None else self.defer_tools

# Bridge tool names: tool_search / tool_describe / tool_call
BRIDGE_TOOL_NAMES = frozenset({TOOL_SEARCH_NAME, TOOL_DESCRIBE_NAME, TOOL_CALL_NAME})
```

---

## Skills (Selected Examples)

### Computer-Use Skill

```markdown
---
name: computer-use
description: "Drive the desktop background-first; escalate on signal."
version: 2.1.0
author: Francesco Bonacci (f-trycua), Hermes Agent
license: MIT
platforms: [macos, windows, linux]
---

# Computer Use (universal, any-model, cross-platform)

You have a `computer_use` tool that drives the user's desktop in the
**background** — your actions do NOT move the user's cursor, steal
keyboard focus, or switch virtual desktops / Spaces.

## The canonical workflow

**Step 1 — Capture first.**
```
computer_use(action="capture", mode="som", app="<the app you're driving>")
```
Returns a screenshot plus an indexed element list.

**Step 2 — Click by element index.**
```
computer_use(action="click", element=7)
```

**Step 3 — Verify.** Re-capture after state-changing actions.

## Actions

*(Excerpt — the upstream Actions list additionally includes right_click, middle_click, drag (from_element/to_element), set_value, and per-line annotations such as `(default: current app)`, `button=left|right|middle`, `raise_window=false`, and `(ticks)`.)*

```
capture           mode=som|vision|ax   app=…
click             element=N     OR     coordinate=[x, y]
double_click      element=N     OR     coordinate=[x, y]
scroll            direction=up|down|left|right   amount=3
type              text="…"
key               keys="<save shortcut>" | "return" | "escape"
wait              seconds=0.5
list_apps
list_windows
focus_app         app="<app name>"
```

## The verify → escalate ladder (background-first)

1. **Element, background (default).** `click(element=N)`. If `effect:"confirmed"`, done.
2. **Fresh verification.** `effect:"unverifiable"` means re-capture before retry.
3. **Pixel, background.** Click by `coordinate=[x,y]` instead of element.
4. **Foreground.** After `effect:"suspected_noop"`, re-issue with `delivery_mode="foreground"`.
```

### Notion Skill

```markdown
---
name: notion
description: "Notion API + ntn CLI: pages, databases, markdown, Workers."
version: 2.0.0
author: community
license: MIT
prerequisites:
  env_vars: [NOTION_API_KEY]
---

# Notion

Talk to Notion two ways. Same integration token works for both.

◆ **`ntn` CLI** — Notion's official CLI. Shorter syntax, one-line file uploads.
◆ **HTTP + curl** — works everywhere including Windows.

## Setup

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store in `${HERMES_HOME:-~/.hermes}/.env`:
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```

## Path A — `ntn` CLI (preferred, macOS / Linux)

```bash
# Raw API calls
ntn api v1/pages parent[page_id]=abc123 \
  properties[title][0][text][content]="Notes"

# Read page as Markdown
ntn api v1/pages/{page_id}/markdown

# File uploads
ntn files create < photo.png
```

## Path B — HTTP + curl (cross-platform, default on Windows)

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"parent": {"page_id": "xxx"}, "properties": {"title": [...]}}'
```
```

### Obsidian Skill

```markdown
---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Notes, Markdown, Vault]
    related_skills: []
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, 
searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.
The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `${HERMES_HOME:-~/.hermes}/.env`.
If it is unset, use `~/Documents/Obsidian Vault`.

*(Excerpt — the upstream skill continues with guidance on not passing `$OBSIDIAN_VAULT_PATH` literally to file tools and on using `terminal` to resolve an unknown vault path.)*

## Read a note

Use `read_file` with the resolved absolute path to the note.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link 
related content.
```

### Excalidraw Skill

```markdown
---
name: excalidraw
description: "Hand-drawn Excalidraw JSON diagrams (arch, flow, seq)."
version: 1.0.1
author: Hermes Agent
license: MIT
---

# Excalidraw Diagram Skill

Create diagrams by writing standard Excalidraw element JSON and saving as `.excalidraw` files.

## Workflow

1. Write the elements JSON -- an array of Excalidraw element objects
2. Save the file using `write_file` to create a `.excalidraw` file
3. Optionally upload for a shareable link

## Element Types

**Rectangle**:
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }
```

**Labeled shape (container binding)**:
```json
{ "type": "rectangle", "id": "r1", "boundElements": [{ "id": "t_r1", "type": "text" }] },
{ "type": "text", "id": "t_r1", "text": "Hello", "containerId": "r1" }
```

## Color Palette

See `references/colors.md` for full color tables. Quick reference:

| Use | Fill Color | Hex |
|-----|-----------|-----|
| Primary / Input | Light Blue | `#a5d8ff` |
| Success / Output | Light Green | `#b2f2bb` |
| Warning / External | Light Orange | `#ffd8a8` |
| Processing / Special | Light Purple | `#d0bfff` |
| Error / Critical | Light Red | `#ffc9c9` |
| Notes / Decisions | Light Yellow | `#fff3bf` |
| Storage / Data | Light Teal | `#c3fae8` |
```

---

## Evaluation Dimensions

### 1. File Organization Clarity
- [ ] AGENTS.md routing table provides clear navigation
- [ ] Root AGENTS.md serves as hub, area AGENTS.md provide depth
- [ ] Consistent structure across all documentation files

### 2. Prompt Caching Invariant
- [ ] System prompt byte-stable for conversation lifetime
- [ ] Context compression is the ONLY sanctioned cache break
- [ ] No mid-conversation toolset changes

### 3. Skill Architecture
- [ ] Skills follow consistent SKILL.md format with YAML frontmatter
- [ ] Each skill has clear prerequisites (env vars, binaries)
- [ ] Skills reference tools without re-implementing functionality

### 4. Plugin System
- [ ] Plugins extend core without modifying it
- [ ] Service-gated tools avoid per-session surface
- [ ] MCP server catalog available for additional tools

### 5. Tool Search System
- [ ] Progressive tool disclosure via bridge tools
- [ ] Tool search/describe/call pattern for large tool surfaces
- [ ] Configurable threshold for manifest embedding

### 6. Multi-Agent Support
- [ ] Subagent lifecycle management
- [ ] Goal persistence across compaction
- [ ] Strict role alternation in message flow

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| File Organization Clarity | 15% | | |
| Prompt Caching Invariant | 20% | | |
| Skill Architecture | 20% | | |
| Plugin System | 15% | | |
| Tool Search System | 15% | | |
| Multi-Agent Support | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Prompt Caching Tests
1. **Byte-stable verification**: Compare system prompt hashes across conversation turns
2. **Compression invariant**: Verify context compression preserves critical information
3. **Toolset stability**: Verify no toolset changes mid-conversation

### Skill Loading Tests
1. **Skill discovery**: Verify skills load from both built-in and optional directories
2. **Prerequisites validation**: Test that missing env vars/binaries are detected
3. **Frontmatter parsing**: Verify YAML frontmatter is correctly parsed

### Tool Search Tests
1. **Bridge tool routing**: Verify tool_search/describe/call work correctly
2. **Manifest embedding**: Verify listing budget is respected
3. **Deferred tools**: Verify defer_tools configuration works

---

## Notes

- **MIT license** allows full quotation and modification
- Demonstrates **AGENTS.md routing pattern** for large codebases
- **Prompt caching invariant** is a key architectural constraint
- **Tool search system** enables progressive disclosure of large tool surfaces
- **200+ skills** demonstrate extensibility pattern