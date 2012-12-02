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

WIDTH = 1200
HEIGHT = 900
FONT_SIZE = 42
BG_COLOR = (100, 100, 100)
FG_COLOR = (255, 255, 255)

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
        self.camera = self.parent_camera.make_child((WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.oven_image = spyral.Image(filename="images/cooking/oven.png")
        self.oven_image.x = 200
        self.oven_image.y = 100
        # @TODO: make sure oven gets drawn

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
        bg = spyral.Image(size=(WIDTH, HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
                

    def render(self):
        self.group.draw()


    def update(self, dt):
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['ascii'] == 's':
                    spyral.director.pop()
                    spyral.director.push(Nom())


class Nom(Scene):
    def __init__(self, passed_in_pet):
        Scene.__init__(self)
        self.camera = self.parent_camera.make_child((WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)

        self.counter = 0
        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.nomIndex = 0
        self.cookieIndex = 0

        self.eatIndex = 0

        # @TODO: eat cookie here; make sure passed_in_pet eats it


    def on_enter(self):
        bg = spyral.Image(size=(WIDTH, HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)

                
    def render(self):
        self.group.draw()
