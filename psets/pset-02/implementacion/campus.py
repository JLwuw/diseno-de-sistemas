from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import time
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User

class CampusEnum(IntEnum):
    NORTH = 0
    SOUTH = 1


class TimeValidator(ABC):
    @staticmethod
    @abstractmethod
    def validate(time: time) -> bool:
        pass


class NorthCampusTimeValidator(TimeValidator):
    opening_time: time = time(hour=6)
    closing_time: time = time(hour=22)

    @staticmethod
    def validate(time: time) -> bool:
        opening_time = NorthCampusTimeValidator.opening_time
        closing_time = NorthCampusTimeValidator.closing_time

        return  opening_time <= time <= closing_time


class SouthCampusTimeValidator(TimeValidator):
    opening_time: time = time(hour=7)
    closing_time: time = time(hour=23)

    @staticmethod
    def validate(time: time):
        opening_time = SouthCampusTimeValidator.opening_time
        closing_time = SouthCampusTimeValidator.closing_time

        return  opening_time <= time <= closing_time


class NotificationSender(ABC):
    @staticmethod
    @abstractmethod
    def send_notification(user: User, message: str) -> None:
        pass


class NorthCampusNotificationSender(NotificationSender):
    @staticmethod
    def send_notification(user: User, message: str) -> None:
        print("Email: " + user.email)
        print("Message: " + message)


class SouthCampusNotificationSender(NotificationSender):
    @staticmethod
    def send_notification(user: User, message: str) -> None:
        print("Text Message: " + user.phone_number)
        print("Message: " + message)


class CampusFactory(ABC):
    @staticmethod
    @abstractmethod
    def get_time_validator() -> TimeValidator:
        pass

    @staticmethod
    @abstractmethod
    def get_notification_sender() -> NotificationSender:
        pass


class NorthCampusFactory(CampusFactory):
    @staticmethod
    def get_time_validator() -> TimeValidator:
        return NorthCampusTimeValidator()

    @staticmethod
    def get_notification_sender() -> NotificationSender:
        return NorthCampusNotificationSender()


class SouthCampusFactory(CampusFactory):
    @staticmethod
    def get_time_validator() -> TimeValidator:
        return SouthCampusTimeValidator()

    @staticmethod
    def get_notification_sender() -> NotificationSender:
        return SouthCampusNotificationSender()