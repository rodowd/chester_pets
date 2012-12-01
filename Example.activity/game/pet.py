import pygame
import spyral
from spyral.sprite import Sprite
from spyral.scene import Scene

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

        
class pet(Scene):
    def __init__(self,group):
        self.group = group
        #self.set_pet(self,pet_type=0,pet_color=0,pet_expression=0,x=0,y=0)

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


    def set_pet(self,pet_type,pet_color,pet_expression,x,y):

        self.t = pet_type
        self.j = pet_expression 
        self.i = pet_color
        
        self.head = Sprite(self.group)
        self.head.image = spyral.Image(filename=HEADS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], HEAD_LAYER)
        self.head.layer = HEAD_LAYER
        self.head.x = PET_POINTS[1][0]+x
        self.head.y = PET_POINTS[1][1]+y

        self.body = Sprite(self.group)
        self.body.image = spyral.Image(filename=BODIES[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], BODY_LAYER)
        self.body.layer = BODY_LAYER
        self.body.x = PET_POINTS[8][0]+x
        self.body.y = PET_POINTS[8][1]+y

        self.arms = Sprite(self.group)
        self.arms.image = spyral.Image(filename=ARMS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], ARMS_LAYER)
        self.arms.layer = ARMS_LAYER
        self.arms.x = PET_POINTS[3][0]+x
        self.arms.y = PET_POINTS[3][1]+y

        self.legs = Sprite(self.group)
        self.legs.image = spyral.Image(filename=LEGS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], LEGS_LAYER)
        self.legs.layer = LEGS_LAYER
        self.legs.x = PET_POINTS[5][0]+x
        self.legs.y = PET_POINTS[5][1]+y

        self.tail = Sprite(self.group)
        self.tail.image = spyral.Image(filename=TAILS[TYPES[self.t]][0])
        self.recolor(COLOR_TAN, COLORS[self.i], TAIL_LAYER)
        self.tail.layer = TAIL_LAYER
        self.tail.x = PET_POINTS[9][0]+x
        self.tail.y = PET_POINTS[9][1]+y

        self.face = Sprite(self.group)
        if self.t <= 1:
            self.face.image=spyral.Image(filename=CD_FACES[self.j])
        elif self.t >=2:
            self.face.image=spyral.Image(filename=DB_FACES[self.j])
        self.face.layer = FACE_LAYER
        self.face.x = PET_POINTS[2][0]+x
        self.face.y = PET_POINTS[2][1]+y
        

    def erase(self):
        self.group.remove(self.head)
        self.group.remove(self.arms)
        self.group.remove(self.body)
        self.group.remove(self.legs)
        self.group.remove(self.face)
        self.group.remove(self.tail)
        
        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$
#END $$$$$$$$$$$$$$$$$$$$$$$
