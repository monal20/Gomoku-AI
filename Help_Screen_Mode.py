#Help Screen Mode

from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

class HelpScreenMode(Mode):
    def appStarted(mode):
        #Buttons
        mode.buttonNames = ["Main Menu", "Instructions", "Resume"]
        mode.numOfButtons = 3
        mode.buttonHeight = mode.height*(1/(mode.numOfButtons*2+1))
        mode.buttonWidth =  mode.width*(9/10) - mode.width*(3/4)
        #Help Coordinates
        mode.imageX = mode.width*(3/8)
        mode.imageY = mode.height/2
        #Self-Drawn Image
        path = "Controls.png"
        mode.controls = mode.loadImage(path)

    #Controller for mouse clicked events
    def mousePressed(mode, event):
        mode.startOtherModes(event.x, event.y)
        pass

    #function that starts other modes if button in question is clicked on
    def startOtherModes(mode, x, y):
        row, col = mode.getCellForButtons(x,y)
        if col == 0:
            #Main Menu
            if row == 1:
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.splashScreenMode)
            #Instructions
            elif row == 3:
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.instructionMode)
            #Resume
            elif row == 5:
                #Resume Mode with respect to player v. player or AI mode
                mode.app.soundMode.click1SFX.play()
                if mode.app.gameMode.isAIMenu == False:
                    mode.app.setActiveMode(mode.app.gameMode)
                else:
                    mode.app.setActiveMode(mode.app.AIMode)


    
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
    
    #draws the buttons for the help menu
    def drawButtons(mode, canvas):
        for col in range(mode.numOfButtons*2):
            x0, y0, x1, y1 = mode.getCellBoundsForButtons(col)
            if col % 2  == 1:
                canvas.create_rectangle(x0, y0, x1, y1) 
                textX, textY = (x0+x1)/2, (y0+y1)/2
                canvas.create_text(textX, textY, text = 
                                    mode.buttonNames[col//2])

    #draws the instructions
    def drawHelpInstructions(mode,canvas):
        canvas.create_image(mode.imageX, mode.imageY, 
                    image=ImageTk.PhotoImage(mode.controls))
        
    #view that draws the winow
    def redrawAll(mode, canvas):
        mode.drawButtons(canvas)
        mode.drawHelpInstructions(canvas)
