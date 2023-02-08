from modules.game import Game
from modules.classes import ChessBoard, Player
from classes_test import MovePieceTest, BuildMoves
import pytest
import string


# Test moves
@pytest.fixture
def chessboard():
    player1 = Player("Raji", "white")
    player2 = Player("Roger", "black")
    chessboard = ChessBoard(player1, player2)
    return chessboard


moves = BuildMoves('./tests/test_moves.txt')
moves.make_data()
@pytest.mark.parametrize('parameters', moves.data)
def test_move(parameters, chessboard):
    move = MovePieceTest(
            parameters.get('piece_type'),
            parameters.get('piece_position'), 
            parameters.get('move_type'),
            parameters.get('moves'),
            chessboard)
    assert move.test()

# Test check_format function

number = range(1, 9)
forbiden_moves = [
        '-1', 0, 111,
        'wewffadsfasdfadsf', '121241231', '', ' ', '   ']
letter_ok = string.ascii_lowercase[:8] + string.ascii_uppercase[:8]
letter_forbiden = string.ascii_lowercase[8:] + string.ascii_uppercase[8:]
combination = []

for n in number:
    for letter in letter_forbiden:
        forbiden_moves.append(f'{n}{letter}')
        forbiden_moves.append(f'{letter}{n}')

for n in number:
    for letter in letter_ok:
        combination.append(f'{letter}{n}')
        combination.append(f'{letter}{n}')


@pytest.mark.parametrize('move', combination)
def test_moves(move, chessboard):
    assert chessboard.check_move_format(move)

@pytest.mark.parametrize('move', forbiden_moves)
def test_forbiden_moves(move, chessboard):
    assert not chessboard.check_move_format(move)


# Test for player's name

@pytest.fixture
def game():
    return Game()


@pytest.mark.parametrize(
        'name',
        [
            '',
            'S890isdohfosdnfsadofnsda;ofsadfbasfjdsf;',
            'qwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
            ])
def test_check_name(name, game):
    assert (not game.check_player1_name(name) and
            not game.check_player2_name(name))
