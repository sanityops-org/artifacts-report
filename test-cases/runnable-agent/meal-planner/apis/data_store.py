"""
Data store for meal planner data.

The recipe catalog and nutrition targets are read from JSON. Meal plans and the
nutrition log are seeded from JSON once and then held in memory for the session
only — nothing is written back to disk (constraint B4 in the design document).
"""

import json
from pathlib import Path
from typing import Any

from models import MealPlan, NutritionLogEntry, NutritionTargets, Recipe


class DataStore:
    """Data persistence manager"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._meal_plans: list[MealPlan] = []
        self._plans_loaded = False
        self._next_plan_id = 1
        self._next_entry_id = 1
        self._log: list[NutritionLogEntry] = []
        self._log_loaded = False
        self._next_log_id = 1

    def _load_list(self, filename: str, model_class: type, key: str) -> list[Any]:
        """Load list data from JSON file"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get(key, [])
        return [model_class.model_validate(item) for item in items]

    # --- Catalog (read-only, from disk) ---
    def load_recipes(self) -> list[Recipe]:
        return self._load_list("recipes.json", Recipe, "recipes")

    def load_targets(self) -> NutritionTargets | None:
        """Load the daily nutrition targets"""
        filepath = self.data_dir / "nutrition_targets.json"
        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        payload = data.get("nutrition_targets")
        if not payload:
            return None
        return NutritionTargets.model_validate(payload)

    # --- Meal plans (seeded once, then in memory) ---
    def load_meal_plans(self) -> list[MealPlan]:
        if not self._plans_loaded:
            self._meal_plans = self._load_list("meal_plans.json", MealPlan, "meal_plans")
            if self._meal_plans:
                self._next_plan_id = max(int(p.plan_id[4:]) for p in self._meal_plans) + 1
                existing_entries = [e for p in self._meal_plans for e in p.entries]
                if existing_entries:
                    self._next_entry_id = max(int(e.entry_id[5:]) for e in existing_entries) + 1
            self._plans_loaded = True
        return self._meal_plans

    def save_meal_plans(self, plans: list[MealPlan]) -> None:
        """Save meal plans to memory only — no disk write"""
        self._meal_plans = plans
        self._plans_loaded = True

    # --- Nutrition log (seeded once, then in memory) ---
    def load_nutrition_log(self) -> list[NutritionLogEntry]:
        if not self._log_loaded:
            self._log = self._load_list("nutrition_log.json", NutritionLogEntry, "nutrition_log")
            if self._log:
                self._next_log_id = max(int(e.log_id[3:]) for e in self._log) + 1
            self._log_loaded = True
        return self._log

    def save_nutrition_log(self, entries: list[NutritionLogEntry]) -> None:
        """Save the nutrition log to memory only — no disk write"""
        self._log = entries
        self._log_loaded = True

    # --- ID sequencing (past any seeded rows) ---
    def next_plan_id(self) -> str:
        plan_id = f"PLAN{self._next_plan_id:04d}"
        self._next_plan_id += 1
        return plan_id

    def next_entry_id(self) -> str:
        entry_id = f"ENTRY{self._next_entry_id:04d}"
        self._next_entry_id += 1
        return entry_id

    def next_log_id(self) -> str:
        log_id = f"LOG{self._next_log_id:04d}"
        self._next_log_id += 1
        return log_id


_STORE_INSTANCE: DataStore | None = None


def get_data_store(data_dir: str = "data") -> DataStore:
    """
    Return the process-wide DataStore.

    Meal plans and the nutrition log live in memory, so every tool must share one
    instance or mutations would be silently dropped between calls. Catalog reads
    are unaffected either way.
    """
    global _STORE_INSTANCE
    if _STORE_INSTANCE is None:
        _STORE_INSTANCE = DataStore(data_dir=data_dir)
    return _STORE_INSTANCE


def reset_data_store() -> None:
    """Drop the shared instance so the next call reseeds from JSON (test isolation)"""
    global _STORE_INSTANCE
    _STORE_INSTANCE = None


__all__ = ["DataStore", "get_data_store", "reset_data_store"]
