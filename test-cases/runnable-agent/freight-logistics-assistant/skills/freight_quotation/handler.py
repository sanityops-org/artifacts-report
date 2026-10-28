"""Freight quotation skill handler."""

from typing import Any, Dict
from pathlib import Path

from apis.data_store import DataStore
from apis.pricing_engine import (
    calculate_quotation,
    compare_carriers,
    get_transit_time,
)
from models.enums import ServiceLevel, CargoCategory

project_root = Path(__file__).parent.parent.parent


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute freight quotation skill.

    Args:
        params: {"intent": str, ...}

    Supported intents:
        - calculate_estimate: {"intent": "calculate_estimate", "origin": str, "destination": str, "weight_kg": float, ...}
        - compare_carriers: {"intent": "compare_carriers", "origin": str, "destination": str, "weight_kg": float, ...}
        - get_transit_time: {"intent": "get_transit_time", "origin": str, "destination": str, ...}

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": str}
    """
    intent = params.get("intent")
    if not intent:
        return {"status": "error", "error": "Missing required parameter: intent"}

    data_store = DataStore(data_dir=project_root / "data")

    if intent == "calculate_estimate":
        return _handle_calculate(params, data_store)
    elif intent == "compare_carriers":
        return _handle_compare(params, data_store)
    elif intent == "get_transit_time":
        return _handle_transit(params, data_store)
    else:
        return {"status": "error", "error": f"Unknown intent: {intent}"}


def _handle_calculate(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle calculate_estimate intent."""
    origin = params.get("origin")
    destination = params.get("destination")
    weight_kg = params.get("weight_kg", 1000)

    if not origin or not destination:
        return {"status": "error", "error": "Missing required parameters: origin and destination"}

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
        return {"status": "error", "error": "Could not calculate quotation"}

    return {
        "status": "success",
        "data": {
            "quote_id": quote.quote_id,
            "total_estimate": quote.total_estimate,
            "transit_days": {
                "min": quote.transit_days_min,
                "max": quote.transit_days_max,
            },
            "valid_until": quote.valid_until.isoformat(),
        },
    }


def _handle_compare(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle compare_carriers intent."""
    origin = params.get("origin")
    destination = params.get("destination")
    weight_kg = params.get("weight_kg")

    if not origin or not destination or not weight_kg:
        return {"status": "error", "error": "Missing required parameters: origin, destination, and weight_kg"}

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

    quotes = [
        {
            "quote_id": q.quote_id,
            "carrier_name": q.carrier_name,
            "total_estimate": q.total_estimate,
            "transit_days_max": q.transit_days_max,
        }
        for q in comparison.quotes
    ]

    return {
        "status": "success",
        "data": {
            "quotes": quotes,
            "best_price_quote": comparison.best_price,
            "fastest_quote": comparison.fastest,
        },
    }


def _handle_transit(params: Dict[str, Any], data_store: DataStore) -> Dict[str, Any]:
    """Handle get_transit_time intent."""
    origin = params.get("origin")
    destination = params.get("destination")

    if not origin or not destination:
        return {"status": "error", "error": "Missing required parameters: origin and destination"}

    service_level = None
    if params.get("service_level"):
        service_level = ServiceLevel(params["service_level"])

    result = get_transit_time(
        origin=origin,
        destination=destination,
        data_store=data_store,
        carrier_id=params.get("carrier_id"),
        service_level=service_level,
    )

    return {
        "status": "success",
        "data": {
            "min_days": result.min_days,
            "max_days": result.max_days,
            "average_days": result.average_days,
            "factors": result.factors,
        },
    }