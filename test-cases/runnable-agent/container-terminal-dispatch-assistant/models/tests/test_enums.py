"""Tests for enum definitions in models/enums.py"""

import pytest
from models.enums import (
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
    EventType,
)


class TestVesselStatus:
    """Tests for VesselStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required vessel statuses exist"""
        assert hasattr(VesselStatus, 'INBOUND')
        assert hasattr(VesselStatus, 'AT_ANCHOR')
        assert hasattr(VesselStatus, 'BERTHING')
        assert hasattr(VesselStatus, 'BERTHED')
        assert hasattr(VesselStatus, 'WORKING')
        assert hasattr(VesselStatus, 'DEPARTING')
        assert hasattr(VesselStatus, 'DEPARTED')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert VesselStatus.INBOUND.value == "inbound"
        assert VesselStatus.AT_ANCHOR.value == "at_anchor"
        assert VesselStatus.BERTHING.value == "berthing"
        assert VesselStatus.BERTHED.value == "berthed"
        assert VesselStatus.WORKING.value == "working"
        assert VesselStatus.DEPARTING.value == "departing"
        assert VesselStatus.DEPARTED.value == "departed"

    def test_count(self):
        """Test that there are exactly 7 vessel statuses"""
        assert len(list(VesselStatus)) == 7


class TestBerthStatus:
    """Tests for BerthStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required berth statuses exist"""
        assert hasattr(BerthStatus, 'AVAILABLE')
        assert hasattr(BerthStatus, 'OCCUPIED')
        assert hasattr(BerthStatus, 'RESERVED')
        assert hasattr(BerthStatus, 'MAINTENANCE')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert BerthStatus.AVAILABLE.value == "available"
        assert BerthStatus.OCCUPIED.value == "occupied"
        assert BerthStatus.RESERVED.value == "reserved"
        assert BerthStatus.MAINTENANCE.value == "maintenance"

    def test_count(self):
        """Test that there are exactly 4 berth statuses"""
        assert len(list(BerthStatus)) == 4


class TestBlockStatus:
    """Tests for BlockStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required block statuses exist"""
        assert hasattr(BlockStatus, 'OPERATIONAL')
        assert hasattr(BlockStatus, 'FULL')
        assert hasattr(BlockStatus, 'CLOSED')
        assert hasattr(BlockStatus, 'MAINTENANCE')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert BlockStatus.OPERATIONAL.value == "operational"
        assert BlockStatus.FULL.value == "full"
        assert BlockStatus.CLOSED.value == "closed"
        assert BlockStatus.MAINTENANCE.value == "maintenance"

    def test_count(self):
        """Test that there are exactly 4 block statuses"""
        assert len(list(BlockStatus)) == 4


class TestContainerType:
    """Tests for ContainerType enum"""

    def test_has_all_required_values(self):
        """Test that all required container types exist"""
        assert hasattr(ContainerType, 'IMPORT')
        assert hasattr(ContainerType, 'EXPORT')
        assert hasattr(ContainerType, 'TRANSSHIPMENT')
        assert hasattr(ContainerType, 'EMPTY')
        assert hasattr(ContainerType, 'DANGEROUS')
        assert hasattr(ContainerType, 'REEFER')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert ContainerType.IMPORT.value == "import"
        assert ContainerType.EXPORT.value == "export"
        assert ContainerType.TRANSSHIPMENT.value == "transshipment"
        assert ContainerType.EMPTY.value == "empty"
        assert ContainerType.DANGEROUS.value == "dangerous"
        assert ContainerType.REEFER.value == "reefer"

    def test_count(self):
        """Test that there are exactly 6 container types"""
        assert len(list(ContainerType)) == 6


class TestContainerSize:
    """Tests for ContainerSize enum"""

    def test_has_all_required_values(self):
        """Test that all required container sizes exist"""
        assert hasattr(ContainerSize, 'TWENTY_GP')
        assert hasattr(ContainerSize, 'FORTY_GP')
        assert hasattr(ContainerSize, 'FORTY_HQ')
        assert hasattr(ContainerSize, 'FORTY_FIVE_LHC')

    def test_values(self):
        """Test that enum values match ISO container codes"""
        assert ContainerSize.TWENTY_GP.value == "20GP"
        assert ContainerSize.FORTY_GP.value == "40GP"
        assert ContainerSize.FORTY_HQ.value == "40HQ"
        assert ContainerSize.FORTY_FIVE_LHC.value == "45LHC"

    def test_count(self):
        """Test that there are exactly 4 container sizes"""
        assert len(list(ContainerSize)) == 4

    def test_aliases_for_common_names(self):
        """Test that common aliases exist for convenience"""
        # Allow users to use GP20, GP40, HQ40 etc.
        assert ContainerSize.GP20.value == "20GP"
        assert ContainerSize.GP40.value == "40GP"
        assert ContainerSize.HQ40.value == "40HQ"


class TestEquipmentType:
    """Tests for EquipmentType enum"""

    def test_has_all_required_values(self):
        """Test that all required equipment types exist"""
        assert hasattr(EquipmentType, 'QUAY_CRANE')
        assert hasattr(EquipmentType, 'RTG')
        assert hasattr(EquipmentType, 'RMG')
        assert hasattr(EquipmentType, 'YARD_TRUCK')
        assert hasattr(EquipmentType, 'REACH_STACKER')
        assert hasattr(EquipmentType, 'TOP_LOADER')

    def test_values(self):
        """Test that enum values are lowercase with underscores"""
        assert EquipmentType.QUAY_CRANE.value == "quay_crane"
        assert EquipmentType.RTG.value == "rtg"
        assert EquipmentType.RMG.value == "rmg"
        assert EquipmentType.YARD_TRUCK.value == "yard_truck"
        assert EquipmentType.REACH_STACKER.value == "reach_stacker"
        assert EquipmentType.TOP_LOADER.value == "top_loader"

    def test_count(self):
        """Test that there are exactly 6 equipment types"""
        assert len(list(EquipmentType)) == 6


class TestEquipmentStatus:
    """Tests for EquipmentStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required equipment statuses exist"""
        assert hasattr(EquipmentStatus, 'IDLE')
        assert hasattr(EquipmentStatus, 'WORKING')
        assert hasattr(EquipmentStatus, 'MOVING')
        assert hasattr(EquipmentStatus, 'FAULT')
        assert hasattr(EquipmentStatus, 'MAINTENANCE')
        assert hasattr(EquipmentStatus, 'OFFLINE')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert EquipmentStatus.IDLE.value == "idle"
        assert EquipmentStatus.WORKING.value == "working"
        assert EquipmentStatus.MOVING.value == "moving"
        assert EquipmentStatus.FAULT.value == "fault"
        assert EquipmentStatus.MAINTENANCE.value == "maintenance"
        assert EquipmentStatus.OFFLINE.value == "offline"

    def test_count(self):
        """Test that there are exactly 6 equipment statuses"""
        assert len(list(EquipmentStatus)) == 6


class TestTaskType:
    """Tests for TaskType enum"""

    def test_has_all_required_values(self):
        """Test that all required task types exist"""
        assert hasattr(TaskType, 'LOAD')
        assert hasattr(TaskType, 'DISCHARGE')
        assert hasattr(TaskType, 'YARD_MOVE')
        assert hasattr(TaskType, 'GATE_OUT')
        assert hasattr(TaskType, 'GATE_IN')

    def test_values(self):
        """Test that enum values are lowercase with underscores"""
        assert TaskType.LOAD.value == "load"
        assert TaskType.DISCHARGE.value == "discharge"
        assert TaskType.YARD_MOVE.value == "yard_move"
        assert TaskType.GATE_OUT.value == "gate_out"
        assert TaskType.GATE_IN.value == "gate_in"

    def test_count(self):
        """Test that there are exactly 5 task types"""
        assert len(list(TaskType)) == 5


class TestTaskStatus:
    """Tests for TaskStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required task statuses exist"""
        assert hasattr(TaskStatus, 'PENDING')
        assert hasattr(TaskStatus, 'ASSIGNED')
        assert hasattr(TaskStatus, 'IN_PROGRESS')
        assert hasattr(TaskStatus, 'COMPLETED')
        assert hasattr(TaskStatus, 'FAILED')
        assert hasattr(TaskStatus, 'CANCELLED')

    def test_values(self):
        """Test that enum values are lowercase with underscores"""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.ASSIGNED.value == "assigned"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.COMPLETED.value == "completed"
        assert TaskStatus.FAILED.value == "failed"
        assert TaskStatus.CANCELLED.value == "cancelled"

    def test_count(self):
        """Test that there are exactly 6 task statuses"""
        assert len(list(TaskStatus)) == 6


class TestGateChannelType:
    """Tests for GateChannelType enum"""

    def test_has_all_required_values(self):
        """Test that all required gate channel types exist"""
        assert hasattr(GateChannelType, 'INBOUND')
        assert hasattr(GateChannelType, 'OUTBOUND')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert GateChannelType.INBOUND.value == "inbound"
        assert GateChannelType.OUTBOUND.value == "outbound"

    def test_count(self):
        """Test that there are exactly 2 gate channel types"""
        assert len(list(GateChannelType)) == 2


class TestGateChannelStatus:
    """Tests for GateChannelStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required gate channel statuses exist"""
        assert hasattr(GateChannelStatus, 'OPEN')
        assert hasattr(GateChannelStatus, 'CLOSED')
        assert hasattr(GateChannelStatus, 'CONGESTED')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert GateChannelStatus.OPEN.value == "open"
        assert GateChannelStatus.CLOSED.value == "closed"
        assert GateChannelStatus.CONGESTED.value == "congested"

    def test_count(self):
        """Test that there are exactly 3 gate channel statuses"""
        assert len(list(GateChannelStatus)) == 3


class TestAppointmentStatus:
    """Tests for AppointmentStatus enum"""

    def test_has_all_required_values(self):
        """Test that all required appointment statuses exist"""
        assert hasattr(AppointmentStatus, 'PENDING')
        assert hasattr(AppointmentStatus, 'VALID')
        assert hasattr(AppointmentStatus, 'EXPIRED')
        assert hasattr(AppointmentStatus, 'COMPLETED')
        assert hasattr(AppointmentStatus, 'CANCELLED')

    def test_values(self):
        """Test that enum values are lowercase strings"""
        assert AppointmentStatus.PENDING.value == "pending"
        assert AppointmentStatus.VALID.value == "valid"
        assert AppointmentStatus.EXPIRED.value == "expired"
        assert AppointmentStatus.COMPLETED.value == "completed"
        assert AppointmentStatus.CANCELLED.value == "cancelled"

    def test_count(self):
        """Test that there are exactly 5 appointment statuses"""
        assert len(list(AppointmentStatus)) == 5


class TestEventType:
    """Tests for EventType enum"""

    def test_has_all_required_values(self):
        """Test that all required event types exist"""
        assert hasattr(EventType, 'TASK_STARTED')
        assert hasattr(EventType, 'TASK_PROGRESS')
        assert hasattr(EventType, 'TASK_COMPLETED')
        assert hasattr(EventType, 'TASK_FAILED')
        assert hasattr(EventType, 'STATUS_CHANGED')
        assert hasattr(EventType, 'ALERT')

    def test_values(self):
        """Test that enum values are lowercase with underscores"""
        assert EventType.TASK_STARTED.value == "task_started"
        assert EventType.TASK_PROGRESS.value == "task_progress"
        assert EventType.TASK_COMPLETED.value == "task_completed"
        assert EventType.TASK_FAILED.value == "task_failed"
        assert EventType.STATUS_CHANGED.value == "status_changed"
        assert EventType.ALERT.value == "alert"

    def test_count(self):
        """Test that there are exactly 6 event types"""
        assert len(list(EventType)) == 6


class TestEnumFromString:
    """Tests for creating enums from string values"""

    def test_vessel_status_from_string(self):
        """Test creating VesselStatus from string"""
        assert VesselStatus("inbound") == VesselStatus.INBOUND
        assert VesselStatus("berthed") == VesselStatus.BERTHED

    def test_task_status_from_string(self):
        """Test creating TaskStatus from string"""
        assert TaskStatus("pending") == TaskStatus.PENDING
        assert TaskStatus("completed") == TaskStatus.COMPLETED

    def test_invalid_string_raises_error(self):
        """Test that invalid string raises ValueError"""
        with pytest.raises(ValueError):
            VesselStatus("invalid_status")