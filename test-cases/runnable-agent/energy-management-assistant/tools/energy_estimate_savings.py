#!/usr/bin/env python3
"""
energy_estimate_savings: Estimate savings from specific efficiency measures.

Calculates projected energy and cost savings from proposed efficiency measures
using baseline consumption data and expected efficiency improvements.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List
import random

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


parameters: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "facility_id": {
            "type": "string",
            "minLength": 6,
            "maxLength": 6,
            "pattern": "^FAC\\d{3}$",
            "description": "Facility identifier from the facility database (format: FAC followed by 3 digits, e.g., FAC001). Baseline consumption is inferred from this facility's recorded data.",
        },
        "measures": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "measure_type": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 50,
                        "enum": ["hvac", "lighting", "equipment", "process", "envelope"],
                        "description": "Type of efficiency measure. hvac = heating/ventilation/air-conditioning; lighting = light fixtures and controls; equipment = process or production equipment; process = production process tuning; envelope = building shell (insulation, glazing).",
                    },
                    "scope": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20,
                        "pattern": "^\\d{1,3}(\\.\\d+)?%$",
                        "description": "Percentage of facility affected, formatted as a percentage string with a percent sign (e.g., '50%', '100%'). The pattern requires 1-3 digits optionally followed by a decimal and a trailing % sign; plain numbers like 50 without the % sign are rejected. Optional; when omitted the tool applies the measure to 100% of the facility.",
                    },
                    "efficiency_improvement": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100,
                        "description": "Expected efficiency gain percentage (0-100).",
                    },
                },
                "required": ["measure_type", "efficiency_improvement"],
            },
            "minItems": 1,
            "maxItems": 10,
            "description": "List of efficiency measures to evaluate (1-10 items).",
        },
    },
    "required": ["facility_id", "measures"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate savings from specified efficiency measures.

    Args:
        params:
            - facility_id: Facility identifier (required)
            - measures: List of measures to evaluate (required)
                Each measure has:
                - measure_type: Type of efficiency measure
                - scope: Percentage of facility affected (optional)
                - efficiency_improvement: Expected efficiency gain percentage

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": "..."}
    """
    facility_id = params.get("facility_id")
    measures = params.get("measures")

    if not facility_id:
        return {"status": "error", "error": "Missing required parameter: facility_id"}
    if not measures:
        return {"status": "error", "error": "Missing required parameter: measures"}

    try:
        # Load data
        data_store = DataStore(data_dir=project_root / "data")
        facilities = data_store.load_facilities()

        # Find facility
        facility = None
        for f in facilities:
            if f.get("facility_id") == facility_id:
                facility = f
                break

        if not facility:
            return {"status": "error", "error": f"Facility {facility_id} not found"}

        annual_consumption = facility.get("annual_consumption_kwh", 2000000)
        electricity_rate = 0.12  # $/kWh

        # Measure type to baseline allocation
        measure_baselines = {
            "hvac": 0.35,
            "lighting": 0.15,
            "equipment": 0.25,
            "process": 0.15,
            "envelope": 0.10
        }

        measure_analyses = []
        total_savings_kwh = 0
        total_savings_cost = 0

        for measure in measures:
            measure_type = measure.get("measure_type", "equipment")
            efficiency = measure.get("efficiency_improvement", 10) / 100
            scope = measure.get("scope", "100%")

            # Determine baseline for this measure type
            baseline_fraction = measure_baselines.get(measure_type.lower(), 0.20)
            baseline_kwh = annual_consumption * baseline_fraction

            # Calculate savings
            savings_kwh = baseline_kwh * efficiency
            projected_kwh = baseline_kwh - savings_kwh

            # Confidence interval (±20%)
            confidence_low = savings_kwh * 0.80
            confidence_high = savings_kwh * 1.20

            cost_savings = savings_kwh * electricity_rate

            measure_analyses.append({
                "measure_type": measure_type,
                "scope": scope,
                "baseline_consumption_kwh": round(baseline_kwh, 0),
                "projected_consumption_kwh": round(projected_kwh, 0),
                "annual_savings_kwh": round(savings_kwh, 0),
                "annual_cost_savings": round(cost_savings, 0),
                "confidence_interval": {
                    "low": round(confidence_low, 0),
                    "high": round(confidence_high, 0)
                }
            })

            total_savings_kwh += savings_kwh
            total_savings_cost += cost_savings

        return {
            "status": "success",
            "data": {
                "facility_id": facility_id,
                "facility_name": facility.get("name", facility_id),
                "measure_analyses": measure_analyses,
                "total_savings": {
                    "annual_kwh": round(total_savings_kwh, 0),
                    "annual_cost": round(total_savings_cost, 0),
                    "percent_of_total": round(total_savings_kwh / annual_consumption * 100, 1)
                },
                "assumptions": [
                    f"Total annual consumption: {annual_consumption:,} kWh",
                    f"Electricity rate: ${electricity_rate}/kWh",
                    "Confidence interval: ±20% of projected savings",
                    "Actual savings depend on implementation quality and operational conditions"
                ]
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Savings estimation failed: {str(e)}"}


if __name__ == "__main__":
    result = execute({
        "facility_id": "FAC001",
        "measures": [
            {"measure_type": "hvac", "efficiency_improvement": 15},
            {"measure_type": "lighting", "efficiency_improvement": 25}
        ]
    })
    import json
    print(json.dumps(result, indent=2))