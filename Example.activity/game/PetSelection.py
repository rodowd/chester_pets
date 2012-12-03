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
import random

WIDTH = 1200
HEIGHT = 900
TITLE_FONT_SIZE = 72
OTHER_FONT_SIZE = 48
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
        self.money = 100

        self.previous_posns = []

        self.selection_x = 600
        self.selection_y = 450

        self.clues = [Clue.Clue("Start")]
        for i in range(29):
            self.clues.append(Clue.Clue(self.clues[i].town))
        self.current_clue = 0
        
        games = ["Crossword", "Basketball", "Cooking"]
        self.minigames = []
        for i in range(30):
            self.minigames.append(games[random.randint(0,0)])
            # @TODO: Change this to (0,2)


        self.destination = "Touheyville"

        self.set_pet()


    def get_last_posn(self):
        if len(self.previous_posns) == 0:
            return

        self.image = spyral.Image(filename="images/pets/%s_big_%s.png" % (PET_TYPES[self.pet_type], PET_COLORS[self.color]))
        self.pos = self.previous_posns.pop()

        

    def get_pet_types(self):
        return PET_TYPES


    def get_pet_colors(self):
        return PET_COLORS


    def get_game(self):
        return self.minigames[self.current_clue]
        
    def get_clue(self):
        return self.clues[self.current_clue]
    
    def on_enter(self):
        bg = spyral.Image(size=(WIDTH, HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)


    def set_pet(self):
        self.image = spyral.Image(filename="images/pets/%s_big_%s.png" % (PET_TYPES[self.pet_type], PET_COLORS[self.color]))
        self.x = self.selection_x
        self.y = self.selection_y


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
        line_space = 50
        instructions_x_posn = 600
        instructions_y_posn = 700
        
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child((WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE)
        other_font = pygame.font.SysFont(None, OTHER_FONT_SIZE)

        self.pet = Pet(self)
        self.group.add(self.pet)

        heading = TextSprite(self.group, title_font)
        heading.anchor = 'midbottom'
        heading.x = 600
        heading.y = 100
        heading.render("CHESTER PETS")      

        color_instructions = TextSprite(self.group, other_font)
        color_instructions.anchor = 'midbottom'
        color_instructions.x = instructions_x_posn
        color_instructions.y = instructions_y_posn + line_space
        color_instructions.render("Press 'c' to cycle through colors.")
        
        type_instructions = TextSprite(self.group, other_font)
        type_instructions.anchor = 'midbottom'
        type_instructions.x = instructions_x_posn
        type_instructions.y = instructions_y_posn + (2 * line_space)
        type_instructions.render("Press 't' to cycle through types of pets.")

        enter_instructions = TextSprite(self.group, other_font)
        enter_instructions.anchor = 'midbottom'
        enter_instructions.x = instructions_x_posn
        enter_instructions.y = instructions_y_posn + (3 * line_space)
        enter_instructions.render("Press 'Enter' when you are finished.") 


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
                if event['ascii'] == 'c':
                    self.next_color()
                elif event['ascii'] =='t':
                    self.next_type()
                elif event['key'] == 13:
                    # enter
                    self.pet.previous_posns.append(self.pet.pos)
                    spyral.director.push(WorldMap.WorldMap(self.pet))
                    spyral.director.push(TownMap.Touheyville(self.pet))
