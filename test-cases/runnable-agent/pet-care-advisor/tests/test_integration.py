"""
Integration tests: full workflows driven through the tools.

The data store is process-wide and holds session state in memory, so each test
resets it to reseed from the shipped JSON.
"""

import pytest

from apis.data_store import reset_data_store


@pytest.fixture(autouse=True)
def fresh_store():
    """Reseed the shared store before each test"""
    reset_data_store()
    yield
    reset_data_store()


def test_care_loop_create_then_complete():
    from tools.care_schedule_today import execute as schedule_today
    from tools.care_task_complete import execute as complete_task
    from tools.care_task_create import execute as create_task

    before = schedule_today({})["data"]["count"]

    created = create_task({"pet_id": "PET001", "type": "walk", "scheduled_time": "06:00"})
    assert created["status"] == "success"
    task_id = created["data"]["task"]["task_id"]

    assert schedule_today({})["data"]["count"] == before + 1

    assert complete_task({"task_id": task_id})["status"] == "success"
    assert schedule_today({})["data"]["count"] == before

    # Completing twice must fail
    again = complete_task({"task_id": task_id})
    assert again["status"] == "error"
    assert "already marked" in again["error"]


def test_new_task_id_does_not_collide_with_seed_data():
    from tools.care_task_create import execute as create_task
    from tools.care_task_list import execute as list_tasks

    seed_ids = {t["task_id"] for t in list_tasks({})["data"]["tasks"]}

    created = create_task({"pet_id": "PET002", "type": "play", "scheduled_time": "09:00"})
    assert created["data"]["task"]["task_id"] not in seed_ids


def test_new_record_id_does_not_collide_with_seed_data():
    from tools.health_record_add import execute as add_record
    from tools.health_record_list import execute as list_records

    seed_ids = {r["record_id"] for r in list_records({"pet_id": "PET001"})["data"]["records"]}

    added = add_record({
        "pet_id": "PET001", "type": "weight", "date": "2026-10-09",
        "description": "Routine weigh-in"
    })
    assert added["status"] == "success"
    assert added["data"]["record"]["record_id"] not in seed_ids


def test_created_record_appears_in_listing():
    from tools.health_record_add import execute as add_record
    from tools.health_record_list import execute as list_records

    add_record({
        "pet_id": "PET005", "type": "vaccination", "date": "2026-10-09",
        "description": "Booster given at the clinic", "next_due": "2027-10-09"
    })

    result = list_records({"pet_id": "PET005"})["data"]
    assert result["count"] == 1
    assert result["due_soon_count"] == 0  # a year away is outside the 30-day window


def test_pet_listing_excludes_pending_pets():
    from tools.pet_list import execute as list_pets

    ids = [p["pet_id"] for p in list_pets({})["data"]["pets"]]
    assert "PET008" not in ids  # seeded as pending


def test_pet_listing_enriches_with_breed():
    from tools.pet_list import execute as list_pets

    for pet in list_pets({})["data"]["pets"]:
        assert pet["breed_name"]
        assert pet["breed_size"] in ("small", "medium", "large")


def test_unknown_ids_produce_errors_not_exceptions():
    from tools.breed_details import execute as breed_details
    from tools.pet_details import execute as pet_details

    assert breed_details({"breed_id": "BREED999"})["status"] == "error"
    assert pet_details({"pet_id": "PET999"})["status"] == "error"
    assert pet_details({})["status"] == "error"


def test_missing_required_parameters_are_named():
    from tools.care_task_create import execute as create_task

    result = create_task({})
    assert result["status"] == "error"
    assert "pet_id" in result["error"]


def test_health_records_flag_overdue_seed_data():
    """PET004 ships with a booster that is past its due date."""
    from tools.health_record_list import execute as list_records

    result = list_records({"pet_id": "PET004"})["data"]
    assert result["overdue_count"] >= 1
    assert result["due_soon_count"] >= 1


def test_user_notes_are_stored_verbatim():
    from tools.care_task_create import execute as create_task

    note = "Half a pouch in the morning, per the vet's note"
    result = create_task({
        "pet_id": "PET002", "type": "feeding",
        "scheduled_time": "08:30", "notes": note
    })
    assert result["data"]["task"]["notes"] == note


def test_no_tool_invents_a_feeding_amount():
    """The create tool stores no amount of its own, only user-supplied notes."""
    from tools.care_task_create import execute as create_task

    result = create_task({"pet_id": "PET002", "type": "feeding", "scheduled_time": "08:30"})
    assert result["data"]["task"]["notes"] is None
    serialized = str(result["data"])
    for forbidden in ("feed_amount", "dosage", "prescription", "diagnosis"):
        assert forbidden not in serialized
