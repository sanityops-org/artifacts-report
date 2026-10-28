"""
Tests for the plan engine: serving scaling, shopping-list rollup, and totals.
"""

import pytest

from apis.plan_engine import (
    build_shopping_list,
    plan_entries_with_recipes,
    plan_totals,
    scale_ingredients,
)
from models import Ingredient, MealPlan, NutritionInfo, PlanEntry, Recipe


def _recipe(recipe_id, name, servings, ingredients, calories=400.0, protein=20.0):
    return Recipe(
        recipe_id=recipe_id, name=name, cuisine="italian", diet_tags=[],
        prep_minutes=10, cook_minutes=10, servings=servings,
        ingredients=[
            Ingredient(name=n, quantity=q, unit=u, category=c) for n, q, u, c in ingredients
        ],
        steps=["Step one."],
        nutrition_per_serving=NutritionInfo(
            calories=calories, protein_g=protein, carbs_g=40.0, fat_g=15.0,
            fiber_g=5.0, sodium_mg=500.0
        ),
    )


@pytest.fixture
def recipes():
    return [
        _recipe("RECIPE001", "Pasta", servings=4, ingredients=[
            ("Pasta", 400.0, "g", "grain"),
            ("Olive oil", 6.0, "tbsp", "pantry"),
        ], calories=500.0, protein=14.0),
        _recipe("RECIPE002", "Salmon", servings=2, ingredients=[
            ("Salmon fillet", 400.0, "g", "protein"),
            ("Olive oil", 2.0, "tbsp", "pantry"),
            ("Lemon", 1.0, "piece", "produce"),
        ], calories=520.0, protein=45.0),
    ]


def _plan(entries):
    return MealPlan(plan_id="PLAN0001", name="Test", start_date="2026-10-09", days=3, entries=entries)


def _entry(entry_id, recipe_id, servings, day=1, meal="dinner"):
    return PlanEntry(entry_id=entry_id, day_index=day, meal_type=meal,
                     recipe_id=recipe_id, servings=servings)


def test_scale_ingredients_at_matching_servings_is_unchanged(recipes):
    scaled = scale_ingredients(recipes[0], servings=4)
    assert [i["quantity"] for i in scaled] == [400.0, 6.0]


def test_scale_ingredients_halves_at_half_servings(recipes):
    scaled = scale_ingredients(recipes[0], servings=2)
    assert [i["quantity"] for i in scaled] == [200.0, 3.0]


def test_scale_ingredients_doubles_at_double_servings(recipes):
    scaled = scale_ingredients(recipes[1], servings=4)
    assert [i["quantity"] for i in scaled] == [800.0, 4.0, 2.0]


def test_scale_ingredients_preserves_unit_and_category(recipes):
    scaled = scale_ingredients(recipes[1], servings=1)
    assert scaled[0]["unit"] == "g"
    assert scaled[0]["category"] == "protein"
    assert scaled[0]["name"] == "Salmon fillet"


def test_shopping_list_sums_the_same_ingredient_and_unit(recipes):
    """Two recipes both use olive oil in tbsp — they must merge into one line."""
    plan = _plan([
        _entry("ENTRY0001", "RECIPE001", servings=4),   # 6 tbsp
        _entry("ENTRY0002", "RECIPE002", servings=2),   # 2 tbsp
    ])

    result = build_shopping_list(plan, recipes)
    olive_oil = [i for i in result["items"] if i["name"] == "Olive oil"]

    assert len(olive_oil) == 1
    assert olive_oil[0]["quantity"] == 8.0


def test_shopping_list_scales_before_summing(recipes):
    """A 4-serving entry of a 2-serving recipe contributes double."""
    plan = _plan([_entry("ENTRY0001", "RECIPE002", servings=4)])  # factor 2

    result = build_shopping_list(plan, recipes)
    quantities = {i["name"]: i["quantity"] for i in result["items"]}

    assert quantities["Salmon fillet"] == 800.0
    assert quantities["Olive oil"] == 4.0
    assert quantities["Lemon"] == 2.0


def test_shopping_list_groups_by_category_then_name(recipes):
    plan = _plan([
        _entry("ENTRY0001", "RECIPE001", servings=4),
        _entry("ENTRY0002", "RECIPE002", servings=2),
    ])

    result = build_shopping_list(plan, recipes)
    keys = [(i["category"], i["name"]) for i in result["items"]]
    assert keys == sorted(keys)


def test_shopping_list_reports_counts(recipes):
    plan = _plan([
        _entry("ENTRY0001", "RECIPE001", servings=4),
        _entry("ENTRY0002", "RECIPE002", servings=2),
    ])

    result = build_shopping_list(plan, recipes)
    assert result["entry_count"] == 2
    assert result["item_count"] == len(result["items"])
    assert result["plan_id"] == "PLAN0001"


def test_shopping_list_reports_unresolved_recipes_instead_of_dropping_them(recipes):
    plan = _plan([
        _entry("ENTRY0001", "RECIPE001", servings=4),
        _entry("ENTRY0002", "RECIPE999", servings=2),
    ])

    result = build_shopping_list(plan, recipes)
    assert len(result["unresolved"]) == 1
    assert result["unresolved"][0]["recipe_id"] == "RECIPE999"
    assert result["entry_count"] == 2


def test_shopping_list_for_an_empty_plan_is_empty(recipes):
    result = build_shopping_list(_plan([]), recipes)
    assert result["items"] == []
    assert result["item_count"] == 0


def test_plan_totals_scale_by_servings(recipes):
    plan = _plan([_entry("ENTRY0001", "RECIPE001", servings=4)])  # 500 x 4

    totals = plan_totals(plan, recipes)
    assert totals["calories"] == 2000.0
    assert totals["protein_g"] == 56.0
    assert totals["servings"] == 4


def test_plan_totals_sum_across_entries(recipes):
    plan = _plan([
        _entry("ENTRY0001", "RECIPE001", servings=2),   # 500 x 2 = 1000
        _entry("ENTRY0002", "RECIPE002", servings=4),   # 520 x 4 = 2080
    ])

    totals = plan_totals(plan, recipes)
    assert totals["calories"] == 3080.0
    assert totals["servings"] == 6


def test_plan_totals_reports_unresolved(recipes):
    plan = _plan([_entry("ENTRY0001", "RECIPE999", servings=1)])

    totals = plan_totals(plan, recipes)
    assert totals["calories"] == 0.0
    assert len(totals["unresolved"]) == 1


def test_plan_entries_are_enriched_and_ordered(recipes):
    plan = _plan([
        _entry("ENTRY0002", "RECIPE002", servings=2, day=2, meal="dinner"),
        _entry("ENTRY0001", "RECIPE001", servings=4, day=1, meal="lunch"),
    ])

    entries = plan_entries_with_recipes(plan, recipes)
    assert [e["entry_id"] for e in entries] == ["ENTRY0001", "ENTRY0002"]
    assert entries[0]["recipe_name"] == "Pasta"
    assert entries[0]["total_minutes"] == 20


def test_plan_entries_mark_a_missing_recipe_as_none(recipes):
    plan = _plan([_entry("ENTRY0001", "RECIPE999", servings=1)])

    entries = plan_entries_with_recipes(plan, recipes)
    assert entries[0]["recipe_name"] is None
    assert entries[0]["total_minutes"] is None
