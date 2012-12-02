import spyral
import pygame

TM_WIDTH = 1200
TM_HEIGHT = 900
NUMBER_FONT = pygame.font.SysFont(None,20)

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
        self.changed_room = False
        self.render()
    def set_moving_images(self):
        move1 = self.get_move1()
        move2 = self.get_move2()
        self.images = [spyral.Image(filename = move1),
                       spyral.Image(filename = move2),
                       spyral.Image(filename = move1),
                       spyral.Image(filename = move2),
                       spyral.Image(filename = move1),
                       spyral.Image(filename = move2),
                       spyral.Image(filename = move1),
                       spyral.Image(filename = move2)]
        for i in range(4):
            self.images[i*2].rotate(i*90)
            self.images[i*2+1].rotate(i*90)
    def get_move1(self):
        moves = ["cat_move1_tan.png",
                 "dog_move1_tan.png",
                 "bird_move_tan.png",
                 "dragon_move_tan.png"]
        return "images/pets/"+moves[self.mapgrid.pet.pet_type]
    def get_move2(self):
        moves = ["cat_move2_tan.png",
                 "dog_move2_tan.png",
                 "bird_move_tan.png",
                 "dragon_move_tan.png"]
        return "images/pets/"+moves[self.mapgrid.pet.pet_type]
    def render(self):
        i = 6
        if self.facing == "up":
            i = 0
        if self.facing == "left":
            i = 2
        if self.facing == "down":
            i = 4
        if self.moved<=.2 and self.moved>0:
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
        self.changed_room = False
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
        self.x = self.grid_x*50+x*125*self.moved-self.pivot_x
        self.y = self.grid_y*50+y*125*self.moved-self.pivot_y
    def is_valid_move(self):
        if not(self.moving):
            return True
        x = self.grid_x
        y = self.grid_y
        if self.moving=="up":
            y-=1
        elif self.moving=="down":
            y+=1
        elif self.moving=="right":
            x+=1
        elif self.moving=="left":
            x-=1
        if self.mapgrid.out_of_bounds(x,y):
            return True
        if not(self.mapgrid.grid[x][y]):
            return False
        return True
    def update(self,dt):
        if self.moving:
            self.moved+=dt
            if self.moved>=.4:
                self.finish_move()
            else:
                self.set_position()
            self.render()
        if not(self.moving):
            oldfacing = self.facing
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
            if not(self.is_valid_move()):
                self.moving = False
            if self.moving or not(oldfacing==self.facing):
                self.render()
            

class MapGrid(spyral.Scene):
    def __init__(self,pet):
        spyral.Scene.__init__(self)
        self.pet = pet
        self.camera = self.parent_camera.make_child(virtual_size = (TM_WIDTH,TM_HEIGHT))
        self.group = spyral.Group(self.camera)
        self.up = False
        self.left = False
        self.right = False
        self.down = False
        self.walking_pet = WalkingPet(self,11,17,0,0)
        self.grid = [[True for y in range(18)] for x in range(24)]
    def out_of_bounds(self,x,y):
        return x<0 or x>=24 or y<0 or y>=18
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
        if self.out_of_bounds(self.walking_pet.grid_x,self.walking_pet.grid_y):
            spyral.director.pop()

class Room(MapGrid):
    def __init__(self,pet,shape):
        MapGrid.__init__(self,pet)
        self.shape = shape
        for y in range(6):
            for x in range(24):
                self.grid[x][y] = False
        for x in range(7):
            for y in range(18):
                self.grid[x][y] = False
                self.grid[23-x][y] = False
        for x in range(3):
            for y in range(3):
                self.grid[x+7][17-y] = False
                self.grid[16-x][17-y] = False
    def on_enter(self):
        bg = spyral.Image(filename = "images/town/the_room.png")
        self.camera.set_background(bg)
        

class Lobby(MapGrid):
    def __init__(self,pet,number,shapes):
        MapGrid.__init__(self,pet)
        self.number = number
        self.shapes = shapes
        for y in range(8):
            for x in range(24):
                self.grid[x][y] = False
        for y in range(10):
            self.grid[0][17-y] = False
            self.grid[23][17-y] = False
        for i in range(4):
            self.grid[2*i+1][13] = False
            self.grid[2*i+1][14] = False
            self.grid[22-2*i][13] = False
            self.grid[22-2*i][14] = False
            self.grid[3*i+1][8] = False
            self.grid[22-3*i][8] = False
        for x in range(10):
            for y in range(3):
                self.grid[x][17-y] = False
                self.grid[23-x][17-y] = False
        for i in range(7):
            self.grid[3*i+2][8] = shapes[i]
            self.grid[3*i+3][8] = shapes[i]
    def on_enter(self):
        bg = spyral.Image(filename="images/town/Lobby.png")
        self.camera.set_background(bg)
    def update(self,dt):
        MapGrid.update(self,dt)
        x = self.walking_pet.grid_x
        y = self.walking_pet.grid_y
        if self.out_of_bounds(x,y):
            return
        if not(self.walking_pet.changed_room):
            if not(isinstance(self.grid[x][y],bool)):
                spyral.director.push(Room(self.grid[x][y]))
                self.walking_pet.changed_room = True
                self.walking_pet.facing = "down"
                self.up = False
                self.down = False
                self.right = False
                self.left = False
                self.walking_pet.render()
                return
                

class Town(MapGrid):
    def __init__(self,pet):
        MapGrid.__init__(self,pet)
        for x in range(4):
            for y in range(7):
                self.grid[x][y] = False
    def add_building(self,data,x,y):
        self.grid[x-1][y-1] = False
        self.grid[x][y-1] = False
        self.grid[x+1][y-1] = False
        self.grid[x-1][y] = False
        self.grid[x+1][y] = False
        self.grid[x][y] = data
    def update(self,dt):
        MapGrid.update(self,dt)
        x = self.walking_pet.grid_x
        y = self.walking_pet.grid_y
        if self.out_of_bounds(x,y):
            return
        if not(self.walking_pet.changed_room):
            if not(isinstance(self.grid[x][y],bool)):
                spyral.director.push(Lobby(self.grid[x][y][0],self.grid[x][y][1]))
                self.walking_pet.changed_room = True
                self.walking_pet.facing = "down"
                self.up = False
                self.down = False
                self.right = False
                self.left = False
                self.walking_pet.render()
                return

class HongKong(Town):
    def __init__(self,pet):
        Town.__init__(self,pet)
        for x in range(4):
            for y in range(3):
                self.grid[x+9][y] = False
        for x in range(11):
            for y in range(5):
                self.grid[23-x][y] = False
        for x in range(5):
            for y in range(2):
                self.grid[23-x][y+5] = False
        self.grid[18][5] = False
        for x in range(2):
            self.grid[23-x][7] = False
            self.grid[20][x+5] = True
        self.grid[23][8] = False
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          6,2)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          10,2)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          6,5)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          10,5)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          14,4)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          14,7)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          20,4)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          2,9)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          6,9)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          10,9)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          19,9)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          14,10)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          5,13)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          9,13)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          13,13)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          18,12)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          17,15)
        self.add_building([20,["Square","Circle","Triangle","Triangle2","Triangle3","Triangle4","Diamond"]],
                          8,16)
        for i in range(5):
            for i2 in range(i+1):
                self.grid[23-i2][i+13] = False
                self.grid[i2][i+13] = False

        self.grid[2][15] = True
        self.grid[3][16] = True
        
    def on_enter(self):
        bg = spyral.Image(filename="images/town/hong_kong.png")
        for y in range(18):
            for x in range(24):
                if not(isinstance(self.grid[x][y],bool)):
                    surf = NUMBER_FONT.render(self.grid[x][y][0].__str__(),True,[255,255,0,255])
                    bg._surf.blit(surf,[x*50+25-surf.get_width()/2,y*50+25-surf.get_height()/2])
        self.camera.set_background(bg)

class Touheyville(Town):
    def __init__(self,pet):
        Town.__init__(self,pet)
    def add_tall_building(self,data,x,y):
        Town.add_building(self,data,x,y)
        self.grid[x-1][y-3] = False
        self.grid[x][y-3] = False
        self.grid[x+1][y-3] = False
        self.grid[x-1][y-2] = False
        self.grid[x+1][y-2] = False
        self.grid[x][y-2] = False
    def on_enter(self):
        bg = spyral.Image(filename="images/town/Touheyville.png")
        self.camera.set_background(bg)
