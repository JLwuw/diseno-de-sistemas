from abc import ABC, abstractmethod


class PriorityRule(ABC):
    @abstractmethod
    def get_priority(self, reservation):
        raise NotImplementedError


class RegularPriorityRule(PriorityRule):
    def get_priority(self, reservation):
        return 1


class CaptainPriorityRule(PriorityRule):
    def get_priority(self, reservation):
        if reservation.requested_at.hour < 18:
            return 2
        return 1