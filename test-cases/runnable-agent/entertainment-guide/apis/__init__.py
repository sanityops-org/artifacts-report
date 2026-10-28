"""
Entertainment Guide API layer.
"""

from apis.data_store import DataStore, get_data_store, reset_data_store
from apis.recommendation_engine import get_recommendations
from apis.search_engine import find_by_actor, find_by_director, get_title_by_id, search_titles

__all__ = [
    "DataStore",
    "get_data_store",
    "reset_data_store",
    "search_titles",
    "find_by_actor",
    "find_by_director",
    "get_title_by_id",
    "get_recommendations",
]
