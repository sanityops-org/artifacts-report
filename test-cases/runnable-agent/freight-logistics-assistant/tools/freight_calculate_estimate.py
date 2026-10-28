#!/usr/bin/env python3
"""freight_calculate_estimate: Calculate freight cost estimate.

Use this tool when the user wants to know the estimated shipping cost for freight.
Requires origin, destination, and either weight_kg or volume_cbm. Returns detailed cost
breakdown including base rate, fuel surcharge, and accessorial charges (liftgate,
inside delivery). If carrier_id is omitted, the first available carrier is used and
the chosen carrier is echoed in the quote result.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.pricing_engine import calculate_quotation
from models.enums import ServiceLevel, CargoCategory

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "origin": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Origin city or facility name. Letters, digits, spaces, and common punctuation only; must start with a letter or digit. Required.",
        },
        "destination": {
            "type": "string",
            "minLength": 2,
            "maxLength": 100,
            "pattern": "^[A-Za-z0-9][A-Za-z0-9 \\-,.'()]*$",
            "description": "Destination city or facility name. Letters, digits, spaces, and common punctuation only; must start with a letter or digit. Required.",
        },
        "weight_kg": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 50000,
            "description": "Cargo weight in kilograms. Required if volume_cbm is not provided.",
        },
        "volume_cbm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 150,
            "description": "Cargo volume in cubic meters. Required if weight_kg is not provided.",
        },
        "cargo_type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20,
            "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
            "description": "Cargo category. Affects pricing surcharges. Optional.",
        },
        "service_level": {
            "type": "string",
            "minLength": 7,
            "maxLength": 8,
            "enum": ["economy", "standard", "express"],
            "default": "standard",
            "description": "Service level. Affects transit time and cost.",
        },
        "carrier_id": {
            "type": "string",
            "minLength": 4,
            "maxLength": 4,
            "pattern": "^C\\d{3}$",
            "description": "Specific carrier ID to use (format: C followed by 3 digits, e.g., C001). Optional. If omitted, the first available carrier in the database is used and the chosen carrier is echoed in the quote result.",
        },
    },
    "required": ["origin", "destination"],
    "anyOf": [
        {"required": ["weight_kg"]},
        {"required": ["volume_cbm"]},
    ],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate freight cost estimate.

    Args:
        params: {"origin": str, "destination": str, "weight_kg": float, ...}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    origin = params.get("origin")
    destination = params.get("destination")
    weight_kg = params.get("weight_kg", 1000)  # Default 1 ton if not specified

    if not origin or not destination:
        return {"status": "error", "error": "Missing required parameters: origin and destination"}

    try:
        data_store = DataStore(data_dir=project_root / "data")

        # Parse enums
        cargo_type = None
        if params.get("cargo_type"):
            cargo_type = CargoCategory(params["cargo_type"])

        service_level = ServiceLevel.STANDARD
        if params.get("service_level"):
            service_level = ServiceLevel(params["service_level"])

        quote = calculate_quotation(
            origin=origin,
            destination=destination,
            weight_kg=weight_kg,
            data_store=data_store,
            volume_cbm=params.get("volume_cbm"),
            cargo_type=cargo_type,
            service_level=service_level,
            carrier_id=params.get("carrier_id"),
        )

        if not quote:
            return {"status": "error", "error": "Could not calculate quotation. Route or carrier not found."}

        accessorial = []
        for charge in quote.accessorial_charges:
            accessorial.append({
                "name": charge.name,
                "description": charge.description,
                "amount": charge.amount,
            })

        return {
            "status": "success",
            "data": {
                "quote_id": quote.quote_id,
                "carrier": {
                    "id": quote.carrier_id,
                    "name": quote.carrier_name,
                },
                "route_id": quote.route_id,
                "origin": quote.origin,
                "destination": quote.destination,
                "distance_km": quote.distance_km,
                "weight_kg": quote.weight_kg,
                "volume_cbm": quote.volume_cbm,
                "service_level": quote.service_level.value,
                "cost_breakdown": {
                    "base_rate": quote.base_rate,
                    "fuel_surcharge": quote.fuel_surcharge,
                    "accessorial_charges": accessorial,
                    "total_estimate": quote.total_estimate,
                },
                "transit_days": {
                    "min": quote.transit_days_min,
                    "max": quote.transit_days_max,
                },
                "valid_until": quote.valid_until.isoformat(),
                "note": "This is an estimate. Actual rates may vary based on carrier confirmation.",
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to calculate estimate: {str(e)}"}


if __name__ == "__main__":
    print(execute({"origin": "Shanghai", "destination": "Beijing", "weight_kg": 5000}))