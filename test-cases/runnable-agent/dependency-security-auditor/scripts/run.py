#!/usr/bin/env python3
"""
Dependency & Security Auditor - Agent startup script

Uses sanityops_agent framework to start the auditor agent.
Automatically scans tools/ directory for tool registration.
"""

import sys
import asyncio
import importlib.util
from pathlib import Path
from typing import Any, Dict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_system_prompt() -> str:
    """Load system prompt from prompts/system.txt"""
    system_file = project_root / "prompts" / "system.txt"
    if system_file.exists():
        return system_file.read_text(encoding="utf-8")
    return "You are a Dependency & Security Auditor."


def print_banner():
    """Print startup banner."""
    print("=" * 60)
    print("  Dependency & Security Auditor v1.0.0")
    print("  Scans Python and Node.js dependencies for vulnerabilities")
    print("=" * 60)
    print()


def main():
    """Main entry point."""
    print_banner()

    # Check for sanityops_agent availability
    try:
        from sanityops_agent import (
            AgentFactory,
            ToolRegistry,
            Tool,
            ToolResult,
            ToolContext,
            ProviderConfig,
        )
        from sanityops_agent.llm.factory import ProviderFactory
    except ImportError:
        print("Error: sanityops_agent package not found.")
        print()
        print("Please install it first:")
        print("  pip install sanityops_agent")
        print()
        print("Or contact your administrator for access.")
        sys.exit(1)

    # Load system prompt
    print("[1] Loading system prompt...")
    system_prompt = load_system_prompt()
    print(f"    Loaded {len(system_prompt)} characters")

    # Create tool registry
    print("\n[2] Scanning tools...")
    context = ToolContext()
    registry = ToolRegistry(context)

    # Scan and register tools
    tools_dir = project_root / "tools"
    tool_count = 0

    if tools_dir.exists():
        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name.startswith("_"):
                continue

            tool_name = tool_file.stem
            spec = importlib.util.spec_from_file_location(tool_name, tool_file)

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[tool_name] = module
                spec.loader.exec_module(module)

                if hasattr(module, "execute"):
                    docstring = module.__doc__ or ""
                    description = docstring.strip().split("\n")[0]

                    # Create tool wrapper
                    execute_func = module.execute

                    def make_executor(func, name):
                        async def execute(self, params=None, **kwargs):
                            try:
                                result = func(params or {})
                                return ToolResult(
                                    content=str(result.get("data", result.get("error", ""))),
                                    success=result.get("status") == "success",
                                    metadata=result
                                )
                            except Exception as e:
                                return ToolResult(
                                    content=f"Error: {str(e)}",
                                    success=False,
                                    metadata={"error": str(e)}
                                )
                        return execute

                    DynamicTool = type(
                        f"{tool_name.capitalize()}Tool",
                        (Tool,),
                        {
                            "name": tool_name,
                            "description": description,
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "params": {"type": "object"}
                                }
                            },
                            "execute": make_executor(execute_func, tool_name),
                        }
                    )

                    registry.register(DynamicTool())
                    tool_count += 1
                    print(f"    Registered: {tool_name}")

    print(f"    Total tools: {tool_count}")

    # Create provider
    print("\n[3] Creating LLM provider...")
    config = ProviderConfig()

    if not config.API_KEY:
        print()
        print("Error: No API key configured.")
        print()
        print("Please set the following environment variables:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # or openai")
        print()
        print("Or create a .env file in the project directory.")
        sys.exit(1)

    provider = ProviderFactory.create(config)
    print(f"    Provider: {provider.model}")

    # Create agent
    print("\n[4] Creating agent...")
    factory = AgentFactory(
        provider=provider,
        tool_registry=registry,
    )
    agent = factory.create_parent_agent(
        system_prompt=system_prompt,
    )

    print("\n" + "-" * 60)
    print("Agent ready. Type your message to begin.")
    print("Commands: 'quit' or 'exit' to stop")
    print("-" * 60)
    print()

    # Interaction loop
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nGoodbye!")
                break

            print("\nAuditor: ", end="", flush=True)
            result = asyncio.run(agent.run(user_input))
            print(result.text)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            continue


if __name__ == "__main__":
    main()