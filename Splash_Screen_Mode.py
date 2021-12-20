#Splash Screen Mode/Main Menu

from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
import pygame

class SplashScreenMode(Mode):
    def appStarted(mode):
        #load self-drawn logo
        path = "Gomoku_Logo.jpeg"
        mode.logo = mode.loadImage(path)
        #Buttons
        mode.buttonNames = ["Ai Mode", "Player vs. Player", "Instructions", "LeaderBoard"]
        mode.numOfButtons = 4
        mode.buttonHeight = mode.height*(1/(mode.numOfButtons*2+1))
        mode.buttonWidth =  mode.width*(9/10) - mode.width*(3/4)
        mode.buttonColor = "white"
        #Title
        mode.titleX = mode.width*(3/8)
        mode.titleY = mode.height/2
        #Leaderboard and Game State
        mode.enteredAIGame = False
        mode.entered2PlayerGame = False
    
    #Controller for mouse clicked events
    def mousePressed(mode, event):
        mode.startOtherModes(event.x, event.y) 

    #function that starts other modes if button in question is clicked on
    def startOtherModes(mode, x, y):
        row, col = mode.getCellForButtons(x,y)
        if col == 0:
            #AI Mode
            if row == 1:
                mode.app.soundMode.click1SFX.play()
                #ask for name if game is not already in progress
                if mode.enteredAIGame == False or mode.app.AIMode.turnsTaken == 0:
                    SplashScreenMode.askForName(mode, 1)
                #start/restart game if re-entered mode
                mode.app.setActiveMode(mode.app.difficultyMode)
                #at least one game has been started with variables initialized
                mode.enteredAIGame = True
            #Player vs Player
            #code has same reasoning as AI mode, but adjusted for 2 players
            elif row == 3:
                mode.app.soundMode.click1SFX.play()
                if mode.entered2PlayerGame == False or mode.app.gameMode.turnsTaken == 0:
                    SplashScreenMode.askForName(mode, 2)
                mode.app.setActiveMode(mode.app.gameMode)
                mode.entered2PlayerGame = True
            #Help Screen
            elif row == 5:
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.instructionMode)
            #LeaderBoard
            elif row == 7:
                mode.app.soundMode.click1SFX.play()
                mode.app.leaderboardMode.appStarted()
                mode.app.setActiveMode(mode.app.leaderboardMode)

    #Asks and stores the name of the "players" for leaderboard purposes
    def askForName(mode, numOfPlayers):
        mode.app.gameMode.p1Name = mode.app.AIMode.p1Name = mode.getUserInput("What is player 1's name?")
        while mode.app.gameMode.p1Name == None or mode.app.gameMode.p1Name.strip() == "":
            mode.app.gameMode.p1Name = mode.app.AIMode.p1Name = mode.getUserInput("Player 1, please enter a proper name")
        mode.app.gameMode.p1Name =  mode.app.gameMode.p1Name.capitalize()
        if numOfPlayers == 2:
            mode.app.gameMode.p2Name = mode.getUserInput("Ok! Now what is player 2's name?")
            while mode.app.gameMode.p2Name == None or mode.app.gameMode.p2Name.strip() == "":
                mode.app.gameMode.p2Name = mode.getUserInput("Player 2, please enter a proper name.")
            mode.app.gameMode.p2Name =  mode.app.gameMode.p2Name.capitalize()
    
    #adpated from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBoundsForButtons(mode, col):
        x0 = mode.width*(3/4)
        x1 = mode.width*(9/10)
        y0 = mode.buttonHeight*(col)
        y1 = mode.buttonHeight*(col+1)
        return (x0, y0, x1, y1)

    #adpated from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellForButtons(mode, x, y):
        col = int((x - mode.width*(3/4))/mode.buttonWidth)
        #checks for when user presses left of buttons
        if x < mode.width*(3/4): col = -1 
        row = int(y/mode.buttonHeight)
        return row,col
    
    #draws the 4 buttons for the main menu and the text
    def drawButtons(mode, canvas):
        for col in range(mode.numOfButtons*2):
            x0, y0, x1, y1 = mode.getCellBoundsForButtons(col)
            if col % 2  == 1:
                canvas.create_rectangle(x0, y0, x1, y1, fill = mode.buttonColor) 
                textX, textY = (x0+x1)/2, (y0+y1)/2
                canvas.create_text(textX, textY, text = 
                                    mode.buttonNames[col//2])

    #inserts the photo into the canvas
    def drawLogo(mode, canvas):
        canvas.create_image(mode.titleX, mode.titleY, 
                    image=ImageTk.PhotoImage(mode.logo))

    def redrawAll(mode, canvas):
        mode.drawLogo(canvas)
        mode.drawButtons(canvas)
        
