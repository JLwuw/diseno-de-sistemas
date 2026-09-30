from character_factory import CharacterFactory
from character import CharacterEnum, Character
from abc import ABC, abstractmethod
from enum import Enum

class GenreEnum(Enum):
    FANTASY = 0
    SCIFI = 1


class GenreFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_player(name, difficulty=None) -> Character:
        pass

    @staticmethod
    @abstractmethod
    def create_enemy(name, difficulty=None) -> Character:
        pass


class FantasyFactory(GenreFactory):
    @staticmethod
    def create_player(name, difficulty=None) -> Character:
        return CharacterFactory.create(CharacterEnum.WARRIOR, name, difficulty)

    @staticmethod
    def create_enemy(name, difficulty=None) -> Character:
        return CharacterFactory.create(CharacterEnum.DRAGON, name, difficulty)


class SciFiFactory(GenreFactory):
    @staticmethod
    def create_player(name, difficulty=None) -> Character:
        return CharacterFactory.create(CharacterEnum.SOLDIER, name, difficulty)

    @staticmethod
    def create_enemy(name, difficulty=None) -> Character:
        return CharacterFactory.create(CharacterEnum.ALIEN, name, difficulty)
