import chess
from engine import ChessEngine
from utils import witty_commentary

# Classification thresholds in centipawns (1 pawn = 100 cp)
CLASS_THRESHOLDS = {
    "Brilliant": 0,
    "Best Move": 0,
    "Excellent": 10,
    "Good": 25,
    "Inaccuracy": 50,
    "Mistake": 100,
    "Blunder": 200,
}

class MoveAnalyzer:
    """
    Sherlock Holmes of the chessboard.
    Deduces whether your last move was a stroke of genius...
    or a confession of madness.
    """

    def __init__(self):
        self.engine = ChessEngine()

    def classify_move(
        self,
        board: chess.Board,
        player_move: chess.Move,
        best_move: chess.Move,
        player_eval: int,
        best_eval: int
    ) -> str:
        """
        Classify a move based on its evaluation delta.
        More deviation from the truth = more regret later.
        """
        if player_move == best_move:
            # Check for sacrifices and dramatic flair
            if self.is_sacrifice(board, player_move) or board.is_capture(player_move):
                piece = board.piece_at(player_move.from_square)
                if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
                    return "Brilliant"
            return "Best Move"

        eval_diff = abs(player_eval - best_eval)
        for label in ["Excellent", "Good", "Inaccuracy", "Mistake", "Blunder"]:
            if eval_diff <= CLASS_THRESHOLDS[label]:
                return label
        return "Blunder"

    def is_sacrifice(self, board: chess.Board, move: chess.Move) -> bool:
        """Detect if the player just threw a piece into the abyss — for art or for madness."""
        piece = board.piece_at(move.from_square)
        if not piece:
            return False
        board.push(move)
        is_attacked = board.is_attacked_by(not board.turn, move.to_square)
        board.pop()
        return is_attacked

    def explain_move(
        self,
        board: chess.Board,
        move: chess.Move,
        classification: str,
        eval_before: int,
        eval_after: int
    ) -> str:
        """Generate a Holmes-style explanation of the move."""
        eval_change = (eval_after - eval_before) / 100
        explanation = witty_commentary(classification, move, board)

        if board.is_capture(move):
            captured = board.piece_at(move.to_square)
            if captured:
                explanation += f" Captures a {chess.piece_name(captured.piece_type)} — rather unceremoniously."
        board.push(move)
        if board.is_check():
            explanation += " Ah! A check — bold, reckless, or both."
        board.pop()

        if abs(eval_change) > 0.5:
            explanation += f" ({'+' if eval_change > 0 else ''}{eval_change:.2f} eval swing.)"
        return explanation

    def analyze_position(self, board: chess.Board, depth: int = 15):
        """
        Peers deep into the abyss of possibilities.
        Returns: best move, evaluation score, and a list of top lines.
        """
        best_move, eval_score, top_lines = self.engine.get_best_move(board)
        return best_move, eval_score, top_lines
