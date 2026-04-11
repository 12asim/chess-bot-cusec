from board import Board, START_FEN
from move_generation import get_legal_moves
from search import search
from opening_book import get_book_move

class ChessBot:
    def __init__(self, fen=START_FEN):
        self.board = Board(fen)
        self.move_history = []
        
    def to_fen(self):
        return self.board.to_fen()
        
    def __call__(self):
        return self.to_fen()
        
    def is_draw(self):
        return self.board.is_draw()
        
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
            
        undo_info = self.board.make_move(move_tuple)
        self.move_history.append((move_tuple, undo_info))
        
    def undo_last_move(self):
        if self.move_history:
            move_tuple, undo_info = self.move_history.pop()
            self.board.unmake_move(move_tuple, undo_info)
            return True
        return False

    def choose_time_limit(self, remaining_time, increment=0.0):
        ply = len(self.move_history)
        # Expect ~50 moves initially, dropping to 20 dynamically to accelerate late game without flagging
        expected_moves = max(20, 50 - ply // 2)
        
        allocated = remaining_time / expected_moves
        allocated += increment * 0.8
        
        allocated -= 0.1 # small fixed move overhead
        
        # never spend too much of the remaining clock on one move
        allocated = min(allocated, remaining_time * 0.25)
        
        return max(0.1, allocated)

    def move(self, depth=2, time_limit=None):
        book_move = get_book_move(self.board)
        if book_move:
            return book_move
            
        if time_limit is not None:
            depth = None
            
        best = search(self.board, depth=depth, time_limit=time_limit)
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
