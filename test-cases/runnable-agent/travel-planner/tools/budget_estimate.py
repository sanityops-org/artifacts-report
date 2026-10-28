#!/usr/bin/env python3
"""
budget_estimate: Estimate trip budget for a destination.
"""

import sys
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.destination_engine import DestinationEngine
from apis.budget_calculator import BudgetCalculator
from models.enums import BudgetLevel

parameters = {
    "type": "object",
    "properties": {
        "destination_id": {
            "type": "string",
            "pattern": "^DEST\\d{3}$",
            "description": "Destination ID (e.g., DEST001)"
        },
        "duration_days": {
            "type": "integer",
            "description": "Trip duration in days"
        },
        "budget_level": {
            "type": "string",
            "description": "Budget level (budget, moderate, luxury)"
        },
        "travelers_count": {
            "type": "integer",
            "description": "Number of travelers (default: 1)"
        }
    },
    "required": ["destination_id", "duration_days"]
}


def execute(params: dict[str, Any]) -> dict[str, Any]:
    """
    Estimate trip budget.

    Args:
        params:
            - destination_id: Destination ID (required)
            - duration_days: Trip duration (required)
            - budget_level: Budget level (optional, default: moderate)
            - travelers_count: Number of travelers (optional, default: 1)

    Returns:
        {"status": "success", "data": {...budget estimate...}} or
        {"status": "error", "error": "..."}
    """
    destination_id = params.get("destination_id")
    duration_days = params.get("duration_days")

    if not destination_id:
        return {"status": "error", "error": "Missing required parameter: destination_id"}
    if not duration_days:
        return {"status": "error", "error": "Missing required parameter: duration_days"}

    try:
        store = get_data_store(str(project_root / "data"))
        destinations = store.load_destinations()
        attractions = store.load_attractions()

        engine = DestinationEngine(destinations, attractions)
        destination = engine.get_destination(destination_id)

        if not destination:
            return {"status": "error", "error": f"Destination {destination_id} not found"}

        try:
            level_enum = BudgetLevel(params.get("budget_level", "moderate").lower())
        except ValueError:
            level_enum = BudgetLevel.MODERATE

        calculator = BudgetCalculator()
        estimate = calculator.estimate_budget(
            destination=destination,
            duration_days=duration_days,
            budget_level=level_enum,
            travelers_count=params.get("travelers_count", 1)
        )

        return {
            "status": "success",
            "data": {
                "destination": destination.name,
                "duration_days": duration_days,
                "budget_level": params.get("budget_level", "moderate"),
                "travelers_count": params.get("travelers_count", 1),
                "estimate": estimate
            }
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to estimate budget: {str(e)}"}
