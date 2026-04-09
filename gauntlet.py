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

def run_gauntlet():
    matchups = [
        (3, 4),
        (4, 5)
    ]
    
    print("Running Gauntlet...")
    for dw, db in matchups:
        matchup, result, fen, plies = play_match(dw, db)
        print(f"Matchup: {matchup}")
        print(f"Result : {result}")
        print(f"Plies  : {plies}")
        print(f"FEN    : {fen}")
        print("-" * 40)

if __name__ == "__main__":
    run_gauntlet()
