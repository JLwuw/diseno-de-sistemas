from abc import ABC, abstractmethod
from datetime import time

class TimeValidator(ABC):
    @abstractmethod
    @staticmethod
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
    @abstractmethod
    @staticmethod
    def send_notification(message: str) -> None:
        pass


class NorthCampusNotificationSender(NotificationSender):
    @staticmethod
    def send_notification(message: str) -> None:
        print("Email: " + message)


class SouthCampusNotificationSender(NotificationSender):
    @staticmethod
    def send_notification(message: str) -> None:
        print("Text Message: " + message)


class CampusFactory(ABC):
    @abstractmethod
    @staticmethod
    def get_time_validator() -> TimeValidator:
        pass

    @abstractmethod
    @staticmethod
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