#!/usr/bin/env python3
"""
Order cancellation tool

Cancel unstarted orders.
"""

import sys
from pathlib import Path
from typing import Any, Dict

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db


class CancelOrderTool(Tool):
    """Order cancellation tool"""

    name = "cancel_order"
    description = "Cancel the taxi order"
    parameters = {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "Order number",
                "minLength": 1,
                "maxLength": 20,
            },
            "reason": {
                "type": "string",
                "description": "Reason for cancellation (optional)",
                "maxLength": 200,
            },
        },
        "required": ["order_id"],
        "additionalProperties": False,
    }
    tags = ["order", "cancel"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, order_id: str, reason: str = "", **kwargs) -> ToolResult:
        """Execute and cancel the order"""
        # Check whether the order exists
        if order_id not in sim_db.ORDERS:
            return ToolResult(
                content=f"Cancellation failed: Order {order_id} does not exist",
                success=False,
                error=f"The order {order_id} does not exist"
            )

        order = sim_db.ORDERS[order_id]

        # Check the order status
        if order["status"] == "cancelled":
            return ToolResult(
                content="Cancellation failed: the order has been canceled",
                success=False,
                error="The order has been cancelled."
            )

        if order["status"] == "completed":
            return ToolResult(
                content="Cancellation failure: The order has been completed and cannot be canceled.",
                success=False,
                error="The order has been completed and cannot be canceled."
            )

        # Update the order status
        order["status"] = "cancelled"
        order["cancel_reason"] = reason

        # Release the vehicle
        vehicle_id = order.get("vehicle_id")
        if vehicle_id and vehicle_id in sim_db.VEHICLES:
            sim_db.VEHICLES[vehicle_id]["status"] = "idle"

        # Calculate refund (simulation: full refund without departure)
        refund_amount = order["fare"]

        return ToolResult(
            success=True,
            content=f"Order {order_id} has been canceled, refund {refund_amount} yuan",
            metadata={
                "order_id": order_id,
                "status": "cancelled",
                "refund_amount": refund_amount,
            }
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = CancelOrderTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({"order_id": "O-000001"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
