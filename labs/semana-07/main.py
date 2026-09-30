from genre_factory import *
from game_facade import GameFacade

def main():
    print("Bienvenido al juego! Escoge un mundo:")
    print("1.) Fantasia")
    print("2.) Sci-Fi")

    while True: 
        menu_choice = int(input("Escoge una opcion [1, 2]: "))

        if int(menu_choice) == 1:
            break
        
        elif int(menu_choice) == 2:
            break

        else:
            print(f"Invalid input: {menu_choice}")




main()