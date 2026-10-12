from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from system_config import SystemConfig
from reservation_status import ReservationStatus

if TYPE_CHECKING:
    from reservation import Reservation
    from user import User
else:
    from reservation_status import ReservationStatus


class CancellationPolicy(ABC):
    @staticmethod
    def _validate_active(reservation: Reservation) -> None:
        if reservation.status is not ReservationStatus.ACTIVE:
            raise ValueError("Only active reservations can be cancelled.")

    @staticmethod
    def _validate_owner(user: User, reservation: Reservation) -> None:
        if reservation.student is not user:
            raise PermissionError("Users may only cancel their own reservations.")

    @staticmethod
    def _validate_before_start(reservation: Reservation, current_datetime: datetime) -> None:
        if current_datetime > reservation.start_datetime:
            raise ValueError("A reservation cannot be cancelled after its start time.")

    @staticmethod
    @abstractmethod
    def cancel(
        user: User,
        reservation: Reservation,
        current_datetime: datetime,
    ) -> None:
        pass


class StudentCancellation(CancellationPolicy):
    @staticmethod
    def cancel(user: User, reservation: Reservation, current_datetime: datetime) -> None:
        print("[Strategy] StudentCancellation applying two-hour rule")
        CancellationPolicy._validate_owner(user, reservation)
        CancellationPolicy._validate_active(reservation)
        CancellationPolicy._validate_before_start(reservation, current_datetime)
        
        system_config = SystemConfig.get_instance()
        cancel_window = system_config.student_cancel_window

        if reservation.start_datetime - current_datetime < cancel_window:
            print("[Strategy] Cancellation becomes NO_SHOW")
            reservation.status = ReservationStatus.NO_SHOW
            reservation.no_show_at = current_datetime
            return

        reservation.status = ReservationStatus.CANCELLED
        print("[Strategy] Cancellation recorded as CANCELLED")


class CaptainCancellation(CancellationPolicy):
    @staticmethod
    def cancel(user: User, reservation: Reservation, current_datetime: datetime) -> None:
        print("[Strategy] CaptainCancellation applying 24-hour rule")
        CancellationPolicy._validate_owner(user, reservation)
        CancellationPolicy._validate_active(reservation)
        CancellationPolicy._validate_before_start(reservation, current_datetime)
        
        system_config = SystemConfig.get_instance()
        cancel_window = system_config.captain_cancel_window

        if reservation.start_datetime - current_datetime < cancel_window:
            print("[Strategy] Cancellation becomes NO_SHOW")
            reservation.status = ReservationStatus.NO_SHOW
            reservation.no_show_at = current_datetime
            return

        reservation.status = ReservationStatus.CANCELLED
        print("[Strategy] Cancellation recorded as CANCELLED")


class AdminCancellation(CancellationPolicy):
    @staticmethod
    def cancel(user: User, reservation: Reservation, current_datetime: datetime) -> None:
        print("[Strategy] AdminCancellation bypassing user penalty")
        reservation.status = ReservationStatus.CANCELLED
