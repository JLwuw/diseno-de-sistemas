from abc import ABC, abstractmethod
from datetime import datetime

from user import Student
from court import Court
from system_config import SystemConfig
from reservation import Reservation
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(frozen=True)
class ReservationDecision:
    approved: bool
    reservations_to_force_cancel: Tuple[Reservation, ...]
    reason: Optional[str]


class ReservationPolicy(ABC):
    @staticmethod
    def _validate_common(
        user: Student,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> Optional[ReservationDecision]:
        if end_datetime <= start_datetime:
            return ReservationDecision(False, (), "End must be after start")

        if start_datetime.date() != end_datetime.date():
            return ReservationDecision(False, (), "Reservation must remain on one day")

        month_start = requested_at.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        if user.no_shows_since(month_start) >= SystemConfig.get_instance().no_show_monthly_limit:
            return ReservationDecision(False, (), "Max no shows exceeded")

        return None


    @staticmethod
    @abstractmethod
    def validate_reservation(
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> ReservationDecision:
        pass


class StudentReservationPolicy(ReservationPolicy):
    @staticmethod
    def validate_reservation(
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> ReservationDecision:
        print("[Strategy] StudentReservationPolicy validating request")
        common_decision = ReservationPolicy._validate_common(
            user, start_datetime, end_datetime, requested_at
        )
        if common_decision is not None:
            print(f"[Strategy] Student policy rejected: {common_decision.reason}")
            return common_decision
        
        if not court.is_available(start_datetime, end_datetime):
            print("[Strategy] Student policy rejected: court unavailable")
            return ReservationDecision(False, (), "Court unavailable at desired time")
        
        print("[Strategy] Student policy approved request")
        return ReservationDecision(True, (), None)


class CaptainReservationPolicy(ReservationPolicy):
    @staticmethod
    def validate_reservation(
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: datetime,
    ) -> ReservationDecision:
        print("[Strategy] CaptainReservationPolicy validating request")
        common_decision = ReservationPolicy._validate_common(
            user, start_datetime, end_datetime, requested_at
        )
        if common_decision is not None:
            print(f"[Strategy] Captain policy rejected: {common_decision.reason}")
            return common_decision
        
        if court.is_available(start_datetime, end_datetime):
            print("[Strategy] Captain policy approved: court is available")
            return ReservationDecision(True, (), None)

        system_config = SystemConfig.get_instance()
        priority_end_time = system_config.captain_priority_end_time
        if requested_at.time() >= priority_end_time:
            print("[Strategy] Captain priority window has ended")
            return ReservationDecision(False, (), "Outside priority window")

        conflicts = court.get_conflicting_reservations(start_datetime, end_datetime)
        for reservation in conflicts:
            if reservation.priority() >= user.reservation_priority:
                print("[Strategy] Captain policy rejected: equal or higher priority conflict")
                return ReservationDecision(False, (), "Conflicting reservation with priority")

        print(f"[Strategy] Captain policy approved and will replace {len(conflicts)} conflict(s)")
        return ReservationDecision(True, tuple(conflicts), "Priority over reservations")

