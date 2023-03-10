from pieces import *
from move import *


class Gamestate:
    """Chess Board"""

    def __init__(self):
        # Board is indexed by board[column][row] or board[file][rank]
        self.board = [[Square(file, rank) for rank in range(8)] for file in range(8)]
        self.moveLog = []
        self.toMove = 'white'
        self.checked = False
        self.checkmate = False
        self.stalemate = False
        self.enPassantSquare = None
        self.enPassantPiece = None
        self.castlingRights = Castle(True, True, True, True)
        self.castleLog = [Castle(self.castlingRights.getwkcRights(), self.castlingRights.getwqcRights(),
                                 self.castlingRights.getbqcRights(), self.castlingRights.getbqcRights())]

        for i in range(8):
            # Add Pawns
            self.board[i][1].addPiece(Pawn(self.board[i][1], 'black'))
            self.board[i][6].addPiece(Pawn(self.board[i][6], 'white'))

        # Add Rooks
        self.board[0][0].addPiece(Rook(self.board[0][0], 'black'))
        self.board[0][7].addPiece(Rook(self.board[0][7], 'white'))
        self.board[7][0].addPiece(Rook(self.board[7][0], 'black'))
        self.board[7][7].addPiece(Rook(self.board[7][7], 'white'))

        # Add Knights
        self.board[1][0].addPiece(Knight(self.board[1][0], 'black'))
        self.board[1][7].addPiece(Knight(self.board[1][7], 'white'))
        self.board[6][0].addPiece(Knight(self.board[6][0], 'black'))
        self.board[6][7].addPiece(Knight(self.board[6][7], 'white'))

        # Add Bishops
        self.board[2][0].addPiece(Bishop(self.board[2][0], 'black'))
        self.board[2][7].addPiece(Bishop(self.board[2][7], 'white'))
        self.board[5][0].addPiece(Bishop(self.board[5][0], 'black'))
        self.board[5][7].addPiece(Bishop(self.board[5][7], 'white'))

        # Add Queens
        self.board[3][0].addPiece(Queen(self.board[3][0], 'black'))
        self.board[3][7].addPiece(Queen(self.board[3][7], 'white'))

        # Add Kings
        self.board[4][0].addPiece(King(self.board[4][0], 'black'))
        self.board[4][7].addPiece(King(self.board[4][7], 'white'))

    def getBoard(self):
        return self.board

    def getMoves(self):
        return self.moveLog

    def addMove(self, move):
        self.moveLog.append(move)

    def getTurn(self):
        return self.toMove

    def getEnPassantSquare(self):
        return self.enPassantSquare

    def getEnPassantPiece(self):
        return self.enPassantPiece

    def getCastleRights(self):
        return self.castlingRights

    def isCheckmate(self):
        return self.checkmate

    def isStalemate(self):
        return self.stalemate

    def printBoard(self):
        tempBoard = [['--' for i in range(8)] for j in range(8)]
        for i in range(8):
            for square in range(8):
                if self.board[i][square].piece:
                    tempBoard[square][i] = self.board[i][square].piece.name
        for rank in tempBoard:
            print(rank)

    def swapTurns(self):
        """Swaps player turns"""
        if self.toMove == 'white':
            self.toMove = 'black'
            return 'black'
        else:
            self.toMove = 'white'
            return 'white'

    def removeMove(self, n):
        """Removes a move from the move log"""
        for i in range(n):
            self.moveLog.pop()

    def makeMove(self, move):
        """Makes moves and updates the chess board"""
        piece = move.getPiece()
        oldSquare = move.getOldSquare()
        newSquare = move.getNewSquare()
        # Check for en passant move
        if newSquare == self.enPassantSquare:
            # 0. Add move to move log
            enPassantPieceSquare = self.enPassantPiece.getSquare()
            self.moveLog.append(Move(piece, newSquare, cp=self.enPassantPiece, cps=enPassantPieceSquare, enPassant=True))
            # 1. Remove piece from old square
            self.board[oldSquare.getFile()][oldSquare.getRank()].removePiece()
            # 2. Move piece to new square
            move.getPiece().setSquare(move.getNewSquare())
            # 3. Add piece to new square
            self.board[newSquare.getFile()][newSquare.getRank()].setPiece(move.getPiece())
            # 4. Remove captured piece from square
            self.board[enPassantPieceSquare.getFile()][enPassantPieceSquare.getRank()].removePiece()
            # 5. Reset en passant square and pieces
            self.enPassantSquare = None
            self.enPassantPiece = None
            return

        # 1. Remove piece from old square
        self.board[oldSquare.getFile()][oldSquare.getRank()].removePiece()
        # 2. Move piece to new square
        move.getPiece().setSquare(move.getNewSquare())
        # 3. Add piece to new square
        self.board[newSquare.getFile()][newSquare.getRank()].setPiece(move.getPiece())
        # 4. Add move to move log
        self.moveLog.append(move)
        # 5. Update en passant not possible after move is made
        self.enPassantSquare = None
        self.enPassantPiece = None

        # Special Pawn Moves
        if piece.getName() == 'Pawn':
            # Two square pawn advance allows for en passant capture
            if abs(oldSquare.getRank() - newSquare.getRank()) == 2:
                self.enPassantSquare = self.board[oldSquare.getFile()][(oldSquare.getRank() + newSquare.getRank())//2]
                self.enPassantPiece = piece

            # Pawn Promotion
            if (piece.getColor() == 'white' and piece.getSquare().getRank() == 0) or (piece.getColor() == 'black' and piece.getSquare().getRank() == 7):
                newPiece = Queen(piece.getSquare(), piece.getColor())
                self.board[newSquare.getFile()][newSquare.getRank()].setPiece(newPiece)

        # Castle move
        if move.isCastle():
            oldSquare = move.getOldSquare()
            newSquare = move.getNewSquare()
            newFile = newSquare.getFile()
            newRank = newSquare.getRank()
            # King side castle move rook
            if newSquare.getFile() - oldSquare.getFile() == 2:
                rook = self.board[newFile+1][newRank].getPiece()
                newRookSquare = self.board[newFile-1][newRank]
                # 1. Remove piece from old rook square
                rook.getSquare().removePiece()
                # 2. Set square for rook
                rook.setSquare(newRookSquare)
                # 3. Set rook to new square piece
                newRookSquare.setPiece(rook)

            # Queen side castle move rook
            elif newSquare.getFile() - oldSquare.getFile() == -2:
                rook = self.board[newFile-2][newRank].getPiece()
                newRookSquare = self.board[newFile+1][newRank]
                # 1. Remove piece from old rook square
                rook.getSquare().removePiece()
                # 2. Set square for rook
                rook.setSquare(newRookSquare)
                # 3. Set rook to new square piece
                newRookSquare.setPiece(rook)

        # Castling rights
        self.updateCastleRights(move)
        self.castleLog.append(Castle(self.castlingRights.getwkcRights(), self.castlingRights.getwqcRights(),
                                     self.castlingRights.getbkcRights(), self.castlingRights.getbqcRights()))

    def undoMove(self):
        """Reverts chessboard back to last move"""
        if len(self.moveLog) != 0:
            lastMove = self.moveLog[-1]
            oldSquare = lastMove.getOldSquare()
            newSquare = lastMove.getNewSquare()

            # Undo castle rights
            # 1. Remove updated castle rights
            self.castleLog.pop()
            # 2. Revert back to previous castle rights
            prevCastle = self.castleLog[-1]
            self.castlingRights = Castle(prevCastle.getwkcRights(), prevCastle.getwqcRights(),
                                         prevCastle.getbkcRights(), prevCastle.getbqcRights())

            # 3. Move piece back to original square
            undoMove = Move(lastMove.getPiece(), lastMove.getOldSquare())
            self.makeMove(undoMove)
            self.castleLog.pop()
            prevCastle = self.castleLog[-1]
            self.castlingRights = Castle(prevCastle.getwkcRights(), prevCastle.getwqcRights(),
                                         prevCastle.getbkcRights(), prevCastle.getbqcRights())

            # 4. Return captured piece if captured piece
            if lastMove.getCapturedPiece():
                undoCapture = Move(lastMove.getCapturedPiece(), lastMove.getCapturedPieceSquare())
                self.makeMove(undoCapture)
                self.castleLog.pop()
                prevCastle = self.castleLog[-1]
                self.castlingRights = Castle(prevCastle.getwkcRights(), prevCastle.getwqcRights(),
                                             prevCastle.getbkcRights(), prevCastle.getbqcRights())
                self.removeMove(1)
            self.removeMove(2)

            # Undo en passant move
            if lastMove.isEnPassantMove():
                # Remove piece from new square
                newSquare = lastMove.getNewSquare()
                self.board[newSquare.getFile()][newSquare.getRank()].removePiece()
                lastMove.getOldSquare().setPiece(lastMove.getPiece())
                lastMove.getPiece().setSquare(lastMove.getOldSquare())
                self.enPassantSquare = newSquare
                self.enPassantPiece = lastMove.getCapturedPiece()

            # Undo two square pawn advance
            if lastMove.getPiece().getName() == 'Pawn' and abs(oldSquare.getRank() - newSquare.getRank()) == 2:
                self.enPassantSquare = None
                self.enPassantPiece = None

            # Undo castle move
            if lastMove.isCastle():
                # King side castle
                if newSquare.getFile() - oldSquare.getFile() == 2:
                    rook = self.board[newSquare.getFile()-1][newSquare.getRank()].getPiece()
                    self.board[newSquare.getFile()+1][newSquare.getRank()].setPiece(rook)
                    self.board[newSquare.getFile()-1][newSquare.getRank()].removePiece()
                # Queen side castle
                else:
                    rook = self.board[newSquare.getFile()+1][newSquare.getRank()].getPiece()
                    self.board[newSquare.getFile()-2][newSquare.getRank()].setPiece(rook)
                    self.board[newSquare.getFile()+1][newSquare.getRank()].removePiece()

    def allPossibleMoves(self):
        """Generates a list of all possible moves that can be made by a player"""
        moves = []
        for rank in range(8):
            for file in range(8):
                if self.board[rank][file].getPiece():
                    color = self.board[rank][file].getPiece().getColor()
                    piece = self.board[rank][file].getPiece()
                    if color == self.toMove:
                        piece.availableMoves(self, moves, self.toMove)
        return moves

    def getValidMoves(self):
        """Filters moves that leave king in check from all possible moves"""
        enPassantSquare = self.enPassantSquare
        enPassantPiece = self.enPassantPiece
        # 1. Generate all possible moves
        allMoves = self.allPossibleMoves()
        # Add castle moves to allMoves
        self.getKingPosition().getPiece().castleMoves(gs=self, moves=allMoves, toMove=self.toMove)
        # 2. Simulate all possible moves
        for i in range(len(allMoves)-1, -1, -1):
            self.makeMove(allMoves[i]) # Simulating current move
            # 3. Get king location after making move
            currKingLocation = self.getKingPosition()
            # 4. Generate all possible moves for opponent
            self.swapTurns()
            oppMoves = self.allPossibleMoves()
            # 5. Simulate all possible moves for opponent
            for oppMove in oppMoves:
                # 6. If opponent move can capture king after current move, then remove that move
                if oppMove.getNewSquare() == currKingLocation:
                    allMoves.remove(allMoves[i])
                    self.checked = True
                    break
            self.swapTurns()
            self.undoMove()
            self.enPassantSquare = enPassantSquare
            self.enPassantPiece = enPassantPiece
        return allMoves

    def getKingPosition(self):
        """Retrieves the location of king of current player's turn"""
        for rank in range(8):
            for file in range(8):
                if self.board[rank][file].getPiece():
                    piece = self.board[rank][file].getPiece()
                    if piece.getName() == 'King' and piece.getColor() == self.toMove:
                        return piece.getSquare()

    def check(self):
        return not self.safeSquare(self.getKingPosition())

    def safeSquare(self, square):
        self.swapTurns()
        opponentMoves = self.allPossibleMoves()
        self.swapTurns()
        for move in opponentMoves:
            newSquare = move.getNewSquare()
            if (newSquare.getRank() == square.getRank()) and (newSquare.getFile() == square.getFile()):
                return False
        return True

    def updateCastleRights(self, move):
        """Updates the current gamestate's castling rights"""
        piece = move.getPiece()
        oldSquare = move.getOldSquare()
        # Lose castle rights if white king moves
        if (piece.getName() == 'King') and (piece.getColor() == 'white'):
            self.castlingRights.wkcLoseRights()
            self.castlingRights.wqcLoseRights()
        # Lose castle rights if black king moves
        elif (piece.getName() == 'King') and (piece.getColor() == 'black'):
            self.castlingRights.bkcLoseRights()
            self.castlingRights.bqcLoseRights()
        elif (piece.getName() == 'Rook') and (piece.getColor() == 'white'):
            # Lose white queen side castle rights if queen side rook moves
            if (oldSquare.getRank() == 7) and (oldSquare.getFile() == 0):
                self.castlingRights.wqcLoseRights()
            # Lose white king side castle rights if king side rook moves
            elif (oldSquare.getRank() == 7) and (oldSquare.getFile() == 7):
                self.castlingRights.wkcLoseRights()
        elif (piece.getName() == 'Rook') and (piece.getColor() == 'black'):
            # Lose black queen side castle rights if queen side rook moves
            if (oldSquare.getRank() == 0) and (oldSquare.getFile() == 0):
                self.castlingRights.bqcLoseRights()
            # Lose black king side castle rights if king side rook moves
            elif (oldSquare.getRank() == 0) and (oldSquare.getFile() == 7):
                self.castlingRights.bkcLoseRights()

    def evalGame(self, validMoves):
        """Check for checkmate or stalemate after move and switching turns"""
        gameOver = False
        print(f"Number of moves remaining for {self.toMove}: {len(validMoves)}")
        if len(validMoves) == 0:
            gameOver = True
            if self.check():
                self.checkmate = True
                print(self.swapTurns(), "wins!")
            else:
                self.stalemate = True
                print("Stalemate!")
        return gameOver


class Square:
    """Represents a square on a chess board"""

    colsToFiles = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    filesToCols = {file: col for col, file in colsToFiles.items()}
    rowsToRanks = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    ranksToRows = {rank: row for row, rank in rowsToRanks.items()}

    def __init__(self, file, rank, piece=None):
        self.file = file
        self.rank = rank
        self.piece = piece
        self.position = self.colsToFiles[file] + self.rowsToRanks[rank]

    # Override equals operator to check if squares are equivalent
    def __eq__(self, other):
        if isinstance(other, Square):
            return self.file == other.file and self.rank == other.rank
        else:
            return False

    def addPiece(self, piece):
        self.piece = piece

    def removePiece(self):
        self.piece = None

    def getPiece(self):
        return self.piece

    def setPiece(self, piece):
        self.piece = piece

    def getPosition(self):
        return self.position

    def getRank(self):
        return self.rank

    def getFile(self):
        return self.file
