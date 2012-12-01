import pygame
import spyral
import random

TM_WIDTH = 640
TM_HEIGHT = 480

class WalkingPet(spyral.Sprite):
    def __init__(self,group,x,y,pivot_X,pivot_y):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.anchor = 'topleft'
        self.grid_x = x
        self.grid_y = y
        self.pos = [40*x-pivot_x,40*y-pivot_y]
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.moving = False
        self.moved = 0
    def render():
        self.image = spyral.Image(filename="pet_images/Tan_Cat_Move1.png")
    def update(self,dt):
        pass
        
class Map(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = [TM_WIDTH,TM_HEIGHT])
        self.group = spyral.Group(self.camera)
        self.up = False
        self.left = False
        self.right = False
        self.down = False
    def update(self,dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
            if event['type'] == 'KEYDOWN':
                if event['key'] == 273:
                    self.up = True
                if event['key'] == 274:
                    self.down = True
                if event['key'] == 275:
                    self.right = True
                if event['key'] == 276:
                    self.left = True
            if event['type'] == 'KEYUP':
                if event['key'] == 273:
                    self.up = False
                if event['key'] == 274:
                    self.down = False
                if event['key'] == 275:
                    self.right = False
                if event['key'] == 276:
                    self.left = False

class Room(Map):
    def __init__(self,number):
        Map.__init__(self)
        self.number = number
    def on_enter(self):
        bg = spyral.Image(size = [TM_WIDTH,TM_HEIGHT])
        bg.fill([0,0,0,255])
        self.camera.set_background(bg)
        
"""
class Lobby(Map):
    def __init__(self,shape):
        pass

class Town(Map):
    def __init__(self,name):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = [TM_WIDTH,TM_HEIGHT])
        self.group = spyral.Group(self.camera)
        self.name = name"""
