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
        standard = Theme(
            color.LIGHT_GREEN,
            color.DARK_GREEN,
            color.LIGHT_GREEN_TRACE,
            color.DARK_GREEN_TRACE
        )
        
        # ToDo
        
        
        walnut = Theme(      
            color.LIGHT_TAN,  
            color.DARK_TAN,
            color.LIGHT_TAN_TRACE,
            color.DARK_TAN_TRACE
            
        )

        blue = Theme(
            color.LIGHT_BLUE,
            color.DARK_BLUE,
            color.LIGHT_BLUE_TRACE,
            color.DARK_BLUE_TRACE
        )
        
        checkers = Theme(
            color.DARK_RED,
            color.LIGHT_GREY,
            color.SKIN,
            color.OLIVE
            
        )

        cosmos = Theme (
            color.COSMOS_LIGHT,
            color.COSMOS_DARK,
            color.COSMOS_LIGHT_TRACE,
            color.COSMOS_DARK_TRACE
        )
        
        self.themes = [standard, walnut, blue, checkers, cosmos]
        