from datetime import datetime
from typing import Any

from user import User, Student, Captain
from court import Court
from reservation import Reservation, StudentReservation, CaptainReservation

class ReservationFactory:
    @staticmethod
    def create(
        student: Student, 
        court: Court, 
        start_datetime: datetime, 
        end_datetime: datetime, 
        requested_at: datetime
    ) -> Reservation:
        if isinstance(student, Captain):
            print("[Factory] Creating CaptainReservation")
            return CaptainReservation(
                student, court, start_datetime, end_datetime, requested_at
            )

        if isinstance(student, Student):
            print("[Factory] Creating StudentReservation")
            return StudentReservation(
                student, court, start_datetime, end_datetime, requested_at
            )

        raise TypeError("Unhandled user type")