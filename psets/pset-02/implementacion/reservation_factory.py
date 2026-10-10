from datetime import datetime
from typing import Any

from campus import CampusEnum
from user import User, Student, Captain
from reservation import Reservation, StudentReservation, CaptainReservation

class ReservationFactory:
    @staticmethod
    def create(
        student: Student, 
        court: Any, 
        campus: CampusEnum,
        start_datetime: datetime, 
        end_datetime: datetime, 
        requested_at: datetime
    ) -> Reservation:
        if isinstance(student, Captain):
            return CaptainReservation(
                student, court, campus, start_datetime, end_datetime, requested_at
            )

        if isinstance(student, Student):
            return StudentReservation(
                student, court, campus, start_datetime, end_datetime, requested_at
            )

        raise TypeError("Unhandled user type")