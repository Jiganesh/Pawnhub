import pygame
from game import Game
from board import Board
from dragger import Dragger
from square import Square
from move import Move
from piece import Knight, Bishop, Rook, Queen

import sys

APPLICATION_NAME = "PawnHub"

from const import WIDTH, HEIGHT, COLS, ROWS, SQUARE_SIZE

        
class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        self.board = Board()
        self.dragger = Dragger()
        pygame.display.set_caption(APPLICATION_NAME)
        
        
    def mainloop(self) -> None:
        
        SCREEN = self.screen
        GAME = self.game
        BOARD = self.game.board
        DRAGGER = self.game.dragger

        def choose_piece():
            pygame.display.set_caption("Choose Piece for Pawn Promotion")
            while BOARD.pawn_promotion :
                
                SCREEN.fill("black")
                
                GAME.show_promotion_pieces(SCREEN)
                
                
                for event in  pygame.event.get():
                    if event.type == pygame.KEYDOWN:                
                        if event.key == pygame.K_k and BOARD.pawn_promotion:
                            BOARD.move(Knight(piece.color), move)
                            BOARD.pawn_promotion = False
                            
                        if event.key == pygame.K_q and BOARD.pawn_promotion:
                            BOARD.move(Queen(piece.color), move)
                            BOARD.pawn_promotion = False
           
                        if event.key == pygame.K_r and BOARD.pawn_promotion:
                            BOARD.move(Rook(piece.color), move)
                            BOARD.pawn_promotion = False

                        if event.key == pygame.K_b and BOARD.pawn_promotion:
                            BOARD.move(Bishop(piece.color), move)
                            BOARD.pawn_promotion = False
                            
                        if event.key == pygame.K_t:
                            GAME.change_theme()
                            
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                
                pygame.display.set_caption(APPLICATION_NAME)
                pygame.display.update()
                                
        while True: 
            GAME.show_bg(SCREEN)
            GAME.show_last_move(SCREEN)
            GAME.show_hover(SCREEN)
            GAME.show_pieces(SCREEN)
            GAME.show_moves(SCREEN)
            
            
            # MOUSE EVENTS
            if DRAGGER.dragging:
                DRAGGER.update_blit(SCREEN)
            
            for event in pygame.event.get():
                
                # Dragging the Piece 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    DRAGGER.update_mouse(event.pos)
                    
                    clicked_row = DRAGGER.mouseY//SQUARE_SIZE
                    clicked_col = DRAGGER.mouseX//SQUARE_SIZE
                    
                    if BOARD.squares[clicked_row][clicked_col].has_a_piece():
                        piece = BOARD.squares[clicked_row][clicked_col].piece
                        
                        if piece.color == GAME.player:
                            BOARD.calc_moves(piece, clicked_row, clicked_col, True)
                            DRAGGER.save_initial(event.pos)
                            DRAGGER.drag_piece(piece)

                        # Show Methods
                        GAME.show_bg(SCREEN)
                        GAME.show_last_move(SCREEN)
                        GAME.show_pieces(SCREEN)
                        GAME.show_moves(SCREEN)

                elif event.type == pygame.MOUSEMOTION:
                    
                    if DRAGGER.dragging :
                        DRAGGER.update_mouse(event.pos)
                        DRAGGER.update_blit(SCREEN)
                    
                    DRAGGER.update_mouse(event.pos)
                    row =  DRAGGER.mouseY//SQUARE_SIZE
                    col =  DRAGGER.mouseX//SQUARE_SIZE
                    try:
                        GAME.set_hower(row, col)    
                    except:
                        pass
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    try : 
                        if DRAGGER.dragging :
                            DRAGGER.update_mouse(event.pos)
                            released_row =  DRAGGER.mouseY//SQUARE_SIZE
                            released_col =  DRAGGER.mouseX//SQUARE_SIZE
                            
                            initial = Square(DRAGGER.initial_row, DRAGGER.initial_col)
                            final = Square(released_row, released_col)
                            captured = BOARD.squares[released_row][released_col].has_a_piece()      
                            
                            move = Move(initial, final)
                            
                            if BOARD.valid_move(piece, move):
                                BOARD.move(DRAGGER.piece, move)
                                BOARD.set_true_en_passant(DRAGGER.piece)    
                                
                                if BOARD.pawn_promotion:
                                    choose_piece()
                                    GAME.show_bg(SCREEN)
                                    GAME.show_pieces(SCREEN)
                            
                                GAME.next_move()
                                GAME.play_sound(captured)
                                
                                
                            GAME.show_bg(SCREEN)
                            GAME.show_pieces(SCREEN)
                    except:
                        pass
                                          
                    DRAGGER.undrag_piece()
                    
                # KEY EVENTS
                
                elif event.type == pygame.KEYDOWN:
                    
                    
                    
                    if event.key == pygame.K_t:
                        GAME.change_theme()
                        
                    if event.key == pygame.K_e:
                        GAME.reset()
                        GAME = self.game
                        BOARD = self.game.board
                        DRAGGER = self.game.dragger
                        

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
 

main = Main()
main.mainloop()
