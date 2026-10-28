"""
DataStore Data persistence layer test
"""

import os
import tempfile
import shutil
from datetime import datetime

import pytest

from models import (
    Vessel,
    Berth,
    YardBlock,
    Container,
    Equipment,
    Task,
    GateChannel,
    Appointment,
    ExecutionRecord,
    VesselStatus,
    BerthStatus,
    BlockStatus,
    ContainerType,
    ContainerSize,
    EquipmentType,
    EquipmentStatus,
    TaskType,
    TaskStatus,
    GateChannelType,
    GateChannelStatus,
    AppointmentStatus,
)

# Import DataStore - will fail initially, which is expected in TDD
from apis.data_store import DataStore


class TestDataStore:
    """DataStore Test class"""

    @pytest.fixture
    def temp_data_dir(self):
        """Create a temporary data directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def data_store(self, temp_data_dir):
        """Create a DataStore instance"""
        return DataStore(data_dir=temp_data_dir)

    def test_data_store_save_and_load_vessels(self, data_store):
        """Test the storage and loading of ship data"""
        vessels = [
            Vessel(
                vessel_id="V001",
                vessel_name="Pacific Star",
                length=300.5,
                draft=12.5,
                eta="2024-01-15T08:00:00",
                container_count=5000,
                inbound_containers=2500,
                outbound_containers=2500,
            ),
            Vessel(
                vessel_id="V002",
                vessel_name="Oriental Pearl",
                length=250.0,
                draft=10.0,
                eta="2024-01-16T10:00:00",
                status=VesselStatus.BERTHED,
                assigned_berth="B01",
                container_count=3000,
                inbound_containers=1500,
                outbound_containers=1500,
            ),
        ]

        # Save data
        data_store.save_vessels(vessels)

        # Load data
        loaded_vessels = data_store.load_vessels()

        # Verify the data
        assert len(loaded_vessels) == 2
        assert loaded_vessels[0].vessel_id == "V001"
        assert loaded_vessels[0].vessel_name == "Pacific Star"
        assert loaded_vessels[1].vessel_id == "V002"
        assert loaded_vessels[1].status == VesselStatus.BERTHED

    def test_data_store_load_empty(self, data_store):
        """Test loading empty data"""
        # When the data file does not exist, an empty list should be returned.
        vessels = data_store.load_vessels()
        assert vessels == []

        berths = data_store.load_berths()
        assert berths == []

        equipment = data_store.load_equipment()
        assert equipment == []

    def test_data_store_save_and_load_berths(self, data_store):
        """Test the storage and loading of berth data"""
        berths = [
            Berth(
                berth_id="B01",
                berth_name="No.1 berth",
                length=350.0,
                max_draft=16.0,
            ),
            Berth(
                berth_id="B02",
                berth_name="Parking space No.2",
                length=400.0,
                max_draft=18.0,
                status=BerthStatus.OCCUPIED,
                current_vessel="V001",
            ),
        ]

        # Save data
        data_store.save_berths(berths)

        # Load data
        loaded_berths = data_store.load_berths()

        # Verify the data
        assert len(loaded_berths) == 2
        assert loaded_berths[0].berth_id == "B01"
        assert loaded_berths[0].berth_name == "No.1 berth"
        assert loaded_berths[1].berth_id == "B02"
        assert loaded_berths[1].status == BerthStatus.OCCUPIED
        assert loaded_berths[1].current_vessel == "V001"

    def test_data_store_save_and_load_equipment(self, data_store):
        """Save and load the data of the test device"""
        equipment = [
            Equipment(
                equip_id="QC01",
                equip_type=EquipmentType.QUAY_CRANE,
                equip_name="No.1 Shore Bridge",
                berth_id="B01",
            ),
            Equipment(
                equip_id="RTG05",
                equip_type=EquipmentType.RTG,
                equip_name="No. 5 tire crane",
                status=EquipmentStatus.WORKING,
                block_id="A01",
            ),
            Equipment(
                equip_id="YT12",
                equip_type=EquipmentType.YARD_TRUCK,
                equip_name="No. 12 collection card",
                status=EquipmentStatus.MOVING,
                current_location="A01Ou",
            ),
        ]

        # Save data
        data_store.save_equipment(equipment)

        # Load data
        loaded_equipment = data_store.load_equipment()

        # Verify the data
        assert len(loaded_equipment) == 3
        assert loaded_equipment[0].equip_id == "QC01"
        assert loaded_equipment[0].equip_type == EquipmentType.QUAY_CRANE
        assert loaded_equipment[1].equip_id == "RTG05"
        assert loaded_equipment[1].status == EquipmentStatus.WORKING
        assert loaded_equipment[2].equip_id == "YT12"
        assert loaded_equipment[2].current_location == "A01Ou"


class TestDataStoreAdditionalModels:
    """DataStore Additional model test"""

    @pytest.fixture
    def temp_data_dir(self):
        """Create a temporary data directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def data_store(self, temp_data_dir):
        """Create a DataStore instance"""
        return DataStore(data_dir=temp_data_dir)

    def test_data_store_save_and_load_yard_blocks(self, data_store):
        """Test the storage and loading of warehouse block data"""
        blocks = [
            YardBlock(
                block_id="A01",
                block_name="ADistrict No. 1 Import Box Store",
                type=ContainerType.IMPORT,
                capacity=1500,
                occupied=850,
            ),
            YardBlock(
                block_id="B01",
                block_name="BDistrict No. 1 Exit Box Stort",
                type=ContainerType.EXPORT,
                capacity=1200,
                occupied=300,
                tiers_max=6,
            ),
        ]

        data_store.save_yard_blocks(blocks)
        loaded_blocks = data_store.load_yard_blocks()

        assert len(loaded_blocks) == 2
        assert loaded_blocks[0].block_id == "A01"
        assert loaded_blocks[0].type == ContainerType.IMPORT
        assert loaded_blocks[1].block_id == "B01"
        assert loaded_blocks[1].tiers_max == 6

    def test_data_store_save_and_load_containers(self, data_store):
        """Test the storage and loading of container data"""
        containers = [
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.FORTY_GP,
                type=ContainerType.IMPORT,
                weight=25.5,
                vessel_id="V001",
                block_id="A01",
                bay=10,
                row=6,
                tier=4,
            ),
            Container(
                container_id="CMAU9876543",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=15.0,
                block_id="B01",
            ),
        ]

        data_store.save_containers(containers)
        loaded_containers = data_store.load_containers()

        assert len(loaded_containers) == 2
        assert loaded_containers[0].container_id == "MSCU1234567"
        assert loaded_containers[0].size == ContainerSize.FORTY_GP
        assert loaded_containers[1].container_id == "CMAU9876543"
        assert loaded_containers[1].tier is None

    def test_data_store_save_and_load_tasks(self, data_store):
        """Storage and loading of test task data"""
        tasks = [
            Task(
                task_id="T0001",
                task_type=TaskType.DISCHARGE,
                status=TaskStatus.ASSIGNED,
                equip_id="QC01",
                vessel_id="V001",
            ),
            Task(
                task_id="T0002",
                task_type=TaskType.LOAD,
                status=TaskStatus.IN_PROGRESS,
                equip_id="QC02",
                estimated_duration=45,
            ),
        ]

        data_store.save_tasks(tasks)
        loaded_tasks = data_store.load_tasks()

        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].task_id == "T0001"
        assert loaded_tasks[0].task_type == TaskType.DISCHARGE
        assert loaded_tasks[1].status == TaskStatus.IN_PROGRESS

    def test_data_store_save_and_load_gate_channels(self, data_store):
        """Test the storage and loading of gate channel data"""
        channels = [
            GateChannel(
                channel_id="G01",
                channel_name="Gate passage No.1",
                type=GateChannelType.INBOUND,
                queue_length=5,
            ),
            GateChannel(
                channel_id="G02",
                channel_name="Exit channel No.2",
                type=GateChannelType.OUTBOUND,
                status=GateChannelStatus.CLOSED,
            ),
        ]

        data_store.save_gate_channels(channels)
        loaded_channels = data_store.load_gate_channels()

        assert len(loaded_channels) == 2
        assert loaded_channels[0].channel_id == "G01"
        assert loaded_channels[0].type == GateChannelType.INBOUND
        assert loaded_channels[1].status == GateChannelStatus.CLOSED

    def test_data_store_save_and_load_appointments(self, data_store):
        """Test the saving and loading of appointment data"""
        appointments = [
            Appointment(
                appointment_id="AP001",
                truck_id="T001",
                driver_name="Zhang San",
                appointment_time="2024-01-15T08:00:00",
                type=TaskType.GATE_OUT,
                container_id="MSCU1234567",
            ),
            Appointment(
                appointment_id="AP002",
                truck_id="T002",
                driver_name="Li Si",
                appointment_time="2024-01-15T09:00:00",
                type=TaskType.GATE_IN,
                container_id="CMAU9876543",
                status=AppointmentStatus.VALID,
            ),
        ]

        data_store.save_appointments(appointments)
        loaded_appointments = data_store.load_appointments()

        assert len(loaded_appointments) == 2
        assert loaded_appointments[0].appointment_id == "AP001"
        assert loaded_appointments[0].driver_name == "Zhang San"
        assert loaded_appointments[1].status == AppointmentStatus.VALID

    def test_data_store_save_and_load_execution_records(self, data_store):
        """Test the saving and loading of the record data"""
        records = [
            ExecutionRecord(
                execution_id="EX0001",
                action="discharge",
                params={"vessel_id": "V001"},
                issued_by="scheduler",
                started_at="2024-01-15T08:00:00",
                estimated_duration=120,
            ),
            ExecutionRecord(
                execution_id="EX0002",
                action="load",
                params={"vessel_id": "V002"},
                issued_by="planner",
                status=TaskStatus.IN_PROGRESS,
                started_at="2024-01-15T10:00:00",
                estimated_duration=90,
            ),
        ]

        data_store.save_execution_records(records)
        loaded_records = data_store.load_execution_records()

        assert len(loaded_records) == 2
        assert loaded_records[0].execution_id == "EX0001"
        assert loaded_records[0].action == "discharge"
        assert loaded_records[1].status == TaskStatus.IN_PROGRESS
