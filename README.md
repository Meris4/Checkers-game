# ♟️ Checkers Game with AI (Dame)

**Course:** Data Structures and Algorithms  
**Language:** Python  
**Semester:** 2nd  
**Academic Year:** 2023/2024  
**Project Type:** Console-Based Board Game with AI Opponent

---

## 📌 Overview

A Python-based implementation of the classic Checkers (Dame) game, allowing a human player to compete against an AI-controlled opponent. The AI uses the **Minimax algorithm with Alpha-Beta Pruning** to analyze possible moves and select optimal strategies based on a custom heuristic evaluation function and adjustable search depth.

The application supports two gameplay modes, mandatory and optional captures, and implements essential checkers mechanics, including multiple jump sequences, king promotion, and backward moves for kings.

---

## 🎮 Core Features

- 👤 **Human vs AI** – play against a computer-controlled opponent
- ♟️ **Move Generation** – generate and validate all legal moves for each game state
- ⚔️ **Capture Mechanics** – support mandatory and optional captures
- 🔗 **Multiple Jump Chains** – perform consecutive captures within a single turn
- 👑 **King Promotion** – promote pieces to kings when reaching the opposite side of the board
- ↩️ **Backward Movement** – allow kings to move and capture backward
- 🎯 **Move Selection** – choose moves through indexed options in the console
- 📺 **Board Rendering** – display the game board and available moves after each turn

---

## 🧠 Algorithms & AI

- **Minimax Algorithm** – explore possible game states and select strategically advantageous moves
- **Alpha-Beta Pruning** – eliminate unnecessary branches of the search tree to improve performance
- **Custom Heuristic Evaluation** – evaluate board positions based on game-specific criteria
- **Depth-Limited Search** – control the number of moves explored by the AI
- **Dynamic Search Depth** – adjust search depth to balance decision quality and execution time
- **HashMap-Based Caching** – store previously evaluated game states to avoid redundant calculations
- **Game Tree Exploration** – simulate possible sequences of moves to determine the best decision

---

## 🧱 Technical Highlights

- **Programming Language:** Python
- **Data Structures:** Matrices, Trees, HashMaps
- **Algorithms:** Minimax, Alpha-Beta Pruning
- **AI Strategy:** Heuristic-based game state evaluation
- **Optimization:** Alpha-Beta Pruning and state caching
- **Search Strategy:** Depth-limited search with adjustable depth
- **Performance:** AI move calculation typically completes within 3 seconds, depending on the search depth and board position

---

## 🕹️ Gameplay Modes

**Mandatory Capture**
- Players must capture an opponent's piece whenever a capture is available.
- The game enforces the forced-capture rule during move selection.

**Optional Capture**
- Players can choose whether to capture an opponent's piece or make another legal move.
- Captures are available but not required.

---

## 🎓 Learning Outcomes

Through this project, I gained practical experience with:

- Implementing adversarial search algorithms for game-playing AI
- Understanding and applying Minimax and Alpha-Beta Pruning
- Designing heuristic functions for evaluating game states
- Working with recursive algorithms and game trees
- Applying data structures to optimize search performance
- Managing game states, legal moves, and complex capture sequences
