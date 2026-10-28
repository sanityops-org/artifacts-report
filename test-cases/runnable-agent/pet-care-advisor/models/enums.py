"""
Enumerations for Pet Care Advisor domain models.
"""

from enum import Enum


class Species(str, Enum):
    """Animal species"""
    DOG = "dog"      # Dog
    CAT = "cat"      # Cat


class PetSize(str, Enum):
    """Adult size class"""
    SMALL = "small"      # Small-scale
    MEDIUM = "medium"    # Medium-sized
    LARGE = "large"      # Large-scale


class Temperament(str, Enum):
    """Temperament traits"""
    FRIENDLY = "friendly"            # Amicable
    ENERGETIC = "energetic"          # Lively
    CALM = "calm"                    # Quiet
    PLAYFUL = "playful"              # Love to play
    INDEPENDENT = "independent"      # Stand alone
    AFFECTIONATE = "affectionate"    # Sticky
    PROTECTIVE = "protective"        # Protect the Lord
    SHY = "shy"                      # Timid


class GroomingLevel(str, Enum):
    """Grooming intensity"""
    LOW = "low"              # Low
    MODERATE = "moderate"    # Centre
    HIGH = "high"            # Tall


class AdoptionStatus(str, Enum):
    """Adoption listing status"""
    AVAILABLE = "available"    # Can be adopted
    PENDING = "pending"        # To be confirmed
    ADOPTED = "adopted"        # Adopted


class PetSex(str, Enum):
    """Pet sex"""
    MALE = "male"        # Public
    FEMALE = "female"    # Mother


class CareTaskType(str, Enum):
    """Care task types"""
    FEEDING = "feeding"          # Feed
    WALK = "walk"                # Take a walk
    GROOMING = "grooming"        # Wash and dress
    MEDICATION = "medication"    # Feed medicine
    VET_VISIT = "vet_visit"      # See a doctor
    PLAY = "play"                # Play with
    TRAINING = "training"        # Train


class CareTaskStatus(str, Enum):
    """Care task status"""
    PENDING = "pending"    # To be completed
    DONE = "done"          # Completed
    SKIPPED = "skipped"    # Skipped


class TaskFrequency(str, Enum):
    """Care task recurrence"""
    ONCE = "once"        # One-time
    DAILY = "daily"      # Every day
    WEEKLY = "weekly"    # Every week


class HealthRecordType(str, Enum):
    """Health record types"""
    VACCINATION = "vaccination"    # Vaccine
    VET_VISIT = "vet_visit"        # See a doctor
    WEIGHT = "weight"              # Weight
    MEDICATION = "medication"      # Administer a medicine
    ALLERGY = "allergy"            # Be anaphylactic


__all__ = [
    "Species",
    "PetSize",
    "Temperament",
    "GroomingLevel",
    "AdoptionStatus",
    "PetSex",
    "CareTaskType",
    "CareTaskStatus",
    "TaskFrequency",
    "HealthRecordType",
]
