# ♟️ ParadoxM Chess Engine

> *"When you have eliminated the impossible, whatever remains, however improbable, must be the truth."*
> — Sherlock Holmes (and this engine, evaluating your blunder)

A fully-featured Python chess engine with a graphical interface, AI opponent, and Sherlock Holmes-style move commentary. Built independently during Semester 1 of B.Tech (CS&E).

---

## 🎮 Features

### 🤖 Engine & AI
- **Minimax search with Alpha-Beta pruning** — the same algorithm family used in professional chess engines
- **Iterative deepening** — searches progressively deeper within a time budget for best move quality
- **Piece-square tables** — separate opening and endgame tables with smooth phase interpolation
- **Configurable search depth & time limit** — up to depth 35, 6 seconds per move by default
- **Zobrist hashing** — efficient board state identification

### 🧠 Move Analysis
- **Real-time move classification** — every move you make is rated as Brilliant, Best Move, Excellent, Good, Inaccuracy, Mistake, or Blunder
- **Sacrifice detection** — engine recognises when you throw a piece with purpose
- **Evaluation swing tracking** — shows how much each move shifts the position in centipawns
- **Sherlock Holmes commentary** — witty, snarky analysis of every move in the style of the world's greatest detective

### 🖥️ GUI (Pygame)
- Full graphical chessboard with piece images
- Board auto-flips based on player color
- Click-to-move with legal move highlights
- Live commentary panel below the board
- Clean Chess.com-inspired color scheme

### ⚙️ Configuration
All engine and UI settings are cleanly managed in `settings.py`:
- Search depth, threads, time per move
- Board orientation, colors, sound
- Game mode: Human vs Engine or Engine vs Engine

---

## 📁 Project Structure

```
paradoxm-chess/
│
├── main.py          # Entry point — launches the game
├── engine.py        # Minimax + Alpha-Beta search, move selection
├── evaluation.py    # Position evaluation with piece-square tables
├── analyzer.py      # Move classifier & Holmes-style explainer
├── ui.py            # Pygame GUI — board, pieces, commentary
├── utils.py         # Zobrist hashing, move formatting, helpers
└── settings.py      # Global configuration
```

---

## 🚀 Getting Started

### Requirements
```
Python 3.8+
pygame
python-chess
```

### Install dependencies
```bash
pip install pygame python-chess
```

### Run the game
```bash
python main.py
```

---

## 🧩 How It Works

### Search Algorithm
The engine uses **Minimax with Alpha-Beta pruning** — it thinks several moves ahead, maximising its own score while minimising yours. Alpha-beta pruning cuts off branches that can't possibly affect the result, making the search significantly faster.

```
Minimax Tree
    MAX (engine)
   /     |     \
 MIN    MIN    MIN   (your responses)
 / \   / \   / \
MAX MAX ...        (engine replies)
```

### Position Evaluation
Each position is scored using:
1. **Material balance** — standard piece values (P=100, N=320, B=330, R=500, Q=900)
2. **Piece-square tables** — bonuses/penalties based on where pieces stand
3. **Game phase interpolation** — seamlessly blends opening and endgame evaluation tables based on remaining material

### Move Classification
After each of your moves, the analyzer compares your move's evaluation against the engine's best move:

| Classification | Eval Difference |
|---|---|
| Brilliant | Best move + sacrifice/capture |
| Best Move | Matches engine's top choice |
| Excellent | Within 10 centipawns |
| Good | Within 25 centipawns |
| Inaccuracy | Within 50 centipawns |
| Mistake | Within 100 centipawns |
| Blunder | 200+ centipawns off |

---

## 📸 Sample Commentary

> *"A blunder! A crime against logic itself."*

> *"Flawless execution. Quite textbook, my dear Watson."*

> *"A brilliant sacrifice — beauty wrapped in logic."*

---

## 🔮 Planned Improvements

- [ ] Transposition table for caching previously evaluated positions
- [ ] Quiescence search to avoid horizon effect
- [ ] Opening book support
- [ ] Move history and undo functionality
- [ ] Stronger endgame tablebase

---

## 👤 Author

**Dilkhush Labana**
B.Tech CS&E — GLS University, Ahmedabad (2025–2029)
📧 Dilkhushlabana366@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/dilkhush-labana)

---

*Built with curiosity, too many late nights, and an unhealthy respect for Sherlock Holmes.*
