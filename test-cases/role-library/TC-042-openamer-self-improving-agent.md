# TC-042: OpenAmer - Self-Improving Autonomous Agent Suite

## Metadata
- **Source Project**: OpenAmer (openamer/openamer)
- **GitHub**: github.com/openamer/openamer
- **License**: Apache-2.0 (with a commercial dual-license tier for larger companies per LICENSE.md)
- **Artifact Type**: Self-improving AI agent for Windows with A2A mesh
- **Collection Date**: 2026-10-12
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
# Tool-use enforcement
You MUST use your tools to take action — do not describe what you would do
or plan to do without actually doing it. When you say you will perform an
action (e.g. 'I will run the tests', 'Let me check the file', 'I will create
the project'), you MUST immediately make the corresponding tool call in the same
response. Never end your turn with a promise of future action — execute it now.
Keep working until the task is actually complete. Do not stop with a summary of
what you plan to do next time. If you have tools available that can accomplish
the task, use them instead of telling the user what you would do.
Every response should either (a) contain tool calls that make progress, or
(b) deliver a final result to the user. Responses that only describe intentions
without acting are not acceptable.
"""
```

### 2. Skills Guidance

```python
SKILLS_GUIDANCE = """
After completing a complex task (5+ tool calls), fixing a tricky error,
or discovering a non-trivial workflow, save the approach as a
skill with skill_manage so you can reuse it next time.
When using a skill and finding it outdated, incomplete, or wrong,
patch it immediately with skill_manage(action='patch') — don't wait to be asked.
Skills that aren't maintained become liabilities.

## Skill Safety Rule
1. **UNAVAILABLE** — If a skill placeholder contains `[SKILL_PRUNED]`, the skill content was lost in compression and is inaccessible.
2. **RELOAD** — Before performing any action that depends on a skill, re-check its content with `skill_view(name='...')` if it shows `[SKILL_PRUNED]`.
3. **WAIT** — If a skill is loading or was just pruned, wait for the reload confirmation before proceeding.
4. **DEDUP** — After reloading a pruned skill, **ignore any remaining `[SKILL_PRUNED]` markers for that same skill** — they are historical artifacts from previous compactions and do not need further action.
"""
```

### 3. Memory Guidance

```python
MEMORY_GUIDANCE = """
You have persistent memory across sessions. Save durable facts using the memory
tool: user preferences, environment details, tool quirks, and stable conventions.
Memory is injected into every turn, so keep it compact and focused on facts that
will still matter later.
Prioritize what reduces future user steering — the most valuable memory is one
that prevents the user from having to correct or remind you again.
User preferences and recurring corrections matter more than procedural task details.
Do NOT save task progress, session outcomes, completed-work logs, or temporary TODO
state to memory; use session_search to recall those from past transcripts.
Specifically: do not record PR numbers, issue numbers, commit SHAs, 'fixed bug X',
'submitted PR Y', 'Phase N done', file counts, or any artifact that will be stale
in 7 days. If a fact will be stale in a week, it does not belong in memory.
If you've discovered a new way to do something, solved a problem that could be
necessary later, save it as a skill with the skill tool.
Write memories as declarative facts, not instructions to yourself.
'User prefers concise responses' ✓ — 'Always respond concisely' ✗.
'Project uses pytest with xdist' ✓ — 'Run tests with pytest -n 4' ✗.
Imperative phrasing gets re-read as a directive in later sessions and can
cause repeated work or override the user's current request. Procedures and
workflows belong in skills, not memory.
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

## Tool / Prompt-Infrastructure Modules (examples — not an exhaustive inventory)

*(Note — `tools/` alone holds 122 Python modules plus subpackages (asi/, computer_use/, environments/); the agent additionally exposes dozens of model-facing tools such as terminal, file, browser, kanban_*, memory, session_search, delegate, and computer-use. The six modules below are prompt-infrastructure examples.)*

| Module | Description |
|------|-------------|
| tool_executor | Execute tool calls |
| tool_dispatch_helpers | Tool dispatch utilities |
| tool_guardrails | Safety constraints for tools |
| skill_manager_tool | Manage skill loading/unloading |
| tool_search | Search available tools |
| mcp_tool_schema | MCP protocol tool schema |

---

## Skill-Management Modules (examples — not agent-facing skills)

*(Note — the agent itself ships 245 bundled SKILL.md files under `skills/` plus 116 under `optional-skills/` at this commit; the four modules below are internal skill-management infrastructure.)*

| Module | Description |
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