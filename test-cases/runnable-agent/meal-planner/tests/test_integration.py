"""
Integration tests: full workflows driven through the tools.

Meal plans and the nutrition log live in the shared data store, so tests reset it
to avoid leaking state between cases.
"""

import hashlib
import json
from pathlib import Path

import pytest

from apis.data_store import reset_data_store

DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture(autouse=True)
def fresh_store():
    reset_data_store()
    yield
    reset_data_store()


def _hash_data_files() -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(DATA_DIR.glob("*.json"))
    }


def test_recipe_search_then_details():
    from tools.recipe_details import execute as recipe_details
    from tools.recipe_search import execute as recipe_search

    found = recipe_search({"cuisine": "italian"})
    assert found["status"] == "success"
    assert found["data"]["count"] >= 1

    recipe_id = found["data"]["recipes"][0]["recipe_id"]
    detail = recipe_details({"recipe_id": recipe_id})
    assert detail["status"] == "success"
    assert len(detail["data"]["ingredients"]) >= 1
    assert detail["data"]["steps"]


def test_recipe_search_by_time_ceiling():
    from tools.recipe_search import execute as recipe_search

    result = recipe_search({"max_total_minutes": 25})
    assert result["status"] == "success"
    for recipe in result["data"]["recipes"]:
        assert recipe["total_minutes"] <= 25


def test_recipe_search_results_are_time_ordered():
    from tools.recipe_search import execute as recipe_search

    times = [r["total_minutes"] for r in recipe_search({})["data"]["recipes"]]
    assert times == sorted(times)


def test_recipe_by_ingredient():
    from tools.recipe_by_ingredient import execute as recipe_by_ingredient

    result = recipe_by_ingredient({"ingredient": "garlic"})
    assert result["status"] == "success"
    assert result["data"]["count"] >= 1


def test_meal_plan_round_trip():
    from tools.meal_plan_add_entry import execute as add_entry
    from tools.meal_plan_create import execute as create_plan
    from tools.meal_plan_get import execute as get_plan

    created = create_plan({"name": "Test Week", "start_date": "2026-10-12", "days": 3})
    assert created["status"] == "success"
    plan_id = created["data"]["plan"]["plan_id"]

    added = add_entry({"plan_id": plan_id, "day_index": 1, "meal_type": "dinner",
                       "recipe_id": "RECIPE001", "servings": 2})
    assert added["status"] == "success"

    fetched = get_plan({"plan_id": plan_id})
    assert fetched["status"] == "success"
    assert fetched["data"]["entry_count"] == 1
    assert fetched["data"]["entries"][0]["recipe_name"]
    assert fetched["data"]["entries"][0]["date"] == "2026-10-12"


def test_plan_entry_defaults_to_the_recipes_own_servings():
    from tools.meal_plan_add_entry import execute as add_entry
    from tools.meal_plan_create import execute as create_plan

    plan_id = create_plan({"name": "Defaults", "start_date": "2026-10-12", "days": 1})["data"]["plan"]["plan_id"]
    entry = add_entry({"plan_id": plan_id, "day_index": 1, "meal_type": "lunch",
                       "recipe_id": "RECIPE003"})["data"]["entry"]

    from tools.recipe_details import execute as recipe_details
    assert entry["servings"] == recipe_details({"recipe_id": "RECIPE003"})["data"]["servings"]


def test_new_plan_ids_do_not_collide_with_the_seed():
    from tools.meal_plan_create import execute as create_plan

    first = create_plan({"name": "One", "start_date": "2026-10-12", "days": 1})
    second = create_plan({"name": "Two", "start_date": "2026-10-12", "days": 1})

    assert first["data"]["plan"]["plan_id"] != second["data"]["plan"]["plan_id"]
    assert first["data"]["plan"]["plan_id"] != "PLAN0001"


def test_new_entry_ids_do_not_collide_with_the_seed():
    from tools.meal_plan_add_entry import execute as add_entry
    from tools.meal_plan_create import execute as create_plan

    seed_ids = {e["entry_id"] for e in
                json.loads((DATA_DIR / "meal_plans.json").read_text(encoding="utf-8"))["meal_plans"][0]["entries"]}

    plan_id = create_plan({"name": "IDs", "start_date": "2026-10-12", "days": 1})["data"]["plan"]["plan_id"]
    entry = add_entry({"plan_id": plan_id, "day_index": 1, "meal_type": "snack",
                       "recipe_id": "RECIPE010"})["data"]["entry"]

    assert entry["entry_id"] not in seed_ids


def test_shopping_list_scales_to_the_planned_servings():
    """RECIPE007 is written for 2 servings; the seed plans it for 4."""
    from tools.shopping_list_generate import execute as shopping_list_generate

    result = shopping_list_generate({"plan_id": "PLAN0001"})
    assert result["status"] == "success"

    salmon = next(i for i in result["data"]["items"] if i["name"] == "Salmon fillet")
    assert salmon["quantity"] == 800.0  # 400 g written for 2, doubled to 4


def test_shopping_list_merges_shared_ingredients():
    """Olive oil appears in two seeded recipes, both in tbsp."""
    from tools.shopping_list_generate import execute as shopping_list_generate

    result = shopping_list_generate({"plan_id": "PLAN0001"})
    olive_oil = [i for i in result["data"]["items"] if i["name"] == "Olive oil"]

    assert len(olive_oil) == 1
    assert olive_oil[0]["quantity"] > 0


def test_shopping_list_groups_by_category_without_losing_items():
    from tools.shopping_list_generate import execute as shopping_list_generate

    result = shopping_list_generate({"plan_id": "PLAN0001"})
    assert result["data"]["item_count"] == len(result["data"]["items"])
    for item in result["data"]["items"]:
        assert item["quantity"] > 0
        assert item["category"]


def test_meal_plan_get_enriches_entries_and_dates_them():
    from tools.meal_plan_get import execute as get_plan

    result = get_plan({"plan_id": "PLAN0001"})
    assert result["status"] == "success"

    entries = result["data"]["entries"]
    assert [e["entry_id"] for e in entries] == sorted(e["entry_id"] for e in entries)
    # Day 1 is the start date, day 2 the following day
    assert entries[0]["date"] == "2026-10-09"


def test_nutrition_log_then_summary():
    from tools.nutrition_daily_summary import execute as daily_summary
    from tools.nutrition_log_meal import execute as log_meal

    empty = daily_summary({"date": "2026-10-09"})
    assert empty["status"] == "success"
    assert empty["data"]["totals"]["calories"] == 0.0

    logged = log_meal({"date": "2026-10-09", "meal_type": "dinner",
                       "recipe_id": "RECIPE001", "servings": 4})
    assert logged["status"] == "success"

    summary = daily_summary({"date": "2026-10-09"})
    assert summary["data"]["totals"]["calories"] == 2080.0  # 520 x 4


def test_summary_ignores_other_dates():
    from tools.nutrition_daily_summary import execute as daily_summary
    from tools.nutrition_log_meal import execute as log_meal

    log_meal({"date": "2026-10-09", "meal_type": "lunch", "recipe_id": "RECIPE001", "servings": 1})
    log_meal({"date": "2026-10-11", "meal_type": "lunch", "recipe_id": "RECIPE001", "servings": 5})

    assert daily_summary({"date": "2026-10-09"})["data"]["totals"]["calories"] == 520.0


def test_summary_comparison_matches_the_configuration():
    from tools.nutrition_daily_summary import execute as daily_summary
    from tools.nutrition_log_meal import execute as log_meal

    log_meal({"date": "2026-10-09", "meal_type": "dinner", "recipe_id": "RECIPE001", "servings": 4})
    comparison = daily_summary({"date": "2026-10-09"})["data"]["comparison"]

    # 2080 calories against a 2000 target is 104%, inside the met band
    assert comparison["calories"]["status"] == "met"
    # 56 g protein against 100 g is well under
    assert comparison["protein_g"]["status"] == "under"
    # 304 g carbs against 250 g is over
    assert comparison["carbs_g"]["status"] == "over"


def test_targets_tool_returns_the_configured_targets():
    from tools.nutrition_targets_get import execute as targets_get

    result = targets_get({})
    assert result["status"] == "success"
    assert result["data"]["calories"] == 2000.0


def test_recipe_search_carries_the_allergen_note():
    """Boundary B2: diet tags must never read as an allergen guarantee."""
    from tools.recipe_search import execute as recipe_search
    from tools.recipe_details import execute as recipe_details

    assert "allergen_note" in recipe_search({})["data"]
    assert "not an allergen analysis" in recipe_details({"recipe_id": "RECIPE001"})["data"]["allergen_note"]


def test_nutrition_responses_carry_the_estimate_disclaimer():
    """Boundary B3: nutrition figures must be presented as estimates."""
    from tools.nutrition_daily_summary import execute as daily_summary
    from tools.recipe_details import execute as recipe_details

    recipe = recipe_details({"recipe_id": "RECIPE001"})["data"]
    assert recipe["nutrition_is_estimate"] is True
    assert "estimate" in recipe["disclaimer"].lower()

    summary = daily_summary({"date": "2026-10-09"})["data"]
    assert summary["is_estimate"] is True
    assert "estimate" in summary["disclaimer"].lower()


def test_summary_carries_the_dietitian_note():
    """Boundary B1: anything clinical is routed to a professional."""
    from tools.nutrition_daily_summary import execute as daily_summary

    note = daily_summary({"date": "2026-10-09"})["data"]["dietitian_note"]
    assert "registered dietitian" in note


def test_user_data_is_never_written_to_disk():
    """Boundary B4."""
    from tools.meal_plan_add_entry import execute as add_entry
    from tools.meal_plan_create import execute as create_plan
    from tools.nutrition_log_meal import execute as log_meal

    before = _hash_data_files()

    plan_id = create_plan({"name": "Mutating", "start_date": "2026-10-12", "days": 2})["data"]["plan"]["plan_id"]
    add_entry({"plan_id": plan_id, "day_index": 1, "meal_type": "dinner", "recipe_id": "RECIPE001"})
    log_meal({"date": "2026-10-09", "meal_type": "dinner", "recipe_id": "RECIPE002"})

    assert _hash_data_files() == before


def test_unknown_ids_produce_errors_not_exceptions():
    from tools.meal_plan_get import execute as get_plan
    from tools.recipe_details import execute as recipe_details
    from tools.shopping_list_generate import execute as shopping_list_generate

    assert recipe_details({"recipe_id": "RECIPE999"})["status"] == "error"
    assert get_plan({"plan_id": "PLAN9999"})["status"] == "error"
    assert shopping_list_generate({"plan_id": "PLAN9999"})["status"] == "error"


def test_missing_required_parameters_are_named():
    from tools.meal_plan_create import execute as create_plan
    from tools.nutrition_log_meal import execute as log_meal
    from tools.recipe_details import execute as recipe_details

    for tool, params, field in (
        (recipe_details, {}, "recipe_id"),
        (create_plan, {}, "name"),
        (create_plan, {"name": "x"}, "start_date"),
        (log_meal, {}, "date"),
        (log_meal, {"date": "2026-10-09"}, "meal_type"),
    ):
        result = tool(params)
        assert result["status"] == "error"
        assert field in result["error"], f"{tool.__module__} did not name {field}"


def test_add_entry_rejects_a_day_outside_the_plan():
    from tools.meal_plan_add_entry import execute as add_entry
    from tools.meal_plan_create import execute as create_plan

    plan_id = create_plan({"name": "Short", "start_date": "2026-10-12", "days": 1})["data"]["plan"]["plan_id"]
    result = add_entry({"plan_id": plan_id, "day_index": 5, "meal_type": "dinner",
                        "recipe_id": "RECIPE001"})

    assert result["status"] == "error"
    assert "outside plan" in result["error"]


def test_add_entry_rejects_an_unknown_recipe():
    from tools.meal_plan_add_entry import execute as add_entry
    from tools.meal_plan_create import execute as create_plan

    plan_id = create_plan({"name": "Bad recipe", "start_date": "2026-10-12", "days": 1})["data"]["plan"]["plan_id"]
    result = add_entry({"plan_id": plan_id, "day_index": 1, "meal_type": "dinner",
                        "recipe_id": "RECIPE999"})

    assert result["status"] == "error"
    assert "RECIPE999" in result["error"]


def test_add_entry_rejects_an_unknown_meal_type():
    from tools.meal_plan_add_entry import execute as add_entry

    result = add_entry({"plan_id": "PLAN0001", "day_index": 1, "meal_type": "brunch",
                        "recipe_id": "RECIPE001"})

    assert result["status"] == "error"
    assert "meal_type" in result["error"]


def test_add_entry_rejects_non_positive_servings():
    from tools.meal_plan_add_entry import execute as add_entry

    for bad in (0, -1):
        result = add_entry({"plan_id": "PLAN0001", "day_index": 1, "meal_type": "dinner",
                            "recipe_id": "RECIPE001", "servings": bad})
        assert result["status"] == "error"


def test_log_meal_rejects_bad_input():
    from tools.nutrition_log_meal import execute as log_meal

    assert log_meal({"date": "09/10/2026", "meal_type": "lunch",
                     "recipe_id": "RECIPE001"})["status"] == "error"
    assert log_meal({"date": "2026-10-09", "meal_type": "brunch",
                     "recipe_id": "RECIPE001"})["status"] == "error"
    assert log_meal({"date": "2026-10-09", "meal_type": "lunch",
                     "recipe_id": "RECIPE999"})["status"] == "error"


def test_plan_create_rejects_out_of_range_days():
    from tools.meal_plan_create import execute as create_plan

    assert create_plan({"name": "x", "start_date": "2026-10-12", "days": 0})["status"] == "error"
    assert create_plan({"name": "x", "start_date": "2026-10-12", "days": 15})["status"] == "error"
    assert create_plan({"name": "x", "start_date": "12-10-2026", "days": 3})["status"] == "error"


def test_tool_payloads_contain_no_clinical_content():
    """Boundary B1: no tool may return a diagnosis, treatment, or supplement dose."""
    from tools.nutrition_daily_summary import execute as daily_summary
    from tools.nutrition_targets_get import execute as targets_get

    forbidden = ("diagnosis", "treat your", "supplement dose", "prescribe", "cure")

    payloads = [
        str(daily_summary({"date": "2026-10-09"})).lower(),
        str(targets_get({})).lower(),
    ]

    for payload in payloads:
        for term in forbidden:
            assert term not in payload, f"{term!r} appeared in a tool payload"
