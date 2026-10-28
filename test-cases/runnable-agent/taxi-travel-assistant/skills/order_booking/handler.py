#!/usr/bin/env python3
"""Taxi ordering skill processing script"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from skills.order_booking.tools.place_order import PlaceOrderTool
from skills.order_booking.tools.cancel_order import CancelOrderTool


class OrderBookingHandler:
    """Taxi order processor"""

    def __init__(self):
        self.place_order_tool = PlaceOrderTool()
        self.cancel_order_tool = CancelOrderTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the order operation"""
        action = params.get("action")
        action_params = params.get("params", {})

        if action == "place_order":
            result = await self.place_order_tool.execute(**action_params)
        elif action == "cancel_order":
            result = await self.cancel_order_tool.execute(**action_params)
        else:
            return {
                "status": "error",
                "error": f"Unknown operation: {action}",
                "message": f"Unsupported operation types: {action}"
            }

        if not result.success:
            return {
                "status": "error",
                "error": result.error,
                "message": result.content
            }

        return {
            "status": "success",
            "data": result.metadata,
            "message": result.content
        }


_handler = OrderBookingHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronized entrance function"""
    return asyncio.run(main(params))


if __name__ == "__main__":
    import json
    result = run({
        "action": "place_order",
        "params": {
            "user_id": "U-123",
            "origin": "L-001",
            "destination": "L-002",
            "phone": "138****1234"
        }
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
