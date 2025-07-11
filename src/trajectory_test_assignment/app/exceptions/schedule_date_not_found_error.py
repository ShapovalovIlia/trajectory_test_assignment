from datetime import date


class ScheduleDateNotFoundError(Exception):
    """Raised when the requested date is not found in the schedule."""

    def __init__(self, date: date):
        super().__init__(f"No workday found for date: {date}")
