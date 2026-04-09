# chess-bot-cusec

A Python chess bot built from scratch for a chess bot competition.

This project does **not** use any premade chess engine or chess library.  
It supports FEN board states, UCI move notation, legal move generation, search, evaluation, opening knowledge, and draw detection.

## Features

- Load a position from **FEN**
- Export the current position to **FEN**
- Accept moves in **UCI** notation
- Return moves in **UCI** notation
- Full legal move generation for standard chess rules:
  - normal moves
  - castling
  - en passant
  - promotion
  - self-check prevention
- Search-based move selection with:
  - minimax
  - alpha-beta pruning
  - iterative deepening
  - quiescence search
  - transposition table
  - move ordering
  - killer move heuristic
  - history heuristic
- Handcrafted positional evaluation with:
  - material values
  - piece-square tables
  - mobility
  - doubled / isolated / passed pawns
  - bishop pair bonus
  - rook open / semi-open file bonuses
  - king safety
  - endgame mop-up bonus
- Small handcrafted **opening book**
- Draw detection:
  - threefold repetition
  - 50-move rule
  - insufficient material
  - stalemate
- Terminal play mode

## Project Structure

- `chess_bot.py` — public bot API
- `board.py` — board state, FEN parsing/serialization, make/unmake move logic, draw tracking
- `move_generation.py` — pseudo-legal and legal move generation, attack detection, check detection
- `evaluation.py` — handcrafted position evaluation
- `search.py` — iterative deepening alpha-beta search, quiescence, transposition table, move ordering
- `opening_book.py` — handcrafted opening repertoire
- `play_terminal.py` — terminal interface to play against the bot
- `tests.py` — unit tests

## Public API

The bot exposes this interface:

- `ChessBot(fen=START_FEN)`
- `to_fen()`
- `update(uci_move)`
- `move(depth=2, time_limit=None)`
- `__call__()` → returns current FEN

## Example Usage

```python
from chess_bot import ChessBot

bot = ChessBot()

print(bot())              # current position in FEN
print(bot.to_fen())       # same as above

move = bot.move(depth=4)  # get a move in UCI format
print(move)

bot.update(move)          # apply the move
print(bot())              # updated FEN
