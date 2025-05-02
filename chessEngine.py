"""
This class is responsible for the storing information about the chess board and the pieces on it.
It also contains methods for moving pieces, checking for valid moves, and checking for checkmate or stalemate.
"""
class Gamestate():
    
    def __init__(self):
        # board is an 8x8 list of lists, where each element is a string representing a piece
        # or "--" for an empty square
        # The pieces are represented as follows:
        # wR = white rook, wN = white knight, wB = white bishop, wQ = white queen, wK = white king, wp = white pawn
        # bR = black rook, bN = black knight, bB = black bishop, bQ = black queen, bK = black king, bp = black pawn
        # The first character represents the color (w for white, b for black)
        # The second character represents the type of piece (R for rook, N for knight, B for bishop, Q for queen, K for king, p for pawn)
        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],#they are 1st row(b)
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],#they are 2nd row(b)
        ["--", "--", "--", "--", "--", "--", "--", "--"],#they are 3rd row(empty)
        ["--", "--", "--", "--", "--", "--", "--", "--"],#they are 4th row(empty)
        ["--", "--", "--", "--", "--", "--", "--", "--"],#they are 5th row(empty)
        ["--", "--", "--", "--", "--", "--", "--", "--"],#they are 6th (empty)
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],#they are 7th row (w)
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]#they are 8th row w)
        self.whiteToMove = True # True if it's w turn to move, False if it's b
        self.movelog = [] # This is a list of all the moves made in the game
#----------------------------------------
    def makeMove(self, move):
        """
        This function updates the board state with the move made.
        It updates the board, switches the turn to the other player, and adds the move to the move log.
        """
        self.board[move.startRow][move.startCol] = "--" # this is to set the starting square to empty
        self.board[move.endRow][move.endCol] = move.pieceMoved # this is to set the ending square to the piece moved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove
        # this is to switch the turn to the other player
#-------------------------------------------
    def undoMove(self):
        """
        This function undoes the last move made in the game.
        It updates the board, switches the turn back to the previous player, and removes the move from the move log.
        """
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
# this is to switch the turn back to the previous player
        
        
        
#------------------------------------------------------------------------------------------------------------
class Move():
    """
    This class is responsible for storing information about a move made in the game.
    It contains the starting and ending square of the move, as well as the piece being moved.
    """
    
    rankstoRows = { "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0 }
    rowsToRanks = { 7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8" }
    filesToCols = { "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7 }
    colsToFiles = { 0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h" }
    
    
    
    def __init__(self, startSq, endSq, board):
        """
        This function initializes the move object with the starting and ending square of the move,
        as well as the board state.
        """
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] # this is to get the piece moved
        self.pieceCaptured = board[self.endRow][self.endCol] # this is to get the piece captured
        self.isPawnPromotion = False
        if self.pieceMoved[1] == "p" and (self.endRow == 0 or self.endRow == 7):
            self.isPawnPromotion = True
            # this is to check if the pawn has reached the other side of the board
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # this is to create a unique ID for the move
#----------------------------------------------
    def __eq__(self, other):
        """
        This function checks if two moves are equal.
        """
        
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
#---------------------------------------------
    def getChessNotation(self):
        """
        This function returns the chess notation for the move made.
        """
        return f"{self.pieceMoved[1]}{self.startRow}{self.startCol}{self.endRow}{self.endCol}"
        # this is to return the chess notation for the move made
#-----------------------------------------------
    def getRankFile(self):
        """
        This function returns the rank and file of the move made.
        """
        return self.startRow, self.startCol, self.endRow, self.endCol
        # this is to return the rank and file of the move made
#----------------------------------------------
    def __str__(self):
        """
        This function returns a string representation of the move made.
        """
        return f"{self.pieceMoved} from {self.startRow}{self.startCol} to {self.endRow}{self.endCol}"
        # this is to return a string representation of the move made
#-----------------------------------------------------------------------------------

        
        
        
        
