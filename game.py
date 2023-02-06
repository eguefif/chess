from classes import ChessBoard, Player
import random


class Game():
    def __init__(self) -> None:
        self.player1: Player
        self.player2: Player
        self.player1_name: str
        self.player2_name: str
        self.chessboard: ChessBoard

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
            self.chessboard.print_interface()
            self.chessboard.draw_game()
            self.chessboard.print_dead_pieces()

            while True:
                print(f"{self.chessboard.active_player.name}, it's your turn.")
                current_position = input("Piece to move:  ")
                target_position = input("To: ")
                if (self.chessboard.check_move_format(target_position) and
                    self.chessboard.check_move_format(current_position)):

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
