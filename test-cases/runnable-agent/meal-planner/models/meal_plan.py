"""
Meal plan models.
"""

from pydantic import BaseModel, Field

from models.enums import MealType


class PlanEntry(BaseModel):
    """A recipe assigned to a day and meal slot"""
    entry_id: str = Field(..., pattern=r"^ENTRY\d{4}$", description="Entry ID")
    day_index: int = Field(..., ge=1, le=14, description="Day number within the plan, 1-based")
    meal_type: MealType = Field(..., description="Meal slot")
    recipe_id: str = Field(..., pattern=r"^RECIPE\d{3}$", description="Recipe ID")
    servings: int = Field(..., ge=1, le=12, description="Servings planned for this slot")


class MealPlan(BaseModel):
    """Multi-day meal plan"""
    plan_id: str = Field(..., pattern=r"^PLAN\d{4}$", description="Plan ID")
    name: str = Field(..., min_length=2, max_length=100, description="Plan name")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    days: int = Field(..., ge=1, le=14, description="Number of days covered")
    entries: list[PlanEntry] = Field(default_factory=list, description="Planned meals")


__all__ = ["PlanEntry", "MealPlan"]
