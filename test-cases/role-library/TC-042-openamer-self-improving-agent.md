# TC-042: OpenAmer - Self-Improving Autonomous Agent Suite

## Metadata
- **Source Project**: OpenAmer (openamer/openamer)
- **GitHub**: github.com/openamer/openamer
- **License**: Apache-2.0
- **Artifact Type**: Self-improving AI agent for Windows with A2A mesh
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction at commit 0e03ed39e26c6f3da76ad7348089fd6ffea651db
- **Scope**: Self-improving AI agent for Windows with A2A mesh

---

## Project Overview

OpenAmer is a **self-improving AI agent** designed for Windows environments with **A2A (Agent-to-Agent) mesh** capabilities. It features a sophisticated system prompt architecture with three cache tiers (stable, context, volatile) and a comprehensive skill management system.

### Key Characteristics
- **Three-tier prompt cache**: Stable, context, volatile for optimal caching
- **Self-improvement loop**: Background review and learning
- **Skill bundles**: Pre-packaged skill combinations
- **Platform hints**: Platform-specific prompt customization
- **A2A mesh**: Agent-to-Agent communication

---

## Agent Prompts

### 1. System Prompt Architecture

```python
"""System-prompt assembly for :class:`AIAgent`.

The agent's system prompt is built once per session and reused across all
turns — only context compression triggers a rebuild.  This keeps the
upstream prefix cache warm.

Three tiers are joined with ``\\n\\n``:

* ``stable``   — identity (SOUL.md or DEFAULT_AGENT_IDENTITY), tool
  guidance, computer-use guidance, openamer subscription block, tool-use
  enforcement guidance + per-model operational guidance, skills prompt,
  alibaba model-name workaround, environment hints, coding guidance,
  platform hints.
* ``context``  — caller-supplied ``system_message`` plus context files
  (AGENTS.md / .cursorrules / etc.) discovered under ``TERMINAL_CWD``,
  plus the session's coding-workspace snapshot.
* ``volatile`` — memory snapshot, USER.md profile, external memory
  provider block, timestamp/session/model/provider line.
"""
```

### 2. Platform Hints Resolution

```python
def _resolve_platform_hint(agent: Any, platform_key: str, default_hint: str) -> str:
    """Apply a per-platform prompt-hint override to the default hint.

    Reads ``agent._platform_hint_overrides`` (populated from
    ``config.yaml`` ``platform_hints`` by ``agent_init``) and resolves the
    effective hint for *platform_key*:

      * ``replace`` — substitute the default hint entirely.
      * ``append``  — keep the default and append the extra text.
      * a bare string value — treated as ``append`` (convenience shorthand).

    Precedence: ``replace`` wins over ``append`` if both are present.
    Override text is added on top of (not instead of) the SOUL/context/
    memory tiers — it only affects the platform-hint segment.
    """
```

### 3. TUI Embedded Pane Clarifier

```python
_TUI_EMBEDDED_PANE_CLARIFIER = (
    " You're in its embedded terminal pane, beside the GUI chat — the user can "
    "select your output (Option-drag on macOS, Shift-drag elsewhere) and press "
    "Cmd/Ctrl+L to send it to the chat composer."
)
```

---

## Prompt Builder Components

### 1. Tool Use Enforcement

```python
TOOL_USE_ENFORCEMENT_GUIDANCE = """
When using tools, follow these rules:
1. Always validate tool inputs against schemas
2. Handle errors gracefully
3. Report results clearly
"""
```

### 2. Skills Guidance

```python
SKILLS_GUIDANCE = """
Skills provide specialized capabilities:
- Load skills from skill directories
- Use skill bundles for common workflows
- Pre-process skill commands before execution
"""
```

### 3. Memory Guidance

```python
MEMORY_GUIDANCE = """
Memory management:
- Store important information
- Retrieve relevant context
- Update memory as needed
"""
```

---

## Skill Utilities

### 1. Skill Metadata Utilities

```python
"""Lightweight skill metadata utilities shared by prompt_builder and skills_tool.

This module intentionally avoids importing the tool registry, CLI config, or any
heavy dependency chain.  It is safe to import at module level without triggering
tool registration or provider resolution.
"""

# Platform mapping for skill filtering
PLATFORM_MAP = {
    "macos": "darwin",
    "linux": "linux",
    "windows": "win32",
}

# Directories excluded from skill scanning
EXCLUDED_SKILL_DIRS = frozenset(
    (
        ".git",
        ".github",
        ".hub",
        ".archive",
        ".venv",
        "venv",
        "node_modules",
        "site-packages",
        "__pycache__",
        ".tox",
        ".nox",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    )
)

# Supporting files inside skill packages
SKILL_SUPPORT_DIRS = frozenset(("references", "templates", "assets", "scripts"))
```

---

## Available Tools (6 Total)

| Tool | Description |
|------|-------------|
| tool_executor | Execute tool calls |
| tool_dispatch_helpers | Tool dispatch utilities |
| tool_guardrails | Safety constraints for tools |
| skill_manager_tool | Manage skill loading/unloading |
| tool_search | Search available tools |
| mcp_tool_schema | MCP protocol tool schema |

---

## Available Skills (4 Total)

| Skill | Description |
|-------|-------------|
| skill_utils | Skill metadata utilities |
| skill_bundles | Pre-packaged skill combinations |
| skill_commands | Skill command execution |
| skill_preprocessing | Skill command preprocessing |

---

## Evaluation Dimensions

### 1. Three-Tier Cache Architecture
- [ ] Stable tier for identity and guidance
- [ ] Context tier for workspace-specific information
- [ ] Volatile tier for session state
- [ ] Cache warming maintained

### 2. Self-Improvement Loop
- [ ] Background review process
- [ ] Learning from execution
- [ ] Prompt optimization
- [ ] Performance tracking

### 3. Platform Customization
- [ ] Platform hint overrides
- [ ] Replace vs append modes
- [ ] Desktop integration
- [ ] Multi-platform support

### 4. Skill Management
- [ ] Skill loading and unloading
- [ ] Skill bundle support
- [ ] Command preprocessing
- [ ] Exclusion filtering

### 5. A2A Mesh Support
- [ ] Agent-to-Agent communication
- [ ] Mesh networking
- [ ] Collaborative workflows
- [ ] State synchronization

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Three-Tier Cache Architecture | 25% | | |
| Self-Improvement Loop | 20% | | |
| Platform Customization | 20% | | |
| Skill Management | 20% | | |
| A2A Mesh Support | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Cache Architecture Tests
1. Verify stable tier persistence
2. Test context tier updates
3. Validate volatile tier refresh

### Self-Improvement Tests
1. Run background review cycle
2. Test learning from errors
3. Verify prompt optimization

### Platform Hint Tests
1. Test replace mode
2. Test append mode
3. Verify platform detection

### Skill Management Tests
1. Load skill bundle
2. Preprocess skill commands
3. Test skill exclusion filtering

### A2A Mesh Tests
1. Connect agents in mesh
2. Test message passing
3. Verify state synchronization

---

## Notes

- OpenAmer demonstrates sophisticated prompt caching architecture
- Three-tier design optimizes upstream prefix cache warming
- Platform hints enable customization per environment
- Skill bundles provide pre-packaged workflows
- Apache-2.0 license allows full examination and modification
- Good reference for building self-improving agents with A2A mesh