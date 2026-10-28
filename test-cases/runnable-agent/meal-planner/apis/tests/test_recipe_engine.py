"""
Tests for the recipe engine.
"""

import pytest

from apis.recipe_engine import find_by_ingredient, get_recipe_by_id, search_recipes, total_minutes
from models import Ingredient, NutritionInfo, Recipe


def _recipe(recipe_id, name, cuisine, diet_tags, prep, cook, ingredients, servings=4):
    return Recipe(
        recipe_id=recipe_id, name=name, cuisine=cuisine, diet_tags=diet_tags,
        prep_minutes=prep, cook_minutes=cook, servings=servings,
        ingredients=[Ingredient(name=n, quantity=q, unit="g", category="produce")
                     for n, q in ingredients],
        steps=["Step one."],
        nutrition_per_serving=NutritionInfo(
            calories=400, protein_g=20, carbs_g=40, fat_g=15, fiber_g=5, sodium_mg=500
        ),
    )


@pytest.fixture
def recipes():
    return [
        _recipe("RECIPE001", "Quick Pasta", "italian", ["vegetarian"],
                10, 15, [("Pasta", 400), ("Garlic", 6)]),
        _recipe("RECIPE002", "Slow Roast Chicken", "american", ["high_protein"],
                30, 90, [("Chicken thigh", 800), ("Garlic", 4)]),
        _recipe("RECIPE003", "Fresh Salad", "mediterranean", ["vegan", "gluten_free"],
                15, 0, [("Cucumber", 2), ("Tomatoes", 300)]),
    ]


def test_total_minutes_adds_prep_and_cook(recipes):
    assert total_minutes(recipes[0]) == 25
    assert total_minutes(recipes[1]) == 120


def test_search_with_no_filters_returns_whole_catalog(recipes):
    assert len(search_recipes(recipes)) == 3


def test_search_orders_by_total_time_then_id(recipes):
    result = search_recipes(recipes)
    assert [r.recipe_id for r in result] == ["RECIPE003", "RECIPE001", "RECIPE002"]


def test_search_by_cuisine(recipes):
    result = search_recipes(recipes, cuisine="italian")
    assert [r.recipe_id for r in result] == ["RECIPE001"]


def test_search_by_diet_tag(recipes):
    result = search_recipes(recipes, diet="gluten_free")
    assert [r.recipe_id for r in result] == ["RECIPE003"]


def test_search_by_max_total_minutes_is_inclusive(recipes):
    """25 minutes must include the 25-minute recipe."""
    result = search_recipes(recipes, max_total_minutes=25)
    assert [r.recipe_id for r in result] == ["RECIPE003", "RECIPE001"]


def test_search_query_matches_recipe_name(recipes):
    result = search_recipes(recipes, query="salad")
    assert [r.recipe_id for r in result] == ["RECIPE003"]


def test_search_query_matches_ingredient_name(recipes):
    """'chicken' should find the recipe even though the name is 'Slow Roast Chicken'... and
    also the one whose ingredient is chicken thigh."""
    result = search_recipes(recipes, query="chicken")
    assert [r.recipe_id for r in result] == ["RECIPE002"]


def test_search_query_is_case_insensitive(recipes):
    assert len(search_recipes(recipes, query="GARLIC")) == 2  # matches ingredient names


def test_search_combines_filters(recipes):
    assert search_recipes(recipes, cuisine="italian", diet="vegan") == []


def test_search_with_unknown_cuisine_is_ignored(recipes):
    """An unparseable enum value must not silently empty the result set."""
    assert len(search_recipes(recipes, cuisine="martian")) == 3


def test_search_with_unknown_diet_is_ignored(recipes):
    assert len(search_recipes(recipes, diet="keto")) == 3


def test_search_respects_limit(recipes):
    assert len(search_recipes(recipes, limit=2)) == 2


def test_get_recipe_by_id(recipes):
    assert get_recipe_by_id("RECIPE002", recipes).name == "Slow Roast Chicken"
    assert get_recipe_by_id("RECIPE999", recipes) is None


def test_find_by_ingredient_matches_substrings(recipes):
    """'chicken' should find 'Chicken thigh'."""
    result = find_by_ingredient("chicken", recipes)
    assert [r.recipe_id for r in result] == ["RECIPE002"]


def test_find_by_ingredient_is_case_insensitive(recipes):
    assert len(find_by_ingredient("GARLIC", recipes)) == 2


def test_find_by_ingredient_orders_by_total_time(recipes):
    result = find_by_ingredient("garlic", recipes)
    assert [r.recipe_id for r in result] == ["RECIPE001", "RECIPE002"]


def test_find_by_ingredient_with_no_match(recipes):
    assert find_by_ingredient("truffle", recipes) == []
