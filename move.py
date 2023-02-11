from board import *

class Move:
    """Represents a chess move"""

    def __init__(self, p, ns, cp=None, cps=None, enPassant=False):
        self.piece = p
        self.square = p.getSquare()
        self.newSquare = ns
        self.capturedPiece = cp
        self.capturedPieceSquare = cps
        self.enPassant = enPassant

    def getPiece(self):
        return self.piece

    def getOldSquare(self):
        return self.square

    def getNewSquare(self):
        return self.newSquare

    def getCapturedPiece(self):
        return self.capturedPiece

    def getCapturedPieceSquare(self):
        return self.capturedPieceSquare

    def isEnPassantMove(self):
        return self.enPassant

    def printMove(self):
        if self.capturedPiece:
            print(self.piece.getName(), "on", self.piece.getSquare().getPosition(), "to", self.newSquare.getPosition(), "and takes", self.capturedPiece.getName())
        else:
            print(self.piece.getName(), "on", self.piece.getSquare().getPosition(), "to", self.newSquare.getPosition())

    # Override equals operator to check for valid move
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.square == other.square and self.newSquare == other.newSquare
        else:
            return False
