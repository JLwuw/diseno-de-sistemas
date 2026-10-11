from abc import ABC, abstractmethod
from datetime import datetime

from user import Student
from court import Court
from campus import CampusEnum
from system_config import SystemConfig
from reservation import Reservation, CaptainReservation


class ReservationCreationPolicy(ABC):
    @staticmethod
    @abstractmethod
    def validate_reservation(
        user: Student,
        court: Court,
        campus: CampusEnum,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> bool:
        pass


class StudentReservationPolicy(ReservationCreationPolicy):
    @staticmethod
    def validate_reservation(
        user: Student,
        court: Court,
        campus: CampusEnum,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> bool:
        
        return court.is_available(start_datetime, end_datetime, campus)


class CaptainReservationPolicy(ReservationCreationPolicy):
    @staticmethod
    def validate_reservation(
        user: Student,
        court: Court,
        campus: CampusEnum,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> bool:

        if court.is_available(start_datetime, end_datetime, campus):
            return True

        system_config = SystemConfig.get_instance()
        priotity_end_time = system_config.captain_priority_end_time

        if requested_at.hour > priotity_end_time.hour:
            return False

        conflicts = court.get_conflicting_reservations(start_datetime, end_datetime, campus)
        for reservation in conflicts:
            if isinstance(reservation, CaptainReservation):
                return False


        return True

