"""
Data store for pet care data.

Catalog data (breeds, pets) is read from JSON. Care tasks and health records are
seeded from JSON once and then held in memory for the session only — nothing is
written back to disk (constraint B4 in the design document).
"""

import json
from pathlib import Path
from typing import Any

from models import Breed, CareTask, HealthRecord, Pet


class DataStore:
    """Data persistence manager"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._care_tasks: list[CareTask] = []
        self._care_tasks_loaded = False
        self._next_task_id = 1
        self._health_records: list[HealthRecord] = []
        self._health_records_loaded = False
        self._next_record_id = 1

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
    def load_breeds(self) -> list[Breed]:
        return self._load_list("breeds.json", Breed, "breeds")

    def load_pets(self) -> list[Pet]:
        return self._load_list("pets.json", Pet, "pets")

    # --- Care tasks (seeded once, then in memory) ---
    def load_care_tasks(self) -> list[CareTask]:
        if not self._care_tasks_loaded:
            self._care_tasks = self._load_list("care_tasks.json", CareTask, "care_tasks")
            if self._care_tasks:
                max_id = max(int(t.task_id[4:]) for t in self._care_tasks)
                self._next_task_id = max_id + 1
            self._care_tasks_loaded = True
        return self._care_tasks

    def save_care_tasks(self, tasks: list[CareTask]) -> None:
        """Save care tasks to memory only — no disk write"""
        self._care_tasks = tasks
        self._care_tasks_loaded = True

    # --- Health records (seeded once, then in memory) ---
    def load_health_records(self) -> list[HealthRecord]:
        if not self._health_records_loaded:
            self._health_records = self._load_list(
                "health_records.json", HealthRecord, "health_records"
            )
            if self._health_records:
                max_id = max(int(r.record_id[3:]) for r in self._health_records)
                self._next_record_id = max_id + 1
            self._health_records_loaded = True
        return self._health_records

    def save_health_records(self, records: list[HealthRecord]) -> None:
        """Save health records to memory only — no disk write"""
        self._health_records = records
        self._health_records_loaded = True

    def next_task_id(self) -> str:
        """Generate the next care task ID, sequenced past the seed data"""
        task_id = f"TASK{self._next_task_id:04d}"
        self._next_task_id += 1
        return task_id

    def next_record_id(self) -> str:
        """Generate the next health record ID, sequenced past the seed data"""
        record_id = f"REC{self._next_record_id:04d}"
        self._next_record_id += 1
        return record_id


_STORE_INSTANCE: DataStore | None = None


def get_data_store(data_dir: str = "data") -> DataStore:
    """
    Return the process-wide DataStore.

    Care tasks and health records live in memory, so every tool must share one
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
