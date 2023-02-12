import os
import platform
from chess.classes import Board


class TerminalGraphic():
    def __init__(self):
        self.board = Board()

    def print_interface(self, player1: str, player2: str) -> None:
        if platform.system == "windows":
            os.systen("cls")
        else:
            os.system("clear")

        print(""*4, "Chess game")
        print(f"white: {player1}")
        print(f"black: {player2}")

    def print_game(self, boardgame: list[list[str]]) -> None:
        for y, row in enumerate(boardgame):
            for x, cell in enumerate(row):
                if len(cell) < 1:
                    self.board.draw_empty_cell(x, y)
                    continue
                name = self._give_name(cell)
                if 'b' in cell:
                    self.board.draw_piece(x, y, name, 'black')
                else:
                    self.board.draw_piece(x, y, name, 'white')
        self.board.print()

    def _give_name(self, cell: str) -> str:
        return cell[0]

    def print_dead_pieces(
             self,
            white_pieces: list[str],
            black_pieces: list[str]
            ) -> None:
        print("Dead pieces:")
        print("White: ", end='')
        for piece in white_pieces:
            print(piece, end="")
        print()
        print("Black: ", end="")
        for piece in black_pieces:
            print(piece, end="")
        print()
