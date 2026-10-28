"""
Tests for the Pet Care Advisor domain models.
"""

import pytest
from pydantic import ValidationError


def test_breed_requires_valid_id_pattern():
    from models import Breed

    Breed(
        breed_id="BREED001", name="Test Breed", species="dog", size="medium",
        temperaments=["calm"], exercise_minutes_per_day=60, grooming_level="low",
        apartment_friendly=True, good_with_kids=True, lifespan_years="10-12",
        description="A breed used only in tests."
    )

    with pytest.raises(ValidationError):
        Breed(
            breed_id="BRD001", name="Test Breed", species="dog", size="medium",
            temperaments=["calm"], exercise_minutes_per_day=60, grooming_level="low",
            apartment_friendly=True, good_with_kids=True, lifespan_years="10-12",
            description="A breed used only in tests."
        )


def test_breed_rejects_exercise_out_of_range():
    from models import Breed

    with pytest.raises(ValidationError):
        Breed(
            breed_id="BREED001", name="Test Breed", species="dog", size="medium",
            temperaments=["calm"], exercise_minutes_per_day=999, grooming_level="low",
            apartment_friendly=True, good_with_kids=True, lifespan_years="10-12",
            description="A breed used only in tests."
        )


def test_breed_requires_at_least_one_temperament():
    from models import Breed

    with pytest.raises(ValidationError):
        Breed(
            breed_id="BREED001", name="Test Breed", species="dog", size="medium",
            temperaments=[], exercise_minutes_per_day=60, grooming_level="low",
            apartment_friendly=True, good_with_kids=True, lifespan_years="10-12",
            description="A breed used only in tests."
        )


def test_breed_rejects_unknown_temperament():
    from models import Breed

    with pytest.raises(ValidationError):
        Breed(
            breed_id="BREED001", name="Test Breed", species="dog", size="medium",
            temperaments=["grumpy"], exercise_minutes_per_day=60, grooming_level="low",
            apartment_friendly=True, good_with_kids=True, lifespan_years="10-12",
            description="A breed used only in tests."
        )


def test_care_task_requires_hh_mm_time():
    from models import CareTask

    CareTask(
        task_id="TASK0001", pet_id="PET001", type="walk",
        scheduled_time="07:30", frequency="daily", created_at="2026-10-09T08:00:00"
    )

    with pytest.raises(ValidationError):
        CareTask(
            task_id="TASK0001", pet_id="PET001", type="walk",
            scheduled_time="7:30am", frequency="daily", created_at="2026-10-09T08:00:00"
        )


def test_care_task_defaults():
    from models import CareTask
    from models.enums import CareTaskStatus, TaskFrequency

    task = CareTask(
        task_id="TASK0001", pet_id="PET001", type="walk",
        scheduled_time="07:30", created_at="2026-10-09T08:00:00"
    )

    assert task.status == CareTaskStatus.PENDING
    assert task.frequency == TaskFrequency.DAILY
    assert task.scheduled_date is None
    assert task.notes is None


def test_health_record_allows_null_next_due():
    from models import HealthRecord

    record = HealthRecord(
        record_id="REC0001", pet_id="PET001", type="weight",
        date="2026-10-09", description="Routine weigh-in"
    )
    assert record.next_due is None


def test_pet_rejects_bad_breed_reference():
    from models import Pet

    with pytest.raises(ValidationError):
        Pet(
            pet_id="PET001", name="Test", breed_id="BREED1", species="dog",
            age_months=12, sex="male", description="A pet used only in tests."
        )


def test_pet_defaults_to_available():
    from models import Pet
    from models.enums import AdoptionStatus

    pet = Pet(
        pet_id="PET001", name="Test", breed_id="BREED001", species="dog",
        age_months=12, sex="male", description="A pet used only in tests."
    )
    assert pet.adoption_status == AdoptionStatus.AVAILABLE


def test_shipped_data_files_validate_against_models():
    """Every row in data/ must satisfy its model — guards against drift."""
    import json
    from pathlib import Path

    from models import Breed, CareTask, HealthRecord, Pet

    data_dir = Path(__file__).parent.parent.parent / "data"

    for filename, key, model in (
        ("breeds.json", "breeds", Breed),
        ("pets.json", "pets", Pet),
        ("care_tasks.json", "care_tasks", CareTask),
        ("health_records.json", "health_records", HealthRecord),
    ):
        payload = json.loads((data_dir / filename).read_text(encoding="utf-8"))
        rows = payload[key]
        assert rows, f"{filename} should ship seed data"
        for row in rows:
            model.model_validate(row)
