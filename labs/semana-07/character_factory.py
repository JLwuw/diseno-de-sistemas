from character import (
    CharacterEnum,
    Warrior,
    Dragon,
    Soldier,
    Alien
)

class CharacterFactory:
    @staticmethod
    def create(character_type: CharacterEnum, name: str):
        if character_type == CharacterEnum.WARRIOR:
            return Warrior(name)
        
        elif character_type == CharacterEnum.DRAGON:
            return Dragon(name)

        elif character_type == CharacterEnum.SOLDIER:
            return Soldier(name)

        elif CharacterEnum.ALIEN:
            return Alien(name)
        
        else:
            raise ValueError(f"Unhandled character type: {character_type}")
