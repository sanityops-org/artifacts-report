#!/usr/bin/env python3
"""
Parts status query tool

Query the attribution of parts (life part/time control), remaining life, and early warning level.
"""

import sys
from pathlib import Path
from typing import Any, Dict

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db
from data.helpers import calc_remaining_life, check_time_control_limit


class QueryComponentStatusTool(Tool):
    """Parts status query tool"""

    name = "query_component_status"
    description = "Query the status of parts, including the remaining hours of the life part/time control - cycle, early warning level"
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
                "description": "Part number, such as PN-12345",
                "minLength": 3,
                "maxLength": 30,
                "pattern": "^[A-Z]{2,4}-[0-9A-Z]+$",
            },
        },
        "required": ["reg_no", "part_no"],
        "additionalProperties": False,
    }
    tags = ["component", "life-limited", "time-controlled", "status"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, reg_no: str, part_no: str, **kwargs) -> ToolResult:
        """Perform part status query"""
        # Verify the existence of the aircraft
        aircraft = sim_db.AIRCRAFT_RECORDS.get(reg_no)
        if not aircraft:
            return ToolResult(
                content=f"Query failure: the plane {reg_no} does not exist",
                success=False,
                error=f"The plane {reg_no} does not exist"
            )

        # Verify the existence of parts
        component = sim_db.COMPONENTS.get(part_no)
        if not component:
            return ToolResult(
                content=f"Query failure: component {part_no} does not exist",
                success=False,
                error=f"The component {part_no} does not exist"
            )

        # Verify that the parts have been installed
        installed = aircraft["components"].get(part_no)
        if not installed:
            return ToolResult(
                content=f"Query failure: aircraft {reg_no} uninstalled parts {part_no}",
                success=False,
                error=f"Component {part_no} is not installed on aircraft {reg_no}"
            )

        category = component.get("category")
        result_data = {
            "part_no": part_no,
            "name": component.get("name"),
            "category": category,
            "install_date": installed.get("install_date"),
            "last_check_date": installed.get("last_check_date"),
        }

        # Calculate the status according to the category
        if category == "life_limited":
            life_result = calc_remaining_life(
                component,
                installed.get("hours_since_install", 0),
                installed.get("cycles_since_install", 0)
            )
            result_data.update({
                "remaining_hours": life_result["remaining_hours"],
                "remaining_cycles": life_result["remaining_cycles"],
                "alert_level": life_result["alert_level"],
                "remaining_ratio": life_result["remaining_ratio"],
            })

        elif category == "time_controlled":
            tci_ref = component.get("tci_reference")
            tci = sim_db.TIME_CONTROLLED_ITEMS.get(tci_ref)
            if tci:
                limit_type = tci.get("limit_type")
                if limit_type == "hours":
                    current = installed.get("hours_since_install", 0)
                elif limit_type == "cycles":
                    current = installed.get("cycles_since_install", 0)
                else:
                    # TODO: calendar The type-time control is currently processed as 0, and the remaining life needs to be calculated according to install_date and the current date.
                    # There is no calendar type in the current simulation data, which is delayed as a known limit.
                    current = 0

                tci_result = check_time_control_limit(tci, current)
                result_data.update({
                    "tci_status": tci_result["status"],
                    "tci_remaining": tci_result["remaining"],
                    "tci_limit": tci_result["limit_value"],
                    "tci_ratio": tci_result["ratio"],
                    "alert_level": "warning" if tci_result["status"] == "warning" else (
                        "exceeded" if tci_result["status"] == "exceeded" else "ok"
                    ),
                })

        else:  # on_condition
            result_data["alert_level"] = "ok"

        return ToolResult(
            success=True,
            content=f"Part {part_no} status: {result_data['alert_level']}",
            metadata=result_data
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = QueryComponentStatusTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({"reg_no": "B-1234", "part_no": "PN-12345"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
