#♟️Chess Game in Python

A Python implementation of chess with a graphical interface using Pygame. This project includes a complete chess engine with all standard rules and a user-friendly interface.

## Features

- Complete chess rules implementation:
  - Piece movements (including castling, en passant, and pawn promotion)
  - Check/checkmate detection
  - Stalemate detection
- Graphical interface with:
  - Piece highlighting
  - Move animations
  - Game over detection
- Game modes:
  - Player vs Player
  - Player vs AI (placeholder for future implementation)
- Interactive features:
  - Move undo (Z key)
  - Game reset (R key)

## 🧠 File Structure
![UML Diagram](https://github.com/Farouk12385/chess/blob/main/Chess%20Structure1.png)

### chessEngine.py

This file contains the core chess logic:

1. **GameState Class**:
   - Maintains the board state (8x8 grid)
   - Tracks game status (checkmate, stalemate)
   - Handles special moves (castling, en passant, promotion)
   - Manages move validation and execution

   Key methods:
   - `makeMove()`: Executes a move on the board
   - `undoMove()`: Reverts the last move
   - `getValidMoves()`: Returns all legal moves considering checks
   - Various piece movement generators (pawns, knights, etc.)

2. **CastleRights Class**:
   - Tracks castling privileges for both players

3. **Move Class**:
   - Represents a chess move with all relevant information
   - Handles chess notation conversion

### chessMain.py

This file handles the graphical interface and game loop:

1. **Initialization**:
   - Sets up the Pygame window
   - Loads piece images (with fallback graphics)

2. **Drawing Functions**:
   - `drawBoard()`: Renders the chess board
   - `drawPieces()`: Draws pieces on the board
   - `highlightSquares()`: Shows selected piece and valid moves
   - `animateMove()`: Animates piece movement

3. **Screens**:
   - `show_intro_screen()`: Displays the game title
   - `show_game_mode_screen()`: Lets players choose game mode

4. **Main Game Loop**:
   - Handles player input (mouse clicks, keyboard shortcuts)
   - Manages game state updates
   - Renders the current board state

## How to Run

1. Ensure you have Python 3 and Pygame installed:

2. Run the game:

3. Controls:
- Left-click to select and move pieces
- Press 'Z' to undo a move
- Press 'R' to reset the game

## Future Improvements

- Implement AI opponent
- Add move history display
- Include sound effects
- Add game clock/timer
- Implement save/load functionality

## Dependencies

- Python 3.x
- Pygame library

Enjoy the game!


    

  

