import numpy as np


N = 9


class Player:
    fences_left = 10

    def __init__(self, starting_position):
        self.position = starting_position


class Board:
    horizontal_fences = np.zeros((N-1, N-1))  # (i, j) fence is between i-th and i+1-th row, and is in j-th and j+1-th column
    vertical_fences = np.zeros((N-1, N-1))  # (i, j) fence is between j-th and j+1-th column, and is in i-th and i+1-th row

    def fence_above(self, position):
        x, y = position
        if y == 0:
            return self.horizontal_fences[x-1][y]
        if y == N-1:
            return self.horizontal_fences[x-1][y-1]
        return self.horizontal_fences[x-1][y-1] or self.horizontal_fences[x-1][y]

    def fence_below(self, position):
        x, y = position
        if y == 0:
            return self.horizontal_fences[x][y]
        if y == N-1:
            return self.horizontal_fences[x][y-1]
        return self.horizontal_fences[x][y-1] or self.horizontal_fences[x][y]

    def fence_on_left(self, position):
        x, y = position
        if x == 0:
            return self.vertical_fences[x][y-1]
        if x == N-1:
            return self.vertical_fences[x-1][y-1]
        return self.vertical_fences[x-1][y-1] or self.vertical_fences[x][y-1]

    def fence_on_right(self, position):
        x, y = position
        if x == 0:
            return self.vertical_fences[x][y]
        if x == N-1:
            return self.vertical_fences[x-1][y]
        return self.vertical_fences[x-1][y] or self.vertical_fences[x][y]


class Game:
    first_player = Player((0, N//2))
    second_player = Player((N-1, N//2))
    current_player = first_player
    other_player = second_player
    board = Board()

    def get_winning_player(self):
        if self.first_player.position[0] == N-1:
            return self.first_player
        if self.second_player.position[0] == 0:
            return self.second_player
        return None

    def get_available_pawn_moves(self):
        x, y = self.current_player.position
        up_move = (x-1, y)
        down_move = (x+1, y)
        left_move = (x, y-1)
        right_move = (x, y+1)
        move_candidates = [up_move, down_move, left_move, right_move]
        moves_not_allowed = [self.board.fence_above,
                         self.board.fence_below,
                         self.board.fence_on_left,
                         self.board.fence_on_right]
        move_candidates = [move for move, is_not_allowed in zip(move_candidates, moves_not_allowed)
                           if self.is_inside_board(move) and not is_not_allowed(self.current_player.position)]
        if self.other_player.position in move_candidates:
            move_candidates.remove(self.other_player.position)
            new_move_candidate = self.current_player.position + 2*(self.other_player.position - self.current_player.position)  # ok, if it inside the board and there is no fence
        return move_candidates

    def get_available_fence_positions(self):
        pass

    def is_inside_board(self, position):
        x, y = position
        return (x >= 0) and (x <= N-1) and (y >= 0) and (y <= N-1)


if __name__ == '__main__':
    p1 = Player((3, 4))
    p2 = Player((6, 1))
    game = Game()
    print(game.get_available_pawn_moves())
    game.board.vertical_fences[0][3] = 1
    print(game.get_available_pawn_moves())
    game.board.vertical_fences[0][4] = 1
    print(game.get_available_pawn_moves())
    game.board.horizontal_fences[0][3] = 1
    print(game.get_available_pawn_moves())
    p2.fences_left = 7
    print(p1.fences_left)
    print(p2.fences_left)
