# Othello Game Clone

## Overview
This project implements the game of Othello (also known as Reversi) in Python using the pygame library. The game supports two-player mode and player-computer mode where the computer AI uses the minimax algorithm with alpha-beta pruning.

## Project Structure
The project consists of the following files:
- `main.py`: The main entry point of the game.
- `othello.py`: Contains the core logic for the Othello game, including the game rules and board state management.
- `ai.py`: Implements the AI opponent using the minimax algorithm with alpha-beta pruning.
- `images/`: Directory containing images used for the game graphics.

## Gameplay Logic
The game follows the standard rules of Othello. Players take turns placing their pieces on the board with the goal of capturing the opponent's pieces by sandwiching them between their own pieces. The game ends when no more moves are possible, and the player with the most pieces on the board wins.

### AI Logic
The AI opponent uses the minimax algorithm with alpha-beta pruning to make its decisions. This algorithm explores the game tree to find the best move based on a heuristic evaluation function.

## How to Run
To run the game, simply execute `main.py` using Python 3. Ensure that the pygame library is installed (`pip install pygame`) before running the game.
