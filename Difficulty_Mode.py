#AI difficulty selection

from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

class DifficultyMode(Mode):
    def appStarted(mode):
        #Buttons
        mode.buttonNames = ["Easy", "Medium", "Hard"]
        mode.numOfButtons = 3
        mode.buttonHeight = mode.height*(1/(mode.numOfButtons*2+1))
        mode.buttonWidth =  mode.width*(9/10) - mode.width*(3/4)
        #Image Coordinates
        mode.imageX = mode.width*(3/8)
        mode.imageY = mode.height/2
        #load self-drawn logo
        path = "AI_Vs_Player.jpeg"
        mode.robot = mode.loadImage(path)

    #Controller for mouse clicked events
    def mousePressed(mode, event):
        mode.startOtherModes(event.x, event.y)
        pass

    #function that starts AI mode with selected difficulty
    def startOtherModes(mode, x, y):
        row, col = mode.getCellForButtons(x,y)
        if col == 0:
            #Easy
            if row == 1:
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.AIMode)
                mode.app.AIMode.easyMode = True
                mode.app.AIMode.mediumMode = mode.app.AIMode.hardMode = False
            #Medium
            elif row == 3:
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.AIMode)
                mode.app.AIMode.mediumMode = True
                mode.app.AIMode.easyMode = mode.app.AIMode.hardMode = False
            #Hard
            elif row == 5:
                mode.app.soundMode.click1SFX.play()
                mode.app.setActiveMode(mode.app.AIMode)
                mode.app.AIMode.hardMode = True
                mode.app.AIMode.mediumMode = mode.app.AIMode.easyMode = False
    
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

    #draws the image which will be inserted later
    def drawImage(mode,canvas):
        canvas.create_image(mode.imageX, mode.imageX, 
                    image=ImageTk.PhotoImage(mode.robot))
        
    #view that draws the window
    def redrawAll(mode, canvas):
        mode.drawImage(canvas)
        mode.drawButtons(canvas)
