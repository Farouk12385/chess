"""
This class is responsible for the storing information about the chess board and the pieces on it.
It also contains methods for moving pieces, checking for valid moves, and checking for checkmate or stalemate.
"""
#------------------------------------------------------------------------------------------------
class GameState():
    def __init__(self):
        # 8x8 2D list representing the board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        
        self.whiteToMove = True
        self.movelog= []  # Fixed: Consistent camelCase naming
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()  # Coordinates for en passant capture
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs)]
#----------------------------
    def makeMove(self, move):
        """
        Execute a move (works for all move types)
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)  # Fixed: Using correct attribute name
        self.whiteToMove = not self.whiteToMove
        
        # Update king's position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
            
        # Pawn promotion
        if move.isPawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N: ").upper()
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
            
        # En passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
            
        # Update enpassant possible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()
            
        # Castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # Kingside
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:  # Queenside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"
        
        # Update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs))
#------------------------------
    def undoMove(self):
        """
        Undo the last move
        """
    def undoMove(self):
        """Undo the last move"""
        if len(self.movelog) == 0:  # Fixed: Using correct attribute name
            return
        
        move = self.movelog.pop()  # Fixed: Using correct attribute name
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.whiteToMove = not self.whiteToMove
        
        # Update king's position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)
        
        # Undo en passant
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = "--"
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)
        
        # Undo 2 square pawn advance
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()
        
        # Undo castling rights
        self.castleRightsLog.pop()
        self.currentCastlingRight = self.castleRightsLog[-1]
        
        # Undo castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # Kingside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                self.board[move.endRow][move.endCol-1] = "--"
            else:  # Queenside
                self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
#------------------------------
    def updateCastleRights(self, move):
        """
        Update castling rights based on move
        """
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    def getValidMoves(self):
        """
        Get all valid moves considering checks
        """
        # Save current state
        temp_enpassant = self.enpassantPossible
        temp_castle_rights = CastleRights(
            self.currentCastlingRight.wks, 
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs, 
            self.currentCastlingRight.bqs)
        
        # 1) Generate all possible moves
        moves = self.getAllPossibleMoves()
        
        # 2) For each move, make the move
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        # 3) Check for checkmate/stalemate
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        # 4) Add castling moves
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        
        # Restore original state
        self.enpassantPossible = temp_enpassant
        self.currentCastlingRight = temp_castle_rights
        
        return moves
#------------------------------
    def inCheck(self):
        """
        Check if current player is in check
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
#------------------------------
    def squareUnderAttack(self, r, c):
        """
        Check if square (r,c) is under attack
        """
        self.whiteToMove = not self.whiteToMove  # Switch to opponent's turn
        opp_moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Switch back
        
        for move in opp_moves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
#------------------------------
    def getAllPossibleMoves(self):
        """
        Get all possible moves without considering checks
        """
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
#------------------------------
    def getPawnMoves(self, r, c, moves):
        """
        Get all pawn moves
        """
        if self.whiteToMove:  # White pawn moves
            if self.board[r-1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r-2, c), self.board))
            
            # Captures
            for d in [-1, 1]:  # Left and right capture
                if 0 <= c+d < 8:
                    if self.board[r-1][c+d][0] == 'b':  # Enemy piece
                        moves.append(Move((r, c), (r-1, c+d), self.board))
                    elif (r-1, c+d) == self.enpassantPossible:
                        moves.append(Move((r, c), (r-1, c+d), self.board, isEnpassantMove=True))
        
        else:  # Black pawn moves
            if self.board[r+1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r+2, c), self.board))
            
            # Captures
            for d in [-1, 1]:  # Left and right capture
                if 0 <= c+d < 8:
                    if self.board[r+1][c+d][0] == 'w':  # Enemy piece
                        moves.append(Move((r, c), (r+1, c+d), self.board))
                    elif (r+1, c+d) == self.enpassantPossible:
                        moves.append(Move((r, c), (r+1, c+d), self.board, isEnpassantMove=True))
#------------------------------
    def getRookMoves(self, r, c, moves):
        """
        Get all rook moves
        """
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))  # Up, down, left, right
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty space
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:  # Off board
                    break
#------------------------------
    def getKnightMoves(self, r, c, moves):
        """
        Get all knight moves
        """
        # Knight moves
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.whiteToMove else 'b'
        # Check each knight move
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Not an ally piece
                    moves.append(Move((r, c), (end_row, end_col), self.board))
#------------------------------
    def getBishopMoves(self, r, c, moves):
        """
        Get all bishop moves
        """
        # Bishop moves
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Diagonals
        enemy_color = 'b' if self.whiteToMove else 'w'
        # Check each diagonal
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty space
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Friendly piece
                        break
                else:  # Off board
                    break
#------------------------------
    def getQueenMoves(self, r, c, moves):
        """
        Get all queen moves
        """
        # bec Queen moves like rook and bishop
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
#------------------------------
    def getKingMoves(self, r, c, moves):
        """
        Get all king moves
        """
        # King moves
        king_moves = ((-1, -1), (-1, 0), (-1, 1),
                    (0, -1),          (0, 1),
                    (1, -1),  (1, 0), (1, 1))
        ally_color = 'w' if self.whiteToMove else 'b'
        # Check each king move
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Not an ally piece
                    moves.append(Move((r, c), (end_row, end_col), self.board))
#------------------------------
    def getCastleMoves(self, r, c, moves):
        """
        Generate all valid castle moves
        """
        if self.squareUnderAttack(r, c):
            return  # Can't castle while in check
        
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)
#------------------------------
    def getKingsideCastleMoves(self, r, c, moves):
        """
        Check kingside castle moves
        """
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))
#------------------------------
    def getQueensideCastleMoves(self, r, c, moves):
        """
        Check queenside castle moves
        """
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

#----------------------------------------------------------------------------------------------------------------------------------------------
class CastleRights():
    """
    Track castling rights for both players
    """
    #------------------------------
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks  # White king side
        self.bks = bks  # Black king side
        self.wqs = wqs  # White queen side
        self.bqs = bqs  # Black queen side

#-------------------------------------------------------------------------------------------------------------------------------------------
class Move():
    """
    Store and manage chess moves
    """
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
#------------------------------
    def __init__(self, start_sq, end_sq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        # Pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or \
                            (self.pieceMoved == 'bp' and self.endRow == 7)
        
        # En passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        
        # Castle move
        self.isCastleMove = isCastleMove
        
        # Move ID
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
#------------------------------
    def __eq__(self, other):
        """
        Override equals method
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
#------------------------------
    def getChessNotation(self):
        """
        Get chess notation of the move
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
#------------------------------
    def getRankFile(self, r, c):
        """
        Convert row, col to chess notation (e.g., 0,0 -> a8)
        """
        return self.cols_to_files[c] + self.rows_to_ranks[r]
#------------------------------
        
        
        
        


        
        
        
        
