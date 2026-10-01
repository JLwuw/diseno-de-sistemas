from abc import ABC
from enum import Enum

class Character(ABC):
    def __init__(self, name: str, hp: int, damage: int, difficulty=None):
        self.name = name
        self.hp = hp
        self.damage = damage

        if difficulty:
            self.hp *= difficulty
            self.damage *= difficulty

    def take_damage(self, damage: int):
        self.hp -= damage
        self.hp = max(self.hp, 0)
        print(f"{self.name} toma {damage} daño! Le queda {self.hp} de vida")


class CharacterEnum(Enum):
    WARRIOR = 0
    DRAGON = 1
    SOLDIER = 2
    ALIEN = 3


class Warrior(Character):
    def __init__(self, name: str, difficulty=None):
        hp = 30
        damage = 10
        super().__init__(name, hp, damage, difficulty)


class Dragon(Character):
    def __init__(self, name: str, difficulty=None):
        hp = 40
        damage = 5
        super().__init__(name, hp, damage, difficulty)


class Soldier(Character):
    def __init__(self, name: str, difficulty=None):
        hp = 30
        damage = 9
        super().__init__(name, hp, damage, difficulty)


class Alien(Character):
    def __init__(self, name: str, difficulty=None):
        hp = 25
        damage = 5
        super().__init__(name, hp, damage, difficulty)