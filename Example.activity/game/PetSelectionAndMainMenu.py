#!/usr/bin/python
'''
Ryan O'Dowd, Kevin Touhey, and Yifan Hong
CISC 374
Fall 2012
'''

__doc__ = '''
          Pet Selection is the scene that
              1. Goes through the types of pets
              2. Goes through the colors of pets
              3. User selects the final pet
          Output:
              -Stores user selection into a global list

                      STUDENT_PET
                          
              -STUDENT_PET[0] = int index for COLORS
              -STUDENT_PET[1] = int index for TYPES

              -Main Menu scene
          '''

import pygame
import spyral
from spyral.sprite import Sprite
from spyral.scene import Scene
import Basketball
import CrosswordPuzzle
import Cooking
import Racing
import globalStudent
from pet import pet

SIZE = (640, 480)
FONT_SIZE = 42
BG_COLOR = (100, 100, 100)
FG_COLOR = (255, 255, 255)
MY_COLOR = (255, 0, 0)

#POINTER
POINTER = 'pet_images/POINTER.png'

#MONEY
STAR = 'pet_images/STAR.png'
DIAMOND = 'pet_images/Diamond.png'
CUBE = 'pet_images/Cube.png'
SPHERE = 'pet_images/Sphere.png'
MOON = 'pet_images/Moon.png'

#MONIES
MONIES = [STAR,
          DIAMOND,
          CUBE,
          SPHERE,
          MOON]


#BEGIN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# IMAGE LOCATIONS
PET_POINTS = [(0, 0), #HATS
              (26, 0), #HEAD
              (26, 0), #FACE
              (16, 63), #ARMS    
              (0, 0), #SLEEVE
              (0, 110), #LEGS
              (0, 0), #PANTS
              (0, 0), #SHIRT
              (44, 50), #BODY
              (67, 45)] #TAIL

class TextSprite(Sprite):
    def __init__(self, group, font):
        Sprite.__init__(self, group)
        self.font = font
        
    def render(self, text):
        surf = self.font.render(text, True, FG_COLOR).convert_alpha()
        # This should be fixed up once the font system is in place
        class DumbImage(spyral.Image):
            def __init__(self):
                self._surf = surf
        self.image = DumbImage()
        self.layer=2

    def change (self):
        self.image.fill(color=BG_COLOR)
        self.layer=0
        Sprite.__del__(self)

    def erase (self):
        Sprite.__del__(self)
        
class PetSelection(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child(SIZE)
        self.group = spyral.Group(self.camera)

        font = pygame.font.SysFont(None, FONT_SIZE)

        self.t = 0

        #PET LOCATION (TOP LEFT HAND CORNER)
    
        self.PET_X = 230
        self.PET_Y = 200

        self.i =0
        self.j =0
        self.t =0

        self.pet = pet(self.group)
        self.pet.set_pet(pet_type=self.t,
                         pet_color=self.i,
                         pet_expression=self.j,
                         x=self.PET_X,
                         y=self.PET_Y)

        instructions = TextSprite(self.group, font)
        instructions.anchor = 'midbottom'
        instructions.x = 320
        instructions.y = 470
        instructions.render("i: color  j: emote t: type  s: select")

        heading = TextSprite(self.group, font)
        heading.anchor = 'midbottom'
        heading.x = 320
        heading.y = 70
        heading.render("CHESTER PETS")      

    def get_head(self):
        return self.head._image._surf

    def get_arms(self):
        return self.arms._image._surf

    def get_legs(self):
        return self.legs._image._surf

    def get_body(self):
        return self.body._image._surf

    def get_tail(self):
        return self.tail._image._surf

    def recolor(self, color1, color2, a):
        if a == HEAD_LAYER:
            surf = self.get_head()
        elif a == BODY_LAYER:
            surf = self.get_body()
        elif a == ARMS_LAYER:
            surf = self.get_arms()
        elif a == LEGS_LAYER:
            surf = self.get_legs()
        elif a == TAIL_LAYER:
            surf = self.get_tail()

        for x in range(surf.get_width()):
            for y in range(surf.get_height()):
                if surf.get_at((x,y)) == color1:
                    surf.set_at((x,y), color2)
                
    def on_enter(self):
        bg = spyral.Image(size=SIZE)
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                
    def render(self):
        self.group.draw()
        
    def nextJ(self):
        self.j += 1
        self.j %= 4
        self.pet.erase()
        self.pet = pet(self.group)
        self.pet.set_pet(pet_type=self.t,
                         pet_color=self.i,
                         pet_expression=self.j,
                         x=self.PET_X,
                         y=self.PET_Y)

    def nextI(self):
        self.i += 1
        self.i %= 9
        self.pet.erase()
        self.pet = pet(self.group)
        self.pet.set_pet(pet_type=self.t,
                         pet_color=self.i,
                         pet_expression=self.j,
                         x=self.PET_X,
                         y=self.PET_Y)
    def nextT(self):
        self.t += 1
        self.t %= 3
        self.pet.erase()
        self.pet = pet(self.group)
        self.pet.set_pet(pet_type=self.t,
                         pet_color=self.i,
                         pet_expression=self.j,
                         x=self.PET_X,
                         y=self.PET_Y)
        
    def update(self, dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['ascii'] == 'j':
                    self.nextJ()
                elif event['ascii'] == 'i':
                    self.nextI()
                elif event['ascii'] =='t':
                    self.nextT()
                elif event['ascii'] == 's':
                    globalStudent.pcolor = self.i
                    globalStudent.ptype = self.t
                    spyral.director.push(MainMenu())
        self.group.update(dt)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$
#END $$$$$$$$$$$$$$$$$$$$$$$

#BEGIN %%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%

#MAIN MENU
"""
Main Menu is the scene that
    -selects an option based on user position on screen

OUTPUTS
    -One of the Mini Game
    -Quits
"""

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
    def __init__(self):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child(SIZE)
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
        #END MONEY MATRIX

        #PET LOCATION (TOP LEFT HAND CORNER)
        PET_X = 430
        PET_Y = 200

        self.pet = pet(self.group)
        self.pet.set_pet(pet_type=globalStudent.ptype,
                         pet_color=globalStudent.pcolor,
                         pet_expression=globalStudent.pface,
                         x=PET_X,
                         y=PET_Y)      
  
        self.p = 0

        self.pointer = Sprite(self.group)
        self.pointer.image = spyral.Image(filename=POINTER)
        self.pointer.layer = 2
        self.pointer.x = POINTER_POINTS[self.p][0]
        self.pointer.y = POINTER_POINTS[self.p][1]
        

        self.set_pointer()      

        instructions = TextSprite(self.group, font)
        instructions.anchor = 'midbottom'
        instructions.x = 320
        instructions.y = 470
        instructions.render("MAIN MENU (p: pick  s: select)")

        self.qbutton = Sprite(self.group)
        self.qbutton.image = spyral.Image(size=(150,50))
        self.qbutton.image.fill(color = (0,0,0))
        self.qbutton.x = 430
        self.qbutton.y = 60
        self.qbutton.layer = 0

        quitbutton = TextSprite(self.group, font)
        quitbutton.anchor = 'midbottom'
        quitbutton.x = 480
        quitbutton.y = 100
        quitbutton.render ("QUIT")
    
    def set_pointer(self):
        self.pointer.image = spyral.Image(filename=POINTER)
        self.pointer.layer = 2
        self.pointer.x = POINTER_POINTS[self.p][0]
        self.pointer.y = POINTER_POINTS[self.p][1]
      
    def nextP(self):
        self.p +=1
        self.p %= len(POINTER_POINTS)
        self.set_pointer()

    def on_enter(self):
        bg = spyral.Image(size=SIZE)
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                
    def render(self):
        self.group.draw()

    #SELECTION
    """
    Based on the current index of self.p
        - 1, 6 is one currency
        - 2, 7 is one currency
        - 3, 8 is one currency
        - 4, 9 is one currency
        - 5    is one currency
        - 10   is the quit button
    """
    def update(self, dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['ascii'] == 'p':
                    self.nextP()
                elif event['ascii'] == 's':
                    if (self.p == 0 or self.p == 5):
                        spyral.director.push(CrosswordPuzzle.CrosswordMain())
                    elif (self.p == 1 or self.p == 6):
                        spyral.director.push(Basketball.Basketball())
                    elif (self.p == 2 or self.p == 7):
                        spyral.director.push(Racing.RacingMain())
                    elif (self.p == 3 or self.p == 8):
                        spyral.director.push(Cooking.CookingMain())
                    elif (self.p == 4):
                        spyral.director.pop()
                    elif (self.p == 9):
                        spyral.director.pop()
                        sys.exit()
                        return
        self.group.update(dt)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#END %%%%%%%%%%%%%%%%%%%%%%%%%%

if __name__ == "__main__":
    spyral.init()
    spyral.director.init(SIZE)
    spyral.director.push(PetSelection())
    spyral.director.run()
