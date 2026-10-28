#!/usr/bin/env python3
"""
energy_suggest_renewables: Provide renewable energy integration recommendations.

Analyzes facility characteristics and location to provide recommendations for solar,
wind, and other renewable energy options. Includes suitability assessment, sizing
guidance, and ROI projections.
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
            "description": "Facility identifier from the facility database (format: FAC followed by 3 digits, e.g., FAC001). Facility location and characteristics are looked up from this ID.",
        },
        "renewable_types": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20,
                "enum": ["solar", "wind", "storage"],
                "description": "One renewable type: solar, wind, or storage.",
            },
            "minItems": 1,
            "maxItems": 3,
            "description": "Types of renewables to assess. Default: ['solar'].",
        },
        "target_coverage": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "description": "Target percentage of consumption to cover (0-100). Default: 50.",
        },
    },
    "required": ["facility_id"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Provide renewable energy integration recommendations.

    Args:
        params:
            - facility_id: Facility identifier (required)
            - renewable_types: Types to assess - ["solar", "wind", "storage"] (optional)
            - target_coverage: Target percentage of consumption to cover (optional)

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": "..."}
    """
    facility_id = params.get("facility_id")
    renewable_types = params.get("renewable_types", ["solar"])
    target_coverage = params.get("target_coverage", 50)

    if not facility_id:
        return {"status": "error", "error": "Missing required parameter: facility_id"}

    try:
        # Load data
        data_store = DataStore(data_dir=project_root / "data")
        facilities = data_store.load_facilities()
        renewable_options = data_store.load_renewable_options()

        # Find facility
        facility = None
        for f in facilities:
            if f.get("facility_id") == facility_id:
                facility = f
                break

        if not facility:
            return {"status": "error", "error": f"Facility {facility_id} not found"}

        annual_consumption = facility.get("annual_consumption_kwh", 2000000)
        floor_area = facility.get("floor_area_m2", 10000)
        facility_type = facility.get("type", "office")

        random.seed(hash(facility_id + "renewable") % 10000)

        # Estimate roof area (typically 30-50% of floor area for single-story, less for multi-story)
        stories = max(1, floor_area // 5000)  # Rough estimate
        roof_area = floor_area / stories * 0.8

        assessments = {}

        # Solar assessment
        if "solar" in renewable_types:
            # Calculate solar potential
            usable_roof = roof_area * 0.7  # Accounting for setbacks, equipment
            panel_capacity_kw = usable_roof * 0.15  # ~150 W/m²
            capacity_factor = 0.18 + random.random() * 0.04
            annual_generation = panel_capacity_kw * 8760 * capacity_factor

            constraints = []
            if random.random() > 0.7:
                constraints.append("Partial roof shading detected - detailed survey recommended")
            if random.random() > 0.8:
                constraints.append("Roof may require structural reinforcement")

            assessments["solar"] = {
                "suitable_roof_area_m2": round(usable_roof, 0),
                "estimated_capacity_kw": round(panel_capacity_kw, 0),
                "annual_generation_kwh": round(annual_generation, 0),
                "capacity_factor": round(capacity_factor, 3),
                "suitability_score": 70 + int(random.random() * 25),
                "coverage_achievable": min(100, round(annual_generation / annual_consumption * 100, 1)),
                "constraints": constraints if constraints else ["No significant constraints identified"],
                "estimated_annual_savings": round(annual_generation * 0.12, 0),
                "estimated_system_cost": round(panel_capacity_kw * 1500, 0)
            }

        # Wind assessment
        if "wind" in renewable_types:
            avg_wind_speed = 4.5 + random.random() * 2
            suitable = avg_wind_speed > 5.5

            assessments["wind"] = {
                "average_wind_speed_ms": round(avg_wind_speed, 1),
                "suitable_turbine_types": ["Small vertical axis"] if suitable else [],
                "estimated_capacity_kw": 50 if suitable else 0,
                "annual_generation_kwh": round(50 * 8760 * 0.15, 0) if suitable else 0,
                "suitability_score": 50 + int(avg_wind_speed * 5) if suitable else 30,
                "constraints": [
                    "Site wind resource marginal for wind energy",
                    "Zoning restrictions may apply",
                    "Noise and visual impact considerations"
                ],
                "recommendation": "Consider solar as primary renewable option" if not suitable else "Small-scale wind may supplement solar"
            }

        # Storage assessment
        if "storage" in renewable_types:
            peak_demand = facility.get("peak_demand_kw", annual_consumption / 8760 * 1.3)
            recommended_size = peak_demand * 2  # 2-hour backup

            assessments["storage"] = {
                "recommended_capacity_kwh": round(recommended_size, 0),
                "recommended_power_kw": round(peak_demand, 0),
                "applications": [
                    "Peak shaving (demand charge reduction)",
                    "Backup power for critical loads",
                    "Solar self-consumption optimization"
                ],
                "estimated_cost": round(recommended_size * 400, 0),
                "estimated_annual_savings": round(peak_demand * 12 * 20, 0),
                "suitability_score": 75 + int(random.random() * 15)
            }

        # Determine primary recommendation
        if "solar" in assessments:
            primary = "solar"
            rationale = f"Solar PV offers the highest suitability score with potential to cover {assessments['solar']['coverage_achievable']}% of annual consumption."
        elif "storage" in assessments:
            primary = "storage"
            rationale = "Energy storage can provide immediate value through demand charge reduction and backup power."
        else:
            primary = "none"
            rationale = "Limited renewable potential at this site. Consider off-site renewable procurement."

        next_steps = [
            "Request professional site assessment for detailed analysis",
            "Review utility interconnection requirements and net metering policies",
            "Evaluate financing options (purchase, lease, PPA)",
            "Check available incentives and tax credits"
        ]

        return {
            "status": "success",
            "data": {
                "facility_id": facility_id,
                "facility_name": facility.get("name", facility_id),
                "target_coverage_percent": target_coverage,
                "assessments": assessments,
                "recommendation": {
                    "primary_option": primary,
                    "rationale": rationale,
                    "next_steps": next_steps
                },
                "disclaimer": "⚠️ Renewable energy installations require professional engineering assessment, utility approval, and applicable permits. These estimates are for planning purposes only."
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Renewable assessment failed: {str(e)}"}


if __name__ == "__main__":
    result = execute({
        "facility_id": "FAC001",
        "renewable_types": ["solar", "storage"]
    })
    import json
    print(json.dumps(result, indent=2))