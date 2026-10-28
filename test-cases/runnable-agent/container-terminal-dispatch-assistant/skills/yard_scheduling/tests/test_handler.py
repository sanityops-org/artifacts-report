"""
Stacking site scheduling skills Handler test
"""

import os
import sys
import pytest

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, project_root)

from skills.yard_scheduling.handler import run
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


class TestQueryYardStatus:
    """Test query the status of the storage box area"""

    def test_query_all_blocks(self, setup_session):
        """Test and query all box areas"""
        result = run_with_session("query_yard_status", {}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "blocks" in result["data"]
        assert "summary" in result["data"]
        assert result["data"]["summary"]["total_blocks"] == 4

    def test_query_block_by_id(self, setup_session):
        """Test query a single box area"""
        result = run_with_session("query_yard_status", {"block_id": "A01"}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "block" in result["data"]
        assert result["data"]["block"]["block_id"] == "A01"
        assert "available_slots" in result["data"]
        assert "utilization_rate" in result["data"]

    def test_query_block_not_found(self, setup_session):
        """Test query non-existent box area"""
        result = run_with_session("query_yard_status", {"block_id": "Z99"}, setup_session)

        assert result["status"] == "error"
        assert "does not exist" in result.get("error", result.get("message", "")).lower()

    def test_query_by_type(self, setup_session):
        """Test filter by type"""
        result = run_with_session("query_yard_status", {"type": "import"}, setup_session)

        assert result["status"] == "success"
        assert "blocks" in result["data"]
        # There should be only the import box area.
        for block in result["data"]["blocks"]:
            assert block["type"] == "import"

    def test_query_invalid_type(self, setup_session):
        """Invalid type of test"""
        result = run_with_session("query_yard_status", {"type": "invalid_type"}, setup_session)

        assert result["status"] == "error"
        assert "invalid" in result.get("error", result.get("message", "")).lower()


class TestQueryContainerLocation:
    """Test and query the location of the container"""

    def test_query_container_by_id(self, setup_session):
        """Test query the location of a single container"""
        result = run_with_session("query_container_location", {"container_id": "ABCD1234567"}, setup_session)

        assert result["status"] == "success"
        assert "data" in result
        assert "container" in result["data"]
        assert result["data"]["container"]["container_id"] == "ABCD1234567"
        assert "location_description" in result["data"]

    def test_query_container_not_found(self, setup_session):
        """Test and query non-existent containers"""
        result = run_with_session("query_container_location", {"container_id": "XXXX9999999"}, setup_session)

        assert result["status"] == "error"
        assert "does not exist" in result.get("error", result.get("message", "")).lower()

    def test_query_containers_by_block(self, setup_session):
        """Test all containers in the query box area"""
        result = run_with_session("query_container_location", {"block_id": "A01"}, setup_session)

        assert result["status"] == "success"
        assert "containers" in result["data"]
        assert result["data"]["block_id"] == "A01"

    def test_query_all_containers(self, setup_session):
        """Test and query all containers"""
        result = run_with_session("query_container_location", {}, setup_session)

        assert result["status"] == "success"
        assert "containers" in result["data"]
        assert result["data"]["count"] == 3


class TestQueryRehandleList:
    """Test query box-turning task list"""

    def test_query_all_rehandle_tasks(self, setup_session):
        """Test and query all box-turning tasks"""
        result = run_with_session("query_rehandle_list", {}, setup_session)

        assert result["status"] == "success"
        assert "tasks" in result["data"]
        assert "status_summary" in result["data"]

    def test_query_by_status(self, setup_session):
        """Test filter by status"""
        result = run_with_session("query_rehandle_list", {"status": "pending"}, setup_session)

        assert result["status"] == "success"
        # All returned tasks should be in the pending state.
        for task in result["data"]["tasks"]:
            assert task["status"] == "pending"

    def test_query_invalid_status(self, setup_session):
        """Invalid status of the test"""
        result = run_with_session("query_rehandle_list", {"status": "invalid_status"}, setup_session)

        assert result["status"] == "error"
        assert "invalid" in result.get("error", result.get("message", "")).lower()


class TestAssignYardSlot:
    """Test the distribution of the drop box location"""

    def test_assign_missing_container_id(self, setup_session):
        """The test is missing containers.ID"""
        result = run_with_session("assign_yard_slot", {"block_id": "A01"}, setup_session)

        assert result["status"] == "error"
        assert "container_id" in result["error"]

    def test_assign_missing_block_id(self, setup_session):
        """The test is missing the box area.ID"""
        result = run_with_session("assign_yard_slot", {"container_id": "ABCD1234567"}, setup_session)

        assert result["status"] == "error"
        assert "block_id" in result["error"]

    def test_assign_container_not_found(self, setup_session):
        """The test container does not exist."""
        result = run_with_session("assign_yard_slot", {
            "container_id": "XXXX9999999",
            "block_id": "A01"
        }, setup_session)

        assert result["status"] == "error"
        assert "does not exist" in result["error"].lower()


class TestCreateRehandleTask:
    """Test and create box-turning tasks"""

    def test_create_missing_container_id(self, setup_session):
        """The test is missing containers.ID"""
        result = run_with_session("create_rehandle_task", {"from_block_id": "A01"}, setup_session)

        assert result["status"] == "error"
        assert "container_id" in result["error"]

    def test_create_missing_from_block_id(self, setup_session):
        """The original box area is missing in the test.ID"""
        result = run_with_session("create_rehandle_task", {"container_id": "ABCD1234567"}, setup_session)

        assert result["status"] == "error"
        assert "from_block_id" in result["error"]

    def test_create_container_not_found(self, setup_session):
        """The test container does not exist."""
        result = run_with_session("create_rehandle_task", {
            "container_id": "XXXX9999999",
            "from_block_id": "A01"
        }, setup_session)

        assert result["status"] == "error"
        assert "does not exist" in result["error"].lower()

    def test_create_container_wrong_location(self, setup_session):
        """The position of the test container does not match"""
        result = run_with_session("create_rehandle_task", {
            "container_id": "ABCD1234567",
            "from_block_id": "B01"  # The container is actually in A01
        }, setup_session)

        assert result["status"] == "error"
        assert "not in" in result["error"]


class TestUpdateContainerLocation:
    """Test and update the container location"""

    def test_update_missing_container_id(self, setup_session):
        """The test is missing containers.ID"""
        result = run_with_session("update_container_location", {
            "block_id": "B01",
            "bay": 10,
            "row": 5,
            "tier": 3
        }, setup_session)

        assert result["status"] == "error"
        assert "container_id" in result["error"]

    def test_update_missing_required_params(self, setup_session):
        """The test lacks the required parameters."""
        result = run_with_session("update_container_location", {
            "container_id": "ABCD1234567"
        }, setup_session)

        assert result["status"] == "error"
        assert "block_id" in result["error"]

    def test_update_container_not_found(self, setup_session):
        """The test container does not exist."""
        result = run_with_session("update_container_location", {
            "container_id": "XXXX9999999",
            "block_id": "B01",
            "bay": 10,
            "row": 5,
            "tier": 3
        }, setup_session)

        assert result["status"] == "error"
        assert "does not exist" in result["error"].lower()


class TestHandlerRouting:
    """Test Handler routing"""

    def test_unknown_intent(self, setup_session):
        """Test unknown operations"""
        result = run_with_session("unknown_operation", {}, setup_session)

        assert result["status"] == "error"
        assert "Unknown operation" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
