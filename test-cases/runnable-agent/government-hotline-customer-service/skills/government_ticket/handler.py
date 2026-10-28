#!/usr/bin/env python3
"""
Government hotline work order skill processor

Handle the creation and inquiry business of complaints/suggestions/consultation work orders.
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from skills.government_ticket.tools.dispatch_engine import DispatchEngineTool
from skills.government_ticket.tools.ticket_store import TicketStoreTool


class GovernmentTicketHandler:
    """Government hotline work order processor"""

    def __init__(self):
        self.dispatch_tool = DispatchEngineTool()
        self.store_tool = TicketStoreTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill requests"""
        action = params.get("action")

        action_map = {
            "create_ticket": self._create_ticket,
            "query_ticket": self._query_ticket,
            "query_ticket_list": self._query_ticket_list
        }

        if action not in action_map:
            return {
                "status": "error",
                "error": f"Unknown operation type: {action}",
                "message": f"Supported operations: {list(action_map.keys())}"
            }

        return await action_map[action](params)

    async def _create_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a work order"""
        ticket_type = params.get("ticket_type")
        content = params.get("content")
        reporter_name = params.get("reporter_name")
        reporter_phone = params.get("reporter_phone")

        if not ticket_type:
            return {"status": "error", "error": "Missing parameters: ticket_type"}

        if not content:
            return {"status": "error", "error": "Missing parameters: content"}

        # 1. Call the dispatch engine
        dispatch_result = await self.dispatch_tool.execute(
            content=content,
            ticket_type=ticket_type
        )

        if not dispatch_result.success:
            return {
                "status": "error",
                "error": "The execution of the dispatch engine failed",
                "details": dispatch_result.error
            }

        dispatch_data = dispatch_result.metadata

        # 2. Create a work order
        store_result = await self.store_tool.execute(
            action="create",
            ticket_type=ticket_type,
            content=content,
            dept_id=dispatch_data["dept_id"],
            dept_name=dispatch_data["dept_name"],
            urgency_level=dispatch_data["urgency_level"],
            reporter_name=reporter_name,
            reporter_phone=reporter_phone
        )

        if not store_result.success:
            return {
                "status": "error",
                "error": "Failed to create a work order",
                "details": store_result.error
            }

        ticket_data = store_result.metadata

        # 3. Return to the receipt
        return {
            "status": "success",
            "message": "The work order was created successfully.",
            "data": {
                "ticket_id": ticket_data["ticket_id"],
                "ticket_type": ticket_data["ticket_type"],
                "status": ticket_data["status"],
                "dept_id": ticket_data["dept_id"],
                "dept_name": ticket_data["dept_name"],
                "urgency_level": ticket_data["urgency_level"],
                "deadline": dispatch_data["deadline"],
                "is_anonymous": ticket_data["is_anonymous"],
                "created_at": ticket_data["created_at"],
                "is_auto_dispatch": dispatch_data["is_auto"],
                "confidence": dispatch_data["confidence"]
            }
        }

    async def _query_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Query a single work order"""
        ticket_id = params.get("ticket_id")

        if not ticket_id:
            return {"status": "error", "error": "Missing parameters: ticket_id"}

        result = await self.store_tool.execute(action="get_by_id", ticket_id=ticket_id)

        if not result.success:
            return {"status": "error", "error": result.error}

        return {
            "status": "success",
            "message": "The query is successful",
            "data": result.metadata
        }

    async def _query_ticket_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Query the list of work orders"""
        phone = params.get("phone")

        if not phone:
            return {"status": "error", "error": "Missing parameters: phone"}

        result = await self.store_tool.execute(action="get_by_phone", phone=phone)

        if not result.success:
            return {"status": "error", "error": result.error}

        return {
            "status": "success",
            "message": f"Query {result.metadata['total']} work orders",
            "data": result.metadata
        }


# Global processor instance
_handler = GovernmentTicketHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    """Skill main entrance (asynchronous)"""
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronized entrance function"""
    return asyncio.run(main(params))


if __name__ == "__main__":
    import json

    result = run({
        "action": "create_ticket",
        "ticket_type": "complaint",
        "content": "Construction noise at night disturbs people",
        "reporter_phone": "13800138000"
    })

    print(json.dumps(result, indent=2, ensure_ascii=False))
