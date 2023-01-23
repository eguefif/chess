from termcolor import colored
import platform
import os


class ChessBoard:
    def __init__(self, player1: "Player", player2: "player") -> None:
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
        self.active_set = self.black_set
    
    def check_move_format(self, moves: [str]) -> bool:
        for move in moves:
            if move[0] not in range(1,9):
                return False
            if move[1] not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
                return False
        return True

    def move_piece(self, current_position: str, target_position: str) -> str:
        self.set_active_set()
        if !self.check_move_format([target_position, current_position]):
            return
        
        x_current, y_current = self.get_xy_position(current_position)
        piece = self.get_piece(x_current, y_current)

        if piece == None:
            print(f"There is not piece on {current_position}.")
            return

        if set.active_player.check is True:
            if piece.p != "z":
                print("Your king is in check, move it.")
                return
        
        x_target, y_target = self.get_xy_position(target_position)
        move_state = piece.is_move_possible(x, y)
        if move_state != "success":
            print("This move is not authorized")

        kill = self.check_for_kill(x_target, y_target)
        if kill.name == "z":
            if kill.is_check_mate():
                return "mate"
            else:
                self.get_non_active_player().check = True
                self.switch_active_player()
                return "success"
        if isinstance(kill, Piece):
            kill.alive = 0
        
        piece.move(x, y)
        self.board.draw_empty_position(x_current, y_current)
        self.switch_active_player()
        return "success"

    def get_non_active_player(self) -> Player:
        if self.active_player == self.player1:
            return self.player2
        else:
            return self.player1

    def switch_active_player(self) -> None:
        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def get_piece(self, x: int, y: int) -> Piece:
        for subset in self.active_set.set:
            for piece in subset:
                if piece.x = x and piece.y = y:
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
        y_position = letter_position.get(position[1])
        return int(position[0]), y_position


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
            print(piee, end=" ")
        print('')

    def give_white_player_name(self) -> None:
        if self.player1.color == "White":
            return self.player1.name
        return self.player2.name

    def give_black_player_name(self) -> None:
        if self.player1.color == "Black":
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
    
    def return_dead_pieces(self) -> list:
        dead_pieces = [piece.name for subset in self.set for piece in subset if piece.alive == 0]
        return dead_pieces

    def draw_pieces(self, board: "Board") -> None:
        for pieces in self.set:
            for piece in pieces:
                piece.draw(board)


class Piece:
    x: int
    y:int
    def __init__(self, color: str) -> None:
        self.color = color
        self.alive = 1
   
    def draw(self, board: "Board") -> None:
        if self.alive == 1:
            board.draw_piece(self.x, self.y, self.p, self.color)

    def is_move_possible(self, x: int, y: int) -> bool:
        ...

    def move(self, x: int, y:int) -> None:
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
        if color == "black":
            self.y = 7
        else:
            self.y = 2

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


class Queen(Piece):
    def __init__(self, color: str, ) -> None:
        super().__init__(color)
        self.p = 'Q'
        self.x = 4
        if color == "black":
            self.y = 8
        else:
            self.y = 1


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

class Board():
    def __init__(self) -> None:
        self.board = [['  ','a', ' ', 'b',  ' ', 'c', ' ', 'd', ' ', 'e' ,' ', 'f', ' ', 'g'], 
                     ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',],
                     ['1', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '1' ],
                     ['2', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '2' ],
                     ['3', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '3' ],
                     ['4', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '4' ],
                     ['5', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '5' ],
                     ['6', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '6' ],
                     ['7', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '7' ],
                     ['8', '|', ' ', '|',' ', '|', ' ', '|', ' ' ,'|', ' ', '|', ' ','|',  ' ', '|', ' ', '|', '8' ],
                     ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',],
                     ['  ','a', ' ', 'b',  ' ', 'c', ' ', 'd', ' ', 'e' ,' ', 'f', ' ', 'g'], 
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

    def draw_empty_position(self, x:int, y: int) -> None:
        self.draw(x, y, ' ')

    def draw(self, x: int, y: int, value: str) -> None:
        self.board[y_1][x*2] = value
