import random

BOOK = {
    # Start position
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -": [("e2e4", 70), ("d2d4", 30)],
    
    # --- 1. e4 defenses ---
    # 1. e4
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3": [("e7e5", 50), ("c7c5", 50)],
    
    # 1... c5 (Sicilian)
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6": [("g1f3", 80), ("b1c3", 20)],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -": [("d7d6", 40), ("b8c6", 40), ("e7e6", 20)],
    # 1. e4 c5 2. Nf3 d6
    "rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": [("d2d4", 90), ("f1e2", 10)],
    # 1. e4 c5 2. Nf3 Nc6
    "r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": [("d2d4", 75), ("f1b5", 25)],
    # 1. e4 c5 2. Nf3 e6
    "rnbqkbnr/pp1p1ppp/4p3/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": [("d2d4", 80), ("c2c3", 20)],
    
    # 1... e5 (Open Game)
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6": [("g1f3", 80), ("b1c3", 20)],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -": [("b8c6", 80), ("g8f6", 15), ("d7d6", 5)],
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": [("f1c4", 60), ("f1b5", 40)],
    # Italian Game
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq -": [("f8c5", 70), ("g8f6", 30)],
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -": [("c2c3", 50), ("d2d3", 40), ("e1g1", 10)],
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -": [("d2d3", 60), ("e1g1", 30), ("f3g5", 10)],
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R b KQkq -": [("g8f6", 100)],
    # Ruy Lopez
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq -": [("a7a6", 70), ("g8f6", 30)],
    
    # --- 1. d4 defenses ---
    # 1. d4
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3": [("d7d5", 60), ("g8f6", 40)],
    
    # 1... d5
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6": [("c2c4", 80), ("g1f3", 20)],
    # 1. d4 d5 2. c4
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3": [("e7e6", 60), ("c7c6", 40)],
    # 1. d4 d5 2. c4 e6
    "rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": [("b1c3", 60), ("g1f3", 40)],
    # 1. d4 d5 2. c4 c6
    "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": [("g1f3", 60), ("b1c3", 40)],
    
    # 1... Nf6 (Indian)
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq -": [("c2c4", 80), ("g1f3", 20)],
    # 1. d4 Nf6 2. Nf3
    "rnbqkb1r/pppppppp/5n2/8/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq -": [("e7e6", 40), ("g7g6", 40), ("d7d5", 20)],
    # 1. d4 Nf6 2. c4
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3": [("e7e6", 60), ("g7g6", 40)],
    # 1. d4 Nf6 2. c4 e6
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": [("g1f3", 60), ("b1c3", 40)],
    # 1. d4 Nf6 2. c4 e6 3. Nf3 (QID/Bogo)
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq -": [("f8e7", 40), ("d7d5", 40), ("b7b6", 20)],
    # 1. d4 Nf6 2. c4 e6 3. Nc3 (Nimzo)
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/2N5/PP2PPPP/R1BQKBNR b KQkq -": [("f8b4", 70), ("d7d5", 30)],
    
    # 1. d4 Nf6 2. c4 g6 (KID / Grunfeld)
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": [("b1c3", 80), ("g1f3", 20)],
    # 1. d4 Nf6 2. c4 g6 3. Nc3
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/2N5/PP2PPPP/R1BQKBNR b KQkq -": [("f8g7", 80), ("d7d5", 20)],
    # 1. d4 Nf6 2. c4 g6 3. Nc3 Bg7
    "rnbqk2r/ppppppbp/5np1/8/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq -": [("e2e4", 80), ("g1f3", 20)]
}

from move_generation import get_legal_moves

def get_book_key(board):
    parts = board.to_fen().split()
    return " ".join(parts[:4])

def get_book_move(board):
    key = get_book_key(board)
    if key in BOOK:
        legal_moves = get_legal_moves(board)
        legal_ucis = []
        for start, end, promo in legal_moves:
            uci = board.square_to_str(start) + board.square_to_str(end)
            if promo: uci += promo.lower()
            legal_ucis.append(uci)
            
        valid_choices = [c for c in BOOK[key] if c[0] in legal_ucis]
        if valid_choices:
            moves = [c[0] for c in valid_choices]
            weights = [c[1] for c in valid_choices]
            return random.choices(moves, weights=weights)[0]
    return None
