"""
Integration tests: full workflows driven through the tools.

The watchlist lives in the shared data store, so tests reset it to avoid leaking
state between cases.
"""

import pytest

from apis.data_store import reset_data_store


@pytest.fixture(autouse=True)
def fresh_store():
    reset_data_store()
    yield
    reset_data_store()


def test_search_then_details():
    from tools.title_details import execute as title_details
    from tools.title_search import execute as title_search

    found = title_search({"query": "Inception"})
    assert found["status"] == "success"
    assert found["data"]["count"] == 1

    title_id = found["data"]["titles"][0]["title_id"]
    detail = title_details({"title_id": title_id})
    assert detail["status"] == "success"
    assert detail["data"]["title"] == "Inception"


def test_watchlist_flow_add_list_mark_remove():
    from tools.watchlist_add import execute as watchlist_add
    from tools.watchlist_list import execute as watchlist_list
    from tools.watchlist_mark_watched import execute as watchlist_mark_watched
    from tools.watchlist_remove import execute as watchlist_remove

    assert watchlist_list({})["data"]["count"] == 0

    added = watchlist_add({"title_id": "TITLE0003"})
    assert added["status"] == "success"
    assert watchlist_list({})["data"]["count"] == 1

    marked = watchlist_mark_watched({"title_id": "TITLE0003", "rating": 9.0})
    assert marked["status"] == "success"
    assert marked["data"]["item"]["status"] == "watched"
    assert marked["data"]["item"]["user_rating"] == 9.0

    removed = watchlist_remove({"title_id": "TITLE0003"})
    assert removed["status"] == "success"
    assert watchlist_list({})["data"]["count"] == 0


def test_watchlist_state_persists_across_tool_calls():
    """Regression guard: per-call stores made the watchlist unreachable."""
    from tools.watchlist_add import execute as watchlist_add
    from tools.watchlist_list import execute as watchlist_list

    watchlist_add({"title_id": "TITLE0001"})
    watchlist_add({"title_id": "TITLE0002"})

    result = watchlist_list({})
    assert result["data"]["count"] == 2


def test_duplicate_add_is_rejected():
    from tools.watchlist_add import execute as watchlist_add

    watchlist_add({"title_id": "TITLE0003"})
    duplicate = watchlist_add({"title_id": "TITLE0003"})

    assert duplicate["status"] == "error"
    assert "already on the watchlist" in duplicate["error"]


def test_adding_an_unknown_title_is_rejected():
    from tools.watchlist_add import execute as watchlist_add

    result = watchlist_add({"title_id": "TITLE9999"})
    assert result["status"] == "error"


def test_removing_a_title_not_on_the_watchlist_is_rejected():
    from tools.watchlist_remove import execute as watchlist_remove

    result = watchlist_remove({"title_id": "TITLE0001"})
    assert result["status"] == "error"
    assert "not on the watchlist" in result["error"]


def test_marking_a_title_not_on_the_watchlist_is_rejected():
    from tools.watchlist_mark_watched import execute as watchlist_mark_watched

    result = watchlist_mark_watched({"title_id": "TITLE0001"})
    assert result["status"] == "error"


def test_rating_outside_the_range_is_rejected():
    from tools.watchlist_add import execute as watchlist_add
    from tools.watchlist_mark_watched import execute as watchlist_mark_watched

    watchlist_add({"title_id": "TITLE0001"})

    for bad in (0.0, 11.0, -3.0):
        result = watchlist_mark_watched({"title_id": "TITLE0001", "rating": bad})
        assert result["status"] == "error", f"rating {bad} should be rejected"


def test_watchlist_list_filters_by_status():
    from tools.watchlist_add import execute as watchlist_add
    from tools.watchlist_list import execute as watchlist_list
    from tools.watchlist_mark_watched import execute as watchlist_mark_watched

    watchlist_add({"title_id": "TITLE0001"})
    watchlist_add({"title_id": "TITLE0002"})
    watchlist_mark_watched({"title_id": "TITLE0001"})

    pending = watchlist_list({"status": "to_watch"})["data"]
    assert pending["count"] == 1
    assert pending["total_watchlist_size"] == 2

    watched = watchlist_list({"status": "watched"})["data"]
    assert watched["count"] == 1


def test_watchlist_entries_are_enriched_with_title_metadata():
    from tools.watchlist_add import execute as watchlist_add
    from tools.watchlist_list import execute as watchlist_list

    watchlist_add({"title_id": "TITLE0021"})
    item = watchlist_list({})["data"]["items"][0]

    assert item["title_name"] == "Breaking Bad"
    assert item["title_type"] == "tv_show"
    assert item["title_year"] == 2008


def test_recommendations_are_tagged_as_suggestions():
    """Boundary B3: recommendations must be presented as suggestions."""
    from tools.get_recommendations import execute as get_recommendations

    result = get_recommendations({"mood": "thoughtful"})
    assert result["status"] == "success"
    assert "suggestion" in result["data"]["note"].lower()


def test_review_list_reports_an_average():
    from tools.review_list import execute as review_list

    result = review_list({"title_id": "TITLE0001"})
    assert result["status"] == "success"
    assert result["data"]["count"] == 3

    ratings = [r["rating"] for r in result["data"]["reviews"]]
    expected = round(sum(ratings) / len(ratings), 2)
    assert result["data"]["average_rating"] == expected


def test_review_list_handles_a_title_with_no_reviews():
    from tools.review_list import execute as review_list

    result = review_list({"title_id": "TITLE0005"})
    assert result["status"] == "success"
    assert result["data"]["count"] == 0
    assert result["data"]["average_rating"] is None


def test_missing_required_parameters_are_named():
    from tools.title_details import execute as title_details
    from tools.title_by_actor import execute as title_by_actor
    from tools.watchlist_add import execute as watchlist_add

    for tool, field in ((title_details, "title_id"), (title_by_actor, "actor_name"),
                        (watchlist_add, "title_id")):
        result = tool({})
        assert result["status"] == "error"
        assert field in result["error"]


def test_tool_payloads_contain_no_piracy_or_streaming_offers():
    """Boundaries B1/B2: no tool may offer playback or unauthorized sources."""
    forbidden = ("watch now", "stream it", "download", "torrent", "free streaming")

    from tools.get_recommendations import execute as get_recommendations
    from tools.title_details import execute as title_details

    payloads = [
        str(title_details({"title_id": "TITLE0001"})),
        str(get_recommendations({"genre": "drama"})),
    ]

    for payload in payloads:
        lowered = payload.lower()
        for term in forbidden:
            assert term not in lowered, f"{term!r} appeared in a tool payload"
