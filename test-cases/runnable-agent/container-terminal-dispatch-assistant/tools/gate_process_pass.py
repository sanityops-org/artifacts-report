#!/usr/bin/env python3
"""
gate_process_pass: Handle the operation of collecting cards in and out.

It includes the verification of the reservation status and the process of entering and leaving the port through the gate channel.
"""

import sys
from pathlib import Path
from typing import Any, Dict
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import DataStore
from models.enums import AppointmentStatus, GateChannelStatus, GateChannelType
from tools._permission import check_tool_permission


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Carry out the card entry and exit processing.

    Args:
        params:
            - truck_id: Collect card vehicle ID (required)
            - channel_id: Channel ID (required)
            - direction: Direction of entry and exit (inbound/outbound) (required)

    Returns:
        {"status": "success", "message": "...", "appointment_valid": bool, ...} Someone
        {"status": "error", "error": "..."}
    """

    # Permission verification
    permission_error = check_tool_permission("gate_process_pass", params)
    if permission_error:
        return permission_error

    truck_id = params.get("truck_id")
    channel_id = params.get("channel_id")
    direction = params.get("direction")

    # Parameter verification
    if not truck_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: truck_id"
        }

    if not channel_id:
        return {
            "status": "error",
            "error": "The required parameters are missing: channel_id"
        }

    if not direction:
        return {
            "status": "error",
            "error": "The required parameters are missing: direction"
        }

    if direction not in ("inbound", "outbound"):
        return {
            "status": "error",
            "error": f"Invalid entry and exit direction: {direction}, must be inbound or outbound"
        }

    data_store = DataStore(data_dir=project_root / "data")

    try:
        channels = data_store.load_gate_channels()
        appointments = data_store.load_appointments()

        # Find the channel
        channel = None
        for c in channels:
            if c.channel_id == channel_id:
                channel = c
                break

        if not channel:
            return {
                "status": "error",
                "error": f"Gate channel {channel_id} does not exist"
            }

        # Check the channel status
        if channel.status != GateChannelStatus.OPEN:
            return {
                "status": "error",
                "error": f"The current status of the gate channel {channel_id} is {channel.status.value}, and it is not allowed to pass."
            }

        # Check the channel type and the direction of entry and exit
        expected_type = GateChannelType.INBOUND if direction == "inbound" else GateChannelType.OUTBOUND
        if channel.type != expected_type:
            return {
                "status": "error",
                "error": f"The channel {channel_id} type is {channel.type.value}, and the {direction} operation is not supported."
            }

        # Find the appointment record
        appointment = None
        for a in appointments:
            if a.truck_id == truck_id:
                appointment = a
                break

        # Make an appointment for verification
        appointment_valid = False
        appointment_info = None
        validation_messages = []

        if not appointment:
            validation_messages.append(f"The reservation record of the collection card {truck_id} was not found.")
        else:
            appointment_info = appointment.model_dump(mode="json")

            # Check the appointment status
            if appointment.status == AppointmentStatus.CANCELLED:
                validation_messages.append(f"Appointment {appointment.appointment_id} has been cancelled")
            elif appointment.status == AppointmentStatus.EXPIRED:
                validation_messages.append(f"The appointment {appointment.appointment_id} has expired")
            elif appointment.status == AppointmentStatus.COMPLETED:
                validation_messages.append(f"Reservation {appointment.appointment_id} completed")
            elif appointment.status in (AppointmentStatus.PENDING, AppointmentStatus.VALID):
                # Check the appointment time
                try:
                    appointment_time = datetime.fromisoformat(appointment.appointment_time)
                    now = datetime.now()

                    # If the appointment has expired (2 hours more than the appointment time)
                    time_diff = (now - appointment_time).total_seconds()
                    if time_diff > 7200:  # 2Hours = 7200 seconds
                        validation_messages.append(f"The appointment {appointment.appointment_id} has exceeded the validity time")
                    else:
                        appointment_valid = True
                except ValueError:
                    validation_messages.append(f"The appointment time format is invalid.: {appointment.appointment_time}")

        # Update the number of queues
        channel.queue_length += 1
        data_store.save_gate_channels(channels)

        # Update the appointment status (if the appointment is valid)
        if appointment and appointment_valid:
            appointment.status = AppointmentStatus.COMPLETED
            data_store.save_appointments(appointments)

        # Construction return results
        if appointment_valid:
            return {
                "status": "success",
                "message": f"The collection card {truck_id} has passed {channel_id} ({channel.channel_name}) {direction}, and the appointment verification has passed.",
                "appointment_valid": True,
                "appointment_info": appointment_info
            }
        else:
            # The appointment verification failed, but it is still allowed to pass (record warning)
            return {
                "status": "success",
                "message": f"The set card {truck_id} has passed {channel_id} ({channel.channel_name}) {direction}, but there is a problem with the appointment verification.",
                "appointment_valid": False,
                "validation_warnings": validation_messages,
                "appointment_info": appointment_info
            }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to process the card entry and exit port: {str(e)}"
        }
