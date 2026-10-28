#!/usr/bin/env python3
"""
health_record_list: List a pet's health records and flag upcoming due dates.
"""

import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.care_engine import records_due_soon
from apis.data_store import get_data_store
from apis.matching_engine import get_pet_by_id

parameters = {
    "type": "object",
    "properties": {
        "pet_id": {
            "type": "string",
            "pattern": "^PET\\d{3}$",
            "description": "Pet ID, e.g. PET001"
        }
    },
    "required": ["pet_id"]
}


def _annotate(record: Any, reference: date) -> Dict[str, Any]:
    """Attach days_until and overdue to a record dict"""
    entry = record.model_dump(mode="json")
    if record.next_due:
        try:
            entry["days_until"] = (date.fromisoformat(record.next_due) - reference).days
            entry["overdue"] = entry["days_until"] < 0
        except ValueError:
            entry["days_until"] = None
            entry["overdue"] = None
    else:
        entry["days_until"] = None
        entry["overdue"] = None
    return entry


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List a pet's health records with due-date annotations.

    Args:
        params:
            - pet_id: Pet ID (required)

    Returns:
        {"status": "success", "data": {"records": [...], "count": N, "overdue_count": N,
         "due_soon": [...], "due_soon_count": N}} or
        {"status": "error", "error": "..."}
    """
    pet_id = params.get("pet_id")
    if not pet_id:
        return {"status": "error", "error": "Missing required parameter: pet_id"}

    try:
        store = get_data_store(str(project_root / "data"))
        pets = store.load_pets()
        records = store.load_health_records()

        pet = get_pet_by_id(pet_id, pets)
        if not pet:
            return {"status": "error", "error": f"Pet not found: {pet_id}"}

        reference = date.today()
        matching = [r for r in records if r.pet_id == pet_id]
        matching.sort(key=lambda r: r.date, reverse=True)

        entries = [_annotate(r, reference) for r in matching]
        overdue_count = sum(1 for e in entries if e["overdue"] is True)

        # Records falling inside the 30-day look-ahead window, with overdue ones included
        due_soon = records_due_soon(matching, within_days=30, today=reference.isoformat())

        return {
            "status": "success",
            "data": {
                "pet_id": pet_id,
                "pet_name": pet.name,
                "records": entries,
                "count": len(entries),
                "overdue_count": overdue_count,
                "due_soon": [
                    {
                        "record_id": e["record_id"],
                        "type": e["type"],
                        "description": e["description"],
                        "next_due": e["next_due"],
                        "days_until": e["days_until"],
                        "overdue": e["overdue"]
                    }
                    for e in due_soon
                ],
                "due_soon_count": len(due_soon)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to list health records: {str(e)}"}
