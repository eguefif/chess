from chess.classes import ChessBoard, Player
from chess.terminal_graphic import TerminalGraphic
import random


class Game():
    def __init__(self) -> None:
        self.player1: Player
        self.player2: Player
        self.player1_name: str
        self.player2_name: str
        self.chessboard: ChessBoard
        self.graphic = TerminalGraphic()

    def check_player1_name(self, player1: str) -> bool:
        if len(player1) > 20:
            print("Player 1's name is too long.")
            return False
        if len(player1) == 0:
            print("Player 1's name is too short.")
            return False
        self.player1_name = player1
        return True

    def check_player2_name(self, player2: str) -> bool:
        if len(player2) == 0:
            print("Player 2's name is too short.")
            return False
        if len(player2) > 20:
            print("Player 2's name is too long.")
            return False
        self.player2_name = player2
        return True

    def set_game(self):
        if random.choice([1, 2]) == 1:
            self.player1 = Player(self.player1_name, "white")
            self.player2 = Player(self.player2_name, "black")
        else:
            self.player1 = Player(self.player1_name, "black")
            self.player2 = Player(self.player2_name, "white")
        self.chessboard = ChessBoard(self.player1, self.player2)

    def launch_game(self):
        while True:
            white_dead_pieces, black_dead_pieces = self.chessboard.get_dead_pieces()
            boardgame = self.chessboard.get_boardgame()
            player1, player2 = self.chessboard.get_players()
            self.graphic.print_interface(player1, player2)
            self.graphic.print_game(boardgame)
            self.graphic.print_dead_pieces(
                    white_dead_pieces,
                    black_dead_pieces)

            while True:
                print(
                    f"\n{self.chessboard.active_player.name}, "
                    "it's your turn.")
                current_position = input("Piece to move position :")
                while not self.chessboard.check_move_format(current_position):
                        current_position = input(
                            "Enter a valid position for piece to move:")
                target_position = input("Target position: ")
                while not self.chessboard.check_move_format(target_position):
                        target_position = input(
                            "Enter a valid position for target position:")

                x_current, y_current = self.chessboard.get_xy_position(
                            current_position)
                x_target, y_target = self.chessboard.get_xy_position(
                            target_position)
                move_state = self.chessboard.move_piece(
                            x_current,
                            y_current,
                            x_target,
                            y_target,
                            )
                if move_state in ["success", "mate", "check"]:
                    input("Push any key to refresh.")
                    break

            if move_state == "mate":
                break
        print(f"The game is over, {self.chessboard.active_player.name} won.")
