"""
Execution and event data model

Define the Pydantic model of Execution Record and FeedbackEvent for the container terminal scheduling system.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from models.enums import EventType, TaskStatus


class FeedbackEvent(BaseModel):
    """
    Feedback event model

    Record the feedback of various events during the execution process.

    Attributes:
        event_id: Unique identifier of the event
        event_type: Type of event
        timestamp: Time of the incident (ISO 8601 format)
        execution_id: Associated execution ID, optional
        payload: Event load data, default to empty dictionary
    """

    event_id: str = Field(
        ...,
        description="Unique identifier of the event",
    )
    event_type: EventType = Field(
        ...,
        description="Type of event",
    )
    timestamp: str = Field(
        ...,
        description="Time of the incident (ISO 8601 format)",
    )
    execution_id: Optional[str] = Field(
        default=None,
        description="Related executionID",
    )
    payload: dict = Field(
        default_factory=dict,
        description="Event load data",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event_id": "E0001",
                    "event_type": "task_started",
                    "timestamp": "2024-01-15T10:30:00",
                    "execution_id": "EX0001",
                    "payload": {"progress": 0},
                },
                {
                    "event_id": "E0002",
                    "event_type": "task_progress",
                    "timestamp": "2024-01-15T11:00:00",
                    "execution_id": "EX0001",
                    "payload": {"progress": 50, "container_count": 20},
                },
                {
                    "event_id": "E0003",
                    "event_type": "alert",
                    "timestamp": "2024-01-15T12:00:00",
                    "execution_id": None,
                    "payload": {"level": "warning", "message": "Equipment QC01 efficiency decreases"},
                },
            ]
        }
    }


class ExecutionRecord(BaseModel):
    """
    Execution record model

    Record the whole process information of port operation.

    Attributes:
        execution_id: Execute the record unique identifier, the format is EX followed by a 4-digit number (such as EX0001)
        action: Execution action name
        params: Execution parameters, default to empty dictionary
        issued_by: Initiator identification
        status: Execution status, default ASSIGNED
        started_at: Start time (ISO 8601 format)
        estimated_duration: The estimated duration (minutes) must be greater than0
        feedback_events: The list of feedback events is empty by default.
    """

    execution_id: str = Field(
        ...,
        pattern=r"^EX\d{4}$",
        description="Execute the record unique identifier, the format is EX followed by a 4-digit number.",
        examples=["EX0001", "EX1234", "EX9999"],
    )
    action: str = Field(
        ...,
        description="Execution action name",
    )
    params: dict = Field(
        default_factory=dict,
        description="Execution parameters",
    )
    issued_by: str = Field(
        ...,
        description="Initiator identification",
    )
    status: TaskStatus = Field(
        default=TaskStatus.ASSIGNED,
        description="Execution status",
    )
    started_at: str = Field(
        ...,
        description="Start time (ISO 8601 format)",
    )
    estimated_duration: int = Field(
        ...,
        gt=0,
        description="Estimated duration (minutes)",
    )
    feedback_events: list[FeedbackEvent] = Field(
        default_factory=list,
        description="List of feedback events",
    )

    @field_validator("execution_id")
    @classmethod
    def validate_execution_id(cls, v: str) -> str:
        """Verify the execution ID format"""
        if not re.match(r"^EX\d{4}$", v):
            raise ValueError(
                f"The execution ID format is invalid: {v}, which must be EX followed by 4 digits (such as EX0001, EX9999)"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "execution_id": "EX0001",
                    "action": "discharge",
                    "params": {"vessel_id": "V001", "container_count": 100},
                    "issued_by": "scheduler",
                    "status": "assigned",
                    "started_at": "2024-01-15T08:00:00",
                    "estimated_duration": 120,
                    "feedback_events": [
                        {
                            "event_id": "E0001",
                            "event_type": "task_started",
                            "timestamp": "2024-01-15T08:00:00",
                            "execution_id": "EX0001",
                            "payload": {"status": "started"},
                        }
                    ],
                },
                {
                    "execution_id": "EX0002",
                    "action": "load",
                    "params": {"vessel_id": "V002", "bay": "BAY12"},
                    "issued_by": "planner",
                    "status": "in_progress",
                    "started_at": "2024-01-15T10:00:00",
                    "estimated_duration": 90,
                    "feedback_events": [],
                },
            ]
        }
    }


__all__ = ["FeedbackEvent", "ExecutionRecord"]
