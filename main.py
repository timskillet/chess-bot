import pygame
import time
from board import *
from move import *
import magnus

WIDTH = HEIGHT = 512
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
SQUARE_SIZE = WIDTH // 8
MAX_FPS = 15


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    gs = Gamestate()
    clock = pygame.time.Clock()

    running = True
    squareSelected = []
    clicks = []
    userWhite = False
    userBlack = False
    moves = gs.getValidMoves()
    while running:
        userTurn = (gs.getTurn() == 'white' and userWhite) or (gs.getTurn() == 'black' and userBlack)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Undo move
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    if len(gs.getMoves()) > 0:
                        gs.undoMove()
                        gs.swapTurns()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if userTurn:
                    location = pygame.mouse.get_pos()
                    file = location[0]//SQUARE_SIZE
                    rank = location[1]//SQUARE_SIZE

                    # Reset selected square if clicked twice
                    if squareSelected == gs.getBoard()[file][rank]:
                        squareSelected = []
                        clicks = []
                        continue
                    # Track selected squares
                    else:
                        print("Piece clicked!")
                        squareSelected = gs.getBoard()[file][rank]
                        clicks.append(squareSelected)

                    # Don't move if piece wasn't clicked first
                    if not clicks[0].getPiece():
                        print('Click a piece!')
                        clicks = []

                    # Make move if valid move and switch turns
                    elif len(clicks) == 2:
                        if clicks[0].piece.color == gs.getTurn():
                            print("Generating moves for", gs.getTurn())
                            piece = clicks[0].getPiece()
                            newSquare = clicks[1]
                            oldSquare = clicks[0]
                            if (piece.getName() == 'King') and (abs(newSquare.getFile() - oldSquare.getFile()) >= 2):
                                move = Move(piece, newSquare, castle=True)
                            elif newSquare.getPiece():
                                move = Move(piece, newSquare, cp=newSquare.getPiece(), cps=newSquare.getPiece().getSquare())
                            else:
                                move = Move(piece, newSquare)

                            # Make move if valid move
                            if move in moves:
                                move.printMove()
                                gs.makeMove(move)
                                gs.swapTurns()
                                squareSelected = []
                                clicks = []
                                # Evaluate game
                                moves = gs.getValidMoves()
                                if gs.evalGame(moves):
                                    exit()

                            # Don't move if not a valid move
                            else:
                                print("Not a valid move!")
                                squareSelected = []
                                clicks = []

                        # Player did not select the correct color piece to move
                        else:
                            print(f"It's {gs.getTurn()}'s turn!")
                            squareSelected = []
                            clicks = []

        # AI Move
        if not userTurn:
            time.sleep(1)
            aiMove = magnus.findCaptureMoves(moves)
            gs.makeMove(aiMove)
            gs.swapTurns()
            moves = gs.getValidMoves()

        displayBoard(screen, gs)
        highlightMoves(screen, gs, moves, squareSelected)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def displayBoard(screen, gs):
    """Displays squares and pieces on the chess board"""

    lightSquareColor = pygame.Color(232, 235, 239)
    darkSquareColor = pygame.Color(125, 135, 150)

    for rank in range(8):
        for file in range(8):
            # Draw squares
            if (rank + file) % 2 == 0:
                pygame.draw.rect(screen, lightSquareColor,
                                 pygame.Rect(rank * SQUARE_SIZE, file * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, darkSquareColor,
                                 pygame.Rect(rank * SQUARE_SIZE, file * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Display piece images
            piece = gs.board[rank][file].piece
            if piece:
                screen.blit(pygame.image.load('images/' + piece.color + piece.name + '.png'),
                            pygame.Rect(rank * SQUARE_SIZE, file * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightMoves(screen, gs, validMoves, square):
    """Highlights possible moves for a selected piece"""
    if isinstance(square, Square):
        if square.getPiece():
            file = square.getFile()
            rank = square.getRank()
            # Check that piece color is same as player's turn
            if square.getPiece().getColor() == gs.getTurn():
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(80)
                s.fill(pygame.Color('green'))
                screen.blit(s, (file*SQUARE_SIZE, rank*SQUARE_SIZE))
                s.fill(pygame.Color('yellow'))
                for move in validMoves:
                    if move.getPiece() == square.getPiece():
                        moveSquare = move.getNewSquare()
                        moveFile = moveSquare.getFile()
                        moveRank = moveSquare.getRank()
                        screen.blit(s, (moveFile*SQUARE_SIZE, moveRank*SQUARE_SIZE))


if __name__ == '__main__':
    main()
    pygame.quit()
