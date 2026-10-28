"""Cargo model for freight logistics."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from models.enums import CargoCategory


class Cargo(BaseModel):
    """Cargo specification model."""
    cargo_type: str = Field(..., description="Cargo type identifier")
    category: CargoCategory = Field(..., description="Cargo category")
    description: Optional[str] = Field(None, description="Cargo description")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    volume_cbm: Optional[float] = Field(None, ge=0, description="Volume in cubic meters")
    length_m: Optional[float] = Field(None, ge=0, description="Length in meters")
    width_m: Optional[float] = Field(None, ge=0, description="Width in meters")
    height_m: Optional[float] = Field(None, ge=0, description="Height in meters")
    hazardous_class: Optional[str] = Field(None, description="UN hazard class if applicable")
    temperature_min: Optional[float] = Field(None, description="Min temperature for reefer cargo")
    temperature_max: Optional[float] = Field(None, description="Max temperature for reefer cargo")
    stackable: bool = Field(True, description="Whether cargo can be stacked")
    fragile: bool = Field(False, description="Whether cargo is fragile")


class CargoType(BaseModel):
    """Cargo type definition with restrictions."""
    type_id: str = Field(..., description="Cargo type ID")
    name: str = Field(..., description="Display name")
    category: CargoCategory = Field(..., description="Category")
    max_weight_kg: float = Field(28000, description="Maximum weight per unit")
    max_volume_cbm: float = Field(80, description="Maximum volume per unit")
    requires_doc: bool = Field(False, description="Requires special documentation")
    hazmat_required: bool = Field(False, description="Requires hazmat certification")