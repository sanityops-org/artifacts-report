"""
Device and task data model

Define the Pydantic model of Equipment and Task for the container terminal dispatch system.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from models.enums import EquipmentType, EquipmentStatus, TaskType, TaskStatus


class Equipment(BaseModel):
    """
    Equipment model

    Describe the attribute information of port operation equipment (shore bridge, field bridge, set card, etc.).

    Attributes:
        equip_id: Device unique identifier, the format is prefix + 2 digits
                  Prefix: QC (shore bridge), RTG (tire crane), RMG (track crane), YT (card collection), RS (front crane), TL (top crane)
        equip_type: Equipment type
        equip_name: Device name
        status: Device status, default IDLE
        current_task: Current task ID, optional
        berth_id: Belonging berth ID (for shore bridge only), optional
        block_id: The ID of the box area (for field bridge only), optional
        current_location: Current location (for card collection only), optional
        efficiency_rate: Efficiency coefficient (box/hour), range 1-60, default25
    """

    equip_id: str = Field(
        ...,
        pattern=r"^(QC|RTG|RMG|YT|RS|TL)\d{2}$",
        description="Device unique identifier, prefix (QC/RTG/RMG/YT/RS/TL) + 2 digits",
        examples=["QC01", "RTG05", "YT12"],
    )
    equip_type: EquipmentType = Field(
        ...,
        description="Equipment type",
    )
    equip_name: str = Field(
        ...,
        description="Device name",
    )
    status: EquipmentStatus = Field(
        default=EquipmentStatus.IDLE,
        description="Equipment status",
    )
    current_task: Optional[str] = Field(
        default=None,
        description="Current taskID",
    )
    berth_id: Optional[str] = Field(
        default=None,
        description="The berth belonging to the shore bridgeID",
    )
    block_id: Optional[str] = Field(
        default=None,
        description="The box area where the field bridge is locatedID",
    )
    current_location: Optional[str] = Field(
        default=None,
        description="The current location of the collection card",
    )
    efficiency_rate: int = Field(
        default=25,
        ge=1,
        le=60,
        description="Efficiency coefficient (box/hour), range1-60",
    )

    @field_validator("equip_id")
    @classmethod
    def validate_equip_id(cls, v: str) -> str:
        """Verify the device ID format"""
        if not re.match(r"^(QC|RTG|RMG|YT|RS|TL)\d{2}$", v):
            raise ValueError(
                f"The device ID format is invalid: {v}, which must be QC/RTG/RMG/YT/RS/TL followed by 2 digits (such as QC01, RTG05)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "equip_id": "QC01",
                    "equip_type": "quay_crane",
                    "equip_name": "No.1 Shore Bridge",
                    "status": "idle",
                    "current_task": None,
                    "berth_id": "B01",
                    "block_id": None,
                    "current_location": None,
                    "efficiency_rate": 25,
                },
                {
                    "equip_id": "RTG05",
                    "equip_type": "rtg",
                    "equip_name": "No. 5 tire crane",
                    "status": "working",
                    "current_task": "T0012",
                    "berth_id": None,
                    "block_id": "A01",
                    "current_location": None,
                    "efficiency_rate": 20,
                },
                {
                    "equip_id": "YT12",
                    "equip_type": "yard_truck",
                    "equip_name": "No. 12 collection card",
                    "status": "moving",
                    "current_task": "T0015",
                    "berth_id": None,
                    "block_id": None,
                    "current_location": "A01Ou",
                    "efficiency_rate": 30,
                },
            ]
        }
    }


class Task(BaseModel):
    """
    Task model

    Describe the attribute information of the port operation task.

    Attributes:
        task_id: The unique identifier of the task, the format is T followed by a 4-digit number (such as T0001)
        task_type: Task type
        status: Task status, default PENDING
        equip_id: Assigned device ID, optional
        container_id: Container ID, optional
        vessel_id: Ship ID, optional
        source_location: Starting position, optional
        target_location: Target position, optional
        created_at: Creation time (ISO 8601 format), optional
        estimated_duration: The estimated duration (minutes) must be greater than 0, default30
    """

    task_id: str = Field(
        ...,
        pattern=r"^T\d{4}$",
        description="The unique identifier of the task, the format is T followed by 4 digits.",
        examples=["T0001", "T0123", "T9999"],
    )
    task_type: TaskType = Field(
        ...,
        description="Task type",
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Task status",
    )
    equip_id: Optional[str] = Field(
        default=None,
        description="Assigned equipmentID",
    )
    container_id: Optional[str] = Field(
        default=None,
        description="ContainerID",
    )
    vessel_id: Optional[str] = Field(
        default=None,
        description="ShippingID",
    )
    source_location: Optional[str] = Field(
        default=None,
        description="Starting position",
    )
    target_location: Optional[str] = Field(
        default=None,
        description="Target position",
    )
    created_at: Optional[str] = Field(
        default=None,
        description="Creation time (ISO 8601 format)",
    )
    estimated_duration: int = Field(
        default=30,
        gt=0,
        description="Estimated duration (minutes)",
    )

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: str) -> str:
        """Verify the task ID format"""
        if not re.match(r"^T\d{4}$", v):
            raise ValueError(
                f"The task ID format is invalid: {v}, which must be followed by T and 4 digits (such as T0001, T9999)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "T0001",
                    "task_type": "discharge",
                    "status": "assigned",
                    "equip_id": "QC01",
                    "container_id": "C001234",
                    "vessel_id": "V001",
                    "source_location": "On the boatBAY12",
                    "target_location": "A01-01-01-01",
                    "created_at": "2024-01-15T10:30:00",
                    "estimated_duration": 45,
                },
                {
                    "task_id": "T0012",
                    "task_type": "yard_move",
                    "status": "in_progress",
                    "equip_id": "RTG05",
                    "container_id": "C005678",
                    "vessel_id": None,
                    "source_location": "A01-02-03-04",
                    "target_location": "B02-01-01-01",
                    "created_at": "2024-01-15T14:00:00",
                    "estimated_duration": 15,
                },
            ]
        }
    }


__all__ = ["Equipment", "Task"]
