from datetime import timedelta
from enum import Enum


class ReservationStatus(Enum):
    ACTIVE = "active"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    NO_SHOW = "no-show"


class Reservation:
    def __init__(self, student, court, start_time, end_time, requested_at):
        if end_time <= start_time:
            raise ValueError("The reservation must end after it starts.")
        self.student = student
        self.court = court
        self.start_time = start_time
        self.end_time = end_time
        self.requested_at = requested_at
        self.status = ReservationStatus.ACTIVE

    def priority(self):
        return self.student.priority_rule.get_priority(self)

    def cancel(self, current_time):
        if self.status is not ReservationStatus.ACTIVE:
            raise ValueError("Only active reservations can be cancelled.")
        remaining = self.start_time - current_time
        if remaining < timedelta(hours=2):
            self.status = ReservationStatus.NO_SHOW
        else:
            self.status = ReservationStatus.CANCELLED

    def finish(self, current_time):
        if self.status is not ReservationStatus.ACTIVE:
            raise ValueError("Only active reservations can be finished.")
        if current_time < self.end_time:
            raise ValueError("A reservation cannot finish before its end time.")
        self.status = ReservationStatus.FINISHED

    def is_active(self):
        return self.status is ReservationStatus.ACTIVE

    def overlaps(self, start_time, end_time):
        return (
            self.is_active()
            and start_time < self.end_time
            and end_time > self.start_time
        )

    def __str__(self):
        return (
            f"{self.student.email} on {self.court.name} "
            f"({self.start_time:%H:%M}-{self.end_time:%H:%M}, "
            f"{self.status.value})"
        )