"""
data_store: Data persistence layer for JSON simulated weather data.
"""

import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from models import Alert, CurrentConditions, DailyForecast, Location

T = TypeVar("T", bound=BaseModel)


class DataStore:
    """Data persistence manager"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._ensure_data_dir()

    def _ensure_data_dir(self) -> None:
        """Ensure the data directory exists"""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def _load_list(self, filename: str, model_class: type[T], key: str) -> list[T]:
        """Load list data from JSON file"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get(key, [])
        return [model_class.model_validate(item) for item in items]

    # --- Locations ---
    def load_locations(self) -> list[Location]:
        return self._load_list("locations.json", Location, "locations")

    # --- Current conditions ---
    def load_current_conditions(self) -> list[CurrentConditions]:
        return self._load_list("current_conditions.json", CurrentConditions, "current_conditions")

    # --- Forecasts ---
    def load_forecasts(self) -> list[DailyForecast]:
        return self._load_list("forecasts.json", DailyForecast, "forecasts")

    # --- Alerts ---
    def load_alerts(self) -> list[Alert]:
        return self._load_list("alerts.json", Alert, "alerts")


__all__ = ["DataStore"]
