"""
Tests for the Meal Planner domain models.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def _ingredient(**overrides):
    base = {"name": "Olive oil", "quantity": 2.0, "unit": "tbsp", "category": "pantry"}
    base.update(overrides)
    return base


def _nutrition(**overrides):
    base = {"calories": 400.0, "protein_g": 20.0, "carbs_g": 40.0,
            "fat_g": 15.0, "fiber_g": 5.0, "sodium_mg": 500.0}
    base.update(overrides)
    return base


def _recipe(**overrides):
    base = {
        "recipe_id": "RECIPE001", "name": "Test Dish", "cuisine": "italian",
        "diet_tags": ["vegetarian"], "prep_minutes": 10, "cook_minutes": 20,
        "servings": 4, "ingredients": [_ingredient()], "steps": ["Do the thing."],
        "nutrition_per_serving": _nutrition(),
    }
    base.update(overrides)
    return base


def test_recipe_requires_valid_id_pattern():
    from models import Recipe

    Recipe.model_validate(_recipe())

    with pytest.raises(ValidationError):
        Recipe.model_validate(_recipe(recipe_id="RECIPE1"))


def test_recipe_rejects_unknown_cuisine():
    from models import Recipe

    with pytest.raises(ValidationError):
        Recipe.model_validate(_recipe(cuisine="martian"))


def test_recipe_rejects_unknown_diet_tag():
    from models import Recipe

    with pytest.raises(ValidationError):
        Recipe.model_validate(_recipe(diet_tags=["keto"]))


def test_recipe_requires_at_least_one_ingredient_and_step():
    from models import Recipe

    with pytest.raises(ValidationError):
        Recipe.model_validate(_recipe(ingredients=[]))

    with pytest.raises(ValidationError):
        Recipe.model_validate(_recipe(steps=[]))


def test_ingredient_quantity_must_be_positive():
    from models import Ingredient

    with pytest.raises(ValidationError):
        Ingredient(name="Garlic", quantity=0, unit="clove", category="produce")

    with pytest.raises(ValidationError):
        Ingredient(name="Garlic", quantity=-3, unit="clove", category="produce")


def test_nutrition_rejects_negative_values():
    from models import NutritionInfo

    with pytest.raises(ValidationError):
        NutritionInfo(calories=-1, protein_g=1, carbs_g=1, fat_g=1, fiber_g=1, sodium_mg=1)


def test_plan_entry_day_index_bounds():
    from models import PlanEntry

    PlanEntry(entry_id="ENTRY0001", day_index=1, meal_type="dinner",
              recipe_id="RECIPE001", servings=2)

    with pytest.raises(ValidationError):
        PlanEntry(entry_id="ENTRY0001", day_index=0, meal_type="dinner",
                  recipe_id="RECIPE001", servings=2)


def test_meal_plan_day_bounds():
    from models import MealPlan

    MealPlan(plan_id="PLAN0001", name="Test", start_date="2026-10-09", days=14)

    with pytest.raises(ValidationError):
        MealPlan(plan_id="PLAN0001", name="Test", start_date="2026-10-09", days=15)


def test_nutrition_log_servings_must_be_positive():
    from models import NutritionLogEntry

    with pytest.raises(ValidationError):
        NutritionLogEntry(log_id="LOG0001", date="2026-10-09", meal_type="lunch",
                          recipe_id="RECIPE001", servings=0)


def test_nutrition_targets_must_be_positive():
    from models import NutritionTargets

    with pytest.raises(ValidationError):
        NutritionTargets(calories=0, protein_g=1, carbs_g=1, fat_g=1, fiber_g=1, sodium_mg=1)


@pytest.mark.parametrize("filename,key,model_name", [
    ("recipes.json", "recipes", "Recipe"),
    ("meal_plans.json", "meal_plans", "MealPlan"),
    ("nutrition_log.json", "nutrition_log", "NutritionLogEntry"),
])
def test_shipped_data_files_validate_against_models(filename, key, model_name):
    """Every row in data/ must satisfy its model — guards against enum drift."""
    import models

    model = getattr(models, model_name)
    payload = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))

    for row in payload[key]:
        model.model_validate(row)


def test_nutrition_targets_file_validates():
    from models import NutritionTargets

    payload = json.loads((DATA_DIR / "nutrition_targets.json").read_text(encoding="utf-8"))
    NutritionTargets.model_validate(payload["nutrition_targets"])


def test_catalog_ships_twelve_recipes():
    recipes = json.loads((DATA_DIR / "recipes.json").read_text(encoding="utf-8"))["recipes"]
    assert len(recipes) == 12


def test_recipe_ids_are_unique():
    recipes = json.loads((DATA_DIR / "recipes.json").read_text(encoding="utf-8"))["recipes"]
    ids = [r["recipe_id"] for r in recipes]
    assert len(ids) == len(set(ids))


def test_seeded_plan_references_known_recipes():
    recipes = json.loads((DATA_DIR / "recipes.json").read_text(encoding="utf-8"))["recipes"]
    plans = json.loads((DATA_DIR / "meal_plans.json").read_text(encoding="utf-8"))["meal_plans"]

    known = {r["recipe_id"] for r in recipes}
    for plan in plans:
        for entry in plan["entries"]:
            assert entry["recipe_id"] in known, f"{entry['entry_id']} references an unknown recipe"


def test_seeded_plan_entries_fall_inside_the_plan_length():
    plans = json.loads((DATA_DIR / "meal_plans.json").read_text(encoding="utf-8"))["meal_plans"]

    for plan in plans:
        for entry in plan["entries"]:
            assert 1 <= entry["day_index"] <= plan["days"], (
                f"{entry['entry_id']} falls outside its plan's {plan['days']} day(s)"
            )


def test_every_cuisine_and_diet_tag_is_exercised_by_the_catalog():
    """A catalogue that never uses a value leaves the filters untested in practice."""
    from models.enums import Cuisine, DietTag

    recipes = json.loads((DATA_DIR / "recipes.json").read_text(encoding="utf-8"))["recipes"]

    used_cuisines = {r["cuisine"] for r in recipes}
    used_diets = {tag for r in recipes for tag in r["diet_tags"]}

    assert used_cuisines == {c.value for c in Cuisine}
    assert used_diets == {d.value for d in DietTag}
