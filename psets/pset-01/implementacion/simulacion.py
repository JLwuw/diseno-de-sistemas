from datetime import datetime, timedelta

from admin import Admin
from court import Court, CourtStatus
from priority_rule import CaptainPriorityRule, RegularPriorityRule
from user import Captain, Student


def print_title(title):
	print(f"\n--- {title} ---")


def build_system():
	admin = Admin("mgomez@usfq.edu.ec", "admin123")
	student = Student(
		"alopez@estud.usfq.edu.ec", "ana123", "00330042",
		RegularPriorityRule(),
	)
	captain = Captain(
		"cperez@estud.usfq.edu.ec", "carlos123", "00330087",
		CaptainPriorityRule(),
	)
	basketball = Court("Basketball court 1")
	tennis = Court("Tennis court 1")
	admin.add_court(basketball)
	admin.add_court(tennis)
	return admin, student, captain, basketball, tennis


def show_upcoming_reservations(student, current_time):
	print_title("View upcoming reservations")
	upcoming = student.get_upcoming_reservations(current_time)
	for reservation in upcoming:
		print(f"Upcoming: {reservation}")
	if not upcoming:
		print(f"{student.email} has no upcoming reservations.")


def show_available_courts(admin, start_time, end_time):
	print_title("View available courts and times")
	available = [
		court
		for court in admin.courts
		if court.is_available(start_time, end_time)
	]
	print(
		f"Available from {start_time:%H:%M} to {end_time:%H:%M}: "
		+ ", ".join(court.name for court in available)
	)


def create_reservation_flow(admin, student, captain, court, now):
	print_title("Create reservation")
	start_time = now + timedelta(days=1)
	end_time = start_time + timedelta(hours=1)
	student_request = student.request_reservation(
		court, start_time, end_time, now
	)
	captain_request = captain.request_reservation(
		court, start_time, end_time, now
	)
	winner = admin.resolve_reservation_conflict(
		[student_request, captain_request]
	)
	print(
		f"Student priority: {student_request.priority()} | "
		f"Captain priority: {captain_request.priority()}"
	)
	reservation = admin.create_reservation(winner)
	print(f"Reservation created for {reservation.student.email}: {reservation}")
	return reservation


def cancellation_flow(admin, student, court, now):
	print_title("Cancel reservation")
	normal_start = now + timedelta(hours=4)
	normal_request = student.request_reservation(
		court, normal_start, normal_start + timedelta(hours=1), now
	)
	normal_reservation = admin.create_reservation(normal_request)
	student.cancel_reservation(normal_reservation, now)
	print(f"Four hours before start: {normal_reservation.status.value}")

	late_start = now + timedelta(hours=1)
	late_request = student.request_reservation(
		court, late_start, late_start + timedelta(hours=1), now
	)
	late_reservation = admin.create_reservation(late_request)
	student.cancel_reservation(late_reservation, now)
	print(f"One hour before start: {late_reservation.status.value}")


def completion_flow(admin, student, court, now):
	print_title("Complete reservation")
	start_time = now + timedelta(hours=2)
	reservation = admin.create_reservation(
		student.request_reservation(
			court, start_time, start_time + timedelta(hours=1), now
		)
	)
	reservation.finish(start_time + timedelta(hours=1))
	print(f"Reservation completed normally: {reservation.status.value}")


def administration_flow(admin, court):
	print_title("Manage courts")
	print(f"Managed court: {court}")
	admin.update_court(court, CourtStatus.MAINTENANCE)
	print(f"Court status updated: {court}")
	admin.update_court(court, CourtStatus.AVAILABLE)
	print(f"Court status restored: {court}")


def conflict_flow(admin, student, captain, court, now):
	print_title("Resolve reservation conflict")
	start_time = now + timedelta(days=2)
	end_time = start_time + timedelta(hours=1)
	requests = [
		student.request_reservation(court, start_time, end_time, now),
		captain.request_reservation(court, start_time, end_time, now),
	]
	winner = admin.resolve_reservation_conflict(requests)
	print(
		f"Conflict between {student.email} and {captain.email}. "
		f"Winner: {winner.student.email} "
		f"(priority {winner.priority()})."
	)


def main():
	admin, student, captain, basketball, tennis = build_system()
	now = datetime(2026, 9, 6, 17, 0)
	login_successfully = student.login(
		"alopez@estud.usfq.edu.ec", "ana123"
	)
	print(f"Student login successful: {login_successfully}")

	reservation = create_reservation_flow(
		admin, student, captain, basketball, now
	)
	show_upcoming_reservations(reservation.student, now)
	show_available_courts(
		admin, now + timedelta(days=3), now + timedelta(days=3, hours=1)
	)
	cancellation_flow(admin, student, tennis, now)
	completion_flow(admin, student, tennis, now)
	administration_flow(admin, tennis)
	conflict_flow(admin, student, captain, basketball, now)


if __name__ == "__main__":
	main()
