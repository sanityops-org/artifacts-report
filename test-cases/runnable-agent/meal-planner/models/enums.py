"""
Enumerations for Meal Planner domain models.
"""

from enum import Enum


class MealType(str, Enum):
    """Meal slots in a day"""
    BREAKFAST = "breakfast"    # Breakfast
    LUNCH = "lunch"            # Lunch
    DINNER = "dinner"          # Dinner
    SNACK = "snack"            # Have a snack


class DietTag(str, Enum):
    """Dietary labels carried by a recipe"""
    VEGETARIAN = "vegetarian"        # Vegetarian meal
    VEGAN = "vegan"                  # Pure vegetarian
    GLUTEN_FREE = "gluten_free"      # Gluten-free
    DAIRY_FREE = "dairy_free"        # No dairy products
    LOW_CARB = "low_carb"            # Low-carbon water
    HIGH_PROTEIN = "high_protein"    # High-protein
    PESCATARIAN = "pescatarian"      # Fish vegetarian
    NUT_FREE = "nut_free"            # Nut-free


class Cuisine(str, Enum):
    """Recipe cuisines"""
    ITALIAN = "italian"                # Italy
    JAPANESE = "japanese"              # Japan
    MEXICAN = "mexican"                # Mexico
    INDIAN = "indian"                  # India
    ASIAN = "asian"                # Asian-style
    MEDITERRANEAN = "mediterranean"    # Mediterranean Sea
    AMERICAN = "american"              # American-style
    THAI = "thai"                      # Thai style


class IngredientCategory(str, Enum):
    """Shopping aisle categories"""
    PRODUCE = "produce"      # Fruit and vegetables
    PROTEIN = "protein"      # Protein
    DAIRY = "dairy"          # Dairy product
    GRAIN = "grain"          # Cereal
    PANTRY = "pantry"        # Stockpile
    SPICE = "spice"          # Flavour


class Unit(str, Enum):
    """Measurement units"""
    G = "g"                # Gram
    KG = "kg"              # Kilogram
    ML = "ml"              # Millilitre
    L = "l"                # Ascend
    TSP = "tsp"            # Teaspoon
    TBSP = "tbsp"          # Tablespoon
    CUP = "cup"            # Glass
    PIECE = "piece"        # Self
    SLICE = "slice"        # Flat, thin piece
    CLOVE = "clove"        # Petal


class TargetStatus(str, Enum):
    """How a day's total compares to its target"""
    UNDER = "under"    # Below the target
    MET = "met"        # Achieve the goal
    OVER = "over"      # Exceed the target


__all__ = [
    "MealType",
    "DietTag",
    "Cuisine",
    "IngredientCategory",
    "Unit",
    "TargetStatus",
]
