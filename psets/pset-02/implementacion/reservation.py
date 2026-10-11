from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from datetime import timedelta
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from user import Student

from cancellation import (
    AdminCancellation,
    CancellationPolicy,
    CaptainCancellation,
    StudentCancellation,
)


class ReservationPriority(IntEnum):
    ADMIN = 0
    CAPTAIN = 1
    STUDENT = 2


class ReservationStatus(IntEnum):
    ACTIVE = 0
    FINISHED = 1
    CANCELLED = 2
    NO_SHOW = 3


class Reservation(ABC):
    def __init__(
        self,
        student: Student,
        court: Any,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
        cancellation_policy: CancellationPolicy,
    ) -> None:
        if end_datetime <= start_datetime:
            raise ValueError("The reservation must end after it starts.")
        
        if start_datetime.date() != end_datetime.date():
            raise ValueError("Reservations must only span a single day")
        
        self.student = student
        self.court = court
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.requested_at = requested_at
        self.status = ReservationStatus.ACTIVE
        self.cancellation_policy = cancellation_policy

    def priority(self) -> ReservationPriority:
        return self.student.reservation_priority

    def cancel(self, current_time: datetime, policy: Optional[CancellationPolicy] = None) -> None:
        cancellation_policy = policy or self.cancellation_policy
        cancellation_policy.cancel(self, current_time)

    def force_cancel(self, current_time: datetime) -> None:
        self.cancel(
            current_time,
            policy=AdminCancellation()
        )

    def finish(self, current_datetime: datetime) -> None:
        if self.status is not ReservationStatus.ACTIVE:
            raise ValueError("Only active reservations can be finished.")
        
        if current_datetime < self.end_datetime:
            raise ValueError("A reservation cannot finish before its end time.")
        
        self.status = ReservationStatus.FINISHED

    def is_active(self) -> bool:
        return self.status is ReservationStatus.ACTIVE

    def overlaps(self, start_time: datetime, end_time: datetime) -> bool:
        return (
            self.is_active()
            and start_time < self.end_datetime
            and end_time > self.start_datetime
        )

    def __str__(self) -> str:
        return (
            f"{self.student.email} on {self.court.name} "
            f"({self.start_datetime:%H:%M}-{self.end_datetime:%H:%M}, "
            f"{self.status.value})"
        )


class StudentReservation(Reservation):
    def __init__(
        self,
        student: Student,
        court: Any,
        start_time: datetime,
        end_time: datetime,
        requested_at: datetime,
    ) -> None:
        cancellation_policy = StudentCancellation()
        super().__init__(student, court, start_time, end_time, requested_at, cancellation_policy)


class CaptainReservation(Reservation):
    def __init__(
        self,
        student: Student,
        court: Any,
        start_time: datetime,
        end_time: datetime,
        requested_at: datetime,
    ) -> None:
        cancellation_policy = CaptainCancellation()
        super().__init__(student, court, start_time, end_time, requested_at, cancellation_policy)