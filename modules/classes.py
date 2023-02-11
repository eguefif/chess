from termcolor import colored
import string


class ChessBoard:
    def __init__(self, player1: "Player", player2: "Player") -> None:
        self.player1 = player1
        self.player2 = player2
        self.white_set = Set("white")
        self.black_set = Set("black")
        self.board = Board()
        if self.player1.color == "white":
            self.active_player = self.player1
        else:
            self.active_player = self.player2
        self.active_set = self.white_set
        self.non_active_set = self.black_set

    def set_active_set(self) -> None:
        if self.active_player.color == "white":
            self.active_set = self.white_set
            self.non_active_set = self.black_set
            return
        self.active_set = self.black_set
        self.non_active_set = self.white_set

    def check_move_format(self, move: str) -> str:
        letters = string.ascii_lowercase[:8] + string.ascii_uppercase[:8]
        try:
            if len(move) != 2:
                return
        except TypeError:
            print("Wrong position format.")
            return
        if move[0] in letters:
            y = move[0]
            x = move[1]
        else:
            y = move[1]
            x = move[0]
        try:
            if int(x) not in range(1, 9):
                return False
        except ValueError:
            print("Wrong position format")
            return
        if y not in letters:
            print("You need a letter from a to h.")
            return
        return f'{y}{x}'

    def get_board_with_pieces(self) -> list:
        """This function return a 8*8 list with all the position marked with
            -0 if empty
            -1 for ally pieces
            -2 for foes
        """
        board = [[0 for a in range(8)] for a in range(8)]
        for subset in self.active_set.set:
            for piece in subset:
                board[piece.x-1][piece.y-1] = 1

        for subset in self.non_active_set.set:
            for piece in subset:
                board[piece.x-1][piece.y-1] = 2
        return board

    def move_piece(self,
                   x_current: int,
                   y_current: int,
                   x_target: int,
                   y_target: int,
                   ) -> str:
        self.set_active_set()

        piece = self.get_piece_if_alive(x_current, y_current)
        if piece is None:
            print("There is no piece.")
            return 'failed'

        if self.active_player.check is True:
            if piece.p != "Z":
                print("Your king is in check, move it.")
                return 'failed'

        board = self.get_board_with_pieces()
        move_state = piece.is_move_possible(x_target, y_target, board)
        if move_state not in ["castling", "success"]:
            print("This move is not authorized")
            return 'failed'

        if move_state == 'castling':
            self.castling(x_current, y_current, x_target, y_target)
            return "success"

        if self.is_target_ally(x_target, y_target):
            print("This move is not authorized.")
            return 'failed'

        kill = self.check_for_kill(x_target, y_target)

        if isinstance(kill, Piece):
            if kill.name == "z":
                if kill.is_check_mate():
                    return "mate"
                else:
                    self.get_non_active_player().check = True
                    self.switch_active_player()
                    return "check"
            self.non_active_set.kill_piece(x_target, y_target)

        self.active_set.move_piece(x_current, y_current, x_target, y_target)
        self.switch_active_player()
        return "success"

    def castling(self, x: int, y: int, x_target: int, y_target: int) -> None:
        self.active_set.move_piece(x, y, x_target, y_target)
        if x_target == 7:
            self.active_set.move_piece(x_target+1, y_target, 6, y)
        else:
            self.active_set.move_piece(x_target-2, y_target, 4, y)

    def is_target_ally(self, x: int, y: int) -> bool:
        board = self.get_board_with_pieces()
        if board[x-1][y-1] == 1:
            return 1
        return 0

    def get_non_active_player(self) -> "Player":
        return self.active_player

    def switch_active_player(self) -> None:
        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def get_piece_if_alive(self, x: int, y: int) -> "Piece":
        piece = self.get_piece_by_position(x, y)
        if piece:
            if piece.alive == 0:
                return None
            return piece

    def get_xy_position(self, position: str) -> (int, int):
        position = self.check_move_format(position)
        if position is None:
            return
        letter_position = {'a': 1,
                           'b': 2,
                           'c': 3,
                           'd': 4,
                           'e': 5,
                           'f': 6,
                           'g': 7,
                           'h': 8,
                           }
        x_position = letter_position.get(position[0])
        return (x_position, int(position[1]))

    def check_for_kill(self, x: int, y: int) -> "Piece":
        for subset in self.non_active_set.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    return piece

        for subset in self.active_set.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    return piece

    def get_boardgame(self):
        boardgame = [['' for i in range(8)] for _ in range(8)]
        for subset in self.white_set.set:
            for piece in subset:
                x, y = piece.get_position_for_board()
                if piece.alive == 0:
                    break
                boardgame[y][x] = piece.name + 'a'
        for subset in self.black_set.set:
            for piece in subset:
                x, y = piece.get_position_for_board()
                if piece.alive == 0:
                    break
                boardgame[y][x] = piece.name + 'b'
        return boardgame

    def get_players(self) -> (str, str):
        return self.give_white_player_name(), self.give_black_player_name()

    def get_dead_pieces(self) -> (list, list):
        white_dead_pieces = self.white_set.return_dead_pieces()
        black_dead_pieces = self.black_set.return_dead_pieces()
        return white_dead_pieces, black_dead_pieces

    def give_white_player_name(self) -> str:
        if self.player1.color == "white":
            return self.player1.name
        return self.player2.name

    def give_black_player_name(self) -> str:
        if self.player1.color == "white":
            return self.player2.name
        return self.player1.name

    def get_piece_by_position(self, x, y):
        for subset in self.white_set.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    return piece
        for subset in self.black_set.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    return piece


class Set():
    def __init__(self, color) -> None:
        self.paws = [Pawn(color, a) for a in range(1, 9)]
        self.rooks = [Rook(color, a) for a in range(2)]
        self.bishops = [Bishop(color, a) for a in range(2)]
        self.knights = [Knight(color, a) for a in range(2)]
        self.queen = [Queen(color)]
        self.king = [King(color)]
        self.set = [self.paws,
                    self.rooks,
                    self.bishops,
                    self.knights,
                    self.queen,
                    self.king,
                    ]

    def move_piece(self, x, y, x_target, y_target):
        for subset in self.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    piece.move(x_target, y_target)

    def kill_piece(self, x: int, y: int) -> None:
        for subset in self.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    piece.alive = 0
                    piece.move(-1, -1)

    def return_dead_pieces(self) -> list:
        dead_pieces = [piece.name for subset in self.set
                       for piece in subset if piece.alive == 0]
        return dead_pieces

    def draw_pieces(self, board: "Board") -> None:
        for pieces in self.set:
            for piece in pieces:
                if piece.alive == 0:
                    break
                piece.draw(board)


class Piece:
    x: int
    y: int
    name: str

    def check_board(self, x: int, y: int, board: [int, int]) -> int:
        return board[x-1][y-1]

    def __init__(self, color: str) -> None:
        self.color = color
        self.alive = 1

    def get_position_for_board(self):
        return self.x-1, self.y-1

    def is_move_possible(self, x: int, y: int) -> bool:
        pass

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Player:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.check = False


class Pawn(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.name = 'p'
        self.x = position
        self.first_move = 1
        if color == "black":
            self.y = 7
        else:
            self.y = 2

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        possible_move = []
        if self.color == 'black':
            y_direction = -1
        else:
            y_direction = 1
        if self.y+y_direction*1 in range(9):
            if super().check_board(x, y, board) == 0:
                possible_move.append((self.x, self.y+y_direction*1))
        if self.y+y_direction*2 in range(9) and self.first_move == 1:
            if super().check_board(x, y, board) == 0:
                self.first_move = 0
                possible_move.append((self.x, self.y+y_direction*2))
        if self.x+1 in range(9) and self.y+y_direction*1 in range(9):
            if super().check_board(x, y, board) == 2:
                possible_move.append((self.x+1, self.y+y_direction*1))
        if self.x-1 in range(9) and self.y+y_direction*1 in range(9):
            if super().check_board(x, y, board) == 2:
                possible_move.append((self.x-1, self.y+y_direction*1))

        if (x, y) in possible_move:
            self.first_move = 0
            return "success"
        return "failed"


class Rook(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.name = 'R'
        if position == 0:
            self.x = 1
        else:
            self.x = 8
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        if x - self.x == 0:
            if y > self.y:
                for y_check in range(self.y+1, y):
                    if super().check_board(x, y_check, board) != 0:
                        return False
            if y < self.y:
                for y_check in range(self.y-1, y, -1):
                    if super().check_board(x, y_check, board) != 0:
                        print(x, y_check, board[x][y_check])
                        return False

        if y - self.y == 0:
            if x > self.x:
                for x_check in range(self.x+1, x):
                    if super().check_board(x_check, y, board) != 0:
                        return False
            if x < self.x:
                for x_check in range(self.x-1, x, -1):
                    if super().check_board(x_check, y, board) != 0:
                        return False

        return "success"


class Bishop(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.name = 'B'
        if position == 0:
            self.x = 3
        else:
            self.x = 6
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        if abs(self.x - x) != abs(self.y - y):
            return False
        if self.x - x > 0 and self.y - y > 0:
            for x_check, y_check in zip(
                    range(self.x-1, x, -1),
                    range(self.y-1, y, -1)):
                if super().check_board(x, y, board) != 0:
                    return False
        if self.x - x < 0 and self.y - y > 0:
            for x_check, y_check in zip(
                    range(self.x+1, x),
                    range(self.y-1, y, -1)):
                if super().check_board(x, y, board) != 0:
                    return False
        if self.x - x < 0 and self.y - y < 0:
            for x_check, y_check in zip(
                    range(self.x+1, x),
                    range(self.y+1, y)):
                if super().check_board(x, y, board) != 0:
                    return False
        if self.x - x > 0 and self.y - y < 0:
            for x_check, y_check in zip(
                    range(self.x-1, x, -1),
                    range(self.y+1, y)):
                if super().check_board(x, y, board) != 0:
                    return False

        if super().check_board(x, y, board) == 1:
            return False
        return "success"


class Knight(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.name = 'K'
        if position == 0:
            self.x = 2
        else:
            self.x = 7
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        possible_moves = [(self.x-1, self.y-2),
                          (self.x-2, self.y-1),
                          (self.x-2, self.y+1),
                          (self.x-1, self.y+2),
                          (self.x+1, self.y+2),
                          (self.x+2, self.y+1),
                          (self.x+2, self.y-1),
                          (self.x+1, self.y-2),
                          ]
        if super().check_board(x, y, board) == 1:
            print('test')
            return "failed"
        if (x, y) not in possible_moves:
            return "failed"
        return "success"

    def __repr__(self):
        return f"Knight {self.color} on {self.x}{self.y}."


class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = 'Q'
        self.x = 4
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        if x - self.x == 0:
            if y > self.y:
                for y_check in range(self.y+1, y):
                    if super().check_board(x, y_check, board) != 0:
                        return False
            if y < self.y:
                for y_check in range(self.y-1, y, -1):
                    if super().check_board(x, y_check, board) != 0:
                        print(x, y_check, board[x][y_check])
                        return False

        if y - self.y == 0:
            if x > self.x:
                for x_check in range(self.x+1, x):
                    if super().check_board(x_check, y, board) != 0:
                        return False
            if x < self.x:
                for x_check in range(self.x-1, x, -1):
                    if super().check_board(x_check, y, board) != 0:
                        return False

        if abs(self.x - x) == abs(self.y - y):
            if self.x - x > 0 and self.y - y > 0:
                for x_check, y_check in zip(
                        range(self.x-1, x, -1),
                        range(self.y-1, y, -1)):
                    if super().check_board(x, y, board) != 0:
                        return False
            if self.x - x < 0 and self.y - y > 0:
                for x_check, y_check in zip(
                        range(self.x+1, x),
                        range(self.y-1, y, -1)):
                    if super().check_board(x, y, board) != 0:
                        return False
            if self.x - x < 0 and self.y - y < 0:
                for x_check, y_check in zip(
                        range(self.x+1, x),
                        range(self.y+1, y)):
                    if super().check_board(x, y, board) != 0:
                        return False
            if self.x - x > 0 and self.y - y < 0:
                for x_check, y_check in zip(
                        range(self.x-1, x, -1),
                        range(self.y+1, y)):
                    if super().check_board(x, y, board) != 0:
                        return False

        if super().check_board(x, y, board) == 1:
            return False
        return "success"


class King(Piece):
    def __init__(self, color: str, ) -> None:
        super().__init__(color)
        self.x = 5
        self.name = 'Z'
        if color == "black":
            self.y = 8
        else:
            self.y = 1
        self.first_move = 1

    def is_check_mate(self):
        return False

    def is_castling_move(self, x: int, y: int, board: list[int]) -> bool:
        if y != self.y or x not in [3, 7]:
            return False
        if x == 3:
            for x_check in [2, 3, 4]:
                if super().check_board(x_check, y, board) != 0:
                    return False
        if x == 7:
            for x_check in [6, 7]:
                if super().check_board(x_check, y, board) != 0:
                    return False
        return True

    def is_move_possible(self, x: int, y: int, board: list) -> list:
        if self.is_castling_move(x, y, board):
            if self.first_move == 1:
                return 'castling'
        possible_move = [(self.x+1, self.y),
                         (self.x+1, self.y+1),
                         (self.x+1, self.y-1),
                         (self.x, self.y+1),
                         (self.x, self.y-1),
                         (self.x-1, self.y),
                         (self.x-1, self.y+1),
                         (self.x-1, self.y-1)
                         ]

        if (x, y) not in possible_move:
            return False

        if super().check_board(x, y, board) == 1:
            return False
        self.first_move = 0
        return "success"


class Board():
    def __init__(self) -> None:
        self.board = [['  ', 'a', ' ', 'b', ' ', 'c', ' ', 'd', ' ', 'e', ' ', 'f', ' ', 'g', ' ', 'h'],
                      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',],
                      ['1', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '1'],
                      ['2', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '2'],
                      ['3', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '3'],
                      ['4', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '4'],
                      ['5', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '5'],
                      ['6', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '6'],
                      ['7', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '7'],
                      ['8', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', ' ', '|', '8'],
                      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',],
                      ['  ', 'a', ' ', 'b', ' ', 'c', ' ', 'd', ' ', 'e', ' ', 'f', ' ', 'g', ' ', 'h'],
                      ]

    def print(self):
        for row in self.board:
            for cell in row:
                print(cell, end='')
            print('')

    def draw_piece(self, x: int, y: int, piece: str, color: str) -> None:
        if color == 'black':
            piece = colored(piece, 'blue')
        else:
            piece = piece
        self._draw(x, y, piece)

    def _draw(self, x: int, y: int, value: str) -> None:
        y_modified = y + 2
        x_modified = (x + 1)*2
        self.board[y_modified][x_modified] = value

    def draw_empty_cell(self, x: int, y: int) -> None:
        self._draw(x, y, ' ')
