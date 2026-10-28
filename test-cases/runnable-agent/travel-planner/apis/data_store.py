"""
Data store for loading and saving travel data.
"""

import json
from pathlib import Path
from typing import Any

from models import Accommodation, Attraction, Destination, Itinerary


class DataStore:
    """Data persistence manager"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._itineraries: dict[str, Itinerary] = {}

    def _load_list(self, filename: str, model_class: type, key: str) -> list[Any]:
        """Load list data from JSON file"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get(key, [])
        return [model_class.model_validate(item) for item in items]

    def load_destinations(self) -> list[Destination]:
        """Load destinations from JSON file"""
        return self._load_list("destinations.json", Destination, "destinations")

    def load_attractions(self) -> list[Attraction]:
        """Load attractions from JSON file"""
        return self._load_list("attractions.json", Attraction, "attractions")

    def load_accommodations(self) -> list[Accommodation]:
        """Load accommodations from JSON file"""
        return self._load_list("accommodations.json", Accommodation, "accommodations")

    def save_itinerary(self, itinerary: Itinerary) -> None:
        """Save itinerary to memory"""
        self._itineraries[itinerary.itinerary_id] = itinerary

    def get_itinerary(self, itinerary_id: str) -> Itinerary | None:
        """Get itinerary by ID"""
        return self._itineraries.get(itinerary_id)

    def next_itinerary_id(self) -> str:
        """Generate the next itinerary ID, sequenced past any already saved"""
        if self._itineraries:
            highest = max(int(i[4:]) for i in self._itineraries)
            return f"ITIN{highest + 1:04d}"
        return "ITIN0001"


_STORE_INSTANCE: DataStore | None = None


def get_data_store(data_dir: str = "data") -> DataStore:
    """
    Return the process-wide DataStore.

    Saved itineraries live in memory, so `itinerary_create` and
    `itinerary_details` must share one instance — otherwise a created itinerary
    could never be read back. Catalog reads are unaffected either way.
    """
    global _STORE_INSTANCE
    if _STORE_INSTANCE is None:
        _STORE_INSTANCE = DataStore(data_dir=data_dir)
    return _STORE_INSTANCE


def reset_data_store() -> None:
    """Drop the shared instance so the next call starts empty (test isolation)"""
    global _STORE_INSTANCE
    _STORE_INSTANCE = None


__all__ = ["DataStore", "get_data_store", "reset_data_store"]
