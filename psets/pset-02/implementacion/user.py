from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from reservation import Reservation

class User(ABC):
    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self._password: str = password
        self.logged_in: bool = False

    def login(self, email: str, password: str) -> bool:
        self.logged_in = (
            email == self.email
            and password == self._password
        )
        return self.logged_in

    def logout(self) -> None:
        self.logged_in = False


class Student(User):
    def __init__(self, email: str, password: str, student_code: str) -> None:
        super().__init__(email, password)
        self.student_code: str = student_code
        self.reservations: List[Reservation] = []

    def request_reservation(self, court: Any, start_time: datetime, end_time: datetime, requested_at: datetime) -> None:
        pass

    def add_reservation(self, reservation: Reservation) -> None:
        self.reservations.append(reservation)

    def get_upcoming_reservations(self, current_time: datetime) -> None:
        pass

    def cancel_reservation(self, reservation: Reservation, current_time: datetime) -> None:
        pass

class Captain(Student):
    pass