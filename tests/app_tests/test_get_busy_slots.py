from datetime import date, time

import pytest

from trajectory_test_assignment.app import (
    Workday,
    Schedule,
    ScheduleDateNotFoundError,
)


@pytest.fixture
def sample_schedule_data():
    return {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 15),
                "start": time(9, 0),
                "end": time(21, 0),
            },
            {
                "id": 2,
                "date": date(2025, 2, 16),
                "start": time(8, 0),
                "end": time(22, 0),
            },
        ],
        "timeslot": [
            {"id": 1, "day_id": 1, "start": time(9, 0), "end": time(12, 0)},
            {"id": 2, "day_id": 1, "start": time(17, 30), "end": time(20, 0)},
            {"id": 3, "day_id": 2, "start": time(14, 30), "end": time(18, 0)},
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
    schedule = Schedule.from_dict(sample_schedule_data)

    assert schedule.get_busy_slots(check_date) == expected


def test_get_busy_slots_empty():
    days = [
        Workday(
            id_=3, date=date(2025, 2, 17), start=time(9, 0), end=time(18, 0)
        )
    ]
    schedule = Schedule(days, [])

    assert schedule.get_busy_slots(date(2025, 2, 17)) == []


def test_overlapping_timeslots():
    data = {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 21),
                "start": time(9, 0),
                "end": time(18, 0),
            }
        ],
        "timeslot": [
            {"id": 1, "day_id": 1, "start": time(10, 0), "end": time(12, 0)},
            {"id": 2, "day_id": 1, "start": time(11, 30), "end": time(13, 0)},
        ],
    }
    schedule = Schedule.from_dict(data)
    result = schedule.get_busy_slots(date(2025, 2, 21))

    assert result == [
        (time(10, 0), time(12, 0)),
        (time(11, 30), time(13, 0)),
    ]


def test_timeslot_invalid_day_reference():
    data = {
        "days": [
            {
                "id": 1,
                "date": date(2025, 2, 22),
                "start": time(9, 0),
                "end": time(17, 0),
            }
        ],
        "timeslot": [
            {"id": 1, "day_id": 99, "start": time(10, 0), "end": time(11, 0)}
        ],
    }
    schedule = Schedule.from_dict(data)

    assert schedule.get_busy_slots(date(2025, 2, 22)) == []


def test_empty_schedule():
    schedule = Schedule.from_dict({"days": [], "timeslot": []})

    with pytest.raises(ScheduleDateNotFoundError):
        schedule.get_busy_slots(date(2025, 2, 15))
