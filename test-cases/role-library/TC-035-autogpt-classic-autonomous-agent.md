# TC-035: AutoGPT Classic - Autonomous Task Agent Suite

## Metadata
- **Source Project**: AutoGPT Classic (Significant-Gravitas/AutoGPT)
- **GitHub**: github.com/Significant-Gravitas/AutoGPT
- **License**: MIT
- **Artifact Type**: Autonomous Agent prompt strategies and tool definitions
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction at commit ca1451c907c70557f8eacfd4c476f1a07afae3b7
- **Scope**: Classic Agent; its registered prompt-strategy alternatives and explicitly mounted Forge command components

---

## Project Overview

AutoGPT Classic is one of the pioneering autonomous AI agent frameworks. It features **multiple prompt strategies** that can be selected for different agent behaviors, along with a comprehensive **Forge component system** that provides tools for file management, web browsing, code execution, and more.

### Key Characteristics
- **7 selectable prompt strategies** sharing one Agent (one_shot is default)
- **18+ tool components** via the Forge architecture
- **Strategy-based behavior**: Different reasoning patterns (one-shot, tree-of-thoughts, reflexion, etc.)

---

## Agent Prompt Strategies

### 1. One-Shot Strategy (Default)

```python
class OneShotAgentPromptConfiguration(SystemConfiguration):
    DEFAULT_BODY_TEMPLATE: str = (
        "## Constraints\n"
        "You operate within the following constraints:\n"
        "{constraints}\n"
        "\n"
        "## Resources\n"
        "You can leverage access to the following resources:\n"
        "{resources}\n"
        "\n"
        "## Commands\n"
        "These are the ONLY commands you can use."
        " Any action you perform must be possible through one of these commands:\n"
        "{commands}\n"
        "\n"
        "## Best practices\n"
        "{best_practices}\n"
        "\n"
        "## Efficiency Guidelines\n"
        "You have LIMITED steps. Be efficient:\n\n"
        "1. UNDERSTAND BEFORE ACTING: Read ALL relevant files before making changes. "
        "Understand requirements, interfaces, and existing code patterns first.\n\n"
        "2. PARALLEL EXECUTION: When multiple operations don't depend on each other, "
        "execute them simultaneously (e.g., read multiple files at once).\n\n"
        "3. WRITE COMPLETE CODE: Write complete, working implementations. "
        "No stubs, TODOs, or placeholders.\n\n"
        "4. VERIFY AFTER CHANGES: After modifying code, verify it works. "
        "Run available linters/formatters/tests if available.\n\n"
        "5. FIX ROOT CAUSE: When debugging, fix the underlying issue, not symptoms. "
        "If a test fails, the bug is in your code, NOT in the test.\n\n"
        "6. CODE STYLE: Mimic existing code conventions. "
        "Don't add comments unless the logic is genuinely complex.\n\n"
        "7. SECURITY: Never expose, log, or commit secrets, API keys, or credentials."
    )

    DEFAULT_CHOOSE_ACTION_INSTRUCTION: str = (
        "Determine exactly one command to use next based on the given goals "
        "and the progress you have made so far, "
        "and respond using the JSON schema specified previously.\n\n"
        "PARALLEL EXECUTION: When multiple operations don't depend on each other, "
        "you may call multiple independent commands simultaneously. For example:\n"
        "- Read multiple files at once before making changes\n"
        "- Execute multiple independent writes\n"
        "- Run multiple search queries in parallel"
    )
```

### 2. Response Schema

```python
class AssistantThoughts(ModelWithSummary):
    observations: str = Field(
        description="Relevant observations from your last action (if any)"
    )
    reasoning: str = Field(description="Reasoning behind choosing this action")
    self_criticism: str = Field(description="Constructive self-criticism")
    plan: list[str] = Field(description="Short list that conveys the long-term plan")
```

---

## Tool Components (Forge Architecture)

### 1. File Manager Component

```python
class FileManagerComponent(
    DirectiveProvider, CommandProvider, ConfigurableComponent[FileManagerConfiguration]
):
    """
    Adds general file manager (e.g. Agent state),
    workspace manager (e.g. Agent output files) support and
    commands to perform operations on files and folders.
    """

    STATE_FILE = "state.json"
    """The name of the file where the agent's state is stored."""

    def __init__(
        self,
        file_storage: FileStorage,
        agent_state: BaseAgentSettings,
        config: Optional[FileManagerConfiguration] = None,
        workspace_root: Optional[Path] = None,
    ):
        """Initialise the FileManagerComponent.
        Either `agent_id` or `config` must be provided."""
```

### Available Tool Components (18 total)

| Component | Description |
|-----------|-------------|
| archive_handler | Archive and compress files |
| clipboard | Clipboard operations |
| code_executor | Execute code snippets |
| context | Context management |
| data_processor | Data processing utilities |
| file_manager | File and workspace management |
| git_operations | Git commands |
| http_client | HTTP requests |
| image_gen | Image generation |
| math_utils | Mathematical operations |
| platform_blocks | Platform-specific operations |
| skills | Dynamic skill loading |
| system | System operations |
| text_utils | Text processing |
| todo | Task management |
| user_interaction | User prompts |
| playwright_browser | Web browser automation |
| search | Web search |

---

## Evaluation Dimensions

### 1. Prompt Strategy Completeness
- [ ] Each strategy has clear action determination logic
- [ ] Response schema is well-defined
- [ ] System prompt template includes constraints, resources, commands
- [ ] Efficiency guidelines are actionable

### 2. Tool Component Architecture
- [ ] Each tool has clear CommandProvider interface
- [ ] Configuration is properly typed with Pydantic
- [ ] Error handling is comprehensive
- [ ] Tools can be dynamically loaded/unloaded

### 3. Multi-Strategy Support
- [ ] Strategies share common interface (PromptStrategy)
- [ ] Strategy selection is configurable
- [ ] Each strategy provides distinct reasoning patterns
- [ ] LLM classification is supported

### 4. Autonomous Execution Capability
- [ ] Agent can operate without continuous user input
- [ ] Has self-criticism and reflection mechanisms
- [ ] Plans are generated and tracked
- [ ] Progress can be measured

### 5. Forge Component Modularity
- [ ] Components are independently usable
- [ ] Clear separation of concerns (file, web, code, etc.)
- [ ] Configuration-driven behavior
- [ ] Sandbox isolation for file operations

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Prompt Strategy Completeness | 25% | | |
| Tool Component Architecture | 25% | | |
| Multi-Strategy Support | 15% | | |
| Autonomous Execution Capability | 20% | | |
| Forge Component Modularity | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Strategy Selection Tests
1. Verify one_shot strategy is used by default
2. Test tree_of_thoughts strategy activation
3. Validate reflexion strategy self-criticism loop

### Tool Execution Tests
1. Test file_manager read/write operations
2. Verify git_operations clone/commit/push
3. Test playwright_browser navigation and screenshot

### Autonomous Behavior Tests
1. Provide a multi-step task without intermediate guidance
2. Verify plan generation and execution tracking
3. Test self-correction on error conditions

---

## Notes

- AutoGPT Classic pioneered the autonomous agent pattern with configurable strategies
- The Forge architecture enables pluggable tool components
- Response schema enforces structured output with reasoning trace
- Parallel execution support for efficiency
- MIT license allows full examination and modification
- Suitable for studying autonomous agent prompt engineering patterns