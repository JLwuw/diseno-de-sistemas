from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from reservation import Reservation


class CourtStatus(Enum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"


class Court:
    def __init__(self, name: str, status: CourtStatus) -> None:
        self.name: str = name
        self.status: CourtStatus = status
        self.reservations: List[Reservation] = []

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        return (
            self.status is CourtStatus.AVAILABLE
            and not self.has_conflict(start_time, end_time)
        )

    def has_conflict(self, start_time: datetime, end_time: datetime) -> bool:
        return any(
            reservation.overlaps(start_time, end_time)
            for reservation in self.reservations
        )

    def add_reservation(self, reservation: Reservation) -> None:
        if reservation.court is not self:
            raise ValueError("The reservation belongs to another court.")
        if not self.is_available(
            reservation.start_time, reservation.end_time
        ):
            raise ValueError("The court is not available for that time.")
        self.reservations.append(reservation)
        reservation.student.add_reservation(reservation)

    def remove_reservation(self, reservation: Reservation) -> None:
        self.reservations.remove(reservation)

    def __str__(self) -> str:
        return f"{self.name} ({self.status.value})"