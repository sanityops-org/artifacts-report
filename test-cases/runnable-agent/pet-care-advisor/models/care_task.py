"""
Care task model describing a scheduled care action.
"""

from pydantic import BaseModel, Field

from models.enums import CareTaskStatus, CareTaskType, TaskFrequency


class CareTask(BaseModel):
    """Care task model"""
    task_id: str = Field(..., pattern=r"^TASK\d{4}$", description="Task ID")
    pet_id: str = Field(..., pattern=r"^PET\d{3}$", description="Pet ID")
    type: CareTaskType = Field(..., description="Care task type")
    scheduled_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Scheduled time (HH:MM)")
    frequency: TaskFrequency = Field(default=TaskFrequency.DAILY, description="Recurrence")
    scheduled_date: str | None = Field(
        None, description="Date for once/weekly tasks (YYYY-MM-DD)"
    )
    status: CareTaskStatus = Field(default=CareTaskStatus.PENDING, description="Task status")
    notes: str | None = Field(None, description="User-supplied notes, passed through verbatim")
    created_at: str = Field(..., description="Creation timestamp (ISO 8601)")


__all__ = ["CareTask"]
