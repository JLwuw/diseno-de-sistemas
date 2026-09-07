class User:
    def __init__(self, email, password):
        self.email = email
        self._password = password
        self.logged_in = False

    def login(self, email, password):
        self.logged_in = (
            email == self.email
            and password == self._password
        )
        return self.logged_in

    def logout(self):
        self.logged_in = False


class Student(User):
    def __init__(self, email, password, student_code, priority_rule):
        super().__init__(email, password)
        self.student_code = student_code
        self.priority_rule = priority_rule
        self.reservations = []

    def request_reservation(self, court, start_time, end_time, requested_at):
        from reservation import Reservation

        return Reservation(
            self, court, start_time, end_time, requested_at
        )

    def add_reservation(self, reservation):
        self.reservations.append(reservation)

    def get_upcoming_reservations(self, current_time):
        from reservation import ReservationStatus

        return [
            reservation
            for reservation in self.reservations
            if reservation.status is ReservationStatus.ACTIVE
            and reservation.start_time >= current_time
        ]

    def cancel_reservation(self, reservation, current_time):
        if reservation.student is not self:
            raise ValueError("A student can cancel only their own reservation.")
        reservation.cancel(current_time)


class Captain(Student):
    pass