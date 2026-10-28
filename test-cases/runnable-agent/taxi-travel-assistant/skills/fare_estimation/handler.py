#!/usr/bin/env python3
"""Cost estimation skill processing script"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from skills.fare_estimation.tools.estimate_fare import EstimateFareTool


class FareEstimationHandler:
    """Cost estimation processor"""

    def __init__(self):
        self.estimate_fare_tool = EstimateFareTool()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Estimated execution cost"""
        origin = params.get("origin")
        destination = params.get("destination")
        category = params.get("category")
        time_of_day = params.get("time_of_day", "day")

        if not origin:
            return {
                "status": "error",
                "error": "The starting point is not provided.",
                "message": "Please provide the starting point."
            }

        if not destination:
            return {
                "status": "error",
                "error": "The end point is not provided.",
                "message": "Please provide the destination location."
            }

        result = await self.estimate_fare_tool.execute(
            origin=origin,
            destination=destination,
            category=category,
            time_of_day=time_of_day
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


_handler = FareEstimationHandler()


async def main(params: Dict[str, Any]) -> Dict[str, Any]:
    return await _handler.execute(params)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronized entrance function"""
    return asyncio.run(main(params))


if __name__ == "__main__":
    import json
    result = run({"origin": "L-001", "destination": "L-002"})
    print(json.dumps(result, indent=2, ensure_ascii=False))
