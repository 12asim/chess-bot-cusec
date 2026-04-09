import time
from move_generation import get_legal_moves, is_in_check
from evaluation import evaluate

TT = {}
history = {}
killers = [[None, None] for _ in range(100)]
EXACT, LOWER, UPPER = 0, 1, 2

def get_piece_value(p):
    p = p.lower()
    if p == 'p': return 100
    if p == 'n': return 320
    if p == 'b': return 330
    if p == 'r': return 500
    if p == 'q': return 900
    if p == 'k': return 20000
    return 0

def order_moves(board, moves, prev_best=None, ply=0):
    def move_score(m):
        score = 0
        if m == prev_best:
            score += 100000
            
        start, end, promo = m
        target = board.pieces[end]
        is_ep = target == '.' and end == board.ep_square and board.pieces[start].lower() == 'p'
        
        if target != '.' or is_ep:
            val = 100 if is_ep else get_piece_value(target)
            score += 10 * val - get_piece_value(board.pieces[start]) + 10000
        elif promo:
            score += get_piece_value(promo) + 8000
        else:
            if ply < len(killers):
                if killers[ply][0] == m: score += 5000
                elif killers[ply][1] == m: score += 4000
            score += history.get(m, 0)
        return score
    return sorted(moves, key=move_score, reverse=True)

class TimeOutException(Exception):
    pass

def quiescence(board, alpha, beta, maximizing, ply):
    eval_score = evaluate(board)
    if maximizing:
        if eval_score >= beta:
            return beta
        alpha = max(alpha, eval_score)
    else:
        if eval_score <= alpha:
            return alpha
        beta = min(beta, eval_score)
        
    moves = get_legal_moves(board)
    q_moves = []
    for m in moves:
        is_ep = m[1] == board.ep_square and board.pieces[m[0]].lower() == 'p'
        if board.pieces[m[1]] != '.' or m[2] or is_ep:
            q_moves.append(m)
            
    def q_score(m):
        if m[2]: return 900
        val = 100 if board.pieces[m[1]] == '.' else get_piece_value(board.pieces[m[1]])
        return 10 * val - get_piece_value(board.pieces[m[0]])
        
    q_moves = sorted(q_moves, key=q_score, reverse=True)
    
    if maximizing:
        max_eval = eval_score
        for move in q_moves:
            undo = board.make_move(move)
            try:
                score = quiescence(board, alpha, beta, False, ply + 1)
            finally:
                board.unmake_move(move, undo)
            max_eval = max(max_eval, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = eval_score
        for move in q_moves:
            undo = board.make_move(move)
            try:
                score = quiescence(board, alpha, beta, True, ply + 1)
            finally:
                board.unmake_move(move, undo)
            min_eval = min(min_eval, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_eval

def alphabeta(board, depth, alpha, beta, maximizing, ply, prev_best=None, start_time=None, time_limit=None):
    if time_limit and start_time and (time.time() - start_time) > time_limit:
        raise TimeOutException()

    if ply > 0 and board.is_draw():
        return None, 0

    tt_key = board.get_tt_key()
    tt_entry = TT.get(tt_key)
    tt_best_move = None

    if tt_entry is not None:
        tt_depth, tt_score, tt_flag, tt_best_move = tt_entry
        if tt_depth >= depth:
            if tt_flag == EXACT:
                return tt_best_move, tt_score
            elif tt_flag == LOWER:
                alpha = max(alpha, tt_score)
            elif tt_flag == UPPER:
                beta = min(beta, tt_score)
            if alpha >= beta:
                return tt_best_move, tt_score

    if depth == 0:
        return None, quiescence(board, alpha, beta, maximizing, ply)
        
    moves = get_legal_moves(board)
    if not moves:
        if is_in_check(board, board.turn):
            return None, (-90000 + ply) if maximizing else (90000 - ply)
        return None, 0
        
    moves = order_moves(board, moves, tt_best_move or prev_best, ply)
    
    best_move = moves[0]
    orig_alpha = alpha
    orig_beta = beta
    
    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            undo = board.make_move(move)
            try:
                _, eval_score = alphabeta(board, depth - 1, alpha, beta, False, ply + 1, None, start_time, time_limit)
            finally:
                board.unmake_move(move, undo)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                is_ep = board.pieces[move[1]] == '.' and move[1] == board.ep_square and board.pieces[move[0]].lower() == 'p'
                if board.pieces[move[1]] == '.' and move[2] is None and not is_ep:
                    if ply < len(killers) and killers[ply][0] != move:
                        killers[ply][1] = killers[ply][0]
                        killers[ply][0] = move
                    history[move] = history.get(move, 0) + depth * depth
                break
                
        flag = EXACT
        if max_eval <= orig_alpha:
            flag = UPPER
        elif max_eval >= orig_beta:
            flag = LOWER
            
        TT[tt_key] = (depth, max_eval, flag, best_move)
        return best_move, max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            undo = board.make_move(move)
            try:
                _, eval_score = alphabeta(board, depth - 1, alpha, beta, True, ply + 1, None, start_time, time_limit)
            finally:
                board.unmake_move(move, undo)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                is_ep = board.pieces[move[1]] == '.' and move[1] == board.ep_square and board.pieces[move[0]].lower() == 'p'
                if board.pieces[move[1]] == '.' and move[2] is None and not is_ep:
                    if ply < len(killers) and killers[ply][0] != move:
                        killers[ply][1] = killers[ply][0]
                        killers[ply][0] = move
                    history[move] = history.get(move, 0) + depth * depth
                break
                
        flag = EXACT
        if min_eval <= orig_alpha:
            flag = UPPER
        elif min_eval >= orig_beta:
            flag = LOWER
            
        TT[tt_key] = (depth, min_eval, flag, best_move)
        return best_move, min_eval

def search(board, depth=None, time_limit=None):
    global TT, killers, history
    if len(TT) > 1000000:
        TT.clear()
        
    killers = [[None, None] for _ in range(100)]
    history = {}
    
    if depth is None and time_limit is None:
        depth = 3
        
    start_time = time.time()
    best_move = None
    target_depth = depth if depth else 99
    
    for d in range(1, target_depth + 1):
        try:
            move, _ = alphabeta(board, d, -float('inf'), float('inf'), board.turn == 'w', 0, best_move, start_time, time_limit)
            if move:
                best_move = move
        except TimeOutException:
            break
            
        if time_limit and (time.time() - start_time) > time_limit:
            break
            
    if best_move is None:
        moves = get_legal_moves(board)
        if moves: return moves[0]
            
    return best_move
