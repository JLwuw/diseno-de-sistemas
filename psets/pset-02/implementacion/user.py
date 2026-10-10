from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, Any, List

from campus import CampusEnum
from court import Court

if TYPE_CHECKING:
    from reservation import Reservation

class User(ABC):
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

    def add_reservation(self, reservation: Reservation) -> None:
        self.reservations.append(reservation)
        

class Captain(Student):
    pass