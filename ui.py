"""
ui.py - Graphical User Interface for ParadoxM Chess Engine
----------------------------------------------------------
Elegant yet deadly — handles display, moves, and witty Sherlockian commentary.
"""

import pygame
import chess
import utils
import settings
from engine import ChessEngine
from evaluation import Evaluation
from analyzer import MoveAnalyzer

# =========================
# UI Constants
# =========================
TILE_SIZE = 80
BOARD_SIZE = TILE_SIZE * 8
FPS = 30
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0)
TEXT_BG = (25, 25, 25)
TEXT_COLOR = (240, 240, 240)

# =========================
# UI Class
# =========================
class ChessUI:
    def __init__(self, engine: ChessEngine, player_color=chess.WHITE):
        pygame.init()
        pygame.display.set_caption("ParadoxM - Sherlock’s Chessboard")

        self.engine = engine
        self.evaluator = Evaluation()
        self.analyzer = MoveAnalyzer()
        self.board = chess.Board()
        self.player_color = player_color

        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18, bold=True)
        self.commentary_font = pygame.font.SysFont("georgia", 16, italic=True)

        self.selected_square = None
        self.possible_moves = []
        self.commentary = "Ah, the game begins. Every pawn hides a secret."
        self.running = True

        self.piece_images = self.load_piece_images()

    # -------------------------
    # Load and draw functions
    # -------------------------
    def load_piece_images(self):
        """Load and scale chess piece images."""
        pieces = {}
        for color in ['w', 'b']:
            for piece in ['p', 'n', 'b', 'r', 'q', 'k']:
                filename = f"{color}{piece}.png"
                img = pygame.image.load(filename)
                img = pygame.transform.smoothscale(img, (TILE_SIZE, TILE_SIZE))
                pieces[color + piece] = img
        return pieces

    def draw_board(self):
        """Draw chessboard with correct orientation."""
        for rank in range(8):
            for file in range(8):
                color = LIGHT_COLOR if (rank + file) % 2 == 0 else DARK_COLOR
                x, y = self.board_to_screen_coords(file, rank)
                pygame.draw.rect(self.screen, color, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

    def draw_pieces(self):
        """Draw all chess pieces."""
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                x, y = self.board_to_screen_coords(file, rank)
                key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().lower()
                self.screen.blit(self.piece_images[key], (x, y))

    def board_to_screen_coords(self, file, rank):
        """Convert board coords to screen position (handles flipping)."""
        if self.player_color == chess.WHITE:
            return file * TILE_SIZE, (7 - rank) * TILE_SIZE
        else:
            return (7 - file) * TILE_SIZE, rank * TILE_SIZE

    def screen_to_square(self, x, y):
        """Convert mouse coords to board square (handles flipping)."""
        file = x // TILE_SIZE
        rank = 7 - (y // TILE_SIZE)
        if self.player_color == chess.BLACK:
            file, rank = 7 - file, 7 - rank
        return chess.square(file, rank)

    # -------------------------
    # Move handling
    # -------------------------
    def handle_click(self, pos):
        """Handle player clicks and selections."""
        if pos[1] > BOARD_SIZE:
            return  # Ignore clicks in commentary area

        square = self.screen_to_square(*pos)
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.player_color:
                self.selected_square = square
                self.possible_moves = [m for m in self.board.legal_moves if m.from_square == square]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.make_player_move(move)
            self.selected_square = None
            self.possible_moves = []

    def make_player_move(self, move):
        board_before = self.board.copy()
        eval_before = self.evaluator.evaluate(board_before)
        best_move, best_eval, _ = self.engine.get_best_move(board_before)

        self.board.push(move)
        eval_after = self.evaluator.evaluate(self.board)

        classification = self.analyzer.classify_move(
        board_before,
        move,
        best_move,
        eval_before,
        best_eval
    )

        self.commentary = self.analyzer.explain_move(
        board_before,
        move,
        classification,
        eval_before,
        eval_after
    )

    # -------------------------
    # Draw Highlights & Text
    # -------------------------
    def draw_highlights(self):
        """Highlight selected square and legal moves."""
        if self.selected_square is not None:
            file = chess.square_file(self.selected_square)
            rank = chess.square_rank(self.selected_square)
            x, y = self.board_to_screen_coords(file, rank)
            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 3)

            for move in self.possible_moves:
                file = chess.square_file(move.to_square)
                rank = chess.square_rank(move.to_square)
                x, y = self.board_to_screen_coords(file, rank)
                pygame.draw.circle(self.screen, (0, 0, 0), (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 8)

    def draw_commentary(self):
        """Draw witty commentary below the board."""
        pygame.draw.rect(self.screen, TEXT_BG, pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100))
        lines = utils.wrap_text(self.commentary, self.commentary_font, BOARD_SIZE - 20)
        for i, line in enumerate(lines):
            text_surf = self.commentary_font.render(line, True, TEXT_COLOR)
            self.screen.blit(text_surf, (10, BOARD_SIZE + 10 + i * 22))

    def draw(self):
        """Render the entire scene."""
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        self.draw_commentary()
        pygame.display.flip()

    # -------------------------
    # Main game loop
    # -------------------------
    def run(self):
        """Run the grand play — the main event loop."""
        print("The stage is set. The first move is a confession.")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        print("Game ended. The mystery, alas, is solved.")
