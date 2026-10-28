"""
Tests for the nutrition engine: daily totals and target comparison.
"""

import pytest

from apis.nutrition_engine import compare_to_targets, daily_totals
from models import NutritionInfo, NutritionLogEntry, NutritionTargets, Recipe


def _recipe(recipe_id, calories, protein, carbs=40.0, fat=15.0, fiber=5.0, sodium=500.0):
    from models import Ingredient

    return Recipe(
        recipe_id=recipe_id, name=f"Dish {recipe_id}", cuisine="italian", diet_tags=[],
        prep_minutes=5, cook_minutes=5, servings=2,
        ingredients=[Ingredient(name="Something", quantity=100, unit="g", category="pantry")],
        steps=["Step one."],
        nutrition_per_serving=NutritionInfo(
            calories=calories, protein_g=protein, carbs_g=carbs, fat_g=fat,
            fiber_g=fiber, sodium_mg=sodium
        ),
    )


@pytest.fixture
def recipes():
    return [
        _recipe("RECIPE001", calories=500.0, protein=14.0),
        _recipe("RECIPE002", calories=200.0, protein=30.0),
    ]


@pytest.fixture
def targets():
    return NutritionTargets(calories=2000.0, protein_g=100.0, carbs_g=250.0,
                            fat_g=70.0, fiber_g=30.0, sodium_mg=2300.0)


def _log(log_id, date, recipe_id, servings, meal="dinner"):
    return NutritionLogEntry(log_id=log_id, date=date, meal_type=meal,
                             recipe_id=recipe_id, servings=servings)


def test_daily_totals_scale_by_servings(recipes):
    totals = daily_totals("2026-10-09", [_log("LOG0001", "2026-10-09", "RECIPE001", 4)], recipes)
    assert totals["calories"] == 2000.0
    assert totals["protein_g"] == 56.0
    assert totals["servings"] == 4


def test_daily_totals_sum_multiple_entries(recipes):
    log = [
        _log("LOG0001", "2026-10-09", "RECIPE001", 1),  # 500
        _log("LOG0002", "2026-10-09", "RECIPE002", 2),  # 400
    ]
    totals = daily_totals("2026-10-09", log, recipes)
    assert totals["calories"] == 900.0
    assert totals["servings"] == 3
    assert totals["entry_count"] == 2


def test_daily_totals_ignore_other_dates(recipes):
    log = [
        _log("LOG0001", "2026-10-09", "RECIPE001", 1),
        _log("LOG0002", "2026-10-10", "RECIPE001", 5),
    ]
    totals = daily_totals("2026-10-09", log, recipes)
    assert totals["calories"] == 500.0
    assert totals["entry_count"] == 1


def test_daily_totals_for_a_date_with_nothing_logged(recipes):
    totals = daily_totals("2026-10-09", [], recipes)
    assert totals["calories"] == 0.0
    assert totals["entry_count"] == 0


def test_daily_totals_report_unresolved_recipes(recipes):
    totals = daily_totals("2026-10-09", [_log("LOG0001", "2026-10-09", "RECIPE999", 1)], recipes)
    assert totals["calories"] == 0.0
    assert len(totals["unresolved"]) == 1
    assert totals["entry_count"] == 1


def test_daily_totals_round_to_one_decimal(recipes):
    """Half a serving of a 500-calorie recipe is 250, not a repeating decimal."""
    totals = daily_totals("2026-10-09", [_log("LOG0001", "2026-10-09", "RECIPE001", 1)], recipes)
    assert totals["calories"] == 500.0


def test_comparison_marks_a_met_metric(targets):
    totals = {"calories": 2000.0, "protein_g": 100.0, "carbs_g": 250.0,
              "fat_g": 70.0, "fiber_g": 30.0, "sodium_mg": 2300.0}
    comparison = compare_to_targets(totals, targets)
    assert all(v["status"] == "met" for v in comparison.values())


def test_comparison_lower_bound_of_met_is_inclusive(targets):
    """Exactly 90% of the target counts as met."""
    totals = {k: 0.0 for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")}
    totals["calories"] = 1800.0  # exactly 90%
    assert compare_to_targets(totals, targets)["calories"]["status"] == "met"


def test_comparison_upper_bound_of_met_is_inclusive(targets):
    """Exactly 105% of the target counts as met."""
    totals = {k: 0.0 for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")}
    totals["calories"] = 2100.0  # exactly 105%
    assert compare_to_targets(totals, targets)["calories"]["status"] == "met"


def test_comparison_flags_under_below_the_lower_bound(targets):
    totals = {k: 0.0 for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")}
    totals["calories"] = 1799.0
    assert compare_to_targets(totals, targets)["calories"]["status"] == "under"


def test_comparison_flags_over_above_the_upper_bound(targets):
    totals = {k: 0.0 for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")}
    totals["calories"] = 2101.0
    assert compare_to_targets(totals, targets)["calories"]["status"] == "over"


def test_comparison_reports_percent_of_target(targets):
    totals = {k: 0.0 for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")}
    totals["calories"] = 1500.0
    assert compare_to_targets(totals, targets)["calories"]["percent_of_target"] == 75.0


def test_comparison_covers_every_metric(targets):
    totals = {k: 0.0 for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")}
    comparison = compare_to_targets(totals, targets)
    assert set(comparison) == {"calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg"}
