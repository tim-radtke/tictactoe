import copy
import numpy as np
from numpy import random

class Player:
    def __init__(self, piece, hardcoded = False):
        self.designator = piece
        if hardcoded:
            self.weight0 = 1
            self.weight1 = 0.1
            self.weight2 = 0.7
            self.weight3 = 0.3
            self.weight4 = 1
            self.weight5 = 0.5
            self.c = 0.1
        else:
            self.weight0 = random.rand()
            self.weight1 = random.rand()
            self.weight2 = random.rand()
            self.weight3 = random.rand()
            self.weight4 = random.rand()
            self.weight5 = random.rand()
            self.c = 0.1

    def calculateVHat(self, board):
        #our funciton is in the form w0 + w1*f1 + w2*f2 + w3*f3 + w4*f4 + w5*f5
        #where f1 -> number of empty spaces on the board
        #where f2 -> number of Xes on the board
        #where f3 -> number of Oes on the board
        #where f4 -> number of double Xes on the board
        #where f5 -> number of double Oes on the board
        vHat = self.weight0 + (self.weight1 * board.numEmptyPositions) + (self.weight2 * board.numXes) + (self.weight3 * board.numOes) + (self.weight4 * board.numDoubleXes) + (self.weight5 * board.numDoubleOes)
        return vHat

    def updateWeights(self, board):
        #the first thing we need to do is calculate the error
        #to do so we need the current board's vhat and our next move's vHat
        vHatCurrentBoard = self.calculateVHat(board)
        #now we need to actually make the next move so we can determine it's vHat
        move = self.determineNextMove(board)
        possibleMoves = board.getEmptyPositions()
        row = possibleMoves[move][0]
        col = possibleMoves[move][1]
        #this will update the main board object on the top level since it is passed as mutable
        hasWon = board.makeMove(row, col, self.designator)
        if hasWon == self.designator:
            #Show on the terminal who won the game if someone wins the game during this move
            print(self.designator + " has won the game!")
        vHatNextMove = self.calculateVHat(board)
        #calculate the error using the formula given in class
        error = vHatNextMove - vHatCurrentBoard

        #now we can move on to updating the weights for our player
        self.weight1 = self.weight1 + (self.c * board.numEmptyPositions * error)
        self.weight2 = self.weight2 + (self.c * board.numXes * error)
        self.weight3 = self.weight3 + (self.c * board.numOes * error)
        self.weight4 = self.weight4 + (self.c * board.numDoubleXes * error)
        self.weight5 = self.weight5 + (self.c * board.numDoubleOes * error)

    def determineNextMove(self, board):
        #We need to go through each of the successors and determine which one maximises or
        #mininimises Vhat depending on if we are X or O
        vHatMax = -10000000
        vHatMin = 10000000
        #get all the successors for the current board
        successors = board.getSuccessors(self.designator)
        #determine the Vhats for each one
        index = 0
        moveIndexMax = 0 #keep track of the index to determine which move to make later
        moveIndexMin = 0 #keep track of the index to determine which move to make later
        for move in successors:
            tempVhat = self.calculateVHat(move)
            if tempVhat > vHatMax:
                vHatMax = tempVhat
                #save the index
                moveIndexMax = index
            if tempVhat < vHatMin:
                vHatMax = tempVhat
                #save the index
                moveIndexMin = index
            index += 1

        #if we are X then we want the max and if we are O then we want the min
        if self.designator == "X":
            return moveIndexMax
        else:
            return moveIndexMin


class Board:
    def __init__(self):
        self.positions = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.numEmptyPositions = 9
        self.numXes = 0
        self.numOes = 0
        self.numDoubleXes = 0
        self.numDoubleOes = 0

    def getEmptyPositions(self):
        emptyPositionsArray = []
        for row in range(3):
            for column in range(3):
                if self.positions[row][column] == " ":
                    emptyPositionsArray.append((row, column))
        return emptyPositionsArray

    def getSuccessors(self, turn):
        loop_counter = self.numEmptyPositions
        empty_positions = self.getEmptyPositions()
        #Create the array of successors to return
        successors = []
        for i in range(loop_counter):
            successors.append(copy.deepcopy(self))

        i = 0
        for someBoard in successors:
            row = (empty_positions[i])[0]
            col = (empty_positions[i])[1]
            someBoard.makeMove(row, col, turn)
            i += 1

        return successors


    def determineDouble(self, turn):
        doubleCount = 0
        #There has to be a better way to do this, but for now this works
        if self.positions[0][0] == turn:
            #need to look at (1,0), (0,1), and (1,1)
            if self.positions[1][0] == turn:
                doubleCount += 1
            if self.positions[0][1] == turn:
                doubleCount += 1
            if self.positions[1][1] == turn:
                doubleCount += 1
        if self.positions[0][1] == turn:
            #need to look at (0,2) and (1,1)
            if self.positions[0][2] == turn:
                doubleCount += 1
            if self.positions[1][1] == turn:
                doubleCount += 1
        if self.positions[0][2] == turn:
            #need to look at (1,2) (1,1)
            if self.positions[1][2] == turn:
                doubleCount += 1
            if self.positions[1][1] == turn:
                doubleCount += 1
        if self.positions[1][0] == turn:
            #need to look at (1,1) (2,0)
            if self.positions[1][1] == turn:
                doubleCount += 1
            if self.positions[2][0] == turn:
                doubleCount += 1
        if self.positions[1][1] == turn:
            #need to look at (1,2) (2,0) (2,1) (2,2)
            if self.positions[1][2] == turn:
                doubleCount += 1
            if self.positions[2][0] == turn:
                doubleCount += 1
            if self.positions[2][1] == turn:
                doubleCount += 1
            if self.positions[2][2] == turn:
                doubleCount += 1
        if self.positions[1][2] == turn:
            #need to look at (2,2)
            if self.positions[2][2] == turn:
                doubleCount += 1
        if self.positions[2][0] == turn:
            #need to look at (2,1)
            if self.positions[2][1] == turn:
                doubleCount += 1
        if self.positions[2][1] == turn:
            #need to look at (2,2)
            if self.positions[2][2] == turn:
                doubleCount += 1
        #do not need to check positions at 2,2 because if there is a double there it has
        #already been accounted for.
        return doubleCount

    def makeMove(self, row, column, whosTurn):
        if whosTurn == "X":
            self.positions[row][column] = "X"
            self.numXes += 1
            self.numDoubleXes = self.determineDouble("X")
        else:
            self.positions[row][column] = "O"
            self.numOes += 1
            self.numDoubleOes = self.determineDouble("O")
        #we have made a move so decrease the number of empty positions
        self.numEmptyPositions -= 1
        #check to see if anyone has won and return that value if one exists
        win = self.checkForWin()
        if win == "X" or win == "O":
            return win
        else:
            return "NO WIN"


    def checkForWin(self):
        # check the rows
        for x in range(3):
            row = set([self.positions[x][0], self.positions[x][1], self.positions[x][2]])
            if len(row) == 1 and self.positions[x][0] != " ":
                return self.positions[x][0]

        #check the columns
        for x in range(3):
            col = set([self.positions[0][x], self.positions[1][x], self.positions[2][x]])
            if len(col) == 1 and self.positions[0][x] != " ":
                return self.positions[0][x]

        #check the diagonals
        diag1 = set([self.positions[0][0], self.positions[1][1], self.positions[2][2]])
        diag2 = set([self.positions[0][2], self.positions[1][1], self.positions[2][0]])
        if (len(diag1) == 1 or len(diag2) == 1) and self.positions[1][1] != " ":
            return self.positions[1][1]
        #no one has one
        return "N"

    def printBoard(self):
        for row in range(3):
            print(" " + self.positions[row][0] + " | " + self.positions[row][1] + " | " + self.positions[row][2])
            if row != 2:
                print("-----------")
