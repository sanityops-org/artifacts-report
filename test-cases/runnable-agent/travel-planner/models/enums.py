"""
Enumerations for Travel Planner domain models.
"""

from enum import Enum


class BudgetLevel(str, Enum):
    """Budget level categories"""
    BUDGET = "budget"        # Economical
    MODERATE = "moderate"    # Comfortable type
    LUXURY = "luxury"        # Luxury type


class Season(str, Enum):
    """Travel seasons"""
    SPRING = "spring"        # Spring
    SUMMER = "summer"        # Summer
    AUTUMN = "autumn"        # Autumn
    WINTER = "winter"        # Winter


class AttractionCategory(str, Enum):
    """Attraction categories"""
    NATURE = "nature"            # Natural landscape
    CULTURE = "culture"          # Cultural attractions
    ADVENTURE = "adventure"      # Adventure activities
    FOOD = "food"                # Food experience
    SHOPPING = "shopping"        # Shopping places
    RELAXATION = "relaxation"    # Relax and relax
    BEACH = "beach"              # Beach
    CITY = "city"                # City sightseeing


class AccommodationType(str, Enum):
    """Accommodation types"""
    HOTEL = "hotel"          # Pub
    HOSTEL = "hostel"        # Youth hostel
    RESORT = "resort"        # Holiday village
    APARTMENT = "apartment"  # Apartment


class TravelTheme(str, Enum):
    """Travel themes"""
    BEACH = "beach"              # Beach
    MOUNTAIN = "mountain"        # Hilly country
    CITY = "city"                # City
    CULTURE = "culture"          # Civilization
    ADVENTURE = "adventure"      # Explore
    FAMILY = "family"            # Family
    ROMANTIC = "romantic"        # Romantic
    FOODIE = "foodie"            # Delicious food
    NATURE = "nature"            # Nature
    RELAXATION = "relaxation"    # Be at leisure
    SHOPPING = "shopping"        # Go shopping


__all__ = [
    "BudgetLevel",
    "Season",
    "AttractionCategory",
    "AccommodationType",
    "TravelTheme",
]
