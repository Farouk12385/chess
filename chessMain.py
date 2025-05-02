"""
this is the main file for the chess game
it is responsible for the game loop and user input
"""

import pygame as p #this is to import the pygame module
p.init()
import chessEngine
#---------------------------------------------------------------------------------
# this is to adjust the size of the window and squares dynamically
WIDTH = HEIGHT = 512  # default size of the window
DIMENSION = 8  # 8x8 board
SQ_SIZE = min(WIDTH, HEIGHT) // DIMENSION  # size of each square
MAX_FPS = 15  # for animations later when we add animations of chess pieces
#---------------------------------------------------------------------------------
IMAGES={} #this will hold the images of the chess pieces use in loadImages function
def loadImages():
    """
    this function loads the images of the chess pieces
    """
    pieces=["wK","wQ","wB","wN","wR","wp","bK","bQ","bB","bN","bR","bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        #Note:1- L use the for loop to be mush easier than loading them one by one
        #Note:2- L use the f-string the vscode say it better than the string concatenation
#----------------------------------------------------------------------------------
def main():
    """
    this function is responsible for main game loop
    it handles user input and updates the game state
    """
    global WIDTH, HEIGHT, SQ_SIZE
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)  # allow resizing of the window
    clock = p.time.Clock()  # this is to set the clock for the game
    screen.fill(p.Color("white"))  # this is to fill the window with white color
    gs = chessEngine.Gamestate()  # to have access to Gamestate class
    loadImages()  # this is to load the images of the chess pieces
    running = True# this is to check if the game is running
    sqSelected = ()  # to keep track of the square selected by the user
    playerClicks = []  #keep track of the clicks of the user
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False # this is to check if the user has closed the window
            if e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                running = False  # this is to check if the user has pressed the escape key to quit the game
            if e.type == p.VIDEORESIZE:  # handle window resizing
                WIDTH, HEIGHT = e.w, e.h
                SQ_SIZE = min(WIDTH, HEIGHT) // DIMENSION
                screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
            elif e.type == p.MOUSEBUTTONDOWN:  # this is to check if the user has clicked the mouse
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE  # this is to get the column of the square
                row= location[1] // SQ_SIZE  # this is to get the row of the square
                if sqSelected == (row, col):  # this is to check if the user has clicked the same square
                    sqSelected = ()# to deselect the square
                else:
                    sqSelected = (row, col)  # this is to set the square selected by the user
                    playerClicks.append(sqSelected)#append 1st click and 2nd click
                if len(playerClicks) == 2:
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())  # this is to print the move made by the user
                    gs.makeMove(move)
                    sqSelected = ()  # this is to deselect the square
                    playerClicks = []  # this is to reset the clicks of the user
        
                    
        drawGameState(screen, gs)  # this is to draw the game state on the screen
        clock.tick(MAX_FPS)  # this is to set the frame rate of the game
        p.display.flip()  # this is to update the window
#---------------------------------------------------------------------------------------------
def drawGameState(screen,gs):
    """
    this function draws the game state on the screen
    """
    drawBoard(screen) #this is to draw the board
    drawPieces(screen,gs.board) #this is to draw the pieces on the board
#---------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
def drawBoard(screen):
    """
    this function draws the board on the screen
    """
    colors=(p.Color("white"),p.Color("gray")) #this is to set the colors of the squares
    from itertools import product #this is to import product for looping
    for r, c in product(range(DIMENSION), repeat=2): #this is to loop through rows and columns
        color=colors[((r+c)%2)] #this is to set the color of the square
        p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE)) #this is to draw the square
#--------------------------------------------------------------------------------------
def drawPieces(screen,board):
    """
    this function draws the pieces on the board
    """
    from itertools import product#vscode say it better to import it here
    for r, c in product(range(DIMENSION), repeat=2):
            piece=board[r][c] #this is to get the piece on the square
            if piece!="--": #this is to check if the square is empty
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE)) #this is to draw the piece on the square
#--------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
if __name__=="__main__":
    main() #this is to run the main function
    quit() #this is to quit the game
#---------------------------------------------------------------------------------------
        
        
        
        
        
        
        
        












