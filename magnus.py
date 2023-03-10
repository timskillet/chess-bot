import random


def generateMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findCaptureMoves(validMoves):
    captureMoves = []
    for move in validMoves:
        if move.getCapturedPiece():
            captureMoves.append(move)
    if len(captureMoves) == 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]
    else:
        return captureMoves[random.randint(0, len(captureMoves) - 1)]


def scoreBoard(gs):
    score = 0
    board = gs.getBoard()
    for rank in board:
        for square in rank:
            if square.getPiece():
                if square.getPiece().getColor() == 'white':
                    print(square.getPiece().getName(), "has", str(square.getPiece().getPoints()), "points")
                    score += square.getPiece().getPoints()
                elif square.getPiece().getColor() == 'black':
                    print(square.getPiece().getName(), "has", str(square.getPiece().getPoints()), "points")
                    score -= square.getPiece().getPoints()
    print("Score is", str(score))
    return score


def findBestMove(gs, validMoves):
    if gs.getTurn() == 'white':
        turnMultiplier = 1
    else:
        turnMultiplier = -1
    maxScore = -999
    bestMove = None
    for move in validMoves:
        gs.makeMove(move)
        if gs.isCheckmate():
            score = 1000
        if gs.isStalemate():
            score = 0
        else:
            score = scoreBoard(gs) * turnMultiplier
        if score > maxScore:
            maxScore = score
            bestMove = move
        gs.undoMove()
    return bestMove

