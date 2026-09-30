from character import (
    CharacterEnum,
    Character,
    Warrior,
    Dragon,
    Soldier,
    Alien
)

class CharacterFactory:
    @staticmethod
    def create(character_type: CharacterEnum, name: str, difficulty=None) -> Character:
        if character_type == CharacterEnum.WARRIOR:
            return Warrior(name, difficulty)
        
        elif character_type == CharacterEnum.DRAGON:
            return Dragon(name, difficulty)

        elif character_type == CharacterEnum.SOLDIER:
            return Soldier(name, difficulty)

        elif CharacterEnum.ALIEN:
            return Alien(name, difficulty)
        
        else:
            raise ValueError(f"Unhandled character type: {character_type}")
