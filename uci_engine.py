import sys
from chess_bot import ChessBot, START_FEN

def main():
    bot = ChessBot()
    
    while True:
        try:
            line = sys.stdin.readline()
        except EOFError:
            break
            
        if not line:
            break
            
        line = line.strip()
        if not line:
            continue
            
        tokens = line.split()
        command = tokens[0].lower()
        
        if command == "uci":
            print("id name Python Chess Bot")
            print("id author Asim Shirinov")
            print("uciok")
            sys.stdout.flush()
            
        elif command == "isready":
            print("readyok")
            sys.stdout.flush()
            
        elif command == "ucinewgame":
            bot = ChessBot()
            
        elif command == "position":
            idx = 1
            if idx < len(tokens) and tokens[idx] == "startpos":
                bot = ChessBot(START_FEN)
                idx += 1
            elif idx < len(tokens) and tokens[idx] == "fen":
                idx += 1
                fen_parts = []
                while idx < len(tokens) and tokens[idx] != "moves":
                    fen_parts.append(tokens[idx])
                    idx += 1
                fen = " ".join(fen_parts)
                bot = ChessBot(fen)
                
            if idx < len(tokens) and tokens[idx] == "moves":
                idx += 1
                for m in tokens[idx:]:
                    try:
                        bot.update(m)
                    except ValueError:
                        # Stop applying further moves immediately to prevent state desync
                        break
                        
        elif command == "go":
            depth = None
            movetime = None
            
            for i in range(1, len(tokens)):
                if tokens[i] == "depth" and i + 1 < len(tokens):
                    try:
                        depth = int(tokens[i + 1])
                    except ValueError:
                        pass
                elif tokens[i] == "movetime" and i + 1 < len(tokens):
                    try:
                        movetime = float(tokens[i + 1]) / 1000.0
                    except ValueError:
                        pass
                        
            if movetime is not None:
                best_move = bot.move(time_limit=movetime)
            elif depth is not None:
                best_move = bot.move(depth=depth)
            else:
                # Default fallback if neither depth nor movetime is specified
                best_move = bot.move(depth=4)
                
            if best_move:
                print(f"bestmove {best_move}")
            else:
                print("bestmove 0000")
            sys.stdout.flush()
            
        elif command == "quit":
            break

if __name__ == "__main__":
    main()
