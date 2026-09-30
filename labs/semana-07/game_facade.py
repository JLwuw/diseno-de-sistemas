from genre_factory import GenreEnum, FantasyFactory, SciFiFactory
from character import Character, CharacterEnum
from attack import RegularAttack, StrongAttack

class GameFacade:
    @staticmethod
    def create_characters(genre: GenreEnum):
        player_name = str(input("Nombre de tu personaje: "))
        enemy_name = str(input("Nombre del enemigo: "))

        if genre == GenreEnum.FANTASY:
            factory = FantasyFactory()

        elif genre == GenreEnum.SCIFI:
            factory = SciFiFactory()

        else:
            raise ValueError(f"Unhandled genre: {genre}")

        player = factory.create_player(player_name)
        enemy = factory.create_enemy(enemy_name)

        return player, enemy

    
    @staticmethod
    def player_turn(player: Character, enemy: Character):

        while True:
            print("Es tu turno! Escoge una estrategia de ataque:")
            print("1.) Ataque regular")
            print("2.) Ataque fuerte")

            try:
                menu_choice = int(input("Escoge una opcion [1-2]: ").strip())
            
            except ValueError:
                print(f"Input invalido. Introduce un numero entero")
                continue
    
            if menu_choice == 1:
                attack_strategy = RegularAttack()
                break

            elif menu_choice == 2:
                attack_strategy = StrongAttack()
                break

            else:
                print(f"Opcion invalida: {menu_choice}. Introduce un numero entre [1-2]")

        



        