"""
Tests for the care engine's scheduling and due-date logic.

Dates are pinned explicitly so the assertions do not depend on the wall clock.
"""

from apis.care_engine import records_due_soon, tasks_due_on
from models import CareTask, HealthRecord


def _task(task_id, time, frequency="daily", date=None, status="pending"):
    return CareTask(
        task_id=task_id, pet_id="PET001", type="walk", scheduled_time=time,
        frequency=frequency, scheduled_date=date, status=status,
        created_at="2026-10-01T08:00:00"
    )


def test_tasks_due_on_includes_daily_tasks():
    tasks = [_task("TASK0001", "07:00", "daily")]
    assert len(tasks_due_on("2026-10-09", tasks)) == 1


def test_tasks_due_on_includes_matching_dated_task():
    tasks = [_task("TASK0002", "10:00", "weekly", "2026-10-09")]
    assert len(tasks_due_on("2026-10-09", tasks)) == 1


def test_tasks_due_on_excludes_non_matching_dated_task():
    tasks = [_task("TASK0003", "10:00", "weekly", "2026-10-16")]
    assert tasks_due_on("2026-10-09", tasks) == []


def test_tasks_due_on_excludes_done_by_default():
    tasks = [_task("TASK0004", "07:00", "daily", status="done")]
    assert tasks_due_on("2026-10-09", tasks) == []


def test_tasks_due_on_can_include_done():
    tasks = [_task("TASK0005", "07:00", "daily", status="done")]
    assert len(tasks_due_on("2026-10-09", tasks, include_done=True)) == 1


def test_tasks_due_on_is_ordered_by_time_then_id():
    tasks = [
        _task("TASK0009", "18:00"),
        _task("TASK0007", "07:00"),
        _task("TASK0008", "07:00"),
    ]
    keys = [(t.scheduled_time, t.task_id) for t in tasks_due_on("2026-10-09", tasks)]
    assert keys == [("07:00", "TASK0007"), ("07:00", "TASK0008"), ("18:00", "TASK0009")]


def _record(record_id, next_due):
    return HealthRecord(
        record_id=record_id, pet_id="PET001", type="vaccination",
        date="2026-01-01", description="A record used only in tests.",
        next_due=next_due
    )


def test_records_due_soon_includes_past_due_and_flags_overdue():
    result = records_due_soon([_record("REC0001", "2026-10-01")],
                              within_days=30, today="2026-10-09")
    assert len(result) == 1
    assert result[0]["overdue"] is True
    assert result[0]["days_until"] == -8


def test_records_due_soon_includes_boundary_day():
    """A record exactly within_days away is inside the window."""
    result = records_due_soon([_record("REC0002", "2026-11-08")],
                              within_days=30, today="2026-10-09")
    assert len(result) == 1
    assert result[0]["days_until"] == 30
    assert result[0]["overdue"] is False


def test_records_due_soon_excludes_beyond_window():
    result = records_due_soon([_record("REC0003", "2026-11-09")],
                              within_days=30, today="2026-10-09")
    assert result == []


def test_records_due_soon_skips_null_next_due():
    assert records_due_soon([_record("REC0004", None)], today="2026-10-09") == []


def test_records_due_soon_is_ordered_by_due_date():
    result = records_due_soon(
        [_record("REC0006", "2026-10-20"), _record("REC0005", "2026-10-01")],
        within_days=30, today="2026-10-09"
    )
    assert [r["record_id"] for r in result] == ["REC0005", "REC0006"]


def test_records_due_soon_is_empty_for_empty_input():
    assert records_due_soon([], today="2026-10-09") == []
