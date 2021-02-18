from tictactoe import Board
from tictactoe import Player
#Training details
training = True
epochs = 200000
numXWins = 0
numOWins = 0

#Setup the game
player1 = Player("X", True) #this is our hardcoded opponent
player2 = Player("O") #this will be our learner


#--MAIN--
if training:
    for training_count in range(epochs):
        print("Currently playing game: " + str(training_count + 1))
        whoseTurnIsIt = 1 # 1 = X and 0 = O
        #create a new board
        board1 = Board()
        while board1.numEmptyPositions > 0:
            if whoseTurnIsIt == 1:
                hasWon = player1.updateWeights(board1)
                if hasWon == "X":
                    numXWins += 1
                    #print("Player 2 function: " + str(player2.weight0) + " " + str(player2.weight1) + " " + str(player2.weight2))
                    #delete the board object
                    del board1
                    break
                elif hasWon == "O":
                    numOWins += 1
                    #delete the board object
                    del board1
                    break
                else:
                    pass
                whoseTurnIsIt = 0
            else:
                hasWon = player2.updateWeights(board1)
                if hasWon == "X":
                    numXWins += 1
                    #print("Player 2 function: " + str(player2.weight0) + " " + str(player2.weight1) + " " + str(player2.weight2))
                    #delete the board object
                    del board1
                    break
                elif hasWon == "O":
                    numOWins += 1
                    #print("Player 2 function: " + str(player2.weight0) + " " + str(player2.weight1) + " " + str(player2.weight2))
                    #delete the board object
                    del board1
                    break
                else:
                    pass
                #board1.printBoard()
                whoseTurnIsIt = 1
    print("Times X won: " + str(numXWins))
    print("Times O won: " + str(numOWins))
    print("Draws: " + str(epochs - (numXWins + numOWins)))
    # print("Player 2 function: " + str(player2.weight0) + " " + str(player2.weight1) + " " + str(player2.weight2) + " " + str(player2.weight3))
else:
    pass
