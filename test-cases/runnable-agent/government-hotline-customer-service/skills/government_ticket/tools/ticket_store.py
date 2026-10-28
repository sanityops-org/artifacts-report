#!/usr/bin/env python3
"""
Work order storage tool

Provide the functions of creating, querying and updating work orders.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data.sim_db import TICKETS
from data.helpers import generate_ticket_id, validate_phone


class TicketStoreTool(Tool):
    """Work order storage tool"""

    name = "ticket_store"
    description = "Work order storage management, support the creation and query of work orders"
    parameters = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Operation type",
                "enum": ["create", "get_by_id", "get_by_phone", "list"]
            },
            "ticket_id": {
                "type": "string",
                "description": "Work order number, required when querying/updating"
            },
            "ticket_type": {
                "type": "string",
                "description": "Work order type",
                "enum": ["complaint", "suggestion", "consultation"]
            },
            "content": {
                "type": "string",
                "description": "Work order content"
            },
            "dept_id": {
                "type": "string",
                "description": "Undertaking department ID"
            },
            "dept_name": {
                "type": "string",
                "description": "Name of the undertaking department"
            },
            "urgency_level": {
                "type": "string",
                "description": "The degree of urgency",
                "enum": ["critical", "urgent", "normal"]
            },
            "reporter_name": {
                "type": "string",
                "description": "The name of the complainant (anonymous can be blank)"
            },
            "reporter_phone": {
                "type": "string",
                "description": "The complainant's mobile phone number"
            },
            "phone": {
                "type": "string",
                "description": "The mobile phone number when querying by mobile phone number"
            }
        },
        "required": ["action"]
    }
    tags = ["ticket", "storage", "crud"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, **kwargs) -> ToolResult:
        """Perform work order operations"""
        action = kwargs.get("action")

        action_map = {
            "create": self._create_ticket,
            "get_by_id": self._get_by_id,
            "get_by_phone": self._get_by_phone,
            "update_status": self._update_status,
            "list": self._list_tickets
        }

        if action not in action_map:
            return ToolResult(
                content="",
                success=False,
                error=f"Unknown operation type: {action}"
            )

        return await action_map[action](**kwargs)

    async def _create_ticket(self, **kwargs) -> ToolResult:
        """Create a work order"""
        ticket_type = kwargs.get("ticket_type")
        content = kwargs.get("content")
        dept_id = kwargs.get("dept_id", "default")
        dept_name = kwargs.get("dept_name", "Comprehensive Coordination Office")
        urgency_level = kwargs.get("urgency_level", "normal")
        reporter_name = kwargs.get("reporter_name")
        reporter_phone = kwargs.get("reporter_phone")

        if not ticket_type or not content:
            return ToolResult(
                content="",
                success=False,
                error="Required parameters are missing: ticket_type or content"
            )

        # Verify the mobile phone number (if provided)
        if reporter_phone and not validate_phone(reporter_phone):
            return ToolResult(
                content="",
                success=False,
                error="The format of the mobile phone number is incorrect."
            )

        ticket_id = generate_ticket_id()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ticket = {
            "ticket_id": ticket_id,
            "ticket_type": ticket_type,
            "content": content,
            "dept_id": dept_id,
            "dept_name": dept_name,
            "urgency_level": urgency_level,
            "status": "pending",
            "reporter_name": reporter_name,
            "reporter_phone": reporter_phone,
            "created_at": now,
            "updated_at": now,
            "is_anonymous": reporter_phone is None
        }

        TICKETS[ticket_id] = ticket

        return ToolResult(
            success=True,
            content=f"The work order has been created successfully, the work order number: {ticket_id}",
            metadata=ticket
        )

    async def _get_by_id(self, **kwargs) -> ToolResult:
        """Query the work order by ID"""
        ticket_id = kwargs.get("ticket_id")

        if not ticket_id:
            return ToolResult(
                content="",
                success=False,
                error="Missing parameters: ticket_id"
            )

        ticket = TICKETS.get(ticket_id)

        if not ticket:
            return ToolResult(
                content="",
                success=False,
                error=f"The work order does not exist.: {ticket_id}"
            )

        return ToolResult(
            success=True,
            content=f"Inquire about the work order: {ticket_id}",
            metadata=ticket
        )

    async def _get_by_phone(self, **kwargs) -> ToolResult:
        """Check the list of work orders by mobile phone number"""
        phone = kwargs.get("phone")

        if not phone:
            return ToolResult(
                content="",
                success=False,
                error="Missing parameters: phone"
            )

        tickets = [
            ticket for ticket in TICKETS.values()
            if ticket.get("reporter_phone") == phone
        ]

        # In reverse order of creation time
        tickets.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        return ToolResult(
            success=True,
            content=f"Query {len(tickets)} work orders",
            metadata={"tickets": tickets, "total": len(tickets)}
        )

    async def _update_status(self, **kwargs) -> ToolResult:
        """Update the status of the work order"""
        ticket_id = kwargs.get("ticket_id")
        new_status = kwargs.get("new_status")

        if not ticket_id or not new_status:
            return ToolResult(
                content="",
                success=False,
                error="Missing parameters: ticket_id or new_status"
            )

        ticket = TICKETS.get(ticket_id)

        if not ticket:
            return ToolResult(
                content="",
                success=False,
                error=f"The work order does not exist.: {ticket_id}"
            )

        old_status = ticket["status"]
        ticket["status"] = new_status
        ticket["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return ToolResult(
            success=True,
            content=f"The status of the work order has been updated.: {old_status} -> {new_status}",
            metadata=ticket
        )

    async def _list_tickets(self, **kwargs) -> ToolResult:
        """List all work orders"""
        tickets = list(TICKETS.values())
        tickets.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        return ToolResult(
            success=True,
            content=f"A total of {len(tickets)} work orders",
            metadata={"tickets": tickets, "total": len(tickets)}
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = TicketStoreTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None
    }


if __name__ == "__main__":
    import json
    result = execute({
        "action": "create",
        "ticket_type": "complaint",
        "content": "Test work order",
        "dept_id": "eco_env",
        "dept_name": "Ecology and Environment Bureau",
        "urgency_level": "normal"
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
