"""
Nutrition engine: daily totals and comparison against targets.
"""

from typing import Any

from models import NutritionLogEntry, NutritionTargets, Recipe
from models.enums import TargetStatus

METRICS = ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sodium_mg")

# A value counts as meeting its target within this band around the target
_MET_LOWER = 0.9
_MET_UPPER = 1.05


def daily_totals(
    target_date: str,
    log_entries: list[NutritionLogEntry],
    recipes: list[Recipe]
) -> dict[str, Any]:
    """
    Total the estimated nutrition logged on a date.

    Args:
        target_date: Date in YYYY-MM-DD form
        log_entries: All log entries
        recipes: Full catalog

    Returns:
        Metric totals plus servings eaten and any entries whose recipe is missing
    """
    catalog = {r.recipe_id: r for r in recipes}

    totals = {metric: 0.0 for metric in METRICS}
    servings_total = 0
    unresolved: list[dict[str, Any]] = []
    matched = 0

    for entry in log_entries:
        if entry.date != target_date:
            continue

        matched += 1

        recipe = catalog.get(entry.recipe_id)
        if recipe is None:
            unresolved.append({"log_id": entry.log_id, "recipe_id": entry.recipe_id})
            continue

        nutrition = recipe.nutrition_per_serving
        for metric in METRICS:
            totals[metric] = round(totals[metric] + getattr(nutrition, metric) * entry.servings, 1)
        servings_total += entry.servings

    result: dict[str, Any] = dict(totals)
    result["servings"] = servings_total
    result["entry_count"] = matched
    result["unresolved"] = unresolved

    return result


def compare_to_targets(
    totals: dict[str, Any],
    targets: NutritionTargets
) -> dict[str, Any]:
    """
    Compare totals against daily targets.

    A metric is `met` when the total falls between 90% and 105% of the target
    inclusive, otherwise `under` or `over`.

    Args:
        totals: Output of daily_totals
        targets: Daily targets

    Returns:
        Per-metric comparison with target, actual, and status
    """
    comparison: dict[str, Any] = {}

    for metric in METRICS:
        target = getattr(targets, metric)
        actual = float(totals.get(metric, 0.0))

        if actual < target * _MET_LOWER:
            status = TargetStatus.UNDER
        elif actual > target * _MET_UPPER:
            status = TargetStatus.OVER
        else:
            status = TargetStatus.MET

        comparison[metric] = {
            "target": target,
            "actual": actual,
            "status": status.value,
            "percent_of_target": round(actual / target * 100, 1),
        }

    return comparison


__all__ = ["METRICS", "daily_totals", "compare_to_targets"]
