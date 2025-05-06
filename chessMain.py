"""
this is the main file for the chess game
it is responsible for the game loop and user input
"""

import pygame as p
from chessEngine import GameState, Move

# Initialize pygame
p.init()

# Constants
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}  # Dictionary to store piece images

# Colors
BG_COLOR = (28, 28, 28)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
GRAY = (100, 100, 100)
HIGHLIGHT = (100, 255, 100, 100)
#------------------------------
def loadImages():
    """
    Load images for chess pieces
    """
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        try:
            IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        except:
            # Fallback: Draw colored rectangles if images not found
            surf = p.Surface((SQ_SIZE, SQ_SIZE), p.SRCALPHA)
            color = (255, 255, 255) if piece[0] == 'w' else (0, 0, 0)
            p.draw.rect(surf, color, (0, 0, SQ_SIZE, SQ_SIZE), 0, 5)
            p.draw.rect(surf, (200, 0, 0) if piece[1] == 'K' else (0, 0, 200), 
                        (5, 5, SQ_SIZE-10, SQ_SIZE-10), 0, 3)
            IMAGES[piece] = surf
#------------------------------
def drawBoard(screen):
    """
    Draw chess board squares
    """
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
#------------------------------
def drawPieces(screen, board):
    """
    Draw chess pieces on board
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
#------------------------------
def highlightSquares(screen, gs, valid_moves, sq_selected):
    """
    Highlight selected square and valid moves
    """
    if sq_selected:
        row, col = sq_selected
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
            # Highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            
            # Highlight valid moves
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))
#------------------------------
def drawGameState(screen, gs, valid_moves, sq_selected):
    """
    Draw complete game state
    """
    drawBoard(screen)
    highlightSquares(screen, gs, valid_moves, sq_selected)
    drawPieces(screen, gs.board)
#------------------------------
def animateMove(move, screen, board, clock):
    """
    Animate piece movement
    """
    d_row = move.endRow - move.startRow
    d_col = move.endCol - move.startCol
    frames = 10  # Animation frames
    for frame in range(frames + 1):
        r, c = (move.startRow + d_row * frame/frames, move.startCol + d_col * frame/frames)
        drawBoard(screen)
        drawPieces(screen, board)
        # Draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
#------------------------------
def drawEndGameText(screen, text):
    """
    Display game over text
    """
    font = p.font.SysFont("Helvetica", 32, True)
    text_surface = font.render(text, True, p.Color("red"))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text_surface, text_rect)
#------------------------------
def show_intro_screen(screen):
    """
    Display intro screen
    """
    title_font = p.font.SysFont("Arial", 72, bold=True)
    small_font = p.font.SysFont("Arial", 24)
    
    title = title_font.render("Python Chess", True, GREEN)
    subtitle = small_font.render("Press any key to continue", True, WHITE)
    
    screen.fill(BG_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 + 150))
    p.display.flip()
    
    waiting = True
    while waiting:
        for e in p.event.get():
            if e.type == p.QUIT:
                return False
            if e.type in (p.KEYDOWN, p.MOUSEBUTTONDOWN):
                waiting = False
    return True
#------------------------------
def show_game_mode_screen(screen):
    """
    Display game mode selection
    """
    title_font = p.font.SysFont("Arial", 64, bold=True)
    button_font = p.font.SysFont("Arial", 36)
    
    title = title_font.render("Select Game Mode", True, GREEN)
    pvp_text = button_font.render("Player vs Player", True, WHITE)
    ai_text = button_font.render("Player vs AI", True, WHITE)
    
    pvp_button = p.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 50)
    ai_button = p.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 50)
    
    while True:
        mouse_pos = p.mouse.get_pos()
        pvp_hover = pvp_button.collidepoint(mouse_pos)
        ai_hover = ai_button.collidepoint(mouse_pos)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                return None
            if e.type == p.MOUSEBUTTONDOWN:
                if pvp_hover:
                    return "1v1"
                elif ai_hover:
                    return "ai"
        
        screen.fill(BG_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        
        p.draw.rect(screen, HIGHLIGHT if pvp_hover else GRAY, pvp_button)
        p.draw.rect(screen, HIGHLIGHT if ai_hover else GRAY, ai_button)
        
        screen.blit(pvp_text, (pvp_button.centerx - pvp_text.get_width()//2, 
                            pvp_button.centery - pvp_text.get_height()//2))
        screen.blit(ai_text, (ai_button.centerx - ai_text.get_width()//2, 
                        ai_button.centery - ai_text.get_height()//2))
        p.display.flip()
#------------------------------
def main():
    """
    Main game loop
    """
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(BG_COLOR)
    p.display.set_caption("Python Chess")
    
    if not show_intro_screen(screen):
        p.quit()
        return
    
    game_mode = show_game_mode_screen(screen)
    if not game_mode:
        p.quit()
        return
    
    gs = GameState()
    loadImages()
    valid_moves = gs.getValidMoves()
    move_made = False
    animate = False
    game_over = False
    sq_selected = ()
    player_clicks = []
    
    running = True
    while running:
        human_turn = (True if game_mode == "1v1" else  gs.whiteToMove)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo
                    gs.undoMove()
                    move_made = True
                    game_over = False
                if e.key == p.K_r:  # Reset
                    gs = GameState()
                    valid_moves = gs.getValidMoves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    game_over = False
            elif e.type == p.MOUSEBUTTONDOWN and not game_over and human_turn:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                
                if len(player_clicks) == 2:
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    for valid_move in valid_moves:
                        if move == valid_move:
                            gs.makeMove(valid_move)
                            move_made = True
                            animate = True
                            sq_selected = ()
                            player_clicks = []
                            break
                    if not move_made:
                        player_clicks = [sq_selected]
        
        # AI move logic would go here
        if not game_over and not human_turn and game_mode == "ai":
            pass  # Placeholder for AI logic
        
        if move_made:
            if animate:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            valid_moves = gs.getValidMoves()
            move_made = False
            animate = False
            
            if gs.checkMate or gs.staleMate:
                game_over = True
        
        drawGameState(screen, gs, valid_moves, sq_selected)
        
        if game_over:
            if gs.checkMate:
                text = "Black wins by checkmate!" if gs.whiteToMove else "White wins by checkmate!"
            else:
                text = "Game ended in stalemate"
            drawEndGameText(screen, text)
        
        p.display.flip()
        clock.tick(MAX_FPS)
    
    p.quit()
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
        



