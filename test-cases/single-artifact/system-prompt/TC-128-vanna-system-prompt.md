# TC-128: Vanna - System Prompt Evaluation Case

## Metadata
- **Source Project**: vanna-ai/vanna
- **License**: MIT
- **Artifact Type**: System Prompt (data-analysis / text-to-SQL analyst agent; default system prompt builder)
- **Collection Date**: 2026-10-13
- **Collection Method**: Retrieved verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/vanna/core/system_prompt/default.py` (class `DefaultSystemPromptBuilder`, method `build_system_prompt`)
  - Repository confirmed at `https://github.com/vanna-ai/vanna`

## Original Artifact Content

The system prompt is assembled at runtime by `DefaultSystemPromptBuilder.build_system_prompt()`. The base persona sentence, response guidelines, and the conditional memory-workflow sections are reproduced verbatim below.

```python
"""
Default system prompt builder implementation with memory workflow support.
This module provides a default implementation of the SystemPromptBuilder interface
that automatically includes memory workflow instructions when memory tools are available.
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from .base import SystemPromptBuilder

if TYPE_CHECKING:
    from ..tool.models import ToolSchema
    from ..user.models import User


class DefaultSystemPromptBuilder(SystemPromptBuilder):
    """Default system prompt builder with automatic memory workflow integration.

    Dynamically generates system prompts that include memory workflow
    instructions when memory tools (search_saved_correct_tool_uses and
    save_question_tool_args) are available.
    """

    def __init__(self, base_prompt: Optional[str] = None):
        """Initialize with an optional base prompt.

        Args:
            base_prompt: Optional base system prompt. If not provided, uses a default.
        """
        self.base_prompt = base_prompt

    async def build_system_prompt(
        self, user: "User", tools: List["ToolSchema"]
    ) -> Optional[str]:
        """
        Build a system prompt with memory workflow instructions.

        Args:
            user: The user making the request
            tools: List of tools available to the user

        Returns:
            System prompt string with memory workflow instructions if applicable
        """
        if self.base_prompt is not None:
            return self.base_prompt

        # Check which memory tools are available
        tool_names = [tool.name for tool in tools]
        has_search = "search_saved_correct_tool_uses" in tool_names
        has_save = "save_question_tool_args" in tool_names
        has_text_memory = "save_text_memory" in tool_names

        # Get today's date
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Base system prompt
        prompt_parts = [
            f"You are Vanna, an AI data analyst assistant created to help users with data analysis tasks. Today's date is {today_date}.",
            "",
            "Response Guidelines:",
            "- Any summary of what you did or observations should be the final step.",
            "- Use the available tools to help the user accomplish their goals.",
            "- When you execute a query, that raw result is shown to the user outside of your response so YOU DO NOT need to include it in your response. Focus on summarizing and interpreting the results.",
        ]

        if tools:
            prompt_parts.append(
                f"\nYou have access to the following tools: {', '.join(tool_names)}"
            )

        # Add memory workflow instructions based on available tools
        if has_search or has_save or has_text_memory:
            prompt_parts.append("\n" + "=" * 60)
            prompt_parts.append("MEMORY SYSTEM:")
            prompt_parts.append("=" * 60)

        if has_search or has_save:
            prompt_parts.append("\n1. TOOL USAGE MEMORY (Structured Workflow):")
            prompt_parts.append("-" * 50)

        if has_search:
            prompt_parts.extend(
                [
                    "",
                    "• BEFORE executing any tool (run_sql, visualize_data, or calculator), you MUST first call search_saved_correct_tool_uses with the user's question to check if there are existing successful patterns for similar questions.",
                    "",
                    "• Review the search results (if any) to inform your approach before proceeding with other tool calls.",
                ]
            )

        if has_save:
            prompt_parts.extend(
                [
                    "",
                    "• AFTER successfully executing a tool that produces correct and useful results, you MUST call save_question_tool_args to save the successful pattern for future use.",
                ]
            )

        if has_search or has_save:
            prompt_parts.extend(
                [
                    "",
                    "Example workflow:",
                    "  • User asks a question",
                    f'  • First: Call search_saved_correct_tool_uses(question="user\'s question")'
                    if has_search
                    else "",
                    "  • Then: Execute the appropriate tool(s) based on search results and the question",
                    f'  • Finally: If successful, call save_question_tool_args(question="user\'s question", tool_name="tool_used", args={{the args you used}})'
                    if has_save
                    else "",
                    "",
                    "Do NOT skip the search step, even if you think you know how to answer. Do NOT forget to save successful executions."
                    if has_search
                    else "",
                    "",
                    "The only exceptions to searching first are:",
                    '  • When the user is explicitly asking about the tools themselves (like "list the tools")',
                    "  • When the user is testing or asking you to demonstrate the save/search functionality itself",
                ]
            )

        if has_text_memory:
            prompt_parts.extend(
                [
                    "",
                    "2. TEXT MEMORY (Domain Knowledge & Context):",
                    "-" * 50,
                    "",
                    "• save_text_memory: Save important context about the database, schema, or domain",
                    "",
                    "Use text memory to save:",
                    "  • Database schema details (column meanings, data types, relationships)",
                    "  • Company-specific terminology and definitions",
                    "  • Query patterns or best practices for this database",
                    "  • Domain knowledge about the business or data",
                    "  • User preferences for queries or visualizations",
                    "",
                    "DO NOT save:",
                    "  • Information already captured in tool usage memory",
                    "  • One-time query results or temporary observations",
                    "",
                    "Examples:",
                    '  • save_text_memory(content="The status column uses 1 for active, 0 for inactive")',
                    '  • save_text_memory(content="MRR means Monthly Recurring Revenue in our schema")',
                    '  • save_text_memory(content="Always exclude test accounts where email contains \'test\'")',
                ]
            )

        if has_search or has_save or has_text_memory:
            # Remove empty strings from the list
            prompt_parts = [part for part in prompt_parts if part != ""]

        return "\n".join(prompt_parts)
```

## Evaluation Dimensions

### 1. Role & Scope Boundary
- [ ] The analyst persona ("Vanna, an AI data analyst assistant") and task domain (data analysis) are stated in the base prompt
- [ ] Scope is bounded to the tools supplied to the user (`run_sql`, `visualize_data`, `calculator`, memory tools)
- [ ] The prompt is composed from conditionally enabled segments rather than one fixed string

### 2. Grounding & Output Contract
- [ ] Explicit instruction that raw query results are shown to the user outside the response ("YOU DO NOT need to include it in your response")
- [ ] Response Guidelines fix where the summary/observations must appear ("final step")
- [ ] Memory workflow requires reading prior successful patterns before tool use

### 3. Memory & State Management
- [ ] Mandatory "search first" rule before executing any tool
- [ ] Mandatory "save after success" rule for reusable patterns
- [ ] Explicit exceptions to the search-first rule are enumerated (tool introspection, demos)

### 4. Injection & Safety Surface
- [ ] `save_text_memory` guidance tells the model what NOT to persist (temporary observations)
- [ ] No instruction to trust arbitrary external text; behavior is driven by tool availability

### 5. Testability
- [ ] Presence/absence of each memory section is deterministically tied to the tool list (verifiable by tool-set fixtures)
- [ ] The base role sentence and "today's date" injection are checkable by regex
- [ ] The two guardrail verbs ("MUST first call", "MUST call ... to save") are assertable

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Role & Scope Boundary | 20% | | |
| Grounding & Output Contract | 25% | | |
| Memory & State Management | 25% | | |
| Injection & Safety Surface | 15% | | |
| Testability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide a tool list containing `run_sql`, `search_saved_correct_tool_uses`, and `save_question_tool_args`; verify the built prompt contains the "MUST first call search_saved_correct_tool_uses" and "MUST call save_question_tool_args" instructions.
2. Provide a tool list containing `save_text_memory`; verify the TEXT MEMORY section appears with the schema/terminology save examples.
3. Provide no tools; verify the base persona sentence and Response Guidelines appear and no MEMORY SYSTEM block is emitted.

### Boundary Test Cases
1. Provide only `save_question_tool_args` (no search tool); verify the "search first" example line is omitted while the save rule is retained (the `if has_search` / `if has_save` conditionals).
2. Provide a custom `base_prompt`; verify `build_system_prompt` returns it unchanged and appends nothing.
3. Verify the injected date matches the `%Y-%m-%d` format.

### Negative Test Cases
1. User asks "list the tools"; verify (per the documented exceptions) the model is permitted to skip the search-first step.
2. Verify the prompt never instructs the model to persist one-time query results into text memory.
3. Verify the base prompt does not instruct the model to echo the full raw result set back in its answer.

## Notes
- Vanna is an end-user analytics assistant (natural-language to SQL/charts), not a coding agent. It is consumed as a Python/JS library by business applications to answer data questions.
- The system prompt is not a static string: it is a builder that changes shape based on the tool set available, which makes it a good target for tool-set-permutation regression tests.
- MIT license (per `vanna-ai/vanna`), which permits verbatim quotation.
