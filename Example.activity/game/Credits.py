#!/usr/bin/python
'''
Ryan O'Dowd
12/01/2012
CISC 374
'''

__doc__ = ''' # @TODO: '''

import spyral

WIDTH = 1200
HEIGHT = 900

class Credits(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(Credits, self).__init__(*args, **kwargs)
        
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        self.group = spyral.Group(self.camera)


    def on_enter(self):
        background = spyral.Image(filename="images/main_backgrounds/credits.png")
        self.camera.set_background(background)

        
    def render(self):
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
