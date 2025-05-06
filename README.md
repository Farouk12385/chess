# ♟️ Chess Game

<div align="center">
  <img src="https://via.placeholder.com/800x200?text=Welcome+To+My+Project" width="80%">
</div>

## ✨ UML
![Alt Text](https://github.com/Farouk12385/chess/blob/main/Chess%20Structure.png)

## 🧠 Chess Gme Explaintion
-Chess Main
 -drawBoard(screen): void
   - To draw board
 -drawPieces(screen, board): void
   - To draw pieces in board
 -highlightSquares(screen, gs, valid_moves, sq_selected): void
   - to highlight valid Moves Squares
 -drawGameState(screen, gs, valid_moves, sq_selected): void
   - to this fuction thats have all previous to combine it in one board
 -animateMove(move, screen, board, clock): void
   - to make animation when pieces move
 -drawEndGameText(screen, text): void
   - to make Screen White is owner or black 
 -showIntroScreen(screen): bool
   - to choose between ai and 1v1
 -showGameModeScreen(screen): str
   - to print Python Chess
-Ai
   - In future
-Game State
  -makeMove(move: Move): void
    - to allow any piece to move
  -undoMove(): void
    - to undo moves of pieces
  -getValidMoves(): list[Move]
    - bec every piece have ileagle moves
  -inCheck(): bool
    - if king in check
  -squareUnderAttack(r: int, c: int): bool
    - to make red light when king under attack
  -getAllPossibleMoves(): list[Move]
    - to show ileagle move for every piece
  -updateCastleRights(move: Move): void
    - to update for king when there's squares can be under attack
  -Move
    

  

