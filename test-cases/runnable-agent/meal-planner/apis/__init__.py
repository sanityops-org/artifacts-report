"""
Meal Planner API layer.
"""

from apis.data_store import DataStore, get_data_store, reset_data_store
from apis.nutrition_engine import compare_to_targets, daily_totals
from apis.plan_engine import (
    build_shopping_list,
    plan_entries_with_recipes,
    plan_totals,
    scale_ingredients,
)
from apis.recipe_engine import find_by_ingredient, get_recipe_by_id, search_recipes, total_minutes

__all__ = [
    "DataStore",
    "get_data_store",
    "reset_data_store",
    "total_minutes",
    "search_recipes",
    "get_recipe_by_id",
    "find_by_ingredient",
    "scale_ingredients",
    "build_shopping_list",
    "plan_totals",
    "plan_entries_with_recipes",
    "daily_totals",
    "compare_to_targets",
]
