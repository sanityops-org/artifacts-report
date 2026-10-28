"""
Care engine: daily task selection and health-record due dates.

`today` is a parameter rather than an implicit clock read so the due-date logic
can be tested against fixed dates.
"""

from datetime import date, datetime, timedelta
from typing import Any

from models import CareTask, HealthRecord
from models.enums import CareTaskStatus, TaskFrequency


def tasks_due_on(
    target_date: str,
    tasks: list[CareTask],
    include_done: bool = False
) -> list[CareTask]:
    """
    Select the care tasks that fall on a given date.

    A task qualifies when its frequency is daily, or when its scheduled_date
    matches the target date (for once and weekly tasks).

    Args:
        target_date: Date in YYYY-MM-DD form
        tasks: All care tasks
        include_done: Keep tasks already marked done

    Returns:
        Matching tasks ordered by scheduled_time, then task_id
    """
    matches: list[CareTask] = []

    for task in tasks:
        if task.frequency == TaskFrequency.DAILY:
            qualifies = True
        else:
            qualifies = task.scheduled_date == target_date

        if not qualifies:
            continue

        if not include_done and task.status == CareTaskStatus.DONE:
            continue

        matches.append(task)

    matches.sort(key=lambda t: (t.scheduled_time, t.task_id))

    return matches


def records_due_soon(
    records: list[HealthRecord],
    within_days: int = 30,
    today: str | None = None
) -> list[dict[str, Any]]:
    """
    Find health records whose next_due date is within a window.

    Records already past due are included and flagged as overdue.

    Args:
        records: All health records
        within_days: Look-ahead window in days
        today: Reference date (YYYY-MM-DD); defaults to the system date

    Returns:
        Record dicts augmented with days_until and overdue, sorted by next_due
    """
    reference = date.fromisoformat(today) if today else date.today()

    upcoming: list[dict[str, Any]] = []

    for record in records:
        if not record.next_due:
            continue

        try:
            due = date.fromisoformat(record.next_due)
        except ValueError:
            continue

        days_until = (due - reference).days

        if days_until > within_days:
            continue

        entry = record.model_dump(mode="json")
        entry["days_until"] = days_until
        entry["overdue"] = days_until < 0
        upcoming.append(entry)

    upcoming.sort(key=lambda e: e["next_due"])

    return upcoming


__all__ = ["tasks_due_on", "records_due_soon"]
