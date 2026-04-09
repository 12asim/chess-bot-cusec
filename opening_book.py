import random

BOOK = {
    # Start position
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -": ["e2e4", "d2d4"],
    
    # 1. e4
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3": ["e7e5", "c7c5"],
    # 1. e4 e5
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6": ["g1f3"],
    # 1. e4 e5 2. Nf3
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -": ["b8c6", "g8f6"],
    # 1. e4 e5 2. Nf3 Nc6
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -": ["f1c4"],
    # 1. e4 e5 2. Nf3 Nc6 3. Bc4
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq -": ["f8c5", "g8f6"],
    # 1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -": ["c2c3", "d2d3", "e1g1"],
    
    # 1. d4
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3": ["d7d5", "g8f6"],
    # 1. d4 d5
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6": ["c2c4", "g1f3"],
    # 1. d4 Nf6
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq -": ["c2c4", "g1f3"],
    # 1. d4 Nf6 2. c4
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3": ["e7e6", "g7g6"],
    # 1. d4 Nf6 2. c4 e6
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq -": ["g1f3", "b1c3"],
    # 1. d4 Nf6 2. c4 e6 3. Nf3
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/5N2/PP2PPPP/RNBQKB1R b KQkq -": ["f8e7", "d7d5"]
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
