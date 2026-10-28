"""
Gate model test

Test the verification logic of GateChannel and Appointment Pydantic models.
"""

import pytest
from pydantic import ValidationError
from models.gate import GateChannel, Appointment
from models.enums import GateChannelType, GateChannelStatus, TaskType, AppointmentStatus


class TestGateChannelModel:
    """GateChannel Model test class"""

    def test_gate_channel_creation(self):
        """Test the normal creation of the gate channel model"""
        channel = GateChannel(
            channel_id="G01",
            channel_name="Gate passage No.1",
            type=GateChannelType.INBOUND,
        )

        assert channel.channel_id == "G01"
        assert channel.channel_name == "Gate passage No.1"
        assert channel.type == GateChannelType.INBOUND
        assert channel.status == GateChannelStatus.OPEN
        assert channel.queue_length == 0

    def test_gate_channel_id_pattern(self):
        r"""Test channel ID format verification (must match ^G\d{2}$)"""
        # Valid format
        valid_ids = ["G01", "G12", "G99"]
        for cid in valid_ids:
            channel = GateChannel(
                channel_id=cid,
                channel_name="Test channel",
                type=GateChannelType.INBOUND,
            )
            assert channel.channel_id == cid

        # Invalid format
        invalid_ids = ["g01", "G1", "G001", "G1A", "X01", "G0", ""]
        for cid in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                GateChannel(
                    channel_id=cid,
                    channel_name="Test channel",
                    type=GateChannelType.INBOUND,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("channel_id",) for e in errors)

    def test_gate_channel_queue_length_validation(self):
        """Test queue length verification (ge=0)"""
        # Effective queue length
        valid_lengths = [0, 1, 10, 100]
        for length in valid_lengths:
            channel = GateChannel(
                channel_id="G01",
                channel_name="Test channel",
                type=GateChannelType.INBOUND,
                queue_length=length,
            )
            assert channel.queue_length == length

        # Invalid queue length
        with pytest.raises(ValidationError) as exc_info:
            GateChannel(
                channel_id="G01",
                channel_name="Test channel",
                type=GateChannelType.INBOUND,
                queue_length=-1,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("queue_length",) for e in errors)

    def test_gate_channel_outbound_type(self):
        """Test the creation of the exit channel"""
        channel = GateChannel(
            channel_id="G02",
            channel_name="Exit channel No.1",
            type=GateChannelType.OUTBOUND,
        )
        assert channel.type == GateChannelType.OUTBOUND

    def test_gate_channel_congested_status(self):
        """Test the congestion state channel"""
        channel = GateChannel(
            channel_id="G03",
            channel_name="Congested passage",
            type=GateChannelType.INBOUND,
            status=GateChannelStatus.CONGESTED,
            queue_length=15,
        )
        assert channel.status == GateChannelStatus.CONGESTED
        assert channel.queue_length == 15


class TestAppointmentModel:
    """Appointment Model test class"""

    def test_appointment_creation(self):
        """The test appointment model is created normally"""
        appointment = Appointment(
            appointment_id="AP001",
            truck_id="T001",
            driver_name="Zhang San",
            appointment_time="2024-01-15T08:00:00",
            type=TaskType.GATE_OUT,
            container_id="C001",
        )

        assert appointment.appointment_id == "AP001"
        assert appointment.truck_id == "T001"
        assert appointment.driver_name == "Zhang San"
        assert appointment.appointment_time == "2024-01-15T08:00:00"
        assert appointment.type == TaskType.GATE_OUT
        assert appointment.container_id == "C001"
        assert appointment.status == AppointmentStatus.PENDING

    def test_appointment_id_pattern(self):
        r"""Test appointment ID format verification (must match ^AP\d{3}$)"""
        # Valid format
        valid_ids = ["AP001", "AP123", "AP999"]
        for aid in valid_ids:
            appointment = Appointment(
                appointment_id=aid,
                truck_id="T001",
                driver_name="Test the driver",
                appointment_time="2024-01-15T08:00:00",
                type=TaskType.GATE_IN,
                container_id="C001",
            )
            assert appointment.appointment_id == aid

        # Invalid format
        invalid_ids = ["ap001", "AP01", "AP0001", "AP1A2", "X001", "AP00", ""]
        for aid in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                Appointment(
                    appointment_id=aid,
                    truck_id="T001",
                    driver_name="Test the driver",
                    appointment_time="2024-01-15T08:00:00",
                    type=TaskType.GATE_IN,
                    container_id="C001",
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("appointment_id",) for e in errors)

    def test_appointment_gate_in_type(self):
        """Test the type of entry appointment"""
        appointment = Appointment(
            appointment_id="AP001",
            truck_id="T001",
            driver_name="Li Si",
            appointment_time="2024-01-15T08:00:00",
            type=TaskType.GATE_IN,
            container_id="C002",
        )
        assert appointment.type == TaskType.GATE_IN

    def test_appointment_valid_status(self):
        """Test the valid appointment status"""
        appointment = Appointment(
            appointment_id="AP001",
            truck_id="T001",
            driver_name="Wang Wu",
            appointment_time="2024-01-15T08:00:00",
            type=TaskType.GATE_OUT,
            container_id="C003",
            status=AppointmentStatus.VALID,
        )
        assert appointment.status == AppointmentStatus.VALID

    def test_appointment_completed_status(self):
        """Test the appointment status"""
        appointment = Appointment(
            appointment_id="AP001",
            truck_id="T001",
            driver_name="Zhao Liu",
            appointment_time="2024-01-15T08:00:00",
            type=TaskType.GATE_OUT,
            container_id="C004",
            status=AppointmentStatus.COMPLETED,
        )
        assert appointment.status == AppointmentStatus.COMPLETED
