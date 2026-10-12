from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from threading import RLock
from typing import Any, Optional

from admin import Admin, AdminBlock
from campus import (
    CampusEnum,
    NorthCampusFactory,
    SouthCampusFactory,
)
from court import Court, CourtStatus
from court_schedule import CourtSchedule
from recurring_reservation import RecurringReservation, RecurringReservationResult
from reservation import ForcedCancellationEvent, Reservation
from reservation_factory import ReservationFactory
from reservation_policy import ReservationDecision
from user import Captain, Student, User


class FacadeError(ValueError):
    pass


@dataclass(frozen=True)
class AuditEvent:
    action: str
    actor: User
    occurred_at: datetime
    reservation: Optional[Reservation] = None
    details: Optional[str] = None


class SportsComplexFacade:
    def __init__(self) -> None:
        self._lock = RLock()
        self.courts: list[Court] = []
        self.audit_events: list[AuditEvent] = []
        self._applied_blocks: dict[Court, list[tuple[date, AdminBlock]]] = {}

    def login(self, user: User, email: str, password: str) -> bool:
        return user.login(email, password)

    def logout(self, user: User) -> None:
        user.logout()

    def get_available_courts(
        self,
        user: User,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> tuple[Court, ...]:
        self._require_authenticated(user)
        return tuple(
            court
            for court in self.courts
            if self._is_court_available(court, start_datetime, end_datetime)
        )

    def reserve_court(
        self,
        user: Student,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
        requested_at: Optional[datetime] = None,
    ) -> Reservation:
        self._require_authenticated(user)
        requested_at = requested_at or datetime.now()

        with self._lock:
            self._validate_campus_hours(court, start_datetime, end_datetime)
            self._validate_not_blocked(court, start_datetime, end_datetime)
            decision = user.validate_reservation(
                court,
                start_datetime,
                end_datetime,
                requested_at,
            )
            self._require_approved(decision)

            for conflict in decision.reservations_to_force_cancel:
                event = conflict.force_cancel(
                    user,
                    requested_at,
                    reason="Higher-priority reservation",
                )
                self._record_forced_cancellation(event, user)

            reservation = ReservationFactory.create(
                user,
                court,
                start_datetime,
                end_datetime,
                requested_at,
            )
            court.add_reservation(reservation)
            self._record("reservation_created", user, requested_at, reservation)
            return reservation

    def cancel_reservation(
        self,
        user: Student,
        reservation: Reservation,
        current_datetime: Optional[datetime] = None,
    ) -> None:
        self._require_authenticated(user)
        if reservation.student is not user:
            raise PermissionError("Users may only cancel their own reservations.")

        current_datetime = current_datetime or datetime.now()
        with self._lock:
            reservation.cancel(user, current_datetime)
            action = (
                "reservation_no_show"
                if reservation.status.name == "NO_SHOW"
                else "reservation_cancelled"
            )
            self._record(action, user, current_datetime, reservation)

    def finish_reservation(
        self,
        user: Student,
        reservation: Reservation,
        current_datetime: Optional[datetime] = None,
    ) -> None:
        self._require_authenticated(user)
        if reservation.student is not user:
            raise PermissionError("Users may only finish their own reservations.")

        current_datetime = current_datetime or datetime.now()
        with self._lock:
            reservation.finish(current_datetime)
            self._record(
                "reservation_finished",
                user,
                current_datetime,
                reservation,
            )

    def force_cancel_reservation(
        self,
        admin: Admin,
        reservation: Reservation,
        reason: str = "Administrative cancellation",
        current_datetime: Optional[datetime] = None,
    ) -> ForcedCancellationEvent:
        self._require_admin(admin)
        current_datetime = current_datetime or datetime.now()
        with self._lock:
            event = reservation.force_cancel(admin, current_datetime, reason)
            self._record_forced_cancellation(event, admin)
            return event

    def view_upcoming_reservations(
        self,
        user: Student,
        current_datetime: Optional[datetime] = None,
    ) -> tuple[Reservation, ...]:
        self._require_authenticated(user)
        current_datetime = current_datetime or datetime.now()
        return tuple(
            reservation
            for reservation in user.reservations
            if reservation.is_active()
            and reservation.start_datetime >= current_datetime
        )

    def create_recurring_reservations(
        self,
        recurring: RecurringReservation,
        requested_at: Optional[datetime] = None,
    ) -> RecurringReservationResult:
        self._require_authenticated(recurring.captain)
        requested_at = requested_at or datetime.now()

        with self._lock:
            occurrences: list[tuple[datetime, datetime]] = []
            conflicting_weeks: list[int] = []
            for week in range(recurring.weeks_to_reserve):
                start_datetime = datetime.combine(
                    recurring.start_date + timedelta(days=7 * week),
                    recurring.start_time,
                )
                end_datetime = datetime.combine(
                    recurring.start_date + timedelta(days=7 * week),
                    recurring.end_time,
                )
                self._validate_campus_hours(
                    recurring.court,
                    start_datetime,
                    end_datetime,
                )
                self._validate_not_blocked(
                    recurring.court,
                    start_datetime,
                    end_datetime,
                )
                if recurring.court.has_conflict(start_datetime, end_datetime):
                    conflicting_weeks.append(week + 1)
                    continue
                if not recurring.court.is_available(start_datetime, end_datetime):
                    raise FacadeError(
                        "The recurring reservation has an unavailable occurrence."
                    )
                occurrences.append((start_datetime, end_datetime))

            if conflicting_weeks:
                return RecurringReservationResult((), tuple(conflicting_weeks))

            reservations = tuple(
                ReservationFactory.create(
                    recurring.captain,
                    recurring.court,
                    start_datetime,
                    end_datetime,
                    requested_at,
                )
                for start_datetime, end_datetime in occurrences
            )
            for reservation in reservations:
                recurring.court.add_reservation(reservation)
                self._record(
                    "recurring_reservation_created",
                    recurring.captain,
                    requested_at,
                    reservation,
                    details=(
                        f"equipment={recurring.equipment!r}; "
                        f"notes={recurring.notes!r}"
                    ),
                )
            return RecurringReservationResult(reservations, ())

    def create_court(
        self,
        admin: Admin,
        name: str,
        campus: CampusEnum,
        schedule: CourtSchedule,
        status: CourtStatus = CourtStatus.AVAILABLE,
    ) -> Court:
        self._require_admin(admin)
        court = Court(name, campus, schedule, status)
        admin.add_court(court)
        self.courts.append(court)
        self._record("court_created", admin, datetime.now(), details=name)
        return court

    def remove_court(self, admin: Admin, court: Court) -> None:
        self._require_managed_court(admin, court)
        with self._lock:
            if court.has_conflict(datetime.min, datetime.max):
                raise FacadeError("A court with active reservations cannot be removed.")
            admin.remove_court(court)
            self.courts.remove(court)
            self._record("court_removed", admin, datetime.now(), details=court.name)

    def update_court_status(
        self,
        admin: Admin,
        court: Court,
        status: CourtStatus,
    ) -> None:
        self._require_managed_court(admin, court)
        admin.update_court(court, status)
        self._record("court_status_updated", admin, datetime.now(), details=court.name)

    def update_court_schedule(
        self,
        admin: Admin,
        court: Court,
        schedule: CourtSchedule,
    ) -> None:
        self._require_managed_court(admin, court)
        admin.update_court_schedule(court, schedule)
        self._record("court_schedule_updated", admin, datetime.now(), details=court.name)

    def resolve_conflict(
        self,
        admin: Admin,
        reservations: list[Reservation],
        current_datetime: Optional[datetime] = None,
    ) -> Reservation:
        self._require_admin(admin)
        current_datetime = current_datetime or datetime.now()
        with self._lock:
            winner = admin.resolve_reservation_conflict(reservations)
            for reservation in reservations:
                if reservation is winner:
                    continue
                event = reservation.force_cancel(
                    admin,
                    current_datetime,
                    reason="Administrative conflict resolution",
                )
                self._record_forced_cancellation(event, admin)
            self._record(
                "conflict_resolved",
                admin,
                current_datetime,
                winner,
            )
            return winner

    def apply_block(
        self,
        admin: Admin,
        block: AdminBlock,
        court: Court,
        target_date: date,
    ) -> tuple[ForcedCancellationEvent, ...]:
        self._require_managed_court(admin, court)
        with self._lock:
            start_datetime = datetime.combine(target_date, block.start_time)
            end_datetime = datetime.combine(target_date, block.end_time)
            self._validate_campus_hours(court, start_datetime, end_datetime)
            events = admin.apply_block(block, court, target_date)
            self._applied_blocks.setdefault(court, []).append(
                (target_date, block.copy())
            )
            for event in events:
                self._record_forced_cancellation(event, admin)
            self._record(
                "block_applied",
                admin,
                datetime.now(),
                details=f"court={court.name}; date={target_date}",
            )
            return events

    def _is_court_available(
        self,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> bool:
        return (
            self._campus_hours_are_valid(court, start_datetime, end_datetime)
            and not self._is_blocked(court, start_datetime, end_datetime)
            and court.is_available(start_datetime, end_datetime)
        )

    def _campus_hours_are_valid(
        self,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> bool:
        validator = self._campus_factory(court).get_time_validator()
        return (
            validator.validate(start_datetime.time())
            and validator.validate(end_datetime.time())
        )

    def _validate_campus_hours(
        self,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> None:
        if not self._campus_hours_are_valid(court, start_datetime, end_datetime):
            raise FacadeError("The requested time is outside campus hours.")

    def _is_blocked(
        self,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> bool:
        for blocked_date, block in self._applied_blocks.get(court, []):
            block_start = datetime.combine(blocked_date, block.start_time)
            block_end = datetime.combine(blocked_date, block.end_time)
            if start_datetime < block_end and end_datetime > block_start:
                return True
        return False

    def _validate_not_blocked(
        self,
        court: Court,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> None:
        if self._is_blocked(court, start_datetime, end_datetime):
            raise FacadeError("The requested time is blocked by an administrator.")

    @staticmethod
    def _campus_factory(court: Court):
        factories = {
            CampusEnum.NORTH: NorthCampusFactory,
            CampusEnum.SOUTH: SouthCampusFactory,
        }
        return factories[court.campus]

    @staticmethod
    def _require_authenticated(user: User) -> None:
        if not user.logged_in:
            raise PermissionError("The user must be authenticated.")

    @staticmethod
    def _require_admin(admin: User) -> None:
        if not isinstance(admin, Admin) or not admin.logged_in:
            raise PermissionError("An authenticated administrator is required.")

    @staticmethod
    def _require_approved(decision: ReservationDecision) -> None:
        if not decision.approved:
            raise FacadeError(decision.reason or "Reservation was rejected.")

    @staticmethod
    def _require_managed_court(admin: Admin, court: Court) -> None:
        SportsComplexFacade._require_admin(admin)
        if court not in admin.courts:
            raise PermissionError("The administrator does not manage this court.")

    def _record(
        self,
        action: str,
        actor: User,
        occurred_at: datetime,
        reservation: Optional[Reservation] = None,
        details: Optional[str] = None,
    ) -> None:
        self.audit_events.append(
            AuditEvent(action, actor, occurred_at, reservation, details)
        )

    def _record_forced_cancellation(
        self,
        event: ForcedCancellationEvent,
        actor: User,
    ) -> None:
        self._record(
            "administrative_cancellation",
            actor,
            event.occurred_at,
            event.reservation,
            event.reason,
        )
        self._notify_forced_cancellation(event)

    def _notify_forced_cancellation(self, event: ForcedCancellationEvent) -> None:
        sender = self._campus_factory(event.reservation.court).get_notification_sender()
        sender.send_notification(
            event.reservation.student,
            f"Your reservation was cancelled: {event.reason}",
        )
