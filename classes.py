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
       board.draw_piece(self.x, self.y, self.p, self.color)


class Player:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color


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
        self.board[y+1][x*2] = piece
