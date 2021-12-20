#Game Mode

from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
import string
from Check_For_Win import *
#modified from: https://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
import time 
import pickle

#Main Class that builds off of the CMU-112 animation framework
class GameMode(Mode):
    #main model that stores game values
    def appStarted(mode):
        #board
        mode.boardRows = mode.boardCols = 15
        mode.pieceRows = mode.pieceCols = mode.boardRows - 1
        mode.board = [[None]*mode.pieceRows for col in range(mode.pieceCols)]
        mode.margin = min(mode.height,mode.width)//10
        mode.boardWidth = mode.width*(3/4)
        mode.boardHeight = mode.height
        mode.cellWidth = (mode.boardWidth-2*mode.margin)/mode.boardCols
        mode.cellHeight = (mode.boardHeight-2*mode.margin)/mode.boardRows
        #players
        mode.p1Color = "black"
        mode.p2Color = "white"
        #mode.p1Name and mode.p2Name initialized in splashMenu
        #pieces
        mode.curRow, mode.curCol, mode.curColor = None, None, mode.p1Color
        mode.movingX = mode.movingY = mode.movingRadius = 0
        #buttons
        mode.buttonX0 = mode.boardWidth
        mode.buttonX1 = mode.width - mode.margin/2
        mode.buttonHeight = mode.height*(1/10)
        #-->confirm button
        mode.conY0 = mode.height*(13/16)
        mode.conY1 = mode.conY0 + mode.buttonHeight
        #-->help button
        mode.helpY0 = mode.height*(1/20)
        mode.helpY1 = mode.helpY0 + mode.buttonHeight
        #gameState
        mode.showCurPiece = False
        mode.gameOver = False
        mode.winner = None
        mode.turnsTaken = 0
        #timer
        mode.timerCalls = 0
        mode.seconds = 0
        mode.minutes = 0
        mode.isTimerOn = False
        #AI parameters
        mode.isAIMenu = False
        #background image
        #->from: https://besthqwallpapers.com/fr/download/original/116443
        path = "Wallpaper.jpg"
        mode.wallpaper = mode.loadImage(path)
        #Self drawn Side bar images
        mode.path2 = "player1.png"
        mode.path3 = "player2.png"
        mode.playerImage = mode.loadImage(mode.path2)

    #Controller for key presses
    def keyPressed(mode, event):
        #if a player wins, press space to restart
        if mode.gameOver == True and event.key == "Space":
            mode.app.setActiveMode(mode.app.splashScreenMode)
            mode.appStarted()
        else:
            #Press enter to place piece and move on to next turn
            if event.key ==  "Enter": mode.placePiece()
            #Move current piece with directional keys
            elif event.key == "Up":
                mode.moveCurPieceWithKeys(0, -1)
            elif event.key == "Down":
                mode.moveCurPieceWithKeys(0, 1)
            elif event.key == "Left":
                mode.moveCurPieceWithKeys(-1, 0)
            elif event.key == "Right":
                mode.moveCurPieceWithKeys(1, 0)
            #restart game
            elif event.key == "r":
                GameMode.appStarted(mode)

    #Controller for events when mouse is pressed
    def mousePressed(mode, event):
        if mode.gameOver != True:
            #begin timer when first piece is placed
            mode.isTimerOn = True 
            row, col = mode.getCellForPieces(event.x, event.y)
            #place new piece if legal and piece not already placed this turn
            if mode.moveIsLegal(row, col, mode.board):
                mode.curRow, mode.curCol = row, col
            #if player actually made a move, place piece
            if mode.curRow != None or mode.curCol != None:
                mode.confirmPressed(event.x, event.y)
            #check if help button is pressed
            mode.openHelpScreenMode(event.x,event.y)

    #Controller for events when mouse is dragged
    def mouseDragged(mode, event):
        if mode.gameOver != True:
            mode.showCurPiece = False
            #store the position of the player's current piece if dragged
            mode.movingX, mode.movingY = event.x, event.y
            mode.movingRadius = mode.cellWidth//2

    #Controller for events when mouse is released
    def mouseReleased(mode, event):
        if mode.gameOver != True:
            mode.movingRadius = 0
            row, col = mode.getCellForPieces(event.x, event.y)
            if mode.moveIsLegal(row,col,mode.board):
                mode.curRow, mode.curCol = row, col
            #show the placed down piece and not the moving piece
            mode.movingRadius = 0
            mode.showCurPiece = True
    
    #function that updates the model
    def timerFired(mode):
        #changes the timer
        if mode.isTimerOn == True:
            mode.timerCalls += 1
            if mode.timerCalls % 10 == 0 and mode.timerCalls != 0:
                #increment seconds
                mode.seconds += 1
                #increment minutes
                if mode.seconds % 60 == 0:
                    mode.minutes += 1
                    mode.seconds = 0
        #Change side bar images according to whose turn it is
        if mode.turnsTaken % 2 ==  0:
            mode.playerImage = mode.loadImage(mode.path2)
        else:
            mode.playerImage = mode.loadImage(mode.path3)


    #checks if the player move is legal
    def moveIsLegal(mode, row, col, board):
        #checks if piece is in bound and not already placed
        if ((row < 0 or row >= mode.pieceRows) or
            (col < 0 or col >= mode.pieceCols) or
            (board[row][col] != None)): return False
        return True

    #place piece and move onto the next player's turn if confirm is clicked 
    def confirmPressed(mode, x, y):
        #check in bounds of confirm button
        if ((x > mode.buttonX0 and x < mode.buttonX1) and 
            (y > mode.conY0 and y < mode.conY1)):
               mode.placePiece()

    #places the current piece onto the board and moves onto next turn
    def placePiece(mode):
        #place current piece onto board
        if not (mode.curRow == None and mode.curCol == None):
            mode.board[mode.curRow][mode.curCol] = mode.curColor
            mode.app.soundMode.piece2.play()
            mode.turnsTaken += 1
            #switch to next player's turn
            mode.curRow = mode.curCol = None
            if mode.curColor == mode.p1Color: mode.curColor = mode.p2Color
            else: mode.curColor = mode.p1Color
            #check for a win once piece is placed
            mode.checkForWin()

    #check if there is an winner on the board
    def checkForWin(mode):
        if CheckForWin.wordSearch(mode.board, mode.p2Color, 5, 1) != None:
            mode.gameOver = True
            time.sleep(1)
            if mode.isAIMenu == False:
                #add winner to scoreboard
                numOfWins = mode.app.leaderboardMode.scoreboard.get(mode.p2Name, 0) + 1 
                mode.winner = "Player 2"
            else:
                numOfWins = mode.app.leaderboardMode.scoreboard.get("AI", 0) + 1 
            #update leaderboard
            mode.app.leaderboardMode.scoreboard[mode.p2Name] = numOfWins
            pickle.dump(mode.app.leaderboardMode.scoreboard, open("scoreboard.txt", "wb"))

        elif (CheckForWin.wordSearch(mode.board, mode.p1Color, 5, 1) != None):
            mode.gameOver = True
            time.sleep(1)
            mode.winner = "Player 1"
            #add winner to scoreboard
            numOfWins = mode.app.leaderboardMode.scoreboard.get(mode.p1Name, 0) + 1 
            mode.app.leaderboardMode.scoreboard[mode.p1Name] = numOfWins
            pickle.dump(mode.app.leaderboardMode.scoreboard, open("scoreboard.txt", "wb"))

    #if help button is clicked, open Help Mode
    def openHelpScreenMode(mode, x, y):
        #check if in bounds
          if ((x > mode.buttonX0 and x < mode.buttonX1) and 
            (y > mode.helpY0 and y < mode.helpY1)):
                mode.AIMenu = False
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.helpScreenMode)

    #move the current piece based on given xDir and yDir
    def moveCurPieceWithKeys(mode, xDir, yDir):
        if not (mode.curRow == None and mode.curCol == None):
         newRow, newCol = mode.curRow+yDir, mode.curCol+xDir
         if mode.moveIsLegal(newRow,newCol, mode.board):
            mode.curRow, mode.curCol = newRow, newCol

    #returns the event based coordinates of a grid based on the given row, col
    #adpated from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBoundsForBoard(mode, row, col):
        x0 = mode.margin + col*mode.cellWidth
        x1 = mode.margin + (col+1)*mode.cellWidth
        y0 = mode.margin + row*mode.cellHeight
        y1 = mode.margin + (row+1)*mode.cellHeight
        return (x0, y0, x1, y1)

    #gets the event based coordinates for the pieces
    #adpated from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBoundsForPieces(mode,row,col):
        x0 = mode.margin + (col+.5)*mode.cellWidth
        x1 = mode.margin + (col+1.5)*mode.cellWidth
        y0 = mode.margin + (row+.5)*mode.cellHeight
        y1 = mode.margin + (row+1.5)*mode.cellHeight
        return (x0, y0, x1, y1)

    #get the model row and col from the x,y coordinates
    #adpated from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellForPieces(mode, x, y):
        row = int((y - mode.margin - mode.cellHeight/2 ) / mode.cellHeight)
        col = int((x - mode.margin - mode.cellWidth/2) / mode.cellWidth)
        return row, col

    #draws the board for the gomoku
    def drawBoard(mode, canvas):
        for row in range(mode.boardRows):
            for col in range(mode.boardCols):
                x0, y0, x1, y1 = mode.getCellBoundsForBoard(row, col)
                canvas.create_rectangle(x0, y0, x1, y1)

    #draw all the pieces in the gomoku class
    def drawGomokuPieces(mode,canvas):
        for row in range(mode.pieceRows):
            for col in range(mode.pieceCols):
                x0, y0, x1, y1 = mode.getCellBoundsForPieces(row, col)
                if mode.board[row][col] != None:
                    canvas.create_oval(x0, y0, x1, y1, fill = mode.board[row][col])

    #draw the piece that the player wants to move to stimulate dragging a piece
    def drawMovingPiece(mode, canvas):
        canvas.create_oval(mode.movingX - mode.movingRadius, 
                            mode.movingY - mode.movingRadius,
                            mode.movingX + mode.movingRadius,
                            mode.movingY + mode.movingRadius,
                            fill = mode.curColor)

    def drawCurrentPlacedPiece(mode, canvas):
        if mode.curRow != None or mode.curCol != None:
            x0, y0, x1, y1 = mode.getCellBoundsForPieces(mode.curRow, mode.curCol)
            canvas.create_oval(x0, y0, x1, y1, fill = mode.curColor)

    #draws the labels around the perimeter of the grid
    def drawLabels(mode,canvas):
        for num in range(mode.pieceCols):
            #RightLeft Labels
            rightLeftCY = mode.margin + (num+1)*mode.cellHeight
            #right
            rightCX = mode.margin//2 
            canvas.create_text(rightCX,rightLeftCY, text = str(num))
            #left
            leftCX = mode.boardWidth - mode.margin//2
            canvas.create_text(leftCX, rightLeftCY, text = str(num))

            #TopBottom Labels
            letter = string.ascii_lowercase[num:num+1]
            #if more than 26 row/cols, make rest of the labels uppercase
            wrapAroundNum = num%26
            if num > 25:
                letter = string.ascii_uppercase[wrapAroundNum:wrapAroundNum+1]
            topBotCX = mode.margin + (num+1)*mode.cellWidth
            #top
            topCY = rightCX
            canvas.create_text(topBotCX, topCY, text = letter) 
            #bottom
            botCY = leftCX
            canvas.create_text(topBotCX, botCY, text = letter)
    
    #draws the Help Button
    def drawHelpButton(mode,canvas):
        canvas.create_rectangle(mode.buttonX0, mode.helpY0, mode.buttonX1,
                         mode.helpY1, fill = "red")
        textX = (mode.buttonX0+mode.buttonX1)/2
        textY = (mode.helpY0+mode.helpY1)/2, 
        canvas.create_text(textX, textY, text = "Help", fill = "black")

    #draws a confirm button to solidy player choice
    def drawConfirmButton(mode, canvas):
        canvas.create_rectangle(mode.buttonX0, mode.conY0, mode.buttonX1, mode.conY1,
                                fill = "black")
        textX, textY = (mode.buttonX0+mode.buttonX1)/2, (mode.conY0+mode.conY1)/2, 
        canvas.create_text(textX, textY, text = "Place Piece", fill = "white")

    #draw the time allotted since the game started
    def drawTimer(mode, canvas):
        #find center x,y for timer text
        textX = textX = (mode.buttonX0+mode.buttonX1)/2
        textY = mode.height*(1/3)
        canvas.create_text(textX, textY, 
                    text = f"Timer",
                    font = "Arial 30 bold")
        #find center x,y for actual time
        textY =  textY + mode.buttonHeight
        #adust text to draw 00:00 as starting time instead of 0:0
        extraSecZero = extraMinZero = ""
        if mode.seconds < 10:
            extraSecZero = "0"
        if mode.minutes < 10:
            extraMinZero = "0"
        canvas.create_text(textX, textY, 
            text = f"{extraMinZero}{mode.minutes}:{extraSecZero}{mode.seconds}",
            font = "Arial 30 bold")

    #Draws a winning message
    def drawWinner(mode, canvas):
        y0 = mode.height*(2/8)
        y1 = mode.height*(4/8)
        canvas.create_rectangle(0, y0, mode.width, y1, fill = "black")
        textX, textY = mode.width/2, (y1+y0)/2
        canvas.create_text(textX, textY, 
            text = f"{mode.winner} wins!! Press space to return to homescreen.",
                                    fill = "white", font = "Arial 18 bold")

    #inserts an image as the background
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, 
                    image=ImageTk.PhotoImage(mode.wallpaper))

    def drawImageOfCurrentPlayer(mode, canvas):
        imageX = mode.boardWidth + (mode.buttonX1 - mode.buttonX0)/2
        imageY = mode.height*(9/14)
        canvas.create_image(imageX, imageY, 
                    image=ImageTk.PhotoImage(mode.playerImage))


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
        mode.drawTimer(canvas)
        if mode.gameOver == True:
            mode.drawWinner(canvas)
        