from termcolor import colored
import platform
import string
import os


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

    def set_active_set(self) -> None:
        if self.active_player.color == "white":
            self.active_set = self.white_set
            self.non_active_set = self.black_set
            return 
        self.active_set = self.black_set
        self.non_active_set = self.white_set

    def check_move_format(self, moves: [str]) -> bool:
        letters = string.ascii_lowercase[:8] + string.ascii_uppercase[:8]
        for move in moves:
            try:
                if len(move) != 2:
                    return False
            except TypeError:
                    print("Wrong position format")
                    return False
            if move[0] in letters:
                y = move[0]
                x = move[1]
            else:
                y = move[1]
                x = move[0]
            try:
                if int(x) not in range(1, 9):
                    return False
            except ValueError as ex:
                print("Wrong position format")
                return False
            if y not in letters:
                return False
        return True

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

    def move_piece(self, current_position: str, target_position: str) -> str:
        self.set_active_set()
        if self.check_move_format(
                [target_position, current_position]) is False:
            print('The target position is not valid.')
            return False

        x_current, y_current = self.get_xy_position(current_position)
        piece = self.get_piece(x_current, y_current)
        if piece is None:
            print(f"There is not piece on {current_position}.")
            return

        if self.active_player.check is True:
            if piece.p != "z":
                print("Your king is in check, move it.")
                return

        x_target, y_target = self.get_xy_position(target_position)
        board = self.get_board_with_pieces()
        move_state = piece.is_move_possible(x_target, y_target, board)
        if move_state != "success":
            print("This move is not authorized")
            return

        kill = self.check_for_kill(x_target, y_target)
        if kill is True:
            if kill.name == "z":
                if kill.is_check_mate():
                    return "mate"
                else:
                    self.get_non_active_player().check = True
                    self.switch_active_player()
                    return "check"
            self.non_active_set.kill_piece(x_target, y_target)

        self.active_set.move_piece(x_current, y_current, x_target, y_target)
        self.board.draw_empty_position(x_current, y_current)
        self.switch_active_player()
        return "success"

    def get_non_active_player(self) -> "Player":
        if self.active_player == self.player1:
            return self.player2
        else:
            return self.player1

    def switch_active_player(self) -> None:
        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def get_piece(self, x: int, y: int) -> "Piece":
        for subset in self.active_set.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    if piece.alive == 0:
                        return None
                    return piece
        return None

    def get_xy_position(self, position: str) -> (int, int):
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

    def draw_game(self):
        self.white_set.draw_pieces(self.board)
        self.black_set.draw_pieces(self.board)
        self.board.print()

    def print_interface(self):
        if platform.system == "windows":
            os.systen("cls")
        else:
            os.system("clear")

        print(""*4, "Chess game")
        print(f"White: {self.give_white_player_name()}")
        print(f"Black: {self.give_black_player_name()}")

    def print_dead_pieces(self):
        print("Dead pieces:")
        white_dead = self.white_set.return_dead_pieces()
        black_dead = self.black_set.return_dead_pieces()
        print("white", end=": ")
        for piece in white_dead:
            print(piece, end=' ')
        print('')
        print("black", end=": ")
        for piece in black_dead:
            print(piece, end=" ")
        print('')

    def check_for_kill(self, x: int, y: int) -> "Piece":
        board = self.get_board_with_pieces()
        if board[x][y] == 2:
            return self.get_piece_by_position(x, y)

    def get_piece_by_position(self, x: int, y: int) -> "Piece":
        for subset in self.white_set.set:
            for piece in subset:
                if piece.x == x and piece.y == y:
                    return piece

    def give_white_player_name(self) -> None:
        if self.player1.color == "white":
            return self.player1.name
        return self.player2.name

    def give_black_player_name(self) -> None:
        if self.player1.color == "black":
            return self.player1.name
        return self.player2.name


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

    def __init__(self, color: str) -> None:
        self.color = color
        self.alive = 1

    def draw(self, board: "Board") -> None:
        if self.alive == 1:
            board.draw_piece(self.x, self.y, self.p, self.color)

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
        self.p = 'p'
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
        for row in board:
            for c in row:
                print(c, ' ', end='')
            print()

        if self.y+y_direction*1 in range(9) :
            if board[self.x-1][self.y-1+1*y_direction] == 0:
                possible_move.append((self.x, self.y+y_direction*1))
        if self.y+y_direction*2 in range(9) and self.first_move == 1:
            if board[self.x-1][self.y-1+y_direction*2] == 0:
                possible_move.append((self.x, self.y+y_direction*2))
        if self.x+1 in range(9) and self.y+y_direction*1 in range(9):
            if board[self.x-1+1][self.y-1+y_direction*1] == 2:
                possible_move.append((self.x+1, self.y+y_direction*1))
        if self.x-1 in range(9) and self.y+y_direction*1 in range(9):
            if board[self.x-1-1][self.y-1+y_direction*1] == 2:
                possible_move.append((self.x-1, self.y+y_direction*1))
        print(possible_move)

        if (x, y) in possible_move:
            self.first_move = 0
            return "success"
        return False


class Rook(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.p = 'R'
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
                for y_check in range(self.y, y):
                    if board[x][y_check] != 0:
                        return False
            if y < self.y:
                for y_check in range(self.y, y, -1):
                    if board[x][y_check] != 0:
                        return False

        if y - self.y == 0:
            if x > self.x:
                for x_check in range(self.x, x):
                    if board[x_check][y] != 0:
                        return False
            if x < self.x:
                for x_check in range(self.x, x, -1):
                    if board[x_check][y] != 0:
                        return False

        return "success"


class Bishop(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.p = 'B'
        if position == 0:
            self.x = 3
        else:
            self.x = 6
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        possible_moves = []
        for x_check, y_check in zip(range(x.self, 9), range(y.self, 9)):
            possible_moves.append(x_check, y_check)
        for x_check, y_check in zip(range(x.self, 0, -1), range(y.self, 9)):
            possible_moves.append(x_check, y_check)
        for x_check, ycheck in zip(range(x.self, 0, -1), range(y.self, 0, -1)):
            possible_moves.append(x_check, y_check)
        for x_check, y_check in zip(range(x.self, 9), range(y.self, 0, -1)):
            possible_moves.append(x_check, y_check)

        if (x, y) not in possible_moves:
            return False

        for x_check, y_check in zip(range(self.x, x), range(self.y, y)):
            if board[x_check][y_check] != 0:
                return False
        return "success"


class Knight(Piece):
    def __init__(self, color: str, position: int) -> None:
        super().__init__(color)
        self.p = 'K'
        if position == 0:
            self.x = 2
        else:
            self.x = 7
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        possible_moves = [(self.x-1, self.y+2),
                          (self.x+1, self.y+2),
                          (self.x-1, self.y-2),
                          (self.x+1, self.y-2),
                          (self.x+2, self.y-1),
                          (self.x-2, self.y-1),
                          (self.x-2, self.y+1),
                          (self.x+2, self.y+1),
                          (self.x+2, self.y-2),
                          ]

        check_position = list(range(9))
        for position, key in enumerate(possible_moves):
            if (position[0] not in check_position or
                position[1] not in check_position):
                possible_moves.pop(key)
            if board[position[0]][position[1]] == 1:
                possible_moves.pop(key)

        if (x, y) in possible_moves:
            return "success"
        return False


class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.p = 'Q'
        self.x = 4
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_move_possible(self, x: int, y: int, board: list) -> bool:
        possible_moves = []
        for x_check, y_check in zip(range(x.self, 9), range(y.self, 9)):
            possible_moves.append(x_check, y_check)
        for x_check, y_check in zip(range(x.self, 0, -1), range(y.self, 9)):
            possible_moves.append(x_check, y_check)
        for x_check, ycheck in zip(range(x.self, 0, -1), range(y.self, 0, -1)):
            possible_moves.append(x_check, y_check)
        for x_check, y_check in zip(range(x.self, 9), range(y.self, 0, -1)):
            possible_moves.append(x_check, y_check)
        for y_check in range(1, 9):
            possible_moves.append((self.x, y))
        for x_check in range(1, 9):
            possible_moves.append((x_check, y))

        if (x, y) not in possible_moves:
            return False

        if y.self - y == 0:
            if x.self > x:
                for x.check in range(x.self, x):
                    if board[x.check][y] != 0:
                        return False
            if x.self < x == 0:
                for x.check in range(x.self, x, -1):
                    if board[x.check][y] != 0:
                        return False
        if x.self - x == 0:
            if y.self > y:
                for y.checkin in range(y.self, y):
                    if board[x][y.check] != 0:
                        return False
            if y.self < y:
                for y.check in range(y.self, y, -1):
                    if board[x][y.check] != 0:
                        return False

        for x_check, y_check in zip(range(self.x, x), range(self.y, y)):
            if board[x_check][y_check] != 0:
                return False
        return "success"


class King(Piece):
    def __init__(self, color: str, ) -> None:
        super().__init__(color)
        self.x = 5
        self.p = 'Z'
        if color == "black":
            self.y = 8
        else:
            self.y = 1

    def is_check_mate(self):
        return False

    def is_move_possible(self, x: int, y: int, board: list) -> list:
        possible_move = [(self.x+1, self.y),
                         (self.x+1, self.y+1),
                         (self.x+1, self.y-1),
                         (self.x, self.y+1),
                         (self.x, self.y-1),
                         (self.x-1, self.y),
                         (self.x-1, self.y+1),
                         (self.x+1, self.y-1)
                         ]

        if (x, y) not in possible_move:
            return False

        if board[x][y] == 1:
            return False
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
        self.draw(x, y, piece)

    def draw_empty_position(self, x: int, y: int) -> None:
        self.draw(x, y, ' ')

    def draw(self, x: int, y: int, value: str) -> None:
        self.board[y+1][x*2] = value
