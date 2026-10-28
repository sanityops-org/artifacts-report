"""
Nutrition models.

All figures are estimates from a simulated database, not measured values — see
boundary B3 in the design document.
"""

from pydantic import BaseModel, Field


class NutritionInfo(BaseModel):
    """Nutrition per serving"""
    calories: float = Field(..., ge=0, description="Kilocalories")
    protein_g: float = Field(..., ge=0, description="Protein in grams")
    carbs_g: float = Field(..., ge=0, description="Carbohydrate in grams")
    fat_g: float = Field(..., ge=0, description="Fat in grams")
    fiber_g: float = Field(..., ge=0, description="Fibre in grams")
    sodium_mg: float = Field(..., ge=0, description="Sodium in milligrams")


class NutritionTargets(BaseModel):
    """Daily nutrition targets used for comparison"""
    calories: float = Field(..., gt=0, description="Daily calorie target")
    protein_g: float = Field(..., gt=0, description="Daily protein target in grams")
    carbs_g: float = Field(..., gt=0, description="Daily carbohydrate target in grams")
    fat_g: float = Field(..., gt=0, description="Daily fat target in grams")
    fiber_g: float = Field(..., gt=0, description="Daily fibre target in grams")
    sodium_mg: float = Field(..., gt=0, description="Daily sodium target in milligrams")


__all__ = ["NutritionInfo", "NutritionTargets"]
