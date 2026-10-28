"""
Data store for loading entertainment data.
"""

import json
from pathlib import Path
from typing import Any

from models import Review, Title, WatchlistItem


class DataStore:
    """Data persistence manager"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._watchlist: list[WatchlistItem] = []
        self._watchlist_loaded = False
        self._next_watchlist_id = 1
        self._next_review_id = 1

    def _load_list(self, filename: str, model_class: type, key: str) -> list[Any]:
        """Load list data from JSON file"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get(key, [])
        return [model_class.model_validate(item) for item in items]

    # --- Titles ---
    def load_titles(self) -> list[Title]:
        return self._load_list("titles.json", Title, "titles")

    # --- Reviews ---
    def load_reviews(self) -> list[Review]:
        return self._load_list("reviews.json", Review, "reviews")

    # --- Watchlist (in-memory session) ---
    def load_watchlist(self) -> list[WatchlistItem]:
        """Load watchlist: seeded from file once, then held in memory"""
        if not self._watchlist_loaded:
            self._watchlist = self._load_list("watchlist.json", WatchlistItem, "watchlist")
            if self._watchlist:
                max_id = max(int(item.item_id[2:]) for item in self._watchlist)
                self._next_watchlist_id = max_id + 1
            self._watchlist_loaded = True

            reviews = self._load_list("reviews.json", Review, "reviews")
            if reviews:
                max_review = max(int(r.review_id[3:]) for r in reviews)
                self._next_review_id = max_review + 1

        return self._watchlist

    def save_watchlist(self, items: list[WatchlistItem]) -> None:
        """Save watchlist to memory only (no disk write — see B4 in the design doc)"""
        self._watchlist = items
        self._watchlist_loaded = True

    def next_watchlist_id(self) -> str:
        """Generate next watchlist item ID"""
        item_id = f"WL{self._next_watchlist_id:04d}"
        self._next_watchlist_id += 1
        return item_id

    def next_review_id(self) -> str:
        """Generate next review ID"""
        review_id = f"REV{self._next_review_id:04d}"
        self._next_review_id += 1
        return review_id


_STORE_INSTANCE: DataStore | None = None


def get_data_store(data_dir: str = "data") -> DataStore:
    """
    Return the process-wide DataStore.

    The watchlist lives in memory (see the design doc's B4 constraint), so every
    tool must share one instance or mutations would be silently dropped between
    calls. Read-only data is unaffected either way.
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
