"""
Recipe engine: search and filtering.

Pure functions — the caller injects the catalog, which keeps them directly
unit-testable without touching the filesystem.
"""

from models import Recipe
from models.enums import Cuisine, DietTag


def total_minutes(recipe: Recipe) -> int:
    """Total time from starting prep to serving"""
    return recipe.prep_minutes + recipe.cook_minutes


def search_recipes(
    recipes: list[Recipe],
    query: str | None = None,
    cuisine: str | None = None,
    diet: str | None = None,
    max_total_minutes: int | None = None,
    limit: int = 20
) -> list[Recipe]:
    """
    Search recipes by cuisine, diet tag, total time, and free-text query.

    An unparseable enum value is ignored rather than emptying the result set —
    the caller gets the result unfiltered on that axis, which is friendlier than
    a silent zero. Ordering is by total time ascending, then recipe_id.

    Args:
        recipes: Full catalog
        query: Substring matched against the recipe name and its ingredient names
        cuisine: Cuisine name
        diet: Diet tag name
        max_total_minutes: Upper bound on prep + cook time
        limit: Maximum results

    Returns:
        Matching recipes
    """
    results = list(recipes)

    if cuisine:
        try:
            cuisine_enum = Cuisine(cuisine.lower())
            results = [r for r in results if r.cuisine == cuisine_enum]
        except ValueError:
            pass

    if diet:
        try:
            diet_enum = DietTag(diet.lower())
            results = [r for r in results if diet_enum in r.diet_tags]
        except ValueError:
            pass

    if max_total_minutes is not None:
        results = [r for r in results if total_minutes(r) <= max_total_minutes]

    if query:
        needle = query.lower().strip()
        results = [
            r for r in results
            if needle in r.name.lower()
            or any(needle in i.name.lower() for i in r.ingredients)
        ]

    results.sort(key=lambda r: (total_minutes(r), r.recipe_id))

    return results[:limit]


def get_recipe_by_id(recipe_id: str, recipes: list[Recipe]) -> Recipe | None:
    """Get a recipe by its ID"""
    for recipe in recipes:
        if recipe.recipe_id == recipe_id:
            return recipe
    return None


def find_by_ingredient(ingredient_name: str, recipes: list[Recipe]) -> list[Recipe]:
    """
    Find recipes that use an ingredient.

    Case-insensitive substring match, so 'chicken' also finds 'chicken thigh'.
    Ordered by total time ascending, then recipe_id.
    """
    needle = ingredient_name.lower().strip()

    results = [
        r for r in recipes
        if any(needle in i.name.lower() for i in r.ingredients)
    ]

    results.sort(key=lambda r: (total_minutes(r), r.recipe_id))

    return results


__all__ = ["total_minutes", "search_recipes", "get_recipe_by_id", "find_by_ingredient"]
