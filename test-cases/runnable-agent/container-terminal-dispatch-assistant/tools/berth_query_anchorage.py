#!/usr/bin/env python3
"""
berth_query_anchorage: Query the ships currently waiting for anchorage.

Returns a list of all ships with the status at_anchor.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import VesselStatus


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out the anchorage ship inquiry.

    Args:
        params: Query parameters (currently not used, keep the extension)

    Returns:
        {"status": "success", "data": {"vessels": [...], "count": N}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")

    try:
        vessels = data_store.load_vessels()

        # Filter out anchored ships
        anchored_vessels = [
            v for v in vessels if v.status == VesselStatus.AT_ANCHOR
        ]

        return {
            "status": "success",
            "data": {
                "vessels": [v.model_dump(mode="json") for v in anchored_vessels],
                "count": len(anchored_vessels)
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the anchorage ship: {str(e)}"
        }
