from datetime import date, time

import pytest

from trajectory_test_assignment.app import Workday, TimeSlot, Schedule


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


def test_from_dict_objects(sample_schedule_data):
    schedule = Schedule.from_dict(sample_schedule_data)

    assert isinstance(schedule, Schedule)
    assert all(isinstance(d, Workday) for d in schedule.days)
    assert all(isinstance(ts, TimeSlot) for ts in schedule.timeslots)

    assert schedule.days[0].date == date(2025, 2, 15)
    assert schedule.timeslots[0].start == time(9, 0)
