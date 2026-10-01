from abc import ABC, abstractmethod
from character import Character

class AttackStrategy(ABC):
    @staticmethod
    @abstractmethod
    def attack(attacker: Character, defender: Character):
        pass

class RegularAttack(AttackStrategy):
    @staticmethod
    def attack(attacker: Character, defender: Character):
        attack_stat = attacker.damage
        defender.take_damage(attack_stat) 

class StrongAttack(AttackStrategy):
    @staticmethod
    def attack(attacker: Character, defender: Character):
        attack_stat = attacker.damage
        damage = int(attack_stat * 1.5)
        defender.take_damage(damage) 