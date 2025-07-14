from datetime import date, time

from trajectory_test_assignment.app.models.schedule import (
    Schedule,
    Workday,
    TimeSlot,
)


def dict_to_schedule(data: dict) -> Schedule:
    days = [
        Workday(
            id_=int(day["id"]),
            date=date.fromisoformat(day["date"]),
            start=time.fromisoformat(day["start"]),
            end=time.fromisoformat(day["end"]),
        )
        for day in data["days"]
    ]

    timeslots = [
        TimeSlot(
            id_=int(ts["id"]),
            day_id=int(ts["day_id"]),
            start=time.fromisoformat(ts["start"]),
            end=time.fromisoformat(ts["end"]),
        )
        for ts in data["timeslots"]
    ]

    return Schedule(days, timeslots)
