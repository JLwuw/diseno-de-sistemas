from enum import Enum


class CourtStatus(Enum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"


class Court:
    def __init__(self, name, status=CourtStatus.AVAILABLE):
        self.name = name
        self.status = status
        self.reservations = []

    def is_available(self, start_time, end_time):
        return (
            self.status is CourtStatus.AVAILABLE
            and not self.has_conflict(start_time, end_time)
        )

    def has_conflict(self, start_time, end_time):
        return any(
            reservation.overlaps(start_time, end_time)
            for reservation in self.reservations
        )

    def add_reservation(self, reservation):
        if reservation.court is not self:
            raise ValueError("The reservation belongs to another court.")
        if not self.is_available(
            reservation.start_time, reservation.end_time
        ):
            raise ValueError("The court is not available for that time.")
        self.reservations.append(reservation)
        reservation.student.add_reservation(reservation)

    def remove_reservation(self, reservation):
        self.reservations.remove(reservation)

    def __str__(self):
        return f"{self.name} ({self.status.value})"