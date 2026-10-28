#!/usr/bin/env python3
"""
Cost estimation tool

Calculate the estimated taxi cost of a variety of models.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db, calc_route, calc_fare, FARE_RULES


class EstimateFareTool(Tool):
    """Cost estimation tool"""

    name = "estimate_fare"
    description = "Estimate the taxi cost and return the cost details of various models."
    parameters = {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "Starting point ID",
                "minLength": 1,
                "maxLength": 20,
            },
            "destination": {
                "type": "string",
                "description": "End point ID",
                "minLength": 1,
                "maxLength": 20,
            },
            "category": {
                "type": "string",
                "description": "Model category (economic | comfort | premium | suv), if not provided, all models will be returned",
                "enum": ["economic", "comfort", "premium", "suv"],
            },
            "time_of_day": {
                "type": "string",
                "description": "Time period (day | night), default day",
                "enum": ["day", "night"],
                "default": "day",
            },
        },
        "required": ["origin", "destination"],
        "additionalProperties": False,
    }
    tags = ["fare", "price", "cost", "estimation"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(
        self,
        origin: str,
        destination: str,
        category: Optional[str] = None,
        time_of_day: str = "day",
        **kwargs
    ) -> ToolResult:
        """Estimated execution cost"""
        # Verify the existence of the starting point
        if origin not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Query failure: the starting point {origin} does not exist",
                success=False,
                error=f"The starting point {origin} does not exist"
            )

        # Verify the existence of the end point
        if destination not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Query failure: the end point {destination} does not exist",
                success=False,
                error=f"The end position {destination} does not exist"
            )

        # Calculate the route
        route = calc_route(origin, destination)
        if route is None:
            return ToolResult(
                content="Query failure: the route cannot be calculated",
                success=False,
                error="Unable to calculate the route"
            )

        origin_name = sim_db.LOCATIONS[origin]["name"]
        dest_name = sim_db.LOCATIONS[destination]["name"]
        distance_km = route["distance_km"]
        duration_min = route["duration_min"]

        # If the model is specified, only the model is calculated.
        if category:
            if category not in FARE_RULES:
                return ToolResult(
                    content=f"Query failure: unknown model {category}",
                    success=False,
                    error=f"Unknown car model: {category}"
                )

            fare = calc_fare(distance_km, duration_min, category, time_of_day)

            return ToolResult(
                success=True,
                content=f"From {origin_name} to {dest_name} ({category}): estimated cost {fare['total']} yuan",
                metadata={
                    "origin": origin,
                    "origin_name": origin_name,
                    "destination": destination,
                    "destination_name": dest_name,
                    "category": category,
                    "distance_km": distance_km,
                    "duration_min": duration_min,
                    "time_of_day": time_of_day,
                    "fare": fare,
                }
            )

        # If the model is not specified, the cost of all models will be returned.
        all_fares = {}
        for cat in FARE_RULES.keys():
            all_fares[cat] = calc_fare(distance_km, duration_min, cat, time_of_day)

        return ToolResult(
            success=True,
            content=f"From {origin_name} to {dest_name}: economic {all_fares['economic']['total']} yuan, comfortable {all_fares['comfort']['total']} yuan",
            metadata={
                "origin": origin,
                "origin_name": origin_name,
                "destination": destination,
                "destination_name": dest_name,
                "distance_km": distance_km,
                "duration_min": duration_min,
                "time_of_day": time_of_day,
                "fares": all_fares,
            }
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = EstimateFareTool()
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
