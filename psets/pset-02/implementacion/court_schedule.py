from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from enum import IntEnum


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


@dataclass(frozen=True)
class TimeBracket:
    start_time: time
    end_time: time

    def __post_init__(self) -> None:
        if self.end_time <= self.start_time:
            raise ValueError("A time bracket must end after it starts.")

    def contains(self, start_time: time, end_time: time) -> bool:
        return self.start_time <= start_time and end_time <= self.end_time
    
    def overlaps(self, start_time: time, end_time: time) -> bool:
        return start_time < self.end_time and end_time > self.start_time


class CourtSchedule:
    def __init__(self) -> None:
        self._brackets: dict[Weekday, list[TimeBracket]] = {
            weekday: [] for weekday in Weekday
        }

    def add_bracket(self, weekday: Weekday, start_time: time, end_time: time) -> None:
        for bracket in self._brackets[weekday]:
            if bracket.overlaps(start_time, end_time):
                raise ValueError("The time bracket overlaps an existing bracket.")
        
        bracket = TimeBracket(start_time, end_time)
        self._brackets[weekday].append(bracket)
        self._brackets[weekday].sort(key=lambda item: item.start_time)

    def remove_bracket(self, weekday: Weekday, bracket: TimeBracket) -> None:
        self._brackets[weekday].remove(bracket)

    def is_available(self, start_datetime: datetime, end_datetime: datetime) -> bool:
        if end_datetime <= start_datetime:
            return False
        if start_datetime.date() != end_datetime.date():
            return False

        weekday = Weekday(start_datetime.weekday())
        return any(
            bracket.contains(start_datetime.time(), end_datetime.time())
            for bracket in self._brackets[weekday]
        )

    def get_brackets_for(self, weekday: Weekday) -> tuple[TimeBracket, ...]:
        return tuple(self._brackets[weekday])
