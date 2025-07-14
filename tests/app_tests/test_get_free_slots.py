from datetime import date, time

import pytest

from trajectory_test_assignment.app import ScheduleDateNotFoundError
from trajectory_test_assignment.infrastructure import dict_to_schedule


def test_get_free_slots_full_day():
    data = {
        "days": [
            {
                "id": "1",
                "date": "2025-02-15",
                "start": "09:00",
                "end": "18:00",
            }
        ],
        "timeslots": [],
    }
    schedule = dict_to_schedule(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == [
        (time(9, 0), time(18, 0))
    ]


def test_get_free_slots_no_free():
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
            {"id": "1", "day_id": "1", "start": "09:00", "end": "18:00"}
        ],
    }
    schedule = dict_to_schedule(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == []


def test_get_free_slots_with_gaps():
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
            {"id": "3", "day_id": "1", "start": "16:00", "end": "17:00"},
        ],
    }
    schedule = dict_to_schedule(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == [
        (time(9, 0), time(10, 0)),
        (time(11, 0), time(13, 0)),
        (time(14, 0), time(16, 0)),
        (time(17, 0), time(18, 0)),
    ]


def test_get_free_slots_start_end_busy():
    data = {
        "days": [
            {
                "id": "1",
                "date": "2025-02-15",
                "start": "08:00",
                "end": "20:00",
            }
        ],
        "timeslots": [
            {"id": "1", "day_id": "1", "start": "08:00", "end": "10:00"},
            {"id": "2", "day_id": "1", "start": "18:00", "end": "20:00"},
        ],
    }
    schedule = dict_to_schedule(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == [
        (time(10, 0), time(18, 0))
    ]


def test_timeslot_outside_workday():
    data = {
        "days": [
            {
                "id": "1",
                "date": "2025-02-20",
                "start": "09:00",
                "end": "17:00",
            }
        ],
        "timeslots": [
            {"id": "1", "day_id": "1", "start": "08:00", "end": "18:00"}
        ],
    }
    schedule = dict_to_schedule(data)
    result = schedule.get_free_slots(date(2025, 2, 20))

    assert result == []


def test_empty_schedule():
    schedule = dict_to_schedule({"days": [], "timeslots": []})

    with pytest.raises(ScheduleDateNotFoundError):
        schedule.get_free_slots(date(2025, 2, 15))
