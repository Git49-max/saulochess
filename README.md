# Saulochess - Chess Analysis Engine

[![PyPI version](https://badge.fury.io/py/saulochess.svg)](https://pypi.org/project/saulochess/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Git49--max%2Fsaulochess-blue.svg)](https://github.com/Git49-max/saulochess)

`saulochess` is a robust Python API for detailed chess game analysis and review, utilizing the powerful Stockfish engine to classify moves and generate analysis comments (such as _brilliant_, _mistake_, _blunder_, etc.).

The package is designed to be flexible and **free from proprietary data dependencies**. The end-user is responsible for providing the Stockfish path and their own open-source openings database to enable the openings functionality.

## Installation

The package is available on PyPI.

```bash
pip install saulochess
```

## Prerequisites

Stockfish Engine: You must have the Stockfish executable (version 16 or higher is recommended) installed and accessible. You will need to provide the path to this executable when initializing the engine.

## API Usage

The main module is chess_review. We recommend that you always start and close the Stockfish engine manually to manage resources efficiently.

1. Single Move Review (review_move)
   This function analyzes the current board position and classifies a specific move, returning Stockfish's best move for comparison.

```Python

import chess.engine
from saulochess import chess_review
import chess

# --- Configuration ---
STOCKFISH_PATH = r"C:\path\to\stockfish.exe" # Update this path

try:
    # 1. Initialize the Stockfish Engine with 'with'
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:

        # 2. Set up the Board and the Move
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") # Initial position
        move = chess.Move.from_uci("e2e4") # The move to be analyzed

        # 3. Review the Move
        classification, review, best_move, san_best = chess_review.review_move(
            board,
            move,
            previous_review="Game Start",
            engine=engine # **REQUIRED: Pass the open engine object**
        )

        # 4. Result
        print(f"Classification: {classification}")
        print(f"Engine Review: {review}")
        print(f"Stockfish Best Move: {san_best} ({best_move})")

# 'with' automatically calls engine.quit() here.

except Exception as e:
    print(f"ERROR: Could not open Stockfish or analyze. Check the path. Details: {e}")
```

2. Full Game Analysis (pgn_game_review)
   The main game analysis function takes a game in PGN string format and returns a tuple containing all analysis data, including accuracy, ELO estimation, and the full list of classifications and comments (18 elements total).

```Python

import chess.engine
from saulochess import chess_review # Assumes the library is installed
import platform
import traceback

# ---------------------------------------------------------------------------
# IMPORTANT: REQUIRED CONFIGURATION
# ---------------------------------------------------------------------------
# 1. Change this variable to the FULL path of the Stockfish executable
STOCKFISH_PATH = r'path\\to\\stockfish.exe' # UPDATE THIS PATH

# Analysis Parameters
ANALYSIS_LIMIT_TYPE = 'depth' # Or 'Time'. We strongly recommend you to use depth, because it's faster and does not impact in the review.
ANALYSIS_TIME_LIMIT = 0.2  # Time in seconds per move (used if ANALYSIS_LIMIT_TYPE="time")
ANALYSIS_DEPTH_LIMIT = 10  # Depth (used if ANALYSIS_LIMIT_TYPE="depth")

# Example PGN for analysis (The Immortal Game)
PGN_EXAMPLE = """

[Event "London, 1851"]
[Site "London ENG"]
[Date "1851.06.21"]
[Round "6"]
[White "Adolf Anderssen"]
[Black "Lionel Adalbert Bagelsen"]
[Result "1-0"]

1. e4 e5 2. f4 exf4 3. Bc4 Qh4+ 4. Kf1 b5 5. Bxb5 Nf6 6. Nf3 Qh6 7. d3 Nh5 8. Nh4 Qg5 9. Nf5 c6 10. g4 Nf6 11. Rg1 cxb5 12. h4 Qg6 13. h5 Qg5 14. Qf3 Nc6 15. Bxf4 Ne5 16. Bxe5 Qc1+ 17. Kf2 Qxc2+ 18. Ke1 Bb4+ 19. Nc3 Bxc3+ 20. bxc3 d6 21. Bxf6 gxf6 22. e5 fxe5 23. Qxa8 O-O 24. Ne7+ Kh8 25. Nxc8 Qxc3+ 26. Ke2 Qc2+ 27. Kf3 Qxd3+ 28. Kf2 Qd2+ 29. Kf1 Qf4+ 30. Ke2 e4 31. Raf1 Qh2+ 32. Ke3 Qe5 33. Rf5 Qc3+ 34. Kxe4 Qc2+ 35. Kd4 Qb2+ 36. Kd5 Qa3 37. Rgf1 h6 38. Rxf7 Qd3+ 39. Kc6 Qc4+ 40. Kb7 Rf7+ 41. Rxf7 Qxf7+ 42. Kxa7 Kg7 43. Ka6 Qxa2+ 44. Kb6 b4 45. Nxd6 b3 46. Nf5+ Kf6 47. Nxh6+ Kg5 48. Nf7+ Kxg4 49. Ne5+ Kh3 50. Nc4 Qc2 51. Na3 Qc1 52. Nb5 b2 53. Nd4 b1=Q 54. Nxb1 Qxb1 55. Qh8+ Kg2 56. Qg7+ Kf1 57. Qf6+ Ke2 58. Qe5+ Kd1 59. Qd4+ Kc1 60. Qc4+ Kb2 61. Qb4+ Ka1 62. Qa3+ Qa2 63. Qxa2+ Kxa2 64. h6 Kb3 65. h7 Kc4 65. h8=Q Kb4 67. Qh4+ Ka3 68. Qb8 Ka2 69. Kc5 Ka3 70. Kc4 Ka2 71. Kc3 Ka1 72. Kc2 Ka2 73. Qb3+ Ka1 74. Qb2# 1-0
"""

# ---------------------------------------------------------------------------


def run_test():
    print("Starting chess_review API test...")

    # A simple check to see if the user has updated the path
    if "path\\to\\stockfish.exe" in STOCKFISH_PATH:
        print("\n--- CONFIGURATION ERROR ---")
        print("Please edit the 'STOCKFISH_PATH' variable with the correct path.")
        return

    try:
        print(f"Opening engine at: {STOCKFISH_PATH}...")
        # Initialize the Stockfish Engine using 'with' to ensure safe closure
        with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:

            print(f"Engine opened successfully. Version: {engine.id['name']}")
            print("\nStarting pgn_game_review...")

            # 3. Analyze the Full Game, PASSING ALL 6 ARGUMENTS
            game_data = chess_review.pgn_game_review(
                pgn_data=PGN_EXAMPLE,
                roast=False,
                limit_type=ANALYSIS_LIMIT_TYPE,
                time_limit=ANALYSIS_TIME_LIMIT,
                depth_limit=ANALYSIS_DEPTH_LIMIT,
                engine=engine # The 'engine' object is passed to the API
            )

            print("Function pgn_game_review completed.")

            # 4. Unpack the 18 returned values
            (
                san_moves, fens, scores, classification_list, review_list, best_review_list,
                san_best_moves, uci_best_moves, devs, tens, mobs, conts,
                white_acc, black_acc, white_elo_est, black_elo_est,
                average_cpl_white, average_cpl_black
            ) = game_data

            print("\n--- GENERAL RESULTS ---")
            print(f"Game analyzed with {len(san_moves)} moves.")
            print(f"White Accuracy: {white_acc:.2f}% (Est. ELO: {white_elo_est})")
            print(f"Black Accuracy: {black_acc:.2f}% (Est. ELO: {black_elo_est})")
            print(f"Average CPL White: {average_cpl_white:.2f}")
            print(f"Average CPL Black: {average_cpl_black:.2f}")

            print("\n--- MOVE-BY-MOVE REVIEW ---")

            if not san_moves:
                print("No moves were analyzed (empty lists returned).")
                return

            # Display results by combining lists
            for i, san in enumerate(san_moves):
                try:
                    classif = classification_list[i].upper() if i < len(classification_list) else "N/A"
                    review = review_list[i] if i < len(review_list) else "(N/A)"
                    best_move = san_best_moves[i] if i < len(san_best_moves) else "N/A"

                    print(f" {i+1}. {san} ({classif}): {review}")
                    print(f"    Best Move: {best_move} | Score: {scores[i]}")

                except IndexError:
                    # Catches cases where one list is shorter than another (internal API error)
                    print(f" {i+1}. {san}: (INCOMPLETE ANALYSIS DATA)")
                except Exception as e_loop:
                    print(f" {i+1}. {san}: (Error printing data: {e_loop})")


    except FileNotFoundError:
        print("\n--- CRITICAL ERROR ---")
        print(f"The Stockfish engine was not found at path: {STOCKFISH_PATH}")
    except Exception as e:
        print(f"\n--- UNEXPECTED ERROR DURING ANALYSIS ---")
        print(f"An error occurred: {e}")
        traceback.print_exc()

    print("\nTest finished.")

if __name__ == "__main__":
    try:
        import chess
    except ImportError:
        print("Error: The 'python-chess' library is not installed.")
        print("Please install it using: pip install python-chess")
    else:
        run_test()

```

3. Openings Integration (Optional Feature)
   To use the openings identification feature, you must load your own Pandas DataFrame and pass it as an argument to the review functions:

```Python

import pandas as pd
from saulochess import chess_review
# ... (Engine initialization)

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

## ⚠️ Known Bug: First Move Analysis

We are currently aware of a minor bug where the analysis of the first move of the game may fail internally, often resulting in an argument of type 'NoneType' is not iterable warning/error.

Symptom: The console may show an internal [AVISO] message or an ERROR classification for the first move only.

Impact: The rest of the game analysis (move 2 onwards) is generally unaffected, and the final summary results (Accuracy, ELO, Avg CPL) are correctly calculated based on the successful analysis of the remaining moves.

We are working on a fix to ensure a smooth analysis start.

## License

This package uses base code licensed under the MIT License. The copyright notice for the original base code is included in the LICENSE file: Copyright (c) 2023 LinkAnJarad.

Further developments are Copyright (c) 2025 Saulo/SauloChess and are also under the MIT License.

The original code is from LinkAnJarad, available in [OpenChess-Insights](https://github.com/LinkAnJarad/OpenChess-Insights/tree/main). I made some alterations, such as improvements of the engine management and translated it to portuguese. The English version is coming soon with a new option of which language you want to see the review :)

By the way, the API code is open-source. If you want to contribute, go to https://github.com/Git49-max/saulochess. Don't forget to see the OpenChess-Insights github too!

Buy LinkAnJarad a coffee: https://buymeacoffee.com/linkanjarad
