from unittest import TestCase

from game import Game, Player


class TestGame(TestCase):

    def setUp(self):
        self.game = Game()

    def test_get_available_pawn_moves(self):
        self.assertEqual(self.game.get_available_pawn_moves(), [(1, 4), (0, 3), (0, 5)])

    def test_get_available_pawn_moves_single_vertical_fence(self):
        self.game.board.vertical_fences[0][3] = 1
        self.assertEqual(self.game.get_available_pawn_moves(), [(1, 4), (0, 5)])

    def test_get_available_pawn_moves_single_horizontal_fence(self):
        self.game.board.horizontal_fences[0][3] = 1
        self.assertEqual(self.game.get_available_pawn_moves(), [(0, 3), (0, 5)])

    def test_get_available_pawn_moves_2_vertical_fences(self):
        self.game.board.vertical_fences[0][3] = 1
        self.game.board.vertical_fences[0][4] = 1
        self.assertEqual(self.game.get_available_pawn_moves(), [(1, 4)])

    def test_get_available_pawn_moves_both_horizontal_and_vertical_fences(self):
        self.game.board.vertical_fences[0][3] = 1
        self.game.board.vertical_fences[0][4] = 1
        self.game.board.horizontal_fences[0][3] = 1
        self.assertEqual(self.game.get_available_pawn_moves(), [])

    def test_get_available_pawn_moves_other_player_in_a_way(self):
        self.game.current_player = Player((1, 2))
        self.game.other_player = Player((0, 2))
        self.game.board.vertical_fences[0][1] = 1
        self.assertEqual(self.game.get_available_pawn_moves(), [(2, 2), (1, 3), (0, 3)])
