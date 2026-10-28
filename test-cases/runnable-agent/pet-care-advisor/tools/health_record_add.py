#!/usr/bin/env python3
"""
health_record_add: Add a health record for a pet, such as a vaccination or vet visit.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from apis.data_store import get_data_store
from apis.matching_engine import get_pet_by_id
from models import HealthRecord
from models.enums import HealthRecordType

parameters = {
    "type": "object",
    "properties": {
        "pet_id": {
            "type": "string",
            "pattern": "^PET\\d{3}$",
            "description": "Pet ID the record belongs to"
        },
        "type": {
            "type": "string",
            "enum": ["vaccination", "vet_visit", "weight", "medication", "allergy"],
            "description": "Health record type"
        },
        "date": {
            "type": "string",
            "description": "Date of the record in YYYY-MM-DD form"
        },
        "description": {
            "type": "string",
            "description": "What happened; supplied by the user"
        },
        "next_due": {
            "type": "string",
            "description": "Next due date in YYYY-MM-DD form, if the record recurs (optional)"
        }
    },
    "required": ["pet_id", "type", "date", "description"]
}


def _valid_date(value: Any) -> bool:
    try:
        datetime.strptime(str(value), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a health record.

    Args:
        params:
            - pet_id: Pet ID (required)
            - type: Record type (required)
            - date: YYYY-MM-DD (required)
            - description: What happened, user-supplied (required)
            - next_due: YYYY-MM-DD if recurring (optional)

    Returns:
        {"status": "success", "data": {"record": {...}}} or
        {"status": "error", "error": "..."}
    """
    pet_id = params.get("pet_id")
    record_type = params.get("type")
    record_date = params.get("date")
    description = params.get("description")

    if not pet_id:
        return {"status": "error", "error": "Missing required parameter: pet_id"}
    if not record_type:
        return {"status": "error", "error": "Missing required parameter: type"}
    if not record_date:
        return {"status": "error", "error": "Missing required parameter: date"}
    if not description:
        return {"status": "error", "error": "Missing required parameter: description"}

    if not _valid_date(record_date):
        return {"status": "error", "error": f"date must be in YYYY-MM-DD form, got {record_date!r}"}

    next_due = params.get("next_due")
    if next_due and not _valid_date(next_due):
        return {
            "status": "error",
            "error": f"next_due must be in YYYY-MM-DD form, got {next_due!r}"
        }

    try:
        record_type_enum = HealthRecordType(str(record_type).lower())
    except ValueError:
        valid = [t.value for t in HealthRecordType]
        return {
            "status": "error",
            "error": f"Unknown record type: {record_type}. Valid types: {valid}"
        }

    try:
        store = get_data_store(str(project_root / "data"))
        pets = store.load_pets()
        records = store.load_health_records()

        pet = get_pet_by_id(pet_id, pets)
        if not pet:
            return {"status": "error", "error": f"Pet not found: {pet_id}"}

        record = HealthRecord(
            record_id=store.next_record_id(),
            pet_id=pet_id,
            type=record_type_enum,
            date=str(record_date),
            description=str(description),
            next_due=str(next_due) if next_due else None
        )

        records.append(record)
        store.save_health_records(records)

        return {
            "status": "success",
            "data": {
                "record": record.model_dump(mode="json"),
                "pet_name": pet.name,
                "record_count": len(records)
            }
        }

    except Exception as e:
        return {"status": "error", "error": f"Failed to add health record: {str(e)}"}
