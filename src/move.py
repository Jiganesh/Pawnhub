from square import Square
from piece import Piece
class Move:
    def __init__(self, initial:Square, final:Square, final_piece = None) -> None:
        self.initial = initial
        self.final = final
        self.final_piece  = final_piece
        
    def __eq__(self, other) -> bool:
        return self.initial == other.initial and self.final == other.final