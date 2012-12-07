#!/usr/bin/python
'''
Ryan O'Dowd
12/01/2012
CISC 374
'''

__doc__ = ''' # @TODO: '''

import spyral
import pygame

WIDTH = 1200
HEIGHT = 900
SCOREBOARD_PERCENTAGE = .8
SCOREBOARD_HEIGHT = 200
FONT_SIZE = 37

CITY_POSNS = [("Touheyville", (400, 400)),
              ("Hong Kong", (1010, 500)),
              ("O'Dowd Shire", (675, 762))]
COLORS = {"city_name": (155, 255, 255)}
font = pygame.font.Font(None, FONT_SIZE)

class IntroScreen(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(IntroScreen, self).__init__(*args, **kwargs)
        
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        # We have to give our camera to the group so it knows where to draw
        self.group = spyral.Group(self.camera)


    def on_enter(self):
        background = spyral.Image(filename="images/main_backgrounds/introduction_screen.png")
        self.camera.set_background(background)

        
    def render(self):
        # Simply tell the group to draw
        self.group.draw()


    def update(self, dt):
        """
        The update loop receives dt as a parameter, which is the amount
        of time which has passed since the last time update was called.
        """
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                # press any key to continue...
                spyral.director.pop()
                return
