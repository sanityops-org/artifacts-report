"""
Equipment scheduling skill test

Test all the tool functions of device scheduling skills.
"""

import os
import sys
import pytest
import json
import shutil

# Add project root to path - go up from skills/equipment_scheduling to project root
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from apis.data_store import DataStore
from skills.equipment_scheduling.handler import run
from apis.tos_api import login
from models.enums import EquipmentStatus, TaskStatus
from models import Equipment, Task


@pytest.fixture(autouse=True)
def setup_session():
    """Log in to create a valid session before each test"""
    result = login("Operation supervisor")
    yield result["data"]


def run_with_session(intent: str, params: dict, session: dict) -> dict:
    """Execution with session information"""
    params_with_session = {**params, "_session": session}
    return run(intent, params_with_session)


# Original test data
ORIGINAL_EQUIPMENT = [
    {
        "equip_id": "QC01",
        "equip_type": "quay_crane",
        "equip_name": "1No. Anqiao",
        "status": "idle",
        "current_task": None,
        "berth_id": "B01",
        "efficiency_rate": 30
    },
    {
        "equip_id": "QC02",
        "equip_type": "quay_crane",
        "equip_name": "2No. Anqiao",
        "status": "working",
        "current_task": "T0001",
        "berth_id": "B01",
        "efficiency_rate": 28
    },
    {
        "equip_id": "RTG01",
        "equip_type": "rtg",
        "equip_name": "1No. Field Bridge",
        "status": "idle",
        "block_id": "A01",
        "efficiency_rate": 20
    },
    {
        "equip_id": "RTG02",
        "equip_type": "rtg",
        "equip_name": "2No. Field Bridge",
        "status": "idle",
        "block_id": "B01",
        "efficiency_rate": 20
    },
    {
        "equip_id": "YT01",
        "equip_type": "yard_truck",
        "equip_name": "1Number set card",
        "status": "idle",
        "current_location": "berth_B01",
        "efficiency_rate": 15
    },
    {
        "equip_id": "YT02",
        "equip_type": "yard_truck",
        "equip_name": "2Number set card",
        "status": "working",
        "current_location": "yard_A01",
        "efficiency_rate": 15
    }
]

ORIGINAL_TASKS = [
    {
        "task_id": "T0001",
        "task_type": "discharge",
        "status": "in_progress",
        "equip_id": "QC02",
        "container_id": "ABCD1234567",
        "vessel_id": "V002",
        "source_location": "vessel_V002",
        "target_location": "yard_A01",
        "created_at": "2026-09-14T06:30:00",
        "estimated_duration": 45
    },
    {
        "task_id": "T0002",
        "task_type": "load",
        "status": "pending",
        "equip_id": None,
        "container_id": "EFGH7654321",
        "vessel_id": "V001",
        "source_location": "yard_B01",
        "target_location": "vessel_V001",
        "created_at": "2026-09-14T08:00:00",
        "estimated_duration": 30
    }
]

DATA_DIR = os.path.join(project_root, "data")


def reset_test_data():
    """Reset the test data to the initial state"""
    equipment_path = os.path.join(DATA_DIR, "equipment.json")
    tasks_path = os.path.join(DATA_DIR, "tasks.json")

    with open(equipment_path, "w", encoding="utf-8") as f:
        json.dump({"equipment": ORIGINAL_EQUIPMENT}, f, ensure_ascii=False, indent=2)

    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump({"tasks": ORIGINAL_TASKS}, f, ensure_ascii=False, indent=2)


class TestQueryEquipmentStatus:
    """Test device status inquiry"""

    def setup_method(self):
        reset_test_data()

    def test_query_all_equipment(self, setup_session):
        """Test and query all devices"""
        result = run_with_session("query_equipment_status", {}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 6
        assert len(result["equipment"]) == 6

    def test_query_by_equip_id(self, setup_session):
        """Test query by device ID"""
        result = run_with_session("query_equipment_status", {"equip_id": "QC01"}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["equipment"][0]["equip_id"] == "QC01"
        assert result["equipment"][0]["equip_name"] == "1No. Anqiao"

    def test_query_by_equip_type(self, setup_session):
        """Test query by device type"""
        result = run_with_session("query_equipment_status", {"equip_type": "quay_crane"}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 2
        for e in result["equipment"]:
            assert e["equip_type"] == "quay_crane"

    def test_query_by_status(self, setup_session):
        """Test query by status"""
        result = run_with_session("query_equipment_status", {"status": "idle"}, setup_session)
        assert result["status"] == "success"
        for e in result["equipment"]:
            assert e["status"] == "idle"

    def test_query_with_combined_filters(self, setup_session):
        """Test combination filtering"""
        result = run_with_session("query_equipment_status", {
            "equip_type": "quay_crane",
            "status": "idle"
        }, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["equipment"][0]["equip_id"] == "QC01"

    def test_query_nonexistent_equipment(self, setup_session):
        """Test and query non-existent devices"""
        result = run_with_session("query_equipment_status", {"equip_id": "QC99"}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 0

    def test_query_invalid_equipment_type(self, setup_session):
        """Test the type of invalid device"""
        result = run_with_session("query_equipment_status", {"equip_type": "invalid_type"}, setup_session)
        assert result["status"] == "error"
        assert "Invalid device type" in result["error"]


class TestQueryEquipmentTask:
    """Test equipment task inquiry"""

    def setup_method(self):
        reset_test_data()

    def test_query_all_tasks(self, setup_session):
        """Test and query all tasks"""
        result = run_with_session("query_equipment_task", {}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 2

    def test_query_by_task_id(self, setup_session):
        """Test query by task ID"""
        result = run_with_session("query_equipment_task", {"task_id": "T0001"}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["tasks"][0]["task_id"] == "T0001"
        assert result["tasks"][0]["equip_id"] == "QC02"

    def test_query_by_equip_id(self, setup_session):
        """Test query tasks by device ID"""
        result = run_with_session("query_equipment_task", {"equip_id": "QC02"}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["tasks"][0]["equip_id"] == "QC02"

    def test_query_by_status(self, setup_session):
        """Test query tasks by status"""
        result = run_with_session("query_equipment_task", {"status": "pending"}, setup_session)
        assert result["status"] == "success"
        assert result["count"] == 1
        assert result["tasks"][0]["task_id"] == "T0002"

    def test_query_invalid_task_status(self, setup_session):
        """Test the invalid task status"""
        result = run_with_session("query_equipment_task", {"status": "invalid_status"}, setup_session)
        assert result["status"] == "error"
        assert "Invalid task status" in result["error"]


class TestDispatchEquipment:
    """Dispatch of test equipment"""

    def setup_method(self):
        reset_test_data()

    def test_dispatch_success(self, setup_session):
        """Successful dispatch of workers in the test"""
        result = run_with_session("dispatch_equipment", {
            "equip_id": "QC01",
            "task_id": "T0002"
        }, setup_session)
        assert result["status"] == "success"
        assert "successfully assigned" in result["message"]

    def test_dispatch_missing_equip_id(self, setup_session):
        """Missing equipment in the testID"""
        result = run_with_session("dispatch_equipment", {"task_id": "T0002"}, setup_session)
        assert result["status"] == "error"
        assert "The required parameters are missing: equip_id" in result["error"]

    def test_dispatch_missing_task_id(self, setup_session):
        """Missing tasks in the testID"""
        result = run_with_session("dispatch_equipment", {"equip_id": "QC01"}, setup_session)
        assert result["status"] == "error"
        assert "The required parameters are missing: task_id" in result["error"]

    def test_dispatch_nonexistent_equipment(self, setup_session):
        """The test device does not exist."""
        result = run_with_session("dispatch_equipment", {
            "equip_id": "QC99",
            "task_id": "T0002"
        }, setup_session)
        assert result["status"] == "error"
        assert "Device QC99 does not exist" in result["error"]

    def test_dispatch_nonexistent_task(self, setup_session):
        """The test task does not exist."""
        result = run_with_session("dispatch_equipment", {
            "equip_id": "QC01",
            "task_id": "T9999"
        }, setup_session)
        assert result["status"] == "error"
        assert "Task T9999 does not exist" in result["error"]

    def test_dispatch_equipment_not_idle(self, setup_session):
        """The test equipment is not free."""
        result = run_with_session("dispatch_equipment", {
            "equip_id": "QC02",
            "task_id": "T0002"
        }, setup_session)
        assert result["status"] == "error"
        assert "unable to dispatch" in result["error"]
        assert "working" in result["error"]
        assert "alternatives" in result
        assert len(result["alternatives"]) > 0
        assert any(a["equip_id"] == "QC01" for a in result["alternatives"])

    def test_dispatch_task_already_assigned(self, setup_session):
        """The test task has been assigned to other devices."""
        # Assign tasks first
        run_with_session("dispatch_equipment", {"equip_id": "QC01", "task_id": "T0002"}, setup_session)
        # Try to redistribute
        result = run_with_session("dispatch_equipment", {
            "equip_id": "RTG01",
            "task_id": "T0002"
        }, setup_session)
        assert result["status"] == "error"
        assert "assigned to the device" in result["error"]


class TestUpdateEquipmentStatus:
    """Test device status update"""

    def setup_method(self):
        reset_test_data()

    def test_update_status_success(self, setup_session):
        """The test is successful and the status is updated"""
        result = run_with_session("update_equipment_status", {
            "equip_id": "QC01",
            "status": "maintenance"
        }, setup_session)
        assert result["status"] == "success"
        assert "updated from idle to maintenance" in result["message"]

    def test_update_status_with_location(self, setup_session):
        """Test the status and location of the update"""
        result = run_with_session("update_equipment_status", {
            "equip_id": "YT01",
            "status": "moving",
            "current_location": "yard_B02"
        }, setup_session)
        assert result["status"] == "success"

    def test_update_missing_equip_id(self, setup_session):
        """Missing equipment in the testID"""
        result = run_with_session("update_equipment_status", {"status": "idle"}, setup_session)
        assert result["status"] == "error"
        assert "The required parameters are missing: equip_id" in result["error"]

    def test_update_missing_status(self, setup_session):
        """The test is missing."""
        result = run_with_session("update_equipment_status", {"equip_id": "QC01"}, setup_session)
        assert result["status"] == "error"
        assert "The required parameters are missing: status" in result["error"]

    def test_update_nonexistent_equipment(self, setup_session):
        """The test device does not exist."""
        result = run_with_session("update_equipment_status", {
            "equip_id": "QC99",
            "status": "idle"
        }, setup_session)
        assert result["status"] == "error"
        assert "Device QC99 does not exist" in result["error"]

    def test_update_invalid_status(self, setup_session):
        """Invalid status of the test"""
        result = run_with_session("update_equipment_status", {
            "equip_id": "QC01",
            "status": "invalid_status"
        }, setup_session)
        assert result["status"] == "error"
        assert "Invalid device status" in result["error"]

    def test_update_to_idle_clears_task(self, setup_session):
        """Clear the task when the test update is idle."""
        # Assign tasks first
        run_with_session("dispatch_equipment", {"equip_id": "QC01", "task_id": "T0002"}, setup_session)
        # Update to idle
        result = run_with_session("update_equipment_status", {
            "equip_id": "QC01",
            "status": "idle"
        }, setup_session)
        assert result["status"] == "success"


class TestCancelTask:
    """Test cancellation task"""

    def setup_method(self):
        reset_test_data()

    def test_cancel_pending_task(self, setup_session):
        """Test and cancel pending tasks"""
        result = run_with_session("cancel_task", {"task_id": "T0002"}, setup_session)
        assert result["status"] == "success"
        assert "canceled" in result["message"].lower()

    def test_cancel_in_progress_task(self, setup_session):
        """Test to cancel the task in progress and release the device"""
        result = run_with_session("cancel_task", {"task_id": "T0001"}, setup_session)
        assert result["status"] == "success"
        assert "canceled" in result["message"].lower()
        assert "released_equipment" in result
        assert result["released_equipment"]["equip_id"] == "QC02"
        assert result["released_equipment"]["new_status"] == "idle"

    def test_cancel_missing_task_id(self, setup_session):
        """Missing tasks in the testID"""
        result = run_with_session("cancel_task", {}, setup_session)
        assert result["status"] == "error"
        assert "The required parameters are missing: task_id" in result["error"]

    def test_cancel_nonexistent_task(self, setup_session):
        """The test task does not exist."""
        result = run_with_session("cancel_task", {"task_id": "T9999"}, setup_session)
        assert result["status"] == "error"
        assert "Task T9999 does not exist" in result["error"]

    def test_cancel_already_cancelled_task(self, setup_session):
        """Test cancellation of canceled tasks"""
        # Cancel the task first.
        run_with_session("cancel_task", {"task_id": "T0002"}, setup_session)
        # Cancel again
        result = run_with_session("cancel_task", {"task_id": "T0002"}, setup_session)
        assert result["status"] == "error"
        assert "canceled" in result["error"].lower()


class TestHandlerUnknownIntent:
    """Test the unknown intention"""

    def setup_method(self):
        reset_test_data()

    def test_unknown_intent(self, setup_session):
        """Test unknown operations"""
        result = run_with_session("unknown_operation", {}, setup_session)
        assert result["status"] == "error"
        assert "Unknown operation" in result["error"]
        assert "available operation" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
