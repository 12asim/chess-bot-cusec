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

    def test_repeated_fen_loading(self):
        bot = ChessBot()
        bot.board.load_fen("k7/8/8/8/8/8/8/K7 w - - 0 1")
        bot.board.load_fen(START_FEN)
        self.assertEqual(bot.to_fen(), START_FEN)

    def test_missing_rook_castling(self):
        fen = "k7/8/8/8/8/8/8/4K3 w K - 0 1"
        bot = ChessBot(fen)
        from move_generation import get_legal_moves
        moves = get_legal_moves(bot.board)
        self.assertNotIn((60, 62, None), moves)

    def test_illegal_castle_through_check(self):
        # Black rook on f2 attacks f1, preventing O-O
        fen = "k7/8/8/8/8/8/5r2/4K2R w K - 0 1"
        bot = ChessBot(fen)
        from move_generation import get_legal_moves
        moves = get_legal_moves(bot.board)
        self.assertNotIn((60, 62, None), moves)

    def test_en_passant_legality_check(self):
        # White pawn on e5, Black pawn on d5. En passant is pseudo-legal,
        # but taking exposes king on e1 to rook on h5... wait, e1 and h5 don't align.
        # Let's say King is on e5 rank. K on a5. r on h5.
        fen = "k7/8/8/K2pP2r/8/8/8/8 w - d6 0 1"
        bot = ChessBot(fen)
        from move_generation import get_legal_moves
        moves = get_legal_moves(bot.board)
        # e5xd6 (28 to 19) is illegal because removing e5 and d5 exposes a5 to h5
        self.assertNotIn((28, 19, None), moves)

    def test_checkmate_stalemate_edge_cases(self):
        # Stalemate
        fen = "7k/5Q2/8/8/8/8/8/K7 b - - 0 1"
        bot = ChessBot(fen)
        from move_generation import get_legal_moves
        self.assertEqual(len(get_legal_moves(bot.board)), 0)
        self.assertIsNone(bot.move())
        
        # Checkmate
        fen = "7k/5Q2/7R/8/8/8/8/K7 b - - 0 1"
        bot = ChessBot(fen)
        self.assertEqual(len(get_legal_moves(bot.board)), 0)
        self.assertIsNone(bot.move())
        
    def test_perft_initial(self):
        from move_generation import get_legal_moves
        def perft(board, depth):
            if depth == 0: return 1
            nodes = 0
            for m in get_legal_moves(board):
                b2 = board.copy()
                b2.apply_move(m)
                nodes += perft(b2, depth - 1)
            return nodes
            
        bot = ChessBot()
        self.assertEqual(perft(bot.board, 1), 20)
        self.assertEqual(perft(bot.board, 2), 400)

if __name__ == '__main__':
    unittest.main()
