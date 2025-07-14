from datetime import date, time

import pytest

from trajectory_test_assignment.app import (
    Workday,
    Schedule,
    ScheduleDateNotFoundError,
)
from trajectory_test_assignment.infrastructure import dict_to_schedule


@pytest.fixture
def sample_schedule_data():
    return {
        "days": [
            {
                "id": "1",
                "date": "2025-02-15",
                "start": "09:00",
                "end": "21:00",
            },
            {
                "id": "2",
                "date": "2025-02-16",
                "start": "08:00",
                "end": "22:00",
            },
        ],
        "timeslots": [
            {"id": "1", "day_id": "1", "start": "09:00", "end": "12:00"},
            {"id": "2", "day_id": "1", "start": "17:30", "end": "20:00"},
            {"id": "3", "day_id": "2", "start": "14:30", "end": "18:00"},
        ],
    }


@pytest.mark.parametrize(
    "check_date, expected",
    [
        (
            date(2025, 2, 15),
            [(time(9, 0), time(12, 0)), (time(17, 30), time(20, 0))],
        ),
        (date(2025, 2, 16), [(time(14, 30), time(18, 0))]),
    ],
)
def test_get_busy_slots(sample_schedule_data, check_date, expected):
    schedule = dict_to_schedule(sample_schedule_data)

    assert schedule.get_busy_slots(check_date) == expected


def test_get_busy_slots_empty():
    days = [
        Workday(
            id_="3", date=date(2025, 2, 17), start=time(9, 0), end=time(18, 0)
        )
    ]
    schedule = Schedule(days, [])

    assert schedule.get_busy_slots(date(2025, 2, 17)) == []


def test_overlapping_timeslots():
    data = {
        "days": [
            {
                "id": "1",
                "date": "2025-02-21",
                "start": "09:00",
                "end": "18:00",
            }
        ],
        "timeslots": [
            {"id": "1", "day_id": "1", "start": "10:00", "end": "12:00"},
            {"id": "2", "day_id": "1", "start": "11:30", "end": "13:00"},
        ],
    }
    schedule = dict_to_schedule(data)
    result = schedule.get_busy_slots(date(2025, 2, 21))

    assert result == [
        (time(10, 0), time(12, 0)),
        (time(11, 30), time(13, 0)),
    ]


def test_timeslot_invalid_day_reference():
    data = {
        "days": [
            {
                "id": "1",
                "date": "2025-02-22",
                "start": "09:00",
                "end": "17:00",
            }
        ],
        "timeslots": [
            {"id": "1", "day_id": "99", "start": "10:00", "end": "11:00"}
        ],
    }
    schedule = dict_to_schedule(data)

    assert schedule.get_busy_slots(date(2025, 2, 22)) == []


def test_empty_schedule():
    schedule = dict_to_schedule({"days": [], "timeslots": []})

    with pytest.raises(ScheduleDateNotFoundError):
        schedule.get_busy_slots(date(2025, 2, 15))
