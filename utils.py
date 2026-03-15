"""
utils.py - Utility functions for ParadoxM Chess Engine
Includes hashing, formatting, and board orientation helpers.
"""
import chess
import random
import settings


# ==========================================================
# ZOBRIST HASHING
# ==========================================================
ZOBRIST_PIECE_KEYS = {}
ZOBRIST_SIDE_KEY = random.getrandbits(64)
import random
import chess

def witty_commentary(classification: str, move: chess.Move, board: chess.Board) -> str:
    """
    Returns a snarky, Holmes-style comment for a move classification.
    """

    comments = {
        "Brilliant": [
            "Ah, a stroke of genius! I dare say even Moriarty would applaud.",
            "A brilliant sacrifice — beauty wrapped in logic.",
            "The move gleams with brilliance — rare and precise as a diamond."
        ],
        "Best Move": [
            "Flawless execution. Quite textbook, my dear Watson.",
            "The most logical continuation — elementary.",
            "Perfect play. You march like a machine of reason."
        ],
        "Excellent": [
            "A commendable move, steady as the Thames on a calm day.",
            "Sound logic. A whiff of genius, if not the full perfume.",
            "An excellent maneuver, though perfection lies a few moves further."
        ],
        "Good": [
            "A solid move — reliable, if not inspired.",
            "Good — though a keener eye might’ve found an even sharper edge.",
            "Respectable play. The kind that wins wars, not hearts."
        ],
        "Inaccuracy": [
            "A slight misstep, Watson — the scent grows faint.",
            "Not quite the trail I’d have followed.",
            "An inaccuracy, minor but telling. The truth slips through your grasp."
        ],
        "Mistake": [
            "A mistake, old chap. Even the best stumble on the foggy nights.",
            "Oh dear... a tactical oversight fit for the tabloids.",
            "The move smells of trouble — and poor reasoning."
        ],
        "Blunder": [
            "A blunder! A crime against logic itself.",
            "Watson, fetch the smelling salts — this one hurts.",
            "Disaster! A blunder worthy of a tragic novel."
        ]
    }

    category = comments.get(classification, ["A curious move indeed."])
    return random.choice(category)

def wrap_text(text, font, max_width):
    """
    Splits long text into multiple lines to fit inside a given width.
    Used for witty commentary display in the UI.
    """
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = f"{current_line} {word}".strip()
        width, _ = font.size(test_line)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def init_zobrist():
    """Initialize zobrist hashing keys"""
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    for sq in chess.SQUARES:
        for piece in pieces:
            for color in [chess.WHITE, chess.BLACK]:
                ZOBRIST_PIECE_KEYS[(sq, piece, color)] = random.getrandbits(64)

def compute_zobrist_hash(board: chess.Board) -> int:
    """Compute zobrist hash for a given board"""
    h = 0
    for sq, piece in board.piece_map().items():
        h ^= ZOBRIST_PIECE_KEYS.get((sq, piece.piece_type, piece.color), 0)
    if board.turn == chess.BLACK:
        h ^= ZOBRIST_SIDE_KEY
    return h


# ==========================================================
# MOVE FORMATTING
# ==========================================================
def format_move(move: chess.Move, board: chess.Board) -> str:
    """
    Format move to human-readable SAN (e.g., Nf3, exd5)
    Safely handles illegal moves without crashing.
    """
    try:
        if move in board.legal_moves:
            return board.san(move)
        else:
            # Fallback to simple coordinate notation
            return move.uci()
    except Exception:
        return move.uci()


def format_score(score: int) -> str:
    """Format evaluation score as human-friendly text"""
    if score > 9000:
        return "M+"  # checkmate imminent
    elif score < -9000:
        return "M-"  # checkmate against
    else:
        return f"{score / 100:.2f}"


# ==========================================================
# BOARD ORIENTATION HELPERS
# ==========================================================
def invert_board_orientation(board: chess.Board, player_color: str):
    """
    Adjust board orientation both horizontally and vertically.
    Returns a FEN string with flipped ranks and files.
    Used for UI rendering to fix inversion issues.
    """
    fen_parts = board.board_fen().split("/")
    fen_parts.reverse()  # vertical flip (rank inversion)
    flipped_rows = []
    for row in fen_parts:
        flipped_rows.append(row[::-1])  # horizontal flip (file inversion)
    flipped_board_fen = "/".join(flipped_rows)
    fen_rest = " ".join(board.fen().split(" ")[1:])
    new_fen = f"{flipped_board_fen} {fen_rest}"

    new_board = chess.Board(new_fen)
    # Make sure turn and castling rights remain correct
    new_board.turn = board.turn
    new_board.castling_rights = board.castling_rights
    new_board.ep_square = board.ep_square
    return new_board if settings.AUTO_FLIP_BOARD and player_color == "black" else board


# ==========================================================
# OTHER HELPERS
# ==========================================================
def move_to_tuple(move: chess.Move):
    """Convert a move to a (from_square, to_square) tuple"""
    return (move.from_square, move.to_square)


def pretty_print_board(board: chess.Board):
    """Prints board in a friendly console format"""
    print("\n   +------------------------+")
    for rank in range(8, 0, -1):
        print(f" {rank} |", end=" ")
        for file in "abcdefgh":
            sq = chess.parse_square(file + str(rank))
            piece = board.piece_at(sq)
            print(piece.symbol() if piece else ".", end=" ")
        print("|")
    print("   +------------------------+")
    print("     a b c d e f g h\n")


# Initialize zobrist keys at module import
init_zobrist()
