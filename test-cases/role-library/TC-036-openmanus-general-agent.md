# TC-036: OpenManus - General Purpose Agent Suite

## Metadata
- **Source Project**: OpenManus (FoundationAgents/OpenManus)
- **GitHub**: github.com/FoundationAgents/OpenManus
- **License**: MIT
- **Artifact Type**: General-purpose autonomous agent prompts and tools
- **Collection Date**: 2025-10-12
- **Collection Method**: GitHub API content extraction at commit 3309bf4e416fb1c74b008f3e86494439a31bad53
- **Scope**: Main.py -> Manus; repository-owned prompt texts and registered local tools

---

## Project Overview

OpenManus is a versatile general-purpose AI agent framework that supports both **local and MCP (Model Context Protocol) tools**. It features a clean agent architecture with a focused set of core tools plus extensible MCP server integration.

### Key Characteristics
- **Single agent design**: Manus agent handles all tasks
- **4 core local tools**: Python execution, file editing, human interaction, termination
- **MCP tool support**: External tools via Model Context Protocol
- **Browser Use integration**: Web browsing via MCP CLI

---

## Agent Prompts

### 1. System Prompt

```python
SYSTEM_PROMPT = (
    "You are OpenManus, an all-capable AI assistant, aimed at solving any task presented by the user. You have various tools at your disposal that you can call upon to efficiently complete complex requests. Whether it's programming, information retrieval, file processing, web browsing, or human interaction (only for extreme cases), you can handle it all."
    "The initial directory is: {directory}"
)
```

### 2. Next Step Prompt

```python
NEXT_STEP_PROMPT = """
Based on user needs, proactively select the most appropriate tool or combination of tools. For complex tasks, you can break down the problem and use different tools step by step to solve it. After using each tool, clearly explain the execution results and suggest the next steps.

If you want to stop the interaction at any point, use the `terminate` tool/function call.
"""
```

---

## Agent Definition

### Manus Agent Class

```python
class Manus(ToolCallAgent):
    """A versatile general-purpose agent with support for both local and MCP tools."""

    name: str = "Manus"
    description: str = "A versatile agent that can solve various tasks using multiple tools including MCP-based tools"

    system_prompt: str = SYSTEM_PROMPT.format(directory=config.workspace_root)
    next_step_prompt: str = NEXT_STEP_PROMPT

    max_observe: int = 10000
    max_steps: int = 20

    # MCP clients for remote tool access
    mcp_clients: MCPClients = Field(default_factory=MCPClients)

    # Add general-purpose tools to the tool collection
    available_tools: ToolCollection = Field(
        default_factory=lambda: ToolCollection(
            PythonExecute(),
            StrReplaceEditor(),
            AskHuman(),
            Terminate(),
        )
    )

    special_tool_names: list[str] = Field(default_factory=lambda: [Terminate().name])

    # Track connected MCP servers
    connected_servers: Dict[str, str] = Field(
        default_factory=dict
    )  # server_id -> url/command
    mcp_instruction_servers: set[str] = Field(default_factory=set, exclude=True)
    _initialized: bool = False

    @classmethod
    async def create(cls, **kwargs) -> "Manus":
        """Factory method to create and properly initialize a Manus instance."""
        instance = cls(**kwargs)
        await instance.initialize_mcp_servers()
        instance._initialized = True
        return instance

    async def initialize_mcp_servers(self) -> None:
        """Initialize connections to configured MCP servers."""
        if _BROWSER_USE_SERVER_ID not in config.mcp_config.servers and os.getenv(
            "OPENMANUS_DISABLE_BROWSER_USE", ""
        ).lower() not in {"1", "true", "yes"}:
            try:
                await self.connect_mcp_server(
                    _BROWSER_USE_COMMAND,
                    _BROWSER_USE_SERVER_ID,
                    use_stdio=True,
                    stdio_args=_BROWSER_USE_ARGS,
                    tool_name_prefix=False,
                    stdio_env=_browser_use_env(),
                )
                logger.info("Connected to Browser Use CLI 3.0 through MCP")
            except Exception as e:
                logger.error(f"Failed to connect to Browser Use CLI 3.0: {e}")
```

---

## Tool Definitions

### 1. Python Execute Tool
Executes Python code for computation and scripting tasks.

### 2. StrReplace Editor Tool
File editing with string replacement operations.

### 3. Ask Human Tool
Request user input when autonomous operation cannot proceed.

### 4. Terminate Tool
End the agent session cleanly.

### MCP Integration
```python
_BROWSER_USE_SERVER_ID = "browser_use"
_BROWSER_USE_COMMAND = "uvx"
_BROWSER_USE_ARGS = ["browser-use", "--cli-mcp"]
_BROWSER_USE_ENV_VARS = (
    "BROWSER_USE_API_KEY",
    "BROWSER_USE_CLOUD_API_URL",
    "BU_BROWSER_ID",
    "BU_CDP_URL",
    "BU_CDP_WS",
    "BU_NAME",
)
_BROWSER_USE_TRANSPORT_INSTRUCTIONS = """\
Browser Use CLI 3.0 is exposed here as MCP tools. When the Browser Use skill
shows `browser-use <<'PY'`, pass the Python body to `browser_exec` instead.
Use `browser_screenshot` when visual inspection is needed. Both tools use the
same persistent browser-harness session as CLI 3.0.
"""
```

---

## Evaluation Dimensions

### 1. System Prompt Clarity
- [ ] Agent identity is clearly defined
- [ ] Capabilities are enumerated
- [ ] Initial context (directory) is provided
- [ ] Scope of operations is clear

### 2. Tool Selection Logic
- [ ] Proactive tool selection guidance
- [ ] Tool combination support
- [ ] Clear termination mechanism
- [ ] Execution result explanation required

### 3. MCP Integration Quality
- [ ] Dynamic MCP server connection
- [ ] Environment variable handling
- [ ] Error handling for connection failures
- [ ] Tool prefix configuration

### 4. Agent Architecture
- [ ] Clean inheritance from ToolCallAgent
- [ ] Async initialization pattern
- [ ] Configuration via Pydantic fields
- [ ] Step limiting for safety

### 5. Extensibility
- [ ] Additional tools can be added
- [ ] MCP servers can be configured
- [ ] Environment-based configuration
- [ ] Factory method for initialization

---

## Scoring Criteria

| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| System Prompt Clarity | 20% | | |
| Tool Selection Logic | 25% | | |
| MCP Integration Quality | 25% | | |
| Agent Architecture | 15% | | |
| Extensibility | 15% | | |
| **Total** | 100% | | |

---

## Test Suggestions

### Basic Functionality Tests
1. Verify Python code execution with various inputs
2. Test file editing operations
3. Validate termination behavior

### MCP Integration Tests
1. Test Browser Use CLI connection
2. Verify MCP tool invocation
3. Test error handling when MCP unavailable

### Autonomous Behavior Tests
1. Provide complex multi-step task
2. Verify tool selection appropriateness
3. Test step limit enforcement

### Edge Cases
1. Test with disabled Browser Use
2. Verify behavior when no tools match task
3. Test re-initialization scenarios

---

## Notes

- OpenManus represents a modern, lightweight autonomous agent design
- MCP protocol integration enables extensible tool ecosystem
- Clean separation of local tools vs MCP tools
- Max steps limit prevents runaway execution
- MIT license allows full examination and modification
- Demonstrates best practices for async agent initialization
- Good reference for building general-purpose agents with tool calling