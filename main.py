"""
main.py - Entry point for ParadoxM Chess Engine
-----------------------------------------------
Launches the engine, initializes UI, and manages game loop.
Now with better logging, graceful shutdown, and Holmesian flair.
"""

import sys
import traceback
import chess
import settings
from ui import ChessUI
from engine import ChessEngine
from analyzer import MoveAnalyzer

def print_banner():
    print("=" * 60)
    print("Python Chess Engine - GM Level".center(60))
    print("=" * 60)
    print("Configuration:")
    print(f"  Max Depth: {settings.MAX_DEPTH}")
    print(f"  Threads: {settings.NUM_THREADS}")
    print(f"  Time per move: {settings.TIME_PER_MOVE}s")
    print(f"  Mode: {settings.MODE}")
    print(f"  Player color: {settings.PLAYER_COLOR}")
    print("=" * 60)


def main():
    try:
        print_banner()

        # Initialize chess essentials
        board = chess.Board()
        engine = ChessEngine()
        analyzer = MoveAnalyzer()
        ui = ChessUI(engine)

        print("Starting chess UI...")
        ui.run()

        print("Game ended. Thanks for playing!")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Closing gracefully...")

    except Exception as e:
        print("\n[!] A mysterious incident has occurred...")
        traceback.print_exc()
        print("\nElementary, my dear Watson — check your board orientation,")
        print("for sometimes the problem lies not in our stars, but our squares.")

    finally:
        # If pygame or any thread remains, ensure proper shutdown
        try:
            import pygame
            pygame.quit()
        except Exception:
            pass

        print("Goodbye, detective. Case closed.")


if __name__ == "__main__":
    main()
