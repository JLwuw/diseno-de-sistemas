from genre_factory import GenreEnum, FantasyFactory, SciFiFactory
from character import Character, CharacterEnum
from attack import RegularAttack, StrongAttack
from game_config import GameConfig
import random
from time import sleep

class GameFacade:
    @staticmethod
    def select_genre() -> GenreEnum:
        print("\nEscoge un mundo:")
        print("1.) Fantasia")
        print("2.) Sci-Fi")

        while True: 
            try:
                menu_choice = int(input("Escoge una opcion [1-2]: ").strip())
            
            except ValueError:
                print(f"Input invalido. Introduce un numero entero")
                continue

            if int(menu_choice) == 1:
                return GenreEnum.FANTASY
            
            elif int(menu_choice) == 2:
                return GenreEnum.SCIFI

            else:
                print(f"Opcion invalida: {menu_choice}. Introduce un numero entero entre [1-2]")


    @staticmethod
    def create_characters(genre: GenreEnum) -> tuple[Character, Character]:
        config = GameConfig.get_instace()
        player_name = str(input("\nNombre de tu personaje: "))
        enemy_name = str(input("Nombre del enemigo: "))

        if genre == GenreEnum.FANTASY:
            factory = FantasyFactory()

        elif genre == GenreEnum.SCIFI:
            factory = SciFiFactory()

        else:
            raise ValueError(f"Unhandled genre: {genre}")

        player = factory.create_player(player_name)
        enemy = factory.create_enemy(enemy_name, config.difficulty)

        return player, enemy

    
    @staticmethod
    def player_turn(player: Character, enemy: Character) -> bool:

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
                print(f"Opcion invalida: {menu_choice}. Introduce un numero entero entre [1-2]")

        print(f"Golpeaste a {enemy.name}!")
        attack_strategy.attack(player, enemy)

        if enemy.hp <= 0:
            return True
        return False


    @staticmethod
    def enemy_turn(player: Character, enemy: Character) -> bool:
        print("\nTurno del enemigo!")
        attack_type = ""

        if random.random() < 0.2:
            attack_type = "fuerte"
            attack_strategy = StrongAttack()

        else:
            attack_type = "regular"
            attack_strategy = RegularAttack()

        print(f"{enemy.name} te ha atacado con un ataque {attack_type}!")
        attack_strategy.attack(enemy, player)

        if player.hp <= 0:
            return True
        return False


    @staticmethod
    def combat(player: Character, enemy: Character):
        turn_counter = 1
        config = GameConfig.get_instace()
        print("\nEmpieza el combate!")
        sleep(1)

        while True: 
            print(f"\nTurno {turn_counter}:")
            sleep(1)

            player_win = GameFacade.player_turn(player, enemy)
            sleep(1)
            if player_win:
                print("Has ganado!")
                return

            enemy_win = GameFacade.enemy_turn(player, enemy)
            sleep(1)
            if enemy_win:
                print("Has perdido...")
                return

            turn_counter += 1
            if turn_counter > config.max_turns:
                print("Cantidad maxima de turnos excedida.")
                return
