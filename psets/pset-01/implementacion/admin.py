from user import User
class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.courts = []

    def add_court(self, court):
        self.courts.append(court)

    def remove_court(self, court):
        self.courts.remove(court)

    def update_court(self, court, status):
        if court not in self.courts:
            raise ValueError("The administrator does not manage this court.")
        court.status = status

    def create_reservation(self, reservation):
        reservation.court.add_reservation(reservation)
        return reservation

    def resolve_reservation_conflict(self, reservations):
        if not reservations:
            raise ValueError("At least one request is required.")
        return max(reservations, key=lambda reservation: reservation.priority())