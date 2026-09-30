from abc import ABC
from enum import Enum

class Character(ABC):
    def __init__(self, name: str, hp: int, damage: int):
        self.name = name
        self.hp = hp
        self.damage = damage

    def take_damage(self, damage: int):
        self.hp -= damage


class CharacterEnum(Enum):
    WARRIOR = 0
    DRAGON = 1
    SOLDIER = 2
    ALIEN = 3


class Warrior(Character):
    def __init__(self, name: str):
        hp = 20
        damage = 10
        super().__init__(name, hp, damage)


class Dragon(Character):
    def __init__(self, name: str):
        hp = 40
        damage = 30
        super().__init__(name, hp, damage)


class Soldier(Character):
    def __init__(self, name: str):
        hp = 15
        damage = 20
        super().__init__(name, hp, damage)


class Alien(Character):
    def __init__(self, name: str):
        hp = 25
        damage = 15
        super().__init__(name, hp, damage)