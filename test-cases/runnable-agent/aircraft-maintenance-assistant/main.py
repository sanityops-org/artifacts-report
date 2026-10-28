#!/usr/bin/env python3
"""Aircraft Maintenance Airworthiness Assistant - command-line entry point.

Usage:
    python main.py B-1234
    python main.py B-1234 --part-no PN-12345
    python main.py B-1234 --ad-id AD-2024-01-001
    python main.py B-1234 --part-no PN-12345 --question "Should this aircraft be released?"

The runner loads the system prompt, registers the four airworthiness tools, sends
the structured request to the configured LLM provider, and prints the report.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(AGENT_DIR))

from sanityops_agent import (
    AgentConfig,
    AgentFactory,
    HookExecutor,
    ProviderConfig,
    ToolContext,
    ToolRegistry,
)
from sanityops_agent.llm.factory import ProviderFactory

from hooks.pretty_output_hook import PrettyOutputHook
from skills.airworthiness_advisor.tools.generate_decision import GenerateDecisionTool
from skills.airworthiness_advisor.tools.query_airworthiness import QueryAirworthinessTool
from skills.airworthiness_advisor.tools.query_component_status import QueryComponentStatusTool
from skills.airworthiness_advisor.tools.query_maintenance_history import QueryMaintenanceHistoryTool

AIRCRAFT_RE = re.compile(r"^[A-Z]-[0-9A-Z]+$")
PART_RE = re.compile(r"^[A-Z]{2,4}-[0-9A-Z]+$")
AD_RE = re.compile(r"^AD-[0-9]{4}-[0-9]{2}-[0-9]{3}$")


def load_system_prompt() -> str:
    """Load the agent system prompt."""
    prompt_path = AGENT_DIR / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a professional aircraft maintenance airworthiness assistant."


def create_tool_registry() -> ToolRegistry:
    """Create a registry containing the four airworthiness tools."""
    context = ToolContext()
    registry = ToolRegistry(context)
    registry.register(QueryAirworthinessTool(context))
    registry.register(QueryComponentStatusTool(context))
    registry.register(QueryMaintenanceHistoryTool(context))
    registry.register(GenerateDecisionTool(context))
    return registry


def build_request(reg_no: str, part_no: str | None, ad_id: str | None, question: str | None) -> str:
    """Build the review request sent to the agent."""
    lines = [
        f"Perform an airworthiness review for aircraft {reg_no}.",
        "Use the available read-only tools to retrieve the relevant AD/SB, component,",
        "and maintenance-history data. Do not infer missing data.",
    ]
    if ad_id:
        lines.append(f"Focus the AD/SB review on {ad_id}.")
    if part_no:
        lines.append(f"Focus the component-life and time-control review on {part_no}.")
    if question:
        lines.extend(["", "Additional request:", question.strip()])
    lines.extend([
        "",
        "Return the structured decision report required by the system prompt:",
        "airworthiness conclusion, required maintenance actions, recommended spare",
        "parts, ground-time impact, and decision rationale.",
    ])
    return "\n".join(lines)


def print_summary(result, elapsed: float, reg_no: str) -> None:
    """Print execution status."""
    print()
    print("=" * 60)
    print("Execution Summary")
    print("=" * 60)
    print(f"  Aircraft:       {reg_no}")
    print(f"  Iterations:     {result.loops_used}")
    print(f"  Execution time: {elapsed:.2f} seconds")
    if result.error:
        print(f"  Status:         FAILED - {result.error}")
    else:
        print("  Status:         SUCCESS")


def print_report(result) -> None:
    """Print the final airworthiness report."""
    if not result.text:
        return
    print()
    print("=" * 60)
    print("Airworthiness Decision Report")
    print("=" * 60)
    print()
    print(result.text)


def create_provider_config() -> ProviderConfig:
    """Load provider configuration from shared and agent-local .env files."""
    return ProviderConfig(_env_file=(AGENT_DIR / ".env", AGENT_DIR.parent / ".env"))


async def run_agent(
    reg_no: str,
    part_no: str | None = None,
    ad_id: str | None = None,
    question: str | None = None,
) -> int:
    """Run the airworthiness agent for one review request."""
    start_time = datetime.now()
    request = build_request(reg_no, part_no, ad_id, question)

    provider_config = create_provider_config()
    if not provider_config.API_KEY or provider_config.API_KEY == "your-api-key-here":
        print("API key is not configured.")
        print()
        print(f"Edit {AGENT_DIR / '.env'} and set:")
        print("  LLM_PROVIDER=anthropic")
        print("  LLM_API_KEY=your-api-key-here")
        print()
        print("Optional:")
        print("  LLM_BASE_URL=https://api.anthropic.com")
        print("  LLM_MODEL_ID=claude-sonnet-4-20250514")
        return 1

    provider = ProviderFactory.create(provider_config)
    registry = create_tool_registry()

    hook_executor = HookExecutor()
    hook_executor.register(PrettyOutputHook())

    factory = AgentFactory(
        provider=provider,
        config=AgentConfig(),
        tool_registry=registry,
        hook_executor=hook_executor,
    )
    agent = factory.create_parent_agent(system_prompt=load_system_prompt())

    print("Aircraft Maintenance Airworthiness Assistant")
    print(f"Aircraft: {reg_no}")
    if part_no:
        print(f"Component: {part_no}")
    if ad_id:
        print(f"AD/SB: {ad_id}")
    print(f"Model: {provider_config.MODEL_ID}")
    print(f"Provider: {provider_config.PROVIDER}")
    print("-" * 60)
    print("Starting review...")

    result = await agent.run(request)
    elapsed = (datetime.now() - start_time).total_seconds()
    print_summary(result, elapsed, reg_no)
    print_report(result)
    return 0 if not result.error else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Aircraft Maintenance Airworthiness Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py B-1234
  python main.py B-1234 --part-no PN-12345
  python main.py B-1234 --ad-id AD-2024-01-001
  python main.py B-1234 --part-no PN-12345 --question "Is this aircraft airworthy?"

Configuration:
  Edit .env and set LLM_PROVIDER and LLM_API_KEY.
        """,
    )
    parser.add_argument("reg_no", help="aircraft registration number, such as B-1234")
    parser.add_argument("--part-no", help="component part number, such as PN-12345")
    parser.add_argument("--ad-id", help="AD number, such as AD-2024-01-001")
    parser.add_argument("--question", "-q", help="optional additional question or instruction")
    args = parser.parse_args(argv)

    args.reg_no = args.reg_no.strip().upper()
    if args.part_no:
        args.part_no = args.part_no.strip().upper()
    if args.ad_id:
        args.ad_id = args.ad_id.strip().upper()

    if not AIRCRAFT_RE.fullmatch(args.reg_no):
        parser.error("reg_no must use the format B-1234")
    if args.part_no and not PART_RE.fullmatch(args.part_no):
        parser.error("--part-no must use a format such as PN-12345")
    if args.ad_id and not AD_RE.fullmatch(args.ad_id):
        parser.error("--ad-id must use the format AD-2024-01-001")
    return args


def main(argv: list[str] | None = None) -> int:
    """Run the CLI."""
    args = parse_args(argv)
    try:
        return asyncio.run(run_agent(args.reg_no, args.part_no, args.ad_id, args.question))
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 130
    except Exception as exc:
        print(f"\nAgent execution failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
