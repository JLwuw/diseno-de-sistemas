from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, List

from campus import CampusEnum
from court import Court
from reservation import ReservationPriority
from reservation_status import ReservationStatus

if TYPE_CHECKING:
    from reservation import Reservation
    from reservation_policy import ReservationDecision, ReservationPolicy

class User(ABC):
    reservation_priority: ClassVar[ReservationPriority]

    def __init__(self, email: str, password: str, phone_number: str) -> None:
        self.email = email
        self._password = password
        self.phone_number = phone_number
        
        self.logged_in = False

    def login(self, email: str, password: str) -> bool:
        self.logged_in = (
            email == self.email
            and password == self._password
        )
        return self.logged_in

    def logout(self) -> None:
        self.logged_in = False


class Student(User):
    reservation_priority = ReservationPriority.STUDENT

    def __init__(
            self, 
            email: str, 
            password: str, 
            phone_number: str, 
            student_code: str, 
            campus: CampusEnum

        ) -> None:
        super().__init__(email, password, phone_number)
        self.student_code = student_code
        self.campus = campus

        self.reservations: List[Reservation] = []
        from reservation_policy import StudentReservationPolicy
        self.reservation_policy = StudentReservationPolicy()

    def add_reservation(self, reservation: Reservation) -> None:
        self.reservations.append(reservation)
    
    def no_shows_since(self, start: datetime) -> int:
        return sum(
            reservation.status is ReservationStatus.NO_SHOW
            and reservation.no_show_at is not None
            and reservation.no_show_at >= start
            for reservation in self.reservations
        )

    def validate_reservation(
        self,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> ReservationDecision:
        return self.reservation_policy.validate_reservation(
            self,
            court,
            start_datetime,
            end_datetime,
            requested_at,
        )


class Captain(Student):
    reservation_priority = ReservationPriority.CAPTAIN

    def __init__(
        self,
        email: str,
        password: str,
        phone_number: str,
        student_code: str,
        campus: CampusEnum,
    ) -> None:
        super().__init__(email, password, phone_number, student_code, campus)
        from reservation_policy import CaptainReservationPolicy
        self.reservation_policy = CaptainReservationPolicy()