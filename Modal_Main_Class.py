##############
# Term Project.py
# Name: Mona Lin
# andrewID: monal
# TP Mentor: Kian Nassre
# Section F0 Lecture 2
##############


from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from Help_Screen_Mode import *
from Splash_Screen_Mode import*
from AI_Mode import *
from Game_Mode import *
from Instruction_Mode import*
from Difficulty_Mode import*
from Sound_Mode import*
from Leaderboard_Mode import*
                         
#Main class that hosts all the other apps fobr the gomoku AI
#structure revised from:
#https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.helpScreenMode = HelpScreenMode()
        app.AIMode = AIMode()
        app.difficultyMode = DifficultyMode()
        app.gameMode = GameMode()
        app.instructionMode = InstructionMode()
        app.soundMode = SoundMode()
        app.leaderboardMode = LeaderboardMode()
        app.setActiveMode(app.splashScreenMode)


app = MyModalApp(width = 800, height = 600)
