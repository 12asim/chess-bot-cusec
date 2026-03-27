from move_generation import get_legal_moves, is_in_check
from evaluation import evaluate

def search(board, depth=3):
    best_move, _ = alphabeta(board, depth, -float('inf'), float('inf'), board.turn == 'w')
    if best_move is None:
        moves = get_legal_moves(board)
        if moves:
            return moves[0]
    return best_move

def alphabeta(board, depth, alpha, beta, maximizing):
    moves = get_legal_moves(board)
    if not moves:
        if is_in_check(board, board.turn):
            return None, -99999 if maximizing else 99999
        return None, 0
        
    if depth == 0:
        return None, evaluate(board)
        
    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            b2 = board.copy()
            b2.apply_move(move)
            _, eval_score = alphabeta(b2, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            b2 = board.copy()
            b2.apply_move(move)
            _, eval_score = alphabeta(b2, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return best_move, min_eval
