from chess.classes import ChessBoard, Player
import pytest
import string

@pytest.fixture
def chessboard():
    player1 = Player("Raji", "white")
    player2 = Player("Roger", "black")
    chessboard = ChessBoard(player1, player2)
    return chessboard

# Test pawn moves
fake_game_legal_moves = [[('e2', 'e4'), ('d7', 'd6'), ('e4', 'e5'), ('d6', 'd5'), ('e5', 'e6')],
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
        chessboard.move_piece(x_current,
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
    x_current, y_current = chessboard.get_xy_position(moves[0][0])
    starting_piece = chessboard.get_piece_by_position(x_current, y_current)
    for move in moves:
        x_current, y_current = chessboard.get_xy_position(move[0])
        x_target, y_target = chessboard.get_xy_position(move[1])
        move_state = chessboard.move_piece(x_current,
                y_current,
                x_target,
                y_target,
                )
        ending_piece = chessboard.get_piece_by_position(x_target, y_target)
    assert move_state == 'failed'


fake_game_kill_moves = [
         [('e2', 'e4'), ('d7', 'd5'), ('e4', 'd5')],
         [('e2', 'e3'), ('d7', 'd5'), ('e3', 'e4'), ('d5', 'e4')],
         [('e2', 'e4'), ('f7', 'f5'), ('e4', 'f5')],
         [('c2', 'c3'), ('d7', 'd5'), ('c3', 'c4'), ('d5', 'c4')],
        ] 

@pytest.mark.parametrize("moves", fake_game_illegal_moves)
def test_illegal_pawn_move(moves, chessboard):
    x_current, y_current = chessboard.get_xy_position(moves[0][0])
    starting_piece = chessboard.get_piece_by_position(x_current, y_current)
    for move in moves:
        x_current, y_current = chessboard.get_xy_position(move[0])
        x_target, y_target = chessboard.get_xy_position(move[1])
        move_state = chessboard.move_piece(x_current,
                y_current,
                x_target,
                y_target,
                )
        ending_piece = chessboard.get_piece_if_alive(x_target, y_target)
        ending_piece_kill = chessboard.non_active_set.return_dead_pieces()
    assert starting_piece == ending_piece and ending_piece_kill[0].is_alive == 0

# Test check_format function

number = range(1, 9)
forbiden_moves = ['-1', 0, 111, 'wewffadsfasdfadsf', '121241231','', ' ', '   ']
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
def test_moves(move, chessboard):
    assert chessboard.check_move_format(move)

@pytest.mark.parametrize('move', combination)
def test_moves(move, chessboard):
    assert chessboard.check_move_format(move)

@pytest.mark.parametrize('move', forbiden_moves)
def test_forbiden_moves(move, chessboard):
    assert not chessboard.check_move_format(move)

@pytest.mark.parametrize('move', forbiden_moves)
def test_forbiden_moves(move, chessboard):
    assert not chessboard.check_move_format(move)
