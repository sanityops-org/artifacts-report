#!/usr/bin/env python3
"""
Code Review Assistant - Simplified Entry Point

Use:
    uv run main.py <Code folder path>

Features:
    - Automatically read all code files in the folder
    - Beautiful output tool call, reasoning process
    - Generate a structured review report
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Any

# Resolve the agent project directory
AGENT_DIR = Path(__file__).parent
sys.path.insert(0, str(AGENT_DIR))

from sanityops_agent import (
    AgentConfig,
    AgentFactory,
    ProviderConfig,
    ToolRegistry,
    ToolContext,
    Hook,
    HookEvent,
    HookContext,
    HookExecutor,
)
from sanityops_agent.llm.factory import ProviderFactory

# Import tools
from skills.code_review.tools.analyze_code import AnalyzeCodeTool
from skills.code_review.tools.generate_report import GenerateReportTool


# ============================================================
# Pretty-print output hook
# ============================================================

class PrettyOutputHook(Hook):
    """Pretty-print the agent runtime."""

    name = "pretty_output"
    description = "Pretty-print tool calls and reasoning output"
    priority = 100  # Default priority

    # Subscribe to all available events
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

    def _print_before_llm(self, ctx: HookContext):
        """Print before LLM call"""
        self.iteration = ctx.data.get("iteration", self.iteration + 1)
        print()
        print(f"{'─' * 50}")
        print(f"🔄 Iteration #{self.iteration + 1} - Thinking...")
        print(f"{'─' * 50}")

    def _print_after_llm(self, ctx: HookContext):
        """Print LLM response"""
        response = ctx.data.get("response")

        if response and hasattr(response, "content") and response.content:
            for block in response.content:
                block_type = getattr(block, "type", None)

                # Handle thinking blocks
                if block_type and "thinking" in str(block_type).lower():
                    thinking = getattr(block, "thinking", "")
                    if thinking:
                        print()
                        print("🧠 Reasoning:")
                        for line in self._truncate(thinking, 500).split("\n"):
                            print(f"   {line}")

                # Handle text blocks
                elif hasattr(block, "text"):
                    text = block.text
                    if text:
                        print()
                        print("💭 AI output:")
                        for line in self._truncate(text, 300).split("\n"):
                            print(f"   {line}")

        # Token usage
        if response and hasattr(response, "usage") and response.usage:
            inp = response.usage.get("input_tokens", "?")
            out = response.usage.get("output_tokens", "?")
            print()
            print(f"📊 Token: Input {inp} | Output {out}")

    def _print_before_tool(self, ctx: HookContext):
        """Print the start of a tool call."""
        tool_name = ctx.data.get("tool_name", "unknown")
        tool_input = ctx.data.get("tool_input", {})

        print()
        print(f"🔧 Calling tool: {tool_name}")

        if tool_input:
            print("   Input parameters:")
            for key, value in tool_input.items():
                val_str = self._format_value(value)
                print(f"     • {key}: {val_str}")

    def _print_after_tool(self, ctx: HookContext):
        """Print tool-call results."""
        tool_name = ctx.data.get("tool_name", "unknown")
        result = ctx.data.get("result", "")
        is_error = ctx.data.get("is_error", False)

        icon = "❌" if is_error else "✅"
        print(f"   {icon} Result:")

        if result:
            for line in self._truncate(str(result), 400).split("\n"):
                print(f"     {line}")

    def _truncate(self, text: str, max_len: int) -> str:
        """Truncate text."""
        if len(text) > max_len:
            return text[:max_len] + f"\n   ... (Total {len(text)} characters)"
        return text

    def _format_value(self, value: Any, max_len: int = 80) -> str:
        """Format a display value."""
        if isinstance(value, str):
            if len(value) > max_len:
                return f'"{value[:max_len]}..." ({len(value)} characters)'
            return f'"{value}"'
        elif isinstance(value, list):
            return f"[{len(value)} items]"
        elif isinstance(value, dict):
            return f"{{{len(value)} items}}"
        return str(value)


# ============================================================
# Code file reading
# ============================================================

def read_code_files(folder_path: str) -> dict[str, str]:
    """Read all the code files in the folder"""
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"The folder does not exist.: {folder}")

    # Supported code file extensions
    code_extensions = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs",
        ".cpp", ".c", ".h", ".hpp", ".cs", ".rb", ".php", ".swift",
        ".kt", ".scala", ".vue", ".svelte", ".sh", ".sql"
    }

    code_files = {}

    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.suffix in code_extensions:
            # Skip irrelevant directories
            skip_dirs = {"node_modules", "__pycache__", ".git", "venv", ".venv", "dist", "build", ".pytest_cache"}
            if any(part in file_path.parts for part in skip_dirs):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                relative_path = file_path.relative_to(folder)
                code_files[str(relative_path)] = content
            except Exception as e:
                print(f"⚠️  Unable to read {file_path.name}: {e}")

    return code_files


def format_code_for_review(code_files: dict[str, str]) -> str:
    """Format the collected code for review."""
    lines = []
    lines.append("Please review the following code files comprehensively.")
    lines.append("Identify security vulnerabilities, performance problems and readability problems, and provide specific suggestions for improvement.")
    lines.append("")
    lines.append("=" * 60)
    lines.append("Code to be reviewed")
    lines.append("=" * 60)

    for file_path, content in code_files.items():
        lines.append(f"\n### Document: {file_path}")
        lines.append(f"Lines: {len(content.splitlines())}")
        lines.append("-" * 40)
        lines.append(f"```\n{content}\n```")

    return "\n".join(lines)


# ============================================================
# Main program
# ============================================================

def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = AGENT_DIR / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a professional code review assistant."


def create_tool_registry() -> ToolRegistry:
    """Create the tool registry."""
    context = ToolContext()
    registry = ToolRegistry(context)
    registry.register(AnalyzeCodeTool(context))
    registry.register(GenerateReportTool(context))
    return registry


def print_banner():
    """Print the launch banner"""
    print()
    print("╔" + "═" * 48 + "╗")
    print("║" + "Code review assistant".center(46) + "║")
    print("║" + "Code Review Assistant v1.0".center(46) + "║")
    print("╚" + "═" * 48 + "╝")
    print()


def print_summary(result, elapsed: float, files_count: int):
    """Print the execution summary."""
    print()
    print("═" * 50)
    print("📊 Execution summary")
    print("═" * 50)
    print(f"  Files reviewed: {files_count}")
    print(f"  Iterations:     {result.loops_used}")
    print(f"  Execution time: {elapsed:.2f} seconds")

    if result.error:
        print(f"  Status: ❌ Failure - {result.error}")
    else:
        print(f"  Status: ✅ Success")


def print_report(result):
    """Print the review report"""
    if result.text:
        print()
        print("═" * 50)
        print("📋 Review report")
        print("═" * 50)
        print()
        print(result.text)


async def run_agent(folder_path: str):
    """Run code review"""
    start_time = datetime.now()

    # Read the code file
    print(f"📂 Reading code folder: {folder_path}")
    code_files = read_code_files(folder_path)

    if not code_files:
        print("❌ No code files were found.")
        return 1

    print(f"   Found {len(code_files)} code files:")
    for path in code_files.keys():
        print(f"     • {path}")

    # Build the review request
    review_request = format_code_for_review(code_files)

    # Load configuration (automatically read from .env)
    provider_config = ProviderConfig()

    if not provider_config.API_KEY:
        print()
        print("❌ API key is not configured.")
        print()
        print("Please configure it in the .env file:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # or openai")
        print()
        print("Optional:")
        print("  LLM_BASE_URL=...")
        print("  LLM_MODEL_ID=...")
        return 1

    # Create the provider
    provider = ProviderFactory.create(provider_config)

    print(f"\n🤖 Model: {provider_config.MODEL_ID}")
    print(f"   Provider: {provider_config.PROVIDER}")

    # Create tools, hooks, and the agent
    tool_registry = create_tool_registry()
    agent_config = AgentConfig()

    hook_executor = HookExecutor()
    hook_executor.register(PrettyOutputHook())

    factory = AgentFactory(
        provider=provider,
        config=agent_config,
        tool_registry=tool_registry,
        hook_executor=hook_executor,
    )

    agent = factory.create_parent_agent(system_prompt=load_system_prompt())

    print()
    print("🚀 Starting review...")
    print("─" * 50)

    # Run the agent
    result = await agent.run(review_request)

    # Print the result
    elapsed = (datetime.now() - start_time).total_seconds()
    print_summary(result, elapsed, len(code_files))
    print_report(result)

    return 0 if not result.error else 1


def main():
    """Main entrance"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Code Review Assistant - review a code folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ./src
  python main.py /path/to/project

Configuration:
  Create a .env file:
    LLM_API_KEY=your-api-key
    LLM_PROVIDER=anthropic
        """
    )

    parser.add_argument("folder", help="The path of the code folder to be reviewed")

    args = parser.parse_args()
    print_banner()

    try:
        return asyncio.run(run_agent(args.folder))
    except KeyboardInterrupt:
        print("\n\n⚠️  User interruption")
        return 130
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Failed to run: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
