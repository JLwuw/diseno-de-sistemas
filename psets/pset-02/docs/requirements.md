RF-05 and 06 where modified

RF-07 through 18 and NFR-06 through 07 are new

## Functional Requirements

### Standard Reservations

- **RF-01:** The system must allow a student to reserve an available sports court for an individual or informal activity.
- **RF-02:** The system must allow an official team captain to reserve a sports court.
- **RF-03:** The system must give official team captains priority when reserving courts before 6:00 PM.

### Cancellation and Reservation Outcomes

- **RF-04:** The system must allow users to cancel their own reservation.
- **RF-05:** If a regular student cancels a reservation less than 2 hours before its start time, the system must record the action as a no-show.
- **RF-06:** If an official team captain cancels a reservation less than 24 hours before its start time, the system must record the action as a no-show

### Court and Conflict Administration

- **RF-07:** The system must allow Sports Complex administrators to create, remove, and manage available courts.
- **RF-08:** The system must allow Sports Complex administrators to resolve conflicts between reservations.
- **RF-09:** If a Sports Complex administrator forcefully cancels a reservation, the system must not apply any consequence to the user who created the reservation.

### Recurring Reservations

- **RF-10:** The system must allow official team captains to create recurring reservations for the same court, day, and time for up to 8 weeks at a time.
- **RF-11:** A recurring reservation may include requests for specific equipment, such as balls or nets, and additional notes for the concierge.
- **RF-12:** If any occurrence of a recurring reservation is unavailable, the system must reject the entire recurring reservation.

### Administrative Blocks

- **RF-13:** The system must allow Sports Complex administrators to create reusable blocking templates containing a time, motive, and optional equipment.
- **RF-14:** The system must allow an administrator to apply a blocking template to any court and time.
- **RF-15:** Applying a block must override any preexisting reservation for the selected court and time.
- **RF-16:** If a block overrides an existing reservation, the system must notify the reservation creator.

### Campuses and Configuration

- **RF-17:** The system must manage reservations across different campuses, each of which may have different available times and notification systems.
- **RF-18:** The system must store configurable system values, including the priority-reservation window and cancellation window, in a single centralized configuration location.

## Non-Functional Requirements

### Performance and Availability

- **RNF-01:** Under normal operating conditions, the system should respond to court-availability, reservation, and cancellation requests within two seconds.
- **RNF-02:** The system should be available at least 99% of the time during the university's normal operating hours.

### Authentication and Authorization

- **RNF-03:** The system must authenticate users using their university credentials.
- **RNF-04:** Students may view and cancel only their own reservations. Sports Complex administrators may manage courts and resolve reservation conflicts.

### Auditability

- **RNF-05:** The system must record reservation creation, cancellation, no-show, completion, and administrative conflict-resolution events, including the responsible user and timestamp.
- 
### Consistency and Concurrency

- **RNF-06:** The system must prevent two users from successfully reserving the same court for overlapping time periods, including when requests are submitted concurrently.
- **RNF-07:** When two overlapping reservations arrive simultaneously, the system must prioritize official team captains over students. If users have the same priority, it must favor the user with fewer no-shows. If they are still tied, it must favor the user with fewer recent reservations. If they remain tied, the system must use the server-side request sequence; if the requests are indistinguishable, it may use an auditable random selection.


