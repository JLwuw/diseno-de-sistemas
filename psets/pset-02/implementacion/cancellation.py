from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reservation import Reservation


class CancellationPolicy(ABC):
    @abstractmethod
    @staticmethod
    def cancel(reservation: Reservation, current_datetime: datetime) -> None:
        pass

class StudentCancellation(CancellationPolicy):
    @staticmethod
    def cancel(reservation: Reservation, current_datetime: datetime) -> None:
        pass

class CaptainCancellation(CancellationPolicy):
    @staticmethod
    def cancel(reservation: Reservation, current_datetime: datetime) -> None:
        pass

class AdminCancellation(CancellationPolicy):
    @staticmethod
    def cancel(reservation: Reservation, current_datetime: datetime) -> None:
        pass