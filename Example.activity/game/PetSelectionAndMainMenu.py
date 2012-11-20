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

SIZE = (640, 480)
FONT_SIZE = 42
BG_COLOR = (100, 100, 100)
FG_COLOR = (255, 255, 255)
MY_COLOR = (255, 0, 0)

# PET TYPE
CAT = 0
DOG = 1
BIRD = 3
DRAGON = 2

TYPES = [CAT, DOG, DRAGON]

# LAYERS
HAT_LAYER = 7
COOKIE_LAYER = 6
HEAD_LAYER = 4
FACE_LAYER = 5
ARMS_LAYER = 3
SLEEVE_LAYER = 4
LEGS_LAYER = 2
PANTS_LAYER = 3
SHIRT_LAYER = 2
BODY_LAYER = 1
TAIL_LAYER = 0

#==========================================
# GLOBAL LIST VARIABLES

"""
This saves the indexes from the lists of pet types and colors
"""
STUDENT_COLOR = 0
STUDENT_TYPE = 0
STUDENT_PET = [STUDENT_COLOR,STUDENT_TYPE]

STUDENT_MONEY = []
STUDENT_HATS = []
#ect

#===========================================

#DEFAULT COLOR IS TAN
COLOR_TAN = (185,122,87)

#ADDITIONAL COLORS
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 255, 0)
COLOR_GREEN = (0, 0, 255)
COLOR_DARK_RED = (125, 0, 0)
COLOR_PINK = (200, 100, 100)
COLOR_PURPLE = (255, 255, 0)
COLOR_ORANGE = (255, 39, 139)
COLOR_WHITE = (255, 255, 255)

COLORS = [COLOR_TAN,
          COLOR_RED,
          COLOR_BLUE,
          COLOR_GREEN,
          COLOR_PINK,
          COLOR_DARK_RED,
          COLOR_PURPLE,
          COLOR_ORANGE,
          COLOR_WHITE]

#********************************************
# FILES

#POINTER
POINTER = 'pet_images/POINTER.png'

#MONEY
STAR = 'pet_images/STAR.png'
DIAMOND = 'pet_images/Diamond.png'
CUBE = 'pet_images/Cube.png'
SPHERE = 'pet_images/Sphere.png'
MOON = 'pet_images/Moon.png'

#HEADS
TAN_CAT_HEAD = 'pet_images/TAN_CAT_HEAD.png'
TAN_DOG_HEAD = 'pet_images/TAN_DOG_HEAD.png'
TAN_DRA_HEAD = 'pet_images/TAN_DRAGON_HEAD.png'

#BODY
TAN_CAT_BODY = 'pet_images/TAN_CAT_BODY.png'

#ARMS
TAN_CAT_ARMS = 'pet_images/TAN_CAT_ARMS.png'
TAN_DRA_ARMS = 'pet_images/TAN_DRAGON_ARMS.png'
TAN_FOLK_CAT_ARMS1 = 'pet_images/TAN_FOLK_CAT_ARMS1.png'
TAN_FOLK_CAT_ARMS2 = 'pet_images/TAN_FOLK_CAT_ARMS2.png'
TAN_CAT_ARMS_NOM1 = 'pet_images/TAN_CAT_ARMS_NOM1.png'
TAN_CAT_ARMS_NOM2 = 'pet_images/TAN_CAT_ARMS_NOM2.png'
TAN_DRA_ARMS_NOM1 = 'pet_images/TAN_DRAGON_ARMS_NOM1.png'
TAN_DRA_ARMS_NOM2 = 'pet_images/TAN_DRAGON_ARMS_NOM2.png'

#LEGS
TAN_CAT_LEGS = 'pet_images/TAN_CAT_LEGS.png'
TAN_DRA_LEGS = 'pet_images/TAN_DRAGON_LEGS.png'
TAN_FOLK_CAT_LEGS1 = 'pet_images/TAN_FOLK_CAT_LEGS1.png'
TAN_FOLK_CAT_LEGS2 = 'pet_images/TAN_FOLK_CAT_LEGS2.png'
TAN_FOLK_CAT_LEGS3 = 'pet_images/TAN_FOLK_CAT_LEGS3.png'

#TAILS
TAN_CAT_TAIL = 'pet_images/TAN_CAT_TAIL.png'
TAN_DOG_TAIL = 'pet_images/TAN_DOG_TAIL.png'
TAN_DRA_TAIL = 'pet_images/TAN_DRAGON_TAIL.png'
TAN_CAT_TAIL2 = 'pet_images/TAN_CAT_TAIL2.png'
TAN_DOG_TAIL2 = 'pet_images/TAN_DOG_TAIL2.png'

#FACES
CD_NORMAL_FACE = 'pet_images/CAT_EXPRESSION_NORMAL.png'
CD_WINK_FACE = 'pet_images/CAT_EXPRESSION_WINK.png'
CD_SAD_FACE = 'pet_images/CAT_EXPRESSION_SAD.png'
CD_HAPPY_FACE = 'pet_images/CAT_EXPRESSION_HAPPY.png'
CD_NOM_FACE = 'pet_images/CAT_NOM_NOM.png'

DB_NORMAL_FACE ='pet_images/DRA_EXPRESSION_NORMAL.png'
DB_SAD_FACE = 'pet_images/DRA_EXPRESSION_SAD.png'
DB_HAPPY_FACE = 'pet_images/DRA_EXPRESSION_HAPPY.png'
DB_WINK_FACE = 'pet_images/DRA_EXPRESSION_WINK.png'

#COOKIE
COOKIE = 'cooking_images/COOKIE.png'
COOKIE_NOMD = 'cooking_images/COOKIE_NOMD.png'

#OVEN
OVEN = 'cooking_images/OVEN.png'
#**********************************************

#MONIES
MONIES = [STAR,
          DIAMOND,
          CUBE,
          SPHERE,
          MOON]

#CAT DOG FACES
CD_FACES = [CD_SAD_FACE,
            CD_NORMAL_FACE,
            CD_WINK_FACE,
            CD_HAPPY_FACE]

#BIRD DRAGON FACES
DB_FACES = [DB_SAD_FACE,
            DB_NORMAL_FACE,
            DB_WINK_FACE,
            DB_HAPPY_FACE]

#COOKIES
COOKIES = [COOKIE,
           COOKIE_NOMD]


#COMPONENTS (FOR SELECTION)
HEADS = [(TAN_CAT_HEAD, TAN_CAT_HEAD, TAN_CAT_HEAD),
         (TAN_DOG_HEAD, TAN_DOG_HEAD, TAN_DOG_HEAD),
         (TAN_DRA_HEAD, TAN_DRA_HEAD, TAN_DRA_HEAD)]

BODIES = [(TAN_CAT_BODY, TAN_CAT_BODY, TAN_CAT_BODY),
          (TAN_CAT_BODY, TAN_CAT_BODY, TAN_CAT_BODY),
          (TAN_CAT_BODY, TAN_CAT_BODY, TAN_CAT_BODY)]

ARMS = [
    (TAN_CAT_ARMS, TAN_CAT_ARMS_NOM1, TAN_CAT_ARMS_NOM2),
    (TAN_CAT_ARMS, TAN_CAT_ARMS_NOM1, TAN_CAT_ARMS_NOM2),
    (TAN_DRA_ARMS, TAN_DRA_ARMS_NOM1, TAN_DRA_ARMS_NOM2),
]

LEGS = [(TAN_CAT_LEGS, TAN_CAT_LEGS,TAN_CAT_LEGS),
        (TAN_CAT_LEGS, TAN_CAT_LEGS,TAN_CAT_LEGS),
        (TAN_DRA_LEGS, TAN_DRA_LEGS,TAN_DRA_LEGS)]

TAILS = [(TAN_CAT_TAIL, TAN_CAT_TAIL2),
         (TAN_DOG_TAIL, TAN_DOG_TAIL2),
         (TAN_DRA_TAIL, TAN_DRA_TAIL)]

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
    
        PET_X = 230
        PET_Y = 200

        self.head = Sprite(self.group)
        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.head.layer = HEAD_LAYER
        self.head.x = PET_POINTS[1][0]+PET_X
        self.head.y = PET_POINTS[1][1]+PET_Y

        self.body = Sprite(self.group)
        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.body.layer = BODY_LAYER
        self.body.x = PET_POINTS[8][0]+PET_X
        self.body.y = PET_POINTS[8][1]+PET_Y

        self.arms = Sprite(self.group)
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.arms.layer = ARMS_LAYER
        self.arms.x = PET_POINTS[3][0]+PET_X
        self.arms.y = PET_POINTS[3][1]+PET_Y

        self.legs = Sprite(self.group)
        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.legs.layer = LEGS_LAYER
        self.legs.x = PET_POINTS[5][0]+PET_X
        self.legs.y = PET_POINTS[5][1]+PET_Y

        self.tail = Sprite(self.group)
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.tail.layer = TAIL_LAYER
        self.tail.x = PET_POINTS[9][0]+PET_X
        self.tail.y = PET_POINTS[9][1]+PET_Y

        self.j = 1

        self.face = Sprite(self.group)
        if self.t <= 1:
            self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2:
            self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER
        self.face.x = PET_POINTS[2][0]+PET_X
        self.face.y = PET_POINTS[2][1]+PET_Y

        self.i = 0
        
        self.set_face()
        self.set_color()
        self.set_type()

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

    def set_color(self):
        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], BODY_LAYER)
        self.body.layer = BODY_LAYER
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], ARMS_LAYER)
        self.arms.layer = ARMS_LAYER

        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], LEGS_LAYER)
        self.legs.layer = LEGS_LAYER
        
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], TAIL_LAYER)
        self.tail.layer = TAIL_LAYER

        if self.t <= 1:
            self.face.image = spyral.Image(filename=CD_FACES[self.j])
        elif self.t >= 2:
            self.face.image = spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER


    def set_face(self):
        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], BODY_LAYER)
        self.body.layer = BODY_LAYER
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], ARMS_LAYER)
        self.arms.layer = ARMS_LAYER

        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], LEGS_LAYER)
        self.legs.layer = LEGS_LAYER
        
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], TAIL_LAYER)
        self.tail.layer = TAIL_LAYER
        
        if self.t <= 1:
            self.face.image = spyral.Image(filename=CD_FACES[self.j])
        elif self.t >= 2:
            self.face.image = spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER

    def set_type(self):
        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], BODY_LAYER)
        self.body.layer = BODY_LAYER
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], ARMS_LAYER)
        self.arms.layer = ARMS_LAYER

        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], LEGS_LAYER)
        self.legs.layer = LEGS_LAYER
        
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], TAIL_LAYER)
        self.tail.layer = TAIL_LAYER

        if self.t <= 1:
            self.face.image = spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2:
            self.face.image = spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER
        
    def nextJ(self):
        self.j += 1
        self.j %= len(CD_FACES)
        self.set_face()

    def nextI(self):
        self.i += 1
        self.i %= len(COLORS)
        self.set_face()

    def nextT(self):
        self.t += 1
        self.t %= len(TYPES)
        self.set_type()
        
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
                    STUDENT_PET[0] = self.i # SAVES COLOR
                    STUDENT_PET[1] = self.t # SAVES TYPE
                    print(STUDENT_PET[0],STUDENT_PET[1])
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
        
        self.i = STUDENT_PET[0] # Color
        self.t = STUDENT_PET[1] # Type

        #PET LOCATION (TOP LEFT HAND CORNER)
        PET_X = 430
        PET_Y = 200
        
        self.head = Sprite(self.group)
        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.head.layer = HEAD_LAYER
        self.head.x = PET_POINTS[1][0]+PET_X
        self.head.y = PET_POINTS[1][1]+PET_Y

        self.body = Sprite(self.group)
        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.body.layer = BODY_LAYER
        self.body.x = PET_POINTS[8][0]+PET_X
        self.body.y = PET_POINTS[8][1]+PET_Y

        self.arms = Sprite(self.group)
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.arms.layer = ARMS_LAYER
        self.arms.x = PET_POINTS[3][0]+PET_X
        self.arms.y = PET_POINTS[3][1]+PET_Y

        self.legs = Sprite(self.group)
        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.legs.layer = LEGS_LAYER
        self.legs.x = PET_POINTS[5][0]+PET_X
        self.legs.y = PET_POINTS[5][1]+PET_Y

        self.tail = Sprite(self.group)
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.tail.layer = TAIL_LAYER
        self.tail.x = PET_POINTS[9][0]+PET_X
        self.tail.y = PET_POINTS[9][1]+PET_Y

        self.j = 1

        self.face = Sprite(self.group)
        if self.t <= 1: self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2: self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER
        self.face.x = PET_POINTS[2][0]+PET_X
        self.face.y = PET_POINTS[2][1]+PET_Y
  
        self.p = 0

        self.pointer = Sprite(self.group)
        self.pointer.image = spyral.Image(filename=POINTER)
        self.pointer.layer = 2
        self.pointer.x = POINTER_POINTS[self.p][0]
        self.pointer.y = POINTER_POINTS[self.p][1]
        

        self.set_pointer()      
        self.set_face()
        self.set_color()
        #self.set_type()

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

    def recolor(self,color1,color2,a):
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
                if surf.get_at((x,y))==color1:
                    surf.set_at((x,y),color2)
                
    def on_enter(self):
        bg = spyral.Image(size=SIZE)
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                
    def render(self):
        self.group.draw()

    def set_color(self):

        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],BODY_LAYER)
        self.body.layer = BODY_LAYER
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],ARMS_LAYER)
        self.arms.layer = ARMS_LAYER

        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],LEGS_LAYER)
        self.legs.layer = LEGS_LAYER
        
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],TAIL_LAYER)
        self.tail.layer = TAIL_LAYER

        if self.t <= 1: self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2: self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER


    def set_face(self):

        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],BODY_LAYER)
        self.body.layer = BODY_LAYER
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],ARMS_LAYER)
        self.arms.layer = ARMS_LAYER

        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],LEGS_LAYER)
        self.legs.layer = LEGS_LAYER
        
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN,COLORS[self.i],TAIL_LAYER)
        self.tail.layer = TAIL_LAYER
        
        if self.t <= 1: self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2: self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER

    
    def set_pointer(self):
        self.pointer.image = spyral.Image(filename=POINTER)
        self.pointer.layer = 2
        self.pointer.x = POINTER_POINTS[self.p][0]
        self.pointer.y = POINTER_POINTS[self.p][1]
      
    def nextJ(self):
        self.j += 1
        self.j %= len(CD_FACES)
        self.set_face()

    def nextP(self):
        self.p +=1
        self.p %= len(POINTER_POINTS)
        self.set_pointer()

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
                        spyral.director.push(Cooking.Bake())
                    elif (self.p == 9):
                        spyral.director.pop()
                        return
        self.group.update(dt)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#END %%%%%%%%%%%%%%%%%%%%%%%%%%

#BEGIN!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!
# @TODO: put it Cooking.py
class Bake(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child(SIZE)
        self.group = spyral.Group(self.camera)

        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.head = Sprite(self.group)
        self.head.image = spyral.Image(filename=OVEN)
        self.head.x = 200
        self.head.y = 100

        instructions = TextSprite(self.group, self.font)
        instructions.anchor = 'midbottom'
        instructions.x = 320
        instructions.y = 470
        instructions.render("s: taste")

        self.heading = TextSprite(self.group, self.font)
        self.heading.anchor = 'midbottom'
        self.heading.x = 330
        self.heading.y = 50
        self.heading.render("BAKING")

    def on_enter(self):
        bg = spyral.Image(size=SIZE)
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
                if event['ascii'] == 's':
                    spyral.director.push(Nom())
        self.group.update(dt)

#NOM SCENE

NOM_INDEX = [ # This selects the pet components
    ( 0, 0, 1, 1, 0 ),
    ( 0, 0, 2, 4, 0 ),
    ( 0, 0, 2, 4, 0 ),
    ( 0, 0, 1, 1, 0 ),
]

COOKIE_POINTS = [
    ((42,110),(42,60)),
    ((42,60),(42,110))
]

class Nom(Scene):

    def __init__(self):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child(SIZE)
        self.group = spyral.Group(self.camera)

        self.counter = 0
        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.nomIndex = 0
        self.cookieIndex = 0

        self.eatIndex = 0
        #PET LOCATION (TOP LEFT HAND CORNER)
    
        PET_X = 230
        PET_Y = 150

        self.j = 1
        self.i = STUDENT_PET[0] # Color
        self.t = STUDENT_PET[1] # Type

        self.head = Sprite(self.group)
        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][NOM_INDEX[self.nomIndex][0]])
        self.head.layer = HEAD_LAYER
        self.head.x = PET_POINTS[1][0]+PET_X
        self.head.y = PET_POINTS[1][1]+PET_Y
        
        self.arms = Sprite(self.group)
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][NOM_INDEX[self.nomIndex][2]])
        self.arms.layer = ARMS_LAYER
        self.arms.x = PET_POINTS[3][0]+PET_X
        self.arms.y = PET_POINTS[3][1]+PET_Y

        self.face = Sprite(self.group)
        if self.t <= 1: self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2: self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER
        self.face.x = PET_POINTS[2][0]+PET_X
        self.face.y = PET_POINTS[2][1]+PET_Y

        self.cookie = Sprite(self.group)
        self.cookie.image = spyral.Image(filename=COOKIES[self.cookieIndex])
        self.cookie.layer = COOKIE_LAYER
        self.cookie.x = COOKIE_POINTS[self.eatIndex][self.cookieIndex][0]+PET_X
        self.cookie.y = COOKIE_POINTS[self.eatIndex][self.cookieIndex][1]+PET_Y       
  
        self.set_color()

        instructions = TextSprite(self.group, self.font)
        instructions.anchor = 'midbottom'
        instructions.x = 320
        instructions.y = 470
        instructions.render("s: quit")

        self.heading = TextSprite(self.group, self.font)
        self.heading.anchor = 'midbottom'
        self.heading.x = 320
        self.heading.y = 50
        self.heading.render("TASTING")

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

    def recolor(self,color1,color2,a):
        if   a==HEAD_LAYER:surf = self.get_head()
        elif a==BODY_LAYER:surf = self.get_body()
        elif a==ARMS_LAYER:surf = self.get_arms()
        elif a==LEGS_LAYER:surf = self.get_legs()
        elif a==TAIL_LAYER:surf = self.get_tail()
        w = surf.get_width()
        h = surf.get_height()
        for x in range(w):
            for y in range(h):
                if surf.get_at((x,y))==color1:
                    surf.set_at((x,y),color2)
                
    def on_enter(self):
        bg = spyral.Image(size=SIZE)
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                
    def render(self):
        self.group.draw()

    def set_color(self):

        #PET LOCATION (TOP LEFT HAND CORNER)
    
        PET_X = 230
        PET_Y = 150

        self.group.remove(self.cookie)
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][NOM_INDEX[self.nomIndex][2]])
        self.recolor(COLOR_TAN,COLORS[self.i],ARMS_LAYER)
        self.arms.layer = ARMS_LAYER
        
        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][NOM_INDEX[self.nomIndex][0]])
        self.recolor(COLOR_TAN,COLORS[self.i],HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        if self.t <= 1: self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2: self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER
        
        self.cookie = Sprite(self.group)
        self.cookie.image = spyral.Image(filename=COOKIES[self.eatIndex])
        self.cookie.layer = COOKIE_LAYER
        self.cookie.x = COOKIE_POINTS[self.eatIndex][self.cookieIndex][0]+PET_X
        self.cookie.y = COOKIE_POINTS[self.eatIndex][self.cookieIndex][1]+PET_Y  



    def setNOM(self):
        self.nomIndex += 1
        self.nomIndex %= len(NOM_INDEX)
        self.cookieIndex += 1
        self.cookieIndex %= len(COOKIES)
        if self.nomIndex <= 1: self.eatIndex = 0
        elif self.nomIndex >= 2: self.eatIndex =1
        self.set_color()
        print(self.nomIndex)

    
    def set_face(self):
        #PET LOCATION (TOP LEFT HAND CORNER)
        PET_X = 230
        PET_Y = 150

        self.group.remove(self.cookie)
        
        self.bg = Sprite(self.group)
        self.bg.image = spyral.Image(size=(200,200))
        self.bg.image.fill(color=BG_COLOR)
        
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][NOM_INDEX[self.nomIndex][2]])
        self.recolor(COLOR_TAN, COLORS[self.i], ARMS_LAYER)
        self.arms.layer = ARMS_LAYER
        
        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][NOM_INDEX[self.nomIndex][0]])
        self.recolor(COLOR_TAN, COLORS[self.i], HEAD_LAYER)
        self.head.layer = HEAD_LAYER

        
        if self.t <= 1:
            self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2:
            self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER

        self.cookie = Sprite(self.group)
        self.cookie.image = spyral.Image(filename=COOKIES[self.eatIndex])
        self.cookie.layer = COOKIE_LAYER
        self.cookie.x = COOKIE_POINTS[self.eatIndex][self.cookieIndex][0]+PET_X
        self.cookie.y = COOKIE_POINTS[self.eatIndex][self.cookieIndex][1]+PET_Y  
    
    def update(self, dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['ascii'] == 's':
                    spyral.director.push(MainMenu())
        self.group.update(dt)
        self.counter += dt

        answer = 0
        if self.counter > 1 and self.counter <= 1+dt:
            self.setNOM()
        if self.counter > 2 and self.counter <= 2+dt:
            self.setNOM()
        if self.counter > 3 and self.counter <= 3+dt:
            self.setNOM()
            #CHANGE ANSWERS HERE!!!!! 
            if answer == 0:
                self.j = 3
                self.set_face()
            elif answer == 1:
                self.j = 0
                self.set_face()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!
#END!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == "__main__":
    spyral.init()
    spyral.director.init(SIZE)
    spyral.director.push(PetSelection())
    spyral.director.run()
