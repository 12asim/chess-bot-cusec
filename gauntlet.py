import time
from chess_bot import ChessBot
from move_generation import get_legal_moves, is_in_check

def play_match(depth_w, depth_b, max_plies=150):
    bot_w = ChessBot()
    bot_b = ChessBot()
    
    ply_count = 0
    result = "Draw by Max Plies"
    
    while ply_count < max_plies:
        board = bot_w.board if bot_w.board.turn == 'w' else bot_b.board
        turn = board.turn
        
        # Check static draw conditions
        if board.is_draw_by_repetition():
            result = "Draw by Repetition"
            break
        if board.is_draw_by_50_move():
            result = "Draw by 50-move rule"
            break
        if board.is_insufficient_material():
            result = "Draw by Insufficient Material"
            break
            
        legal_moves = get_legal_moves(board)
        if not legal_moves:
            if is_in_check(board, turn):
                result = "1-0" if turn == 'b' else "0-1"
            else:
                result = "1/2-1/2 (Stalemate)"
            break
            
        if turn == 'w':
            move = bot_w.move(depth=depth_w)
        else:
            move = bot_b.move(depth=depth_b)
            
        if not move:
            result = "Error: No move returned"
            break
            
        bot_w.update(move)
        bot_b.update(move)
        ply_count += 1
        
    final_fen = bot_w.to_fen()
    return f"Depth {depth_w} vs Depth {depth_b}", result, final_fen, ply_count

import sys

def run_gauntlet():
    games_per_matchup = 2
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        games_per_matchup = int(sys.argv[1])

    matchups = [
        (3, 4),
        (4, 5)
    ]
    
    print(f"Running Gauntlet ({games_per_matchup} paired games per matchup)...")
    scores = {}
    
    for dw, db in matchups:
        scores[(dw, db)] = {'wins1': 0, 'wins2': 0, 'draws': 0}
        
        for g in range(games_per_matchup):
            m1, res1, fen1, plies1 = play_match(dw, db)
            print(f"Game {g*2+1}: {m1:<20} | {res1:<20} | {plies1} plies")
            if res1 == "1-0": scores[(dw, db)]['wins1'] += 1
            elif res1 == "0-1": scores[(dw, db)]['wins2'] += 1
            else: scores[(dw, db)]['draws'] += 1
            
            m2, res2, fen2, plies2 = play_match(db, dw)
            print(f"Game {g*2+2}: {m2:<20} | {res2:<20} | {plies2} plies")
            if res2 == "1-0": scores[(dw, db)]['wins2'] += 1
            elif res2 == "0-1": scores[(dw, db)]['wins1'] += 1
            else: scores[(dw, db)]['draws'] += 1
            
        print("-" * 40)

    print("\nGauntlet Summary:")
    print(f"{'Matchup':<15} | {'W/L/D for first depth'}")
    print("-" * 40)
    for (d1, d2), sc in scores.items():
        print(f"Depth {d1} vs {d2:<2} | +{sc['wins1']} -{sc['wins2']} ={sc['draws']}")

if __name__ == "__main__":
    run_gauntlet()
