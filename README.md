# ♟️ Python Chess Engine

A fully playable chess engine built in Python — featuring a custom AI bot opponent. Developed independently as a personal project during Semester 1 of B.Tech (CS&E) at GLS University.

---

## 🎮 Features

- ✅ Full chess rules implementation (legal move validation, turn management)
- ✅ Check and checkmate detection
- ✅ Playable AI bot opponent — not unbeatable, but it'll keep you on your toes!
- ✅ Two-player and Player vs Bot modes
- ✅ Modular codebase split across multiple files for clean structure

---

## 🛠️ Tech Stack

| | |
|---|---|
| **Language** | Python 3 |
| **Structure** | Multi-module |
| **AI** | Custom bot logic |

---

## 📁 Project Structure

```
chess-engine/
│
├── main.py          # Entry point — run this to start the game
├── board.py         # Board state, setup, and display
├── pieces.py        # Piece definitions and movement rules
├── engine.py        # Bot AI logic
└── utils.py         # Helper functions
```

> Note: File names may vary slightly — check the source files directly.

---

## 🚀 How to Run

**Requirements:** Python 3.x installed on your machine.

```bash
# Clone the repository
git clone https://github.com/dk-8838/chess-engine.git

# Navigate into the folder
cd chess-engine

# Run the game
python main.py
```

---

## 🤖 About the Bot

The AI opponent is built with custom logic that evaluates board positions and picks moves accordingly. It's not a grandmaster — but it plays a real game and will occasionally surprise you. A great foundation to build stronger AI on top of (minimax, alpha-beta pruning coming soon).

---

## 📌 What I Learned

- Translating real-world game rules into clean, logical code
- Structuring a Python project across multiple modules
- Building a basic AI decision-making system from scratch
- Debugging complex state management (board positions, move history)

---

## 🔮 Planned Improvements

- [ ] Minimax algorithm with alpha-beta pruning for stronger AI
- [ ] Graphical UI using Pygame
- [ ] Move history and undo functionality
- [ ] Opening book support

---

## 👤 Author

**Dilkhush Labana**
B.Tech CS&E — GLS University, Ahmedabad
📧 Dilkhushlabana366@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/dilkhush-labana)

---

*Built with curiosity and way too many late nights debugging king moves.*
