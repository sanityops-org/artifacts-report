"""
Gate data model

Define the Pydantic model of GateChannel and Appointment for the container terminal dispatching system.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from models.enums import GateChannelType, GateChannelStatus, TaskType, AppointmentStatus


class GateChannel(BaseModel):
    """
    Gate channel model

    Describe the attribute information of the container terminal gate channel, including the basic information of the channel, the status, the queue, etc.

    Attributes:
        channel_id: Channel unique identifier, the format is G followed by 2 digits (such as G01)
        channel_name: Channel name
        type: Channel type, entry gate or exit gate
        status: Channel status, default OPEN
        queue_length: Queue length, default 0
    """

    channel_id: str = Field(
        ...,
        pattern=r"^G\d{2}$",
        description="Channel unique identifier, the format is G followed by 2 digits.",
        examples=["G01", "G12", "G99"],
    )
    channel_name: str = Field(
        ...,
        description="Channel name",
    )
    type: GateChannelType = Field(
        ...,
        description="Channel type (in/out gate)",
    )
    status: GateChannelStatus = Field(
        default=GateChannelStatus.OPEN,
        description="Channel status",
    )
    queue_length: int = Field(
        default=0,
        ge=0,
        description="Queue length",
    )

    @field_validator("channel_id")
    @classmethod
    def validate_channel_id(cls, v: str) -> str:
        """Verify the channel ID format"""
        if not re.match(r"^G\d{2}$", v):
            raise ValueError(
                f"The channel ID format is invalid: {v}, which must be G followed by 2 digits (such as G01)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "channel_id": "G01",
                    "channel_name": "Gate passage No.1",
                    "type": "inbound",
                    "status": "open",
                    "queue_length": 5,
                }
            ]
        }
    }


class Appointment(BaseModel):
    """
    Make an appointment model

    Describe the attribute information of the card entry appointment, including the basic information of the reservation, vehicle information, the appointment time, etc.

    Attributes:
        appointment_id: The unique identifier of the reservation, the format is AP followed by 3 digits (such as AP001)
        truck_id: Collect card vehiclesID
        driver_name: Driver's name
        appointment_time: Appointment time (ISO 8601 format)
        type: Task type, pick-up box (GATE_OUT) or delivery box(GATE_IN)
        container_id: ContainerID
        status: Appointment status, default PENDING
    """

    appointment_id: str = Field(
        ...,
        pattern=r"^AP\d{3}$",
        description="The reservation is a unique identifier, and the format is AP followed by 3 digits.",
        examples=["AP001", "AP123", "AP999"],
    )
    truck_id: str = Field(
        ...,
        description="Collect card vehiclesID",
    )
    driver_name: str = Field(
        ...,
        description="Driver's name",
    )
    appointment_time: str = Field(
        ...,
        description="Appointment time (ISO 8601 format)",
    )
    type: TaskType = Field(
        ...,
        description="Task type (pick up the box GATE_OUT/delit the box)GATE_IN）",
    )
    container_id: str = Field(
        ...,
        description="ContainerID",
    )
    status: AppointmentStatus = Field(
        default=AppointmentStatus.PENDING,
        description="Appointment status",
    )

    @field_validator("appointment_id")
    @classmethod
    def validate_appointment_id(cls, v: str) -> str:
        """Verify the reservation ID format"""
        if not re.match(r"^AP\d{3}$", v):
            raise ValueError(
                f"The reservation ID format is invalid: {v}, which must be followed by 3 digits after AP (such as AP001)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "appointment_id": "AP001",
                    "truck_id": "T001",
                    "driver_name": "Zhang San",
                    "appointment_time": "2024-01-15T08:00:00",
                    "type": "gate_out",
                    "container_id": "C001",
                    "status": "pending",
                }
            ]
        }
    }


__all__ = ["GateChannel", "Appointment"]
