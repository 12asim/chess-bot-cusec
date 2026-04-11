from chess_bot import ChessBot
from move_generation import get_legal_moves, is_in_check
import time

def print_board(board):
    print()
    for rank in range(8):
        row_label = 8 - rank
        row = board.pieces[rank * 8:(rank + 1) * 8]
        print(f"{row_label} " + " ".join(row))
    print("  a b c d e f g h")
    print()

def game_over_message(bot):
    if bot.board.is_draw_by_repetition():
        return "Draw by repetition."
    if bot.board.is_draw_by_50_move():
        return "Draw by 50-move rule."
    if bot.board.is_insufficient_material():
        return "Draw by insufficient material."

    legal_moves = get_legal_moves(bot.board)
    if legal_moves:
        return None

    if is_in_check(bot.board, bot.board.turn):
        winner = "Black" if bot.board.turn == "w" else "White"
        return f"Checkmate. {winner} wins."
    return "Stalemate."

def main():
    print("Python Chess Bot Terminal")
    print("Enter moves in UCI format like e2e4, g1f3, g7g8q")
    print("Commands: board, fen, legal, undo, undo1, quit")
    print()

    side = input("Play as white or black? (w/b): ").strip().lower()
    if side not in ("w", "b"):
        side = "w"

    clock_text = input("Game clock in seconds (leave empty for depth-based): ").strip()
    clock = None
    if clock_text:
        try:
            clock = float(clock_text)
        except ValueError:
            print("Invalid clock input, falling back to depth mode.")
            clock = None
            
    if clock is not None:
        increment_text = input("Increment in seconds (default 0): ").strip()
        increment = 0.0
        if increment_text:
            try:
                increment = float(increment_text)
            except ValueError:
                print("Invalid increment input, using 0.0.")
                increment = 0.0
        depth = 2
    else:
        depth_text = input("Bot search depth (default 2): ").strip()
        depth = 2
        if depth_text:
            try:
                depth = int(depth_text)
                if depth <= 0:
                    print("Invalid depth input, using default 2.")
                    depth = 2
            except ValueError:
                print("Invalid depth input, using default 2.")
                depth = 2
        increment = 0.0

    bot = ChessBot()
    clock_states = [clock]

    while True:
        print_board(bot.board)
        print("FEN:", bot.to_fen())

        result = game_over_message(bot)
        if result:
            print(result)
            break

        if bot.board.turn == side:
            user_input = input("Your move: ").strip().lower()

            if user_input == "quit":
                print("Goodbye.")
                break
            elif user_input == "board":
                continue
            elif user_input == "fen":
                print(bot.to_fen())
                continue
            elif user_input == "legal":
                legal_moves = get_legal_moves(bot.board)
                legal_uci = []
                for start, end, promo in legal_moves:
                    move = bot.board.square_to_str(start) + bot.board.square_to_str(end)
                    if promo:
                        move += promo.lower()
                    legal_uci.append(move)
                print("Legal moves:", " ".join(legal_uci))
                continue
            elif user_input == "undo":
                if len(bot.move_history) >= 2:
                    bot.undo_last_move()
                    bot.undo_last_move()
                    clock_states.pop()
                    clock_states.pop()
                    clock = clock_states[-1]
                elif len(bot.move_history) == 1:
                    bot.undo_last_move()
                    clock_states.pop()
                    clock = clock_states[-1]
                else:
                    print("Nothing to undo.")
                continue
            elif user_input == "undo1":
                if len(bot.move_history) >= 1:
                    bot.undo_last_move()
                    clock_states.pop()
                    clock = clock_states[-1]
                else:
                    print("Nothing to undo.")
                continue

            try:
                bot.update(user_input)
                clock_states.append(clock)
            except Exception as e:
                print("Invalid move:", e)
        else:
            if clock is not None:
                allocated = bot.choose_time_limit(clock, increment)
                print(f"Bot thinking for up to {allocated:.2f}s... (Clock: {clock:.2f}s)")
                t0 = time.time()
                bot_move = bot.move(time_limit=allocated)
                elapsed = time.time() - t0
                clock -= elapsed
                clock += increment
                if clock <= 0:
                    print("Bot ran out of time! You win on time.")
                    break
            else:
                bot_move = bot.move(depth=depth)

            if bot_move is None:
                result = game_over_message(bot)
                print(result if result else "No legal moves.")
                break
            print(f"Bot plays: {bot_move}")
            bot.update(bot_move)
            clock_states.append(clock)

if __name__ == "__main__":
    main()