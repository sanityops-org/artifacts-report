"""
Parking scheduling skills Handler test
"""

import os
import sys
import pytest

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, project_root)

from skills.berth_scheduling.handler import run
from apis.tos_api import login


@pytest.fixture(autouse=True)
def setup_session():
    """Log in to create a valid session before each test"""
    result = login("Operation supervisor")
    yield result["data"]  # Return session data


def run_with_session(intent: str, params: dict, session: dict) -> dict:
    """Execution with session information"""
    params_with_session = {**params, "_session": session}
    return run(intent, params_with_session)


class TestHandlerQueryVessel:
    """Test query_vessel_plan intent"""

    def test_query_vessel_without_id(self, setup_session):
        """Test without vessel_id to query all ships"""
        result = run_with_session("query_vessel_plan", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "vessels" in result["data"]
        assert isinstance(result["data"]["vessels"], list)

    def test_query_vessel_with_id(self, setup_session):
        """Test the specified vessel_id to query a single ship"""
        result = run_with_session("query_vessel_plan", {"vessel_id": "V001"}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "vessel" in result["data"]

    def test_query_vessel_not_found(self, setup_session):
        """Test and query non-existent ships"""
        result = run_with_session("query_vessel_plan", {"vessel_id": "V999"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result


class TestHandlerQueryBerth:
    """Test query_berth_status intent"""

    def test_query_berth_without_filter(self, setup_session):
        """Test and query all berths"""
        result = run_with_session("query_berth_status", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "berths" in result["data"]
        assert isinstance(result["data"]["berths"], list)

    def test_query_berth_with_id(self, setup_session):
        """Test specify berth_id to query a single berth"""
        result = run_with_session("query_berth_status", {"berth_id": "B01"}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        # A single berth returns the "berth" key
        assert "berth" in result["data"]

    def test_query_berth_not_found(self, setup_session):
        """Test and query non-existent berths"""
        result = run_with_session("query_berth_status", {"berth_id": "B999"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result


class TestHandlerUnknownIntent:
    """Test unknown intent processing"""

    def test_unknown_intent(self, setup_session):
        """Test unknown intent and return an error"""
        result = run_with_session("unknown_action", {}, setup_session)

        assert result["status"] == "error"
        assert "error" in result
        assert "Unknown operation" in result["error"]
        assert "available operation" in result["error"]

    def test_empty_intent(self, setup_session):
        """Test empty intent"""
        result = run_with_session("", {}, setup_session)

        assert result["status"] == "error"


class TestHandlerQueryAnchorage:
    """Test query_anchorage intent"""

    def test_query_anchorage(self, setup_session):
        """Test and query anchorage ships"""
        result = run_with_session("query_anchorage", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "vessels" in result["data"]


class TestHandlerAssignBerth:
    """Test assign_berth intent"""

    def test_assign_berth_missing_vessel_id(self, setup_session):
        """The test is missing the vessel_id parameter"""
        result = run_with_session("assign_berth", {"berth_id": "B01"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_assign_berth_missing_berth_id(self, setup_session):
        """The test is missing the berth_id parameter"""
        result = run_with_session("assign_berth", {"vessel_id": "V001"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result
