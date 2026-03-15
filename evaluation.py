"""
evaluation.py - Position evaluation with piece-square tables
Enhanced for stability and orientation correctness.
"""

import chess
import settings


# ==========================================================
# PIECE-SQUARE TABLES
# (white’s perspective, A1=0 … H8=63)
# ==========================================================

PAWN_TABLE_OPENING = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

PAWN_TABLE_ENDGAME = [
    0, 0, 0, 0, 0, 0, 0, 0,
    80, 80, 80, 80, 80, 80, 80, 80,
    50, 50, 50, 50, 50, 50, 50, 50,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    0, 0, 0, 0, 0, 0, 0, 0
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

ROOK_TABLE = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0
]

QUEEN_TABLE = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

KING_TABLE_OPENING = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 40, 20, 0, 0, 20, 40, 20
]

KING_TABLE_ENDGAME = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 0, 10, 10, 0, -10, -30,
    -40, -20, -10, 0, 0, -10, -20, -40,
    -50, -40, -30, -20, -20, -30, -40, -50
]


# ==========================================================
# EVALUATOR CLASS
# ==========================================================
class Evaluation:
    """Evaluates a chess position with PSTs and material balance."""

    def __init__(self):
        self.piece_tables = {
            chess.PAWN: (PAWN_TABLE_OPENING, PAWN_TABLE_ENDGAME),
            chess.KNIGHT: (KNIGHT_TABLE, KNIGHT_TABLE),
            chess.BISHOP: (BISHOP_TABLE, BISHOP_TABLE),
            chess.ROOK: (ROOK_TABLE, ROOK_TABLE),
            chess.QUEEN: (QUEEN_TABLE, QUEEN_TABLE),
            chess.KING: (KING_TABLE_OPENING, KING_TABLE_ENDGAME),
        }

    def get_game_phase(self, board: chess.Board) -> float:
        """Compute game phase (1=open, 0=endgame) based on material."""
        total_material = 0
        max_material = sum(settings.PIECE_VALUES[p] * 2 * n for p, n in {
            'P': 8, 'N': 2, 'B': 2, 'R': 2, 'Q': 1
        }.items())

        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            piece_value = settings.PIECE_VALUES[chess.piece_symbol(piece_type).upper()]
            count = len(board.pieces(piece_type, chess.WHITE)) + len(board.pieces(piece_type, chess.BLACK))
            total_material += count * piece_value

        return min(total_material / max_material, 1.0)

    def get_piece_square_value(self, piece_type, square, is_white, phase) -> int:
        """Interpolated piece-square value, flipped correctly for black."""
        opening_table, endgame_table = self.piece_tables[piece_type]

        # Flip square vertically for black
        if not is_white:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            square = chess.square(file, 7 - rank)

        opening_value = opening_table[square]
        endgame_value = endgame_table[square]
        return int(phase * opening_value + (1 - phase) * endgame_value)

    def evaluate(self, board: chess.Board) -> int:
        """Evaluate board: positive for white advantage, negative for black."""
        if board.is_checkmate():
            return -20000 if board.turn == chess.WHITE else 20000
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        phase = self.get_game_phase(board)

        for piece_type in self.piece_tables:
            piece_value = settings.PIECE_VALUES[chess.piece_symbol(piece_type).upper()]
            for sq in board.pieces(piece_type, chess.WHITE):
                score += piece_value
                score += self.get_piece_square_value(piece_type, sq, True, phase)
            for sq in board.pieces(piece_type, chess.BLACK):
                score -= piece_value
                score -= self.get_piece_square_value(piece_type, sq, False, phase)

        return score
