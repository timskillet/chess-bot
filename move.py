from board import *


class Castle:
    """Represents the castle move"""

    def __init__(self, wkc, wqc, bkc, bqc):
        self.whiteKingSideCastle = wkc
        self.whiteQueenSideCastle = wqc
        self.blackKingSideCastle = bkc
        self.blackQueenSideCastle = bqc

    def printCastleRights(self):
        print(self.whiteKingSideCastle, self.whiteQueenSideCastle, self.blackKingSideCastle, self.blackQueenSideCastle)

    def wkcLoseRights(self):
        self.whiteKingSideCastle = False

    def wqcLoseRights(self):
        self.whiteQueenSideCastle = False

    def bkcLoseRights(self):
        self.blackKingSideCastle = False

    def bqcLoseRights(self):
        self.blackQueenSideCastle = False

    def getwkcRights(self):
        return self.whiteKingSideCastle

    def getwqcRights(self):
        return self.whiteQueenSideCastle

    def getbkcRights(self):
        return self.blackKingSideCastle

    def getbqcRights(self):
        return self.blackQueenSideCastle

class Move:
    """Represents a chess move"""

    def __init__(self, p, ns, cp=None, cps=None, enPassant=False, castle=False):
        self.piece = p
        self.square = p.getSquare()
        self.newSquare = ns
        self.capturedPiece = cp
        self.capturedPieceSquare = cps
        self.enPassant = enPassant
        self.castle = castle

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

    def isCastle(self):
        return self.castle

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
