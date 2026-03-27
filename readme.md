# chess-bot-cusec

A Python chess bot built from scratch for a chess bot competition.

It does not use any premade chess engine or chess library. The bot supports FEN board states, UCI move notation, legal move generation, and a basic search algorithm to choose moves.

## Features

- Load a chess position from FEN
- Export the current position to FEN
- Accept moves in UCI notation
- Generate legal moves in UCI notation
- Handle standard chess rules:
  - normal legal moves
  - castling
  - en passant
  - promotion
  - check / self-check prevention
  - checkmate / stalemate detection
- Basic minimax search with alpha-beta pruning

## Project Structure

- `chess_bot.py` — public API
- `board.py` — board state, FEN parsing/serialization, move application
- `move_generation.py` — legal move generation and attack detection
- `evaluation.py` — position evaluation
- `search.py` — minimax and alpha-beta pruning
- `tests.py` — test suite

## Public API

The bot exposes this interface:

- `ChessBot(fen=START_FEN)`
- `to_fen()`
- `update(uci_move)`
- `move()`
- `__call__()` → returns current FEN

## Example Usage

```python
from chess_bot import ChessBot

bot = ChessBot()

print(bot())          # current position in FEN
print(bot.to_fen())   # same as above

m = bot.move()        # get one legal move in UCI format
print(m)

bot.update(m)         # apply that move
print(bot())          # updated FEN