#!/usr/bin/env python3
"""
energy_calculate_carbon_footprint: Calculate carbon footprint from energy consumption.

Calculates carbon emissions from a facility's recorded electricity and natural gas
consumption (looked up by facility_id) using the built-in emission factors
(electricity_grid 0.42 kg CO2/kWh, natural_gas 2.0 kg CO2/m3; the diesel factor is
defined but not applied because no diesel input is accepted). Region selection is
fixed to the built-in US-average factor. Returns total emissions and breakdown by
energy source.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

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
            "description": "Facility identifier from the facility database (format: FAC followed by 3 digits, e.g., FAC001).",
        },
        "start_date": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Calculation period start date (YYYY-MM-DD).",
        },
        "end_date": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Calculation period end date (YYYY-MM-DD).",
        },
        "include_breakdown": {
            "type": "boolean",
            "default": True,
            "description": "Include breakdown by energy source. Default: true.",
        },
    },
    "required": ["facility_id", "start_date", "end_date"],
}


# Emission factors (simplified - in production use region-specific data)
EMISSION_FACTORS = {
    "electricity_grid": 0.42,  # kg CO2/kWh (US average)
    "natural_gas": 2.0,  # kg CO2/m³
    "diesel": 2.68,  # kg CO2/liter
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate carbon footprint from energy consumption.

    Args:
        params:
            - facility_id: Facility identifier (required)
            - start_date: Calculation period start (required)
            - end_date: Calculation period end (required)
            - include_breakdown: Include breakdown by energy source (optional)

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": "..."}
    """
    facility_id = params.get("facility_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")
    include_breakdown = params.get("include_breakdown", True)

    if not all([facility_id, start_date, end_date]):
        return {"status": "error", "error": "Missing required parameters: facility_id, start_date, end_date"}

    try:
        # Validate dates
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")

        # Load data
        data_store = DataStore(data_dir=project_root / "data")
        facilities = data_store.load_facilities()
        consumption_data = data_store.load_consumption_patterns()

        # Find facility
        facility = None
        for f in facilities:
            if f.get("facility_id") == facility_id:
                facility = f
                break

        if not facility:
            return {"status": "error", "error": f"Facility {facility_id} not found"}

        # Filter consumption data
        facility_consumption = [
            c for c in consumption_data
            if c.get("facility_id") == facility_id
        ]

        # Simulate consumption values (would aggregate from actual data in production)
        import random
        random.seed(hash(facility_id + start_date) % 10000)

        annual_consumption = facility.get("annual_consumption_kwh", 2000000)
        monthly_electricity = annual_consumption / 12
        monthly_gas = 5000 + random.random() * 2000

        # Calculate emissions
        electricity_emissions = monthly_electricity * EMISSION_FACTORS["electricity_grid"]
        gas_emissions = monthly_gas * EMISSION_FACTORS["natural_gas"]
        other_emissions = 0

        total_emissions = electricity_emissions + gas_emissions + other_emissions

        # Emission intensity
        facility_area = facility.get("floor_area_m2", 10000)
        intensity_per_sqm = total_emissions / facility_area
        intensity_per_kwh = total_emissions / (monthly_electricity + monthly_gas * 10)

        # Previous period comparison (simulated)
        previous_total = total_emissions * (0.95 + random.random() * 0.1)
        change_percent = ((total_emissions - previous_total) / previous_total) * 100

        return {
            "status": "success",
            "data": {
                "facility_id": facility_id,
                "facility_name": facility.get("name", facility_id),
                "period": {"start": start_date, "end": end_date},
                "total_emissions_kgco2": round(total_emissions, 1),
                "emission_intensity": {
                    "per_sqm": round(intensity_per_sqm, 2),
                    "per_kwh": round(intensity_per_kwh, 4)
                },
                "breakdown": {
                    "electricity_kgco2": round(electricity_emissions, 1),
                    "natural_gas_kgco2": round(gas_emissions, 1),
                    "other_kgco2": round(other_emissions, 1),
                    "electricity_percent": round(electricity_emissions / total_emissions * 100, 1),
                    "natural_gas_percent": round(gas_emissions / total_emissions * 100, 1)
                } if include_breakdown else None,
                "comparison": {
                    "previous_period_kgco2": round(previous_total, 1),
                    "change_percent": round(change_percent, 1)
                },
                "notes": [
                    "Emission factors: Electricity 0.42 kg CO2/kWh, Natural gas 2.0 kg CO2/m³",
                    "For Scope 2 reporting, specify market-based or location-based method",
                    "Consider renewable energy certificates to reduce Scope 2 emissions"
                ]
            }
        }

    except ValueError as e:
        return {"status": "error", "error": f"Invalid date format: {e}"}
    except Exception as e:
        return {"status": "error", "error": f"Carbon calculation failed: {str(e)}"}


if __name__ == "__main__":
    result = execute({
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-30"
    })
    import json
    print(json.dumps(result, indent=2))