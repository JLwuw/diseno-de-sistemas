from character import (
    CharacterEnum,
    Warrior,
    Dragon,
    Soldier,
    Alien
)

class CharacterFactory:
    def create(character_type: CharacterEnum, name):
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
