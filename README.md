# Saulochess - Chess Analysis Engine

[![PyPI version](https://badge.fury.io/py/saulochess.svg)](https://pypi.org/project/saulochess/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Git49--max%2Fsaulochess-blue.svg)](https://github.com/Git49-max/saulochess)

`saulochess` is a robust Python API for detailed chess game analysis and review, utilizing the powerful Stockfish engine to classify moves and generate analysis comments (such as _brilliant_, _mistake_, _blunder_, etc.).

The package is designed to be flexible and **free from proprietary data dependencies**. The end-user is responsible for providing the Stockfish path and their own open-source openings database (using public domain sources like Lichess CC0) to enable the openings functionality.

## Installation

The package is available on PyPI.

```bash
pip install saulochess
```

Prerequisites
Stockfish Engine: You must have the Stockfish executable (version 16 or higher is recommended) installed and accessible. You will need to provide the path to this executable when initializing the engine.

API Usage
The main module is chess_review. We recommend that you always start and close the Stockfish engine manually to manage resources efficiently.

1. Single Move Review (review_move)
   This function analyzes the current board position and classifies a specific move, returning Stockfish's best move for comparison.

```Python

import chess.engine
from saulochess import chess_review
import chess

# --- 1. Initialize the Stockfish Engine ---
# Replace "stockfish" with the full path (e.g., "C:/stockfish/stockfish-windows-x86-64.exe")
# if it is not in your system's PATH.
try:
    engine = chess.engine.open_uci("stockfish")
except Exception as e:
    print(f"ERROR: Could not open Stockfish. Check the path. Details: {e}")
    exit()

# --- 2. Set up the Board and the Move ---
board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Initial position
move = chess.Move.from_uci("e2e4") # The move to be analyzed

# --- 3. Review the Move ---
classification, review, best_move, san_best = chess_review.review_move(
    board,
    move,
    previous_review="Game Start",
    engine=engine # **REQUIRED: Pass the open engine object**
)

# --- 4. Result ---
print(f"Classification: {classification}")
print(f"Engine Review: {review}")
print(f"Stockfish Best Move: {san_best} ({best_move})")

# --- 5. Close the Engine ---
engine.quit()
```

2. Full Game Analysis (review_game_data)
   The main game analysis function takes a list of moves in UCI notation and returns a tuple containing all analysis data, including accuracy, ELO estimation, and the full list of classifications and comments.

```Python

from saulochess import chess_review
import chess.engine
# ... (other imports)

# 1. Initialize the Engine (same process as above)
engine = chess.engine.open_uci("stockfish")

# 2. List of moves in UCI
uci_moves = [
    'e2e4', 'e7e5', 'g1f3', 'b8c6',
    'f1c4', 'g8f6', 'd2d3', 'h7h6'
]

# 3. Analyze the Game
# 'roast=True' activates funnier comments; 'roast=False' is technical.
game_data = chess_review.review_game_data(
    uci_moves,
    roast=True,
    engine=engine # **REQUIRED**
)

# 4. The function returns a tuple of 15 elements. Unpack them in the correct order:
(
    san_moves, fens, scores, classification_list, review_list, best_review_list,
    san_best_moves, uci_best_moves, devs, tens, mobs, conts,
    white_acc, black_acc, white_elo_est, black_elo_est
) = game_data

print(f"\n--- Final Summary ---")
print(f"White's Accuracy: {white_acc:.2f}% (Est. ELO: {white_elo_est})")
print(f"Comment for 3rd Move: {review_list[2]}")

# 5. Close the Engine
engine.quit()
```

3. Openings Integration (Optional Feature)
   To use the openings identification feature, you must load your own Pandas DataFrame and pass it as an argument to the review functions:

```Python

import pandas as pd
from saulochess import chess_review

# 1. Load your own opening database.
# Your CSV must have 'pgn' and 'name' columns.
try:
    my_openings_df = pd.read_csv("path/to/my_openings_database.csv")
except:
    my_openings_df = None

engine = chess.engine.open_uci("stockfish")

# 2. Use the feature by passing the DataFrame:
classification, review, best_move, san_best = chess_review.review_move(
    board,
    move,
    previous_review="Initial",
    engine=engine,
    openings_df=my_openings_df, # <--- PASS THE DATAFRAME HERE
    check_if_opening=True       # <--- ACTIVATE THE CHECK HERE
)


engine.quit()
```

License
This package uses base code licensed under the MIT License. The copyright notice for the original base code is included in the LICENSE file: Copyright (c) 2023 LinkAnJarad.

Further developments are Copyright (c) 2025 Saulo/SauloChess and are also under the MIT License.

The original code is from LinkAnJarad, available in https://github.com/LinkAnJarad/OpenChess-Insights/blob/main/chess_review.py. I made some alterations, such as improvements of the engine management and translated it to portuguese. The english version is coming soon with a new option of wich language you want to see the review :)
