# TC-021: Microsoft AutoGen - Multi-Agent Suite

## Metadata
- **Source Project**: Microsoft AutoGen (microsoft/autogen)
- **Commit SHA**: 027ecf0a379bcc1d09956d46d12d44a3ad9cee14
- **License**: CC-BY-4.0
- **Artifact Type**: Multi-Agent Framework
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

Microsoft AutoGen is a **multi-agent conversation framework** that enables the development of LLM applications using multiple conversational agents. The framework provides core agent types, team orchestration, and tool integration capabilities.

### Core Agent Types

| Agent Type | Responsibility | Primary Artifact Type |
|------------|----------------|----------------------|
| **AssistantAgent** | LLM-powered assistant with tool use capabilities | System Prompt + Tool Schema |
| **CodeExecutorAgent** | Generates and executes code snippets | System Prompt + Tool Schema |
| **SocietyOfMindAgent** | Inner team orchestration wrapper | System Prompt + Tool Schema |
| **UserProxyAgent** | Human-in-the-loop interface | Tool Schema |

---

## Logical Artifact Inventory

### 1. System Prompts (2)

#### 1.1 SocietyOfMindAgent (Team Orchestrator)
```python
# python/packages/autogen-agentchat/src/autogen_agentchat/agents/_society_of_mind_agent.py

class SocietyOfMindAgent(BaseChatAgent, Component[SocietyOfMindAgentConfig]):
    """An agent that uses an inner team of agents to generate responses.

    Each time the agent's :meth:`on_messages` or :meth:`on_messages_stream`
    method is called, it runs the inner team of agents and then uses the
    model client to generate a response based on the inner team's messages.
    Once the response is generated, the agent resets the inner team by
    calling :meth:`Team.reset`.

    Limit context size sent to the model:

    You can limit the number of messages sent to the model by setting
    the `model_context` parameter to a :class:`~autogen_core.model_context.BufferedChatCompletionContext`.
    This will limit the number of recent messages sent to the model and can be useful
    when the model has a limit on the number of tokens it can process.
    You can also create your own model context by subclassing
    :class:`~autogen_core.model_context.ChatCompletionContext`.

    Args:
        name (str): The name of the agent.
        team (Team): The team of agents to use.
        model_client (ChatCompletionClient): The model client to use for preparing responses.
        description (str, optional): The description of the agent.
        instruction (str, optional): The instruction to use when generating a response using the inner team's messages.
            Defaults to :attr:`DEFAULT_INSTRUCTION`. It assumes the role of 'system'.
        response_prompt (str, optional): The response prompt to use when generating a response using the inner team's messages.
            Defaults to :attr:`DEFAULT_RESPONSE_PROMPT`. It assumes the role of 'system'.
        model_context (ChatCompletionContext | None, optional): The model context for storing and retrieving :class:`~autogen_core.models.LLMMessage`. It can be preloaded with initial messages. The initial messages will be cleared when the agent is reset.
    """

    DEFAULT_INSTRUCTION = "Earlier you were asked to fulfill a request. You and your team worked diligently to address that request. Here is a transcript of that conversation:"
    """str: The default instruction to use when generating a response using the
    inner team's messages. The instruction will be prepended to the inner team's
    messages when generating a response using the model. It assumes the role of
    'system'."""

    DEFAULT_RESPONSE_PROMPT = (
        "Output a standalone response to the original request, without mentioning any of the intermediate discussion."
    )
    """str: The default response prompt to use when generating a response using
    the inner team's messages. It assumes the role of 'system'."""

    DEFAULT_DESCRIPTION = "An agent that uses an inner team of agents to generate responses."
    """str: The default description for a SocietyOfMindAgent."""
```

#### 1.2 AssistantAgent (Tool-Using Agent)
```python
# python/packages/autogen-agentchat/src/autogen_agentchat/agents/_assistant_agent.py

class AssistantAgent(BaseChatAgent, Component[AssistantAgentConfig]):
    """An agent that provides assistance with tool use.
    The :meth:`on_messages` returns a :class:`~autogen_agentchat.base.Response`
    in which :attr:`~autogen_agentchat.base.Response.chat_message` is the final
    response message.

    The :meth:`on_messages_stream` creates an async generator that produces
    the inner messages as they are created, and the :class:`~autogen_agentchat.base.Response`
    object as the last item before closing the generator.

    The :meth:`BaseChatAgent.run` method returns a :class:`~autogen_agentchat.base.TaskResult`
    containing the messages produced by the agent. In the list of messages,
    :attr:`~autogen_agentchat.base.TaskResult.messages`,
    the last message is the final response message.

    .. attention::

        The caller must only pass the new messages to the agent on each call
        to the :meth:`on_messages`, :meth:`on_messages_stream`, :meth:`BaseChatAgent.run`,
        or :meth:`BaseChatAgent.run_stream` methods.
        The agent maintains its state between calls to these methods.
        Do not pass the entire conversation history to the agent on each call.

    .. warning::
        The assistant agent is not thread-safe or coroutine-safe.
        It should not be shared between multiple tasks or coroutines, and it should
        not call its methods concurrently.

    **Tool call behavior:**

    * If the model returns no tool call, then the response is immediately returned as a :class:`~autogen_agentchat.messages.TextMessage` or a :class:`~autogen_agentchat.messages.StructuredMessage` (when using structured output) in :attr:`~autogen_agentchat.base.Response.chat_message`. This ends the tool call iteration loop regardless of the `max_tool_iterations` setting.
    * When the model returns tool calls, they will be executed right away:
        - When `reflect_on_tool_use` is False, the tool call results are returned as a :class:`~autogen_agentchat.messages.ToolCallSummaryMessage` in :attr:`~autogen_agentchat.base.Response.chat_message`. You can customise the summary with either a static format string (`tool_call_summary_format`) **or** a callable (`tool_call_summary_formatter`); the callable is evaluated once per tool call.
        - When `reflect_on_tool_use` is True, the another model inference is made using the tool calls and results, and final response is returned as a :class:`~autogen_agentchat.messages.TextMessage` or a :class:`~autogen_agentchat.messages.StructuredMessage` (when using structured output) in :attr:`~autogen_agentchat.base.Response.chat_message`.
        - `reflect_on_tool_use` is set to `True` by default when `output_content_type` is set.
        - `reflect_on_tool_use` is set to `False` by default when `output_content_type` is not set.
    * If the model returns multiple tool calls, they will be executed concurrently. To disable parallel tool calls you need to configure the model client. For example, set `parallel_tool_calls=False` for :class:`~autogen_ext.models.openai.OpenAIChatCompletionClient` and :class:`~autogen_ext.models.openai.AzureOpenAIChatCompletionClient`.
    * The `max_tool_iterations` parameter controls how many sequential tool call iterations the agent can perform in a single run. When set to 1 (default), the agent executes tool calls once and returns the result. When set higher, the agent can make additional model calls to execute more tool calls if the model continues to request them, enabling multi-step tool-based workflows.

    **Hand off behavior:**

    * If a handoff is triggered, a :class:`~autogen_agentchat.messages.HandoffMessage` will be returned in :attr:`~autogen_agentchat.base.Response.chat_message`.
    * If there are tool calls, they will also be executed right away before returning the handoff.
    * The tool calls and results are passed to the target agent through :attr:`~autogen_agentchat.messages.HandoffMessage.context`.
    """
```

---

### 2. Tool Schemas (2)

#### 2.1 TeamTool (Multi-Agent Delegation)
```python
# python/packages/autogen-agentchat/src/autogen_agentchat/tools/_team.py

class TeamToolConfig(BaseModel):
    """Configuration for the TeamTool."""

    name: str
    """The name of the tool."""
    description: str
    """The name and description of the tool."""
    team: ComponentModel
    """The team to be used for running the task."""
    return_value_as_last_message: bool = False
    """Whether to return the value as the last message of the task result."""


class TeamTool(TaskRunnerTool, Component[TeamToolConfig]):
    """Tool that can be used to run a task.

    The tool returns the result of the task execution as a :class:`~autogen_agentchat.base.TaskResult` object.

    .. important::
        When using TeamTool, you **must** disable parallel tool calls in the model client configuration
        to avoid concurrency issues. Teams cannot run concurrently as they maintain internal state
        that would conflict with parallel execution. For example, set ``parallel_tool_calls=False``
        for :class:`~autogen_ext.models.openai.OpenAIChatCompletionClient` and
        :class:`~autogen_ext.models.openai.AzureOpenAIChatCompletionClient`.

    Args:
        team (BaseGroupChat): The team to be used for running the task.
        name (str): The name of the tool.
        description (str): The description of the tool.
        return_value_as_last_message (bool): Whether to use the last message content of the task result
            as the return value of the tool in :meth:`~autogen_agentchat.tools.TaskRunnerTool.return_value_as_string`.
            If set to True, the last message content will be returned as a string.
            If set to False, the tool will return all messages in the task result as a string concatenated together,
            with each message prefixed by its source (e.g., "writer: ...", "assistant: ...").
    """
```

#### 2.2 CodeExecutorAgent (Agent Config Schema)

*(Note — CodeExecutorAgent is a `BaseChatAgent` with a component config schema rather than a tool; it is kept under Tool Schemas here as a config-schema artifact. The agents/tools packages also contain `MessageFilterAgent` (agents/_message_filter_agent.py), `AgentTool` (tools/_agent.py), and its base `TaskRunnerTool` (tools/_task_runner_tool.py), which are not quoted.)*

```python
# python/packages/autogen-agentchat/src/autogen_agentchat/agents/_code_executor_agent.py

class CodeExecutorAgentConfig(BaseModel):
    """Configuration for CodeExecutorAgent"""

    name: str
    code_executor: ComponentModel
    model_client: ComponentModel | None = None
    description: str | None = None
    sources: List[str] | None = None
    system_message: str | None = None
    model_client_stream: bool = False
    model_context: ComponentModel | None = None
    supported_languages: List[str] | None = None


class RetryDecision(BaseModel):
    reason: str
    retry: bool


class ApprovalRequest(BaseModel):
    """Request for approval of code execution."""

    code: str
    context: List[LLMMessage]


class ApprovalResponse(BaseModel):
    """Response to approval request."""

    approved: bool
    reason: str


class CodeExecutorAgent(BaseChatAgent, Component[CodeExecutorAgentConfig]):
    """(Experimental) An agent that generates and executes code snippets based on user instructions.

    .. note::

        This agent is experimental and may change in future releases.

    It is typically used within a team with another agent that generates code snippets
    to be executed or alone with `model_client` provided so that it can generate code
    based on user query, execute it and reflect on the code result.

    When used with `model_client`, it will generate code snippets using the model
    and execute them using the provided `code_executor`. The model will also reflect on the
    code execution results. The agent will yield the final reflection result from the model
    as the final response.

    When used without `model_client`, it will only execute code blocks found in
    :class:`~autogen_agentchat.messages.TextMessage` messages and returns the output
    of the code execution.

    Args:
        name (str): The name of the agent.
        code_executor (CodeExecutor): The code executor responsible for executing code received in messages
            (:py:class:`~autogen_ext.code_executors.docker.DockerCommandLineCodeExecutor` recommended. See example below)
        model_client (ChatCompletionClient, optional): The model client to use for inference and generating code.
            If not provided, the agent will only execute code blocks found in input messages.
        model_client_stream (bool, optional): If `True`, the model client will be used in streaming mode.
        description (str, optional): The description of the agent. If not provided,
            :class:`~autogen_agentchat.agents.CodeExecutorAgent.DEFAULT_AGENT_DESCRIPTION` will be used.
        system_message (str, optional): The system message for the model. If provided, it will be prepended to the messages in the model context when making an inference. Set to `None` to disable.
            Defaults to :class:`~autogen_agentchat.agents.CodeExecutorAgent.DEFAULT_SYSTEM_MESSAGE`. This is only used if `model_client` is provided.
        sources (Sequence[str], optional): Check only messages from the specified agents for the code to execute.
            This is useful when the agent is part of a group chat and you want to limit the code execution to messages from specific agents.
            If not provided, all messages will be checked for code blocks.
        supported_languages (List[str], optional): List of programming languages that will be parsed and executed from agent response;
            others will be ignored. Defaults to DEFAULT_SUPPORTED_LANGUAGES.
        approval_func (Optional[Union[Callable[[ApprovalRequest], ApprovalResponse], Callable[[ApprovalRequest], Awaitable[ApprovalResponse]]]], optional): A function that is called before each code execution to get approval.
            The function takes an ApprovalRequest containing the code to be executed and the current context, and returns an ApprovalResponse.
            The function can be either synchronous or asynchronous. If None (default), all code executions are automatically approved.
    """
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] 4 Agent types with clear responsibility boundaries
- [ ] Each agent's role clearly defines its positioning (assistant, code executor, orchestrator, human proxy)
- [ ] Inter-agent dependencies (input/output) are clearly defined through Team abstraction

### 2. Workflow Completeness
- [ ] Multi-agent orchestration via Team abstraction
- [ ] Support for both sequential and parallel agent execution
- [ ] Code execution with approval mechanism

### 3. Prompt Consistency
- [ ] Standardized instruction/response prompt patterns
- [ ] Model context management across agents
- [ ] Configurable system messages

### 4. Tool Modularity
- [ ] Tools can be registered with agents
- [ ] TeamTool enables agent-to-agent delegation
- [ ] Code execution as both tool and agent capability

### 5. Observability
- [ ] Streaming message support
- [ ] Event-based message handling
- [ ] State management across conversations

### 6. Extensibility
- [ ] Component-based architecture with configuration schemas
- [ ] Custom agent creation through BaseChatAgent
- [ ] Tool registration mechanism

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
1. **Multi-agent conversation**: Create a team of AssistantAgents with different roles
2. **Code execution flow**: Test AssistantAgent generating code for CodeExecutorAgent
3. **SocietyOfMindAgent**: Test inner team orchestration and response generation

### Unit Tests
1. **Agent creation**: Verify agent configuration and component loading
2. **Tool registration**: Test tool schema generation and execution
3. **State management**: Verify message context handling between turns

### Integration Tests
1. **Team orchestration**: Test RoundRobinGroupChat and other group chat patterns
2. **Handoff mechanism**: Verify agent-to-agent handoff with context passing
3. **Streaming support**: Test streaming message handling

---

## Notes

- **CC-BY-4.0 license** allows full quotation with attribution
- The framework emphasizes **component-based configuration** for agent definitions
- SocietyOfMindAgent pattern enables **nested multi-agent architectures**
- TeamTool provides **tool-based multi-agent delegation** capability