from __future__ import annotations

from court import Court
from datetime import date, datetime, time, timedelta
from system_config import SystemConfig
from typing import Optional, List
from dataclasses import dataclass
from reservation import Reservation
from reservation_factory import ReservationFactory
from user import Captain


@dataclass(frozen=True)
class RecurringReservationResult:
    reservations: tuple[Reservation, ...]
    conflicting_weeks: tuple[int, ...]

    @property
    def approved(self) -> bool:
        return not self.conflicting_weeks


class RecurringReservation:
    def __init__(
        self,
        captain: Captain,
        court: Court,
        start_date: date,
        start_time: time,
        end_time: time,
        weeks_to_reserve: int,
        equipment: Optional[list[str]],
        notes: Optional[str],
    ) -> None:
        self.captain = captain
        self.court = court
        self.weeks_to_reserve = weeks_to_reserve
        self.equipment = equipment
        self.notes = notes
        self.reservations: List[Reservation]
        self.start_date = start_date
        self.start_time = start_time
        self.end_time = end_time


    def create_reservations(self) -> RecurringReservationResult:
        reservations: List[Reservation] = []
        conflicting_weeks: list[int] = []
        start_recurring_datetime = datetime.combine(self.start_date, self.start_time)
        end_recurring_datetime = datetime.combine(self.start_date, self.end_time)
        reservation_factory = ReservationFactory()

        for i in range(self.weeks_to_reserve):
            start_datetime = start_recurring_datetime + timedelta(days=(7*i))
            end_datetime =  end_recurring_datetime + timedelta(days=(7*i))

            if self.court.has_conflict(start_datetime, end_datetime):
                conflicting_weeks.append(i + 1)
                continue


            reservation = reservation_factory.create(
                self.captain, self.court, start_datetime, end_datetime, datetime.now()
            )
            
            reservations.append(reservation)

        if conflicting_weeks:
            return RecurringReservationResult((), tuple(conflicting_weeks))

        return RecurringReservationResult(tuple(reservations), ())


class RecurringReservationBuilder:
    def __init__(
        self,
        captain: Captain,
        court: Court,
        start_date: date,
        start_time: time,
        end_time: time,
        weeks_to_reserve: int
    ) -> None:

        system_config = SystemConfig.get_instance()
        min_weeks = system_config.min_recurring_reservation_weeks
        max_weeks = system_config.max_recurring_reservation_weeks

        if not min_weeks <= weeks_to_reserve <= max_weeks:
            raise ValueError(f"Recurring reservations must last {min_weeks} to {max_weeks} weeks.")

        if end_time <= start_time:
            raise ValueError("End time must be after start time")

        self.captain = captain
        self.court = court
        self.start_date = start_date
        self.start_time = start_time
        self.end_time = end_time
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
            self.captain,
            self.court,
            self.start_date,
            self.start_time,
            self.end_time,
            self.weeks_to_reserve,
            self.equipment,
            self.notes,
        )
