from board import Board

PIECE_VALUES = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
    'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000,
}

PST = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
   10, 10, 20, 30, 30, 20, 10, 10,
   50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0
]

def evaluate(board):
    score = 0
    for sq in range(64):
        p = board.pieces[sq]
        if p != '.':
            score += PIECE_VALUES[p]
            if p == 'P':
                score += PST[sq]
            elif p == 'p':
                score -= PST[63 - sq]
            elif p == 'N':
                score += PST[sq] // 2
            elif p == 'n':
                score -= PST[63 - sq] // 2
    return score
