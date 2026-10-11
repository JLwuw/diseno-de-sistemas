from __future__ import annotations

from datetime import time, date, datetime
from typing import Optional
from court import Court, CourtStatus
from copy import deepcopy

from user import User
from reservation import Reservation
from reservation import ReservationPriority
from schedule import CourtSchedule

class Admin(User):
    reservation_priority = ReservationPriority.ADMIN

    def __init__(self, email: str, password: str, phone_number: str) -> None:
        super().__init__(email, password, phone_number)
        self.courts = []

    def add_court(self, court: Court) -> None:
        self.courts.append(court)

    def remove_court(self, court: Court) -> None:
        self.courts.remove(court)

    def update_court(self, court: Court, status: CourtStatus) -> None:
        if court not in self.courts:
            raise ValueError("The administrator does not manage this court.")
        court.status = status

    def update_court_schedule(
        self,
        court: Court,
        schedule: CourtSchedule,
    ) -> None:
        if court not in self.courts:
            raise ValueError("The administrator does not manage this court.")
        court.schedule = schedule

    def resolve_reservation_conflict(self, reservations: list[Reservation]):
        if not reservations:
            raise ValueError("At least one request is required.")
        return min(reservations, key=lambda reservation: reservation.priority())

    def apply_block(self, admin_block: AdminBlock, court: Court, date: date):
        if court not in self.courts:
            raise ValueError("The administrator does not manage this court.")

        admin_block.apply_to(court, date)
    

class AdminBlock():
    def __init__(
            self, 
            start_time: time,
            end_time: time,
            motive: str, 
            equipment: Optional[list[str]],
        ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.motive = motive
        self.equipment = equipment


    def copy(self) -> AdminBlock:
        return deepcopy(self)

    def apply_to(self, court: Court, date: date):
        start_datetime = datetime.combine(date, self.start_time)
        end_datetime = datetime.combine(date, self.end_time)

        conflicts = court.get_conflicting_reservations(start_datetime, end_datetime)

        for reservation in conflicts:
            reservation.force_cancel(datetime.now())

    