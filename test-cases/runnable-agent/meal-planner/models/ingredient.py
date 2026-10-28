"""
Ingredient model.
"""

from pydantic import BaseModel, Field

from models.enums import IngredientCategory, Unit


class Ingredient(BaseModel):
    """Recipe ingredient"""
    name: str = Field(..., min_length=2, max_length=60, description="Ingredient name")
    quantity: float = Field(..., gt=0, description="Quantity for the recipe's default servings")
    unit: Unit = Field(..., description="Measurement unit")
    category: IngredientCategory = Field(..., description="Shopping aisle category")


__all__ = ["Ingredient"]
