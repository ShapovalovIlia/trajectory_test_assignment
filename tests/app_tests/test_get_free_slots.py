from datetime import date, time

import pytest

from trajectory_test_assignment.app import Schedule, ScheduleDateNotFoundError


def test_get_free_slots_full_day():
    data = {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 15),
                "start": time(9, 0),
                "end": time(18, 0),
            }
        ],
        "timeslot": [],
    }
    schedule = Schedule.from_dict(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == [
        (time(9, 0), time(18, 0))
    ]


def test_get_free_slots_no_free():
    data = {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 15),
                "start": time(9, 0),
                "end": time(18, 0),
            }
        ],
        "timeslot": [
            {"id": 1, "day_id": 1, "start": time(9, 0), "end": time(18, 0)}
        ],
    }
    schedule = Schedule.from_dict(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == []


def test_get_free_slots_with_gaps():
    data = {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 15),
                "start": time(9, 0),
                "end": time(18, 0),
            }
        ],
        "timeslot": [
            {"id": 1, "day_id": 1, "start": time(10, 0), "end": time(11, 0)},
            {"id": 2, "day_id": 1, "start": time(13, 0), "end": time(14, 0)},
            {"id": 3, "day_id": 1, "start": time(16, 0), "end": time(17, 0)},
        ],
    }
    schedule = Schedule.from_dict(data)

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
                "id": 1,
                "date": date(2025, 2, 15),
                "start": time(8, 0),
                "end": time(20, 0),
            }
        ],
        "timeslot": [
            {"id": 1, "day_id": 1, "start": time(8, 0), "end": time(10, 0)},
            {"id": 2, "day_id": 1, "start": time(18, 0), "end": time(20, 0)},
        ],
    }
    schedule = Schedule.from_dict(data)

    assert schedule.get_free_slots(date(2025, 2, 15)) == [
        (time(10, 0), time(18, 0))
    ]


def test_timeslot_outside_workday():
    data = {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 20),
                "start": time(9, 0),
                "end": time(17, 0),
            }
        ],
        "timeslot": [
            {"id": 1, "day_id": 1, "start": time(8, 0), "end": time(18, 0)}
        ],
    }
    schedule = Schedule.from_dict(data)
    result = schedule.get_free_slots(date(2025, 2, 20))

    assert result == []


def test_empty_schedule():
    schedule = Schedule.from_dict({"days": [], "timeslot": []})

    with pytest.raises(ScheduleDateNotFoundError):
        schedule.get_free_slots(date(2025, 2, 15))
