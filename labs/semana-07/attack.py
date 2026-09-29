from abc import ABC, abstractmethod

class AttackStrategy(ABC):
    @abstractmethod
    def attack(self):
        pass

class RegularAttack(AttackStrategy):
    def attack(self):
        pass

class StrongAttach(AttackStrategy):
    def attack(self):
        pass