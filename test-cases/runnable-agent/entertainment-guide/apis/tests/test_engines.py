"""
Tests for the title search and recommendation engines.
"""

import pytest

from apis.recommendation_engine import get_recommendations
from apis.search_engine import find_by_actor, find_by_director, get_title_by_id, search_titles
from models import Title


@pytest.fixture
def titles():
    return [
        Title(title_id="TITLE0001", title="Alpha Action", type="movie", year=2000,
              genres=["action", "thriller"], director="Nolan",
              cast=["Leonardo DiCaprio", "Someone Else"], rating=9.0,
              synopsis="An action film used only in tests.", mood_tags=["excited"]),
        Title(title_id="TITLE0002", title="Beta Drama", type="movie", year=2005,
              genres=["drama"], director="Nolan", cast=["Leonardo DiCaprio"],
              rating=8.0, synopsis="A drama used only in tests.", mood_tags=["thoughtful"]),
        Title(title_id="TITLE0003", title="Gamma Show", type="tv_show", year=2010,
              genres=["comedy"], director="Someone", cast=["Other Actor"],
              rating=8.5, synopsis="A show used only in tests.", mood_tags=["happy"]),
    ]


def test_search_with_no_filters_returns_whole_catalog(titles):
    assert len(search_titles(titles=titles)) == 3


def test_search_orders_by_rating_descending(titles):
    result = search_titles(titles=titles)
    assert [t.title_id for t in result] == ["TITLE0001", "TITLE0003", "TITLE0002"]


def test_search_by_type(titles):
    result = search_titles(title_type="tv_show", titles=titles)
    assert [t.title_id for t in result] == ["TITLE0003"]


def test_search_by_genre(titles):
    result = search_titles(genre="action", titles=titles)
    assert [t.title_id for t in result] == ["TITLE0001"]


def test_search_by_query_matches_synopsis(titles):
    result = search_titles(query="drama used only", titles=titles)
    assert [t.title_id for t in result] == ["TITLE0002"]


def test_search_query_matches_cast(titles):
    result = search_titles(query="other actor", titles=titles)
    assert [t.title_id for t in result] == ["TITLE0003"]


def test_search_combines_filters(titles):
    assert search_titles(title_type="movie", genre="comedy", titles=titles) == []


def test_search_with_unknown_genre_is_ignored(titles):
    """An unparseable enum value must not silently empty the result set."""
    assert len(search_titles(genre="western", titles=titles)) == 3


def test_search_respects_limit(titles):
    assert len(search_titles(titles=titles, limit=2)) == 2


def test_find_by_actor(titles):
    result = find_by_actor("Leonardo DiCaprio", titles)
    assert [t.title_id for t in result] == ["TITLE0001", "TITLE0002"]


def test_find_by_actor_is_case_insensitive(titles):
    assert len(find_by_actor("leonardo dicaprio", titles)) == 2


def test_find_by_actor_with_no_match(titles):
    assert find_by_actor("Nobody", titles) == []


def test_find_by_director(titles):
    result = find_by_director("Nolan", titles)
    assert [t.title_id for t in result] == ["TITLE0001", "TITLE0002"]


def test_find_by_director_with_no_match(titles):
    assert find_by_director("Nobody", titles) == []


def test_get_title_by_id(titles):
    assert get_title_by_id("TITLE0002", titles).title == "Beta Drama"
    assert get_title_by_id("TITLE9999", titles) is None


def test_recommendations_with_no_filters_are_rating_ordered(titles):
    result = get_recommendations(titles)
    assert [t.title_id for t in result] == ["TITLE0001", "TITLE0003", "TITLE0002"]


def test_recommendations_by_genre(titles):
    result = get_recommendations(titles, genre="comedy")
    assert [t.title_id for t in result] == ["TITLE0003"]


def test_recommendations_by_mood(titles):
    result = get_recommendations(titles, mood="thoughtful")
    assert [t.title_id for t in result] == ["TITLE0002"]


def test_recommendations_combine_genre_and_mood(titles):
    """A genre and a mood that do not co-occur yields nothing."""
    assert get_recommendations(titles, genre="action", mood="happy") == []


def test_recommendations_respect_limit(titles):
    assert len(get_recommendations(titles, limit=1)) == 1


def test_recommendations_with_unknown_mood_is_ignored(titles):
    assert len(get_recommendations(titles, mood="contemplative")) == 3
