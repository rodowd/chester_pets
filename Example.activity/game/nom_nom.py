#!/usr/bin/python
'''
Ryan O'Dowd, Kevin Touhey, and Yifan Hong
CISC 374
Fall 2012
'''

import pygame
import spyral
from spyral.sprite import Sprite
from spyral.scene import Scene
import globalStudent

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

#BEGIN!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!
# @TODO: put it Cooking.py

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
                    spyral.director.pop()
                    spyral.director.push(Nom())
        self.group.update(dt)

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
        self.i = globalStudent.pcolor
        self.t = globalStudent.ptype

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
                    spyral.director.pop()
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

