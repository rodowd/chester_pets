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

CITY_POSNS = {"Hong Kong": (100, 100),
              "Touheyville": (400, 400),
              "O'Dowd Shire": (500, 500)}
COLORS = {"background": (240, 219, 81),
          "basketball": (255, 174, 0),
          "hoop": (33, 3, 3),
          "point": (0, 0, 0),
          "labels": (0, 0, 0),
          "inputs": (0, 0, 0),
          "axes": (232, 189, 46),
          "highlighted_fill": (255, 255, 153),
          "not_highlighted_fill": (153, 153, 153),
          "shot_location": (253, 53, 53),
          "shoot_fill": (192, 159, 46)}
font = pygame.font.Font(None, FONT_SIZE)


class Ball(spyral.Sprite):
    '''
    The basketball that shows user where they are on the map
    '''
    def __init__(self, scene):
        super(Ball, self).__init__()
        self.scene = scene

        self.image = spyral.Image(filename="basketball_images/basketball.png")
        
        self.anchor = "center"


class Pet(spyral.Sprite):
    def __init__(self, scene):
        super(Pet, self).__init__()
        self.scene = scene

        self.image = spyral.Image(filename="basketball_images/Tan_Side_Cat.png") # @TODO: make this dynamic
        
        self.anchor = "center"
        self.x = 1100 # @TODO: magic
        self.y = 700 # @TODO: magic


class Scoreboard(spyral.Sprite):
    def __init__(self, scene):
        super(Scoreboard, self).__init__()
        self.scene = scene

        self.curr_x_input = ""
        self.curr_y_input = ""

        self.score_posn = (1000, 100) # @TODO: magic

        self.inputs_text_posn = (1000, self.score_posn[1] + FONT_SIZE) # @TODO: magic

        self.x_input_posn = (self.inputs_text_posn[0] + 10, self.score_posn[1] + FONT_SIZE) # TODO: magic
        self.y_input_posn = (self.inputs_text_posn[0] + 68, self.score_posn[1] + FONT_SIZE) # TODO: magic

        self.submit_text_posn = (1000, self.y_input_posn[1] + FONT_SIZE) # @TODO: magic
        self.submit_input_posn = (1000 + 15, self.y_input_posn[1] + FONT_SIZE) # @TODO: magic

        self.input_rect_size = (45, 30) # @TODO: magic
        self.submit_rect_size = (95, 30) # @TODO: magic

        self.x_input_rect = spyral.Rect(self.x_input_posn, self.input_rect_size)
        self.y_input_rect = spyral.Rect(self.y_input_posn, self.input_rect_size)
        self.submit_input_rect = spyral.Rect(self.submit_input_posn, self.submit_rect_size)

        # score
        temp_surface = font.render("Score: %x/%x" % (self.scene.score, self.scene.num_shots), True, COLORS["labels"])
        self.image._surf.blit(temp_surface, self.score_posn)

        # parens
        temp_surface = font.render("(       ,       )", True, COLORS["inputs"])
        self.image._surf.blit(temp_surface, self.inputs_text_posn)

        # x input
        temp_surface = font.render("   %s" % self.scene.x_input, True, COLORS["inputs"])
        self.image._surf.blit(temp_surface, self.inputs_text_posn)

        # y input
        temp_surface = font.render("           %s" % self.scene.y_input, True, COLORS["inputs"])
        self.image._surf.blit(temp_surface, self.inputs_text_posn)

        # submit input
        temp_surface = font.render("   Shoot!", True, COLORS["inputs"])
        self.image._surf.blit(temp_surface, self.submit_text_posn)


    def update(self, dt):
        if (self.curr_score != self.scene.score or
                                    self.curr_shots != self.scene.num_shots):
            self.curr_score = self.scene.score
            self.curr_shots = self.scene.num_shots
            self.redraw_all_pieces()
            return

        if (self.curr_x_input != self.scene.x_input or
                                    self.curr_y_input != self.scene.y_input):
            self.curr_x_input = self.scene.x_input
            self.curr_y_input = self.scene.y_input
            self.redraw_all_pieces()
            return


    def get_input(self, posn):
        print posn[0], posn[1]
        if self.x_input_rect.collide_point(posn):
            # user clicked inside of x input box
            self.highlighted_coord = "x"
            self.scene.x_input = ""
            self.redraw_all_pieces() # in case highlighting has changed
        if self.y_input_rect.collide_point(posn):
            # user clicked inside of y input box
            self.highlighted_coord = "y"
            self.scene.y_input = ""
            self.redraw_all_pieces() # in case highlighting has changed
        if self.submit_input_rect.collide_point(posn):
            if self.scene.x_input == "" or self.scene.y_input == "":
                return
            self.scene.waiting_for_input = False


class WorldMap(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(WorldMap, self).__init__(*args, **kwargs)
        
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        
        self.posn_marker_ball = Ball(self)
        self.posn_marker_ball.pos = CITY_POSNS.values()[0]

        # We have to give our camera to the group so it knows where to draw
        self.group = spyral.Group(self.camera)
        # We can add the sprites to the group
        self.scoreboard = Scoreboard(self)
        self.group.add(self.scoreboard)

        self.pet = Pet(self)
        self.group.add(self.pet)


    def on_enter(self):
        background = spyral.Image(filename="world_images/world.png")#
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
                if event['key'] == 27:
                    spyral.director.pop()
                    return
                elif event['key'] == 77:
                    print "left"
                    self.posn_marker_ball.pos = CITY_POSNS.values()[1]
                elif event['key'] == 78:
                    print "right"
                elif event['key'] == 79:
                    print "up"
                elif event['key'] == 80:
                    print "down"
                elif event['key'] == "\r":
                    print "enter"
                    # @TODO: go to racing game
