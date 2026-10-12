# TC-022: AG2 (AutoGen) - Multi-Agent Suite

## Metadata
- **Source Project**: AG2 (ag2ai/ag2)
- **Commit SHA**: 2b8636381b2235e7d77d181a35fbd241d15fe3f1
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent Framework
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

AG2 is the **next-generation multi-agent framework** that evolved from Microsoft AutoGen. It provides a streamlined Agent abstraction with built-in tool management, prompt-based structured output, and provider-agnostic tool schemas.

### Core Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Agent Class** | Core agentic unit with model loop and tool invocation | System Prompt + Tool Schema |
| **PromptedSchema** | Prompt-based structured output for models without native support | System Prompt |
| **ShellTool** | Provider-executed server-side shell commands | Tool Schema |
| **WebSearchTool** | Provider-executed web search | Tool Schema |
| **CodeExecutionTool** | Provider-neutral code execution | Tool Schema |
| **SkillsTool** | Provider-side skills activation | Tool Schema |

---

## Logical Artifact Inventory

### 1. System Prompts (2)

#### 1.1 Agent Core Prompt Management
```python
# ag2/agent.py

"""Agent — the agentic unit of ag2.

An ``Agent`` runs a model loop, invokes tools, honours middleware, surfaces
events through observers, and optionally runs the harness primitives
(assembly policies, compaction/aggregation, knowledge store, subtask
spawning).

A bare ``Agent(name, config=cfg)`` has zero harness middleware — it behaves
exactly like a plain LLM loop. Harness features are opt-in: pass ``assembly=``
for context policies, ``knowledge=KnowledgeConfig(...)`` for a knowledge store,
or ``tasks=TaskConfig(...)`` to enable subtask spawning (disabled by default).
"""

@dataclass
class TaskConfig:
    """Groups task-spawning Agent parameters.

    By default a subtask Agent inherits **all** of the parent's user-supplied
    tools (everything passed via ``tools=``). Subtask Agents never receive the
    auto-injected ``run_subtask`` / ``run_subtasks`` tools, so recursive
    delegation is structurally impossible — no depth limiting required.

    Use ``include_tools`` (allowlist) and ``exclude_tools`` (blocklist) to
    narrow what the subtask sees, and ``extra_tools`` to add capabilities the
    parent doesn't have. ``max_concurrency`` optionally bounds the total
    number of sub-tasks running for this Agent across both spawning tools.
    """

    config: ModelConfig | None = None
    prompt: str = "You are a task agent. Complete the assigned task thoroughly and concisely. Return only the result."
    include_tools: Iterable[str] | None = None
    exclude_tools: Iterable[str] = ()
    extra_tools: Iterable[Callable[..., Any] | Tool] = ()
    max_concurrency: int | None = None
```

#### 1.2 PromptedSchema (Prompt-Based Structured Output)
```python
# ag2/response/prompted.py

_DEFAULT_PROMPT_TEMPLATE = (
    "You must respond with valid JSON that conforms to the following JSON schema:\n"
    "```json\n"
    "{schema}\n"
    "```\n"
    "Do not include any text, markdown formatting, or explanation outside the JSON object."
)


class PromptedSchema(ResponseProto[T]):
    """Response schema that uses prompt-based instructions instead of native API structured output.

    Use this for models or providers that do not support built-in structured output
    (e.g., ``response_format``). The JSON schema is injected into the system prompt,
    instructing the model to return valid JSON matching the schema. Validation is
    still performed using the inner schema's ``validate`` method.

    Examples:
        Using with a type directly::

            agent = Agent(..., response_schema=PromptedSchema(MyModel))

        Wrapping an existing ResponseProto::

            schema = ResponseSchema(int | str)
            agent = Agent(..., response_schema=PromptedSchema(schema))
    """

    @overload
    def __init__(
        self,
        inner: ResponseProto[T],
        /,
        *,
        prompt_template: str | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        inner: type[T],
        /,
        *,
        prompt_template: str | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        inner: ClassInfo,
        /,
        *,
        prompt_template: str | None = None,
    ) -> None: ...

    def __init__(
        self,
        inner: "ResponseProto[T] | type[T] | ClassInfo",
        /,
        *,
        prompt_template: str | None = None,
    ) -> None:
        self._inner = ResponseSchema[T].ensure_schema(inner)

        self.name = self._inner.name
        self.description = self._inner.description

        self._json_schema = self._inner.json_schema
        self._prompt_template = prompt_template or _DEFAULT_PROMPT_TEMPLATE
        if self._json_schema:
            schema_str = json.dumps(self._json_schema, indent=2)
            self.system_prompt = self._prompt_template.format(schema=schema_str)
        else:
            self.system_prompt = None

        # Set public property to None to avoid native JSON schema validation
        self.json_schema = None
```

---

### 2. Tool Schemas (4)

#### 2.1 ShellTool (Server-Side Shell Execution)
```python
# ag2/tools/builtin/shell.py

SHELL_TOOL_NAME = "shell"


@dataclass(slots=True)
class ShellToolSchema(ToolSchema):
    """Provider-neutral capability flag for provider-executed shell.

    Currently only OpenAI Responses API executes shell server-side.
    Anthropic's bash tool is client-side and is rejected with
    :class:`~ag2.exceptions.UnsupportedToolError` — use
    :class:`~ag2.tools.SandboxShellTool` instead.
    """

    type: str = field(default=SHELL_TOOL_NAME, init=False)
    version: Literal["bash_20250124"] = "bash_20250124"
    environment: ShellEnvironment | None = None


class ShellTool(Tool):
    """Shell execution tool — provider-executed server-side.

    Provider support:

    - **OpenAI Responses API** — maps to ``shell``. Use ``environment`` to
      control where commands execute: ``ContainerAutoEnvironment``,
      ``ContainerReferenceEnvironment``.

    - **Anthropic** — NOT supported. Claude's ``bash`` tool is a client-side
      tool (the application must execute the command and return the result).
      Using ``ShellTool`` with ``AnthropicConfig`` raises
      :class:`~ag2.exceptions.UnsupportedToolError`. Use
      :class:`~ag2.tools.SandboxShellTool` instead, which runs
      commands via subprocess and works with any provider.
    """
```

#### 2.2 WebSearchTool (Provider Web Search)
```python
# ag2/tools/builtin/web_search.py

WEB_SEARCH_TOOL_NAME = "web_search"


@dataclass(slots=True)
class UserLocation:
    city: str | None = None
    region: str | None = None
    country: str | None = None
    timezone: str | None = None


@dataclass(slots=True)
class WebSearchToolSchema(ToolSchema):
    type: str = field(default=WEB_SEARCH_TOOL_NAME, init=False)
    search_context_size: Literal["low", "medium", "high"] | None = None
    max_uses: int | None = None
    user_location: UserLocation | None = None
    allowed_domains: list[str] | None = None
    blocked_domains: list[str] | None = None
    web_search_version: Literal["web_search_20250305", "web_search_20260209", "web_search_20260318"] = (
        "web_search_20250305"
    )


class WebSearchTool(Tool):
    __slots__ = ()
```

*(Note — the four builtin tools quoted here are a selection; `ag2/tools/builtin/` also provides AnthropicBashTool, FileSearchTool, GoogleMapsTool, WebFetchTool, MCPServerTool, ToolSearchTool, ImageGenerationTool, XSearchTool, MemoryTool, and RetrievalTool, plus `SandboxShellTool` in ag2/tools/shell/tool.py.)*

#### 2.3 CodeExecutionTool (Provider-Neutral Code Execution)
```python
# ag2/tools/builtin/code_execution.py

CODE_EXECUTION_TOOL_NAME = "code_execution"

CodeExecutionVersions: TypeAlias = Literal[
    "code_execution_20250825",
    "code_execution_20260120",
    "code_execution_20260521",
]


@dataclass(slots=True)
class CodeExecutionToolSchema(ToolSchema):
    """Provider-neutral capability flag for code execution."""

    type: str = field(default=CODE_EXECUTION_TOOL_NAME, init=False)
    version: CodeExecutionVersions = "code_execution_20250825"


class CodeExecutionTool(Tool):
    """Provider-neutral code execution capability.

    Each LLM client's mapper is responsible for converting this schema
    into the correct provider-specific API format.
    """
```

#### 2.4 SkillsTool (Provider-Side Skills)
```python
# ag2/tools/builtin/skills.py

@dataclass(slots=True)
class Skill:
    """A reference to a provider-managed skill.

    Args:
        id: Skill identifier. Provider-specific:

            - Anthropic first-party skills: ``"pptx"``, ``"xlsx"``, ``"docx"``, ``"pdf"``.
            - OpenAI system skills carry the ``openai-`` prefix
              (e.g. ``"openai-spreadsheets"``); bare ids like ``"spreadsheet"``
              are rejected with 404 "System skill not found".
            - Custom skill ids as returned by the provider's skills API
              (e.g. ``"skill_abc123"``).
        version: Version pin, always a string:

            - Anthropic: a version date such as ``"20251013"`` or ``"latest"``.
              ``None`` is sent as ``"latest"``.
            - OpenAI: a positive-integer string such as ``"2"`` or ``"latest"``.
              ``None`` omits the field, meaning the skill's ``default_version``.
    """

    id: str
    version: str | None = None


SKILLS_TOOL_NAME = "skills"


@dataclass(slots=True)
class SkillsToolSchema(ToolSchema):
    """Provider-neutral capability flag for provider-side skills.

    Skills are passed to the provider via a separate API parameter
    (``container`` for Anthropic, the hosted shell tool's
    ``environment.skills`` for OpenAI Responses).
    They never appear as standalone entries in the ``tools[]`` array.
    """

    type: str = field(default=SKILLS_TOOL_NAME, init=False)
    skills: list[Skill] = field(default_factory=list)


class SkillsTool(Tool):
    """Declares provider-side skills to be activated for this agent.

    Accepts skill identifiers as plain strings (shorthand for the provider's
    default version) or :class:`Skill` objects when a specific version is
    required. Skills are executed server-side by the provider — no local
    executor is registered.

    Provider support:

    - **Anthropic** — skills ride the ``container`` API parameter as
      ``{"type": "anthropic", "skill_id": ..., "version": ...}`` entries; they
      never appear in ``tools[]``. Skills run inside the code-execution
      container, so a :class:`~ag2.tools.CodeExecutionTool` is added
      automatically when missing.

    - **OpenAI Responses API** — skills attach to the hosted shell tool as
      ``skill_reference`` entries in its ``container_auto`` environment; a
      ``{"type": "shell"}`` tool is appended automatically when missing.

    Example::

        # Anthropic: first-party skills, auto-adds CodeExecutionTool
        agent = Agent(
            name="analyst",
            config=AnthropicConfig(model="claude-sonnet-5", ...),
            tools=[SkillsTool("pptx", Skill("xlsx", version="latest"))],
        )

        # OpenAI Responses: system skills use the "openai-" prefix,
        # auto-adds the hosted shell tool
        agent = Agent(
            name="analyst",
            config=OpenAIResponsesConfig(model="gpt-5.4", ...),
            tools=[SkillsTool("openai-spreadsheets")],
        )
    """
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Single Agent class with configurable behavior
- [ ] Clear separation between agent, tools, and response schemas
- [ ] TaskConfig for subtask spawning with explicit tool inheritance rules

### 2. Workflow Completeness
- [ ] Model loop with tool invocation
- [ ] Middleware support for custom workflows
- [ ] Observer pattern for event handling

### 3. Prompt Consistency
- [ ] Standardized prompt template for structured output
- [ ] Configurable system prompts
- [ ] JSON schema injection for non-native providers

### 4. Tool Modularity
- [ ] Provider-agnostic tool schemas
- [ ] Version-specific tool configurations
- [ ] Skills as first-class tool type

### 5. Observability
- [ ] Event streaming through observers
- [ ] Usage tracking and reporting
- [ ] Context management

### 6. Extensibility
- [ ] Custom tool creation via Tool base class
- [ ] Response schema customization
- [ ] Middleware injection points

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|-----------|--------|-------------|-------|
| Role Clarity | 20% | | |
| Workflow Completeness | 25% | | |
| Prompt Consistency | 15% | | |
| Tool Modularity | 20% | | |
| Observability | 10% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### End-to-End Tests
1. **Multi-provider tool execution**: Test ShellTool and WebSearchTool across OpenAI and Anthropic
2. **Structured output**: Verify PromptedSchema with models lacking native support
3. **Skills activation**: Test provider-side skills (Anthropic pptx, OpenAI spreadsheets)

### Unit Tests
1. **Tool schema generation**: Verify correct schema for each provider
2. **Response validation**: Test PromptedSchema JSON validation
3. **TaskConfig**: Verify subtask tool inheritance rules

### Integration Tests
1. **Provider switching**: Test agent with same tools across different providers
2. **Skill activation**: Verify automatic tool injection (CodeExecutionTool for Anthropic)
3. **Environment configuration**: Test ContainerAutoEnvironment and ContainerReferenceEnvironment

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- AG2 is the **successor to Microsoft AutoGen** with a simplified architecture
- Provider-agnostic design enables **seamless provider switching**
- SkillsTool enables **first-party provider skills** (pptx, xlsx, etc.)