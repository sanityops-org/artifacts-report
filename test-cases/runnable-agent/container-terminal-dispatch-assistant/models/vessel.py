"""
Ship and berth data model

The Pydantic model that defines the vessel (Vessel) and berth (Berth) is used for the container terminal dispatching system.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from models.enums import VesselStatus, BerthStatus


class Vessel(BaseModel):
    """
    Ship model

    Describe the attribute information of container ships, including the basic information, status, operation data, etc. of the ship.

    Attributes:
        vessel_id: The unique identifier of the ship, in the format of V followed by a 3-digit number (such as V001)
        vessel_name: Ship name, 2-50 characters
        vessel_type: Ship type, the default is container_ship
        length: Ship length (meters), range (0, 400]
        draft: Ship's tap depth (meters), range (0, 20]
        eta: Estimated arrival time (ISO 8601 format)
        etd: Estimated departure time (ISO 8601 format), optional
        status: Ship status, default INBOUND
        assigned_berth: The assigned berth ID is optional
        container_count: The total number of containers
        inbound_containers: The number of imported containers
        outbound_containers: The number of export containers
    """

    vessel_id: str = Field(
        ...,
        pattern=r"^V\d{3}$",
        description="The unique identifier of the ship, the format is V followed by 3 digits.",
        examples=["V001", "V123", "V999"],
    )
    vessel_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name of the ship",
    )
    vessel_type: str = Field(
        default="container_ship",
        description="Type of ship",
    )
    length: float = Field(
        ...,
        gt=0,
        le=400,
        description="The length of the ship (meters), the maximum is 400 meters",
    )
    draft: float = Field(
        ...,
        gt=0,
        le=20,
        description="Ship's dept depth (meters), up to 20 meters",
    )
    eta: str = Field(
        ...,
        description="Estimated arrival time (ISO 8601 format)",
    )
    etd: Optional[str] = Field(
        default=None,
        description="Estimated departure time (ISO 8601 format)",
    )
    status: VesselStatus = Field(
        default=VesselStatus.INBOUND,
        description="Ship status",
    )
    assigned_berth: Optional[str] = Field(
        default=None,
        description="Allocated berthID",
    )
    container_count: int = Field(
        ...,
        ge=0,
        description="The total number of containers",
    )
    inbound_containers: int = Field(
        ...,
        ge=0,
        description="The number of imported containers",
    )
    outbound_containers: int = Field(
        ...,
        ge=0,
        description="The number of export containers",
    )

    @field_validator("vessel_id")
    @classmethod
    def validate_vessel_id(cls, v: str) -> str:
        """Verify the ship ID format"""
        if not re.match(r"^V\d{3}$", v):
            raise ValueError(
                f"The ship ID format is invalid: {v}, which must be followed by V and 3 digits (such as V001)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "vessel_id": "V001",
                    "vessel_name": "Pacific Star",
                    "vessel_type": "container_ship",
                    "length": 300.5,
                    "draft": 12.5,
                    "eta": "2024-01-15T08:00:00",
                    "etd": "2024-01-16T18:00:00",
                    "status": "inbound",
                    "assigned_berth": "B01",
                    "container_count": 5000,
                    "inbound_containers": 2500,
                    "outbound_containers": 2500,
                }
            ]
        }
    }


class Berth(BaseModel):
    """
    Berth model

    Describe the attribute information of the port berth, including the basic information of the berth, status, operation status, etc.

    Attributes:
        berth_id: The unique identifier of the berth, the format is B followed by 2 digits (such as B01)
        berth_name: The name of the berth
        length: The length of the berth (meters) must be greater than0
        max_draft: The maximum berth depth (meters) must be greater than0
        status: Parking status, default AVAILABLE
        current_vessel: The currently docked ship ID can be selected
        available_from: Available time (ISO 8601 format), optional
    """

    berth_id: str = Field(
        ...,
        pattern=r"^B\d{2}$",
        description="The unique identifier of the berth, the format is B followed by a 2-digit number.",
        examples=["B01", "B12", "B99"],
    )
    berth_name: str = Field(
        ...,
        description="The name of the berth",
    )
    length: float = Field(
        ...,
        gt=0,
        description="The length of the berth (meters)",
    )
    max_draft: float = Field(
        ...,
        gt=0,
        description="The maximum berth's top depth (meters)",
    )
    status: BerthStatus = Field(
        default=BerthStatus.AVAILABLE,
        description="Berth status",
    )
    current_vessel: Optional[str] = Field(
        default=None,
        description="Ships currently dockedID",
    )
    available_from: Optional[str] = Field(
        default=None,
        description="Available time (ISO 8601 format)",
    )

    @field_validator("berth_id")
    @classmethod
    def validate_berth_id(cls, v: str) -> str:
        """Verify the berth ID format"""
        if not re.match(r"^B\d{2}$", v):
            raise ValueError(
                f"The berth ID format is invalid: {v}, which must be B followed by 2 digits (such as B01)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "berth_id": "B01",
                    "berth_name": "No.1 berth",
                    "length": 350.0,
                    "max_draft": 16.0,
                    "status": "available",
                    "current_vessel": None,
                    "available_from": None,
                }
            ]
        }
    }


__all__ = ["Vessel", "Berth"]
