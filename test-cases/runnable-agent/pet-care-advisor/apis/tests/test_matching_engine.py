"""
Tests for the matching engine.
"""

import pytest

from apis.matching_engine import filter_pets, get_breed_by_id, get_pet_by_id, search_breeds
from models import Breed, Pet


@pytest.fixture
def breeds():
    return [
        Breed(
            breed_id="BREED001", name="Alpha Hound", species="dog", size="large",
            temperaments=["friendly", "energetic"], exercise_minutes_per_day=90,
            grooming_level="moderate", apartment_friendly=False, good_with_kids=True,
            lifespan_years="10-12", description="An energetic large breed for testing."
        ),
        Breed(
            breed_id="BREED002", name="Beta Cat", species="cat", size="small",
            temperaments=["calm"], exercise_minutes_per_day=20, grooming_level="low",
            apartment_friendly=True, good_with_kids=True, lifespan_years="12-15",
            description="A calm small breed for testing."
        ),
    ]


@pytest.fixture
def pets(breeds):
    return [
        Pet(pet_id="PET001", name="Young", breed_id="BREED001", species="dog",
            age_months=10, sex="male", adoption_status="available",
            description="A young available pet for testing."),
        Pet(pet_id="PET002", name="Older", breed_id="BREED001", species="dog",
            age_months=60, sex="female", adoption_status="available",
            description="An older available pet for testing."),
        Pet(pet_id="PET003", name="Reserved", breed_id="BREED001", species="dog",
            age_months=20, sex="male", adoption_status="pending",
            description="A reserved pet that must not appear in listings."),
        Pet(pet_id="PET004", name="Kitten", breed_id="BREED002", species="cat",
            age_months=6, sex="female", adoption_status="available",
            description="A young available cat for testing."),
    ]


def test_search_breeds_no_filters_returns_all(breeds):
    assert len(search_breeds(breeds)) == 2


def test_search_breeds_by_species(breeds):
    result = search_breeds(breeds, species="cat")
    assert [b.breed_id for b in result] == ["BREED002"]


def test_search_breeds_by_temperament(breeds):
    result = search_breeds(breeds, temperament="energetic")
    assert [b.breed_id for b in result] == ["BREED001"]


def test_search_breeds_by_query_matches_description(breeds):
    result = search_breeds(breeds, query="calm small")
    assert [b.breed_id for b in result] == ["BREED002"]


def test_search_breeds_unknown_filter_value_is_ignored(breeds):
    """An unparseable enum value must not silently empty the result set."""
    result = search_breeds(breeds, species="dragon")
    assert len(result) == 2


def test_search_breeds_is_ordered_by_name(breeds):
    names = [b.name for b in search_breeds(breeds)]
    assert names == sorted(names)


def test_search_breeds_respects_limit(breeds):
    assert len(search_breeds(breeds, limit=1)) == 1


def test_filter_pets_excludes_non_available(pets, breeds):
    ids = [p.pet_id for p in filter_pets(pets, breeds)]
    assert "PET003" not in ids
    assert len(ids) == 3


def test_filter_pets_by_species_via_breed_join(pets, breeds):
    result = filter_pets(pets, breeds, species="cat")
    assert [p.pet_id for p in result] == ["PET004"]


def test_filter_pets_by_size_via_breed_join(pets, breeds):
    result = filter_pets(pets, breeds, size="small")
    assert [p.pet_id for p in result] == ["PET004"]


def test_filter_pets_by_temperament_via_breed_join(pets, breeds):
    result = filter_pets(pets, breeds, temperament="energetic")
    assert [p.pet_id for p in result] == ["PET001", "PET002"]  # PET003 is pending


def test_filter_pets_by_max_age(pets, breeds):
    result = filter_pets(pets, breeds, max_age_months=10)
    assert [p.pet_id for p in result] == ["PET004", "PET001"]


def test_filter_pets_is_ordered_by_age_then_id(pets, breeds):
    result = filter_pets(pets, breeds)
    keys = [(p.age_months, p.pet_id) for p in result]
    assert keys == sorted(keys)


def test_filter_pets_skips_pet_with_missing_breed(pets, breeds):
    """An orphaned breed reference must not raise."""
    orphan = Pet(pet_id="PET099", name="Orphan", breed_id="BREED099", species="dog",
                 age_months=5, sex="male", description="A pet with no breed on file.")
    result = filter_pets(pets + [orphan], breeds)
    assert "PET099" not in [p.pet_id for p in result]
    assert len(result) == 3


def test_filter_pets_returns_empty_when_nothing_matches(pets, breeds):
    assert filter_pets(pets, breeds, max_age_months=0) == []


def test_lookup_helpers(breeds, pets):
    assert get_breed_by_id("BREED002", breeds).name == "Beta Cat"
    assert get_breed_by_id("BREED999", breeds) is None
    assert get_pet_by_id("PET001", pets).name == "Young"
    assert get_pet_by_id("PET999", pets) is None
