from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True, slots=True)
class Workday:
    id_: int
    date: date
    start: time
    end: time
