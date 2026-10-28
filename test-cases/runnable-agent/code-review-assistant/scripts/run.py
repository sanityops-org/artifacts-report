#!/usr/bin/env python3
"""
Agent Start the script

Start the code review assistant Agent and run it using the sanityops_agent framework.
LLM Configuration through .env file settings (LLM_API_KEY, LLM_PROVIDER, etc.).
"""

import sys
import os
import asyncio
from pathlib import Path

# Add the project path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sanityops_agent import (
    AgentConfig,
    AgentFactory,
    ProviderConfig,
    ToolRegistry,
    ToolContext,
)
from sanityops_agent.llm.factory import ProviderFactory

# Import custom tools
from skills.code_review.tools.analyze_code import AnalyzeCodeTool
from skills.code_review.tools.generate_report import GenerateReportTool


def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = project_root / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a professional code review assistant to help users analyze and improve code quality."


def create_tool_registry() -> ToolRegistry:
    """Create a tool registration form"""
    context = ToolContext()
    registry = ToolRegistry(context)
    registry.register(AnalyzeCodeTool(context))
    registry.register(GenerateReportTool(context))
    return registry


def create_provider():
    """Set up LLM Provider

    The configuration automatically reads from .env through ProviderConfig:
    - LLM_API_KEY: API Key key
    - LLM_PROVIDER: Type of provider (anthropic/openai)
    - LLM_BASE_URL: Optional, custom endpoint
    - LLM_MODEL_ID: Optional, model ID
    """
    config = ProviderConfig()

    if not config.API_KEY:
        print("Warning: Not configured API Key")
        print()
        print("Please configure it in the .env file:")
        print("  LLM_API_KEY=your-api-key")
        print("  LLM_PROVIDER=anthropic  # Someone openai")
        print()
        print("Optional configuration:")
        print("  LLM_BASE_URL=...")
        print("  LLM_MODEL_ID=...")

    return ProviderFactory.create(config)


async def run_agent(user_input: str = None):
    """Be in motion Agent"""
    provider = create_provider()
    agent_config = AgentConfig()
    tool_registry = create_tool_registry()
    system_prompt = load_system_prompt()

    factory = AgentFactory(
        provider=provider,
        config=agent_config,
        tool_registry=tool_registry,
    )

    agent = factory.create_parent_agent(system_prompt=system_prompt)

    print(f"Code review assistant starts")
    print(f"Model: {provider.model}")
    print("-" * 60)

    if user_input:
        result = await agent.run(user_input)
        print("\n" + "=" * 60)
        print("Review results:")
        print("=" * 60)
        if hasattr(result, 'text'):
            print(result.text)
        elif hasattr(result, 'content'):
            print(result.content)
        else:
            print(str(result))
        return result
    else:
        print("Please enter the code you want to review (enter 'exit' to exit):")
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() == "exit":
                    print("Goodbye!")
                    break
                if not user_input:
                    continue

                result = await agent.run(user_input)
                print("\n" + "-" * 40)
                if hasattr(result, 'text'):
                    print(result.text)
                elif hasattr(result, 'content'):
                    print(result.content)
                else:
                    print(str(result))

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break


def main():
    """Main entrance"""
    import argparse

    parser = argparse.ArgumentParser(description="Code review assistant")
    parser.add_argument("--input", "-i", type=str, help="The path of the code file to be reviewed")
    parser.add_argument("--text", "-t", type=str, help="Enter the code to be reviewed directly")
    args = parser.parse_args()

    user_input = None
    if args.text:
        user_input = args.text
    elif args.input:
        input_path = Path(args.input)
        if input_path.exists():
            user_input = f"Please review the following codes:\n\n{input_path.read_text(encoding='utf-8')}"
        else:
            print(f"Error: The file does not exist: {input_path}")
            return 1

    try:
        asyncio.run(run_agent(user_input))
        return 0
    except Exception as e:
        print(f"Failed to run: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
