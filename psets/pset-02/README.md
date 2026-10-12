## Design Decisions

### Deep Copy in Prototype Pattern

We use `deepcopy`  because the block can contain data which other copies will change, especially the optional equipment list. Each  block must be independent from the reusable template: changing the equipment, motive, or other parts of one copy should only affect that copy, not the template or any other copy

### Singleton Configuration

`SystemConfig` is a Singleton so important parameters like the cancellation windows, priority times, recurring reservation limits, and no show limits have one source of truth. This avoids inconsistent configuration between policies and makes configuration access simple from all classes

The costs are it can create hidden dependencies, and make testint more difficult since one test can unintentionally affect the configuration a configuration from different tests

### Concurrency Strategy

The implementation uses a pessimistic approach. `SportsComplexFacade` acquires a lock before validating reservations, preventing any other thread from accessing the same critical sections at the same time. This prevents two simultaneous requests from both passing the availability check and reserving the same court

The tradeoff is that competing requests are processed one by one, depending on which one has the lock, reducing the amount of requests processed at the same time

## Design Patterns Table

| Design pattern used | Matching requirement | Problem it solves | Classes and methods involved |
|---|---|---|---|
| Factory | RF-01, RF-02 | Creates the correct reservation subtype without making callers depend on whether the user is a student or captain. | `ReservationFactory.create()`; `StudentReservation`; `CaptainReservation` |
| Abstract Factory | RF-17 | Provides campus-specific families of services, including opening-hour validation and notification delivery, without coupling the facade to a particular campus. | `CampusFactory.get_time_validator()`; `CampusFactory.get_notification_sender()`; `NorthCampusFactory`; `SouthCampusFactory`; `NorthCampusTimeValidator`; `SouthCampusTimeValidator`; `NorthCampusNotificationSender`; `SouthCampusNotificationSender` |
| Builder | RF-10, RF-11, RF-12 | Constructs recurring reservations with required values and optional equipment and concierge notes while validating the allowed number of weeks. | `RecurringReservationBuilder.__init__()`; `with_equipment()`; `with_notes()`; `build()`; `RecurringReservation` |
| Prototype | RF-13, RF-14 | Reuses an administrative block template by cloning it before applying the block to a court and date. | `AdminBlock.copy()`; `AdminBlock.apply_to()`; `Admin.apply_block()` |
| Singleton | RF-18 | Centralizes configurable values such as cancellation windows, priority cutoff, recurring-reservation limits, and no-show limits. | `SystemConfig._instance`; `SystemConfig.__init__()`; `SystemConfig.get_instance()` |
| Strategy: reservation creation | RF-01, RF-02, RF-03, RNF-07 | Encapsulates different reservation-approval rules for students and captains, including priority decisions and conflicting reservations. | `ReservationPolicy`; `StudentReservationPolicy.validate_reservation()`; `CaptainReservationPolicy.validate_reservation()`; `Student.reservation_policy`; `Captain.reservation_policy`; `Student.validate_reservation()`; `ReservationDecision` |
| Strategy: cancellation | RF-04, RF-05, RF-06, RF-09 | Encapsulates different cancellation windows and outcomes without putting student, captain, and administrative rules in `Reservation`. | `CancellationPolicy`; `StudentCancellation.cancel()`; `CaptainCancellation.cancel()`; `AdminCancellation.cancel()`; `Reservation.cancel()`; `Reservation.force_cancel()` |
| Facade | RF-01 through RF-18, RNF-03 through RNF-07 | Provides one coordinated entry point for authentication, reservations, recurring reservations, court management, blocks, cancellations, notifications, audit events, and concurrency control. | `SportsComplexFacade.login()`; `reserve_court()`; `cancel_reservation()`; `finish_reservation()`; `force_cancel_reservation()`; `create_recurring_reservations()`; `create_court()`; `remove_court()`; `update_court_status()`; `update_court_schedule()`; `resolve_conflict()`; `apply_block()`; `view_upcoming_reservations()` |
