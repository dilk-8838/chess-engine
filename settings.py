# ==========================================================
# settings.py - Global Configuration for ParadoxM Chess Engine
# ==========================================================

# --------------------------
# Engine Search Settings
# --------------------------
MAX_DEPTH = 35                # Maximum search depth
PRACTICAL_DEPTH = 20          # Depth to reach in ~5-6 seconds
NUM_THREADS = 5               # Parallel threads for root search
TIME_PER_MOVE = 6.0           # Seconds allocated per move

# --------------------------
# Transposition Table Settings
# --------------------------
TT_SIZE = 2**20               # 1 million entries
TT_EXACT = 0
TT_LOWERBOUND = 1
TT_UPPERBOUND = 2

# --------------------------
# Evaluation Settings
# --------------------------
PIECE_VALUES = {
    'P': 100,    # Pawn
    'N': 320,    # Knight
    'B': 330,    # Bishop
    'R': 500,    # Rook
    'Q': 900,    # Queen
    'K': 20000   # King
}

# --------------------------
# Move Ordering Scores
# --------------------------
SCORE_PV = 2_000_000
SCORE_CAPTURE_BASE = 1_000_000
SCORE_KILLER_1 = 900_000
SCORE_KILLER_2 = 800_000
SCORE_HISTORY_BASE = 1000  # Small bump for frequent good moves

# --------------------------
# Move Classification (centipawns)
# --------------------------
CLASS_BRILLIANT_THRESHOLD = 50
CLASS_BEST_THRESHOLD = 20
CLASS_EXCELLENT_THRESHOLD = 50
CLASS_GOOD_THRESHOLD = 100
CLASS_INACCURACY_THRESHOLD = 200
CLASS_MISTAKE_THRESHOLD = 400
CLASS_BLUNDER_THRESHOLD = 700

# --------------------------
# UI Settings
# --------------------------
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60

# Board orientation fix
# ----------------------
# True = auto-flip the board for black player
# False = keep white at bottom always
AUTO_FLIP_BOARD = True

# --------------------------
# Colors (Chess.com inspired)
# --------------------------
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_LIGHT = (205, 210, 106)
HIGHLIGHT_DARK = (170, 162, 58)
SELECTED_LIGHT = (246, 246, 130)
SELECTED_DARK = (186, 202, 43)
LAST_MOVE_LIGHT = (246, 246, 105)
LAST_MOVE_DARK = (186, 202, 43)

# --------------------------
# Evaluation Bar Colors
# --------------------------
EVAL_WHITE = (255, 255, 255)
EVAL_BLACK = (50, 50, 50)
EVAL_BORDER = (0, 0, 0)

# --------------------------
# Text Colors
# --------------------------
TEXT_BLACK = (0, 0, 0)
TEXT_WHITE = (255, 255, 255)
TEXT_GRAY  = (128, 128, 128)

# --------------------------
# Sound Settings
# --------------------------
ENABLE_SOUND = True
MOVE_SOUND_VOLUME = 0.7
CAPTURE_SOUND_VOLUME = 0.8

# --------------------------
# Game Mode Configuration
# --------------------------
MODE = "hve"          # "hve" = human vs engine, "eve" = engine vs engine
PLAYER_COLOR = "white"  # "white" or "black"
