from chess.classes import ChessBoard, Player
import pytest
import string

player1 = Player("Raji", "white")
player2 = Player("Roger", "black")

chessboard = ChessBoard(player1, player2)

# Test moves

number = range(1, 9)
forbiden_moves = ['-1', 0, 111, ]
letter_ok = string.ascii_lowercase[:8] + string.ascii_uppercase[:8]
letter_forbiden = string.ascii_lowercase[8:] + string.ascii_uppercase[8:]
combination = []

for n in number:
    for l in letter_forbiden:
        forbiden_moves.append(f'{n}{l}')
        forbiden_moves.append(f'{l}{n}')

for n in number:
    for l in letter_ok:
        combination.append(f'{l}{n}')
        combination.append(f'{l}{n}')

@pytest.mark.parametrize('move', combination)
def test_moves(move):
    assert chessboard.check_move_format((move, 'a1'))

@pytest.mark.parametrize('move', combination)
def test_moves(move):
    assert chessboard.check_move_format(('a1', move))

@pytest.mark.parametrize('move', forbiden_moves)
def test_forbiden_moves(move):
    assert not chessboard.check_move_format(('a1', move))

@pytest.mark.parametrize('move', forbiden_moves)
def test_forbiden_moves(move):
    assert not chessboard.check_move_format(('a1', move))
