from modules.game import Game
from modules.classes import ChessBoard, Player
from classes_test import MovePieceTest, BuildMoves
import pytest
import string


@pytest.fixture
def chessboard():
    player1 = Player("Raji", "white")
    player2 = Player("Roger", "black")
    chessboard = ChessBoard(player1, player2)
    return chessboard


# Test castling
castle_tests = [
        ['g1', 'f1', ['e2e3', 'e7e6', 'f1e2', 'f8e7', 'g1f3', 'g8f6', 'e1g1']],
        ['c1', 'd1', ['d2d4', 'd7d5', 'd1d3', 'd8d6', 'c1d2', 'c8d7', 'b1a3',
                      'b8a6', 'e1c1']],
        ['g8', 'f8', ['e2e3', 'e7e6', 'f1e2', 'f8e7', 'g1f3', 'g8f6', 'e1g1',
                      'e8g8']],
        ['c8', 'd8', ['d2d4', 'd7d5', 'd1d3', 'd8d6', 'c1d2', 'c8d7', 'b1a3',
                      'b8a6', 'e1c1', 'e8c8']],
        ]


@pytest.mark.parametrize('parameters', castle_tests)
def test_castling(parameters, chessboard):
    king_x, king_y = chessboard.get_xy_position(parameters[0])
    rook_x, rook_y = chessboard.get_xy_position(parameters[1])
    moves = parameters[2]
    for move in moves:
        x, y = chessboard.get_xy_position(move[:2])
        x_target, y_target = chessboard.get_xy_position(move[2:])
        assert chessboard.move_piece(x, y, x_target, y_target) == 'success'
    check_king = chessboard.get_piece_by_position(king_x, king_y)
    check_rook = chessboard.get_piece_by_position(rook_x, rook_y)
    assert check_king.name == 'Z' and check_rook.name == 'R'


# Test moves
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
