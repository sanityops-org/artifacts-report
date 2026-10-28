#!/usr/bin/env python3
"""
berth_query_vessel_plan: Check the mooring plan of the ship.

Support querying a single ship by vessel_id, and return all ships if not transmitted.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out the ship plan inquiry.

    Args:
        params:
            - vessel_id: Ship ID (optional)

    Returns:
        {"status": "success", "data": {"vessels": [...]}} Someone
        {"status": "success", "data": {"vessel": {...}}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    vessel_id = params.get("vessel_id")

    try:
        vessels = data_store.load_vessels()

        if vessel_id:
            # Query a single ship
            for vessel in vessels:
                if vessel.vessel_id == vessel_id:
                    return {
                        "status": "success",
                        "data": {
                            "vessel": vessel.model_dump(mode="json")
                        }
                    }
            # No ship found
            return {
                "status": "error",
                "error": f"Ship {vessel_id} does not exist"
            }

        # Return to all ships
        return {
            "status": "success",
            "data": {
                "vessels": [v.model_dump(mode="json") for v in vessels]
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the ship plan: {str(e)}"
        }
