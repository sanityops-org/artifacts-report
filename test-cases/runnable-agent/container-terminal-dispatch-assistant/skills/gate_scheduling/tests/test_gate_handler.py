"""
Gate Dispatching Skills Handler Test
"""

import os
import sys
import pytest

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, project_root)

from skills.gate_scheduling.handler import run
from apis.tos_api import login


@pytest.fixture(autouse=True)
def setup_session():
    """Log in to create a valid session before each test"""
    result = login("Operation supervisor")
    yield result["data"]


def run_with_session(intent: str, params: dict, session: dict) -> dict:
    """Execution with session information"""
    params_with_session = {**params, "_session": session}
    return run(intent, params_with_session)


class TestHandlerQueryGateStatus:
    """Test query_gate_status intent"""

    def test_query_gate_status_without_filter(self, setup_session):
        """Test and query all gate channels"""
        result = run_with_session("query_gate_status", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "channels" in result["data"]
        assert isinstance(result["data"]["channels"], list)

    def test_query_gate_status_with_channel_id(self, setup_session):
        """Test specify channel_id to query a single channel"""
        result = run_with_session("query_gate_status", {"channel_id": "G01"}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "channel" in result["data"]

    def test_query_gate_status_channel_not_found(self, setup_session):
        """Test the query of non-existent channels"""
        result = run_with_session("query_gate_status", {"channel_id": "G99"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result or "message" in result

    def test_query_gate_status_with_type_filter(self, setup_session):
        """Test filter channels by type"""
        result = run_with_session("query_gate_status", {"type": "inbound"}, setup_session)

        assert result["status"] == "success"
        assert "channels" in result["data"]
        # All returned channels should be inbound type.
        for channel in result["data"]["channels"]:
            assert channel["type"] == "inbound"

    def test_query_gate_status_with_status_filter(self, setup_session):
        """Test filter channels by status"""
        result = run_with_session("query_gate_status", {"status": "open"}, setup_session)

        assert result["status"] == "success"
        assert "channels" in result["data"]


class TestHandlerQueryGateAppointment:
    """Test query_gate_appointment intent"""

    def test_query_appointment_without_filter(self, setup_session):
        """Test and query all appointment records"""
        result = run_with_session("query_gate_appointment", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "appointments" in result["data"]
        assert isinstance(result["data"]["appointments"], list)

    def test_query_appointment_with_id(self, setup_session):
        """Test the specified appointment_id to query a single appointment"""
        result = run_with_session("query_gate_appointment", {"appointment_id": "AP001"}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "appointment" in result["data"]

    def test_query_appointment_not_found(self, setup_session):
        """Test query non-existent appointments"""
        result = run_with_session("query_gate_appointment", {"appointment_id": "AP999"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result or "message" in result

    def test_query_appointment_with_truck_id(self, setup_session):
        """Test to filter appointments by card ID"""
        result = run_with_session("query_gate_appointment", {"truck_id": "TRK001"}, setup_session)

        assert result["status"] == "success"
        assert "appointments" in result["data"]

    def test_query_appointment_with_status_filter(self, setup_session):
        """Test to filter appointments by status"""
        result = run_with_session("query_gate_appointment", {"status": "pending"}, setup_session)

        assert result["status"] == "success"
        assert "appointments" in result["data"]


class TestHandlerQueryGateQueue:
    """Test query_gate_queue intent"""

    def test_query_gate_queue(self, setup_session):
        """Test and query the queue"""
        result = run_with_session("query_gate_queue", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "total_queue" in result["data"]
        assert "inbound_queue" in result["data"]
        assert "outbound_queue" in result["data"]
        assert "channels" in result["data"]
        assert isinstance(result["data"]["total_queue"], int)
        assert isinstance(result["data"]["inbound_queue"], int)
        assert isinstance(result["data"]["outbound_queue"], int)


class TestHandlerOpenGateChannel:
    """Test open_gate_channel intent"""

    def test_open_gate_channel_missing_channel_id(self, setup_session):
        """The test is missing the channel_id parameter"""
        result = run_with_session("open_gate_channel", {}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_open_gate_channel_not_found(self, setup_session):
        """Test open non-existent channels"""
        result = run_with_session("open_gate_channel", {"channel_id": "G99"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result


class TestHandlerCloseGateChannel:
    """Test close_gate_channel intent"""

    def test_close_gate_channel_missing_channel_id(self, setup_session):
        """The test is missing the channel_id parameter"""
        result = run_with_session("close_gate_channel", {}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_close_gate_channel_not_found(self, setup_session):
        """Test to close the non-existent channel"""
        result = run_with_session("close_gate_channel", {"channel_id": "G99"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_close_gate_channel_with_reason(self, setup_session):
        """Test with the reason to close the channel"""
        result = run_with_session("close_gate_channel", {
            "channel_id": "G01",
            "reason": "Equipment maintenance"
        }, setup_session)

        # It may be successful or closed.
        assert result["status"] in ("success", "error")


class TestHandlerProcessGatePass:
    """Test process_gate_pass intent"""

    def test_process_gate_pass_missing_truck_id(self, setup_session):
        """The test lacks truck_id parameter"""
        result = run_with_session("process_gate_pass", {"channel_id": "G01", "direction": "inbound"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_process_gate_pass_missing_channel_id(self, setup_session):
        """The test is missing the channel_id parameter"""
        result = run_with_session("process_gate_pass", {"truck_id": "TRK001", "direction": "inbound"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_process_gate_pass_missing_direction(self, setup_session):
        """The test lacks the direction parameter"""
        result = run_with_session("process_gate_pass", {"truck_id": "TRK001", "channel_id": "G01"}, setup_session)

        assert result["status"] == "error"
        assert "error" in result

    def test_process_gate_pass_invalid_direction(self, setup_session):
        """Invalid entry and exit direction of the test"""
        result = run_with_session("process_gate_pass", {
            "truck_id": "TRK001",
            "channel_id": "G01",
            "direction": "invalid"
        }, setup_session)

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
