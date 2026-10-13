# TC-028: SuperAGI - Multi-Agent Suite

## Metadata
- **Source Project**: SuperAGI (TransformerOptimus/SuperAGI)
- **Commit SHA**: c3c1982e7bd6a11cfed53c5a193ea502f924b1b6
- **License**: MIT
- **Artifact Type**: Multi-Agent Framework
- **Collection Date**: 2026-10-12
- **Collection Method**: GitHub API content extraction from verified commit. Tool coverage is a selection: `superagi/tools/` contains ~20 more tool packages (github, google_search, google_serp_search, google_calendar, slack, jira, twitter, instagram, image_generation, searx, apollo, knowledge_search, resource, thinking, webscaper, plus file-toolkit append/delete/list operations), and the task prompt texts live in `superagi/agent/prompts/` (superagi.txt, initialize_tasks.txt, analyse_task.txt, create_tasks.txt, prioritize_tasks.txt).

---

## Project Overview

SuperAGI is an **autonomous agent framework** that provides a comprehensive prompt template system and tool ecosystem for building autonomous AI agents. It includes task management, code generation, and various utility tools.

### Core Capabilities

| Capability | Description | Primary Artifact Type |
|------------|-------------|----------------------|
| **Prompt Builder** | Dynamic prompt construction with variable substitution | System Prompt |
| **Prompt Templates** | Task-based prompt templates for different phases | System Prompt |
| **File Operations** | Reading and writing files | Tool Schema |
| **Code Generation** | Autonomous code writing and execution | Tool Schema |
| **Search** | Web search capabilities | Tool Schema |
| **Email** | Email sending functionality | Tool Schema |

---

## Logical Artifact Inventory

### 1. System Prompts (2)

#### 1.1 Agent Prompt Builder
```python
# superagi/agent/agent_prompt_builder.py

FINISH_NAME = "finish"


class AgentPromptBuilder:
    """Agent prompt builder for LLM agent."""

    @staticmethod
    def add_list_items_to_string(items: List[str]) -> str:
        list_string = ""
        for i, item in enumerate(items):
            list_string += f"{i + 1}. {item}\n"
        return list_string

    @classmethod
    def add_tools_to_prompt(cls, tools: List[BaseTool], add_finish: bool = True) -> str:
        """Add tools to the prompt.

        Args:
            tools (List[BaseTool]): The list of tools.
            add_finish (bool): Whether to add finish tool or not.
        """
        final_string = ""
        for i, item in enumerate(tools):
            final_string += f"{i + 1}. {cls._generate_tool_string(item)}\n"
        finish_description = (
            "use this to signal that you have finished all your objectives"
        )
        finish_args = (
            '"response": "final response to let '
            'people know you have finished your objectives"'
        )
        finish_string = (
            f"{len(tools) + 1}. \"{FINISH_NAME}\": "
            f"{finish_description}, args: {finish_args}"
        )
        if add_finish:
            final_string = final_string + finish_string + "\n\n"
        else:
            final_string = final_string + "\n"

        return final_string

    @classmethod
    def _generate_tool_string(cls, tool: BaseTool) -> str:
        output = f"\"{tool.name}\": {tool.description}"
        output += f", args json schema: {json.dumps(tool.args)}"
        return output
    
    @classmethod
    def clean_prompt(cls, prompt):
        prompt = re.sub('[ \t]+', ' ', prompt)
        return prompt.strip()

    @classmethod
    def replace_main_variables(cls, super_agi_prompt: str, goals: List[str], instructions: List[str], constraints: List[str],
                               tools: List[BaseTool], add_finish_tool: bool = True):
        """Replace the main variables in the super agi prompt.

        Args:
            super_agi_prompt (str): The super agi prompt.
            goals (List[str]): The list of goals.
            instructions (List[str]): The list of instructions.
            constraints (List[str]): The list of constraints.
            tools (List[BaseTool]): The list of tools.
            add_finish_tool (bool): Whether to add finish tool or not.
        """
        super_agi_prompt = super_agi_prompt.replace("{goals}", AgentPromptBuilder.add_list_items_to_string(goals))
        if len(instructions) > 0 and len(instructions[0]) > 0:
            task_str = "INSTRUCTION(Follow these instruction to decide the flow of execution and decide the next steps for achieving the task):"
            super_agi_prompt = super_agi_prompt.replace("{instructions}", "INSTRUCTION: " + '\n' +  AgentPromptBuilder.add_list_items_to_string(instructions))
            super_agi_prompt = super_agi_prompt.replace("{task_instructions}", task_str + '\n' +  AgentPromptBuilder.add_list_items_to_string(instructions))
        else:
            super_agi_prompt = super_agi_prompt.replace("{instructions}", '')
        super_agi_prompt = super_agi_prompt.replace("{task_instructions}", "")
        super_agi_prompt = super_agi_prompt.replace("{constraints}",
                                                    AgentPromptBuilder.add_list_items_to_string(constraints))

        tools_string = AgentPromptBuilder.add_tools_to_prompt(tools, add_finish_tool)
        super_agi_prompt = super_agi_prompt.replace("{tools}", tools_string)
        return super_agi_prompt

    @classmethod
    def replace_task_based_variables(cls, super_agi_prompt: str, current_task: str, last_task: str,
                                     last_task_result: str, pending_tasks: List[str], completed_tasks: list, token_limit: int):
        """Replace the task based variables in the super agi prompt.

        Args:
            super_agi_prompt (str): The super agi prompt.
            current_task (str): The current task.
            last_task (str): The last task.
            last_task_result (str): The last task result.
            pending_tasks (List[str]): The list of pending tasks.
            completed_tasks (list): The list of completed tasks.
            token_limit (int): The token limit.
        """
        if "{current_task}" in super_agi_prompt:
            super_agi_prompt = super_agi_prompt.replace("{current_task}", current_task)
        if "{last_task}" in super_agi_prompt:
            super_agi_prompt = super_agi_prompt.replace("{last_task}", last_task)
        if "{last_task_result}" in super_agi_prompt:
            super_agi_prompt = super_agi_prompt.replace("{last_task_result}", last_task_result)
        if "{pending_tasks}" in super_agi_prompt:
            super_agi_prompt = super_agi_prompt.replace("{pending_tasks}", str(pending_tasks))

        completed_tasks.reverse()
        if "{completed_tasks}" in super_agi_prompt:
            completed_tasks_arr = []
            for task in completed_tasks:
                completed_tasks_arr.append(task['task'])
            super_agi_prompt = super_agi_prompt.replace("{completed_tasks}", str(completed_tasks_arr))

        base_token_limit = TokenCounter.count_message_tokens([{"role": "user", "content": super_agi_prompt}])
        pending_tokens = token_limit - base_token_limit
        final_output = ""
        if "{task_history}" in super_agi_prompt:
            for task in reversed(completed_tasks[-10:]):
                final_output = f"Task: {task['task']}\nResult: {task['response']}\n" + final_output
                token_count = TokenCounter.count_message_tokens([{"role": "user", "content": final_output}])
                if token_count > min(600, pending_tokens):
                    break
            super_agi_prompt = super_agi_prompt.replace("{task_history}", "\n" + final_output + "\n")
        return super_agi_prompt
```

#### 1.2 Agent Prompt Template
```python
# superagi/agent/agent_prompt_template.py

FINISH_NAME = "finish"


class AgentPromptTemplate:

    @staticmethod
    def add_list_items_to_string(items: List[str]) -> str:
        list_string = ""
        for i, item in enumerate(items):
            list_string += f"{i + 1}. {item}\n"
        return list_string

    @classmethod
    def clean_prompt(cls, prompt):
        prompt = re.sub('[ \t]+', ' ', prompt)
        return prompt.strip()

    @classmethod
    def get_super_agi_single_prompt(cls):
        super_agi_prompt = PromptReader.read_agent_prompt(__file__, "superagi.txt")

        return {"prompt": super_agi_prompt, "variables": ["goals", "instructions", "constraints", "tools"]}

    @classmethod
    def start_task_based(cls):
        super_agi_prompt = PromptReader.read_agent_prompt(__file__, "initialize_tasks.txt")

        return {"prompt": AgentPromptTemplate.clean_prompt(super_agi_prompt), "variables": ["goals", "instructions"]}

    @classmethod
    def analyse_task(cls):
        constraints = [
            'Exclusively use the tools listed in double quotes e.g. "tool name"'
        ]
        super_agi_prompt = PromptReader.read_agent_prompt(__file__, "analyse_task.txt")
        super_agi_prompt = AgentPromptTemplate.clean_prompt(super_agi_prompt) \
            .replace("{constraints}", AgentPromptTemplate.add_list_items_to_string(constraints))
        return {"prompt": super_agi_prompt, "variables": ["goals", "instructions", "tools", "current_task"]}

    @classmethod
    def create_tasks(cls):
        super_agi_prompt = PromptReader.read_agent_prompt(__file__, "create_tasks.txt")
        return {"prompt": AgentPromptTemplate.clean_prompt(super_agi_prompt),
                "variables": ["goals", "instructions", "last_task", "last_task_result", "pending_tasks"]}

    @classmethod
    def prioritize_tasks(cls):
        super_agi_prompt = PromptReader.read_agent_prompt(__file__, "prioritize_tasks.txt")
        return {"prompt": AgentPromptTemplate.clean_prompt(super_agi_prompt),
                "variables": ["goals", "instructions", "last_task", "last_task_result", "pending_tasks"]}
```

---

### 2. Tool Schemas (7)

#### 2.1 Read File Tool
```python
# superagi/tools/file/read_file.py

class ReadFileSchema(BaseModel):
    """Input for CopyFileTool."""
    file_name: str = Field(..., description="Path of the file to read")


class ReadFileTool(BaseTool):
    """
    Read File tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "Read File"
    agent_id: int = None
    agent_execution_id: int = None
    args_schema: Type[BaseModel] = ReadFileSchema
    description: str = "Reads the file content in a specified location"
    resource_manager: Optional[FileManager] = None
```

#### 2.2 Write File Tool
```python
# superagi/tools/file/write_file.py

class WriteFileInput(BaseModel):
    """Input for CopyFileTool."""
    file_name: str = Field(..., description="Name of the file to write. Only include the file name. Don't include path.")
    content: str = Field(..., description="File content to write")


class WriteFileTool(BaseTool):
    """
    Write File tool

    Attributes:
        name : The name.
        description : The description.
        agent_id: The agent id.
        args_schema : The args schema.
        resource_manager: File resource manager.
    """
    name: str = "Write File"
    args_schema: Type[BaseModel] = WriteFileInput
    description: str = "Writes text to a file"
    agent_id: int = None
    resource_manager: Optional[FileManager] = None
```

#### 2.3 Improve Code Tool
```python
# superagi/tools/code/improve_code.py

class ImproveCodeSchema(BaseModel):
    pass


class ImproveCodeTool(BaseTool):
    """
    Used to improve the already generated code by reading the code from the files

    Attributes:
        llm: LLM used for code generation.
        name : The name of the tool.
        description : The description of the tool.
        resource_manager: Manages the file resources.
    """
    llm: Optional[BaseLlm] = None
    agent_id: int = None
    agent_execution_id: int = None
    name = "ImproveCodeTool"
    description = (
        "This tool improves the generated code."
    )
    args_schema: Type[ImproveCodeSchema] = ImproveCodeSchema
    resource_manager: Optional[FileManager] = None
    tool_response_manager: Optional[ToolResponseQueryManager] = None
    goals: List[str] = []
```

#### 2.4 Coding Tool (Write Code)
```python
# superagi/tools/code/write_code.py

class CodingSchema(BaseModel):
    code_description: str = Field(
        ...,
        description="Description of the coding task",
    )


class CodingTool(BaseTool):
    """
    Used to generate code.

    Attributes:
        llm: LLM used for code generation.
        name : The name of tool.
        description : The description of tool.
        args_schema : The args schema.
        goals : The goals.
        resource_manager: Manages the file resources
    """
    llm: Optional[BaseLlm] = None
    agent_id: int = None
    agent_execution_id: int = None
    name = "CodingTool"
    description = (
        "You will get instructions for code to write. You will write a very long answer. "
        "Make sure that every detail of the architecture is, in the end, implemented as code. "
        "Think step by step and reason yourself to the right decisions to make sure we get it right. "
        "You will first lay out the names of the core classes, functions, methods that will be necessary, "
        "as well as a quick comment on their purpose. Then you will output the content of each file including each function and class and ALL code."
    )
    args_schema: Type[CodingSchema] = CodingSchema
    goals: List[str] = []
    resource_manager: Optional[FileManager] = None
    tool_response_manager: Optional[ToolResponseQueryManager] = None

    def _execute(self, code_description: str) -> str:
        """Execute the write_code tool.

        Args:
            code_description : The coding task description.

        Returns:
            Generated code with where the code is being saved or error message.
        """
        prompt = PromptReader.read_tools_prompt(__file__, "write_code.txt") + "\nUseful to know:\n" + PromptReader.read_tools_prompt(__file__, "generate_logic.txt")
        prompt = prompt.replace("{goals}", AgentPromptBuilder.add_list_items_to_string(self.goals))
        prompt = prompt.replace("{code_description}", code_description)
        # ... code generation logic
```

#### 2.5 Write Test Tool
```python
# superagi/tools/code/write_test.py

class WriteTestSchema(BaseModel):
    test_description: str = Field(
        ...,
        description="Description of the testing task",
    )
    test_file_name: str = Field(
        ...,
        description="Name of the file to write. Only include the file name. Don't include path."
    )


class WriteTestTool(BaseTool):
    """
    Used to generate unit tests based on the specification.

    Attributes:
        llm: LLM used for test generation.
        name : The name of tool.
        description : The description of tool.
        args_schema : The args schema.
        goals : The goals.
        resource_manager: Manages the file resources
    """
    name = "WriteTestTool"
    description = (
        "You are a super smart developer using Test Driven Development to write tests according to a specification.\n"
        "Please generate tests based on the above specification. The tests should be as simple as possible, "
        "but still cover all the functionality.\n"
        "Write it in the file"
    )
    args_schema: Type[WriteTestSchema] = WriteTestSchema
```

#### 2.6 DuckDuckGo Search Tool
```python
# superagi/tools/duck_duck_go/duck_duck_go_search.py

class DuckDuckGoSearchSchema(BaseModel):
    query: str = Field(
        ...,
        description="The search query for duckduckgo search.",
    )


class DuckDuckGoSearchTool(BaseTool):
    """
    Duck Duck Go Search tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "DuckDuckGoSearch"
    description = (
        "A tool for performing a DuckDuckGo search and extracting snippets and webpages."
        "Input should be a search query."
    )
    args_schema: Type[DuckDuckGoSearchSchema] = DuckDuckGoSearchSchema
```

#### 2.7 Send Email Tool
```python
# superagi/tools/email/send_email.py

class SendEmailInput(BaseModel):
    to: str = Field(..., description="Email Address of the Receiver, default email address is 'example@example.com'")
    subject: str = Field(..., description="Subject of the Email to be sent")
    body: str = Field(..., description="Email Body to be sent. Escape special characters in the body. Do not add senders details and end it with Warm Regards without entering any name.")


class SendEmailTool(BaseTool):
    """
    Send an Email tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "Send Email"
    args_schema: Type[BaseModel] = SendEmailInput
    description: str = "Send an Email"
```

---

### 3. Skills (0)

Note: SuperAGI does not include bundled SKILL.md files. The framework uses configured toolsets instead of skill definitions.

---

## Evaluation Dimensions

### 1. Role Clarity
- [ ] Clear separation between prompt building, templates, and tools
- [ ] Task-based workflow phases (initialize, analyze, create, prioritize)
- [ ] Variable substitution system for prompt customization

### 2. Workflow Completeness
- [ ] Task creation and prioritization
- [ ] Code generation with architecture planning
- [ ] Token-limited history management

### 3. Prompt Consistency
- [ ] Standardized variable format ({goals}, {instructions}, etc.)
- [ ] Template-based prompt generation
- [ ] Automatic tool schema injection

### 4. Tool Modularity
- [ ] BaseTool abstraction for tool creation
- [ ] JSON schema for tool arguments
- [ ] Resource management integration

### 5. Observability
- [ ] Token counting and limiting
- [ ] Task history tracking
- [ ] Execution logging

### 6. Extensibility
- [ ] Custom tool creation
- [ ] Template extension
- [ ] Resource manager integration

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
1. **Task workflow**: Test complete task creation, analysis, and prioritization
2. **Code generation**: Test CodingTool with architecture planning
3. **File operations**: Test read/write tools with various file types

### Unit Tests
1. **Prompt building**: Verify correct variable substitution
2. **Tool schema generation**: Test JSON schema output
3. **Token counting**: Verify token limit enforcement

### Integration Tests
1. **Web search**: Test DuckDuckGo search integration
2. **Email sending**: Test email tool functionality
3. **Code analysis**: Test code analyser tool

---

## Notes

- **MIT license** allows full quotation and modification
- SuperAGI emphasizes **autonomous task execution** with structured workflows
- The prompt builder provides **dynamic prompt construction**
- Tools cover **file operations, code generation, and web search**