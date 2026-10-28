#!/usr/bin/env python3
"""
berth_update_plan: Update the ship's berth plan.

Support updating the ship's ETA, ETD or allocation of berth information.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implement the update of the ship's mooring plan.

    Args:
        params:
            - vessel_id: Ship ID (required)
            - eta: Estimated arrival time, ISO 8601 format (optional)
            - etd: Estimated departure time, ISO 8601 format (optional)
            - assigned_berth: Assigned berth ID (optional)

    Returns:
        {"status": "success", "message": "...", "updated_fields": [...]} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("berth_update_plan", params)
    if permission_error:
        return permission_error

    vessel_id = params.get("vessel_id")

    # Parameter verification
    if not vessel_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: vessel_id"
        }

    # Check whether there is an update field
    eta = params.get("eta")
    etd = params.get("etd")
    assigned_berth = params.get("assigned_berth")

    if not any([eta, etd, assigned_berth]):
        return {
            "status": "error",
            "error": "Please provide at least one updated field. (eta, etd, assigned_berth)"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        vessels = data_store.load_vessels()

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

        # Record the updated fields
        updated_fields = []

        # RenewETA
        if eta:
            vessel.eta = eta
            updated_fields.append("eta")

        # RenewETD
        if etd:
            vessel.etd = etd
            updated_fields.append("etd")

        # Update the allocation of berths
        if assigned_berth:
            vessel.assigned_berth = assigned_berth
            updated_fields.append("assigned_berth")

        # Save data
        data_store.save_vessels(vessels)

        return {
            "status": "success",
            "message": f"Ship {vessel_id} ({vessel.vessel_name}) mooring plan has been updated",
            "updated_fields": updated_fields
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to update the mooring plan: {str(e)}"
        }
