# TC-024: CAMEL - Multi-Agent Suite

## Metadata
- **Source Project**: CAMEL-AI (camel-ai/camel)
- **Commit SHA**: 24fde60ad739b4be8f8f533fea9ba54256fbc4a2
- **License**: Apache-2.0
- **Artifact Type**: Multi-Agent Framework
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit

---

## Project Overview

CAMEL is a **communicative agent framework** that enables multi-agent collaboration through role-playing scenarios. It provides specialized agent types, comprehensive toolkits, and a skill system for building complex AI applications.

### Core Agent Types

| Agent Type | Responsibility | Primary Artifact Type |
|------------|----------------|----------------------|
| **ChatAgent** | General-purpose conversational agent | System Prompt + Tool Schema |
| **CriticAgent** | Evaluates and selects from multiple options | System Prompt |
| **KnowledgeGraphAgent** | Extracts nodes and relationships from content | System Prompt |

### Toolkits Available

| Toolkit | Domain | Primary Functions |
|---------|--------|------------------|
| **SearchToolkit** | Web search | Google, DuckDuckGo, Wikipedia, Wolfram Alpha |
| **BrowserToolkit** | Web automation | Navigation, interaction, screenshot |
| **ArxivToolkit** | Academic papers | Search, download, read |
| **ExcelToolkit** | Spreadsheet operations | Read, write, analyze |
| **DataCommonsToolkit** | Knowledge graph | Query public data |

---

## Logical Artifact Inventory

### 1. System Prompts (3)

*(Note — `camel/agents/` contains 11 agent modules; the three quoted below are a selection. Not covered: mcp_agent, repo_agent, role_assignment_agent, search_agent, task_agent, multi_hop_generator_agent, programmed_agent_instruction, base.)*

#### 1.1 ChatAgent (General-Purpose Agent)

*(Excerpt — the upstream `__init__` accepts ~29 parameters, including summarize_threshold, scheduling_strategy, agent_id, retry_attempts, retry_delay, mask_tool_output, prune_tool_calls_from_memory, and more; only the leading docstring Args and the full signature are shown.)*

```python
# camel/agents/chat_agent.py

@track_agent(name="ChatAgent")
class ChatAgent(BaseAgent):
    r"""Class for managing conversations of CAMEL Chat Agents.

    Args:
        system_message (Union[BaseMessage, str], optional): The system message
            for the chat agent. (default: :obj:`None`)
        model (Union[BaseModelBackend, Tuple[str, str], str, ModelType,
            Tuple[ModelPlatformType, ModelType], List[BaseModelBackend],
            List[str], List[ModelType], List[Tuple[str, str]],
            List[Tuple[ModelPlatformType, ModelType]]], optional):
            The model backend(s) to use. Can be a single instance,
            a specification (string, enum, tuple), or a list of instances
            or specifications to be managed by `ModelManager`. If a list of
            specifications (not `BaseModelBackend` instances) is provided,
            they will be instantiated using `ModelFactory`. (default:
            :obj:`ModelPlatformType.DEFAULT` with `ModelType.DEFAULT`)
        memory (AgentMemory, optional): The agent memory for managing chat
            messages. If `None`, a :obj:`ChatHistoryMemory` will be used.
            (default: :obj:`None`)
        message_window_size (int, optional): The maximum number of previous
            messages to include in the context window. If `None`, no windowing
            is performed. (default: :obj:`None`)

    (…further Args: summarize_threshold, token_limit, output_language, tools,
    toolkits_to_register_agent, external_tools, response_terminators, …)
    """

    def __init__(
        self,
        system_message: Optional[Union[BaseMessage, str]] = None,
        model: Optional[
            Union[
                BaseModelBackend,
                Tuple[str, str],
                str,
                ModelType,
                Tuple[ModelPlatformType, ModelType],
                List[BaseModelBackend],
                List[str],
                List[ModelType],
                List[Tuple[str, str]],
                List[Tuple[ModelPlatformType, ModelType]],
            ]
        ] = None,
        memory: Optional[AgentMemory] = None,
        message_window_size: Optional[int] = None,
        summarize_threshold: Optional[int] = 50,
        token_limit: Optional[int] = None,
        output_language: Optional[str] = None,
        tools: Optional[List[Union[FunctionTool, Callable]]] = None,
        toolkits_to_register_agent: Optional[
            List[RegisteredAgentToolkit]
        ] = None,
        external_tools: Optional[
            List[Union[FunctionTool, Callable, Dict[str, Any]]]
        ] = None,
        response_terminators: Optional[List[ResponseTerminator]] = None,
        scheduling_strategy: str = "round_robin",
        max_iteration: Optional[int] = None,
        agent_id: Optional[str] = None,
        stop_event: Optional[threading.Event] = None,
        tool_execution_timeout: Optional[float] = Constants.TIMEOUT_THRESHOLD,
        mask_tool_output: bool = False,
        pause_event: Optional[Union[threading.Event, asyncio.Event]] = None,
        prune_tool_calls_from_memory: bool = False,
        enable_snapshot_clean: bool = False,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
        step_timeout: Optional[float] = Constants.TIMEOUT_THRESHOLD,
        on_request_usage: Optional[Callable[[Dict[str, Any]], Any]] = None,
        stream_accumulate: Optional[bool] = None,
        summary_window_ratio: float = 0.6,
        tool_log_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        # Resolve model backends into a ModelManager, assign agent_id,
        # set up memory/context creator, and register tools.
        ...
```

#### 1.2 CriticAgent (Evaluation Agent)
```python
# camel/agents/critic_agent.py

class CriticAgent(ChatAgent):
    """A class for the critic agent that assists in selecting an option.

    Args:
        system_message (Union[BaseMessage, str], optional): The system message
            for the chat agent. (default: :obj:`None`)
        model (Union[BaseModelBackend, Tuple[str, str], str, ModelType,
            Tuple[ModelPlatformType, ModelType], List[BaseModelBackend],
            List[str], List[ModelType], List[Tuple[str, str]],
            List[Tuple[ModelPlatformType, ModelType]]], optional):
            The model backend(s) to use. (default: :obj:`None`)
        message_window_size (int, optional): The maximum number of previous
            messages to include in the context window. (default: :obj:`6`)
        retry_attempts (int, optional): The number of retry attempts if the
            critic fails to return a valid option. (default: :obj:`2`)
        verbose (bool, optional): Whether to print the critic's messages.
        logger_color (Any): The color of the menu options displayed to the
            user. (default: :obj:`Fore.MAGENTA`)
    """

    def __init__(
        self,
        system_message: Optional[Union[BaseMessage, str]] = None,
        model: Optional[
            Union[
                BaseModelBackend,
                Tuple[str, str],
                str,
                ModelType,
                Tuple[ModelPlatformType, ModelType],
                List[BaseModelBackend],
                List[str],
                List[ModelType],
                List[Tuple[str, str]],
                List[Tuple[ModelPlatformType, ModelType]],
            ]
        ] = None,
        memory: Optional[AgentMemory] = None,
        message_window_size: int = 6,
        retry_attempts: int = 2,
        verbose: bool = False,
        logger_color: Any = Fore.MAGENTA,
    ) -> None:
        super().__init__(
            system_message,
            model=model,
            memory=memory,
            message_window_size=message_window_size,
        )
        self.options_dict: Dict[str, str] = dict()
        self.retry_attempts = retry_attempts
        self.verbose = verbose
        self.logger_color = logger_color

    def flatten_options(self, messages: Sequence[BaseMessage]) -> str:
        """Flattens the options to the critic.

        Args:
            messages (Sequence[BaseMessage]): A list of `BaseMessage` objects.

        Returns:
            str: A string containing the flattened options to the critic.
        """
        options = [message.content for message in messages]
        flatten_options = (
            f"> Proposals from "
            f"{messages[0].role_name} ({messages[0].role_type}). "
            "Please choose an option:\n"
        )
        for index, option in enumerate(options):
            flatten_options += f"Option {index + 1}:\n{option}\n\n"
            self.options_dict[str(index + 1)] = option
        format = (
            f"Please first enter your choice ([1-{len(self.options_dict)}]) "
            "and then your explanation and comparison: "
        )
        return flatten_options + format

    def get_option(self, input_message: BaseMessage) -> str:
        """Gets the option selected by the critic.

        Returns:
            str: The option selected by the critic.
        """
        # ... retry logic and parsing
```

#### 1.3 KnowledgeGraphAgent (Graph Extraction)
```python
# camel/agents/knowledge_graph_agent.py

text_prompt = """
You are tasked with extracting nodes and relationships from given content and
structures them into Node and Relationship objects. Here's the outline of what
you needs to do:

Content Extraction:
You should be able to process input content and identify entities mentioned
within it.
Entities can be any noun phrases or concepts that represent distinct entities
in the context of the given content.

Node Extraction:
For each identified entity, you should create a Node object.
Each Node object should have a unique identifier (id) and a type (type).
Additional properties associated with the node can also be extracted and
stored.

Relationship Extraction:
You should identify relationships between entities mentioned in the content.
For each relationship, create a Relationship object.
A Relationship object should have a subject (subj) and an object (obj) which
are Node objects representing the entities involved in the relationship.
Each relationship should also have a type (type), and additional properties if
applicable.

Output Formatting:
The extracted nodes and relationships should be formatted as instances of the
provided Node and Relationship classes.
Ensure that the extracted data adheres to the structure defined by the classes.
Output the structured data in a format that can be easily validated against
the provided code.
Do not wrap the output in lists or dictionaries, provide the Node and
Relationship with unique identifiers.
Strictly follow the format provided in the example output, do not add any
additional information.


Instructions for you:
Read the provided content thoroughly.
Identify distinct entities mentioned in the content and categorize them as
nodes.
Determine relationships between these entities and represent them as directed
relationships.
Provide the extracted nodes and relationships in the specified format below.
Example for you:

Example Content:
"John works at XYZ Corporation. He is a software engineer. The company is
located in New York City."

Expected Output:

Nodes:

Node(id='John', type='Person')
Node(id='XYZ Corporation', type='Organization')
Node(id='New York City', type='Location')

Relationships:

Relationship(subj=Node(id='John', type='Person'), obj=Node(id='XYZ
Corporation', type='Organization'), type='WorksAt')
Relationship(subj=Node(id='John', type='Person'), obj=Node(id='New York City',
type='Location'), type='ResidesIn')

===== TASK =====
Please extracts nodes and relationships from given content and structures them
into Node and Relationship objects.

{task}
"""


class KnowledgeGraphAgent(ChatAgent):
    """An agent that can extract node and relationship information for
    different entities from given `Element` content.

    Attributes:
        task_prompt (TextPrompt): A prompt for the agent to extract node and
            relationship information for different entities.
    """

    def __init__(
        self,
        model: Optional[BaseModelBackend] = None,
    ) -> None:
        system_message = BaseMessage(
            role_name="Graphify",
            role_type=RoleType.ASSISTANT,
            meta_dict=None,
            content="Your mission is to transform unstructured content "
            "into structured graph data. Extract nodes and relationships with "
            "precision, and let the connections unfold. Your graphs will "
            "illuminate the hidden connections within the chaos of "
            "information.",
        )
        super().__init__(system_message, model=model)
```

---

### 2. Tool Schemas (2)

*(Note — `camel/toolkits/` contains 88 toolkit modules; the two quoted below are a selection. Three toolkits referenced in the overview — ArxivToolkit (camel/toolkits/arxiv_toolkit.py), ExcelToolkit (camel/toolkits/excel_toolkit.py), and DataCommonsToolkit (camel/toolkits/data_commons_toolkit.py) — exist upstream but are not quoted here.)*

#### 2.1 SearchToolkit (Web Search)
```python
# camel/toolkits/search_toolkit.py

@MCPServer()
class SearchToolkit(BaseToolkit):
    """A class representing a toolkit for web search.

    This class provides methods for searching information on the web using
    search engines like Google, DuckDuckGo, Wikipedia and Wolfram Alpha, Brave,
    Perplexity.
    """

    def __init__(
        self,
        timeout: Optional[float] = None,
        exclude_domains: Optional[List[str]] = None,
    ):
        """Initializes the SearchToolkit.

        Args:
            timeout (float): Timeout for API requests in seconds.
            exclude_domains (Optional[List[str]]): List of domains to
                exclude from search results.
        """
        super().__init__(timeout=timeout)
        self.exclude_domains = exclude_domains

    @api_keys_required([(None, "SERPER_API_KEY")])
    def search_serper(
        self,
        query: str,
        page: int = 10,
        location: str = "United States",
    ) -> Dict[str, Any]:
        """Use Serper.dev API to perform Google search.

        Args:
            query (str): The search query.
            page (int): The page number of results to retrieve.
            location (str): The location for the search results.

        Returns:
            Dict[str, Any]: The search result dictionary.
        """

    @dependencies_required("wikipedia")
    def search_wiki(self, entity: str) -> str:
        """Search the entity in WikiPedia and return the summary of the
        required page, containing factual information about
        the given entity.

        Args:
            entity (str): The entity to be searched.

        Returns:
            str: The summary of this entity in a string.
        """
```

#### 2.2 BrowserToolkit (Web Automation)
```python
# camel/toolkits/browser_toolkit.py

class BaseBrowser:
    def __init__(
        self,
        headless=True,
        cache_dir: Optional[str] = None,
        channel: Literal["chrome", "msedge", "chromium"] = "chromium",
        cookie_json_path: Optional[str] = None,
        user_data_dir: Optional[str] = None,
    ):
        """Initialize the WebBrowser instance.

        Args:
            headless (bool): Whether to run the browser in headless mode.
            cache_dir (Union[str, None]): The directory to store cache files.
            channel (Literal["chrome", "msedge", "chromium"]): The browser
                channel to use.
            cookie_json_path (Optional[str]): Path to a JSON file containing
                authentication cookies and browser storage state.
            user_data_dir (Optional[str]): The directory to store user data
                for persistent context.
        """
```

---

### 3. Skills (2)

*(Note — the repo-root `.camel/skills/` directory contains 2 skills: `docs-incremental-update` (quoted below) and `skill-creator` (not quoted). Three additional example skills live under `examples/toolkits/skill_toolkit_example/.camel/skills/` (code-reviewer, data-analyzer, report-writer) and are not quoted here.)*

#### 3.1 Docs Incremental Update Skill (excerpt)
```markdown
# .camel/skills/docs-incremental-update/SKILL.md

---
name: docs-incremental-update
description: >
  Incrementally update Mintlify documentation (.mdx) from Python source
  changes only. Use when: (1) Python files referenced in doc_code_map
  frontmatter have changed, (2) a PR touches Python modules documented in
  docs/mintlify/key_modules/ or docs/mintlify/mcp/, (3) the user asks to
  sync docs after Python code changes. Prefer minimal diffs and leave correct
  content untouched.
---

# Docs Incremental Update

Update Mintlify .mdx documentation so it stays in sync with CAMEL source code.

## Scope

- Only use this skill when the driver is **Python source changes** referenced
  by a target document's `doc_code_map`.
- Do **not** use it for docs-only edits, workflow/YAML changes, or broad
  wording cleanups without Python changes.
- Prefer **no document change** when Python edits are internal and do not
  affect public API, behavior, configuration, examples, or reader understanding.

## Workflow

### Step 1 — Identify Impacted Docs

Determine which `.mdx` files are affected by the code change.

```bash
# From repo root, pass only changed Python files
python docs/mintlify/scripts/docs_sync/doc_code_map.py impacted \
  --changed-file <file1> --changed-file <file2>
```

### Step 2 — Read Current Doc and Relevant Code

For each impacted doc:
1. Open the target `.mdx` file and inspect its `doc_code_map` frontmatter.
2. Use the provided changed Python file list as initial context.
3. Read any source files needed to judge whether the doc is still accurate.

### Step 3 — Update the Document Body

Rewrite only the parts of the body that are outdated relative to the code.

Rules:
- **Edit the target doc directly through terminal tools** for this run.
- **Prefer the smallest possible diff** — keep all already-correct content.
- **Preserve frontmatter** — never modify the `---` block.
- **Update code snippets** — fix imports, class names, method signatures, parameters.
```

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] 3 Agent types with clear specialization (chat, critic, knowledge graph)
- [ ] Each agent has specific output format and behavior
- [ ] Role-based task assignment

### 2. Workflow Completeness
- [ ] Multi-toolkit integration for diverse tasks
- [ ] CriticAgent enables multi-choice decision making
- [ ] KnowledgeGraphAgent for structured extraction

### 3. Prompt Consistency
- [ ] Standardized prompt templates with variable substitution
- [ ] Clear output format specifications
- [ ] Example-driven prompt design

### 4. Tool Modularity
- [ ] BaseToolkit abstraction for tool creation
- [ ] MCP server integration
- [ ] Multiple domain-specific toolkits

### 5. Observability
- [ ] Verbose mode for debugging
- [ ] Token counting and management
- [ ] Response termination conditions

### 6. Extensibility
- [ ] Custom toolkit creation
- [ ] Agent subclassing
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
1. **Multi-agent collaboration**: ChatAgent with CriticAgent for option selection
2. **Knowledge extraction**: Test KnowledgeGraphAgent with various content types
3. **Web search flow**: Test SearchToolkit integration with ChatAgent

### Unit Tests
1. **Agent creation**: Verify agent configuration and memory setup
2. **Tool execution**: Test toolkit function calls
3. **Skill loading**: Verify skill disclosure and runtime loading

### Integration Tests
1. **Browser automation**: Test BrowserToolkit navigation and interaction
2. **Academic search**: Test ArxivToolkit paper retrieval
3. **Spreadsheet operations**: Test ExcelToolkit read/write

---

## Notes

- **Apache-2.0 license** allows full quotation and modification
- CAMEL emphasizes **role-playing scenarios** for multi-agent collaboration
- The toolkit system provides **domain-specific capabilities**
- Skills enable **project-specific workflows** with declarative configuration