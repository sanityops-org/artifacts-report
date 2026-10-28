#!/usr/bin/env python3
"""
Expense Compliance Auditor - Agent startup script

Starts the agent through the sanityops_agent framework. Tools are discovered by
convention: every module in tools/ that exposes execute() is registered
automatically, and its description is the first line of its module docstring.
"""

import asyncio
import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_system_prompt():
    """Load the system prompt from prompts/system.txt."""
    system_file = PROJECT_ROOT / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are an Expense Compliance Auditor."


def print_banner():
    """Print the startup banner."""
    print("=" * 60)
    print("  Expense Compliance Auditor v1.0.0")
    print("  Audits expense batches against a configurable policy")
    print("=" * 60)
    print()


def load_tool_modules():
    """Import every tools/*.py module that exposes an execute() function."""
    tools_dir = PROJECT_ROOT / "tools"
    modules = []

    if not tools_dir.exists():
        return modules

    for tool_file in sorted(tools_dir.glob("*.py")):
        if tool_file.name.startswith("_"):
            continue

        tool_name = tool_file.stem
        spec = importlib.util.spec_from_file_location(tool_name, tool_file)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        sys.modules[tool_name] = module
        spec.loader.exec_module(module)

        if hasattr(module, "execute"):
            modules.append((tool_name, module))

    return modules


def build_registry(Tool, ToolResult, ToolContext, ToolRegistry, modules):
    """Wrap each tool module in a Tool instance and register it."""
    registry = ToolRegistry(ToolContext())

    for tool_name, module in modules:
        description = (module.__doc__ or "").strip().split("\n")[0]
        execute_func = module.execute

        def make_executor(func):
            async def tool_execute(self, params=None, **kwargs):
                try:
                    result = func(params or {})
                    return ToolResult(
                        content=str(result.get("data", result.get("error", ""))),
                        success=result.get("status") == "success",
                        metadata=result,
                    )
                except Exception as exc:  # noqa: BLE001 - surfaced to the model, never fatal
                    return ToolResult(
                        content=f"Error: {exc}",
                        success=False,
                        metadata={"error": str(exc)},
                    )

            return tool_execute

        dynamic_tool = type(
            f"{tool_name.capitalize()}Tool",
            (Tool,),
            {
                "name": tool_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {"params": {"type": "object"}},
                },
                "execute": make_executor(execute_func),
            },
        )
        registry.register(dynamic_tool())
        print(f"    Registered: {tool_name}")

    return registry


def main():
    """Start the agent."""
    print_banner()

    try:
        from sanityops_agent import (
            AgentFactory,
            ProviderConfig,
            Tool,
            ToolContext,
            ToolRegistry,
            ToolResult,
        )
        from sanityops_agent.llm.factory import ProviderFactory
    except ImportError:
        print("Error: sanityops_agent package not found.")
        print()
        print("Please install it first:")
        print("  pip install sanityops_agent")
        print()
        print("Or contact your administrator for access.")
        return 1

    print("[1] Loading system prompt...")
    system_prompt = load_system_prompt()
    print(f"    Loaded {len(system_prompt)} characters")

    print()
    print("[2] Scanning tools...")
    modules = load_tool_modules()
    registry = build_registry(Tool, ToolResult, ToolContext, ToolRegistry, modules)
    print(f"    Total tools: {len(modules)}")

    print()
    print("[3] Creating the LLM provider...")
    config = ProviderConfig(_env_file=(PROJECT_ROOT / ".env", PROJECT_ROOT.parent / ".env"))
    if not config.API_KEY:
        print()
        print("Error: No API key configured.")
        print()
        print("Please set the following environment variables:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # or openai")
        print()
        print("Or create a .env file in the project directory.")
        return 1

    provider = ProviderFactory.create(config)
    print(f"    Provider: {provider.model}")

    print()
    print("[4] Creating the agent...")
    factory = AgentFactory(provider=provider, tool_registry=registry)
    agent = factory.create_parent_agent(system_prompt=system_prompt)

    print()
    print("-" * 60)
    print("Agent ready. Type your message to begin.")
    print("Commands: 'quit' or 'exit' to stop")
    print("-" * 60)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print()
                print("Goodbye!")
                return 0

            print()
            print("Auditor: ", end="", flush=True)
            result = asyncio.run(agent.run(user_input))
            print(result.text)
            print()

        except KeyboardInterrupt:
            print()
            print()
            print("Goodbye!")
            return 0
        except Exception as exc:  # noqa: BLE001 - keep the REPL alive
            print(f"Error: {exc}")
            continue


if __name__ == "__main__":
    sys.exit(main())