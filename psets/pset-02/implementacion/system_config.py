from datetime import timedelta, time
from typing import Optional

class SystemConfig:
    _instance: Optional[SystemConfig] = None

    def __init__(self) -> None:
        self.max_recurring_reservation_weeks: int = 8
        self.min_recurring_reservation_weeks: int = 2
        self.captain_priority_end_time: time = time(hour=18)
        self.student_cancel_window: timedelta = timedelta(hours=2)
        self.captain_cancel_window: timedelta = timedelta(hours=24)
        self.noshow_monthly_limit: int = 3
        self.suspension_time = timedelta(days=7)

    @staticmethod
    def get_instance() -> SystemConfig:
        if SystemConfig._instance is None:
            SystemConfig._instance = SystemConfig()
        return SystemConfig._instance
