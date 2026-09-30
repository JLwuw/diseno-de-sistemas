from character_factory import CharacterFactory
from character import CharacterEnum
from abc import ABC, abstractmethod
from enum import Enum

class GenreEnum(Enum):
    FANTASY = 0
    SCIFI = 1


class GenreFactory(ABC):
    @abstractmethod
    def create_player(name):
        pass

    @abstractmethod
    def create_enemy(name):
        pass


class FantasyFactory:
    @staticmethod
    def create_player(name):
        return CharacterFactory.create(CharacterEnum.WARRIOR, name)

    @staticmethod
    def create_enemy(name):
        return CharacterFactory.create(CharacterEnum.DRAGON, name)


class SciFiFactory:
    @staticmethod
    def create_player(name):
        return CharacterFactory.create(CharacterEnum.SOLDIER, name)

    @staticmethod
    def create_enemy(name):
        return CharacterFactory.create(CharacterEnum.ALIEN, name)
