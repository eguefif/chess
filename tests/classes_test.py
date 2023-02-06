class MovePieceTest():
    def __init__(
            self,
            piece_type,
            piece_position,
            move_type,
            moves,
            chessboard):
        self._piece_type = piece_type
        self._piece_x = piece_position[0]
        self._piece_y = piece_position[1]
        self._move_type = move_type
        self._moves = moves
        self._chessboard = chessboard

    def test(self) -> bool:
        if self._move_type == "legal_move":
            return self._test_legal_moves()
        elif self._move_type == "illegal_move":
            return self._test_illegal_moves()
        elif self._move_type == "kill":
            return self._test_kill_moves()
        return False

    def _test_legal_moves(self) -> bool:
        starting_piece = self._chessboard.get_piece_by_position(
                self._piece_x,
                self._piece_y)
        print(self._piece_x, self._piece_y, id(starting_piece))
        for move in self._moves:
            x_current, y_current = self._chessboard.get_xy_position(move[0])
            x_target, y_target = self._chessboard.get_xy_position(move[1])
            move_state = self._chessboard.move_piece(
                    x_current,
                    y_current,
                    x_target,
                    y_target,
                    )
            print(f'Move from {x_current}{y_current} to {x_target}{y_target}')
            ending_piece = self._chessboard.get_piece_by_position(
                    x_target,
                    y_target)
        print(x_target, y_target, id(ending_piece))
        return (move_state == "success" and
                id(starting_piece) == id(ending_piece))

    def _test_illegal_moves(self) -> bool:
        for move in self._moves:
            x_current, y_current = self._chessboard.get_xy_position(move[0])
            x_target, y_target = self._chessboard.get_xy_position(move[1])
            move_state = self._chessboard.move_piece(
                    x_current,
                    y_current,
                    x_target,
                    y_target,
                    )
        return move_state == 'failed'

    def _test_kill_moves(self) -> bool:
        for move in self._moves:
            x_current, y_current = self._chessboard.get_xy_position(move[0])
            x_target, y_target = self._chessboard.get_xy_position(move[1])
            killed_piece = self._chessboard.get_piece_by_position(
                    x_target,
                    y_target)
            self._chessboard.move_piece(
                    x_current,
                    y_current,
                    x_target,
                    y_target,
                    )
        return killed_piece.alive == 0


class BuildMoves:
    def __init__(self, file_info, file_moves):
        self._info = file_info
        self._moves = file_moves
        self.data = []

    def make_data(self):
        list_info = self._give_basic_info()
        list_moves = self._give_list_of_moves()
        for key, info in enumerate(list_info):
            datum = {}
            datum['piece_type'] = info[0]
            datum['piece_position'] = info[1]
            datum['move_type'] = info[2]
            datum['moves'] = list_moves[key]
            self.data.append(datum)

    def _give_basic_info(self):
        """ This function return a list of basic info. Each row of the
        file is composed as followed:
        0-> piece type
        1-> piece position x
        2-> piece position y
        3-> move type (legal move, ilegal move, kill)
        """
        list_info = []
        with open(self._info, 'r') as file:
            data = file.readlines()
        for line in data:
            piece, x, y, move_type = line.split(',')
            info = []
            info.append(piece.strip())
            info.append([int(x), int(y)])
            info.append(move_type.strip())
            list_info.append(info)
        return list_info

    def _give_list_of_moves(self):
        """
           This function open the moves file and read a row.
           On each a row, there are moves.
           One move is composed by two positin, current and target position.
           Example of a row:
           a2a4, a7a6
           The first move is from a2 to a4 for the white.
           The second move is from a7 to a6. It is a black move.
        """
        list_moves = []
        with open(self._moves, 'r') as file:
            data = file.readlines()

        for line in data:
            entries = line.split(',')
            moves = []
            for entry in entries:
                move = []
                move.append(entry[0].strip() + entry[1].strip())
                move.append(entry[2].strip() + entry[3].strip())
                moves.append(move)
            list_moves.append(moves)
        return list_moves
