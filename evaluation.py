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

def get_attacks(board):
    w_att = [0] * 64
    b_att = [0] * 64
    for p, sqs in board.piece_lists.items():
        is_w = p.isupper()
        att = w_att if is_w else b_att
        pt = p.lower()
        for sq in sqs:
            r, c = sq // 8, sq % 8
            if pt == 'p':
                dr = -1 if is_w else 1
                if 0 <= r + dr < 8:
                    if c > 0: att[(r+dr)*8 + c-1] += 1
                    if c < 7: att[(r+dr)*8 + c+1] += 1
            elif pt == 'n':
                for dr, dc in N_WAYS:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < 8 and 0 <= nc < 8: att[nr*8 + nc] += 1
            elif pt == 'k':
                for dr, dc in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < 8 and 0 <= nc < 8: att[nr*8 + nc] += 1
            else:
                ways = []
                if pt in ['b', 'q']: ways.extend(B_WAYS)
                if pt in ['r', 'q']: ways.extend(R_WAYS)
                for dr, dc in ways:
                    nr, nc = r+dr, c+dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        att[nr*8 + nc] += 1
                        if board.pieces[nr*8 + nc] != '.': break
                        nr += dr; nc += dc
    return w_att, b_att

def evaluate(board):
    w_att, b_att = get_attacks(board)
    mg_score = 0
    eg_score = 0
    w_pawn_files = {f: [] for f in range(8)}
    b_pawn_files = {f: [] for f in range(8)}
    w_pawn_sq_color = [0, 0]
    b_pawn_sq_color = [0, 0]
    
    phase = 0
    w_king_sq = -1
    b_king_sq = -1
    
    for p, sqs in board.piece_lists.items():
        pt = p.lower()
        if pt in ['n', 'b']: phase += len(sqs)
        elif pt == 'r': phase += 2 * len(sqs)
        elif pt == 'q': phase += 4 * len(sqs)
        
        for sq in sqs:
            file = sq % 8
            rank = sq // 8
            if p == 'P': 
                w_pawn_files[file].append(rank)
                w_pawn_sq_color[(rank + file) % 2] += 1
            elif p == 'p': 
                b_pawn_files[file].append(rank)
                b_pawn_sq_color[(rank + file) % 2] += 1
            elif p == 'K': w_king_sq = sq
            elif p == 'k': b_king_sq = sq

    phase = min(24, phase)

    w_bishops = 0
    b_bishops = 0
    
    w_passed = []
    b_passed = []
    
    # Pawn structure
    for f in range(8):
        wp = w_pawn_files[f]
        bp = b_pawn_files[f]
        
        if len(wp) > 1: 
            mg_score -= 20 * (len(wp) - 1)
            eg_score -= 20 * (len(wp) - 1)
        if len(bp) > 1: 
            mg_score += 20 * (len(bp) - 1)
            eg_score += 20 * (len(bp) - 1)
        
        w_adj = (w_pawn_files[f-1] if f > 0 else []) + (w_pawn_files[f+1] if f < 7 else [])
        if wp and not w_adj: 
            mg_score -= 20 * len(wp)
            eg_score -= 20 * len(wp)
        
        b_adj = (b_pawn_files[f-1] if f > 0 else []) + (b_pawn_files[f+1] if f < 7 else [])
        if bp and not b_adj: 
            mg_score += 20 * len(bp)
            eg_score += 20 * len(bp)
        
        for r in wp:
            if not [br for br in bp + b_adj if br < r]:
                w_passed.append((r, f))
                adv = 7 - r
                mg_score += 10 + adv * 10
                eg_score += 10 + adv * 30 + (adv * adv * 2)
                
                outside = abs(f - 3.5)
                eg_score += int(outside * 15)
                
                has_support = False
                if f > 0:
                    for adj_r in w_pawn_files[f-1]:
                        if abs(adj_r - r) <= 1: has_support = True
                if f < 7:
                    for adj_r in w_pawn_files[f+1]:
                        if abs(adj_r - r) <= 1: has_support = True
                if has_support:
                    mg_score += 15
                    eg_score += 50
        for r in bp:
            if not [wr for wr in wp + w_adj if wr > r]:
                b_passed.append((r, f))
                adv = r
                mg_score -= 10 + adv * 10
                eg_score -= 10 + adv * 30 + (adv * adv * 2)
                
                outside = abs(f - 3.5)
                eg_score -= int(outside * 15)
                
                has_support = False
                if f > 0:
                    for adj_r in b_pawn_files[f-1]:
                        if abs(adj_r - r) <= 1: has_support = True
                if f < 7:
                    for adj_r in b_pawn_files[f+1]:
                        if abs(adj_r - r) <= 1: has_support = True
                if has_support:
                    mg_score -= 15
                    eg_score -= 50

    if w_king_sq != -1:
        w_king_r, w_king_f = w_king_sq // 8, w_king_sq % 8
        for pr, pf in w_passed:
            dist = max(abs(w_king_r - pr), abs(w_king_f - pf))
            eg_score += (7 - dist) * 5
        for pr, pf in b_passed:
            dist = max(abs(w_king_r - pr), abs(w_king_f - pf))
            eg_score += (7 - dist) * 8

    if b_king_sq != -1:
        b_king_r, b_king_f = b_king_sq // 8, b_king_sq % 8
        for pr, pf in b_passed:
            dist = max(abs(b_king_r - pr), abs(b_king_f - pf))
            eg_score -= (7 - dist) * 5
        for pr, pf in w_passed:
            dist = max(abs(b_king_r - pr), abs(b_king_f - pf))
            eg_score -= (7 - dist) * 8

    w_space = 0
    b_space = 0

    for sq in range(64):
        file = sq % 8
        if 2 <= file <= 5: 
            rank = sq // 8
            if rank <= 3:
                if w_att[sq] > 0 and b_att[sq] == 0: w_space += 2
                elif w_att[sq] > 0: w_space += 1
            elif rank >= 4:
                if b_att[sq] > 0 and w_att[sq] == 0: b_space += 2
                elif b_att[sq] > 0: b_space += 1

    for p, sqs in board.piece_lists.items():
        val = PIECE_VALUES[p]
        pt = p.lower()
        is_white = p.isupper()
        color_sign = 1 if is_white else -1
        val_abs = abs(val)
        
        for sq in sqs:
            file = sq % 8
            rank = sq // 8
            
            mg_score += val
            eg_score += val
            
            idx = sq if is_white else 63 - sq
            
            if pt != 'k':
                if is_white:
                    if b_att[sq] > 0:
                        if w_att[sq] == 0:
                            mg_score -= val_abs // 10
                            eg_score -= val_abs // 10
                        elif val_abs > 100:
                            mg_score -= 10
                            eg_score -= 10
                else:
                    if w_att[sq] > 0:
                        if b_att[sq] == 0:
                            mg_score += val_abs // 10
                            eg_score += val_abs // 10
                        elif val_abs > 100:
                            mg_score += 10
                            eg_score += 10
            
            if pt in PST:
                pst_val = PST[pt][idx]
                mg_score += color_sign * pst_val
                eg_score += color_sign * pst_val
                
            if pt == 'n':
                mob = get_mob(board, sq, False, N_WAYS) * 4
                mg_score += color_sign * mob
                eg_score += color_sign * mob
                
                if is_white:
                    r_front = rank + 1
                    supported = (file > 0 and r_front in w_pawn_files[file-1]) or (file < 7 and r_front in w_pawn_files[file+1])
                    if supported:
                        mg_score += 15
                        eg_score += 5
                        safe = True
                        if file > 0 and any(br < rank for br in b_pawn_files[file-1]): safe = False
                        if file < 7 and any(br < rank for br in b_pawn_files[file+1]): safe = False
                        if safe:
                            mg_score += 20
                            eg_score += 10
                else:
                    r_front = rank - 1
                    supported = (file > 0 and r_front in b_pawn_files[file-1]) or (file < 7 and r_front in b_pawn_files[file+1])
                    if supported:
                        mg_score -= 15
                        eg_score -= 5
                        safe = True
                        if file > 0 and any(wr > rank for wr in w_pawn_files[file-1]): safe = False
                        if file < 7 and any(wr > rank for wr in w_pawn_files[file+1]): safe = False
                        if safe:
                            mg_score -= 20
                            eg_score -= 10
            elif pt == 'b':
                mob = get_mob(board, sq, True, B_WAYS) * 3
                mg_score += color_sign * mob
                eg_score += color_sign * mob
                
                sq_color = (rank + file) % 2
                if is_white:
                    w_bishops += 1
                    blocked_cnt = w_pawn_sq_color[sq_color]
                    mg_score -= blocked_cnt * 3
                    eg_score -= blocked_cnt * 4
                else:
                    b_bishops += 1
                    blocked_cnt = b_pawn_sq_color[sq_color]
                    mg_score += blocked_cnt * 3
                    eg_score += blocked_cnt * 4
            elif pt == 'r':
                mob = get_mob(board, sq, True, R_WAYS) * 2
                mg_score += color_sign * mob
                eg_score += color_sign * mob
                if is_white:
                    if not w_pawn_files[file]:
                        mg_score += 20 if b_pawn_files[file] else 35
                        eg_score += 10 if b_pawn_files[file] else 15
                    if rank == 1:
                        if b_king_sq // 8 <= 1 or any(1 in b_pawn_files[f] for f in range(8)) or any(2 in b_pawn_files[f] for f in range(8)):
                            mg_score += 20
                            eg_score += 25
                    if any(pr < rank for pr, pf in w_passed if pf == file):
                        eg_score += 25
                    if any(pr > rank for pr, pf in b_passed if pf == file):
                        eg_score += 25
                else:
                    if not b_pawn_files[file]:
                        mg_score -= 20 if w_pawn_files[file] else 35
                        eg_score -= 10 if w_pawn_files[file] else 15
                    if rank == 6:
                        if w_king_sq // 8 >= 6 or any(6 in w_pawn_files[f] for f in range(8)) or any(5 in w_pawn_files[f] for f in range(8)):
                            mg_score -= 20
                            eg_score -= 25
                    if any(pr > rank for pr, pf in b_passed if pf == file):
                        eg_score -= 25
                    if any(pr < rank for pr, pf in w_passed if pf == file):
                        eg_score -= 25
            elif pt == 'q':
                mob = get_mob(board, sq, True, R_WAYS + B_WAYS) * 1
                mg_score += color_sign * mob
                eg_score += color_sign * mob
            elif pt == 'k':
                mg_score += color_sign * PST_K_MG[idx]
                eg_score += color_sign * PST_K_EG[idx]
                
                shield = 0
                for f2 in [file-1, file, file+1]:
                    if 0 <= f2 < 8:
                        if is_white and not w_pawn_files[f2]: shield -= 20
                        if not is_white and not b_pawn_files[f2]: shield += 20
                
                mg_score += shield
    
                kz_attacks = 0
                for dr, dc in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1), (0,0)]:
                    nr, nc = rank+dr, file+dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if is_white: kz_attacks += b_att[nr*8 + nc]
                        else: kz_attacks += w_att[nr*8 + nc]
                
                if is_white: mg_score -= kz_attacks * 5
                else: mg_score += kz_attacks * 5
                
    mg_score += w_space * 2
    mg_score -= b_space * 2

    total_pawns = sum(len(f) for f in w_pawn_files.values()) + sum(len(f) for f in b_pawn_files.values())
    w_bp_bonus = max(15, 45 - total_pawns * 2)
    b_bp_bonus = max(15, 45 - total_pawns * 2)

    if w_bishops >= 2: 
        mg_score += w_bp_bonus
        eg_score += 50
    if b_bishops >= 2: 
        mg_score -= b_bp_bonus
        eg_score -= 50
    
    score = (mg_score * phase + eg_score * (24 - phase)) // 24
    
    if phase <= 6:
        if score > 400:
            cmd = max(3 - (b_king_sq//8), b_king_sq//8 - 4) + max(3 - (b_king_sq%8), b_king_sq%8 - 4)
            md = abs(w_king_sq//8 - b_king_sq//8) + abs(w_king_sq%8 - b_king_sq%8)
            score += cmd * 10 + (14 - md) * 4
        elif score < -400:
            cmd = max(3 - (w_king_sq//8), w_king_sq//8 - 4) + max(3 - (w_king_sq%8), w_king_sq%8 - 4)
            md = abs(w_king_sq//8 - b_king_sq//8) + abs(w_king_sq%8 - b_king_sq%8)
            score -= cmd * 10 + (14 - md) * 4
            
    return score
