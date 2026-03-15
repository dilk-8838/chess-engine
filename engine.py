"""
engine.py - Core chess engine logic
Performs position evaluation and search (Minimax with Alpha-Beta pruning)
Integrated with witty Sherlock-style commentary system.
"""

import chess
import time
from evaluation import Evaluation


class ChessEngine:
    """Core chess engine using alpha-beta search and heuristic evaluation."""

    def __init__(self, max_depth=4, time_limit=5.0):
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.evaluator = Evaluation()
        self.start_time = 0
        self.nodes_searched = 0

    # -------------------------------------------------------
    # Core Search
    # -------------------------------------------------------
    def search(self, board: chess.Board, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
        """Recursive alpha-beta search with depth and time constraints."""
        self.nodes_searched += 1

        # Time cutoff
        if time.time() - self.start_time > self.time_limit:
            return self.evaluator.evaluate(board)

        # Terminal states
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board)

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return self.evaluator.evaluate(board)

        if is_maximizing:
            value = -float("inf")
            for move in legal_moves:
                board.push(move)
                value = max(value, self.search(board, depth - 1, alpha, beta, False))
                board.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cutoff
            return value
        else:
            value = float("inf")
            for move in legal_moves:
                board.push(move)
                value = min(value, self.search(board, depth - 1, alpha, beta, True))
                board.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return value

    # -------------------------------------------------------
    # Move Selection
    # -------------------------------------------------------
    def get_best_move(self, board: chess.Board):
        """
        Returns the best move and evaluation for the current position.
        Uses iterative deepening for better time control.
        """
        best_move = None
        best_eval = -float("inf") if board.turn == chess.WHITE else float("inf")
        self.start_time = time.time()
        self.nodes_searched = 0

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None, self.evaluator.evaluate(board), []

        # Iterative deepening
        for depth in range(1, self.max_depth + 1):
            if time.time() - self.start_time > self.time_limit:
                break

            for move in legal_moves:
                board.push(move)
                eval_score = self.search(
                    board, depth - 1, -float("inf"), float("inf"), not board.turn
                )
                board.pop()

                if board.turn == chess.WHITE:
                    if eval_score > best_eval:
                        best_eval = eval_score
                        best_move = move
                else:
                    if eval_score < best_eval:
                        best_eval = eval_score
                        best_move = move

        # Collect top 3 moves (for UI display)
        top_lines = []
        for move in sorted(
            legal_moves,
            key=lambda m: self.evaluate_move(board, m),
            reverse=board.turn == chess.WHITE,
        )[:3]:
            score = self.evaluate_move(board, move)
            top_lines.append((move, score))

        elapsed = round(time.time() - self.start_time, 2)
        print(
            f"[Engine] Best Move: {best_move}, Eval: {best_eval/100:+.2f}, "
            f"Depth: {self.max_depth}, Nodes: {self.nodes_searched}, Time: {elapsed}s"
        )

        return best_move, best_eval, top_lines

    # -------------------------------------------------------
    # Quick Move Evaluation (for sorting)
    # -------------------------------------------------------
    def evaluate_move(self, board: chess.Board, move: chess.Move) -> int:
        """Quick static evaluation for move ordering."""
        board.push(move)
        value = self.evaluator.evaluate(board)
        board.pop()
        return value

    # -------------------------------------------------------
    # Move Execution Helper
    # -------------------------------------------------------
    def make_move(self, board: chess.Board, move: chess.Move):
        """Execute a move and return updated board and evaluation."""
        board.push(move)
        eval_score = self.evaluator.evaluate(board)
        return board, eval_score
