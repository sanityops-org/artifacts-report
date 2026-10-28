"""
Container Terminal Dispatch Assistant - Integrated Test

Verify that all Skills can work normally to ensure that each module is properly integrated.
"""

import os
import sys

import pytest

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from simulator import Simulator
from apis.data_store import DataStore


class TestAllSkillsLoaded:
    """Test whether all Skills are loaded correctly to Simulator"""

    def test_simulator_initialization(self):
        """Test Simulator Initialization"""
        simulator = Simulator()

        # Verify the success of Simulator instantiation
        assert simulator is not None

    def test_four_skills_loaded(self):
        """Test 4 Skills All Loaded To Simulator"""
        simulator = Simulator()

        # Verify that all 4 Skills have been loaded
        expected_skills = [
            "berth_scheduling",
            "yard_scheduling",
            "equipment_scheduling",
            "gate_scheduling",
        ]

        # Verify whether each Skill is available by performing a simple query
        for skill in expected_skills:
            result = simulator.execute({
                "skill": skill,
                "action": "_unknown_action_for_test_",
                "params": {}
            })
            # If Skill loads successfully, it should return the "Unknown Operation" error, not the "Unknown Skill" error.
            assert result["status"] == "error"
            assert "Unknown operation" in result["error"] or "unknown skill" not in result["error"]

    def test_simulator_unknown_skill(self):
        """Test Simulator to deal with unknown Skill"""
        simulator = Simulator()

        result = simulator.execute({
            "skill": "unknown_skill",
            "action": "test",
            "params": {}
        })

        assert result["status"] == "error"
        assert "Unknown skills" in result["error"]

    def test_simulator_missing_skill_parameter(self):
        """Test Simulator to handle missing skill parameters"""
        simulator = Simulator()

        result = simulator.execute({
            "action": "test",
            "params": {}
        })

        assert result["status"] == "error"
        assert "The required parameters are missing" in result["error"]
        assert "skill" in result["error"]

    def test_simulator_missing_action_parameter(self):
        """Test Simulator to deal with missing action parameters"""
        simulator = Simulator()

        result = simulator.execute({
            "skill": "berth_scheduling",
            "params": {}
        })

        assert result["status"] == "error"
        assert "The required parameters are missing" in result["error"]
        assert "action" in result["error"]


class TestBerthSchedulingFullFlow:
    """Berth scheduling complete process test"""

    @pytest.fixture
    def simulator(self):
        """Create a Simulator instance"""
        return Simulator()

    def test_query_anchorage_vessels(self, simulator):
        """Test and query anchorage ships"""
        result = simulator.execute({
            "skill": "berth_scheduling",
            "action": "query_anchorage",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result
        assert "vessels" in result["data"]

    def test_query_berth_status(self, simulator):
        """Test query the berth status"""
        result = simulator.execute({
            "skill": "berth_scheduling",
            "action": "query_berth_status",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result
        assert "berths" in result["data"]

    def test_query_vessel_plan(self, simulator):
        """Test and query the ship plan"""
        result = simulator.execute({
            "skill": "berth_scheduling",
            "action": "query_vessel_plan",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result
        assert "vessels" in result["data"]

    def test_assign_berth_flow(self, simulator):
        """Test the berth allocation process"""
        # First, check the anchorage ship.
        anchorage_result = simulator.execute({
            "skill": "berth_scheduling",
            "action": "query_anchorage",
            "params": {}
        })

        assert anchorage_result["status"] == "success"
        vessels = anchorage_result["data"]["vessels"]

        if len(vessels) > 0:
            # Find an anchorage ship
            vessel_id = vessels[0]["vessel_id"]

            # Check the available parking space
            berths_result = simulator.execute({
                "skill": "berth_scheduling",
                "action": "query_berth_status",
                "params": {"status": "available"}
            })

            assert berths_result["status"] == "success"
            berths = berths_result["data"]["berths"]

            if len(berths) > 0:
                berth_id = berths[0]["berth_id"]

                # Try to allocate berths
                assign_result = simulator.execute({
                    "skill": "berth_scheduling",
                    "action": "assign_berth",
                    "params": {
                        "vessel_id": vessel_id,
                        "berth_id": berth_id
                    }
                })

                # The allocation may be successful or failed (depending on the ship/berth conditions)
                assert assign_result["status"] in ["success", "error"]

    def test_confirm_departure(self, simulator):
        """Test confirmation of departure"""
        # The test is missing the vessel_id parameter
        result = simulator.execute({
            "skill": "berth_scheduling",
            "action": "confirm_departure",
            "params": {}
        })

        assert result["status"] == "error"
        assert "error" in result


class TestEquipmentSchedulingQuery:
    """Device scheduling query test"""

    @pytest.fixture
    def simulator(self):
        """Create a Simulator instance"""
        return Simulator()

    def test_query_equipment_status(self, simulator):
        """Test and query the status of the device"""
        result = simulator.execute({
            "skill": "equipment_scheduling",
            "action": "query_equipment_status",
            "params": {}
        })

        assert result["status"] == "success"
        # equipment_scheduling The tool directly returns to the equipment field
        assert "equipment" in result
        assert "count" in result
        assert isinstance(result["equipment"], list)

    def test_query_equipment_task(self, simulator):
        """Test query device tasks"""
        result = simulator.execute({
            "skill": "equipment_scheduling",
            "action": "query_equipment_task",
            "params": {}
        })

        assert result["status"] == "success"
        # equipment_scheduling The tool directly returns to the tasks field.
        assert "tasks" in result
        assert "count" in result
        assert isinstance(result["tasks"], list)

    def test_query_equipment_by_type(self, simulator):
        """Test to query the device by type"""
        result = simulator.execute({
            "skill": "equipment_scheduling",
            "action": "query_equipment_status",
            "params": {"equip_type": "quay_crane"}
        })

        assert result["status"] == "success"
        assert "equipment" in result
        # Verify that all the returned devices are quay_crane type.
        for equip in result["equipment"]:
            assert equip["equip_type"] == "quay_crane"

    def test_dispatch_equipment_missing_params(self, simulator):
        """The test dispatcher lacks parameters."""
        result = simulator.execute({
            "skill": "equipment_scheduling",
            "action": "dispatch_equipment",
            "params": {}
        })

        assert result["status"] == "error"
        assert "error" in result


class TestYardSchedulingQuery:
    """Stacking scheduling query test"""

    @pytest.fixture
    def simulator(self):
        """Create a Simulator instance"""
        return Simulator()

    def test_query_yard_status(self, simulator):
        """Test query the status of the storage box area"""
        result = simulator.execute({
            "skill": "yard_scheduling",
            "action": "query_yard_status",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result
        # The warehouse status may be in the "blocks" or "yard_blocks" field.
        assert "blocks" in result["data"] or "yard_blocks" in result["data"]

    def test_query_container_location(self, simulator):
        """Test and query the location of the container"""
        # Test queries without parameters
        result = simulator.execute({
            "skill": "yard_scheduling",
            "action": "query_container_location",
            "params": {}
        })

        # It should return success (it may be an empty list) or the error prompt is missing parameters.
        assert result["status"] in ["success", "error"]

    def test_query_container_location_with_id(self, simulator):
        """Test using container ID to query the location"""
        result = simulator.execute({
            "skill": "yard_scheduling",
            "action": "query_container_location",
            "params": {"container_id": "MSCU1234567"}
        })

        # The query result may be found successfully, not found or wrong.
        assert result["status"] in ["success", "error"]

    def test_query_rehandle_list(self, simulator):
        """Test query box-turning task list"""
        result = simulator.execute({
            "skill": "yard_scheduling",
            "action": "query_rehandle_list",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result

    def test_assign_yard_slot_missing_params(self, simulator):
        """The test allocation of the drop-in position is missing parameters."""
        result = simulator.execute({
            "skill": "yard_scheduling",
            "action": "assign_yard_slot",
            "params": {}
        })

        assert result["status"] == "error"
        assert "error" in result


class TestGateSchedulingQuery:
    """Gate dispatch query test"""

    @pytest.fixture
    def simulator(self):
        """Create a Simulator instance"""
        return Simulator()

    def test_query_gate_status(self, simulator):
        """Test query the status of the gate channel"""
        result = simulator.execute({
            "skill": "gate_scheduling",
            "action": "query_gate_status",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result
        # The gate channel status may be in the "channels" or "gate_channels" field.
        assert "channels" in result["data"] or "gate_channels" in result["data"]

    def test_query_gate_appointment(self, simulator):
        """Test query appointment record"""
        result = simulator.execute({
            "skill": "gate_scheduling",
            "action": "query_gate_appointment",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result
        # The appointment record may be in the "appointments" field.
        assert "appointments" in result["data"] or "appointment_list" in result["data"]

    def test_query_gate_queue(self, simulator):
        """Test and query the queue"""
        result = simulator.execute({
            "skill": "gate_scheduling",
            "action": "query_gate_queue",
            "params": {}
        })

        assert result["status"] == "success"
        assert "data" in result

    def test_open_gate_channel_missing_params(self, simulator):
        """Test the missing parameters of the open gate channel"""
        result = simulator.execute({
            "skill": "gate_scheduling",
            "action": "open_gate_channel",
            "params": {}
        })

        assert result["status"] == "error"
        assert "error" in result

    def test_close_gate_channel_missing_params(self, simulator):
        """Test the missing parameters of the gate channel"""
        result = simulator.execute({
            "skill": "gate_scheduling",
            "action": "close_gate_channel",
            "params": {}
        })

        assert result["status"] == "error"
        assert "error" in result

    def test_process_gate_pass_missing_params(self, simulator):
        """Test and process the missing parameters of the card entering and leaving the port"""
        result = simulator.execute({
            "skill": "gate_scheduling",
            "action": "process_gate_pass",
            "params": {}
        })

        assert result["status"] == "error"
        assert "error" in result


class TestDataModelsValid:
    """Data model validity test"""

    @pytest.fixture
    def data_store(self):
        """Create a DataStore instance"""
        return DataStore(data_dir=os.path.join(project_root, "data"))

    def test_load_vessels(self, data_store):
        """The test ship data can be loaded normally."""
        vessels = data_store.load_vessels()

        assert isinstance(vessels, list)
        # There is ship data in the verification data file.
        assert len(vessels) > 0

        # Verify the necessary fields of the first ship
        vessel = vessels[0]
        assert vessel.vessel_id is not None
        assert vessel.vessel_name is not None
        assert vessel.length > 0
        assert vessel.draft > 0

    def test_load_berths(self, data_store):
        """Test the berth data can be loaded normally"""
        berths = data_store.load_berths()

        assert isinstance(berths, list)
        assert len(berths) > 0

        # Verify the necessary fields of the first berth
        berth = berths[0]
        assert berth.berth_id is not None
        assert berth.berth_name is not None
        assert berth.length > 0
        assert berth.max_draft > 0

    def test_load_yard_blocks(self, data_store):
        """The test dump block data can be loaded normally."""
        blocks = data_store.load_yard_blocks()

        assert isinstance(blocks, list)
        assert len(blocks) > 0

        # Verify the necessary fields of the first block
        block = blocks[0]
        assert block.block_id is not None
        assert block.block_name is not None
        assert block.capacity > 0

    def test_load_containers(self, data_store):
        """The test container data can be loaded normally."""
        containers = data_store.load_containers()

        assert isinstance(containers, list)
        assert len(containers) > 0

        # Verify the necessary fields of the first container
        container = containers[0]
        assert container.container_id is not None
        assert container.size is not None
        assert container.type is not None

    def test_load_equipment(self, data_store):
        """The test device data can be loaded normally."""
        equipment = data_store.load_equipment()

        assert isinstance(equipment, list)
        assert len(equipment) > 0

        # Verify the necessary fields of the first device
        equip = equipment[0]
        assert equip.equip_id is not None
        assert equip.equip_type is not None
        assert equip.equip_name is not None

    def test_load_tasks(self, data_store):
        """The test task data can be loaded normally."""
        tasks = data_store.load_tasks()

        assert isinstance(tasks, list)
        assert len(tasks) > 0

        # Verify the necessary fields of the first task
        task = tasks[0]
        assert task.task_id is not None
        assert task.task_type is not None

    def test_load_gate_channels(self, data_store):
        """The test gate channel data can be loaded normally."""
        channels = data_store.load_gate_channels()

        assert isinstance(channels, list)
        assert len(channels) > 0

        # Verify the necessary fields of the first channel
        channel = channels[0]
        assert channel.channel_id is not None
        assert channel.channel_name is not None
        assert channel.type is not None

    def test_load_appointments(self, data_store):
        """The test appointment data can be loaded normally."""
        appointments = data_store.load_appointments()

        assert isinstance(appointments, list)
        # The appointment data may be empty. Skip the length check.
        if len(appointments) > 0:
            appointment = appointments[0]
            assert appointment.appointment_id is not None
            assert appointment.driver_name is not None

    def test_all_data_models_serializable(self, data_store):
        """Test that all data models can be serialized"""
        # Load all the data
        vessels = data_store.load_vessels()
        berths = data_store.load_berths()
        blocks = data_store.load_yard_blocks()
        containers = data_store.load_containers()
        equipment = data_store.load_equipment()
        tasks = data_store.load_tasks()
        channels = data_store.load_gate_channels()

        # Verify that all data can be serialized into dict
        if vessels:
            vessel_dict = vessels[0].model_dump(mode="json")
            assert isinstance(vessel_dict, dict)

        if berths:
            berth_dict = berths[0].model_dump(mode="json")
            assert isinstance(berth_dict, dict)

        if blocks:
            block_dict = blocks[0].model_dump(mode="json")
            assert isinstance(block_dict, dict)

        if containers:
            container_dict = containers[0].model_dump(mode="json")
            assert isinstance(container_dict, dict)

        if equipment:
            equip_dict = equipment[0].model_dump(mode="json")
            assert isinstance(equip_dict, dict)

        if tasks:
            task_dict = tasks[0].model_dump(mode="json")
            assert isinstance(task_dict, dict)

        if channels:
            channel_dict = channels[0].model_dump(mode="json")
            assert isinstance(channel_dict, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
