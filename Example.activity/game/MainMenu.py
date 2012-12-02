#!/usr/bin/python
'''
Ryan O'Dowd, Kevin Touhey, and Yifan Hong
CISC 374
Fall 2012
'''

__doc__ = '''
            Main Menu is the scene that
                -selects an option based on user position on screen

            OUTPUTS
                -One of the Mini Game
                -Quits
          '''

from spyral.sprite import Sprite
import pygame
import spyral
import Basketball
import CrosswordPuzzle
#import Cooking
import Racing
import WorldMap
import TownMap
import PetSelection
from spyral.scene import Scene

BG_COLOR = (100, 100, 100)

WIDTH = 1200
HEIGHT = 900
FONT_SIZE = 56

POINTER = 'images/pets/pointer.png'

STAR = 'images/pets/star.png'
DIAMOND = 'images/pets/diamond.png'
CUBE = 'images/pets/cube.png'
SPHERE = 'images/pets/sphere.png'
MOON = 'images/pets/moon.png'

#MONIES
MONIES = [STAR,
          DIAMOND,
          CUBE,
          SPHERE,
          MOON]

# MONEY LOCATIONS
MONEY_POINTS = [
    (0, 0),
    (0, 140),
    (0, 280),
    (140, 0),
    (140, 140),
    (140, 280),
    (280, 0),
    (280, 140),
    (280, 280),
]

# POINTER_LOCATION
POINTER_POINTS =[
    (40, 40),
    (40, 180),
    (40, 320),
    (180, 40),
    (180, 180),
    (180, 320),
    (320, 40),
    (320, 180),
    (320, 320),
    (440, 40)] # QUIT BUTTON
"""
NOTE: Lots of Main Menu is a direct copy of PetSelection
      To actually have an emoting pet on screne you need this code
      We added it to brighten up the main menu
"""
class MainMenu(Scene):
    def __init__(self, pet):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child((WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        font = pygame.font.SysFont(None, FONT_SIZE)

        #BEGIN MONEY MATRIX
        self.M00 = Sprite(self.group)
        self.M00.image = spyral.Image(filename=MONIES[1])
        self.M00.layer = 1 
        self.M00.x = MONEY_POINTS[0][0]
        self.M00.y = MONEY_POINTS[0][1]

        self.M10 = Sprite(self.group)
        self.M10.image = spyral.Image(filename=MONIES[2])
        self.M10.layer = 1 
        self.M10.x = MONEY_POINTS[1][0]
        self.M10.y = MONEY_POINTS[1][1]

        self.M20 = Sprite(self.group)
        self.M20.image = spyral.Image(filename=MONIES[3])
        self.M20.layer = 1 
        self.M20.x = MONEY_POINTS[2][0]
        self.M20.y = MONEY_POINTS[2][1]

        self.M01 = Sprite(self.group)
        self.M01.image = spyral.Image(filename=MONIES[4])
        self.M01.layer = 1 
        self.M01.x = MONEY_POINTS[3][0]
        self.M01.y = MONEY_POINTS[3][1]

        self.M11 = Sprite(self.group)
        self.M11.image = spyral.Image(filename=MONIES[0])
        self.M11.layer = 1 
        self.M11.x = MONEY_POINTS[4][0]
        self.M11.y = MONEY_POINTS[4][1]

        self.M21 = Sprite(self.group)
        self.M21.image = spyral.Image(filename=MONIES[1])
        self.M21.layer = 1 
        self.M21.x = MONEY_POINTS[5][0]
        self.M21.y = MONEY_POINTS[5][1]

        self.M02 = Sprite(self.group)
        self.M02.image = spyral.Image(filename=MONIES[2])
        self.M02.layer = 1 
        self.M02.x = MONEY_POINTS[6][0]
        self.M02.y = MONEY_POINTS[6][1]

        self.M12 = Sprite(self.group)
        self.M12.image = spyral.Image(filename=MONIES[3])
        self.M12.layer = 1 
        self.M12.x = MONEY_POINTS[7][0]
        self.M12.y = MONEY_POINTS[7][1]

        self.M22 = Sprite(self.group)
        self.M22.image = spyral.Image(filename=MONIES[4])
        self.M22.layer = 1 
        self.M22.x = MONEY_POINTS[8][0]
        self.M22.y = MONEY_POINTS[8][1]

        self.pick = 0

        self.pointer = Sprite(self.group)
        self.pointer.image = spyral.Image(filename=POINTER)
        self.pointer.layer = 2
        self.pointer.x = POINTER_POINTS[self.pick][0]
        self.pointer.y = POINTER_POINTS[self.pick][1]

        self.set_pointer()      

        instructions = PetSelection.TextSprite(self.group, font)
        instructions.anchor = 'midbottom'
        instructions.x = 320
        instructions.y = 470
        instructions.render("MAIN MENU (p: next  s: select)")

        self.qbutton = Sprite(self.group)
        self.qbutton.image = spyral.Image(size=(150,50))
        self.qbutton.image.fill(color = (0,0,0))
        self.qbutton.x = 430
        self.qbutton.y = 60
        self.qbutton.layer = 0

        quitbutton = PetSelection.TextSprite(self.group, font)
        quitbutton.anchor = 'midbottom'
        quitbutton.x = 480
        quitbutton.y = 100
        quitbutton.render ("QUIT")

        self.pet = pet
        self.group.add(self.pet)

    
    def set_pointer(self):
        self.pointer.image = spyral.Image(filename=POINTER)
        self.pointer.layer = 2
        self.pointer.x = POINTER_POINTS[self.pick][0]
        self.pointer.y = POINTER_POINTS[self.pick][1]
      
    def next_pick(self):
        self.pick = (self.pick + 1) % len(POINTER_POINTS)
        self.set_pointer()

    def on_enter(self):
        bg = spyral.Image(size=(WIDTH, HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                
    def render(self):
        self.group.draw()

    def update(self, dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['ascii'] == 'p':
                    self.next_pick()
                elif event['ascii'] == 's':
                    if (self.pick == 0):
                        spyral.director.push(WorldMap.WorldMap())
                    elif (self.pick == 5):
                        spyral.director.push(CrosswordPuzzle.CrosswordMain())
                    elif (self.pick == 1 or self.p == 6):
                        spyral.director.push(Basketball.Basketball())
                    elif (self.pick == 2 or self.p == 7):
                        spyral.director.push(Racing.RacingMain())
                    elif (self.pick == 3 or self.p == 8):
                        spyral.director.push(TownMap.Room(100))
                    elif (self.pick == 4):
                        spyral.director.pop()
                        return
                    elif (self.pick == 9):
                        spyral.director.pop()
                        return
        self.group.update(dt)

if __name__ == "__main__":
    spyral.init()
    spyral.director.init((WIDTH, HEIGHT))
    spyral.director.push(PetSelection())
    spyral.director.run()
