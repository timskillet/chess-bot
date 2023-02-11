from board import *
from move import *


class Piece:
    """Parent class for all chess pieces"""
    canMove = False
    name = 'Piece'
    directions = []

    def __init__(self, sq, c):
        self.square = sq
        self.color = c

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

    def getSquare(self):
        return self.square

    def setSquare(self, sq):
        self.square = sq

    def removeSquare(self):
        self.square = None

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a piece given its location on the chessboard"""
        board = gs.getBoard()
        for direction in self.directions:
            for i in range(1, 9):
                newFile = self.square.getFile() + direction[0] * i
                newRank = self.square.getRank() + direction[1] * i
                if 0 <= newFile <= 7 and 0 <= newRank <= 7:
                    newSquare = board[newFile][newRank]
                    # If square is empty, then can move
                    if not board[newFile][newRank].getPiece():
                        move = Move(self, newSquare)
                        moves.append(move)
                    # If square has diff color piece, then can move
                    elif newSquare.piece.color != self.color:
                        move = Move(self, newSquare, cp=newSquare.getPiece(),
                                    cps=newSquare.getPiece().getSquare())
                        moves.append(move)
                        break
                    # If blocked by same color piece, then can't move further
                    else:
                        break
                else:
                    break


class Pawn(Piece):
    """Represents a pawn"""
    white_directions = [(0, -1), (0, -2), (-1, -1), (1, -1)]
    black_directions = [(0, 1), (0, 2), (-1, 1), (1, 1)]
    enPassantDirections = [(-1, 0), (1, 0)]
    name = "Pawn"
    abbrev = ''
    points = 1
    enPassantCapture = False

    def __init__(self, square, color):
        super().__init__(square, color)

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a pawn given its location on the chessboard"""
        if toMove == 'white':
            directions = self.white_directions
        else:
            directions = self.black_directions

        # Move forward one square
        newFile = self.square.getFile() + directions[0][0]
        newRank = self.square.getRank() + directions[0][1]
        newSquare = gs.getBoard()[newFile][newRank]
        if 0 <= newFile <= 7 and 0 <= newRank <= 7:
            # If square is empty, then can move
            if not newSquare.getPiece():
                move = Move(self, newSquare)
                moves.append(move)
                # Move two spaces if not moved
                if (self.square.getRank() == 6 and self.color == 'white') or (self.square.getRank() == 1 and self.color == 'black'):
                    newFile = self.square.getFile() + directions[1][0]
                    newRank = self.square.getRank() + directions[1][1]
                    newSquare = gs.getBoard()[newFile][newRank]
                    if not newSquare.getPiece():
                        moves.append(Move(self, newSquare))

        # Check for diagonal and en passant captures
        for direction in directions[2:]:
            newFile = self.square.getFile() + direction[0]
            newRank = self.square.getRank() + direction[1]
            if 0 <= newFile <= 7 and 0 <= newRank <= 7:
                newSquare = gs.getBoard()[newFile][newRank]
                # If diagonal square is occupied by opponent piece, then can capture
                if newSquare.getPiece():
                    if newSquare.getPiece().getColor() != self.color:
                        moves.append(Move(self, newSquare, cp=newSquare.getPiece(),
                                          cps=newSquare.getPiece().getSquare()))
                # If diagonal square is empty, check for en passant capture
                elif newSquare == gs.getEnPassantSquare() and gs.getEnPassantPiece().getColor() != self.color:
                    moves.append(Move(self, newSquare, cp=gs.getEnPassantPiece(),
                                      cps=gs.getEnPassantPiece().getSquare(), enPassant=True))

        # # En passant
        # if gs.canEnPassant():
        #     newFile = self.square.getFile() + directions[-1][0]
        #     newRank = self.square.getRank() + directions[-1][1]
        #     if 0 <= newFile <= 7 and 0 <= newRank <= 7:
        #         newSquare = gs.getBoard()[newFile][newRank]
        #         piece = newSquare.getPiece()
        #         # If square beside piece is occupied by opponent piece, then can en Passant capture
        #         if piece:
        #             if piece.getColor() != self.color and piece.getName() == 'Pawn':
        #                 if piece.enPassantCapture:
        #                     moves.append(Move(self, newSquare, cp=newSquare.getPiece(),
        #                                       cps=newSquare.getPiece().getSquare()))

class Knight(Piece):
    """Represents a knight"""
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    name = "Knight"
    abbrev = 'N'
    points = 3

    def __init__(self, square, color):
        super().__init__(square, color)

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a knight given its location on the chessboard"""
        for direction in self.directions:
            newFile = self.square.getFile() + direction[0]
            newRank = self.square.getRank() + direction[1]
            if 0 <= newFile <= 7 and 0 <= newRank <= 7:
                newSquare = gs.getBoard()[newFile][newRank]
                # If square is empty, then can move
                if not newSquare.getPiece():
                    moves.append(Move(self, newSquare))
                # If square is occupied by opponent piece, then can move
                elif newSquare.getPiece().getColor() != self.color:
                    moves.append(Move(self, newSquare, cp=newSquare.getPiece(),
                                      cps=newSquare.getPiece().getSquare()))
                # If blocked by same color piece, then can't move

class Bishop(Piece):
    """Represents a bishop"""
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    name = "Bishop"
    abbrev = 'B'
    points = 3

    def __init__(self, square, color):
        super().__init__(square, color)

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a bishop given its location on the chessboard"""
        super().availableMoves(gs, moves, toMove)


class Rook(Piece):
    """Represents a rook"""
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    name = "Rook"
    abbrev = 'R'
    points = 5

    def __init__(self, square, color):
        super().__init__(square, color)

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a rook given its location on the chessboard"""
        super().availableMoves(gs, moves, toMove)


class Queen(Piece):
    """Represents a queen"""
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    name = "Queen"
    abbrev = 'Q'
    points = 9

    def __init__(self, square, color):
        super().__init__(square, color)

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a queen given its location on the chessboard"""
        super().availableMoves(gs, moves, toMove)


class King(Piece):
    """Represents a king"""
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    name = "King"
    abbrev = 'K'

    def __init__(self, square, color):
        super().__init__(square, color)

    def availableMoves(self, gs, moves, toMove):
        """Generates a list of possible moves for a king given its location on the chessboard"""
        for direction in self.directions:
            newFile = self.square.getFile() + direction[0]
            newRank = self.square.getRank() + direction[1]
            if 0 <= newFile <= 7 and 0 <= newRank <= 7:
                newSquare = gs.getBoard()[newFile][newRank]
                # If square is empty, then can move
                if not newSquare.getPiece():
                    moves.append(Move(self, newSquare))
                # If square is occupied by opponent piece, then can move
                elif newSquare.getPiece().getColor() != self.color:
                    moves.append(Move(self, newSquare, cp=newSquare.getPiece(),
                                      cps=newSquare.getPiece().getSquare()))
