import time
from chess_bot import ChessBot

FENS = [
    # Opening
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
    # Middlegame
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
    # Tactical
    "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - - 0 1",
    "3r2k1/p4p1p/1p4p1/3q4/3P1Q2/8/PP3PPP/4R1K1 w - - 0 1",
    "r2q1rk1/1pp1bppp/p1n2n2/3p1b2/3P4/PQN1PN2/1P1B1PPP/R3KB1R w KQ - 0 1",
    # Endgame
    "8/k7/3p4/p2P1p2/P2P1P2/8/8/K7 w - - 0 1",
    "8/8/5k2/R7/8/P7/8/4K3 w - - 0 1"
]

def run_benchmark():
    print("Running Benchmark...")
    print(f"{'Idx':<4} | {'Elapsed (s)':<12} | {'Move':<6} | {'FEN'}")
    print("-" * 80)
    
    total_time = 0
    for idx, fen in enumerate(FENS, 1):
        bot = ChessBot(fen)
        start = time.perf_counter()
        move = bot.move(depth=4)
        elapsed = time.perf_counter() - start
        
        total_time += elapsed
        move_str = move if move else "None"
        print(f"{idx:<4} | {elapsed:<12.3f} | {move_str:<6} | {fen}")
        
    avg_time = total_time / len(FENS)
    print("-" * 80)
    print(f"Total Time: {total_time:.3f}s")
    print(f"Average Time / Pos: {avg_time:.3f}s")

if __name__ == "__main__":
    run_benchmark()
