from enum import IntEnum


class ReservationStatus(IntEnum):
	ACTIVE = 0
	FINISHED = 1
	CANCELLED = 2
	NO_SHOW = 3
