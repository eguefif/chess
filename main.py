from classes import ChessBoard


chessboard = ChessBoard('test1', 'test2')

while True:
    chessboard.draw_game()
    move = input("Your move: ")
