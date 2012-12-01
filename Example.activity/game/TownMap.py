import pygame
import spyral
import random

TM_WIDTH = 1200
TM_HEIGHT = 900

class WalkingPet(spyral.Sprite):
    def __init__(self,mapgrid,x,y,pivot_x,pivot_y):
        spyral.Sprite.__init__(self,mapgrid.group)
        self.group.add(self)
        self.mapgrid = mapgrid
        self.anchor = 'topleft'
        self.grid_x = x
        self.grid_y = y
        self.pos = [50*x-pivot_x,50*y-pivot_y]
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.moving = False
        self.moved = 0
        self.facing = "up"
        self.set_moving_images()
        self.render()
    def set_moving_images(self):
        self.images = [spyral.Image(filename = "pet_images/Tan_Cat_Move1.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move2.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move1.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move2.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move1.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move2.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move1.png"),
                       spyral.Image(filename = "pet_images/Tan_Cat_Move2.png")]
        for i in range(4):
            self.images[i*2].rotate(i*90)
            self.images[i*2+1].rotate(i*90)
    def render(self):
        i = 6
        if self.facing == "up":
            i = 0
        if self.facing == "left":
            i = 2
        if self.facing == "down":
            i = 4
        if self.moved<=.25 and self.moved>0:
            self.image = self.images[i+1]
        else:
            self.image = self.images[i]
    def finish_move(self):
        if self.moving=="up":
            self.grid_y-=1
        elif self.moving=="down":
            self.grid_y+=1
        elif self.moving=="right":
            self.grid_x+=1
        elif self.moving=="left":
            self.grid_x-=1
        self.pos = [50*self.grid_x-self.pivot_x,50*self.grid_y-self.pivot_y]
        print self.grid_x,self.grid_y
        print self.pos[0],self.pos[1]
        self.moving = False
        self.moved = 0
    def set_position(self):
        x = 0
        y = 0
        if self.moving=="up":
            y = -1
        elif self.moving=="down":
            y = 1
        elif self.moving=="right":
            x = 1
        elif self.moving=="left":
            x = -1
        self.x = self.grid_x*50+x*100*self.moved-self.pivot_x
        self.y = self.grid_y*50+y*100*self.moved-self.pivot_y
    def update(self,dt):
        if self.moving:
            self.moved+=dt
            if self.moved>=.5:
                self.finish_move()
            else:
                self.set_position()
            self.render()
        if not(self.moving):
            if self.mapgrid.up:
                self.moving = "up"
            elif self.mapgrid.down:
                self.moving = "down"
            elif self.mapgrid.right:
                self.moving = "right"
            elif self.mapgrid.left:
                self.moving = "left"
            if self.moving:
                self.facing = self.moving
            
                
class MapGrid(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (TM_WIDTH,TM_HEIGHT))
        self.group = spyral.Group(self.camera)
        self.up = False
        self.left = False
        self.right = False
        self.down = False
        self.pet = WalkingPet(self,10,10,0,0)
    def render(self):
        self.group.draw()
    def update(self,dt):
        self.group.update(dt)
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

class Room(MapGrid):
    def __init__(self,number):
        MapGrid.__init__(self)
        self.number = number
    def on_enter(self):
        bg = spyral.Image(filename="world_images/TheROOM.png")
        self.camera.set_background(bg)
        
"""
class Lobby(MapGrid):
    def __init__(self,shape):
        pass

class Town(MapGrid):
    def __init__(self,name):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = [TM_WIDTH,TM_HEIGHT])
        self.group = spyral.Group(self.camera)
        self.name = name"""
