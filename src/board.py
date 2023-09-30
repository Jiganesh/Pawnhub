from const import ROWS, COLS
from const import BLACK, WHITE
from square import Square
from move import Move
from sound import Sound
import os

import copy
from piece import Pawn, Rook, Knight, Bishop, Queen, King

class Board :
    
    def __init__(self):
        
        self.squares = [[ Square(row, col) for col in range (COLS)] for row in range(ROWS) ]
        self.add_pieces()
        self.last_move = None
        self.pawn_promotion = None
        
    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True
                            
    def move(self, piece, move, testing = False):
        initial = move.initial
        final = move.final
        
        en_passant_empty = self.squares[final.row][final.col].is_empty()
        
        captured = self.squares[final.row][final.col].has_a_piece()
        
        
        # LOGIC OF PAWNHUB
        
        initial_piece = self.squares[initial.row][initial.col].piece
        self.squares[initial.row][initial.col].piece = None

        if final.row ==0 or final.row==7 and initial_piece.name == "pawn"  :
            self.squares[final.row][final.col].piece = piece
        elif captured and initial_piece.name != "king":
            self.squares[final.row][final.col].piece = Pawn(piece.color)
        else : 
            self.squares[final.row][final.col].piece = piece
            
        # LOGIC OF TRADITIONAL CHESS 
        
        # self.squares[initial.row][initial.col].piece = None
        # self.squares[final.row][final.col].piece = piece

            
        

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(
                        os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            
            # pawn promotion
            else:
                self.check_promotion(piece, final)
        
        
        
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
        
        piece.moved = True
        piece.clear_moves()
        self.last_move = move
        
    def en_passant(self, initial, final):
        return abs(initial.row - final.row)
        
    def in_check(self, piece, move):
        
        temp_board = copy.deepcopy(self)
        temp_piece = copy.deepcopy(piece)
        
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival(temp_piece.color):
                    enemy_piece = temp_board.squares[row][col].piece
                    
                    temp_board.calc_moves(enemy_piece, row, col, False)
                    for predicted_move in enemy_piece.moves:
                        
                        final_row, final_col = predicted_move.final.row, predicted_move.final.col

                        if isinstance(temp_board.squares[final_row][final_col].piece, King):
                            return True
        return False        
        
    def check_promotion(self, piece, final):
        
        if final.row == 0 or final.row == 7:
            self.pawn_promotion = True
            
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
        
    def valid_move (self, piece, move):
        return move in piece.moves
     
    def calc_moves(self, piece, row, col, bool):
        
        def pawn_moves():
            
            steps = 1 if piece.moved == True else 2
            
            # possible moves moving forward
                        
            starting_point = row + piece.direction 
            ending_point = row + (piece.direction * (steps+1)) # (steps +1) as in range end is exclusive
                        
            for possible_move_row in range(starting_point, ending_point, piece.direction):
                
                if Square.in_range(possible_move_row):
                    
                    if self.squares[possible_move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        if bool : 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
                    else: # piece is blocked as something is in front of it
                        break
                else: # no square available to move forward
                    break
                
            # possible diagonal kill moves
            
            possible_move_row = row + piece.direction
            possible_move_cols = [col-1, col+1]
            
            for possible_move_col in possible_move_cols:
                
                if Square.in_range(possible_move_row, possible_move_col) and self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                    initial = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final = Square(possible_move_row, possible_move_col, final_piece)
                    move = Move(initial, final)
                    if bool : 
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
               
               
            # LEFT EN PASSANT          
            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5
            #left en_passant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col-1].has_rival(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            move = Move(initial, final)
                            
                            if bool : 
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                
            # RIGHT EN PASSANT          
            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5
            #left en_passant
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col+1].has_rival(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            move = Move(initial, final)
                            
                            if bool : 
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            
                        
                    

                
        def rook_moves():
            
            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ]
            
            for x, y in directions:
                possible_moves_row = row
                possible_moves_col = col
                
                while Square.in_range(possible_moves_row, possible_moves_col):
                    
                    if possible_moves_row == row and possible_moves_col == col:
                        pass
                    
                    elif self.squares[possible_moves_row][possible_moves_col].has_ally(piece.color):
                        break
                
                    elif self.squares[possible_moves_row][possible_moves_col].has_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row, possible_moves_col, final_piece)
                        move = Move(initial, final)
                        if bool : 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                        break
                    
                    elif self.squares[possible_moves_row][possible_moves_col].is_empty():
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row, possible_moves_col, final_piece)

                        move = Move(initial, final)
                        if bool : 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                            
                    possible_moves_row+=x
                    possible_moves_col+=y
                    

        
        def bishop_moves():
            
            directions = [
                (1, 1),
                (-1, -1),
                (1, -1),
                (-1, 1)
            ]
            
            for x, y in directions:
           
                possible_moves_row = row
                possible_moves_col = col
                
                while Square.in_range(possible_moves_row, possible_moves_col):
                    
                    if possible_moves_row == row and possible_moves_col == col:
                        pass
                    
                    elif self.squares[possible_moves_row][possible_moves_col].has_ally(piece.color):
                        break
                
                    elif self.squares[possible_moves_row][possible_moves_col].has_rival(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row, possible_moves_col)
                        move = Move(initial, final, final_piece)
                        
                        if bool : 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                        break
                    
                    elif self.squares[possible_moves_row][possible_moves_col].is_empty():
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row, possible_moves_col, final_piece)
                        move = Move(initial, final, final_piece)
                        
                        if bool : 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                        
                    possible_moves_row+=x
                    possible_moves_col+=y

                
        def knight_moves():
            possible_moves = [
                (row + 2, col + 1),
                (row + 2, col -1),
                (row -2,  col + 1),
                (row -2,  col -1),
                (row + 1, col + 2),
                (row + 1, col -2),
                (row -1,  col + 2),
                (row -1,  col -2)
            ]
            
            for possible_row, possible_col in possible_moves:
                if Square.in_range(possible_row, possible_col) and self.squares[possible_row][possible_col].is_empty_or_rival(piece.color):
                    # Square of new move
                    initial = Square(row, col)
                    final = Square(possible_row, possible_col)
                    final_piece = self.squares[possible_row][possible_col].piece
                    # Create new move
                    move = Move(initial, final, final_piece) 
                    if bool : 
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                        else:
                            break
                    else:
                        piece.add_move(move)

        def king_moves():
            
            
            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (1, 1),
                (-1, -1),
                (1, -1),
                (-1, 1)
            ]
            for x , y in directions:
                possible_row = row + x
                possible_col = col + y
                
                if Square.in_range(possible_row, possible_col) and self.squares[possible_row][possible_col].is_empty_or_rival(piece.color):
                    # Square of new move
                    initial = Square(row, col)
                    final = Square(possible_row, possible_col)
                    
                    # Create new move
                    move = Move(initial, final)
                    if bool : 
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    
            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_a_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_a_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)                

        if isinstance(piece, Pawn):
            pawn_moves()
            
        if isinstance(piece, Rook):
            rook_moves()
        
        if isinstance(piece, Knight):
            knight_moves()
        
        if isinstance(piece, Bishop): 
            bishop_moves()
        
        if isinstance(piece, Queen):
            rook_moves()
            bishop_moves()
        
        if isinstance(piece, King):
            king_moves()
            
            
            
    def add_pieces(self):
        
        # Loading white pieces
        
        # Pawns
        pawn_row  = 6
        for col in range (COLS):
            self.squares[pawn_row][col].piece = Pawn(WHITE)
            
            
        # --------------------------- DELETE BELOW CODE ONCE DONE ---------------------
        # self.squares[5][1].piece = Pawn(BLACK)
        # self.squares[4][3].piece = Queen(BLACK)
        # self.squares[3][4].piece = King(BLACK)
        # self.squares[3][3].piece = Queen(WHITE)
        # self.squares[5][2].piece = Queen(BLACK)
        # self.squares[4][7].piece = Rook(WHITE)
        # self.squares[5][6].piece = Bishop(BLACK)
        # self.squares[2][2].piece = Pawn(WHITE)
        #---------------------------------------------------------------------------------
        master_row = 7  
        # Rooks
        self.squares[master_row][0].piece = Rook(WHITE)
        self.squares[master_row][-1].piece = Rook(WHITE)
        
        #Knights
        self.squares[master_row][1].piece = Knight(WHITE)
        self.squares[master_row][-2].piece = Knight(WHITE)
        
        #Bishops
        self.squares[master_row][2].piece = Bishop(WHITE)
        self.squares[master_row][-3].piece = Bishop(WHITE)
        
        #Queen
        self.squares[master_row][3].piece= Queen(WHITE)
        
        #King
        self.squares[master_row][4].piece = King(WHITE)
        
        
        
        # Loading black Pieces
        
        # Pawns
        pawn_row  = 1
        for col in range (COLS):
            self.squares[pawn_row][col].piece = Pawn(BLACK)
            
        master_row = 0  
        # Rooks
        self.squares[master_row][0].piece = Rook(BLACK)
        self.squares[master_row][-1].piece = Rook(BLACK)
        
        #Knights
        self.squares[master_row][1].piece = Knight(BLACK)
        self.squares[master_row][-2].piece = Knight(BLACK)
        
        #Bishops
        self.squares[master_row][2].piece = Bishop(BLACK)
        self.squares[master_row][-3].piece = Bishop(BLACK)
        
        #Queen
        self.squares[master_row][3].piece= Queen(BLACK)
        
        #King
        self.squares[master_row][4].piece = King(BLACK)
        
        
