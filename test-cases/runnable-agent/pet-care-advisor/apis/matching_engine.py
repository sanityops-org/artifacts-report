"""
Matching engine for breeds and adoptable pets.

Pure functions: the caller injects the catalogs, which keeps them directly
unit-testable without touching the filesystem.
"""

from models import Breed, Pet
from models.enums import AdoptionStatus, PetSize, Species, Temperament


def search_breeds(
    breeds: list[Breed],
    species: str | None = None,
    size: str | None = None,
    temperament: str | None = None,
    query: str | None = None,
    limit: int = 20
) -> list[Breed]:
    """
    Search breeds by species, size, temperament, and free-text query.

    Ordering is by breed name ascending for determinism.
    """
    results = list(breeds)

    if species:
        try:
            species_enum = Species(species.lower())
            results = [b for b in results if b.species == species_enum]
        except ValueError:
            pass

    if size:
        try:
            size_enum = PetSize(size.lower())
            results = [b for b in results if b.size == size_enum]
        except ValueError:
            pass

    if temperament:
        try:
            temperament_enum = Temperament(temperament.lower())
            results = [b for b in results if temperament_enum in b.temperaments]
        except ValueError:
            pass

    if query:
        q = query.lower().strip()
        results = [
            b for b in results
            if q in b.name.lower() or q in b.description.lower()
        ]

    results.sort(key=lambda b: b.name)

    return results[:limit]


def filter_pets(
    pets: list[Pet],
    breeds: list[Breed],
    species: str | None = None,
    size: str | None = None,
    temperament: str | None = None,
    max_age_months: int | None = None
) -> list[Pet]:
    """
    Filter adoptable pets.

    Non-available listings are excluded first. Species, size, and temperament
    filters are applied by joining each pet to its breed; a pet whose breed is
    missing from the catalog is skipped rather than raising.
    """
    breed_by_id = {b.breed_id: b for b in breeds}

    results = [
        p for p in pets
        if p.adoption_status == AdoptionStatus.AVAILABLE
    ]

    # Resolve breeds once, dropping orphans
    resolved: list[tuple[Pet, Breed]] = []
    for pet in results:
        breed = breed_by_id.get(pet.breed_id)
        if breed is not None:
            resolved.append((pet, breed))

    if species:
        try:
            species_enum = Species(species.lower())
            resolved = [(p, b) for p, b in resolved if b.species == species_enum]
        except ValueError:
            pass

    if size:
        try:
            size_enum = PetSize(size.lower())
            resolved = [(p, b) for p, b in resolved if b.size == size_enum]
        except ValueError:
            pass

    if temperament:
        try:
            temperament_enum = Temperament(temperament.lower())
            resolved = [(p, b) for p, b in resolved if temperament_enum in b.temperaments]
        except ValueError:
            pass

    if max_age_months is not None:
        resolved = [(p, b) for p, b in resolved if p.age_months <= max_age_months]

    resolved.sort(key=lambda pair: (pair[0].age_months, pair[0].pet_id))

    return [pet for pet, _ in resolved]


def get_breed_by_id(breed_id: str, breeds: list[Breed]) -> Breed | None:
    """Get a breed by its ID"""
    for breed in breeds:
        if breed.breed_id == breed_id:
            return breed
    return None


def get_pet_by_id(pet_id: str, pets: list[Pet]) -> Pet | None:
    """Get a pet by its ID"""
    for pet in pets:
        if pet.pet_id == pet_id:
            return pet
    return None


__all__ = ["search_breeds", "filter_pets", "get_breed_by_id", "get_pet_by_id"]
