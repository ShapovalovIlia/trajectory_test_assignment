from datetime import date, time

from trajectory_test_assignment.app.models import Workday, TimeSlot
from trajectory_test_assignment.app.exceptions import ScheduleDateNotFoundError


class Schedule:
    def __init__(self, days: list[Workday], timeslots: list[TimeSlot]):
        self.days = days
        self.timeslots = timeslots
        self.date_map = {day.date: day for day in days}

    def get_busy_slots(self, date: date) -> list[tuple[time, time]]:
        """
        Returns the list of occupied time intervals for the given date.

        :param date: Date to retrieve busy slots for.
        :raises ScheduleDateNotFoundError: If the date is not present in the schedule.
        :return: List of (start, end) tuples representing busy intervals.
        """
        if date not in self.date_map:
            raise ScheduleDateNotFoundError(date)

        day_id = self.date_map[date].id_
        return sorted(
            [
                (ts.start, ts.end)
                for ts in self.timeslots
                if ts.day_id == day_id
            ]
        )

    def get_free_slots(self, date: date) -> list[tuple[time, time]]:
        """
        Returns the list of free time intervals for the given date.

        :param date: Date to retrieve free slots for.
        :raises ScheduleDateNotFoundError: If the date is not present in the schedule.
        :return: List of (start, end) tuples representing free intervals.
        """
        if date not in self.date_map:
            raise ScheduleDateNotFoundError(date)

        day = self.date_map[date]
        busy_slots = self.get_busy_slots(date)

        free_slots = []
        current_start = day.start

        for start, end in busy_slots:
            if current_start < start:
                free_slots.append((current_start, start))
            current_start = end

        if current_start < day.end:
            free_slots.append((current_start, day.end))

        return free_slots

    def is_time_available(self, date: date, start: time, end: time) -> bool:
        """
        Returns True if the given time interval [start, end) is fully available (not busy) on the given date.
        Raises ScheduleDateNotFoundError if the date is not in the schedule.
        """

        if date not in self.date_map:
            raise ScheduleDateNotFoundError(date)

        for busy_start, busy_end in self.get_busy_slots(date):
            if not (end <= busy_start or start >= busy_end):
                return False

        day = self.date_map[date]

        return day.start <= start < end <= day.end
