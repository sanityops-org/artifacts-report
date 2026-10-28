"""
Execution and event model test module

Test the creation and verification of FeedbackEvent and ExecutionRecord models.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime

from models.enums import EventType, TaskStatus
from models.execution import FeedbackEvent, ExecutionRecord


class TestFeedbackEvent:
    """FeedbackEvent Model test"""

    def test_feedback_event_creation(self):
        """Test the basic creation of feedback events"""
        event = FeedbackEvent(
            event_id="E0001",
            event_type=EventType.TASK_STARTED,
            timestamp="2024-01-15T10:30:00",
            execution_id="EX0001",
            payload={"progress": 0},
        )

        assert event.event_id == "E0001"
        assert event.event_type == EventType.TASK_STARTED
        assert event.timestamp == "2024-01-15T10:30:00"
        assert event.execution_id == "EX0001"
        assert event.payload == {"progress": 0}

    def test_feedback_event_optional_execution_id(self):
        """Test execution_id can be None"""
        event = FeedbackEvent(
            event_id="E0002",
            event_type=EventType.ALERT,
            timestamp="2024-01-15T11:00:00",
        )

        assert event.execution_id is None
        assert event.payload == {}  # Default empty dictionary

    def test_feedback_event_default_payload(self):
        """Test payload defaults to empty dictionary"""
        event = FeedbackEvent(
            event_id="E0003",
            event_type=EventType.STATUS_CHANGED,
            timestamp="2024-01-15T12:00:00",
        )

        assert event.payload == {}


class TestExecutionRecord:
    """ExecutionRecord Model test"""

    def test_execution_record_creation(self):
        """Basic creation of test execution records"""
        execution = ExecutionRecord(
            execution_id="EX0001",
            action="discharge",
            params={"vessel_id": "V001", "container_count": 100},
            issued_by="scheduler",
            status=TaskStatus.ASSIGNED,
            started_at="2024-01-15T08:00:00",
            estimated_duration=120,
        )

        assert execution.execution_id == "EX0001"
        assert execution.action == "discharge"
        assert execution.params == {"vessel_id": "V001", "container_count": 100}
        assert execution.issued_by == "scheduler"
        assert execution.status == TaskStatus.ASSIGNED
        assert execution.started_at == "2024-01-15T08:00:00"
        assert execution.estimated_duration == 120
        assert execution.feedback_events == []  # Default empty list

    def test_execution_record_id_pattern(self):
        """Test execution record ID format verification"""
        # EffectiveID
        valid_ids = ["EX0001", "EX1234", "EX9999"]
        for exec_id in valid_ids:
            execution = ExecutionRecord(
                execution_id=exec_id,
                action="load",
                params={},
                issued_by="operator",
                started_at="2024-01-15T10:00:00",
                estimated_duration=60,
            )
            assert execution.execution_id == exec_id

        # Be invalidID
        invalid_ids = ["EX001", "EX00001", "EX001A", "eX0001", "T0001"]
        for exec_id in invalid_ids:
            with pytest.raises(ValidationError):
                ExecutionRecord(
                    execution_id=exec_id,
                    action="load",
                    params={},
                    issued_by="operator",
                    started_at="2024-01-15T10:00:00",
                    estimated_duration=60,
                )

    def test_execution_record_with_events(self):
        """The test execution record contains feedback events."""
        event1 = FeedbackEvent(
            event_id="E0001",
            event_type=EventType.TASK_STARTED,
            timestamp="2024-01-15T08:00:00",
            execution_id="EX0001",
            payload={"status": "started"},
        )
        event2 = FeedbackEvent(
            event_id="E0002",
            event_type=EventType.TASK_PROGRESS,
            timestamp="2024-01-15T09:00:00",
            execution_id="EX0001",
            payload={"progress": 50},
        )

        execution = ExecutionRecord(
            execution_id="EX0001",
            action="discharge",
            params={"vessel_id": "V001"},
            issued_by="scheduler",
            started_at="2024-01-15T08:00:00",
            estimated_duration=120,
            feedback_events=[event1, event2],
        )

        assert len(execution.feedback_events) == 2
        assert execution.feedback_events[0].event_id == "E0001"
        assert execution.feedback_events[1].event_id == "E0002"

    def test_execution_record_estimated_duration_must_be_positive(self):
        """The test estimated_duration must be greater than0"""
        with pytest.raises(ValueError, match="greater than 0"):
            ExecutionRecord(
                execution_id="EX0001",
                action="load",
                params={},
                issued_by="operator",
                started_at="2024-01-15T10:00:00",
                estimated_duration=0,
            )

        with pytest.raises(ValueError, match="greater than 0"):
            ExecutionRecord(
                execution_id="EX0001",
                action="load",
                params={},
                issued_by="operator",
                started_at="2024-01-15T10:00:00",
                estimated_duration=-5,
            )

    def test_execution_record_default_status(self):
        """The default status of the test is ASSIGNED"""
        execution = ExecutionRecord(
            execution_id="EX0001",
            action="load",
            params={},
            issued_by="operator",
            started_at="2024-01-15T10:00:00",
            estimated_duration=60,
        )

        assert execution.status == TaskStatus.ASSIGNED

    def test_execution_record_default_params(self):
        """Test params defaults to empty dictionary"""
        execution = ExecutionRecord(
            execution_id="EX0001",
            action="load",
            issued_by="operator",
            started_at="2024-01-15T10:00:00",
            estimated_duration=60,
        )

        assert execution.params == {}
