#!/usr/bin/env python3
"""
gate_query_appointment: Check the reservation record of collecting cards into Hong Kong.

Support filtering by appointment ID, card collection ID and appointment status.
"""

import sys
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the appointment record inquiry.

    Args:
        params:
            - appointment_id: Appointment ID, specify to query a single record (optional)
            - truck_id: Set card ID filtering (optional)
            - status: Appointment status filter (pending, valid, expired, completed, cancelled) (optional)

    Returns:
        {"status": "success", "data": {"appointments": [...]}} Someone
        {"status": "success", "data": {"appointment": {...}}} Someone
        {"status": "error", "error": "..."}
    """
    data_store = DataStore(data_dir=project_root / "data")
    appointment_id = params.get("appointment_id")
    truck_id = params.get("truck_id")
    status_filter = params.get("status")

    try:
        appointments = data_store.load_appointments()

        if appointment_id:
            # Inquire about a single appointment
            for appointment in appointments:
                if appointment.appointment_id == appointment_id:
                    return {
                        "status": "success",
                        "data": {
                            "appointment": appointment.model_dump(mode="json")
                        }
                    }
            # No appointment found
            return {
                "status": "error",
                "error": f"Appointment {appointment_id} does not exist"
            }

        # Apply filter conditions
        filtered_appointments = appointments

        if truck_id:
            filtered_appointments = [
                a for a in filtered_appointments if a.truck_id == truck_id
            ]

        if status_filter:
            filtered_appointments = [
                a for a in filtered_appointments if a.status.value == status_filter
            ]

        return {
            "status": "success",
            "data": {
                "appointments": [a.model_dump(mode="json") for a in filtered_appointments]
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to query the appointment record: {str(e)}"
        }
