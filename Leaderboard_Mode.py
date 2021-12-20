#Leaderboard: saves all the highest scores of top 3 users
from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
import pickle

#class to list the scores of users
#basic framework taken from: https://www.youtube.com/watch?v=GC50dexQsRo
class LeaderboardMode(Mode):
    """ Uncomment to reset scoreboard
    scoreboard = dict()
    scoreboard = pickle.dump(scoreboard, open("scoreboard.txt", "wb"))"""
    scoreboard = pickle.load(open("scoreboard.txt", "rb"))

    def appStarted(mode):
        #Menu coodinates
        mode.menuX0 = mode.width*(1/20)
        mode.menuX1 = mode.width*(1/5)
        mode.menuY0 = mode.height*(1/15)
        mode.menuY1 = mode.height*(3/15)
        #view
        mode.top5 = [("Tester", 0)]
        mode.x0 = mode.width*(1/4)
        mode.x1 = mode.width*(3/4)
        mode.yMargin = mode.height/10
        mode.cellHeight = (mode.height - 2*mode.yMargin)/5
        mode.decideTopScores()

    #compare all scores and get top 5
    def decideTopScores(mode):
        for person in LeaderboardMode.scoreboard:
            #compare with top 5
            for top in range(len(mode.top5)):
                name, score = mode.top5[top]
                #if score is higher, insert once
                tempScore = LeaderboardMode.scoreboard[person]
                if tempScore > score:
                    mode.top5.insert(top, (person, tempScore))
                    break
        #delete tester
        mode.top5.pop()
        #limit to top 5
        if len(mode.top5) > 5:
            mode.top5 = mode.top5[0:5]

     #controller for mouse clicked events
    def mousePressed(mode, event):
        mode.backToMainMenu(event.x, event.y)
    
    def drawScoreBoard(mode,canvas):
        for i in range(len(mode.top5)):
            #make top score colorful
            if i == 0:
                color = "gold"
            else:
                color = "white"
            #draw board
            y0 = mode.yMargin + i*mode.cellHeight
            y1 = y0 + mode.cellHeight
            canvas.create_rectangle(mode.x0, y0, mode.x1, y1, fill = color)
            #insert text
            textX = (mode.x0 + mode.x1)/2 
            textY = (y0 + y1)/2
            name, score = mode.top5[i]
            canvas.create_text(textX, textY, text = f"{name}: {score}",
                                font = "Arial 24 bold")

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

    def redrawAll(mode, canvas): 
        mode.drawScoreBoard(canvas)
        mode.drawMenuButton(canvas)
