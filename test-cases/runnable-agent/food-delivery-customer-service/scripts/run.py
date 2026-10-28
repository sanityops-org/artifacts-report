#!/usr/bin/env python3
"""
Agent Start the script

Start the intelligent customer service Agent of the takeaway platform and run it using the sanityops_agent framework.
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
    Tool,
    ToolResult,
)
from sanityops_agent.llm.factory import ProviderFactory


# ============== Definition of tools ==============

class CreateOrderTool(Tool):
    """Create an order tool"""
    name = "create_order"
    description = "To create a takeaway order, a list of goods and a delivery address are required."
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "items": {
                "type": "array",
                "description": "List of goods",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "quantity": {"type": "integer"},
                        "price": {"type": "number"}
                    }
                }
            },
            "address": {"type": "string", "description": "Delivery address"},
            "remark": {"type": "string", "description": "Remarks (optional)"}
        },
        "required": ["user_id", "items", "address"]
    }

    async def execute(self, user_id: str, items: list, address: str, remark: str = None, **kwargs) -> ToolResult:
        from skills.order_management.handler import main
        result = main({
            "action": "create_order",
            "params": {"user_id": user_id, "items": items, "address": address, "remark": remark}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class QueryOrderTool(Tool):
    """Order inquiry tool"""
    name = "query_order"
    description = "Check the status and details of takeaway orders"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "order_id": {"type": "string", "description": "Order number"}
        },
        "required": ["user_id", "order_id"]
    }

    async def execute(self, user_id: str, order_id: str, **kwargs) -> ToolResult:
        from skills.order_management.handler import main
        result = main({
            "action": "query_order",
            "params": {"user_id": user_id, "order_id": order_id}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class RemindOrderTool(Tool):
    """Order reminder tool"""
    name = "remind_order"
    description = "Urge the merchant to process the order as soon as possible"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "order_id": {"type": "string", "description": "Order number"}
        },
        "required": ["user_id", "order_id"]
    }

    async def execute(self, user_id: str, order_id: str, **kwargs) -> ToolResult:
        from skills.order_management.handler import main
        result = main({
            "action": "remind_order",
            "params": {"user_id": user_id, "order_id": order_id}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class ModifyOrderTool(Tool):
    """Modify the order tool"""
    name = "modify_order"
    description = "Modify the delivery address or notes of the order"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "order_id": {"type": "string", "description": "Order number"},
            "address": {"type": "string", "description": "New delivery address (optional)"},
            "remark": {"type": "string", "description": "New remarks (optional)"}
        },
        "required": ["user_id", "order_id"]
    }

    async def execute(self, user_id: str, order_id: str, address: str = None, remark: str = None, **kwargs) -> ToolResult:
        from skills.order_management.handler import main
        result = main({
            "action": "modify_order",
            "params": {"user_id": user_id, "order_id": order_id, "address": address, "remark": remark}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class CancelOrderTool(Tool):
    """Order cancellation tool"""
    name = "cancel_order"
    description = "If you cancel the takeaway order, it will be judged whether it can be automatically refunded according to the order status."
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "order_id": {"type": "string", "description": "Order number"}
        },
        "required": ["user_id", "order_id"]
    }

    async def execute(self, user_id: str, order_id: str, **kwargs) -> ToolResult:
        from skills.order_management.handler import main
        result = main({
            "action": "cancel_order",
            "params": {"user_id": user_id, "order_id": order_id}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class ApplyRefundTool(Tool):
    """Apply for a refund tool"""
    name = "apply_refund"
    description = "Apply for an order refund, and automatically judge whether it can be refunded or need to be transferred according to the order status."
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "order_id": {"type": "string", "description": "Order number"},
            "amount": {"type": "number", "description": "Refund amount"},
            "reason": {"type": "string", "description": "Reason for refund"}
        },
        "required": ["user_id", "order_id", "amount", "reason"]
    }

    async def execute(self, user_id: str, order_id: str, amount: float, reason: str, **kwargs) -> ToolResult:
        from skills.after_sale.handler import main
        result = main({
            "action": "apply_refund",
            "params": {"user_id": user_id, "order_id": order_id, "amount": amount, "reason": reason}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class QueryRefundTool(Tool):
    """Inquire about refund tools"""
    name = "query_refund"
    description = "Check the progress of the refund"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "refund_id": {"type": "string", "description": "Refund order number"}
        },
        "required": ["user_id", "refund_id"]
    }

    async def execute(self, user_id: str, refund_id: str, **kwargs) -> ToolResult:
        from skills.after_sale.handler import main
        result = main({
            "action": "query_refund",
            "params": {"user_id": user_id, "refund_id": refund_id}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


class CreateTicketTool(Tool):
    """Create a work order tool"""
    name = "create_ticket"
    description = "Create manual customer service work orders to deal with disputes or complex after-sales problems"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "ConsumerID"},
            "order_id": {"type": "string", "description": "Order number"},
            "reason": {"type": "string", "description": "The reason for the work order"},
            "detail": {"type": "string", "description": "Detailed description"}
        },
        "required": ["user_id", "order_id", "reason", "detail"]
    }

    async def execute(self, user_id: str, order_id: str, reason: str, detail: str, **kwargs) -> ToolResult:
        from skills.after_sale.handler import main
        result = main({
            "action": "create_ticket",
            "params": {"user_id": user_id, "order_id": order_id, "reason": reason, "detail": detail}
        })
        return ToolResult(
            content=result.get("message", ""),
            success=result["status"] == "success",
            metadata=result
        )


# ============== Startup logic ==============

def load_system_prompt() -> str:
    """Load system prompts"""
    prompt_path = project_root / "prompts" / "system.txt"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are the intelligent customer service of the takeaway platform, helping customers deal with orders and refunds."


def create_tool_registry() -> ToolRegistry:
    """Create a tool registration form"""
    context = ToolContext()
    registry = ToolRegistry(context)

    # Order management tools
    registry.register(CreateOrderTool(context))
    registry.register(QueryOrderTool(context))
    registry.register(RemindOrderTool(context))
    registry.register(ModifyOrderTool(context))
    registry.register(CancelOrderTool(context))

    # After-sales service tools
    registry.register(ApplyRefundTool(context))
    registry.register(QueryRefundTool(context))
    registry.register(CreateTicketTool(context))

    return registry


def create_provider():
    """Set up LLM Provider"""
    config = ProviderConfig(_env_file=(project_root / ".env", project_root.parent / ".env"))

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

    print("Takeaway Platform Intelligent Customer Service Agent Launch")
    print(f"Model: {provider.model}")
    print("-" * 60)
    print("I can help you.:")
    print("  - Place an order, inquire about the order, urge the order, modify the order, cancel the order")
    print("  - Apply for a refund, check the progress of the refund, and transfer to manual customer service")
    print("-" * 60)

    if user_input:
        result = await agent.run(user_input)
        print("\n" + "=" * 60)
        if hasattr(result, 'text'):
            print(result.text)
        elif hasattr(result, 'content'):
            print(result.content)
        else:
            print(str(result))
        return result
    else:
        print("Please enter your needs (enter 'exit' to exit):")
        print("Example: I want to order a Gongbao chicken, check my order, and help me cancel the order.")
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

    parser = argparse.ArgumentParser(description="Intelligent customer service of takeaway platform Agent")
    parser.add_argument("--input", "-i", type=str, help="Enter the query content directly")
    args = parser.parse_args()

    try:
        asyncio.run(run_agent(args.input))
        return 0
    except Exception as e:
        print(f"Failed to run: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
