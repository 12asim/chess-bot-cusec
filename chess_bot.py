from board import Board, START_FEN
from move_generation import get_legal_moves
from search import search

class ChessBot:
    def __init__(self, fen=START_FEN):
        self.board = Board(fen)
        
    def to_fen(self):
        return self.board.to_fen()
        
    def __call__(self):
        return self.to_fen()
        
    def update(self, uci_move):
        if len(uci_move) not in [4, 5]:
            raise ValueError(f"Invalid UCI move format: {uci_move}")
            
        start_sq = self.board.square_from_str(uci_move[:2])
        end_sq = self.board.square_from_str(uci_move[2:4])
        promo = uci_move[4] if len(uci_move) == 5 else None
        if promo and self.board.turn == 'w':
            promo = promo.upper()
            
        move_tuple = (start_sq, end_sq, promo)
        legals = get_legal_moves(self.board)
        
        if move_tuple not in legals:
            raise ValueError(f"Illegal move: {uci_move}")
            
        self.board.apply_move(move_tuple)
        
    def move(self, depth=2):
        best = search(self.board, depth=depth)
        if best is None:
            return None
            
        start, end, promo = best
        uci = self.board.square_to_str(start) + self.board.square_to_str(end)
        if promo:
            uci += promo.lower()
        return uci

if __name__ == "__main__":
    b = ChessBot()
    print("Start FEN:", b())
    m = b.move()
    print("Bot moves:", m)
    b.update(m)
    print("New FEN:", b())
