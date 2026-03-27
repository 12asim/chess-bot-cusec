START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class Board:
    def __init__(self, fen=START_FEN):
        self.pieces = ['.'] * 64
        self.turn = 'w'
        self.castling = "-"
        self.ep_square = -1
        self.halfmove = 0
        self.fullmove = 1
        self.load_fen(fen)

    def load_fen(self, fen):
        parts = fen.split()
        if len(parts) != 6:
            raise ValueError("Invalid FEN string")

        board_part, turn_part, castling_part, ep_part, half_part, full_part = parts
        
        # Parse board
        index = 0
        for char in board_part:
            if char == '/':
                continue
            elif char.isdigit():
                index += int(char)
            else:
                self.pieces[index] = char
                index += 1
                
        self.turn = turn_part
        self.castling = castling_part
        
        self.ep_square = -1
        if ep_part != '-':
            self.ep_square = self.square_from_str(ep_part)
            
        self.halfmove = int(half_part)
        self.fullmove = int(full_part)

    def to_fen(self):
        fen_board = []
        for rank in range(8):
            empty_count = 0
            for file in range(8):
                idx = rank * 8 + file
                piece = self.pieces[idx]
                if piece == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_board.append(str(empty_count))
                        empty_count = 0
                    fen_board.append(piece)
            if empty_count > 0:
                fen_board.append(str(empty_count))
            if rank < 7:
                fen_board.append('/')
                
        board_str = "".join(fen_board)
        ep_str = self.square_to_str(self.ep_square) if self.ep_square != -1 else "-"
        return f"{board_str} {self.turn} {self.castling} {ep_str} {self.halfmove} {self.fullmove}"

    @staticmethod
    def square_from_str(s):
        file = ord(s[0]) - ord('a')
        rank = 8 - int(s[1])
        return rank * 8 + file

    @staticmethod
    def square_to_str(idx):
        if idx == -1:
            return "-"
        file = idx % 8
        rank = 8 - (idx // 8)
        return f"{chr(file + ord('a'))}{rank}"

    def copy(self):
        new_board = Board.__new__(Board)
        new_board.pieces = self.pieces[:]
        new_board.turn = self.turn
        new_board.castling = self.castling
        new_board.ep_square = self.ep_square
        new_board.halfmove = self.halfmove
        new_board.fullmove = self.fullmove
        return new_board

    def apply_move(self, move_tuple):
        start, end, promo = move_tuple
        piece = self.pieces[start]
        captured = self.pieces[end]
        
        # Prevent completely invalid calls
        if piece == '.': return
        
        if piece.lower() == 'p' or captured != '.':
            self.halfmove = 0
        else:
            self.halfmove += 1
            
        if piece.lower() == 'p' and end == self.ep_square:
            if piece == 'P':
                self.pieces[end + 8] = '.'
            else:
                self.pieces[end - 8] = '.'
                
        self.pieces[end] = self.pieces[start]
        self.pieces[start] = '.'
        if promo:
            self.pieces[end] = promo
            
        if piece.lower() == 'k' and abs(start - end) == 2:
            if end == 62:
                self.pieces[61] = self.pieces[63]
                self.pieces[63] = '.'
            elif end == 58:
                self.pieces[59] = self.pieces[56]
                self.pieces[56] = '.'
            elif end == 6:
                self.pieces[5] = self.pieces[7]
                self.pieces[7] = '.'
            elif end == 2:
                self.pieces[3] = self.pieces[0]
                self.pieces[0] = '.'
        
        self.ep_square = -1
        if piece.lower() == 'p' and abs(start - end) == 16:
            self.ep_square = (start + end) // 2
            
        if start == 60 or end == 60: self.castling = self.castling.replace('K', '').replace('Q', '')
        if start == 4 or end == 4: self.castling = self.castling.replace('k', '').replace('q', '')
        if start == 63 or end == 63: self.castling = self.castling.replace('K', '')
        if start == 56 or end == 56: self.castling = self.castling.replace('Q', '')
        if start == 7 or end == 7: self.castling = self.castling.replace('k', '')
        if start == 0 or end == 0: self.castling = self.castling.replace('q', '')
        if not self.castling: self.castling = "-"
            
        if self.turn == 'b':
            self.fullmove += 1
            self.turn = 'w'
        else:
            self.turn = 'b'
