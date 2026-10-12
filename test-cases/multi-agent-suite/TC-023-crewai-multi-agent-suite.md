# TC-023: CrewAI - Multi-Agent Suite

## Metadata
- **Source Project**: CrewAI (crewAIInc/crewAI)
- **Commit SHA**: 74fe931a39007c1ff7540c013f30ba2496c3148e
- **License**: MIT
- **Artifact Type**: Multi-Agent Framework
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

CrewAI is a **role-playing multi-agent framework** that enables building autonomous AI teams through role-based agent definitions. Each agent has specific roles, goals, and tools, working together as a crew to accomplish complex tasks.

### Core Agent Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Role-Playing Prompts** | Agent role definition and task execution prompts | System Prompt |
| **Agent Tools** | Delegate work, ask questions, and collaborate | Tool Schema |
| **External Tools** | Integration with external services (Brave Search, etc.) | Tool Schema |

---

## Logical Artifact Inventory

### 1. System Prompts (2)

#### 1.1 Role-Playing Prompt Templates
```python
# lib/crewai/src/crewai/utilities/prompts.py

class Prompts(BaseModel):
    """Manages and generates prompts for a generic agent.

    Notes:
        - Need to refactor so that prompt is not tightly coupled to agent.
    """

    has_tools: bool = Field(
        default=False, description="Indicates if the agent has access to tools"
    )
    use_native_tool_calling: bool = Field(
        default=False,
        description="Whether to use native function calling instead of ReAct format",
    )
    system_template: str | None = Field(
        default=None, description="Custom system prompt template"
    )
    prompt_template: str | None = Field(
        default=None, description="Custom user prompt template"
    )
    response_template: str | None = Field(
        default=None, description="Custom response prompt template"
    )
    use_system_prompt: bool = Field(
        default=False,
        description="Whether to use the system prompt when no custom templates are provided",
    )
    agent: Any = Field(description="Reference to the agent using these prompts")
    skill_loader_tool_name: str | None = Field(
        default=None,
        description="Name the runtime skill loader tool is registered under",
    )

    def task_execution(self) -> SystemPromptResult | StandardPromptResult:
        """Generate a standard prompt for task execution.

        Returns:
            A dictionary containing the constructed prompt(s).
        """
        slices: list[COMPONENTS] = ["role_playing"]
        if self.has_tools:
            if not self.use_native_tool_calling:
                slices.append("tools")
        else:
            slices.append("no_tools")
        system: str = (
            self._build_prompt(slices)
            + self._build_skill_block()
            + self._build_date_block()
        )

        task_slice: COMPONENTS
        if self.use_native_tool_calling:
            task_slice = "native_task"
        elif self.has_tools:
            task_slice = "task"
        else:
            task_slice = "task_no_tools"
        slices.append(task_slice)

        if (
            not self.system_template
            and not self.prompt_template
            and self.use_system_prompt
        ):
            return SystemPromptResult(
                system=system,
                user=self._build_prompt([task_slice]),
                prompt=self._build_prompt(slices)
                + self._build_skill_block()
                + self._build_date_block(),
            )
        return StandardPromptResult(
            prompt=self._build_prompt(
                slices,
                self.system_template,
                self.prompt_template,
                self.response_template,
            )
            + self._build_skill_block()
            + self._build_date_block()
        )

    def _build_skill_block(self) -> str:
        """Render always-on instructions and the available skill catalog.

        Metadata-only skills remain a stable prompt-cache anchor. Their full
        instructions are disclosed through the runtime loader tool only when the
        model determines that a skill applies to the current request.
        """
        skills = getattr(self.agent, "skills", None)
        if not skills:
            return ""

        from crewai.skills.loader import build_skill_catalog, format_skill_context
        from crewai.skills.models import INSTRUCTIONS, Skill
        from crewai.skills.tool import LOAD_SKILL_TOOL_NAME

        loaded = [skill for skill in skills if isinstance(skill, Skill)]
        active = [
            format_skill_context(skill)
            for skill in loaded
            if skill.disclosure_level >= INSTRUCTIONS
        ]
        catalog = build_skill_catalog(loaded)

        blocks: list[str] = []
        if active:
            blocks.append("<skills>\n" + "\n\n".join(active) + "\n</skills>")
        if catalog:
            loader = self.skill_loader_tool_name or LOAD_SKILL_TOOL_NAME
            entries = "\n\n".join(
                format_skill_context(skill, label=label)
                for label, skill in catalog.items()
            )
            blocks.append(
                "<available_skills>\n"
                "These skills are not loaded. Most requests need none of them, "
                "so answer directly unless one clearly applies to this request. "
```

#### 1.2 Hierarchical Manager Agent Prompts
```python
# lib/crewai/src/crewai/translations/en.json (Referenced)

# The translations file contains prompt templates for:
# - Hierarchical manager agents
# - Memory and reasoning prompts
# - Planning prompts
# - Task delegation prompts
```

---

### 2. Tool Schemas (2)

#### 2.1 Agent Tools (Collaboration)
```python
# lib/crewai/src/crewai/tools/agent_tools/agent_tools.py

class AgentTools:
    """Manager class for agent-related tools"""

    def __init__(self, agents: Sequence[BaseAgent]) -> None:
        self.agents = agents

    def tools(self) -> list[BaseTool]:
        """Get all available agent tools"""
        coworkers = ", ".join([f"{agent.role}" for agent in self.agents])

        delegate_tool = DelegateWorkTool(
            agents=self.agents,
            description=I18N_DEFAULT.tools("delegate_work").format(coworkers=coworkers),  # type: ignore
        )

        ask_tool = AskQuestionTool(
            agents=self.agents,
            description=I18N_DEFAULT.tools("ask_question").format(coworkers=coworkers),  # type: ignore
        )

        return [delegate_tool, ask_tool]
```

#### 2.2 Brave Search Tool (External Integration)

*(Note — the quoted tools are a selection: `lib/crewai/src/crewai/tools/agent_tools/` also provides `AddImageTool` and `ReadFileTool`, and the `brave_search_tool` package ships brave_web/news/video/image/local_pois/llm_context variants.)*

```python
# lib/crewai-tools/src/crewai_tools/tools/brave_search_tool/brave_search_tool.py

FreshnessPreset = Literal["pd", "pw", "pm", "py"]
FreshnessRange = Annotated[
    str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}to\d{4}-\d{2}-\d{2}$")
]
Freshness = FreshnessPreset | FreshnessRange
SafeSearch = Literal["off", "moderate", "strict"]


class BraveSearchTool(BaseTool):
    """A tool that performs web searches using the Brave Search API."""

    name: str = "Brave Search"
    description: str = (
        "A tool that performs web searches using the Brave Search API. "
        "Results are returned as structured JSON data."
    )
    args_schema: type[BaseModel] = WebSearchParams
    search_url: str = "https://api.search.brave.com/res/v1/web/search"
    n_results: int = 10
    save_file: bool = False
    env_vars: list[EnvVar] = Field(
        default_factory=lambda: [
            EnvVar(
                name="BRAVE_API_KEY",
                description="API key for Brave Search",
                required=True,
            ),
        ]
    )
    # Rate limiting parameters
    _last_request_time: ClassVar[float] = 0
    _min_request_interval: ClassVar[float] = 1.0  # seconds

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if "BRAVE_API_KEY" not in os.environ:
            raise ValueError(
                "BRAVE_API_KEY environment variable is required for BraveSearchTool"
            )

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        current_time = time.time()
        if (current_time - self._last_request_time) < self._min_request_interval:
            time.sleep(
                self._min_request_interval - (current_time - self._last_request_time)
            )
        BraveSearchTool._last_request_time = time.time()

        try:
            # Fallback to "query" or "search_query" for backwards compatibility
            query = kwargs.get("q") or kwargs.get("query") or kwargs.get("search_query")
            if not query:
                raise ValueError("Query is required")

            payload = {"q": query}

            if country := kwargs.get("country"):
                payload["country"] = country

            # Fallback to "search_language" for backwards compatibility
            if search_lang := kwargs.get("search_lang") or kwargs.get("search_language"):
                payload["search_lang"] = search_lang

            # Fallback to deprecated n_results parameter if no count is provided
            count = kwargs.get("count")
            if count is not None:
                payload["count"] = count
            else:
                payload["count"] = self.n_results

            # Offset may be 0, so avoid truthiness check
            offset = kwargs.get("offset")
            if offset is not None:
                payload["offset"] = offset

            if safesearch := kwargs.get("safesearch"):
                payload["safesearch"] = safesearch

            save_file = kwargs.get("save_file", self.save_file)
            if freshness := kwargs.get("freshness"):
                payload["freshness"] = freshness
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Agents defined by role, goal, and backstory
- [ ] Clear role-based task assignment
- [ ] Hierarchical manager agent support

### 2. Workflow Completeness
- [ ] Sequential and parallel task execution
- [ ] Agent collaboration through delegation tools
- [ ] Skill system for reusable capabilities

### 3. Prompt Consistency
- [ ] Standardized prompt templates
- [ ] I18N support for multiple languages
- [ ] Custom template support

### 4. Tool Modularity
- [ ] BaseTool abstraction for tool creation
- [ ] Agent-to-agent communication tools
- [ ] External service integrations

### 5. Observability
- [ ] Task execution tracking
- [ ] Agent output logging
- [ ] Error handling and retry

### 6. Extensibility
- [ ] Custom tool creation
- [ ] Custom prompt templates
- [ ] Skill system for reusable behaviors

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
1. **Crew execution**: Create a crew with multiple roles and test task completion
2. **Delegation workflow**: Test agent-to-agent delegation
3. **Hierarchical mode**: Test manager agent coordinating worker agents

### Unit Tests
1. **Prompt generation**: Verify correct prompt assembly for different configurations
2. **Tool execution**: Test delegate_work and ask_question tools
3. **Skill loading**: Test skill disclosure and runtime loading

### Integration Tests
1. **External tools**: Test BraveSearchTool integration
2. **Multi-language**: Verify I18N prompt generation
3. **Custom templates**: Test system_template and prompt_template customization

---

## Notes

- **MIT license** allows full quotation and modification
- CrewAI emphasizes **role-playing paradigm** for agent definition
- The skill system provides **lazy-loaded capabilities** with disclosure levels
- Agent tools enable **peer-to-peer collaboration** within crews