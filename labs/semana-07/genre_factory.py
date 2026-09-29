from character_factory import CharacterFactory
from character import CharacterEnum



class FantasyFactory:
    def create(warrior_name, dragon_name):
        warrior = CharacterFactory.create(CharacterEnum.WARRIOR, warrior_name)
        dragon = CharacterFactory.create(CharacterEnum.DRAGON, dragon_name)
        return warrior, dragon


class SciFiFactory:
    def create(soldier_name, alien_name):
        soldier = CharacterFactory.create(CharacterEnum.SOLDIER, soldier_name)
        alien = CharacterFactory.create(CharacterEnum.ALIEN, alien_name)
        return soldier, alien
