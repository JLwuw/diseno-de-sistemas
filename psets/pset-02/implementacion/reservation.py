from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from datetime import timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from cancellation import *

if TYPE_CHECKING:
    from user import Student


class ReservationStatus(Enum):
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    NO_SHOW = "no-show"


class Reservation(ABC):
    def __init__(
        self,
        student: Student,
        court: Any,
        start_time: datetime,
        end_time: datetime,
        requested_at: datetime,
        cancellation_policy: CancellationPolicy,
    ) -> None:
        if end_time <= start_time:
            raise ValueError("The reservation must end after it starts.")
        self.student = student
        self.court = court
        self.start_time = start_time
        self.end_time = end_time
        self.requested_at = requested_at
        self.status = ReservationStatus.ACTIVE
        self.cancellation_policy = cancellation_policy

    def cancel(self, current_time: datetime, policy: Optional[CancellationPolicy] = None) -> None:
        cancellation_policy = policy or self.cancellation_policy
        cancellation_policy.cancel(self, current_time)

    def force_cancel(self, current_time: datetime) -> None:
        self.cancel(
            current_time,
            policy=AdminCancellation()
        )

    def finish(self, current_time: datetime) -> None:
        if self.status is not ReservationStatus.ACTIVE:
            raise ValueError("Only active reservations can be finished.")
        if current_time < self.end_time:
            raise ValueError("A reservation cannot finish before its end time.")
        self.status = ReservationStatus.FINISHED

    def is_active(self) -> bool:
        return self.status is ReservationStatus.ACTIVE

    def overlaps(self, start_time: datetime, end_time: datetime) -> bool:
        return (
            self.is_active()
            and start_time < self.end_time
            and end_time > self.start_time
        )

    def __str__(self) -> str:
        return (
            f"{self.student.email} on {self.court.name} "
            f"({self.start_time:%H:%M}-{self.end_time:%H:%M}, "
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