#AI Mode

from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from Game_Mode import*
import random
import math
from Check_For_Win import *

#subclass that controls the AI and enable single-user play
class AIMode(GameMode):
    def appStarted(mode):
        GameMode.appStarted(mode)
        #AI modes
        mode.easyMode = False
        mode.mediumMode = False
        mode.hardMode = False
        #image
        mode.path3 = "playerAI.png"
        #leaderboard name
        mode.p2Name = "AI"
        
    def timerFired(mode):
        if mode.gameOver != True:
            #Change side bar images according to whose turn it is
            if mode.turnsTaken % 2 ==  0:
                mode.playerImage = mode.loadImage(mode.path2)
            else:
                mode.playerImage = mode.loadImage(mode.path3)
            #have the AI place the piece if player 1 has not won
            if  mode.curColor == mode.p2Color:
                AIMode.getBestPosition(mode)
                #self drawn
                mode.playerImage = mode.loadImage(mode.path3)
                mode.placePiece()

    def getBestPosition(mode):
        AIMode.minimax(mode, mode.board,0,0,2, mode.p2Color, -math.inf, math.inf)

    #assign points based on the state of the board
    def heuristic(mode, board, player, row, col):
        #Four-in-a-row
        if player == mode.p1Color:
            opponent = mode.p2Color
        else:
            opponent = mode.p1Color
        score = -1
        
        #Change Heuristic based on AI difficulty
        if mode.mediumMode == True or mode.easyMode == True:
            #gives the numbers for pieces in a row and neighboring pieces in one direction only
            #does not count oo_oo as a possible 5-in-row, but rather 3
            oppRun, oppCount, playerRun, playerCount = CheckForWin.countPiecesFromCellInOneDir(board,
                                                    opponent, player, row, col)
        elif mode.hardMode == True:
            #gives the numbers for pieces in a row and neighboring pieces in two directions directions
            #accounts for oo_oo a possible 5-in-row
            oppRun, oppCount, playerRun, playerCount = CheckForWin.countPiecesFromCellInTwoDir(board,
                                                    opponent, player, row, col)
        
        #randomize easy Mode more
        if mode.easyMode:
            if (mode.turnsTaken < 10 and 
            (row > mode.pieceRows//3 and row < (mode.pieceRows//3)*2) and 
            (col > mode.pieceCols//3 and col < (mode.pieceCols//3)*2)):
                score += 100

        #Assign points to each location based on the state of the board
        #offensive moves 
        if playerRun >= 5: 
            score -= 10000000
            if mode.mediumMode:
                score = score//10
        elif playerRun == 4 and oppRun < 5:
            score -= 100000
            if mode.mediumMode:
                score = score//10
        elif playerRun == 3:
            score -= 10000
        elif playerRun == 2: 
            score -= 100

        #account for neighboring Pieces if in medium Mode
        if mode.mediumMode and mode.turnsTaken > 10:
            score -= 100*playerCount
    
        #defensive moves
        if oppRun >= 5:
            if not mode.easyMode:
                score -= 10000000
        if oppRun == 4:
            if not mode.easyMode:
                score -= 100000
        elif oppRun == 3:
            if mode.easyMode:
                score -= 10000
        elif oppRun == 3:
            if mode.easyMode:
                score -= 1100
            else:
                score -= 1000
        elif oppRun == 2:
            if mode.turnsTaken < 4:
                score -= 100
            else:
                score -=10
        return score
    
    #Returns the best move based position of the board using recursive backtracking 
    #Adapted according by the following resources:
    #1.https://medium.com/swlh/optimizing-decision-making-with-the-minimax-ai-algorithm-69cce500c6d6
    #2.https://www.scirp.org/journal/paperinformation.aspx?paperid=90972
    #3.https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/?ref=rp
    #4.https://sandipanweb.wordpress.com/2017/03/06/using-minimax-with-alpha-beta-pruning-and-heuristic-evaluation-to-solve-2048-game-with-computer/
    #5.https://www.youtube.com/watch?v=l-hh51ncgDI
    #6.https://youtube.com/watch?v=y7AKtWGOPAE
    def minimax(mode, board, row, col, depth, player, alpha, beta):
        #base case
        if depth == 0 or CheckForWin.wordSearch(mode.board, player, 5, 1) != None:
             return AIMode.heuristic(mode, board, player, row, col)

        #Maximizer -> AI
        if player == mode.p2Color:
            #assume worst case first
            score = -math.inf
            #check each position
            for row in range(mode.pieceRows):
                for col in range(mode.pieceCols):
                    #recursively check for best possible move
                    if GameMode.moveIsLegal(mode, row, col, mode.board):
                        #test move
                        mode.board[row][col]= mode.p2Color
                        tempScore = (AIMode.minimax(mode, mode.board, row, col,
                                 depth - 1, mode.p1Color, alpha, beta))
                        #backtrack
                        mode.board[row][col] = None
                        if tempScore > score: 
                            mode.curRow, mode.curCol = row, col
                            score = tempScore
                            #alpha beta pruning
                            #from: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
                            alpha = max(alpha,score)
                            if beta <= alpha: break
            #return highest score
            return score

        #Minimizer -> player
        else:
            #assume player makes the optimal move
            score = math.inf
            #check each position
            for row in range(mode.pieceRows):
                for col in range(mode.pieceCols):
                    #recursively check for opponent's optimal move
                    if GameMode.moveIsLegal(mode, row, col, mode.board):
                        #test
                        mode.board[row][col]= mode.p1Color
                        tempScore = (AIMode.minimax(mode, mode.board, row, col,
                                    depth - 1, mode.p2Color, alpha, beta))
                        #backtrack
                        mode.board[row][col] = None
                        if tempScore < score: 
                            mode.curRow, mode.curCol = row, col
                            score = tempScore
                            #alpha beta pruning
                            #from: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
                            beta = min(beta,score)
                            if beta <= alpha: break
            #return lowest score
            return score

    #if help button is clicked, open Help Mode
    def openHelpScreenMode(mode, x, y):
        #check if in bounds
          if ((x > mode.buttonX0 and x < mode.buttonX1) and 
            (y > mode.helpY0 and y < mode.helpY1)):
                mode.app.soundMode.click1SFX.play()
                mode.app.gameMode.isAIMenu = True
                mode.app.setActiveMode(mode.app.helpScreenMode)

    #Main view function that draws all the features of the game
    def redrawAll(mode, canvas):
        mode.drawBackground(canvas)
        mode.drawImageOfCurrentPlayer(canvas)
        mode.drawBoard(canvas)
        mode.drawLabels(canvas)
        mode.drawGomokuPieces(canvas)
        mode.drawMovingPiece(canvas)
        mode.drawConfirmButton(canvas)
        mode.drawHelpButton(canvas)
        if mode.showCurPiece == True:
            mode.drawCurrentPlacedPiece(canvas)
        if mode.gameOver == True:
            mode.drawWinner(canvas)
