from modules.game import Game

game = Game()

print("Welcome to chess")
while True:
    player1_name = input("What is the name of the first player: ")
    if game.check_player1_name(player1_name):
        break
while True:
    player2_name = input("What is the name of the second player: ")
    if game.check_player2_name(player2_name):
        break

game.set_game()
game.launch_game()
