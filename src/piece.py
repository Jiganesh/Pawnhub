from const import WHITE, BLACK
class Piece:
    
    def __init__(self, name, color, value, texture=None, texture_rect = None) -> None:
        self.name = name
        self.color = color.lower()
        self.moved = False
        self.value = value * 1 if color == WHITE else -1
        self.texture = None
        self.set_texture()
        self.texture_rect = texture_rect
        self.moves = []
        
    def set_texture(self, size = 80):
        file_path =  f"assets/images/imgs-{size}px/{self.color}_{self.name}.png"
        self.texture = file_path     
    
    def add_move(self, move):
        self.moves.append(move)
        
    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    def __init__(self, color) -> None:
        self.en_passant = False
        
        if color == BLACK:
            self.direction = 1
        else:
            self.direction = -1
            
        super().__init__("pawn", color, 1.0)
        
        
class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color, 3.00)
        
class Bishop(Piece):
    def __init__(self, color):
        super().__init__("bishop", color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color, 5.0)
        
class Queen(Piece):
    def __init__(self, color):
        super().__init__("queen", color, 9.0)
    
class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", color, float("inf"))
        
        

