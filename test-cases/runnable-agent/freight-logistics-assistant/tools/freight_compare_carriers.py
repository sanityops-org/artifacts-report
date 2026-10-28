#!/usr/bin/env python3
"""freight_compare_carriers: Compare freight quotes from multiple carriers.

Use this tool when the user wants to compare pricing from different carriers for the
same shipment. Returns quotes from multiple carriers with rates and transit times,
highlighting the best price and fastest options. If the carriers list is omitted,
up to 5 available carriers are compared.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.pricing_engine import compare_carriers
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
            "description": "Cargo weight in kilograms. Required.",
        },
        "volume_cbm": {
            "type": "number",
            "minimum": 0.1,
            "maximum": 150,
            "description": "Cargo volume in cubic meters. Optional.",
        },
        "cargo_type": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20,
            "enum": ["general", "refrigerated", "hazardous", "oversized", "fragile", "high_value"],
            "description": "Cargo category. Optional.",
        },
        "service_level": {
            "type": "string",
            "minLength": 7,
            "maxLength": 8,
            "enum": ["economy", "standard", "express"],
            "default": "standard",
            "description": "Service level. Optional.",
        },
        "carriers": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 4,
                "maxLength": 4,
                "pattern": "^C\\d{3}$",
                "description": "Carrier identifier from the carrier database (format: C followed by 3 digits, e.g., C001).",
            },
            "minItems": 1,
            "maxItems": 5,
            "description": "List of 1-5 specific carrier IDs to compare. Optional. If omitted, compares up to 5 available carriers.",
        },
    },
    "required": ["origin", "destination", "weight_kg"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare freight quotes from multiple carriers.

    Args:
        params: {"origin": str, "destination": str, "weight_kg": float, ...}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    origin = params.get("origin")
    destination = params.get("destination")
    weight_kg = params.get("weight_kg")

    if not origin or not destination or not weight_kg:
        return {"status": "error", "error": "Missing required parameters: origin, destination, and weight_kg"}

    try:
        data_store = DataStore(data_dir=project_root / "data")

        # Parse enums
        cargo_type = None
        if params.get("cargo_type"):
            cargo_type = CargoCategory(params["cargo_type"])

        service_level = ServiceLevel.STANDARD
        if params.get("service_level"):
            service_level = ServiceLevel(params["service_level"])

        comparison = compare_carriers(
            origin=origin,
            destination=destination,
            weight_kg=weight_kg,
            data_store=data_store,
            volume_cbm=params.get("volume_cbm"),
            cargo_type=cargo_type,
            service_level=service_level,
            carrier_ids=params.get("carriers"),
        )

        quotes = []
        for q in comparison.quotes:
            quotes.append({
                "quote_id": q.quote_id,
                "carrier": {
                    "id": q.carrier_id,
                    "name": q.carrier_name,
                },
                "total_estimate": q.total_estimate,
                "transit_days": {
                    "min": q.transit_days_min,
                    "max": q.transit_days_max,
                },
                "valid_until": q.valid_until.isoformat(),
            })

        return {
            "status": "success",
            "data": {
                "origin": comparison.origin,
                "destination": comparison.destination,
                "weight_kg": comparison.weight_kg,
                "quotes": quotes,
                "total_carriers": len(quotes),
                "best_price_quote": comparison.best_price,
                "fastest_quote": comparison.fastest,
                "generated_at": comparison.generated_at.isoformat(),
                "note": "All quotes are estimates. Verify rates with carriers before booking.",
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to compare carriers: {str(e)}"}


if __name__ == "__main__":
    print(execute({"origin": "Shanghai", "destination": "Beijing", "weight_kg": 5000}))