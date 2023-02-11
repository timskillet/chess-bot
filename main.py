import pygame
from board import *
from move import *

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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Undo move
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    gs.undoMove()
                    gs.swapTurns()

            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                        moves = gs.getValidMoves()
                        piece = clicks[0].getPiece()
                        newSquare = clicks[1]
                        if newSquare.getPiece():
                            move = Move(piece, newSquare, cp=newSquare.getPiece(), cps=newSquare.getPiece().getSquare())
                        else:
                            move = Move(piece, newSquare)

                        # Make move if valid move
                        if move in moves:
                            gs.makeMove(move)

                            # Evaluate game after move to check for winner
                            gs.swapTurns()
                            if gs.evalGame():
                                exit()
                            squareSelected = []
                            clicks = []

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

        displayBoard(screen, gs)
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


if __name__ == '__main__':
    main()
    pygame.quit()
