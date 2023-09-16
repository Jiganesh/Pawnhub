
from piece import Piece
class Square :
    
    def __init__(self, row, col, piece = None) -> None:
        self.row = row 
        self.col = col
        self.piece = piece
        
    def __eq__(self, other) -> bool:
        return self.row == other.row and self.col == other.col
        
    def is_empty(self):
        return not self.has_a_piece()
        
    def has_rival (self, color):
        return self.has_a_piece() and self.piece.color != color
        
    def has_ally(self, color):
        return self.has_a_piece() and self.piece.color == color
    
    def is_empty_or_rival(self,color):
        return self.is_empty() or self.has_rival(color)
        
        
    def has_a_piece(self):
        return self.piece != None
    
    @staticmethod
    def in_range(*args):
        for i in args:
            if not (0<=i<8):
                return False
        return True
        
    