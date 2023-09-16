from piece import Knight, Bishop, Queen, Rook

class Promotion :
    def __init__(self,color) -> None:
        self.color = color
        self.array = [Knight(color), Bishop(color), Rook(color), Queen(color)]