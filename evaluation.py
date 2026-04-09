from board import Board

PIECE_VALUES = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
    'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000,
}

PST_P = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
PST_N = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]
PST_B = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]
PST_R = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
]
PST_Q = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
PST_K_MG = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]
PST_K_EG = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]
PST = {'P': PST_P, 'N': PST_N, 'B': PST_B, 'R': PST_R, 'Q': PST_Q}

N_WAYS = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
R_WAYS = [(0,1), (0,-1), (1,0), (-1,0)]
B_WAYS = [(1,1), (1,-1), (-1,1), (-1,-1)]

def get_mob(board, sq, is_slide, ways):
    m = 0
    r, c = sq // 8, sq % 8
    is_white = board.pieces[sq].isupper()
    for dr, dc in ways:
        nr, nc = r+dr, c+dc
        while 0 <= nr < 8 and 0 <= nc < 8:
            target = board.pieces[nr*8 + nc]
            if target == '.':
                m += 1
            else:
                if is_white != target.isupper():
                    m += 1
                break
            if not is_slide: break
            nr += dr; nc += dc
    return m

def evaluate(board):
    score = 0
    material_val = 0
    w_pawn_files = {f: [] for f in range(8)}
    b_pawn_files = {f: [] for f in range(8)}
    
    for sq in range(64):
        p = board.pieces[sq]
        if p == '.': continue
        pt = p.lower()
        if pt in ['n', 'b']: material_val += 300
        elif pt == 'r': material_val += 500
        elif pt == 'q': material_val += 900
        
        file = sq % 8
        rank = sq // 8
        if p == 'P': w_pawn_files[file].append(rank)
        elif p == 'p': b_pawn_files[file].append(rank)

    endgame = material_val <= 2000
    w_bishops = 0
    b_bishops = 0
    w_king_sq = -1
    b_king_sq = -1
    
    # Pawn structure
    for f in range(8):
        wp = w_pawn_files[f]
        bp = b_pawn_files[f]
        
        if len(wp) > 1: score -= 20 * (len(wp) - 1)
        if len(bp) > 1: score += 20 * (len(bp) - 1)
        
        w_adj = (w_pawn_files[f-1] if f > 0 else []) + (w_pawn_files[f+1] if f < 7 else [])
        if wp and not w_adj: score -= 20 * len(wp)
        
        b_adj = (b_pawn_files[f-1] if f > 0 else []) + (b_pawn_files[f+1] if f < 7 else [])
        if bp and not b_adj: score += 20 * len(bp)
        
        for r in wp:
            if not [br for br in bp + b_adj if br < r]:
                score += 10 + (7 - r) * 10
        for r in bp:
            if not [wr for wr in wp + w_adj if wr > r]:
                score -= 10 + r * 10

    for sq in range(64):
        p = board.pieces[sq]
        if p == '.': continue
        
        score += PIECE_VALUES[p]
        pt = p.lower()
        is_white = p.isupper()
        color_sign = 1 if is_white else -1
        idx = sq if is_white else 63 - sq
        
        if pt in PST:
            score += color_sign * PST[pt][idx]
            
        file = sq % 8
        if pt == 'n':
            score += color_sign * get_mob(board, sq, False, N_WAYS) * 4
        elif pt == 'b':
            score += color_sign * get_mob(board, sq, True, B_WAYS) * 3
            if is_white: w_bishops += 1
            else: b_bishops += 1
        elif pt == 'r':
            score += color_sign * get_mob(board, sq, True, R_WAYS) * 2
            if is_white:
                if not w_pawn_files[file]:
                    score += 15 if b_pawn_files[file] else 25
            else:
                if not b_pawn_files[file]:
                    score -= 15 if w_pawn_files[file] else 25
        elif pt == 'q':
            score += color_sign * get_mob(board, sq, True, R_WAYS + B_WAYS) * 1
        elif pt == 'k':
            if is_white: w_king_sq = sq
            else: b_king_sq = sq
            if endgame:
                score += color_sign * PST_K_EG[idx]
            else:
                score += color_sign * PST_K_MG[idx]
                shield = 0
                for f2 in [file-1, file, file+1]:
                    if 0 <= f2 < 8:
                        if is_white and not w_pawn_files[f2]: shield -= 15
                        if not is_white and not b_pawn_files[f2]: shield += 15
                score += shield
                
    if w_bishops >= 2: score += 30
    if b_bishops >= 2: score -= 30
    
    if endgame:
        if score > 400:
            cmd = max(3 - (b_king_sq//8), b_king_sq//8 - 4) + max(3 - (b_king_sq%8), b_king_sq%8 - 4)
            md = abs(w_king_sq//8 - b_king_sq//8) + abs(w_king_sq%8 - b_king_sq%8)
            score += cmd * 10 + (14 - md) * 4
        elif score < -400:
            cmd = max(3 - (w_king_sq//8), w_king_sq//8 - 4) + max(3 - (w_king_sq%8), w_king_sq%8 - 4)
            md = abs(w_king_sq//8 - b_king_sq//8) + abs(w_king_sq%8 - b_king_sq%8)
            score -= cmd * 10 + (14 - md) * 4
            
    return score
