#!/usr/bin/env python3
"""shipment_list_by_route: List shipments by route filter.

Use this tool when the user wants to see a list of shipments filtered by origin and/or
destination city names; at least one of origin or destination is required. Status and
date range are supplementary filters. Returns a summary list of matching shipments.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from apis.tracking_engine import list_shipments_by_route, ShipmentFilter

parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "origin": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "Filter by origin city name (partial match supported). Optional.",
        },
        "destination": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "Filter by destination city name (partial match supported). Optional.",
        },
        "status": {
            "type": "string",
            "enum": ["pending", "picked_up", "in_transit", "out_for_delivery", "delivered", "exception"],
            "description": "Filter by shipment status. Optional.",
        },
        "date_from": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Filter shipments with pickup date on or after this date (YYYY-MM-DD). Optional.",
        },
        "date_to": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Filter shipments with pickup date on or before this date (YYYY-MM-DD). Optional.",
        },
        "limit": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50,
            "default": 50,
            "description": "Maximum number of shipments to return (1-50, default 50).",
        },
    },
    "required": [],
    "anyOf": [
        {"required": ["origin"]},
        {"required": ["destination"]},
    ],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List shipments by route or filter criteria.

    Args:
        params: {"origin": str, "destination": str, "status": str, "date_from": str, "date_to": str, "limit": int}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    try:
        data_store = DataStore(data_dir=project_root / "data")

        # Build filter
        filter_params = ShipmentFilter()
        if params.get("origin"):
            filter_params.origin = params["origin"]
        if params.get("destination"):
            filter_params.destination = params["destination"]
        if params.get("status"):
            filter_params.status = params["status"]
        if params.get("date_from"):
            filter_params.date_from = datetime.strptime(params["date_from"], "%Y-%m-%d")
        if params.get("date_to"):
            filter_params.date_to = datetime.strptime(params["date_to"], "%Y-%m-%d")

        shipments = list_shipments_by_route(filter_params, data_store)

        limit = params.get("limit", 50)
        try:
            limit = max(1, min(int(limit), 50))
        except (TypeError, ValueError):
            limit = 50

        results = []
        for s in shipments:
            results.append({
                "tracking_number": s.tracking_number,
                "origin": s.origin,
                "destination": s.destination,
                "status": s.status.value,
                "carrier_name": s.carrier_name,
                "pickup_date": s.pickup_date.isoformat() if s.pickup_date else None,
                "eta": s.eta.isoformat() if s.eta else None,
                "weight_kg": s.weight_kg,
            })
            if len(results) >= limit:
                break

        return {
            "status": "success",
            "data": {
                "total_count": len(results),
                "filters_applied": {k: v for k, v in params.items() if v},
                "shipments": results,
            },
        }
    except Exception as e:
        return {"status": "error", "error": f"Failed to list shipments: {str(e)}"}


if __name__ == "__main__":
    print(execute({"origin": "Shanghai"}))