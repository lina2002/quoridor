import numpy as np


N = 9


class Player:
    fences_left = 10

    def __init__(self, starting_position):
        self.position = starting_position


def is_up(difference):
    return difference == (-1, 0)

def is_down(difference):
    return difference == (1, 0)

def is_left(difference):
    return difference == (0, -1)

def is_right(difference):
    return difference == (0, 1)


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

    def is_blocked_by_fence(self, position_from, position_to):
        difference = position_to - position_from
        if is_up(difference):
            return self.fence_above(position_from)
        elif is_down(difference):
            return self.fence_below(position_from)
        elif is_left(difference):
            return self.fence_on_left(position_from)
        elif is_right(difference):
            return self.fence_on_right(position_from)


def is_horizontal(difference):
    return difference[0] == 0


def is_inside_board(position):
    x, y = position
    return (x >= 0) and (x <= N-1) and (y >= 0) and (y <= N-1)


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
                           if is_inside_board(move) and not is_not_allowed(self.current_player.position)]
        if self.other_player.position in move_candidates:
            move_candidates.remove(self.other_player.position)
            difference = self.other_player.position - self.current_player.position
            new_move_candidate = self.current_player.position + 2*(self.other_player.position - self.current_player.position)  # ok, if it inside the board and there is no fence
            if not is_inside_board(new_move_candidate) or self.board.is_blocked_by_fence(self.other_player.position, new_move_candidate):
                x_o, y_o = self.other_player.position
                new_move_candidates = []
                if is_horizontal(difference):
                    other_up = (x_o, y_o-1)
                    other_down = (x_o, y_o+1)
                    if is_inside_board(other_up) and not self.board.fence_above(self.other_player.position):
                        new_move_candidates.append(other_up)
                    if is_inside_board(other_down) and not self.board.fence_below(self.other_player.position):
                        new_move_candidates.append(other_down)
                else:
                    other_left = (x_o-1, y_o)
                    other_right = (x_o+1, y_o)
                    if is_inside_board(other_left) and not self.board.fence_on_left(self.other_player.position):
                        new_move_candidates.append(other_left)
                    if is_inside_board(other_right) and not self.board.fence_on_right(self.other_player.position):
                        new_move_candidates.append(other_right)
                move_candidates = move_candidates + new_move_candidates
            else:
                move_candidates.append(new_move_candidate)
        return move_candidates

    def get_available_fence_positions(self):
        pass


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
