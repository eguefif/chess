from chess.classes import ChessBoard, Player
from chess.game import Game
import pytest
import string


@pytest.fixture
def chessboard():
    player1 = Player("Raji", "white")
    player2 = Player("Roger", "black")
    chessboard = ChessBoard(player1, player2)
    return chessboard


# Test pawn moves
fake_game_legal_moves = [
         [('e2', 'e4'), ('d7', 'd6'), ('e4', 'e5'),
             ('d6', 'd5'), ('e5', 'e6')],
         [('e2', 'e3'), ('d7', 'd5'), ('e3', 'e4')],
         [('e2', 'e4'), ('d7', 'd5'), ('e4', 'e5')]
        ]


@pytest.mark.parametrize("moves", fake_game_legal_moves)
def test_legal_pawn_move(moves, chessboard):
    x_current, y_current = chessboard.get_xy_position(moves[0][0])
    starting_piece = chessboard.get_piece_by_position(x_current, y_current)
    for move in moves:
        x_current, y_current = chessboard.get_xy_position(move[0])
        x_target, y_target = chessboard.get_xy_position(move[1])
        chessboard.move_piece(
                x_current,
                y_current,
                x_target,
                y_target,
                )
        ending_piece = chessboard.get_piece_by_position(x_target, y_target)
    assert id(starting_piece) == id(ending_piece)


fake_game_illegal_moves = [
         [('e2', 'e4'), ('e7', 'e5'), ('e4', 'e5')],
         [('e2', 'e1')],
         [('e2', 'a1')],
         [('a1', 'a5')],
         [('e2', 'd7')],
         [('f2', 'g2')],
         [('g2', 'h3')],
         [('b2', 'a3')],
        ]


@pytest.mark.parametrize("moves", fake_game_illegal_moves)
def test_illegal_pawn_move(moves, chessboard):
    for move in moves:
        x_current, y_current = chessboard.get_xy_position(move[0])
        x_target, y_target = chessboard.get_xy_position(move[1])
        move_state = chessboard.move_piece(
                x_current,
                y_current,
                x_target,
                y_target,
                )
    assert move_state == 'failed'


fake_game_kill_moves = [
         [('e2', 'e4'), ('d7', 'd5'), ('e4', 'd5')],
         [('e2', 'e3'), ('d7', 'd5'), ('e3', 'e4'), ('d5', 'e4')],
         [('e2', 'e4'), ('f7', 'f5'), ('e4', 'f5')],
         [('c2', 'c3'), ('d7', 'd5'), ('c3', 'c4'), ('d5', 'c4')],
        ]


@pytest.mark.parametrize("moves", fake_game_kill_moves)
def test_kill_pawn_move(moves, chessboard):
    for move in moves:
        x_current, y_current = chessboard.get_xy_position(move[0])
        x_target, y_target = chessboard.get_xy_position(move[1])
        killed_piece = chessboard.get_piece_by_position(x_target, y_target)
        chessboard.move_piece(
                x_current,
                y_current,
                x_target,
                y_target,
                )
        ending_piece = chessboard.get_piece_by_position(x_target, y_target)
    assert killed_piece.alive == 0 and ending_piece.alive == 1

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
            "'salut",
            'tt/t',
            'qwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
            'asddfadfasdfdsasdfa',
            ])
def test_check_name(name, game):
    assert (not game.check_player1_name(name) and
            not game.check_player2_name(name))
