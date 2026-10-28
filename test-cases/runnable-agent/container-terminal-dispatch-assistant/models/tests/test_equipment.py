"""
Equipment and task model test

Test the creation, verification and constraint of Equipment and Task Pydantic models.
"""

import pytest
from pydantic import ValidationError

from models.enums import EquipmentType, EquipmentStatus, TaskType, TaskStatus


class TestEquipmentCreation:
    """Test the creation of Equipment model"""

    def test_equipment_creation_qc(self):
        """Test and create shore bridge equipment"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="QC01",
            equip_type=EquipmentType.QUAY_CRANE,
            equip_name="No.1 Shore Bridge",
            berth_id="B01",
        )

        assert equipment.equip_id == "QC01"
        assert equipment.equip_type == EquipmentType.QUAY_CRANE
        assert equipment.equip_name == "No.1 Shore Bridge"
        assert equipment.status == EquipmentStatus.IDLE
        assert equipment.current_task is None
        assert equipment.berth_id == "B01"
        assert equipment.block_id is None
        assert equipment.current_location is None
        assert equipment.efficiency_rate == 25

    def test_equipment_creation_rtg(self):
        """Test and create tire crane equipment"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="RTG05",
            equip_type=EquipmentType.RTG,
            equip_name="No. 5 tire crane",
            block_id="A01",
        )

        assert equipment.equip_id == "RTG05"
        assert equipment.equip_type == EquipmentType.RTG
        assert equipment.equip_name == "No. 5 tire crane"
        assert equipment.status == EquipmentStatus.IDLE
        assert equipment.block_id == "A01"
        assert equipment.berth_id is None

    def test_equipment_creation_yt(self):
        """Test and create on-site trailer equipment"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="YT12",
            equip_type=EquipmentType.YARD_TRUCK,
            equip_name="No. 12 collection card",
            current_location="SluicewayA",
            efficiency_rate=30,
        )

        assert equipment.equip_id == "YT12"
        assert equipment.equip_type == EquipmentType.YARD_TRUCK
        assert equipment.current_location == "SluicewayA"
        assert equipment.efficiency_rate == 30

    def test_equipment_all_types(self):
        """Test and create all types of devices"""
        from models.equipment import Equipment

        # Shore bridge
        qc = Equipment(equip_id="QC01", equip_type=EquipmentType.QUAY_CRANE, equip_name="QC1")
        assert qc.equip_type == EquipmentType.QUAY_CRANE

        # Tire crane
        rtg = Equipment(equip_id="RTG01", equip_type=EquipmentType.RTG, equip_name="RTG1")
        assert rtg.equip_type == EquipmentType.RTG

        # Track crane
        rmg = Equipment(equip_id="RMG01", equip_type=EquipmentType.RMG, equip_name="RMG1")
        assert rmg.equip_type == EquipmentType.RMG

        # On-site trailer
        yt = Equipment(equip_id="YT01", equip_type=EquipmentType.YARD_TRUCK, equip_name="YT1")
        assert yt.equip_type == EquipmentType.YARD_TRUCK

        # Front hanging
        rs = Equipment(equip_id="RS01", equip_type=EquipmentType.REACH_STACKER, equip_name="RS1")
        assert rs.equip_type == EquipmentType.REACH_STACKER

        # Top hanging
        tl = Equipment(equip_id="TL01", equip_type=EquipmentType.TOP_LOADER, equip_name="TL1")
        assert tl.equip_type == EquipmentType.TOP_LOADER


class TestEquipmentIdPrefixValidation:
    """Test device ID prefix verification"""

    def test_equipment_id_valid_prefix_qc(self):
        """Test the effective shore bridgeID"""
        from models.equipment import Equipment

        for i in ["QC01", "QC12", "QC99"]:
            equipment = Equipment(
                equip_id=i,
                equip_type=EquipmentType.QUAY_CRANE,
                equip_name=f"Equipment{i}",
            )
            assert equipment.equip_id == i

    def test_equipment_id_valid_prefix_rtg(self):
        """Test the effective tire craneID"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="RTG05",
            equip_type=EquipmentType.RTG,
            equip_name="RTG5",
        )
        assert equipment.equip_id == "RTG05"

    def test_equipment_id_valid_prefix_rmg(self):
        """Test the effective track craneID"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="RMG03",
            equip_type=EquipmentType.RMG,
            equip_name="RMG3",
        )
        assert equipment.equip_id == "RMG03"

    def test_equipment_id_valid_prefix_yt(self):
        """Test the effective collection cardID"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="YT25",
            equip_type=EquipmentType.YARD_TRUCK,
            equip_name="YT25",
        )
        assert equipment.equip_id == "YT25"

    def test_equipment_id_valid_prefix_rs(self):
        """Test the effective front craneID"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="RS02",
            equip_type=EquipmentType.REACH_STACKER,
            equip_name="RS2",
        )
        assert equipment.equip_id == "RS02"

    def test_equipment_id_valid_prefix_tl(self):
        """Test the effective top craneID"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="TL01",
            equip_type=EquipmentType.TOP_LOADER,
            equip_name="TL1",
        )
        assert equipment.equip_id == "TL01"

    def test_equipment_id_invalid_prefix(self):
        """Test invalid device ID prefix"""
        from models.equipment import Equipment

        invalid_ids = ["QC1", "QC001", "QCABC", "XX01", "qc01", "QC001", "QCA1"]

        for invalid_id in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                Equipment(
                    equip_id=invalid_id,
                    equip_type=EquipmentType.QUAY_CRANE,
                    equip_name="Test equipment",
                )
            assert "equip_id" in str(exc_info.value).lower()

    def test_equipment_id_missing_digits(self):
        """Test devices with missing numbersID"""
        from models.equipment import Equipment

        with pytest.raises(ValidationError):
            Equipment(
                equip_id="QC",
                equip_type=EquipmentType.QUAY_CRANE,
                equip_name="Test equipment",
            )

    def test_equipment_id_too_many_digits(self):
        """Test devices with too many numbersID"""
        from models.equipment import Equipment

        with pytest.raises(ValidationError):
            Equipment(
                equip_id="QC001",
                equip_type=EquipmentType.QUAY_CRANE,
                equip_name="Test equipment",
            )


class TestEquipmentEfficiencyRange:
    """Test equipment efficiency range verification"""

    def test_equipment_efficiency_default(self):
        """Test the default efficiency value"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="QC01",
            equip_type=EquipmentType.QUAY_CRANE,
            equip_name="QC1",
        )
        assert equipment.efficiency_rate == 25

    def test_equipment_efficiency_min_value(self):
        """Minimum value of test efficiency"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="QC01",
            equip_type=EquipmentType.QUAY_CRANE,
            equip_name="QC1",
            efficiency_rate=1,
        )
        assert equipment.efficiency_rate == 1

    def test_equipment_efficiency_max_value(self):
        """Maximum value of test efficiency"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="QC01",
            equip_type=EquipmentType.QUAY_CRANE,
            equip_name="QC1",
            efficiency_rate=60,
        )
        assert equipment.efficiency_rate == 60

    def test_equipment_efficiency_below_min(self):
        """The test efficiency is lower than the minimum value."""
        from models.equipment import Equipment

        with pytest.raises(ValidationError):
            Equipment(
                equip_id="QC01",
                equip_type=EquipmentType.QUAY_CRANE,
                equip_name="QC1",
                efficiency_rate=0,
            )

    def test_equipment_efficiency_above_max(self):
        """The test efficiency is higher than the maximum value."""
        from models.equipment import Equipment

        with pytest.raises(ValidationError):
            Equipment(
                equip_id="QC01",
                equip_type=EquipmentType.QUAY_CRANE,
                equip_name="QC1",
                efficiency_rate=61,
            )

    def test_equipment_efficiency_valid_middle(self):
        """Test the effective intermediate efficiency value"""
        from models.equipment import Equipment

        equipment = Equipment(
            equip_id="QC01",
            equip_type=EquipmentType.QUAY_CRANE,
            equip_name="QC1",
            efficiency_rate=35,
        )
        assert equipment.efficiency_rate == 35


class TestTaskCreation:
    """Test the creation of Task model"""

    def test_task_creation_basic(self):
        """Test and create basic tasks"""
        from models.equipment import Task

        task = Task(
            task_id="T0001",
            task_type=TaskType.LOAD,
        )

        assert task.task_id == "T0001"
        assert task.task_type == TaskType.LOAD
        assert task.status == TaskStatus.PENDING
        assert task.equip_id is None
        assert task.container_id is None
        assert task.vessel_id is None
        assert task.source_location is None
        assert task.target_location is None
        assert task.estimated_duration == 30

    def test_task_creation_full(self):
        """Test to create complete tasks"""
        from models.equipment import Task

        task = Task(
            task_id="T0012",
            task_type=TaskType.DISCHARGE,
            status=TaskStatus.ASSIGNED,
            equip_id="QC01",
            container_id="C001234",
            vessel_id="V001",
            source_location="On the boatBAY12",
            target_location="A01-01-01-01",
            created_at="2024-01-15T10:30:00",
            estimated_duration=45,
        )

        assert task.task_id == "T0012"
        assert task.task_type == TaskType.DISCHARGE
        assert task.status == TaskStatus.ASSIGNED
        assert task.equip_id == "QC01"
        assert task.container_id == "C001234"
        assert task.vessel_id == "V001"
        assert task.source_location == "On the boatBAY12"
        assert task.target_location == "A01-01-01-01"
        assert task.created_at == "2024-01-15T10:30:00"
        assert task.estimated_duration == 45

    def test_task_all_types(self):
        """Test and create all types of tasks"""
        from models.equipment import Task

        # Shipment mission
        load = Task(task_id="T0001", task_type=TaskType.LOAD)
        assert load.task_type == TaskType.LOAD

        # Unloading task
        discharge = Task(task_id="T0002", task_type=TaskType.DISCHARGE)
        assert discharge.task_type == TaskType.DISCHARGE

        # In-field transfer box
        yard_move = Task(task_id="T0003", task_type=TaskType.YARD_MOVE)
        assert yard_move.task_type == TaskType.YARD_MOVE

        # Exit the gate
        gate_out = Task(task_id="T0004", task_type=TaskType.GATE_OUT)
        assert gate_out.task_type == TaskType.GATE_OUT

        # Enter the gate
        gate_in = Task(task_id="T0005", task_type=TaskType.GATE_IN)
        assert gate_in.task_type == TaskType.GATE_IN

    def test_task_all_statuses(self):
        """Test all states of the task"""
        from models.equipment import Task

        statuses = [
            TaskStatus.PENDING,
            TaskStatus.ASSIGNED,
            TaskStatus.IN_PROGRESS,
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        ]

        for status in statuses:
            task = Task(task_id="T0001", task_type=TaskType.LOAD, status=status)
            assert task.status == status


class TestTaskIdPattern:
    """Test task ID format verification"""

    def test_task_id_valid(self):
        """Test effective tasksID"""
        from models.equipment import Task

        valid_ids = ["T0001", "T0012", "T0123", "T1234", "T9999"]

        for task_id in valid_ids:
            task = Task(task_id=task_id, task_type=TaskType.LOAD)
            assert task.task_id == task_id

    def test_task_id_invalid_format(self):
        """Test the invalid task ID format"""
        from models.equipment import Task

        invalid_ids = [
            "T001",      # Only 3 digits
            "T00001",    # 5Digits
            "T001A",     # Contains letters
            "t0001",     # Ordinary form of numerals
            "00123",     # Missing T prefix
            "QT001",     # Wrong prefix
            "T0",        # There are too few numbers.
            "T",         # Only the prefix
            "TABC",      # Full letters
        ]

        for invalid_id in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                Task(task_id=invalid_id, task_type=TaskType.LOAD)
            assert "task_id" in str(exc_info.value).lower()

    def test_task_id_boundary_values(self):
        """Test task ID boundary value"""
        from models.equipment import Task

        # Minimum value T0001
        task_min = Task(task_id="T0001", task_type=TaskType.LOAD)
        assert task_min.task_id == "T0001"

        # Maximum value T9999
        task_max = Task(task_id="T9999", task_type=TaskType.LOAD)
        assert task_max.task_id == "T9999"


class TestTaskDuration:
    """Estimated duration verification of test tasks"""

    def test_task_duration_default(self):
        """Test the default duration"""
        from models.equipment import Task

        task = Task(task_id="T0001", task_type=TaskType.LOAD)
        assert task.estimated_duration == 30

    def test_task_duration_valid(self):
        """Valid duration of the test"""
        from models.equipment import Task

        for duration in [1, 15, 30, 60, 120]:
            task = Task(
                task_id="T0001",
                task_type=TaskType.LOAD,
                estimated_duration=duration,
            )
            assert task.estimated_duration == duration

    def test_task_duration_zero(self):
        """The duration of the test is zero."""
        from models.equipment import Task

        with pytest.raises(ValidationError):
            Task(
                task_id="T0001",
                task_type=TaskType.LOAD,
                estimated_duration=0,
            )

    def test_task_duration_negative(self):
        """Test the duration of negative numbers"""
        from models.equipment import Task

        with pytest.raises(ValidationError):
            Task(
                task_id="T0001",
                task_type=TaskType.LOAD,
                estimated_duration=-10,
            )
