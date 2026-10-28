#!/usr/bin/env python3
"""
Route planning skill processing script
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from skills.route_planning.tools.plan_route import PlanRouteTool


class RoutePlanningHandler:
    """Route planning processor"""

    def __init__(self):
        self.plan_route_tool = PlanRouteTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Implement route planning"""
        origin = params.get("origin")
        destination = params.get("destination")

        if not origin:
            return {
                "status": "error",
                "error": "The starting point is not provided.",
                "message": "Please provide the starting point (origin parameter)"
            }

        if not destination:
            return {
                "status": "error",
                "error": "The end point is not provided.",
                "message": "Please provide the destination location (destination parameters)"
            }

        result = await self.plan_route_tool.execute(origin=origin, destination=destination)

        if not result.success:
            return {
                "status": "error",
                "error": result.error,
                "message": result.content
            }

        return {
            "status": "success",
            "data": {
                "route": result.metadata
            },
            "message": f"Route query is successful:{result.content}"
        }


_handler = RoutePlanningHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronized entrance function"""
    return asyncio.run(main(params))


if __name__ == "__main__":
    import json
    result = run({"origin": "L-001", "destination": "L-002"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
