

import pygame

from const import ROWS, COLS, WIDTH, HEIGHT, SQUARE_SIZE
from const import BLACK, WHITE
from dragger import Dragger
from config import Config
from promotion import Promotion
from color import PITCH_BLACK
from board import Board

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config ()
        self.promotion = Promotion(WHITE)
        self.hovered_square = None
        self.player = WHITE
        
    def reset(self) -> None:
        self.__init__()

    def show_bg(self, surface) -> None:
        theme = self.config.theme
        
        DARK = theme.bg.dark
        LIGHT = theme.bg.light
        
        for row in range(ROWS):
            for col in range(COLS):
                
                if (row + col) % 2 == 0 :
                    color = LIGHT
                else :
                    color = DARK
                    
                rectangle = (row*SQUARE_SIZE, col*SQUARE_SIZE, WIDTH, HEIGHT)
                pygame.draw.rect(surface, color, rectangle)
                
                # row coordinates
                if col == 0:
                    #color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    #label
                    label = self.config.font.render(str(ROWS-row), 1, color)
                    label_pos = ( 5, 5 + row * SQUARE_SIZE)
                    
                    surface.blit(label, label_pos)
                    
                if row == 7:
                    color = theme.bg.dark if (row+col) % 2 == 0 else theme.bg.light
                    #label
                    letter = chr(97+col)
                    label = self.config.font.render(str(letter), 1, color)
                    label_pos = (80 + col * SQUARE_SIZE, 80 + 7 * SQUARE_SIZE)
                    surface.blit(label, label_pos)            
                
                
    def show_pieces(self, surface)-> None:
        
        for row in range (ROWS):
            for col in range(COLS):
                
                
                if self.board.squares[row][col].has_a_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # If the piece is not being dragged:
                    if piece is not self.dragger.piece:
                        piece.set_texture(80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        # (Suppose this is a square [] what square_size  // does is take image to center otherwise the center of image is aligned to 0,0 of resp square)
                        
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface)-> None:
        
        if self.dragger.dragging:
            piece= self.dragger.piece 
            # Show all valid moves  
            for move in piece.moves:
                
                row , col = move.final.row, move.final.col
                
                # color = '#C86464' if (row + col) %2 == 0 else "#C84646"
                # rect = (col * SQUARE_SIZE, row * SQUARE_SIZE , SQUARE_SIZE, SQUARE_SIZE)
                # pygame.draw.rect(surface, color, rect)
                
                img = pygame.image.load('assets/images/legal_move.png')
                img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                dot = img.get_rect(center = img_center)
                surface.blit(img, dot)
                
    def show_last_move(self, surface) -> None:
        
        theme = self.config.theme
        
        DARK = theme.trace.dark
        LIGHT = theme.trace.light
        
        if self.board.last_move :
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in (initial, final):
                color = LIGHT if (pos.row + pos.col) % 2 ==0 else DARK 
                rect = (pos.col * SQUARE_SIZE , pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)
                
                
    def show_hover(self, surface) -> None:
        
        if self.hovered_square:
            color = PITCH_BLACK
            rect =  (self.hovered_square.col * SQUARE_SIZE, self.hovered_square.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect, 2)
            
    def show_promotion_pieces(self, surface) -> None:
        
        color = self.config.theme.trace.light

        pieces = self.promotion.array
        for i in range (2, 10, 2):
            # Drawing Rectangle
            pygame.draw.rect(surface, color, pygame.Rect(30, i*75, 740, 100)) 

            
            piece = pieces[(i//2)-1]
            
            label = self.config.font.render("To promote to {0} press {1}".format(piece.name, piece.name[0]), 16, BLACK)
            label_pos = ( 35, i*75 + 20)
            
            piece.set_texture(80)
            img = pygame.image.load(piece.texture)
            img_center = (650, i* 75 + 50)
            # (Suppose this is a square [] what square_size  // does is take image to center otherwise the center of image is aligned to 0,0 of resp square)
            
            piece.texture_rect = img.get_rect(center=img_center)
                        
            surface.blit(label, label_pos)       
            surface.blit(img, piece.texture_rect)
     
                
                
    def next_move (self):
        self.player = BLACK if self.player == WHITE else WHITE
        
    def set_hower(self, row, col):
        self.hovered_square = self.board.squares[row][col]
        
        
    def change_theme(self):
        self.config.change_theme()
        
    def play_sound(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()