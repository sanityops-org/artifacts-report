#!/usr/bin/env python3
"""Vehicle query skill processing script"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from skills.vehicle_query.tools.query_vehicle import QueryVehicleTool


class VehicleQueryHandler:
    """Vehicle query processor"""

    def __init__(self):
        self.query_vehicle_tool = QueryVehicleTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute vehicle inquiry"""
        location = params.get("location")
        category = params.get("category")
        radius_km = params.get("radius_km", 5.0)

        if not location:
            return {
                "status": "error",
                "error": "No location provided",
                "message": "Please provide the location information."
            }

        result = await self.query_vehicle_tool.execute(
            location=location,
            category=category,
            radius_km=radius_km
        )

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


_handler = VehicleQueryHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronized entrance function"""
    return asyncio.run(main(params))


if __name__ == "__main__":
    import json
    result = run({"location": "L-001"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
