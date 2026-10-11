from abc import ABC, abstractmethod
from datetime import datetime

from user import Student
from court import Court
from system_config import SystemConfig
from reservation import Reservation


class ReservationPolicy(ABC):
    @staticmethod
    @abstractmethod
    def validate_reservation(
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> bool:
        pass


class StudentReservationPolicy(ReservationPolicy):
    @staticmethod
    def validate_reservation(
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> bool:
        
        return court.is_available(start_datetime, end_datetime)


class CaptainReservationPolicy(ReservationPolicy):
    @staticmethod
    def validate_reservation(
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> bool:

        if court.is_available(start_datetime, end_datetime):
            return True

        system_config = SystemConfig.get_instance()
        priority_end_time = system_config.captain_priority_end_time

        if requested_at.time() >= priority_end_time:
            return False

        conflicts = court.get_conflicting_reservations(start_datetime, end_datetime)
        for reservation in conflicts:
            if reservation.priority() <= user.reservation_priority:
                return False

        for reservation in conflicts:
            reservation.force_cancel(requested_at)

        return True

