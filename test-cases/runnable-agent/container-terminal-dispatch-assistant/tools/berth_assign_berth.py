#!/usr/bin/env python3
"""
berth_assign_berth: Assign the ship to the designated berth.

The execution verification includes permission verification, berth status, ship water, ship length, and return the alternative berth recommendation when it fails.
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
    Execute the berth allocation.

    Args:
        params:
            - vessel_id: Ship ID (required)
            - berth_id: Berth ID (required)
            - _session: Conversation information (system injection)

    Returns:
        {"status": "success", "message": "..."} Someone
        {"status": "error", "error": "...", "alternatives": [...]}
    """
    # 1. Permission verification
    permission_error = check_tool_permission("berth_assign_berth", params)
    if permission_error:
        return permission_error

    vessel_id = params.get("vessel_id")
    berth_id = params.get("berth_id")

    # Parameter verification
    if not vessel_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: vessel_id"
        }

    if not berth_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: berth_id"
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

        # Find a berth
        berth = None
        for b in berths:
            if b.berth_id == berth_id:
                berth = b
                break

        if not berth:
            return {
                "status": "error",
                "error": f"Berth {berth_id} does not exist"
            }

        # Check the berth status
        if berth.status != BerthStatus.AVAILABLE:
            # Find an alternative berth
            alternatives = _find_alternative_berths(vessel, berths, berth_id)

            status_msg = {
                BerthStatus.OCCUPIED: "It has been occupied",
                BerthStatus.RESERVED: "It has been reserved",
                BerthStatus.MAINTENANCE: "Under maintenance"
            }

            return {
                "status": "error",
                "error": f"Berth {berth_id} {status_msg.get(berth.status, ' unavailable')}",
                "alternatives": alternatives
            }

        # Check the ship's water <= berth max_draft
        if vessel.draft > berth.max_draft:
            alternatives = _find_alternative_berths(vessel, berths, berth_id)

            return {
                "status": "error",
                "error": f"Ship draft {vessel.draft}m exceeds the maximum draft limit of berth {berth.max_draft}m",
                "alternatives": alternatives
            }

        # Check the length of the ship <= the length of the berth
        if vessel.length > berth.length:
            alternatives = _find_alternative_berths(vessel, berths, berth_id)

            return {
                "status": "error",
                "error": f"The length of the ship {vessel.length}m exceeds the berth length limit {berth.length}m",
                "alternatives": alternatives
            }

        # Execute the allocation
        # Update the parking status
        berth.status = BerthStatus.OCCUPIED
        berth.current_vessel = vessel_id

        # Update the status of the ship
        vessel.assigned_berth = berth_id
        vessel.status = VesselStatus.BERTHING

        # Save data
        data_store.save_berths(berths)
        data_store.save_vessels(vessels)

        return {
            "status": "success",
            "message": f"The ship {vessel_id} ({vessel.vessel_name}) has been successfully assigned to the berth. {berth_id} ({berth.berth_name})"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to allocate berths: {str(e)}"
        }


def _find_alternative_berths(vessel, berths: list, excluded_berth_id: str = None) -> list:
    """
    Find eligible alternative berths.

    Args:
        vessel: Ship object
        berths: List of parking spaces
        excluded_berth_id: Excluded berthID

    Returns:
        list: List of eligible alternative berths
    """
    alternatives = []

    for berth in berths:
        # Exclude designated berths
        if berth.berth_id == excluded_berth_id:
            continue

        # Must be available
        if berth.status != BerthStatus.AVAILABLE:
            continue

        # Water-in-water restrictions
        if vessel.draft > berth.max_draft:
            continue

        # Length limit
        if vessel.length > berth.length:
            continue

        alternatives.append({
            "berth_id": berth.berth_id,
            "berth_name": berth.berth_name,
            "length": berth.length,
            "max_draft": berth.max_draft
        })

    return alternatives
