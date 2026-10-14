# TC-060: CowAgent - General Assistant (System-Prompt Builder & Tools)

## Metadata
- **Source Project**: CowAgent (zhayujie/CowAgent)
- **GitHub**: github.com/zhayujie/CowAgent
- **License**: MIT
- **Artifact Type**: General-purpose personal AI assistant — modular system-prompt builder + agent skills/tools
- **Collection Date**: 2026-10-13
- **Collection Method**: GitHub raw-content fetch on branch `master` — `https://raw.githubusercontent.com/zhayujie/CowAgent/master/agent/prompt/builder.py` and `https://raw.githubusercontent.com/zhayujie/CowAgent/master/agent/tools/base_tool.py`; project overview cross-checked against `https://raw.githubusercontent.com/zhayujie/CowAgent/master/README.md`
- **Scope**: The two logical artifacts that define the agent's behaviour surface — the prompt-builder that assembles the system prompt from subsystems (tools, skills, memory, knowledge, workspace, permissions, user identity, project context, runtime), and the `BaseTool` contract every tool implements

---

## Project Overview

CowAgent is an open-source general AI assistant that proactively plans tasks, controls the computer and external services, creates and runs Skills, builds a personal knowledge base and long-term memory, forms multi-agent teams, and grows through self-evolution — described by its authors as a reference implementation of "Agent Harness engineering."

### Key Characteristics
- **Plug-in LLM providers**: any major provider (Claude, GPT, Gemini, DeepSeek, Qwen, GLM, Kimi, MiniMax, Doubao, …), each capability (chat / vision / image / ASR / TTS / embedding) routable independently
- **Multi-channel**: Web console, Telegram, Slack, Discord, WeChat, Feishu, DingTalk, QQ, and more, all served by one Agent instance
- **Modular prompt assembly**: the system prompt is a list of ordered sections built at runtime, not a static string
- **Tools + Skills**: "Tools are atomic capabilities … Skills are higher-level workflows defined by a manifest file that compose multiple tools"
- **Memory & knowledge**: three-tier memory (context → daily → MEMORY.md) with a nightly "Deep Dream" distillation pass, plus a topic-organized Markdown knowledge base
- **Multi-agent teams**: each Agent has its own role, model, skills and knowledge, collaborating in a shared conversation

---

## Agent Prompts

### 1. Modular System-Prompt Builder (`agent/prompt/builder.py`)

The prompt builder assembles the full system prompt from independent subsystems. The canonical section order is documented directly in `build_agent_system_prompt`:

```python
def build_agent_system_prompt(..., **kwargs) -> str:
    """
    Build the agent system prompt.
    Section order (by importance and logical flow):
    1. Tooling - core capabilities, introduced first
    2. Skills - right after tools, since skills are read via the read tool
    3. Memory - memory recall and writing guidance
    3.5 Knowledge - structured knowledge base (injects knowledge/index.md)
    4. Workspace - working environment description
    4.5 Permissions - what this session may change (omitted for full access)
    5. User identity - user info (optional)
    6. Project context - AGENT.md, USER.md, RULE.md, MEMORY.md, BOOTSTRAP.md
    7. Runtime info - meta info (time, model, etc.)
    """
```

The assembly function builds a `sections` list and conditionally emits each block, joining them at the end:

```python
    sections = []
    # 1. Tooling (most important, goes first)
    if tools:
        sections.extend(_build_tooling_section(tools, language))
    # 2. Skills (right after tools, since they need the read tool)
    if skill_manager:
        sections.extend(_build_skills_section(skill_manager, tools, language))
    # 3. Memory (standalone memory capability)
    if memory_manager:
        sections.extend(
            _build_memory_section(memory_manager, tools, language, workspace_dir, project_dir)
        )
    # 3.5 Knowledge (structured knowledge base)
    if conf().get("knowledge", True):
        sections.extend(_build_knowledge_section(workspace_dir, language, project_dir))
    # 4. Workspace ...
    ...
    # 8. Response language (always appended, independent of the skeleton language)
    sections.extend(_build_response_language_section(language))
    return "\n".join(sections)
```

### 2. Tooling Section (English branch of `_build_tooling_section`)

```python
    if is_en:
        lines = [
            "## 🔧 Tooling",
            "",
            "Available tools (names are case-sensitive, call exactly as listed):",
            "\n".join(tool_lines),
            "",
            "Tool-calling style:",
            "",
            "- For multi-step tasks, complex decisions or sensitive operations, briefly explain what you are doing and why, so the user follows key progress",
            "- Never just announce intent and stop: if you say you will do something, actually call the tool in the same turn. A text-only reply ends the turn, so only reply with plain text once the work is genuinely finished",
            "- Keep going until the task is done, then report the result to the user",
            "- Always redact secrets, tokens and other sensitive info in replies",
            "- Put URLs directly in the reply text; the system handles and renders them. Don't download and re-send them via the send tool",
            "",
        ]
        if has_subagent:
            lines.insert(
                -1,
                "- Hand a self-contained task that needs research, search or information gathering to `subagent`: one task, or several at once via tasks running in parallel; it brings back the conclusion",
            )
```

Each available tool is listed with a one-line summary from a fixed `core_summaries` map (e.g. `read`: "read file content", `write`: "create or overwrite a file", `web_search`: "web search", `subagent`: "hand a self-contained task to a sub agent and get back only its conclusion"), and the display order is pinned by an explicit `tool_order` list.

### 3. Skills Section (English branch of `_build_skills_section`)

```python
    if language == "en":
        lines = [
            "## 🧩 Skills (mandatory)",
            "",
            "Before replying: scan the <description> of every skill in <available_skills> below.",
            "",
            f"- If a skill's description matches the user's need: use the `{read_tool_name}` tool to read the SKILL.md at its <location> path, then strictly follow the instructions in the file. "
            "Prefer using a skill when one matches.",
            "- If multiple skills apply, pick the best-matching one, then read and follow it.",
            "- If no skill clearly applies: do not read any SKILL.md, just use the general tools.",
            "",
            f"**Important**: skills are not tools and cannot be called directly. The only way to use a skill is to read its SKILL.md with `{read_tool_name}`, then act on the file's content. "
            "Never read multiple skills at once — only read one after selecting it.",
            "",
            "Available skills:"
        ]
```

The section ends by appending the list produced by `skill_manager.build_skills_prompt()`, so the enumerable skill index is owned by the skill subsystem, not the builder.

### 4. Response-Language Section (`_build_response_language_section`)

```python
def _build_response_language_section(language: str) -> List[str]:
    if language == "en":
        return [
            "## 🌐 Response language",
            "",
            "By default, reply in the same language as the user's input, "
            "unless the user explicitly asks for another language.",
            "",
        ]
    ...
```

---

## Skill Definitions

### 1. Tool Contract — `BaseTool` (`agent/tools/base_tool.py`)

Skills and the agent loop both rest on a single tool base class. Its class-level contract defines lifecycle, availability, cancellation and concurrency:

```python
class BaseTool:
    """Base class for all tools."""
    # Default decision stage is pre-process
    stage = ToolStage.PRE_PROCESS
    # Class attributes must be inherited
    name: str = "base_tool"
    description: str = "Base tool"
    params: dict = {}  # Store JSON Schema
    ...
    # Whether several calls to this tool in one turn may run at the same time.
    # Off by default: the agent loop runs tools in the order the model asked
    # for them, and most tools are written expecting exactly that. Turn it on
    # only for work that is independent by construction and slow enough that
    # queueing it is the dominant cost.
    parallel_safe: bool = False
```

Two decision stages gate whether a tool is chosen by the agent or fires automatically after the final answer:

```python
class ToolStage(Enum):
    """Enum representing tool decision stages"""
    PRE_PROCESS = "pre_process"  # Tools that need to be actively selected by the agent
    POST_PROCESS = "post_process"  # Tools that automatically execute after final_answer
```

The tool result deliberately separates the machine-facing and person-facing views:

```python
class ToolResult:
    """Tool execution result
    ``result`` is what the model reads, so it is written for a model: JSON,
    exit codes, whatever parses cleanly. ``display`` is the same outcome
    written for a person, and clients render it instead when it is set.
    """
```

Argument coercion is centralised so each tool only validates its own range:

```python
    def _coerce_integer_args(self, params):
        """Models often quote integers ("offset": "2"); convert every argument the
        schema declares as an integer, so each tool only checks its own range."""
```

The schema exposed to the model is bound to the instance, not the class, so runtime-dependent tools can override name/wording/parameters:

```python
    def get_json_schema(self) -> dict:
        """The tool as the model sees it.
        Bound to the instance, not the class, so a tool whose name, wording or
        parameters depend on runtime state can override any of them in
        __init__ and have both this and the agent loop's direct read of
        `.description` agree.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.params
        }
```

Availability and card-rendering checks "err towards offering the capability": a check that throws returns `True` (available) and a failed card check returns `False` (fall back to the generic card), logging a debug line rather than removing a capability.

### 2. Available Skills (per README)

| Skill surface | Description |
|-------|-------------|
| Skill Hub | Open skill marketplace — browse, search, install in one click |
| GitHub / ClawHub / URL | Install skills from any source |
| `skill-creator` | Conversational authoring — generate custom skills through dialogue |
| Built-in commands | `/skill list`, `/skill search <keyword>`, `/skill install <name>` |

Built-in tools enumerated in the README cover file I/O (`read` / `write` / `edit` / `ls`), terminal (`bash`), file sending (`send`), memory retrieval (`memory`), environment variables (`env_config`), web fetching (`web_fetch`), scheduling (`scheduler`), web search (`web_search`), vision (`vision`) and browser automation (`browser`) — the same names the tooling section summarises.

---

## Evaluation Dimensions

### 1. Prompt Modularity
- [ ] System prompt is assembled from independent, individually-testable sections
- [ ] Section order is explicit and justified by logical flow
- [ ] Each section can be omitted cleanly when its subsystem is absent

### 2. Instruction Quality
- [ ] Tool-calling style rules are actionable (no "announce and stop")
- [ ] Skill-selection rule is unambiguous ("read one SKILL.md, then act")
- [ ] Sensitive-information handling (redaction) is stated explicitly

### 3. Internationalisation
- [ ] English and Chinese branches carry identical semantics
- [ ] Response-language rule is decoupled from the prompt skeleton language
- [ ] Tool summaries are localised rather than hard-coded in one language

### 4. Tool Contract Design
- [ ] Base class defines lifecycle, availability, cancellation and concurrency
- [ ] Model-facing vs person-facing result views are separated (`result` / `display`)
- [ ] Integer-argument coercion is centralised; per-tool validation stays local
- [ ] Graceful degradation: failing availability/card checks do not drop capabilities

### 5. Extensibility & Security
- [ ] New tools/skills can be added without touching the builder core
- [ ] Secrets/tokens are explicitly redacted in replies
- [ ] Parallel execution is opt-in and documented as a deliberate choice

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Prompt Modularity | 25% | | |
| Instruction Quality | 20% | | |
| Internationalisation | 15% | | |
| Tool Contract Design | 25% | | |
| Extensibility & Security | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Prompt Assembly Tests
1. Build a prompt with each subsystem present and absent; verify section order matches the documented sequence
2. Confirm the response-language section is always appended regardless of skeleton language
3. Verify the `subagent` delegation line appears only when the `subagent` tool is available

### Localisation Tests
1. Diff the English and Chinese branches of the tooling and skills sections for semantic parity
2. Confirm tool summaries fall back to the bare tool name when no summary is defined

### Tool Contract Tests
1. Feed quoted-integer arguments (`{"offset": "2"}`) and confirm coercion succeeds; feed a non-integer and confirm a typed failure
2. Force `is_available()` / `renders_own_cards()` to raise and confirm the tool is still offered / falls back to the generic card
3. Verify a tool exception inside `execute` becomes a failed `ToolResult`, never `None`
4. Confirm `parallel_safe` defaults to off and only opt-in tools run concurrently

---

## Notes

- **MIT license** permits full quotation and modification.
- CowAgent is a **general-purpose personal assistant**, not a coding agent: its artifacts are about tool orchestration, memory, knowledge and skills, so it exercises the non-code agent path of this library.
- The prompt builder is a good example of **runtime-composed system prompts**: the prompt is data (a list of sections) rather than a fixed template.
- The `BaseTool` contract is a strong reference for **tool-facing UI concerns** (`result` for the model, `display` for the human) and for **fail-open capability checks**.
- The Chinese-language branches exist in the source (`language == "zh"`); this case quotes only the English branches and describes the rest in English to keep the document single-language.
