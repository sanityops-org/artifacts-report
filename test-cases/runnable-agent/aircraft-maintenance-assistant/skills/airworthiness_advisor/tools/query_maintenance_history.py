#!/usr/bin/env python3
"""
Resume query tool

Query aircraft history, residual defects, and historical AD execution records.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional, List

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db
from data.helpers import assess_defect_impact


class QueryMaintenanceHistoryTool(Tool):
    """Resume query tool"""

    name = "query_maintenance_history"
    description = "Query aircraft history, legacy defects, and historical AD execution records"
    parameters = {
        "type": "object",
        "properties": {
            "reg_no": {
                "type": "string",
                "description": "Aircraft registration number, such as B-1234",
                "minLength": 2,
                "maxLength": 10,
                "pattern": "^[A-Z]-[0-9A-Z]+$",
            },
            "part_no": {
                "type": "string",
                "description": "The part number is optional. If it is provided, the installation history of the part will be returned.",
                "minLength": 3,
                "maxLength": 30,
                "pattern": "^[A-Z]{2,4}-[0-9A-Z]+$",
            },
        },
        "required": ["reg_no"],
        "additionalProperties": False,
    }
    tags = ["history", "defects", "records"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(
        self,
        reg_no: str,
        part_no: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """Execution of resume inquiry"""
        aircraft = sim_db.AIRCRAFT_RECORDS.get(reg_no)
        if not aircraft:
            return ToolResult(
                content=f"Query failure: the plane {reg_no} does not exist",
                success=False,
                error=f"The plane {reg_no} does not exist"
            )

        result_data = {
            "reg_no": reg_no,
            "model": aircraft.get("model"),
            "total_hours": aircraft.get("total_hours"),
            "total_cycles": aircraft.get("total_cycles"),
        }

        # Check the history of parts
        if part_no:
            installed = aircraft["components"].get(part_no)
            if not installed:
                return ToolResult(
                    success=True,
                    content=f"Parts {part_no} are not installed on the aircraft {reg_no}",
                    metadata={**result_data, "component_history": None}
                )
            result_data["component_history"] = {
                "part_no": part_no,
                **installed,
            }

        # Dealing with residual defects
        open_defects = aircraft.get("open_defects", [])
        assessed_defects = []
        for defect in open_defects:
            impact = assess_defect_impact(defect)
            assessed_defects.append({
                **defect,
                "impact": impact["impact"],
                "airworthy": impact["airworthy"],
                "mel_controlled": impact.get("mel_controlled", False),
            })
        result_data["open_defects"] = assessed_defects

        # AD Execution record
        result_data["ad_compliance_records"] = aircraft.get("ad_compliance", {})

        return ToolResult(
            success=True,
            content=f"Aircraft {reg_no} resume inquiry completed",
            metadata=result_data
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = QueryMaintenanceHistoryTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({"reg_no": "B-1234"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
