import spyral
import pygame
import Basketball
import CrosswordPuzzle
import Cooking
import random
import PetSelection
import EndingScreen

TM_WIDTH = 1200
TM_HEIGHT = 900
NUMBER_FONT = pygame.font.SysFont(None,30)
CLUE_FONT = pygame.font.SysFont(None,30)
MOVE_DELAY = .3

class WalkingPet(spyral.Sprite):
    def __init__(self,mapgrid,x,y,pivot_x,pivot_y):
        spyral.Sprite.__init__(self,mapgrid.group)
        self.group.add(self)
        self.hat = mapgrid.pet.hat
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
        self.active = True
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
        hat = False
        if self.mapgrid.pet.hat:
            hat = spyral.Image(filename = self.get_hat())
        for i in range(4):
            if hat:
                self.images[i*2]._surf.blit(hat._surf,[0,0])
                self.images[i*2+1]._surf.blit(hat._surf,[0,0])
            self.images[i*2].rotate(i*90)
            self.images[i*2+1].rotate(i*90)
    def get_hat(self):
        pets = ["cat","dog","bird","dragon"]
        pet = self.mapgrid.pet
        return "images/pets/accessories/hats/"+pet.hat+"_"+pets[pet.pet_type]+"_move.png"
    def get_move1(self):
        moves = ["cat_move1_",
                 "dog_move1_",
                 "bird_move1_",
                 "dragon_move1_"]
        colors = ["tan",
                  "red",
                  "blue",
                  "green",
                  "magenta",
                  "cyan",
                  "yellow"]
        return "images/pets/"+moves[self.mapgrid.pet.pet_type]+colors[self.mapgrid.pet.color]+".png"
    def get_move2(self):
        moves = ["cat_move2_",
                 "dog_move2_",
                 "bird_move2_",
                 "dragon_move2_"]
        colors = ["tan",
                  "red",
                  "blue",
                  "green",
                  "magenta",
                  "cyan",
                  "yellow"]
        return "images/pets/"+moves[self.mapgrid.pet.pet_type]+colors[self.mapgrid.pet.color]+".png"
    def render(self):
        i = 6
        if self.facing == "up":
            i = 0
        if self.facing == "left":
            i = 2
        if self.facing == "down":
            i = 4
        if self.moved<=MOVE_DELAY/2 and self.moved>0:
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
        self.x = self.grid_x*50+x*50*self.moved/MOVE_DELAY-self.pivot_x
        self.y = self.grid_y*50+y*50*self.moved/MOVE_DELAY-self.pivot_y
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
        if not(self.hat == self.mapgrid.pet.hat):
            self.hat = self.mapgrid.pet.hat
            self.set_moving_images()
            self.render()
        if not(self.active):
            return
        if self.moving:
            self.moved+=dt
            if self.moved>=MOVE_DELAY:
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
    def __init__(self, passed_in_pet):
        spyral.Scene.__init__(self)
        self.pet = passed_in_pet
        self.camera = self.parent_camera.make_child(virtual_size = (TM_WIDTH,TM_HEIGHT))
        self.group = spyral.Group(self.camera)
        self.up = False
        self.left = False
        self.right = False
        self.down = False
        self.walking_pet = WalkingPet(self,11,17,0,0)
        self.grid = [[True for y in range(18)] for x in range(24)]
        self.clue = ClueSprite(self.group,self.pet)
        self.pet = passed_in_pet


    def out_of_bounds(self,x,y):
        return x<0 or x>=24 or y<0 or y>=18


    def render(self):
        self.group.draw()


    def update(self,dt):
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                return
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
            self.pet.get_last_posn()

class ClueSprite(spyral.Sprite):
    def __init__(self, group, passed_in_pet):
        spyral.Sprite.__init__(self, group)
        self.group.add(self)
        self.pet = passed_in_pet
        self.clue = self.pet.get_clue()
        self.anchor = 'topleft'
        self.pos = [0,0]
        self.render()
    def render(self):
        self.image = spyral.Image(size=[200,350])
        surf = CLUE_FONT.render(self.clue.town,True,[255,255,0,255])
        self.image._surf.blit(surf,[100-surf.get_width()/2,80])
        surf = CLUE_FONT.render(self.clue.number_clue,True,[255,255,0,255])
        self.image._surf.blit(surf,[100-surf.get_width()/2,150])
        for i in range(len(self.clue.shape_clue)):
            shape = self.clue.shape_clue[i]
            image = self.get_shape_image(shape)
            self.image._surf.blit(image._surf,[25*i+25,230])
    def get_shape_image(self,shape):
        if shape=="Circle":
            return spyral.Image(filename = "images/town/circle.png")
        if shape=="Square":
            return spyral.Image(filename = "images/town/square.png")
        if shape=="Diamond":
            return spyral.Image(filename = "images/town/diamond.png")
        if shape=="Triangle1":
            return spyral.Image(filename = "images/town/triangle_up.png")
        if shape=="Triangle2":
            return spyral.Image(filename = "images/town/triangle_right.png")
        if shape=="Triangle3":
            return spyral.Image(filename = "images/town/triangle_left.png")
        if shape=="Triangle4":
            return spyral.Image(filename = "images/town/triangle_down.png")
        image = spyral.Image(size = [20,20])
        image.draw_rect([255,255,0,255],[0,19],[20,2])
        return image
    def update(self,dt):
        if not(self.clue==self.pet.get_clue()):
            self.clue = self.pet.get_clue()
            self.render()
        
        
class Room(MapGrid):
    def __init__(self, passed_in_pet, shape, number):
        MapGrid.__init__(self, passed_in_pet)
        self.shape = shape
        self.number = number
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
        self.grid[11][6] = "Chest"
        self.grid[11][7] = "Chest"
        self.grid[12][6] = "Chest"
        self.grid[12][7] = "Chest"
    def on_enter(self):
        bg = 0
        if self.number==self.pet.get_clue().number and self.shape==self.pet.get_clue().shape:
            bg = spyral.Image(filename = "images/town/the_room.png")
        else:
            bg = spyral.Image(filename = "images/town/empty_room.png")
        self.camera.set_background(bg)
    def update(self,dt):
        MapGrid.update(self,dt)
        x = self.walking_pet.grid_x
        y = self.walking_pet.grid_y
        if self.out_of_bounds(x,y):
            return
        if not(self.walking_pet.changed_room):
            if not(isinstance(self.grid[x][y],bool)):
                if not(self.number==self.pet.get_clue().number and
                       self.shape==self.pet.get_clue().shape):
                    return
                if self.pet.get_game()=="Basketball":
                    spyral.director.push(Basketball.Basketball(self.pet))
                elif self.pet.get_game()=="Crossword":
                    spyral.director.push(CrosswordPuzzle.CrosswordMain(self.pet))
                elif self.pet.get_game()=="Cooking":
                    spyral.director.push(Cooking.Cooking(self.pet))
                else:
                    self.walking_pet.active = False
                    spyral.director.replace(EndingScreen.EndingScreen(self.walking_pet))
                    return

                self.walking_pet.changed_room = True
                self.walking_pet.facing = "down"
                self.up = False
                self.down = False
                self.right = False
                self.left = False
                self.walking_pet.render()
                return
        

class Lobby(MapGrid):
    def __init__(self, passed_in_pet, number, shapes):
        MapGrid.__init__(self, passed_in_pet)
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
        bg = spyral.Image(filename="images/town/lobby_hong_kong.png")
        self.camera.set_background(bg)
    def update(self,dt):
        MapGrid.update(self,dt)
        x = self.walking_pet.grid_x
        y = self.walking_pet.grid_y
        if self.out_of_bounds(x,y):
            return
        if not(self.walking_pet.changed_room):
            if not(isinstance(self.grid[x][y],bool)):
                spyral.director.push(Room(self.pet,self.grid[x][y],self.number))
                self.walking_pet.changed_room = True
                self.walking_pet.facing = "down"
                self.up = False
                self.down = False
                self.right = False
                self.left = False
                self.walking_pet.render()
                return


class Store(MapGrid):
    def __init__(self,passed_in_pet):
        MapGrid.__init__(self,passed_in_pet)
        for x in range(7):
            for y in range(17):
                self.grid[x][y] = False
                self.grid[23-x][y] = False
        for y in range(9):
            for x in range(10):
                self.grid[x+7][y] = False
        for x in range(3):
            for y in range(3):
                self.grid[x+7][17-y] = False
                self.grid[16-x][17-y] = False
        self.grid[9][8] = "Hat"
        self.grid[10][8] = "Hat"
        self.grid[13][8] = "Motor"
        self.grid[14][8] = "Motor"
    def update(self,dt):
        MapGrid.update(self,dt)
        x = self.walking_pet.grid_x
        y = self.walking_pet.grid_y
        if self.out_of_bounds(x,y):
            return
        if not(self.walking_pet.changed_room):
            if not(isinstance(self.grid[x][y],bool)):
                if self.grid[x][y]=="Hat":
                    spyral.director.push(HatShop(self.pet))
                else:
                    spyral.director.push(MotorShop(self.pet))
                self.walking_pet.changed_room = True
                self.walking_pet.facing = "down"
                self.up = False
                self.down = False
                self.right = False
                self.left = False
                self.walking_pet.render()
                return
    def on_enter(self):
        bg = spyral.Image(filename="images/town/store.png")
        self.camera.set_background(bg)    

class MoneySprite(spyral.Sprite):
    def __init__(self,group,pet):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.pet = pet
        self.money = pet.money
        self.pos = [10,10]
        self.render()
    def render(self):
        self.image = spyral.Image(size = [600,300])
        string = "Chester Points: "+self.money.__str__()
        font = pygame.font.SysFont(None,60)
        surf = font.render(string,True,[0,0,0,255])
        font = pygame.font.SysFont(None,30)
        self.image._surf.blit(surf,[25,50-surf.get_height()/2])
        surf = font.render("Arrow Keys: Cycle through items.",True,[0,0,0,255])
        self.image._surf.blit(surf,[25,100-surf.get_height()/2])
        surf = font.render("Enter Key: Purchase/equip item.",True,[0,0,0,255])
        self.image._surf.blit(surf,[25,150-surf.get_height()/2])
        surf = font.render("Escape Key: Leave shop.",True,[0,0,0,255])
        self.image._surf.blit(surf,[25,200-surf.get_height()/2])
    def update(self,dt):
        if not(self.money == self.pet.money):
            self.money = self.pet.money
            self.render()

class Shop(spyral.Scene):
    def __init__(self,passed_in_pet):
        spyral.Scene.__init__(self)
        self.pet = passed_in_pet
        self.camera = self.parent_camera.make_child(virtual_size = (TM_WIDTH,TM_HEIGHT))
        self.group = spyral.Group(self.camera)
        MoneySprite(self.group,self.pet)
    def render(self):
        self.group.draw()
    def on_enter(self):
        bg = spyral.Image(size = [TM_WIDTH,TM_HEIGHT])
        bg.fill([192,192,0,255])
        self.camera.set_background(bg)
    def cycleLeft(self):
        pass
    def cycleRight(self):
        pass
    def pressEnter(self):
        pass
    def leaveShop(self):
        pass
    def update(self,dt):
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'KEYDOWN':
                if event['key'] == 275:
                    self.cycleRight()
                if event['key'] == 276:
                    self.cycleLeft()
                if event['key'] == 13:
                    self.pressEnter()
                if event['key'] == 27:
                    self.leaveShop()

class PriceSprite(spyral.Sprite):
    def __init__(self,group,cost):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.pos = [TM_WIDTH/2,TM_HEIGHT-100]
        self.anchor = 'center'
        self.cost = cost
        self.render()
    def render(self):
        self.image = spyral.Image(size=[500,100])
        string = "Cost: "+self.cost.__str__()
        if self.cost == "Wearing" or self.cost == "Using" or self.cost == "Already Owned":
            string = self.cost
        font = pygame.font.SysFont(None,50)
        surf = font.render(string,True,[0,0,0,255])
        self.image._surf.blit(surf,[250-surf.get_width()/2,50-surf.get_height()/2])
    def change_cost(self,cost):
        self.cost = cost
        self.render()

class MotorShop(Shop):
    def __init__(self,passed_in_pet):
        Shop.__init__(self,passed_in_pet)
        self.old_vehicle = self.pet.vehicle
        self.vehicles = [PetSelection.Vehicle("car",[200,50,300,300]),
                         PetSelection.Vehicle("motorcycle_blue",[230,40,360,260]),
                         PetSelection.Vehicle("motorcycle_dark",[230,40,360,260]),
                         PetSelection.Vehicle("motorcycle_green",[230,40,360,260]),
                         PetSelection.Vehicle("motorcycle_pink",[230,40,360,260]),
                         PetSelection.Vehicle("motorcycle_red",[230,40,360,260]),
                         PetSelection.Vehicle("motorcycle_yellow",[230,40,360,260]),
                         PetSelection.Vehicle("sport_blue",[210,60,220,280]),
                         PetSelection.Vehicle("sport_dark",[210,60,220,280]),
                         PetSelection.Vehicle("sport_green",[210,60,220,280]),
                         PetSelection.Vehicle("shoe",[180,60,360,360])]
        self.cost = [random.randint(150,450) for x in self.vehicles]
        self.car_index = 0
        self.costsprite = PriceSprite(self.group,self.cost[0])
        self.update_vehicle()
    def update_vehicle(self):
        self.group.remove(self.pet.vehicle)
        self.pet.vehicle = self.vehicles[self.car_index]
        self.group.add(self.pet.vehicle)
        if self.pet.vehicle.name == self.old_vehicle.name:
            self.costsprite.change_cost("Using")
            return
        for string in self.pet.vehicles:
            if string==self.pet.vehicle.name:
                self.costsprite.change_cost("Already Owned")
                return
        self.costsprite.change_cost(self.cost[self.car_index])
    def cycleLeft(self):
        self.car_index = (self.car_index-1)%len(self.vehicles)
        self.update_vehicle()
    def cycleRight(self):
        self.car_index = (self.car_index+1)%len(self.vehicles)
        self.update_vehicle()
    def pressEnter(self):
        if self.old_vehicle == self.pet.vehicle:
            return
        for string in self.pet.vehicles:
            if string == self.pet.vehicle.name:
                print string,"poop"
                self.old_vehicle = self.pet.vehicle
                self.update_vehicle()
                return
        if self.pet.money >= self.cost[self.car_index]:
            self.pet.money -= self.cost[self.car_index]
            self.old_vehicle = self.pet.vehicle
            self.pet.vehicles.append(self.pet.vehicle.name)
            self.update_vehicle()
    def on_enter(self):
        bg = spyral.Image(filename = "images/town/motorshop.png")
        self.camera.set_background(bg)
    def leaveShop(self):
        self.pet.vehicle = self.old_vehicle
        spyral.director.pop()
        
                 
class HatShop(Shop):
    def __init__(self,passed_in_pet):
        Shop.__init__(self,passed_in_pet)
        self.group.add(self.pet)
        self.pet.pos = [TM_WIDTH/2,TM_HEIGHT/2]
        self.oldHat = self.pet.hat
        self.hats = [False,"cap_red","cap_green","cap_magenta","cap_tan","cap_cyan","cap_yellow","cap_blue","cap_black","cap_white","top","rice_white","rice_black","santa"]
        self.cost = [random.randint(50,150) for x in self.hats]
        self.cost[0] = 0
        self.hat_index = 1
        self.costsprite = PriceSprite(self.group,self.cost[1])
        self.update_hat()
    def update_hat(self):
        self.pet.hat = self.hats[self.hat_index]
        self.pet.set_pet_image("big")
        if self.pet.hat == self.oldHat:
            self.costsprite.change_cost("Wearing")
            return
        for string in self.pet.hats:
            if string==self.pet.hat:
                self.costsprite.change_cost("Already Owned")
                return
        self.costsprite.change_cost(self.cost[self.hat_index])
    def cycleLeft(self):
        self.hat_index = (self.hat_index-1)%len(self.hats)
        self.update_hat()
    def cycleRight(self):
        self.hat_index = (self.hat_index+1)%len(self.hats)
        self.update_hat()
    def pressEnter(self):
        if self.oldHat == self.pet.hat:
            return
        for string in self.pet.hats:
            if string == self.pet.hat:
                self.oldHat = self.pet.hat
                self.update_hat()
                return
        if self.pet.money >= self.cost[self.hat_index]:
            self.pet.money -= self.cost[self.hat_index]
            self.oldHat = self.pet.hat
            self.pet.hats.append(self.oldHat)
            self.update_hat()
    def on_enter(self):
        bg = spyral.Image(filename = "images/town/hat_shop.png")
        self.camera.set_background(bg)
    def leaveShop(self):
        self.pet.hat = self.oldHat
        self.pet.set_pet_image("big")
        spyral.director.pop()
        
    
        

class Town(MapGrid):
    def __init__(self, passed_in_pet):
        MapGrid.__init__(self, passed_in_pet)
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
                next_room = self.grid[x][y]
                if next_room == "$":
                    spyral.director.push(Store(self.pet))
                else:
                    spyral.director.push(Lobby(self.pet,next_room[0],next_room[1]))
                self.walking_pet.changed_room = True
                self.walking_pet.facing = "down"
                self.up = False
                self.down = False
                self.right = False
                self.left = False
                self.walking_pet.render()
                return
    def paint_numbers(self,bg):
        for y in range(18):
            for x in range(24):
                if not(isinstance(self.grid[x][y],bool)):
                    string = ""
                    if self.grid[x][y]=="$":
                        string = "$"
                    else:
                        string = self.grid[x][y][0].__str__()
                    surf = NUMBER_FONT.render(string,True,[255,255,0,255])
                    bg._surf.blit(surf,[x*50+25-surf.get_width()/2,y*50+25-surf.get_height()/2])

class HongKong(Town):
    def __init__(self, passed_in_pet):
        Town.__init__(self, passed_in_pet)
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
        standard_shapes = ["Square","Circle","Triangle1","Triangle2","Triangle3","Triangle4","Diamond"]
        self.add_building([62,standard_shapes],6,2)
        self.add_building([66,standard_shapes],10,2)
        self.add_building([63,standard_shapes],6,5)
        self.add_building([67,standard_shapes],10,5)
        self.add_building([71,standard_shapes],14,4)
        self.add_building([72,standard_shapes],14,7)
        self.add_building([75,standard_shapes],20,4)
        self.add_building([61,standard_shapes],2,9)
        self.add_building([64,standard_shapes],6,9)
        self.add_building([68,standard_shapes],10,9)
        self.add_building([76,standard_shapes],19,9)
        self.add_building([73,standard_shapes],14,10)
        self.add_building([65,standard_shapes],5,13)
        self.add_building([69,standard_shapes],9,13)
        self.add_building([74,standard_shapes],13,13)
        self.add_building([77,standard_shapes],18,12)
        self.add_building("$",17,15)
        self.add_building([70,standard_shapes],8,16)
        for i in range(5):
            for i2 in range(i+1):
                self.grid[23-i2][i+13] = False
                self.grid[i2][i+13] = False

        self.grid[2][15] = True
        self.grid[3][16] = True
        
    def on_enter(self):
        bg = spyral.Image(filename="images/town/hong_kong.png")
        self.paint_numbers(bg)
        self.camera.set_background(bg)

class Touheyville(Town):
    def __init__(self, passed_in_pet):
        Town.__init__(self, passed_in_pet)
        standard_shapes = ["Square","Circle","Triangle1","Triangle2","Triangle3","Triangle4","Diamond"]
        self.add_building([21,standard_shapes],2,8)
        self.add_building([22,standard_shapes],4,11)
        self.add_building([23,standard_shapes],4,14)
        self.add_building([24,standard_shapes],8,3)
        self.add_skyscraper([25,standard_shapes],8,8)
        self.add_building([26,standard_shapes],8,11)
        self.add_building([27,standard_shapes],8,14)
        self.add_building([28,standard_shapes],12,5)
        self.add_building([29,standard_shapes],12,8)
        self.add_building([30,standard_shapes],12,11)
        self.add_skyscraper([31,standard_shapes],12,16)
        self.add_building([32,standard_shapes],16,4)
        self.add_building([33,standard_shapes],16,7)
        self.add_tall_building([34,standard_shapes],16,11)
        self.add_building([35,standard_shapes],16,16)
        self.add_building([36,standard_shapes],20,7)
        self.add_building([37,standard_shapes],20,11)
        self.add_building("$",20,14)
        for y in range(6):
            self.grid[0][17-y] = False
        self.grid[1][15] = False
        for x in range(4):
            for y in range(2):
                self.grid[x+1][17-y] = False
        for x in range(2):
            self.grid[x+5][17] = False
        for x in range(20):
            self.grid[23-x][0] = False
        for x in range(9):
            self.grid[23-x][1] = False
        for y in range(3):
            for x in range(5-y):
                self.grid[23-x][y+2] = False
        self.grid[23][5] = False
        for x in range(2):
            self.grid[x+4][1] = False
    def add_skyscraper(self,data,x,y):
        self.add_tall_building(data,x,y)
        self.grid[x-1][y-3] = False
        self.grid[x][y-3] = False
        self.grid[x+1][y-3] = False
    def add_tall_building(self,data,x,y):
        Town.add_building(self,data,x,y)
        self.grid[x-1][y-2] = False
        self.grid[x+1][y-2] = False
        self.grid[x][y-2] = False
    def on_enter(self):
        bg = spyral.Image(filename="images/town/touheyville.png")
        self.paint_numbers(bg)
        self.camera.set_background(bg)

class ODowdShire(Town):
    def __init__(self, passed_in_pet):
        Town.__init__(self, passed_in_pet)
        standard_shapes = ["Square","Circle","Triangle1","Triangle2","Triangle3","Triangle4","Diamond"]
        self.add_tower([41,standard_shapes],9,3)
        self.add_tower([42,standard_shapes],13,2)
        self.add_building([43,standard_shapes],17,2)
        self.add_building([44,standard_shapes],21,3)
        self.add_tower([45,standard_shapes],6,6)
        self.add_building([46,standard_shapes],10,6)
        self.add_building([47,standard_shapes],14,5)
        self.add_tower([48,standard_shapes],18,6)
        self.add_tower([49,standard_shapes],22,7)
        self.add_building([50,standard_shapes],8,9)
        self.add_building([51,standard_shapes],21,10)
        self.add_tower([52,standard_shapes],2,14)
        self.add_tower([53,standard_shapes],6,14)
        self.add_tower([54,standard_shapes],14,12)
        self.add_tower([55,standard_shapes],10,16)
        self.add_tower([56,standard_shapes],15,16)
        self.add_building("$",19,16)
        for y in range(11):
            self.grid[0][17-y] = False
        for y in range(3):
            self.grid[1][10+y] = False
            self.grid[2][9+y] = False
            self.grid[12][9+y] = False
            self.grid[13][8+y] = False
            self.grid[14][7+y] = False
            self.grid[15][7+y] = False
            self.grid[16][8+y] = False
            self.grid[17][9+y] = False
            self.grid[18][10+y] = False
        self.grid[16][11] = False
        for y in range(2):
            self.grid[4][9+y] = False
            self.grid[5][10+y] = False
            self.grid[y+1][17] = False
            self.grid[6][11+y] = False
            self.grid[7][12+y] = False
            self.grid[8][11+y] = False
            self.grid[10][11+y] = False
            self.grid[11][10+y] = False
            self.grid[20][12+y] = False
            self.grid[21][12+y] = False
        for x in range(2):
            for y in range(6):
                self.grid[23-x][17-y] = False
        for y in range(3):
            for x in range(3-y):
                self.grid[x+4][y+1] = False
        for x in range(20):
            self.grid[23-x][0] = False
        for x in range(5):
            self.grid[23-x][1] = False
        for y in range(4):
            self.grid[23][y+2] = False
    def add_tower(self,data,x,y):
        Town.add_building(self,data,x,y)
        self.grid[x][y-2] = False
    def on_enter(self):
        bg = spyral.Image(filename="images/town/odowd_shire.png")
        self.paint_numbers(bg)
        self.camera.set_background(bg)
