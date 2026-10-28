"""
Search engine for titles.
"""

from models import Title
from models.enums import Genre, TitleType


def search_titles(
    query: str | None = None,
    title_type: str | None = None,
    genre: str | None = None,
    titles: list[Title] | None = None,
    limit: int = 20
) -> list[Title]:
    """
    Search titles by query, type, or genre.

    Args:
        query: Substring matched against title, director, cast, and synopsis
        title_type: "movie" or "tv_show"
        genre: Genre name
        titles: Full catalog
        limit: Maximum results

    Returns:
        Matching titles, ordered by rating descending then title_id ascending
    """
    results = list(titles or [])

    if title_type:
        try:
            type_enum = TitleType(title_type.lower())
            results = [t for t in results if t.type == type_enum]
        except ValueError:
            pass

    if genre:
        try:
            genre_enum = Genre(genre.lower())
            results = [t for t in results if genre_enum in t.genres]
        except ValueError:
            pass

    if query:
        q = query.lower().strip()
        results = [
            t for t in results
            if q in t.title.lower()
            or q in t.director.lower()
            or any(q in actor.lower() for actor in t.cast)
            or q in t.synopsis.lower()
        ]

    results.sort(key=lambda t: (-t.rating, t.title_id))

    return results[:limit]


def find_by_actor(actor_name: str, titles: list[Title]) -> list[Title]:
    """Find titles featuring an actor (case-insensitive substring match)"""
    name = actor_name.lower().strip()
    results = [t for t in titles if any(name in actor.lower() for actor in t.cast)]
    results.sort(key=lambda t: (-t.rating, t.title_id))
    return results


def find_by_director(director_name: str, titles: list[Title]) -> list[Title]:
    """Find titles by a director (case-insensitive substring match)"""
    name = director_name.lower().strip()
    results = [t for t in titles if name in t.director.lower()]
    results.sort(key=lambda t: (-t.rating, t.title_id))
    return results


def get_title_by_id(title_id: str, titles: list[Title]) -> Title | None:
    """Get a title by its ID"""
    for t in titles:
        if t.title_id == title_id:
            return t
    return None


__all__ = ["search_titles", "find_by_actor", "find_by_director", "get_title_by_id"]
