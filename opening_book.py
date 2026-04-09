import random

BOOK = {
    # Start position
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -": ["e2e4", "d2d4"],
    
    # --- 1. e4 defenses ---
    # 1. e4
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3": ["e7e5", "c7c5"],
    
    # 1... c5 (Sicilian)
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6": ["g1f3", "b1c3"],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -": ["d7d6", "b8c6", "e7e6"],
    # 1. e4 c5 2. Nf3 d6
    "rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": ["d2d4", "f1e2"],
    # 1. e4 c5 2. Nf3 Nc6
    "r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": ["d2d4", "f1b5"],
    # 1. e4 c5 2. Nf3 e6
    "rnbqkbnr/pp1p1ppp/4p3/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": ["d2d4", "c2c3"],
    
    # 1... e5 (Open Game)
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6": ["g1f3", "b1c3"],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -": ["b8c6", "g8f6", "d7d6"],
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": ["f1c4", "f1b5"],
    # Italian Game
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq -": ["f8c5", "g8f6"],
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -": ["c2c3", "d2d3", "e1g1"],
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -": ["d2d3", "e1g1", "f3g5"],
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R b KQkq -": ["g8f6"],
    # Ruy Lopez
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq -": ["a7a6", "g8f6"],
    
    # --- 1. d4 defenses ---
    # 1. d4
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3": ["d7d5", "g8f6"],
    
    # 1... d5
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6": ["c2c4", "g1f3"],
    # 1. d4 d5 2. c4
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3": ["e7e6", "c7c6"],
    # 1. d4 d5 2. c4 e6
    "rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": ["b1c3", "g1f3"],
    # 1. d4 d5 2. c4 c6
    "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": ["g1f3", "b1c3"],
    
    # 1... Nf6 (Indian)
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq -": ["c2c4", "g1f3"],
    # 1. d4 Nf6 2. Nf3
    "rnbqkb1r/pppppppp/5n2/8/3P4/5N2/PPP1PPPP/RNBQKB1R b KQkq -": ["e7e6", "g7g6", "d7d5"],
    # 1. d4 Nf6 2. c4
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3": ["e7e6", "g7g6"],
    # 1. d4 Nf6 2. c4 e6
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": ["g1f3", "b1c3"],
    # 1. d4 Nf6 2. c4 e6 3. Nf3 (QID/Bogo)
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq -": ["f8e7", "d7d5", "b7b6"],
    # 1. d4 Nf6 2. c4 e6 3. Nc3 (Nimzo)
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/2N5/PP2PPPP/R1BQKBNR b KQkq -": ["f8b4", "d7d5"],
    
    # 1. d4 Nf6 2. c4 g6 (KID / Grunfeld)
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": ["b1c3", "g1f3"],
    # 1. d4 Nf6 2. c4 g6 3. Nc3
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/2N5/PP2PPPP/R1BQKBNR b KQkq -": ["f8g7", "d7d5"],
    # 1. d4 Nf6 2. c4 g6 3. Nc3 Bg7
    "rnbqk2r/ppppppbp/5np1/8/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq -": ["e2e4", "g1f3"]
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
            
        valid_choices = [c for c in BOOK[key] if c in legal_ucis]
        if valid_choices:
            return random.choice(valid_choices)
    return None
