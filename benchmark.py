import sys
import time
from chess_bot import ChessBot

BOOK_OR_EASY = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
]

NON_BOOK_SEARCH = [
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
    "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - - 0 1",
    "3r2k1/p4p1p/1p4p1/3q4/3P1Q2/8/PP3PPP/4R1K1 w - - 0 1",
    "r2q1rk1/1pp1bppp/p1n2n2/3p1b2/3P4/PQN1PN2/1P1B1PPP/R3KB1R w KQ - 0 1",
    "8/k7/3p4/p2P1p2/P2P1P2/8/8/K7 w - - 0 1",
    "8/8/5k2/R7/8/P7/8/4K3 w - - 0 1"
]

def run_benchmark():
    depth = 4
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        depth = int(sys.argv[1])
        
    print(f"Running Benchmark at Depth {depth}...")
    print(f"{'Idx':<4} | {'Group':<14} | {'Elapsed (s)':<12} | {'Move':<6} | {'FEN'}")
    print("-" * 100)
    
    total_time = 0
    slowest_time = 0
    slowest_idx = -1
    
    idx = 1
    
    for group_name, fens in [("BOOK_OR_EASY", BOOK_OR_EASY), ("NON_BOOK_SEARCH", NON_BOOK_SEARCH)]:
        for fen in fens:
            bot = ChessBot(fen)
            start = time.perf_counter()
            move = bot.move(depth=depth)
            elapsed = time.perf_counter() - start
            
            if group_name == "NON_BOOK_SEARCH":
                total_time += elapsed
                if elapsed > slowest_time:
                    slowest_time = elapsed
                    slowest_idx = idx
            
            move_str = move if move else "None"
            print(f"{idx:<4} | {group_name:<14} | {elapsed:<12.3f} | {move_str:<6} | {fen}")
            idx += 1
            
    print("-" * 100)
    if NON_BOOK_SEARCH:
        avg_time = total_time / len(NON_BOOK_SEARCH)
        print("Summary for NON_BOOK_SEARCH:")
        print(f"Total Time : {total_time:.3f}s")
        print(f"Avg Time   : {avg_time:.3f}s")
        print(f"Slowest    : Idx {slowest_idx} ({slowest_time:.3f}s)")

if __name__ == "__main__":
    run_benchmark()
