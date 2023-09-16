import pygame
import os
import color

from sound import Sound
from theme import Theme

class Config:
    
    def __init__(self):
        self.themes = []
        self.add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold= True)
        
        # font
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav')
        )
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav')
        )
    
    def change_theme(self): 
        self.idx +=1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]
        
    
    def add_themes(self):
        green = Theme(
            color.LIGHT_GREEN,
            color.DARK_GREEN,
            color.YELLOW,
            color.DARK_YELLOW
        )
        
        # ToDo
        
        
        brown = Theme(      
            color.LIGHT_BROWN,  
            color.DARK_BROWN,
            color.TINT,
            color.BROWN
            
        )

        blue = Theme(
            color.LIGHT_BLUE,
            color.DARK_BLUE,
            color.FAINT_BLUE,
            color.BLUE
        )
        
        red = Theme(
            color.RED,
            color.CHECKERS_BLACK,
            color.SKIN,
            color.OLIVE
            
        )
        
        self.themes = [green, blue, brown, red]
        