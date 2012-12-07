#!/usr/bin/python
'''
Ryan O'Dowd
12/01/2012
CISC 374
'''

__doc__ = ''' # @TODO: '''

import spyral
import Credits

WIDTH = 1200
HEIGHT = 900

class EndingScreen(spyral.Scene):
    def __init__(self, passed_in_pet, *args, **kwargs):
        super(EndingScreen, self).__init__(*args, **kwargs)
        
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        # We have to give our camera to the group so it knows where to draw
        self.group = spyral.Group(self.camera)

        self.group.add(passed_in_pet)

        self.credits_have_been_shown = False;


    def on_enter(self):
        background = spyral.Image(filename="images/main_backgrounds/ending_screen.png")
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
                spyral.director.replace(Credits.Credits())
                return
