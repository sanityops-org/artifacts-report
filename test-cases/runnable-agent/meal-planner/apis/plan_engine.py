"""
Plan engine: meal-plan assembly and shopping-list rollup.
"""

from typing import Any

from models import MealPlan, Recipe


def scale_ingredients(recipe: Recipe, servings: int) -> list[dict[str, Any]]:
    """
    Scale a recipe's ingredients to a serving count.

    Quantities are written for `recipe.servings`, so a plan entry asking for a
    different number scales proportionally rather than reusing the written values.

    Args:
        recipe: Source recipe
        servings: Servings actually wanted

    Returns:
        Ingredient dicts with scaled quantities rounded to one decimal place
    """
    factor = servings / recipe.servings

    scaled = []
    for ingredient in recipe.ingredients:
        entry = ingredient.model_dump(mode="json")
        entry["quantity"] = round(ingredient.quantity * factor, 1)
        scaled.append(entry)

    return scaled


def build_shopping_list(plan: MealPlan, recipes: list[Recipe]) -> dict[str, Any]:
    """
    Roll a meal plan up into a single shopping list.

    The same ingredient in the same unit across multiple entries is summed into
    one line. Entries whose recipe is not in the catalog are reported under
    `unresolved` rather than being dropped silently.

    Args:
        plan: The meal plan
        recipes: Full catalog

    Returns:
        {"items": [...], "unresolved": [...], "entry_count": N}
    """
    catalog = {r.recipe_id: r for r in recipes}

    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    unresolved: list[dict[str, Any]] = []

    for entry in plan.entries:
        recipe = catalog.get(entry.recipe_id)
        if recipe is None:
            unresolved.append({
                "entry_id": entry.entry_id,
                "recipe_id": entry.recipe_id,
                "reason": "recipe not found in catalog"
            })
            continue

        for ingredient in scale_ingredients(recipe, entry.servings):
            key = (ingredient["name"].lower(), ingredient["unit"])
            if key in grouped:
                grouped[key]["quantity"] = round(
                    grouped[key]["quantity"] + ingredient["quantity"], 1
                )
            else:
                grouped[key] = {
                    "name": ingredient["name"],
                    "quantity": ingredient["quantity"],
                    "unit": ingredient["unit"],
                    "category": ingredient["category"],
                }

    items = sorted(grouped.values(), key=lambda i: (i["category"], i["name"]))

    return {
        "plan_id": plan.plan_id,
        "items": items,
        "item_count": len(items),
        "unresolved": unresolved,
        "entry_count": len(plan.entries),
    }


def plan_totals(plan: MealPlan, recipes: list[Recipe]) -> dict[str, Any]:
    """
    Total the estimated nutrition across a plan.

    Args:
        plan: The meal plan
        recipes: Full catalog

    Returns:
        {"calories": x, "protein_g": ..., "servings": N, "unresolved": [...]}
    """
    catalog = {r.recipe_id: r for r in recipes}

    totals = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0,
        "sodium_mg": 0.0,
    }
    servings_total = 0
    unresolved: list[dict[str, Any]] = []

    for entry in plan.entries:
        recipe = catalog.get(entry.recipe_id)
        if recipe is None:
            unresolved.append({"entry_id": entry.entry_id, "recipe_id": entry.recipe_id})
            continue

        nutrition = recipe.nutrition_per_serving
        for key in totals:
            totals[key] = round(totals[key] + getattr(nutrition, key) * entry.servings, 1)
        servings_total += entry.servings

    result: dict[str, Any] = dict(totals)
    result["servings"] = servings_total
    result["unresolved"] = unresolved

    return result


def plan_entries_with_recipes(plan: MealPlan, recipes: list[Recipe]) -> list[dict[str, Any]]:
    """
    Attach recipe names and times to each plan entry.

    Saves the model a second lookup per entry.
    """
    catalog = {r.recipe_id: r for r in recipes}

    enriched = []
    for entry in plan.entries:
        item = entry.model_dump(mode="json")
        recipe = catalog.get(entry.recipe_id)
        item["recipe_name"] = recipe.name if recipe else None
        item["total_minutes"] = (
            recipe.prep_minutes + recipe.cook_minutes if recipe else None
        )
        enriched.append(item)

    enriched.sort(key=lambda e: (e["day_index"], e["meal_type"], e["entry_id"]))

    return enriched


__all__ = ["scale_ingredients", "build_shopping_list", "plan_totals", "plan_entries_with_recipes"]
