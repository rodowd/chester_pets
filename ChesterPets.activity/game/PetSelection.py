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
import WorldMap
import TownMap
import Clue
import IntroScreen

WIDTH = 1200
HEIGHT = 900
TITLE_FONT_SIZE = 72
OTHER_FONT_SIZE = 48
BG_COLOR = (100, 100, 100)
FG_COLOR = (0, 0, 0)
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
        self.hat = False
        self.hats = [False]

        self.anchor = "center"
        self.money = 0

        self.previous_posns = []

        self.selection_x = 600
        self.selection_y = 450

        games = ["Crossword", "Basketball", "Cooking"]
        self.minigames = [games[i%3] for i in range(10)]
        self.minigames[9] = "Ending"


        self.clues = [Clue.Clue("Start")]
        for i in range(10):
            self.clues.append(Clue.Clue(self.clues[i].town))
        self.current_clue = 0
        
        self.destination = "Touheyville"

        self.vehicle = Vehicle("car",[200,50,300,300])
        self.vehicles = ["car"]

        self.set_pet()


    def get_last_posn(self):
        if len(self.previous_posns) == 0:
            return

        
        self.set_pet_image("big")
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
        self.set_pet_image("big")
        self.x = self.selection_x
        self.y = self.selection_y

    def set_pet_image(self,name):
        string = ("images/pets/%s_"+name+"_%s.png") % (PET_TYPES[self.pet_type], PET_COLORS[self.color])
        self.image = spyral.Image(filename = string)
        if self.hat:
            if name=="nom1" or name=="nom2":
                name = "big"
            string = ("images/pets/accessories/hats/%s_%s_"+name+".png") % (self.hat,PET_TYPES[self.pet_type])
            hat_image = spyral.Image(filename = string)
            self.image._surf.blit(hat_image._surf,[0,0])

class Vehicle(spyral.Sprite):
    def __init__(self,name,stats):
        spyral.Sprite.__init__(self)
        self.name = name
        self.stats = stats
        self.pos = [WIDTH/2,HEIGHT-350]
        self.anchor = 'center'
        self.render()
    def render(self):
        self.image = spyral.Image(size = [500,500])
        image = spyral.Image(filename = "images/racing/automobiles/"+self.name+".png")
        self.image._surf.blit(image._surf,[250-image._surf.get_width()/2,100-image._surf.get_height()/2])
        stat_names = ["Speed","Accel.","Handle","Turning"]
        maxes = [400,100,600,600]
        colors = [[255,0,0,255],[0,0,255,255],[255,255,0,255],[0,255,0,255]]
        font = pygame.font.SysFont(None,40)
        for i in range(4):
            surf = font.render(stat_names[i],True,[0,0,0,255])
            self.image._surf.blit(surf,[20,200+50*i])
            self.image.draw_rect(colors[i],[150,195+50*i],[(300.0*self.stats[i])/maxes[i],35])

class TextSprite(Sprite):
    def __init__(self, group, font):
        Sprite.__init__(self, group)
        self.font = font
        
    def render(self, text):
        surf = self.font.render(text, True, FG_COLOR).convert_alpha()
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
        instructions_y_posn = 570
        
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child((WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        other_font = pygame.font.SysFont(None, OTHER_FONT_SIZE)

        self.pet = Pet(self)
        self.group.add(self.pet)

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
        bg = spyral.Image(filename="images/main_backgrounds/pet_selection.png")
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
                    spyral.director.replace(WorldMap.WorldMap(self.pet))
                    spyral.director.push(IntroScreen.IntroScreen())
