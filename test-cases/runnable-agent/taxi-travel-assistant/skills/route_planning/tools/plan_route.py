#!/usr/bin/env python3
"""
Route planning tools

Query the best travel route and return the distance, duration and toe.
"""

import sys
from pathlib import Path
from typing import Any, Dict

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db, calc_route


class PlanRouteTool(Tool):
    """Route planning tools"""

    name = "plan_route"
    description = "Query the best travel route, return the distance, duration, tot fee"
    parameters = {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "Starting point location ID, such as L-001 (Beijing West Railway Station)",
                "minLength": 1,
                "maxLength": 20,
            },
            "destination": {
                "type": "string",
                "description": "End point ID, such as L-002 (Capital AirportT3）",
                "minLength": 1,
                "maxLength": 20,
            },
        },
        "required": ["origin", "destination"],
        "additionalProperties": False,
    }
    tags = ["route", "navigation", "distance"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(self, origin: str, destination: str, **kwargs) -> ToolResult:
        """Implement route planning"""
        # Verify the existence of the starting point
        if origin not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Query failure: the starting point {origin} does not exist",
                success=False,
                error=f"The starting point {origin} does not exist. Please check the location. ID"
            )

        # Verify the existence of the end point
        if destination not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Query failure: the end point {destination} does not exist",
                success=False,
                error=f"The end position {destination} does not exist, please check the location. ID"
            )

        # Calculate the route
        route = calc_route(origin, destination)

        if route is None:
            return ToolResult(
                content="Query failure: the route cannot be calculated",
                success=False,
                error="The route cannot be calculated. Please check the starting and ending positions."
            )

        origin_name = sim_db.LOCATIONS[origin]["name"]
        dest_name = sim_db.LOCATIONS[destination]["name"]

        return ToolResult(
            success=True,
            content=f"From {origin_name} to {dest_name}: distance {route['distance_km']} kilometers, estimated {route['duration_min']} minutes",
            metadata={
                "origin": origin,
                "origin_name": origin_name,
                "destination": destination,
                "destination_name": dest_name,
                "distance_km": route["distance_km"],
                "duration_min": route["duration_min"],
                "toll": route["toll"],
                "waypoints": route["waypoints"],
            }
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = PlanRouteTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({"origin": "L-001", "destination": "L-002"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
