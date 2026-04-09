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

    def test_opening_book_startpos(self):
        bot = ChessBot()
        move = bot.move(depth=1)
        self.assertIn(move, ["e2e4", "d2d4"])
        
    def test_opening_book_reply(self):
        bot = ChessBot()
        bot.update('e2e4')
        move = bot.move(depth=1)
        self.assertIn(move, ["e7e5", "c7c5"])

    def test_opening_book_extended(self):
        bot = ChessBot()
        bot.update('d2d4')
        bot.update('g8f6')
        bot.update('c2c4')
        move = bot.move(depth=1)
        self.assertIn(move, ["e7e6", "g7g6"])
        
        bot2 = ChessBot()
        bot2.update('e2e4')
        bot2.update('c7c5')
        move2 = bot2.move(depth=1)
        self.assertIn(move2, ["g1f3", "b1c3"])

    def test_invalid_book_entry_ignored(self):
        import opening_book
        bot = ChessBot()
        key = opening_book.get_book_key(bot.board)
        original = opening_book.BOOK[key][:]
        
        # Force the book to only contain a very illegal move
        opening_book.BOOK[key] = ["e1e8"]
        move = bot.move(depth=1)
        
        self.assertNotEqual(move, "e1e8")
        
        # Restore
        opening_book.BOOK[key] = original

    def test_make_unmake_roundtrip(self):
        tests = [
            # Normal
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", (52, 36, None)), # e2e4
            # Capture
            ("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2", (28, 19, None)), # e4xd5
            # En Passant
            ("k7/8/8/3pP3/8/8/8/K7 w - d6 0 1", (28, 19, None)), # e5xd6 ep
            # Castling Kingside
            ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", (60, 62, None)), # e1g1
            # Castling Queenside
            ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", (60, 58, None)), # e1c1
            # Promotion
            ("8/P7/8/8/8/8/8/k6K w - - 0 1", (8, 0, 'Q')), # a7a8q
            # Black Castling Kingside
            ("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1", (4, 6, None)),
            # Black Castling Queenside
            ("r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1", (4, 2, None)),
            # Black Promotion
            ("8/8/8/8/8/8/p7/k6K b - - 0 1", (48, 56, 'q')),
            # Capture home rook (affects castling rights directly)
            ("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1", (60, 0, None))
        ]
        
        for fen, m in tests:
            bot = ChessBot(fen)
            orig_fen = bot.to_fen()
            orig_tt = bot.board.get_tt_key()
            undo = bot.board.make_move(m)
            self.assertNotEqual(bot.to_fen(), orig_fen)
            bot.board.unmake_move(m, undo)
            self.assertEqual(bot.to_fen(), orig_fen)
            self.assertEqual(bot.board.get_tt_key(), orig_tt)

    def test_draw_conditions(self):
        # 50-move rule (halfmove = 100)
        bot = ChessBot("8/8/8/8/8/8/8/k6K w - - 100 1")
        self.assertTrue(bot.board.is_draw_by_50_move())
        self.assertTrue(bot.board.is_draw())

        # Insufficient material
        tests_insuf = [
            "8/8/8/8/8/8/8/k6K w - - 0 1", # K v K
            "8/8/8/8/8/8/8/k6K b - - 0 1", # K v K
            "8/8/8/8/8/8/8/kB5K w - - 0 1", # KB v K
            "8/8/8/8/8/8/8/kN5K w - - 0 1"  # KN v K
        ]
        for f in tests_insuf:
            self.assertTrue(ChessBot(f).board.is_insufficient_material())

        # Sufficient material
        tests_suf = [
            "8/8/8/8/8/8/8/kR5K w - - 0 1", # KR v K
            "8/8/8/8/8/8/8/kP5K w - - 0 1", # KP v K
            "8/8/8/8/8/8/8/kBN4K w - - 0 1" # KBN v K
        ]
        for f in tests_suf:
            self.assertFalse(ChessBot(f).board.is_insufficient_material())

        # Threefold repetition and unmake tracking
        bot = ChessBot("8/8/8/8/8/8/8/k6K w - - 0 1")
        m1 = (63, 62, None) # Kh1-g1
        m2 = (0, 1, None)   # Ka8-b8
        m3 = (62, 63, None) # Kg1-h1
        m4 = (1, 0, None)   # Kb8-a8
        
        # Move 1
        u1 = bot.board.make_move(m1)
        u2 = bot.board.make_move(m2)
        # Move 2 (first repeat)
        u3 = bot.board.make_move(m3)
        u4 = bot.board.make_move(m4)
        self.assertEqual(bot.board.history.get(bot.board.get_tt_key(), 0), 2)
        self.assertFalse(bot.board.is_draw_by_repetition())
        # Move 3 (second repeat)
        u5 = bot.board.make_move(m1)
        u6 = bot.board.make_move(m2)
        u7 = bot.board.make_move(m3)
        u8 = bot.board.make_move(m4)
        
        self.assertEqual(bot.board.history.get(bot.board.get_tt_key(), 0), 3)
        self.assertTrue(bot.board.is_draw_by_repetition())
        self.assertTrue(bot.board.is_draw())

        # Test unmake tracking restoration
        bot.board.unmake_move(m4, u8)
        self.assertEqual(bot.board.history.get(bot.board.get_tt_key(), 0), 2)
        self.assertFalse(bot.board.is_draw_by_repetition())

if __name__ == '__main__':
    unittest.main()
