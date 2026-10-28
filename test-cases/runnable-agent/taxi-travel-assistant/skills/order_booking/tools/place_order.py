#!/usr/bin/env python3
"""
Ordering tools

Create an order and send a car.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

from sanityops_agent import Tool, ToolContext, ToolResult

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

from data import sim_db, find_nearby_vehicles, calc_route, calc_fare


class PlaceOrderTool(Tool):
    """Ordering tools"""

    name = "place_order"
    description = "Create taxi orders and automatically match nearby vehicles"
    parameters = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "Consumer ID",
                "minLength": 1,
                "maxLength": 50,
            },
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
            "phone": {
                "type": "string",
                "description": "Contact number",
                "minLength": 1,
                "maxLength": 20,
            },
            "category": {
                "type": "string",
                "description": "Model preference (economic | comfort | premium | suv)",
                "enum": ["economic", "comfort", "premium", "suv"],
            },
        },
        "required": ["user_id", "origin", "destination", "phone"],
        "additionalProperties": False,
    }
    tags = ["order", "booking", "place", "create"]

    def __init__(self, context: ToolContext | None = None):
        super().__init__(context)

    async def execute(
        self,
        user_id: str,
        origin: str,
        destination: str,
        phone: str,
        category: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """Execute the order"""
        # Verify the existence of the starting and ending points
        if origin not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Order failure: the starting point {origin} does not exist",
                success=False,
                error=f"The starting point {origin} does not exist"
            )

        if destination not in sim_db.LOCATIONS:
            return ToolResult(
                content=f"Order failure: the end point {destination} does not exist",
                success=False,
                error=f"The end position {destination} does not exist"
            )

        # Find available vehicles nearby
        vehicles = find_nearby_vehicles(origin, category, radius_km=5.0)

        if not vehicles:
            category_text = f"{category} " if category else ""
            return ToolResult(
                content=f"Order failure: There are no available {category_text} vehicles nearby",
                success=False,
                error="No vehicles available"
            )

        # Choose the nearest vehicle
        selected_vehicle = vehicles[0]
        vehicle_id = selected_vehicle["vehicle_id"]

        # Get the route and the cost
        route = calc_route(origin, destination)
        fare = calc_fare(route["distance_km"], route["duration_min"], selected_vehicle["category"])

        # Create an order
        order_id = sim_db.generate_order_id()
        order = {
            "order_id": order_id,
            "user_id": user_id,
            "vehicle_id": vehicle_id,
            "origin": origin,
            "origin_name": sim_db.LOCATIONS[origin]["name"],
            "destination": destination,
            "destination_name": sim_db.LOCATIONS[destination]["name"],
            "phone": phone,
            "status": "pending",
            "fare": fare["total"],
            "distance_km": route["distance_km"],
            "duration_min": route["duration_min"],
            "created_at": "2026-09-04 10:00:00",  # Simulation time
        }
        sim_db.ORDERS[order_id] = order

        # Update the status of the vehicle
        sim_db.VEHICLES[vehicle_id]["status"] = "busy"

        origin_name = sim_db.LOCATIONS[origin]["name"]
        dest_name = sim_db.LOCATIONS[destination]["name"]

        return ToolResult(
            success=True,
            content=f"The order is successful! Order number {order_id}, {selected_vehicle['driver_name']} ({selected_vehicle['model']}) is expected to arrive in {selected_vehicle['eta_min']} minutes",
            metadata={
                "order_id": order_id,
                "vehicle_id": vehicle_id,
                "vehicle": {
                    "plate_no": selected_vehicle["plate_no"],
                    "model": selected_vehicle["model"],
                    "category": selected_vehicle["category"],
                    "driver_name": selected_vehicle["driver_name"],
                    "driver_phone": sim_db.VEHICLES[vehicle_id]["driver_phone"],
                    "rating": selected_vehicle["rating"],
                    "eta_min": selected_vehicle["eta_min"],
                },
                "origin_name": origin_name,
                "destination_name": dest_name,
                "fare": fare["total"],
                "distance_km": route["distance_km"],
                "duration_min": route["duration_min"],
            }
        )


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous execution entrance"""
    import asyncio
    tool = PlaceOrderTool()
    result = asyncio.run(tool.execute(**params))
    return {
        "status": "success" if result.success else "error",
        "data": result.metadata if result.success else None,
        "error": result.error if not result.success else None,
    }


if __name__ == "__main__":
    import json
    result = execute({
        "user_id": "U-123",
        "origin": "L-001",
        "destination": "L-002",
        "phone": "138****1234"
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
