from __future__ import annotations

from datetime import date, datetime, time
from threading import Barrier, Lock, Thread

from admin import Admin, AdminBlock
from campus import (
	CampusEnum,
	NorthCampusFactory,
	SouthCampusFactory,
)
from court import CourtStatus
from court_schedule import CourtSchedule, Weekday
from recurring_reservation import RecurringReservationBuilder
from sports_complex_facade import FacadeError, SportsComplexFacade
from user import Captain, Student


REQUESTED_AT = datetime(2026, 10, 10, 12)


def build_schedule(opening_time: time, closing_time: time) -> CourtSchedule:
	schedule = CourtSchedule()
	for weekday in Weekday:
		schedule.add_bracket(weekday, opening_time, closing_time)
	return schedule


def login(facade: SportsComplexFacade, user: Student | Admin) -> None:
	if not facade.login(user, user.email, user._password):
		raise RuntimeError(f"Could not authenticate {user.email}")


def print_campus_notification(user: Student, campus: CampusEnum) -> None:
	factory = (
		NorthCampusFactory
		if campus is CampusEnum.NORTH
		else SouthCampusFactory
	)
	factory.get_notification_sender().send_notification(
		user,
		f"Reservation created for {campus.name} campus.",
	)


def main() -> None:
	facade = SportsComplexFacade()
	admin = Admin("admin@university.edu", "admin-password", "555-0000")
	login(facade, admin)

	north_schedule = build_schedule(time(6), time(22))
	south_schedule = build_schedule(time(7), time(23))
	north_court = facade.create_court(
		admin,
		"North Court 1",
		CampusEnum.NORTH,
		north_schedule,
		CourtStatus.AVAILABLE,
	)
	south_court = facade.create_court(
		admin,
		"South Court 1",
		CampusEnum.SOUTH,
		south_schedule,
		CourtStatus.AVAILABLE,
	)

	print("\n1. Reservation in each campus")
	north_student = Student(
		"north.student@university.edu", "password", "555-0001", "N-001", CampusEnum.NORTH
	)
	south_student = Student(
		"south.student@university.edu", "password", "555-0002", "S-001", CampusEnum.SOUTH
	)
	login(facade, north_student)
	login(facade, south_student)
	north_reservation = facade.reserve_court(
		north_student, north_court, datetime(2026, 10, 12, 8),
		datetime(2026, 10, 12, 9), REQUESTED_AT,
	)
	south_reservation = facade.reserve_court(
		south_student, south_court, datetime(2026, 10, 12, 9),
		datetime(2026, 10, 12, 10), REQUESTED_AT,
	)
	print(f"North reservation: {north_reservation.status.name}")
	print(f"South reservation: {south_reservation.status.name}")
	print_campus_notification(north_student, CampusEnum.NORTH)
	print_campus_notification(south_student, CampusEnum.SOUTH)

	print("\n2. Reservation rejected outside campus hours")
	try:
		facade.reserve_court(
			north_student, south_court, datetime(2026, 10, 12, 6),
			datetime(2026, 10, 12, 7), REQUESTED_AT,
		)
	except FacadeError as error:
		print(f"Reservation rejected: {error}")

	print("\n3. Recurring reservations")
	captain = Captain(
		"captain@university.edu", "password", "555-0003", "C-001", CampusEnum.NORTH
	)
	login(facade, captain)
	successful_recurring = RecurringReservationBuilder(
		captain, north_court, date(2026, 10, 12), time(10), time(11), 2
	).with_equipment(["ball"]).with_notes("Leave equipment at concierge").build()
	successful_result = facade.create_recurring_reservations(
		successful_recurring, REQUESTED_AT
	)
	print(f"Successful occurrences: {len(successful_result.reservations)}")

	conflict_student = Student(
		"conflict.student@university.edu", "password", "555-0004", "S-002", CampusEnum.NORTH
	)
	login(facade, conflict_student)
	facade.reserve_court(
		conflict_student, north_court, datetime(2026, 10, 19, 12),
		datetime(2026, 10, 19, 13), REQUESTED_AT,
	)
	failed_recurring = RecurringReservationBuilder(
		captain, north_court, date(2026, 10, 12), time(12), time(13), 3
	).build()
	failed_result = facade.create_recurring_reservations(
		failed_recurring, REQUESTED_AT
	)
	print(f"Conflicting weeks: {failed_result.conflicting_weeks}")

	print("\n4. Cancellation strategies")
	on_time = facade.reserve_court(
		north_student, north_court, datetime(2026, 10, 12, 14),
		datetime(2026, 10, 12, 15), REQUESTED_AT,
	)
	facade.cancel_reservation(north_student, on_time, datetime(2026, 10, 12, 11))
	print(f"Student on-time cancellation: {on_time.status.name}")

	captain_late = facade.reserve_court(
		captain, north_court, datetime(2026, 10, 12, 16),
		datetime(2026, 10, 12, 17), REQUESTED_AT,
	)
	facade.cancel_reservation(captain, captain_late, datetime(2026, 10, 12, 15))
	print(f"Captain late cancellation: {captain_late.status.name}")

	forced = facade.reserve_court(
		north_student, north_court, datetime(2026, 10, 12, 18),
		datetime(2026, 10, 12, 19), REQUESTED_AT,
	)
	facade.force_cancel_reservation(
		admin, forced, "Administrative test cancellation", datetime(2026, 10, 12, 12)
	)
	print(f"Forced admin cancellation: {forced.status.name}")

	print("\n5. Monthly no-show limit")
	limited_student = Student(
		"limited.student@university.edu", "password", "555-0005", "S-003", CampusEnum.NORTH
	)
	login(facade, limited_student)
	for day in (13, 14, 15):
		reservation = facade.reserve_court(
			limited_student, north_court, datetime(2026, 10, day, 8),
			datetime(2026, 10, day, 9), REQUESTED_AT,
		)
		facade.cancel_reservation(
			limited_student, reservation, datetime(2026, 10, day, 7, 30)
		)
	print(f"No-shows this month: {limited_student.no_shows_since(datetime(2026, 10, 1))}")
	try:
		facade.reserve_court(
			limited_student, north_court, datetime(2026, 10, 16, 8),
			datetime(2026, 10, 16, 9), REQUESTED_AT,
		)
	except FacadeError as error:
		print(f"Fourth reservation rejected: {error}")

	print("\n6. Cloned administrative block")
	block_court = facade.create_court(
		admin, "North Court 2", CampusEnum.NORTH,
		build_schedule(time(6), time(22)), CourtStatus.AVAILABLE,
	)
	existing = facade.reserve_court(
		north_student, block_court, datetime(2026, 10, 20, 14),
		datetime(2026, 10, 20, 15), REQUESTED_AT,
	)
	block = AdminBlock(time(14), time(15), "Maintenance", ["net"])
	first_events = facade.apply_block(admin, block, block_court, date(2026, 10, 20))
	second_events = facade.apply_block(
		admin, block.copy(), north_court, date(2026, 10, 20)
	)
	print(f"Pre-existing reservation after block: {existing.status.name}")
	print(f"Cancellation events on first court: {len(first_events)}")
	print(f"Events on cloned block's second court: {len(second_events)}")

	print("\n7. Concurrent reservation attempts")
	concurrent_court = facade.create_court(
		admin, "North Court 3", CampusEnum.NORTH,
		build_schedule(time(6), time(22)), CourtStatus.AVAILABLE,
	)
	first_captain = Captain(
		"captain.one@university.edu", "password", "555-0006", "C-002", CampusEnum.NORTH
	)
	second_captain = Captain(
		"captain.two@university.edu", "password", "555-0007", "C-003", CampusEnum.NORTH
	)
	login(facade, first_captain)
	login(facade, second_captain)
	barrier = Barrier(2)
	result_lock = Lock()
	results: list[tuple[str, str]] = []

	def attempt_reservation(captain_user: Captain) -> None:
		barrier.wait()
		try:
			facade.reserve_court(
				captain_user, concurrent_court, datetime(2026, 10, 21, 11),
				datetime(2026, 10, 21, 12), datetime(2026, 10, 21, 10),
			)
			result = (captain_user.email, "approved")
		except FacadeError as error:
			result = (captain_user.email, f"rejected: {error}")
		with result_lock:
			results.append(result)

	threads = [
		Thread(target=attempt_reservation, args=(first_captain,)),
		Thread(target=attempt_reservation, args=(second_captain,)),
	]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	for result in sorted(results):
		print(f"{result[0]}: {result[1]}")
	print(f"Successful reservations: {len(concurrent_court.reservations)}")


if __name__ == "__main__":
	main()