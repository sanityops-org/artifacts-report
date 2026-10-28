#!/usr/bin/env python3
"""
Vehicle query tool

Check the available taxis nearby.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db, find_nearby_vehicles


class QueryVehicleTool(Tool):
    """Vehicle query tool"""

    name = "query_vehicle"
    description = "Check the available taxis nearby, return to the vehicle list and estimated arrival time."
    parameters = {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "Place ID",
                "minLength": 1,
                "maxLength": 20,
            },
            "category": {
                "type": "string",
                "description": "Model category filtering (economic | comfort | premium | suv)",
                "enum": ["economic", "comfort", "premium", "suv"],
            },
            "radius_km": {
                "type": "number",
                "description": "Search radius (kilometers)",
                "minimum": 0.1,
                "maximum": 50,
                "default": 5.0,
            },
        },
        "required": ["location"],
        "additionalProperties": False,
    }
    tags = ["vehicle", "taxi", "nearby", "available"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(
        self,
        location: str,
        category: Optional[str] = None,
        radius_km: float = 5.0,
        **kwargs
    ) -> ToolResult:
        """Execute vehicle inquiry"""
        # Verify the existence of the location
        if location not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Query failed: location {location} does not exist",
                success=False,
                error=f"Location {location} does not exist"
            )

        loc_name = sim_db.LOCATIONS[location]["name"]

        # Find nearby vehicles
        vehicles = find_nearby_vehicles(location, category, radius_km)

        if not vehicles:
            category_text = f"（{category}）" if category else ""
            return ToolResult(
                success=True,
                content=f"{loc_name} There are no available {category_text} vehicles within {radius_km} kilometers nearby.",
                metadata={
                    "location": location,
                    "location_name": loc_name,
                    "category": category,
                    "radius_km": radius_km,
                    "vehicles": [],
                    "count": 0,
                }
            )

        category_text = f"{category} " if category else ""
        returned_vehicles = vehicles[:10]  # Return up to 10 vehicles
        return ToolResult(
            success=True,
            content=f"{loc_name} Find {len(vehicles)} available {category_text} vehicles nearby",
            metadata={
                "location": location,
                "location_name": loc_name,
                "category": category,
                "radius_km": radius_km,
                "vehicles": returned_vehicles,
                "count": len(returned_vehicles),
            }
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = QueryVehicleTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({"location": "L-001"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
