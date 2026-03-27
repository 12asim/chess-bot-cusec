from chess_bot import ChessBot
from move_generation import get_legal_moves, is_in_check

def print_board(board):
    print()
    for rank in range(8):
        row_label = 8 - rank
        row = board.pieces[rank * 8:(rank + 1) * 8]
        print(f"{row_label} " + " ".join(row))
    print("  a b c d e f g h")
    print()

def game_over_message(bot):
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
    print("Commands: board, fen, legal, quit")
    print()

    side = input("Play as white or black? (w/b): ").strip().lower()
    if side not in ("w", "b"):
        side = "w"

    depth_text = input("Bot search depth (default 2): ").strip()
    depth = int(depth_text) if depth_text.isdigit() and int(depth_text) > 0 else 2

    bot = ChessBot()

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

            try:
                bot.update(user_input)
            except Exception as e:
                print("Invalid move:", e)
        else:
            bot_move = bot.move(depth=depth)
            if bot_move is None:
                result = game_over_message(bot)
                print(result if result else "No legal moves.")
                break
            print(f"Bot plays: {bot_move}")
            bot.update(bot_move)

if __name__ == "__main__":
    main()