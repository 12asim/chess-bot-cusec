from board import Board

def is_attacked(board, sq, attacker_color):
    row, col = sq // 8, sq % 8
    enemy_pawn = 'p' if attacker_color == 'b' else 'P'
    enemy_knight = 'n' if attacker_color == 'b' else 'N'
    enemy_bishop = 'b' if attacker_color == 'b' else 'B'
    enemy_rook = 'r' if attacker_color == 'b' else 'R'
    enemy_queen = 'q' if attacker_color == 'b' else 'Q'
    enemy_king = 'k' if attacker_color == 'b' else 'K'
    
    if attacker_color == 'w':
        p_attacks = [(row+1, col-1), (row+1, col+1)]
    else:
        p_attacks = [(row-1, col-1), (row-1, col+1)]
        
    for r, c in p_attacks:
        if 0 <= r < 8 and 0 <= c < 8 and board.pieces[r*8+c] == enemy_pawn:
            return True

    for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
        r, c = row+dr, col+dc
        if 0 <= r < 8 and 0 <= c < 8 and board.pieces[r*8+c] == enemy_knight:
            return True
            
    rays = [
        (0, 1, [enemy_rook, enemy_queen]), (0, -1, [enemy_rook, enemy_queen]),
        (1, 0, [enemy_rook, enemy_queen]), (-1, 0, [enemy_rook, enemy_queen]),
        (1, 1, [enemy_bishop, enemy_queen]), (1, -1, [enemy_bishop, enemy_queen]),
        (-1, 1, [enemy_bishop, enemy_queen]), (-1, -1, [enemy_bishop, enemy_queen]),
    ]
    for dr, dc, pieces in rays:
        r, c = row+dr, col+dc
        while 0 <= r < 8 and 0 <= c < 8:
            p = board.pieces[r*8+c]
            if p != '.':
                if p in pieces: return True
                break
            r += dr
            c += dc

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            r, c = row+dr, col+dc
            if 0 <= r < 8 and 0 <= c < 8 and board.pieces[r*8+c] == enemy_king:
                return True
                
    return False

def is_in_check(board, color):
    k_char = 'K' if color == 'w' else 'k'
    try:
        k_pos = board.pieces.index(k_char)
    except ValueError:
        return False
    return is_attacked(board, k_pos, 'b' if color == 'w' else 'w')

def get_pseudo_legal_moves(board):
    moves = []
    us = board.turn
    
    for sq in range(64):
        p = board.pieces[sq]
        if p == '.': continue
        if (us == 'w' and p.islower()) or (us == 'b' and p.isupper()):
            continue
            
        row, col = sq // 8, sq % 8
        
        if p.lower() == 'p':
            dir = -1 if us == 'w' else 1
            start_rank = 6 if us == 'w' else 1
            promo_rank = 0 if us == 'w' else 7
            
            fwd = sq + dir * 8
            if 0 <= fwd < 64 and board.pieces[fwd] == '.':
                if fwd // 8 == promo_rank:
                    for pr in ['q', 'r', 'b', 'n']:
                        moves.append((sq, fwd, pr.upper() if us == 'w' else pr))
                else:
                    moves.append((sq, fwd, None))
                    if row == start_rank:
                        fwd2 = fwd + dir * 8
                        if board.pieces[fwd2] == '.':
                            moves.append((sq, fwd2, None))
                            
            for dc in [-1, 1]:
                if 0 <= col + dc < 8:
                    cap_sq = sq + dir * 8 + dc
                    if 0 <= cap_sq < 64:
                        target = board.pieces[cap_sq]
                        if target != '.' and ((us == 'w' and target.islower()) or (us == 'b' and target.isupper())):
                            if cap_sq // 8 == promo_rank:
                                for pr in ['q', 'r', 'b', 'n']:
                                    moves.append((sq, cap_sq, pr.upper() if us == 'w' else pr))
                            else:
                                moves.append((sq, cap_sq, None))
                        elif cap_sq == board.ep_square:
                            moves.append((sq, cap_sq, None))
                            
        elif p.lower() == 'n':
            for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
                r, c = row+dr, col+dc
                if 0 <= r < 8 and 0 <= c < 8:
                    cap_sq = r * 8 + c
                    target_p = board.pieces[cap_sq]
                    if target_p == '.' or ((us == 'w' and target_p.islower()) or (us == 'b' and target_p.isupper())):
                        moves.append((sq, cap_sq, None))
                        
        elif p.lower() in ['b', 'r', 'q', 'k']:
            if p.lower() == 'b': rays = [(1,1), (1,-1), (-1,1), (-1,-1)]
            elif p.lower() == 'r': rays = [(0,1), (0,-1), (1,0), (-1,0)]
            elif p.lower() == 'q': rays = [(1,1), (1,-1), (-1,1), (-1,-1), (0,1), (0,-1), (1,0), (-1,0)]
            elif p.lower() == 'k': rays = [(1,1), (1,-1), (-1,1), (-1,-1), (0,1), (0,-1), (1,0), (-1,0)]
            
            for dr, dc in rays:
                r, c = row+dr, col+dc
                while 0 <= r < 8 and 0 <= c < 8:
                    cap_sq = r * 8 + c
                    target_p = board.pieces[cap_sq]
                    if target_p == '.':
                        moves.append((sq, cap_sq, None))
                    elif (us == 'w' and target_p.islower()) or (us == 'b' and target_p.isupper()):
                        moves.append((sq, cap_sq, None))
                        break
                    else:
                        break
                    if p.lower() == 'k': break
                    r += dr
                    c += dc
                    
        if p.lower() == 'k':
            if us == 'w':
                if 'K' in board.castling and board.pieces[61] == '.' and board.pieces[62] == '.':
                    if not is_attacked(board, 60, 'b') and not is_attacked(board, 61, 'b') and not is_attacked(board, 62, 'b'):
                        moves.append((60, 62, None))
                if 'Q' in board.castling and board.pieces[59] == '.' and board.pieces[58] == '.' and board.pieces[57] == '.':
                    if not is_attacked(board, 60, 'b') and not is_attacked(board, 59, 'b') and not is_attacked(board, 58, 'b'):
                        moves.append((60, 58, None))
            else:
                if 'k' in board.castling and board.pieces[5] == '.' and board.pieces[6] == '.':
                    if not is_attacked(board, 4, 'w') and not is_attacked(board, 5, 'w') and not is_attacked(board, 6, 'w'):
                        moves.append((4, 6, None))
                if 'q' in board.castling and board.pieces[3] == '.' and board.pieces[2] == '.' and board.pieces[1] == '.':
                    if not is_attacked(board, 4, 'w') and not is_attacked(board, 3, 'w') and not is_attacked(board, 2, 'w'):
                        moves.append((4, 2, None))

    return moves

def get_legal_moves(board):
    moves = get_pseudo_legal_moves(board)
    legals = []
    curr_turn = board.turn
    for m in moves:
        b2 = board.copy()
        b2.apply_move(m)
        if not is_in_check(b2, curr_turn):
            legals.append(m)
    return legals
