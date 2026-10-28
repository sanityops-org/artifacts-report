"""Pretty-print hook for the aircraft maintenance agent."""

from typing import Any

from sanityops_agent import Hook, HookContext, HookEvent


class PrettyOutputHook(Hook):
    """Print model reasoning, tool calls, and token usage."""

    name = "pretty_output"
    description = "Pretty-print tool calls and reasoning output"
    priority = 100

    events = [
        HookEvent.BEFORE_LLM_CALL,
        HookEvent.AFTER_LLM_CALL,
        HookEvent.BEFORE_TOOL_EXEC,
        HookEvent.AFTER_TOOL_EXEC,
    ]

    def __init__(self):
        super().__init__()
        self.iteration = 0

    async def handle(self, ctx: HookContext) -> HookContext:
        """Handle hook events."""
        if ctx.event == HookEvent.BEFORE_LLM_CALL:
            self._print_before_llm(ctx)
        elif ctx.event == HookEvent.AFTER_LLM_CALL:
            self._print_after_llm(ctx)
        elif ctx.event == HookEvent.BEFORE_TOOL_EXEC:
            self._print_before_tool(ctx)
        elif ctx.event == HookEvent.AFTER_TOOL_EXEC:
            self._print_after_tool(ctx)
        return ctx

    def _print_before_llm(self, ctx: HookContext) -> None:
        """Print before an LLM call."""
        self.iteration = ctx.data.get("iteration", self.iteration + 1)
        print()
        print("-" * 50)
        print(f"Iteration #{self.iteration + 1} - thinking...")
        print("-" * 50)

    def _print_after_llm(self, ctx: HookContext) -> None:
        """Print the LLM response summary."""
        response = ctx.data.get("response")
        if response and hasattr(response, "content") and response.content:
            for block in response.content:
                block_type = getattr(block, "type", None)
                if block_type and "thinking" in str(block_type).lower():
                    thinking = getattr(block, "thinking", "")
                    if thinking:
                        print()
                        print("Reasoning:")
                        for line in self._truncate(thinking, 500).split("\n"):
                            print(f"   {line}")
                elif hasattr(block, "text") and block.text:
                    print()
                    print("AI output:")
                    for line in self._truncate(block.text, 300).split("\n"):
                        print(f"   {line}")

        if response and hasattr(response, "usage") and response.usage:
            inp = response.usage.get("input_tokens", "?")
            out = response.usage.get("output_tokens", "?")
            print()
            print(f"Token usage: input={inp}, output={out}")

    def _print_before_tool(self, ctx: HookContext) -> None:
        """Print the start of a tool call."""
        tool_name = ctx.data.get("tool_name", "unknown")
        tool_input = ctx.data.get("tool_input", {})
        print()
        print(f"Calling tool: {tool_name}")
        if tool_input:
            print("   Input parameters:")
            for key, value in tool_input.items():
                print(f"     - {key}: {self._format_value(value)}")

    def _print_after_tool(self, ctx: HookContext) -> None:
        """Print tool-call results."""
        result = ctx.data.get("result", "")
        is_error = ctx.data.get("is_error", False)
        print(f"   {'Error' if is_error else 'Result'}:")
        if result:
            for line in self._truncate(str(result), 400).split("\n"):
                print(f"     {line}")

    def _truncate(self, text: str, max_len: int) -> str:
        """Truncate long output."""
        if len(text) > max_len:
            return text[:max_len] + f"\n   ... ({len(text)} characters total)"
        return text

    def _format_value(self, value: Any, max_len: int = 80) -> str:
        """Format a display value."""
        if isinstance(value, str):
            if len(value) > max_len:
                return f'"{value[:max_len]}..." ({len(value)} characters)'
            return f'"{value}"'
        if isinstance(value, list):
            return f"[{len(value)} items]"
        if isinstance(value, dict):
            return f"{{{len(value)} items}}"
        return str(value)
