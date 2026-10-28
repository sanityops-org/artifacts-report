#!/usr/bin/env python3
"""
energy_analyze_consumption: Analyze energy consumption patterns and detect anomalies.

Analyzes consumption data for a facility over a specified period, identifying
usage patterns, peak demand, and anomalies. Returns structured analysis results.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timedelta
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
            "description": "Facility identifier from the facility database (format: FAC followed by 3 digits, e.g., FAC001).",
        },
        "start_date": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Analysis period start date (YYYY-MM-DD format).",
        },
        "end_date": {
            "type": "string",
            "minLength": 10,
            "maxLength": 10,
            "format": "date",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
            "description": "Analysis period end date (YYYY-MM-DD format).",
        },
        "granularity": {
            "type": "string",
            "minLength": 5,
            "maxLength": 7,
            "enum": ["hourly", "daily", "monthly"],
            "default": "daily",
            "description": "Data grouping granularity. Default: daily.",
        },
    },
    "required": ["facility_id", "start_date", "end_date"],
}


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute consumption analysis for a facility.

    Args:
        params:
            - facility_id: Facility identifier (required)
            - start_date: Analysis period start (YYYY-MM-DD) (required)
            - end_date: Analysis period end (YYYY-MM-DD) (required)
            - granularity: Data grouping - "hourly", "daily", "monthly" (optional)

    Returns:
        {"status": "success", "data": {...}} or {"status": "error", "error": "..."}
    """
    facility_id = params.get("facility_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")
    granularity = params.get("granularity", "daily")

    if not all([facility_id, start_date, end_date]):
        return {"status": "error", "error": "Missing required parameters: facility_id, start_date, end_date"}

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end < start:
            return {"status": "error", "error": "end_date must be after start_date"}

        days = (end - start).days + 1
        if days < 1:
            return {"status": "error", "error": "Analysis period must be at least 1 day"}

    except ValueError as e:
        return {"status": "error", "error": f"Invalid date format: {e}"}

    try:
        # Load facility data
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

        # Filter consumption data for facility and date range
        facility_consumption = [
            c for c in consumption_data
            if c.get("facility_id") == facility_id
        ]

        # Base consumption from facility data or estimated
        base_annual = facility.get("annual_consumption_kwh", 2000000)
        base_daily = base_annual / 365

        # Generate analysis results
        random.seed(hash(facility_id + start_date) % 10000)
        total_consumption = base_daily * days * (0.9 + random.random() * 0.2)
        peak_demand = base_daily / 24 * 1.3
        average_daily = total_consumption / days

        # Pattern analysis
        peak_hours = [9, 10, 11, 14, 15, 16]
        weekday_weekend = 1.4 + random.random() * 0.3
        load_factor = 0.65 + random.random() * 0.15

        # Anomaly detection
        anomalies = []
        anomaly_count = min(3, max(0, days // 7))
        for i in range(anomaly_count):
            anomaly_date = start + timedelta(days=random.randint(0, days - 1))
            expected = base_daily * (0.95 + random.random() * 0.1)
            actual = expected * (1.3 + random.random() * 0.4)
            anomalies.append({
                "date": anomaly_date.strftime("%Y-%m-%d"),
                "consumption_kwh": round(actual, 1),
                "expected_kwh": round(expected, 1),
                "deviation_percent": round((actual - expected) / expected * 100, 1),
                "severity": "high" if (actual - expected) / expected > 0.5 else "medium"
            })

        # Benchmark comparison
        facility_type_avg = 6000
        performance = 50 + int((facility_type_avg - average_daily) / facility_type_avg * 50)
        performance = max(10, min(90, performance))

        if average_daily < facility_type_avg * 0.8:
            assessment = "above_average"
        elif average_daily < facility_type_avg * 1.2:
            assessment = "average"
        else:
            assessment = "below_average"

        return {
            "status": "success",
            "data": {
                "facility_id": facility_id,
                "facility_name": facility.get("name", facility_id),
                "facility_type": facility.get("type", "unknown"),
                "analysis_period": {"start": start_date, "end": end_date},
                "total_consumption_kwh": round(total_consumption, 1),
                "peak_demand_kw": round(peak_demand, 1),
                "average_daily_kwh": round(average_daily, 1),
                "patterns": {
                    "peak_hours": peak_hours,
                    "weekday_weekend_ratio": round(weekday_weekend, 2),
                    "load_factor": round(load_factor, 2)
                },
                "anomalies": sorted(anomalies, key=lambda x: x["date"]),
                "benchmark_comparison": {
                    "facility_type_average": facility_type_avg,
                    "performance_percentile": performance,
                    "assessment": assessment
                }
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Analysis failed: {str(e)}"}


if __name__ == "__main__":
    result = execute({
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-30"
    })
    import json
    print(json.dumps(result, indent=2))