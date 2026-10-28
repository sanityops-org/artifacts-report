"""
Tests for the Entertainment Guide domain models.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def test_title_requires_valid_id_pattern():
    from models import Title

    Title(title_id="TITLE0001", title="Test Film", type="movie", year=2020,
          genres=["drama"], director="A Director", synopsis="A synopsis long enough to validate.",
          rating=7.5)

    with pytest.raises(ValidationError):
        Title(title_id="TITLE1", title="Test Film", type="movie", year=2020,
              genres=["drama"], director="A Director", synopsis="A synopsis long enough to validate.",
              rating=7.5)


def test_title_rating_bounds():
    from models import Title

    with pytest.raises(ValidationError):
        Title(title_id="TITLE0001", title="Test Film", type="movie", year=2020,
              genres=["drama"], director="A Director", synopsis="A synopsis long enough to validate.",
              rating=11.0)


def test_title_requires_at_least_one_genre():
    from models import Title

    with pytest.raises(ValidationError):
        Title(title_id="TITLE0001", title="Test Film", type="movie", year=2020,
              genres=[], director="A Director", synopsis="A synopsis long enough to validate.",
              rating=7.5)


def test_title_rejects_unknown_genre():
    from models import Title

    with pytest.raises(ValidationError):
        Title(title_id="TITLE0001", title="Test Film", type="movie", year=2020,
              genres=["western"], director="A Director",
              synopsis="A synopsis long enough to validate.", rating=7.5)


def test_title_season_fields_are_optional():
    from models import Title

    movie = Title(title_id="TITLE0001", title="Test Film", type="movie", year=2020,
                  genres=["drama"], director="A Director",
                  synopsis="A synopsis long enough to validate.", rating=7.5)
    assert movie.seasons is None
    assert movie.episodes_per_season is None


def test_watchlist_item_defaults_to_to_watch():
    from models import WatchlistItem
    from models.enums import WatchlistStatus

    item = WatchlistItem(item_id="WL0001", title_id="TITLE0001", added_date="2026-10-09")
    assert item.status == WatchlistStatus.TO_WATCH
    assert item.watched_date is None
    assert item.user_rating is None


def test_watchlist_item_rejects_out_of_range_user_rating():
    from models import WatchlistItem

    with pytest.raises(ValidationError):
        WatchlistItem(item_id="WL0001", title_id="TITLE0001", added_date="2026-10-09",
                      user_rating=12.0)


def test_review_rating_bounds():
    from models import Review

    with pytest.raises(ValidationError):
        Review(review_id="REV0001", title_id="TITLE0001", user_name="Tester",
               rating=0.0, comment="A comment long enough", date="2026-10-09")


@pytest.mark.parametrize("filename,key,model_name", [
    ("titles.json", "titles", "Title"),
    ("reviews.json", "reviews", "Review"),
    ("watchlist.json", "watchlist", "WatchlistItem"),
])
def test_shipped_data_files_validate_against_models(filename, key, model_name):
    """Every row in data/ must satisfy its model — guards against enum drift."""
    import models

    model = getattr(models, model_name)
    payload = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))

    for row in payload[key]:
        model.model_validate(row)


def test_catalog_ships_thirty_titles():
    titles = json.loads((DATA_DIR / "titles.json").read_text(encoding="utf-8"))["titles"]
    assert len(titles) == 30


def test_every_review_references_a_known_title():
    titles = json.loads((DATA_DIR / "titles.json").read_text(encoding="utf-8"))["titles"]
    reviews = json.loads((DATA_DIR / "reviews.json").read_text(encoding="utf-8"))["reviews"]

    known = {t["title_id"] for t in titles}
    for review in reviews:
        assert review["title_id"] in known, f"{review['review_id']} references an unknown title"


def test_movies_have_runtime_and_shows_have_seasons():
    titles = json.loads((DATA_DIR / "titles.json").read_text(encoding="utf-8"))["titles"]

    for title in titles:
        if title["type"] == "movie":
            assert title.get("runtime_minutes"), f"{title['title']} is a movie with no runtime"
        else:
            assert title.get("seasons"), f"{title['title']} is a show with no season count"
            assert len(title["episodes_per_season"]) == title["seasons"], (
                f"{title['title']} episode list does not match its season count"
            )
