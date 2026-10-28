"""
Field data model

Define the Pydantic model of YardBlock and Container for the container terminal scheduling system.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from models.enums import BlockStatus, ContainerType, ContainerSize


class YardBlock(BaseModel):
    """
    Stacking block model

    Describe the attribute information of the warehouse block, including the basic information, capacity, status, etc. of the block.

    Attributes:
        block_id: The unique identifier of the block, the format is 1 capital letter (A-F) + 2 digits (such as A01)
        block_name: Block name
        type: Types of containers stored in blocks
        capacity: The maximum capacity of the block (box position), range (0, 2000]
        occupied: The amount occupied, the default is0
        tiers_max: The maximum number of stacking layers, the range is [1, 9], the default is5
        status: Block status, default OPERATIONAL
    """

    block_id: str = Field(
        ...,
        pattern=r"^[A-F]\d{2}$",
        description="The unique identifier of the block, in the format of 1 capital letter (A-F) followed by 2 digits",
        examples=["A01", "B12", "F99"],
    )
    block_name: str = Field(
        ...,
        description="Block name",
    )
    type: ContainerType = Field(
        ...,
        description="Types of containers stored in blocks",
    )
    capacity: int = Field(
        ...,
        gt=0,
        le=2000,
        description="The maximum capacity of the block (box position), the maximum2000",
    )
    occupied: int = Field(
        default=0,
        ge=0,
        description="Occupied quantity",
    )
    tiers_max: int = Field(
        default=5,
        ge=1,
        le=9,
        description="Maximum number of stacking layers, range1-9",
    )
    status: BlockStatus = Field(
        default=BlockStatus.OPERATIONAL,
        description="Block status",
    )

    @field_validator("block_id")
    @classmethod
    def validate_block_id(cls, v: str) -> str:
        """Verify the block ID format"""
        if not re.match(r"^[A-F]\d{2}$", v):
            raise ValueError(
                f"The block ID format is invalid: {v}, which must be a capital letter between A-F followed by a 2-digit number (such as A01)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "block_id": "A01",
                    "block_name": "ADistrict No. 1 Import Box Store",
                    "type": "import",
                    "capacity": 1500,
                    "occupied": 850,
                    "tiers_max": 5,
                    "status": "operational",
                }
            ]
        }
    }


class Container(BaseModel):
    """
    Container model

    Describe the property information of the container, including the basic information, size, type, weight, location, etc. of the container.

    Attributes:
        container_id: Container unique identifier, ISO 6346 format (4 capital letters + 7 digits)
        size: Container size
        type: Container type
        weight: Container weight (tons), range [0, 40]
        vessel_id: Ship ID, optional
        block_id: The block ID of the warehouse where it is located is optional
        bay: Shell number, range [1, ∞), optional
        row: Row number, range [1, ∞), optional
        tier: Layer number, range [1, 9], optional
    """

    container_id: str = Field(
        ...,
        pattern=r"^[A-Z]{4}\d{7}$",
        description="Container unique identifier, ISO 6346 format (4 capital letters + 7 digits)",
        examples=["MSCU1234567", "CMAU9876543"],
    )
    size: ContainerSize = Field(
        ...,
        description="Container size",
    )
    type: ContainerType = Field(
        ...,
        description="Container type",
    )
    weight: float = Field(
        ...,
        ge=0,
        le=40,
        description="Container weight (tons), up to 40 tons",
    )
    vessel_id: Optional[str] = Field(
        default=None,
        description="The ship in which it is locatedID",
    )
    block_id: Optional[str] = Field(
        default=None,
        description="The block of the warehouse where it is locatedID",
    )
    bay: Optional[int] = Field(
        default=None,
        ge=1,
        description="Shell number",
    )
    row: Optional[int] = Field(
        default=None,
        ge=1,
        description="Arrange in numerical order",
    )
    tier: Optional[int] = Field(
        default=None,
        ge=1,
        le=9,
        description="Floor number, range1-9",
    )

    @field_validator("container_id")
    @classmethod
    def validate_container_id(cls, v: str) -> str:
        """Verify the container ID format (ISO 6346)"""
        if not re.match(r"^[A-Z]{4}\d{7}$", v):
            raise ValueError(
                f"The container ID format is invalid: {v}, which must be 4 capital letters followed by 7 digits (ISO 6346 format, such as MSCU1234567)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "container_id": "MSCU1234567",
                    "size": "40GP",
                    "type": "import",
                    "weight": 25.5,
                    "vessel_id": "V001",
                    "block_id": "A01",
                    "bay": 10,
                    "row": 6,
                    "tier": 4,
                }
            ]
        }
    }


__all__ = ["YardBlock", "Container"]
