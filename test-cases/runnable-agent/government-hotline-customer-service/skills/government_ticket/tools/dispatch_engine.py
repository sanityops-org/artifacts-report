#!/usr/bin/env python3
"""
Intelligent distribution engine

According to the content of the work order, it automatically matches the undertaking department and determines the urgency.
"""

import sys
from pathlib import Path
from typing import Any, Dict

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data.helpers import match_department, classify_urgency, calculate_deadline
from data.sim_db import URGENCY_DEADLINE


class DispatchEngineTool(Tool):
    """Intelligent distribution engine tool"""

    name = "dispatch_engine"
    description = "The intelligent dispatch engine automatically matches the undertaking department according to the content of the work order and determines the degree of urgency."
    parameters = {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Work order content"
            },
            "ticket_type": {
                "type": "string",
                "description": "Work order type",
                "enum": ["complaint", "suggestion", "consultation"]
            }
        },
        "required": ["content", "ticket_type"]
    }
    tags = ["dispatch", "routing", "urgency"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, **kwargs) -> ToolResult:
        """Execute the distribution"""
        content = kwargs.get("content", "")
        ticket_type = kwargs.get("ticket_type", "complaint")

        if not content:
            return ToolResult(
                content="",
                success=False,
                error="Missing parameters: content"
            )

        # 1. Matching department
        dept_result = match_department(content)

        # 2. Determine the degree of urgency
        urgency_result = classify_urgency(content)

        # 3. The default ordinary level of the consulting class
        if ticket_type == "consultation":
            urgency_result["level"] = "normal"
            urgency_result["matched_keywords"] = []
            urgency_result["deadline_hours"] = URGENCY_DEADLINE["normal"]

        # 4. Calculate the deadline
        deadline = calculate_deadline(urgency_result["level"])

        result = {
            "dept_id": dept_result["dept_id"],
            "dept_name": dept_result["dept_name"],
            "dept_contact": dept_result.get("dept_contact"),
            "is_auto": dept_result["is_auto"],
            "confidence": dept_result["confidence"],
            "matched_keyword": dept_result.get("matched_keyword"),
            "urgency_level": urgency_result["level"],
            "urgency_keywords": urgency_result["matched_keywords"],
            "deadline_hours": urgency_result["deadline_hours"],
            "deadline": deadline
        }

        return ToolResult(
            success=True,
            content=f"Assemnt: {dept_result['dept_name']} ({urgency_result['level']})",
            metadata=result
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = DispatchEngineTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None
    }


if __name__ == "__main__":
    import json
    result = execute({
        "content": "The noise of construction at night seriously disturbs people.",
        "ticket_type": "complaint"
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
