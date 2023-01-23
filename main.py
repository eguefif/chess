from classes import ChessBoard, Player
import random

print("Welcome to chess")
player1_name = input("What is the name of the first player: ")
player2_name = input("What is the name of the second player: ")

if random.choice([1, 2]) == 1:
    player1 = Player(player1_name, "White")
    player2 = Player(player2_name, "Black")
else:
    player1 = Player(player1_name, "Black")
    player2 = Player(player2_name, "White")


chessboard = ChessBoard(player1, player2)

while True:
    chessboard.print_interface()
    chessboard.draw_game()
    chessboard.print_dead_pieces()
    
    while !True:
        print(f"{chessboard.active_player.name}, it's your turn.")
        current_position = input("Piece to move:  ")
        target_position = input("To: ")
        move_state = chessboard.move_piece(current_position, target_position)
        if move_state == "success" or "mate":
            break
    
    if move_state == "mate":
        break

print(f"The game is over. {chessboard.active_player.name} won.")


    
