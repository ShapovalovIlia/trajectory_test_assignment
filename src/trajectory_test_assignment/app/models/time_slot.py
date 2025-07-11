from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True, slots=True)
class TimeSlot:
    id_: int
    day_id: int
    start: time
    end: time
