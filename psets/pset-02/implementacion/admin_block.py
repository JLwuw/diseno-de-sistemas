from __future__ import annotations

from datetime import time, date
from typing import Optional
from court import Court
from copy import deepcopy

class AdminBlock():
    def __init__(
            self, 
            start_time: time,
            end_time: time,
            motive: str, 
            equipment: Optional[list[str]],
        ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.motive = motive
        self.equipment = equipment


    def copy(self) -> AdminBlock:
        return deepcopy(self)

    def apply(self, court: Court, date: date):
        pass

    