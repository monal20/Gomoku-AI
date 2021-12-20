#Class that displays instructions for how to play the game

from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

class InstructionMode(Mode):
    def appStarted(mode):
        #Menu coodinates
        mode.menuX0 = mode.width*(1/20)
        mode.menuX1 = mode.width*(1/5)
        mode.menuY0 = mode.height*(1/15)
        mode.menuY1 = mode.height*(3/15)
        #Image coordinates
        mode.imageX = mode.width/2
        mode.imageY = mode.height/2
        #Image self drawn
        path = "Background.png"
        mode.instructions =  mode.loadImage(path)
        
    #controller for mouse clicked events
    def mousePressed(mode, event):
        mode.backToMainMenu(event.x, event.y)

    #opens up Menu Mode if button is clicked
    def backToMainMenu(mode, x, y):
        if ((x > mode.menuX0 and x < mode.menuX1) and 
            (y > mode.menuY0 and y < mode.menuY1)):
            mode.app.soundMode.click1SFX.play()
            mode.app.setActiveMode(mode.app.splashScreenMode)

    #draws the menu button
    def drawMenuButton(mode,canvas):
        #create box
        canvas.create_rectangle(mode.menuX0,mode.menuY0,mode.menuX1,mode.menuY1)
        #create text
        textX = (mode.menuX0 + mode.menuX1)/2
        textY = (mode.menuY0 + mode.menuY1)/2
        canvas.create_text(textX, textY, text = "Main Menu")

    #draws the instructions
    #instructions from: http://www.opengames.com.ar/en/rules/Gomoku
    def drawInstructions(mode,canvas):
        canvas.create_image(mode.imageX, mode.imageY, 
                    image=ImageTk.PhotoImage(mode.instructions))
        
    def redrawAll(mode, canvas):
        mode.drawInstructions(canvas)
        mode.drawMenuButton(canvas)
        