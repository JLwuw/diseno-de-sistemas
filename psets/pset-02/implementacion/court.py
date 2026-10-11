from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from reservation import Reservation, ReservationStatus
    from campus import CampusEnum


class CourtStatus(IntEnum):
    AVAILABLE = 0
    MAINTENANCE = 1


class Court:
    def __init__(self, name: str, status: CourtStatus) -> None:
        self.name = name
        self.status = status
        self.reservations: List[Reservation] = []

    def is_available(self, start_datetime: datetime, end_datetime: datetime, campus: CampusEnum) -> bool:
        return (
            self.status is CourtStatus.AVAILABLE
            and not self.has_conflict(start_datetime, end_datetime, campus)
        )

    def has_conflict(self, start_datetime: datetime, end_datetime: datetime, campus: CampusEnum) -> bool:
        return any(
            reservation.campus == campus
            and reservation.status == ReservationStatus.ACTIVE
            and reservation.overlaps(start_datetime, end_datetime)
            for reservation in self.reservations
        )

    def get_conflicting_reservations(self, start_datetime: datetime, end_datetime: datetime, campus: CampusEnum) -> List[Reservation]:
        conflicting = []

        for reservation in self.reservations:
            if self.has_conflict(start_datetime, end_datetime, campus):
                conflicting.append(reservation)

        return conflicting

    def add_reservation(self, reservation: Reservation) -> None:
        if reservation.court is not self:
            raise ValueError("The reservation belongs to another court.")

        start_datetime = reservation.start_datetime
        end_datetime = reservation.end_datetime
        campus = reservation.campus
        if not self.is_available(start_datetime, end_datetime, campus):
            raise ValueError("The court is not available for that time.")
        
        self.reservations.append(reservation)
        reservation.student.add_reservation(reservation)

    def remove_reservation(self, reservation: Reservation) -> None:
        self.reservations.remove(reservation)

    def __str__(self) -> str:
        return f"{self.name} ({self.status.value})"