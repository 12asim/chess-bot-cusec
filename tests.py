import unittest
from chess_bot import ChessBot, START_FEN

class TestChessBot(unittest.TestCase):
    def test_fen_round_trip(self):
        bot = ChessBot()
        self.assertEqual(bot(), START_FEN)
        self.assertEqual(bot.to_fen(), START_FEN)
        
    def test_normal_legal_moves(self):
        bot = ChessBot()
        bot.update('e2e4')
        bot.update('e7e5')
        bot.update('g1f3')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('f3')], 'N')
        self.assertEqual(bot.board.turn, 'b')
        
    def test_illegal_move_rejection(self):
        bot = ChessBot()
        with self.assertRaises(ValueError):
            bot.update('e2e5')
        with self.assertRaises(ValueError):
            bot.update('g1g3')
        with self.assertRaises(ValueError):
            bot.update('e1e2')
            
    def test_castling(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
        bot = ChessBot(fen=fen)
        bot.update('e1g1')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('g1')], 'K')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('f1')], 'R')
        bot.update('e8c8')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('c8')], 'k')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('d8')], 'r')
        
    def test_en_passant(self):
        fen = "k7/8/8/3pP3/8/8/8/K7 w - d6 0 1"
        bot = ChessBot(fen=fen)
        bot.update('e5d6')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('d5')], '.')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('d6')], 'P')
        
    def test_promotion(self):
        fen = "8/P7/8/8/8/8/8/k6K w - - 0 1"
        bot = ChessBot(fen=fen)
        bot.update('a7a8q')
        self.assertEqual(bot.board.pieces[bot.board.square_from_str('a8')], 'Q')
        
    def test_move_returns_legal_uci(self):
        bot = ChessBot()
        m = bot.move()
        self.assertTrue(len(m) in [4, 5])
        bot.update(m)
        
    def test_checkmate_scenario(self):
        # White K on b6, R on h1. Black K on a8. White to play Rh8#
        fen = "k7/8/1K6/8/8/8/8/7R w - - 0 1"
        bot = ChessBot(fen)
        m = bot.move()
        self.assertEqual(m, "h1h8")
        bot.update(m)
        m2 = bot.move()
        self.assertIsNone(m2)

if __name__ == '__main__':
    unittest.main()
