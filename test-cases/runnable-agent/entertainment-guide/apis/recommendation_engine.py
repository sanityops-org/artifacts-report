"""
Recommendation engine.
"""

from models import Title
from models.enums import Genre, Mood


def get_recommendations(
    titles: list[Title],
    genre: str | None = None,
    mood: str | None = None,
    limit: int = 10
) -> list[Title]:
    """
    Get recommendations filtered by genre and/or mood, ranked by rating.

    Args:
        titles: Full catalog
        genre: Optional genre filter
        mood: Optional mood filter
        limit: Maximum results

    Returns:
        Recommended titles, ordered by rating descending then title_id ascending
    """
    results = list(titles)

    if genre:
        try:
            genre_enum = Genre(genre.lower())
            results = [t for t in results if genre_enum in t.genres]
        except ValueError:
            pass

    if mood:
        try:
            mood_enum = Mood(mood.lower())
            results = [t for t in results if mood_enum in t.mood_tags]
        except ValueError:
            pass

    results.sort(key=lambda t: (-t.rating, t.title_id))

    return results[:limit]


__all__ = ["get_recommendations"]
