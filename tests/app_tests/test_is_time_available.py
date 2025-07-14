from datetime import date, time

import pytest

from trajectory_test_assignment.app import (
    ScheduleDateNotFoundError,
)
from trajectory_test_assignment.infrastructure import dict_to_schedule


def make_schedule():
    data = {
        "days": [
            {
                "id": "1",
                "date": "2025-02-15",
                "start": "09:00",
                "end": "18:00",
            }
        ],
        "timeslots": [
            {"id": "1", "day_id": "1", "start": "10:00", "end": "11:00"},
            {"id": "2", "day_id": "1", "start": "13:00", "end": "14:00"},
        ],
    }
    return dict_to_schedule(data)


def test_time_available_free():
    schedule = make_schedule()
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(11, 0), time(12, 0))
        is True
    )
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(9, 0), time(10, 0))
        is True
    )
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(14, 0), time(15, 0))
        is True
    )


def test_time_available_busy():
    schedule = make_schedule()
    assert (
        schedule.is_time_available(
            date(2025, 2, 15), time(10, 30), time(11, 30)
        )
        is False
    )
    assert (
        schedule.is_time_available(
            date(2025, 2, 15), time(12, 30), time(13, 30)
        )
        is False
    )
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(10, 0), time(11, 0))
        is False
    )


def test_time_available_out_of_bounds():
    schedule = make_schedule()
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(8, 0), time(9, 0))
        is False
    )
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(17, 0), time(19, 0))
        is False
    )
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(8, 0), time(19, 0))
        is False
    )


def test_time_available_no_day():
    schedule = make_schedule()
    with pytest.raises(ScheduleDateNotFoundError):
        schedule.is_time_available(date(2025, 2, 16), time(9, 0), time(10, 0))


def test_time_available_touching_slot_end():
    schedule = make_schedule()
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(11, 0), time(12, 0))
        is True
    )


def test_time_available_touching_slot_start():
    schedule = make_schedule()
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(12, 0), time(13, 0))
        is True
    )


def test_time_available_exact_match_with_slot():
    schedule = make_schedule()
    assert (
        schedule.is_time_available(date(2025, 2, 15), time(10, 0), time(11, 0))
        is False
    )


def test_time_available_one_minute_overlap():
    schedule = make_schedule()

    assert (
        schedule.is_time_available(
            date(2025, 2, 15), time(10, 59), time(11, 30)
        )
        is False
    )
