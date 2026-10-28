"""
Pet Care Advisor API layer.
"""

from apis.care_engine import records_due_soon, tasks_due_on
from apis.data_store import DataStore, get_data_store, reset_data_store
from apis.matching_engine import filter_pets, get_breed_by_id, get_pet_by_id, search_breeds

__all__ = [
    "DataStore",
    "get_data_store",
    "reset_data_store",
    "search_breeds",
    "filter_pets",
    "get_breed_by_id",
    "get_pet_by_id",
    "tasks_due_on",
    "records_due_soon",
]
