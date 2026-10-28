#!/usr/bin/env python3
"""
berth_confirm_departure: Confirm the departure of the ship.

Release the berth resources and update the ship status to have left Hong Kong.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import BerthStatus, VesselStatus
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implement the confirmation of the ship's departure.

    Args:
        params:
            - vessel_id: Ship ID (required)

    Returns:
        {"status": "success", "message": "..."} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("berth_confirm_departure", params)
    if permission_error:
        return permission_error

    vessel_id = params.get("vessel_id")

    # Parameter verification
    if not vessel_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: vessel_id"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        vessels = data_store.load_vessels()
        berths = data_store.load_berths()

        # Search for ships
        vessel = None
        for v in vessels:
            if v.vessel_id == vessel_id:
                vessel = v
                break

        if not vessel:
            return {
                "status": "error",
                "error": f"Ship {vessel_id} does not exist"
            }

        # Check whether the ship is moored
        if vessel.status not in [VesselStatus.BERTHED, VesselStatus.WORKING, VesselStatus.DEPARTING]:
            return {
                "status": "error",
                "error": f"The current status of the ship {vessel_id} is {vessel.status.value}, which is not in a mooring state and cannot confirm the departure."
            }

        # Check whether the ship has an allocated berth
        if not vessel.assigned_berth:
            return {
                "status": "error",
                "error": f"The ship {vessel_id} has not been assigned a berth and cannot confirm the departure."
            }

        # Find a berth
        berth_id = vessel.assigned_berth
        berth = None
        for b in berths:
            if b.berth_id == berth_id:
                berth = b
                break

        if not berth:
            return {
                "status": "error",
                "error": f"The berth {berth_id} allocated by the ship does not exist"
            }

        # Release the berth
        berth.status = BerthStatus.AVAILABLE
        berth.current_vessel = None

        # Update the status of the ship
        vessel.status = VesselStatus.DEPARTED
        vessel.assigned_berth = None

        # Save data
        data_store.save_berths(berths)
        data_store.save_vessels(vessels)

        return {
            "status": "success",
            "message": f"The ship {vessel_id} ({vessel.vessel_name}) has been confirmed to leave the port, and the berth {berth_id} has been released."
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Confirm the failure of departure: {str(e)}"
        }
