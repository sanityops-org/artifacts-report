"""
Recipe model.
"""

from pydantic import BaseModel, Field

from models.enums import Cuisine, DietTag
from models.ingredient import Ingredient
from models.nutrition import NutritionInfo


class Recipe(BaseModel):
    """Recipe model"""
    recipe_id: str = Field(..., pattern=r"^RECIPE\d{3}$", description="Recipe ID")
    name: str = Field(..., min_length=2, max_length=100, description="Recipe name")
    cuisine: Cuisine = Field(..., description="Cuisine")
    diet_tags: list[DietTag] = Field(default_factory=list, description="Dietary labels")
    prep_minutes: int = Field(..., ge=0, le=600, description="Preparation time in minutes")
    cook_minutes: int = Field(..., ge=0, le=600, description="Cooking time in minutes")
    servings: int = Field(..., ge=1, le=12, description="Servings the quantities are written for")
    ingredients: list[Ingredient] = Field(..., min_length=1, description="Ingredient list")
    steps: list[str] = Field(..., min_length=1, description="Preparation steps")
    nutrition_per_serving: NutritionInfo = Field(..., description="Estimated nutrition per serving")


__all__ = ["Recipe"]
