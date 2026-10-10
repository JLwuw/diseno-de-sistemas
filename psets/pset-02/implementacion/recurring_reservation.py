from court import Court
from datetime import date, datetime, time
from enum import IntEnum
from system_config import SystemConfig
from typing import Optional


class Weekday(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class RecurringReservation:
    def __init__(
        self,
        court: Court,
        weekday: Weekday,
        start_time: time,
        weeks_to_reserve: int,
        equipment: Optional[list[str]],
        notes: Optional[str],
    ) -> None:
        self.court = court
        self.weekday = weekday
        self.start_time = start_time
        self.weeks_to_reserve = weeks_to_reserve
        self.equipment = equipment
        self.notes = notes

    def occurrence_on(self, year: int, week: int) -> datetime:
        reservation_date = date.fromisocalendar(
            year,
            week,
            self.weekday,
        )
        return datetime.combine(reservation_date, self.start_time)

    def create_reservations(self):
        pass


class RecurringReservationBuilder:
    def __init__(
        self,
        court: Court,
        weekday: Weekday,
        start_time: time,
        weeks_to_reserve: int
    ) -> None:

        system_config = SystemConfig.get_instance()
        min_weeks = system_config.min_recurring_reservation_weeks
        max_weeks = system_config.max_recurring_reservation_weeks

        if not min_weeks <= weeks_to_reserve <= max_weeks:
            raise ValueError(f"Recurring reservations must last {min_weeks} to {max_weeks} weeks.")

        self.court = court
        self.weekday = weekday
        self.start_time = start_time
        self.weeks_to_reserve = weeks_to_reserve
        self.equipment: list[str] = []
        self.notes: Optional[str] = None

    def with_equipment(self, equipment: list[str]) -> RecurringReservationBuilder:
        self.equipment = equipment
        return self

    def with_notes(self, notes: str) -> RecurringReservationBuilder:
        self.notes = notes
        return self

    def build(self) -> RecurringReservation:
        return RecurringReservation(
            self.court,
            self.weekday,
            self.start_time,
            self.weeks_to_reserve,
            self.equipment,
            self.notes,
        )
