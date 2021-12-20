#Sound
from cmu_112_graphics import *
#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
import pygame
#from: https://www.pygame.org/docs/tut/ImportInit.html

#controls the sound effects and background music for the game
#adapted from: https://youtu.be/2BikxsbkuIU
class SoundMode(Mode):
        pygame.init()
        pygame.mixer.init()
        #The following 3 sound effects are from: shttps://www.zapsplat.com
        click1SFX = pygame.mixer.Sound("piece1.ogg")
        piece1 = pygame.mixer.Sound("piece2.ogg")
        piece2 = pygame.mixer.Sound("piece3.ogg")

        #background music
        """from: Curious by Nicolai Heidlas Music https://soundcloud.com/nicolai-heidlas
        Creative Commons — Attribution 3.0 Unported— CC BY 3.0 
        https://www.youtube.com/redirect?redir_token=QUFFLUhqbmNHWWxMbzlvaDFkMlVfYTBRR1pGNGw5blRHd3xBQ3Jtc0trUmZtRk5NRHBTelgtMTFhV3ZpNUNVLTREQkRaeVh5S0U5Sm44TEwtaUdlZEtTOXp0eW5WNG5IWEpSVnE0ZXVzVWREb0hCd290N1hoWlUtc1drY1BsNjdMUEdVUERUN3E3WU9JQl9uV0ZZS0g2Vzhtaw%3D%3D&q=http%3A%2F%2Fcreativecommons.org%2Flicenses%2Fb&event=video_description&v=gZ71fkloi-8
        Music provided by Music for Creators https://youtu.be/6XvOqLcDr48"""
        music = pygame.mixer.music.load("Curious-Nicolai Heidlas.ogg")
        playBackground = pygame.mixer.music.play(-1)



