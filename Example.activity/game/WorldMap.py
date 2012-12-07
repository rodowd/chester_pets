#!/usr/bin/python
'''
Ryan O'Dowd
12/01/2012
CISC 374
'''

__doc__ = ''' The central hub for getting to all of the towns '''

import spyral
import pygame
import Racing
import Basketball # @TODO: for debug; delete
import CrosswordPuzzle # @TODO: for debug; delete
import Cooking # @TODO: for debug; delete
import TownMap

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

class CityName(spyral.Sprite):
    def __init__(self, scene):
        super(CityName, self).__init__()
        self.scene = scene

        self.name_posn = (500, 50)

        self.draw_city_name()

        self.curr_city = self.scene.curr_city


    def draw_city_name(self):
        self.image = spyral.Image(size=(WIDTH, HEIGHT))

        temp_surface = font.render(CITY_POSNS[self.scene.curr_city % 3][0], True, COLORS["city_name"])
        self.image._surf.blit(temp_surface, self.name_posn)


    def update(self, dt):
        if self.curr_city != self.scene.curr_city:
            # only repaint if name changes
            self.draw_city_name()
            self.curr_city = self.scene.curr_city


class WorldMap(spyral.Scene):
    def __init__(self, passed_in_pet, *args, **kwargs):
        super(WorldMap, self).__init__(*args, **kwargs)
        
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        
        # We have to give our camera to the group so it knows where to draw
        self.group = spyral.Group(self.camera)
        # We can add the sprites to the group

        self.curr_city = 0

        self.city_name = CityName(self)
        self.group.add(self.city_name)

        self.pet = passed_in_pet
        self.pet.pos = CITY_POSNS[self.curr_city][1]
        self.group.add(self.pet)
        self.reset_pos = False


    def on_enter(self):
        background = spyral.Image(filename="images/world/world.png")
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
        if self.reset_pos:
            self.pet.pos = self.reset_pos
            self.reset_pos = False
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                # pop once for WorldMap
                spyral.director.pop()
                # pop twice for PetSelection (couldn't pop before because it
                # was the only thing on the stack)
                spyral.director.pop()
                return
            if event['type'] == 'KEYDOWN':
                if event['key'] == 276 or event['key'] == 274:
                    # left arrow
                    self.curr_city -= 1
                    self.pet.pos = CITY_POSNS[self.curr_city % 3][1]
                elif event['key'] == 275 or event['key'] == 273:
                    # right arrow
                    self.curr_city += 1
                    self.pet.pos = CITY_POSNS[self.curr_city % 3][1]
                elif event['key'] == 13:
                    # enter key
                    new_dest = CITY_POSNS[self.curr_city % 3][0]
                    if self.pet.destination == new_dest:
                        self.reset_pos = self.pet.pos
                        if new_dest == "Touheyville":
                            self.pet.previous_posns.append(self.pet.pos)
                            spyral.director.push(TownMap.Touheyville(self.pet))
                        elif new_dest == "Hong Kong":
                            self.pet.previous_posns.append(self.pet.pos)
                            spyral.director.push(TownMap.HongKong(self.pet))
                        else:
                            self.pet.previous_posns.append(self.pet.pos)
                            spyral.director.push(TownMap.ODowdShire(self.pet))
                        return
                    self.pet.destination = new_dest
                    self.reset_pos = self.pet.pos
                    spyral.director.push(Racing.RacingMain(self.pet))
                # @TODO: rest is for debug; delete
                elif event['ascii'] == 'q':
                    self.pet.previous_posns.append(self.pet.pos)
                    spyral.director.push(CrosswordPuzzle.CrosswordMain(self.pet))
                elif event['ascii'] == 'w':
                    self.pet.previous_posns.append(self.pet.pos)
                    spyral.director.push(Basketball.Basketball(self.pet))
                elif event['ascii'] == 'e':
                    self.pet.previous_posns.append(self.pet.pos)
                    spyral.director.push(Cooking.Cooking(self.pet))
