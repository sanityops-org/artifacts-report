#!/usr/bin/env python3
"""
berth_query_berth_status: Check the parking occupancy status and availability information.

Support filtering and querying individual berths by status.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform the berth status query.

    Args:
        params:
            - status: Parking status filtering (available, occupied, reserved, maintenance) (optional)
            - berth_id: Berth ID, specify to query a single berth (optional)

    Returns:
        {"status": "success", "data": {"berths": [...]}} Someone
        {"status": "success", "data": {"berth": {...}}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    status_filter = params.get("status")
    berth_id = params.get("berth_id")

    try:
        berths = data_store.load_berths()

        if berth_id:
            # Query a single berth
            for berth in berths:
                if berth.berth_id == berth_id:
                    return {
                        "status": "success",
                        "data": {
                            "berth": berth.model_dump(mode="json")
                        }
                    }
            # No parking space found
            return {
                "status": "error",
                "error": f"Berth {berth_id} does not exist"
            }

        # Filter by status
        if status_filter:
            filtered_berths = [
                b for b in berths if b.status.value == status_filter
            ]
        else:
            filtered_berths = berths

        return {
            "status": "success",
            "data": {
                "berths": [b.model_dump(mode="json") for b in filtered_berths]
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the berth status: {str(e)}"
        }
