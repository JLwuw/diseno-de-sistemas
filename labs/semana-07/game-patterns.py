from game_facade import GameFacade

def main():
    print("Bienvenido al juego!")
    genre = GameFacade.select_genre()
    player, enemy = GameFacade.create_characters(genre)
    GameFacade.combat(player, enemy)

main()