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

#import MainMenu # @TODO: delete
import pygame
import spyral
from spyral.sprite import Sprite
from spyral.scene import Scene
import WorldMap
import TownMap
import Clue

WIDTH = 1200
HEIGHT = 900
FONT_SIZE = 56
BG_COLOR = (100, 100, 100)
FG_COLOR = (255, 255, 255)
MY_COLOR = (255, 0, 0)

PET_TYPES = ["cat", "dog", "bird", "dragon"]

PET_COLORS = ["tan",
              "red",
              "blue",
              "green",
              "magenta",
              "cyan",
              "yellow"]
        
class Pet(spyral.Sprite):
    def __init__(self, scene):
        super(Pet, self).__init__()
        self.scene = scene

        self.color = 0
        self.pet_type = 0

        self.anchor = "center"

        self.x = 230 # @TODO: magic
        self.y = 200 # @TODO: magic

        self.clues = [Clue.Clue("Start")]
        for i in range(29):
            self.clues.append(Clue.Clue(self.clues[i].town))
        self.current_clue = 0

        self.set_pet()

    def get_clue(self):
        return self.clues[self.current_clue]
    
    def on_enter(self):
        bg = spyral.Image(size=(WIDTH, HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)


    def set_pet(self):
        self.image = spyral.Image(filename="images/pets/%s_big_%s.png" % (PET_TYPES[self.pet_type], PET_COLORS[self.color]))


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
        self.layer = 2

    def change (self):
        self.image.fill(color=BG_COLOR)
        self.layer = 0
        Sprite.__del__(self)

        
class PetSelection(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child((WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        font = pygame.font.SysFont(None, FONT_SIZE)

        self.pet = Pet(self)
        self.group.add(self.pet)

        instructions = TextSprite(self.group, font)
        instructions.anchor = 'midbottom'
        instructions.x = 450
        instructions.y = 600
        instructions.render("i: color  t: type  s: select")

        heading = TextSprite(self.group, font)
        heading.anchor = 'midbottom'
        heading.x = 450
        heading.y = 70
        heading.render("CHESTER PETS")      

    def on_enter(self):
        bg = spyral.Image(size=(WIDTH, HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                
    def render(self):
        self.group.draw()
        
    def next_color(self):
        self.pet.color = (self.pet.color + 1) % len(PET_COLORS)
        self.pet.set_pet()

    def next_type(self):
        self.pet.pet_type = (self.pet.pet_type + 1) % len(PET_TYPES)
        self.pet.set_pet()
        
    def update(self, dt):
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['ascii'] == 'i':
                    self.next_color()
                elif event['ascii'] =='t':
                    self.next_type()
                elif event['ascii'] == 's':
                    spyral.director.push(TownMap.Touheyville(self.pet))
                    #spyral.director.push(WorldMap.WorldMap(self.pet))
        self.group.update(dt)
