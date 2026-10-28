"""
Nutrition log model.
"""

from pydantic import BaseModel, Field

from models.enums import MealType


class NutritionLogEntry(BaseModel):
    """A meal eaten on a given date"""
    log_id: str = Field(..., pattern=r"^LOG\d{4}$", description="Log entry ID")
    date: str = Field(..., description="Date eaten (YYYY-MM-DD)")
    meal_type: MealType = Field(..., description="Meal slot")
    recipe_id: str = Field(..., pattern=r"^RECIPE\d{3}$", description="Recipe ID")
    servings: int = Field(..., ge=1, le=12, description="Servings eaten")


__all__ = ["NutritionLogEntry"]
