from tictactoe import Board
from tictactoe import Player


board1 = Board()
player1 = Player("X", True) #this is our hardcoded opponent
player2 = Player("O") #this will be our learner


whoseTurnIsIt = 1 # 1 = X and 0 = O
while board1.numEmptyPositions > 0:
    if whoseTurnIsIt == 1:
        move = player1.determineNextMove(board1)
        possibleMoves = board1.getEmptyPositions()
        row = possibleMoves[move][0]
        col = possibleMoves[move][1]
        hasWon = board1.makeMove(row, col, player1.designator)
        print()
        board1.printBoard()
        if hasWon == "X":
            print("X has won the game")
            break
        whoseTurnIsIt = 0
    else:
        print("w0= " + str(player2.weight0) + ", w1= " + str(player2.weight1) + ", w2= " + str(player2.weight2) + ", w3= " + str(player2.weight3) + ", w4= " + str(player2.weight4) + ", w5= " + str(player2.weight5))
        player2.updateWeights(board1)
        board1.printBoard()
        print("w0= " + str(player2.weight0) + ", w1= " + str(player2.weight1) + ", w2= " + str(player2.weight2) + ", w3= " + str(player2.weight3) + ", w4= " + str(player2.weight4) + ", w5= " + str(player2.weight5))
        whoseTurnIsIt = 1
