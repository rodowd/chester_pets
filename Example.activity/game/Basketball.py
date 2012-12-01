#!/usr/bin/python
'''
Ryan O'Dowd
10/28/12
CISC 374
'''

__doc__ = ''' This basketball game teaches the concept of the coordinate
              system and specifically the first quadrant.  The user is
              presented with a coordinate system containing multiple hoops, one
              of which is lit up (the target).  The user then must enter the
              correct coordinates into the empty ordered pair in the
              scoreboard and click shoot.  The ball is then shot and goes
              through the hoop if the coordinates are correct.'''

import spyral
import pygame
import random
import time

WIDTH = 1200
HEIGHT = 900
COORD_WIDTH = WIDTH * .7
COORD_HEIGHT = HEIGHT * .8
PAD_LEFT = (WIDTH - COORD_WIDTH) * .3
PAD_RIGHT = WIDTH - COORD_WIDTH - PAD_LEFT
PAD_TOP = (HEIGHT - COORD_HEIGHT) * .3
PAD_BOTTOM = HEIGHT - COORD_HEIGHT - PAD_TOP
NUM_X_POINTS = 10.0
NUM_Y_POINTS = 8.0
SCOREBOARD_PERCENTAGE = .8
SCOREBOARD_HEIGHT = 200
FONT_SIZE = 37

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
    The basketballs that go up and down
    '''
    def __init__(self, scene, size_factor):
        '''
        # @TODO: 
        '''
        super(Ball, self).__init__()
        self.scene = scene

        self.ball_speed_up = -900
        self.ball_speed_fast = 500
        self.ball_speed_slow = 150
        self.ball_slow_range = 50

        self.hangtime = 80

        self.image = spyral.Image(filename="basketball_images/basketball.png")
        
        self.vel_y = 0;
        
        self.anchor = "center"


    def shoot_up(self, dt):
        self.vel_y = self.ball_speed_up


    def shoot_down(self, dt, x_coord):
        self.vel_y = self.ball_speed_fast
        self.x = ((x_coord / NUM_X_POINTS) * COORD_WIDTH) + PAD_LEFT


    def update(self, dt):
        self.y += dt * self.vel_y
        pass


class Hoop(spyral.Sprite):
    def __init__(self, scene, coord):
        super(Hoop, self).__init__()
        self.scene = scene

        self.is_target = False

        hoop_image = spyral.Image(filename="basketball_images/hoop.png")
        
        self.image = hoop_image

        self.x_coord = coord[0]
        self.y_coord = coord[1]

        self.anchor = "center"
        self.x = (self.x_coord / NUM_X_POINTS) * COORD_WIDTH + PAD_LEFT
        self.y = HEIGHT - ((self.y_coord / NUM_Y_POINTS) * COORD_HEIGHT) - PAD_BOTTOM


def get_hoops(scene):
    hoops = []
    hoop_posns = []
    num_hoops = 7

    for i in range(num_hoops):
        temp_coord = (random.choice(range(int(NUM_X_POINTS + 1))),
                        random.choice(range(int(NUM_Y_POINTS + 1))))
        while temp_coord in hoop_posns:
            temp_coord = (random.choice(range(int(NUM_X_POINTS + 1))),
                            random.choice(range(int(NUM_Y_POINTS + 1))))
        hoops.append(Hoop(scene, temp_coord))
        hoop_posns.append(temp_coord)

    target_hoop = random.choice(range(num_hoops))
    new_hoop_image = spyral.Image(filename="basketball_images/target_hoop.png")
    hoops[target_hoop].image = new_hoop_image
    hoops[target_hoop].is_target = True

    return hoops


class Pet(spyral.Sprite):
    def __init__(self, scene):
        super(Pet, self).__init__()
        self.scene = scene

        self.image = spyral.Image(filename="basketball_images/Tan_Side_Cat.png") # @TODO: make this dynamic
        
        self.anchor = "center"
        self.x = 1000 # @TODO: magic
        self.y = 700 # @TODO: magic


class Graph(spyral.Sprite):
    def __init__(self, scene):
        super(Graph, self).__init__()
        self.scene = scene

        self.image = spyral.Image(size=(WIDTH, HEIGHT))

        arrow_dim = 20
        axis_thickness = 5
        x_label_offset = 20
        y_label_offset = 20

        # x-axis
        x_axis_end_point_xposn = PAD_LEFT + COORD_WIDTH + 70 # @TODO: magic
        x_axis_end_point_yposn = PAD_TOP + COORD_HEIGHT
        pygame.draw.line(self.image._surf,
                         COLORS["axes"],
                         (x_axis_end_point_xposn, x_axis_end_point_yposn),
                         (0, PAD_TOP + COORD_HEIGHT),
                         axis_thickness)
        # axis arrow
        pygame.draw.line(self.image._surf,
                         COLORS["axes"],
                         (x_axis_end_point_xposn, x_axis_end_point_yposn),
                         (x_axis_end_point_xposn - arrow_dim, x_axis_end_point_yposn - arrow_dim),
                         axis_thickness)
        # axis arrow
        pygame.draw.line(self.image._surf,
                         COLORS["axes"],
                         (x_axis_end_point_xposn, x_axis_end_point_yposn),
                         (x_axis_end_point_xposn - arrow_dim, x_axis_end_point_yposn + arrow_dim),
                         axis_thickness)

        # y-axis
        y_axis_end_point_xposn = PAD_LEFT
        y_axis_end_point_yposn = PAD_TOP - 40
        pygame.draw.line(self.image._surf,
                         COLORS["axes"],
                         (y_axis_end_point_xposn, y_axis_end_point_yposn),
                         (PAD_LEFT, HEIGHT),
                         axis_thickness)
        # axis arrow
        pygame.draw.line(self.image._surf,
                         COLORS["axes"],
                         (y_axis_end_point_xposn, y_axis_end_point_yposn),
                         (y_axis_end_point_xposn - arrow_dim, y_axis_end_point_yposn + arrow_dim),
                         axis_thickness)
        # axis arrow
        pygame.draw.line(self.image._surf,
                         COLORS["axes"],
                         (y_axis_end_point_xposn, y_axis_end_point_yposn),
                         (y_axis_end_point_xposn + arrow_dim, y_axis_end_point_yposn + arrow_dim),
                         axis_thickness)
        
        # x-axis labels
        for i in range(int(NUM_X_POINTS)+1):
            x = ((i / NUM_X_POINTS) * COORD_WIDTH) + PAD_LEFT
            temp_surface = font.render(str(i), True, COLORS["labels"])
            self.image._surf.blit(temp_surface, (x, (PAD_TOP + COORD_HEIGHT +
                                                        y_label_offset)))
        # y-axis labels
        for i in range(int(NUM_Y_POINTS)+1):
            y = HEIGHT - ((i / NUM_Y_POINTS) * COORD_HEIGHT) - PAD_BOTTOM
            temp_surface = font.render(str(i), True, COLORS["labels"])
            self.image._surf.blit(temp_surface, (PAD_LEFT - x_label_offset, y))

        #self.image.draw_rect(COLORS["graph_outline"],
                                    #(PAD_LEFT, PAD_TOP),
                                    #(COORD_WIDTH, COORD_HEIGHT),
                                    #border_width=2)


class Point(spyral.Sprite):
    def __init__(self, scene, i, j):
        super(Point, self).__init__()
        self.scene = scene

        point_radius = 2

        self.image = spyral.Image(size=(point_radius*2, point_radius*2))
        self.image.draw_circle(COLORS["point"], (point_radius, point_radius), point_radius)

        self.anchor = "center"
        self.x = ((i / NUM_X_POINTS) * COORD_WIDTH) + PAD_LEFT
        self.y = HEIGHT - ((j / NUM_Y_POINTS) * COORD_HEIGHT) - PAD_BOTTOM


class ShotPoint(Point):
    def __init__(self, scene):
        super(Point, self).__init__()
        self.scene = scene

        self.point_radius = 6

        self.image = spyral.Image(size=(self.point_radius*2, self.point_radius*2))
        self.image.draw_circle(COLORS["shot_location"], (self.point_radius, self.point_radius), self.point_radius)

        self.anchor = "center"

    def update(self, dt):
        self.image = spyral.Image(size=(WIDTH, HEIGHT))
        self.image = spyral.Image(size=(self.point_radius*2, self.point_radius*2))
        self.image.draw_circle(COLORS["shot_location"], (self.point_radius, self.point_radius), self.point_radius)
        if self.scene.x_input != "" and self.scene.y_input != "" and not self.scene.user_has_shot:
            self.x = ((int(self.scene.x_input) / NUM_X_POINTS) * COORD_WIDTH) + PAD_LEFT
            self.y = HEIGHT - ((int(self.scene.y_input) / NUM_Y_POINTS) * COORD_HEIGHT) - PAD_BOTTOM
        else:
            self.x = -100 # @TODO: ad hoc
            self.y = -100 # @TODO: ad hoc
        

class Scoreboard(spyral.Sprite):
    def __init__(self, scene):
        super(Scoreboard, self).__init__()
        self.scene = scene

        self.curr_score = 0
        self.curr_shots = 0

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

        self.highlighted_coord = "x"

        self.redraw_all_pieces()
    

    def redraw_all_pieces(self):
        self.image = spyral.Image(size=(WIDTH, HEIGHT))

        self.image.draw_rect(COLORS["axes"],
                                    (PAD_LEFT + COORD_WIDTH + ((1 - SCOREBOARD_PERCENTAGE) / 2.0)*PAD_RIGHT, PAD_TOP),
                                    (SCOREBOARD_PERCENTAGE * PAD_RIGHT, SCOREBOARD_HEIGHT))

        # draw input rects
        if self.highlighted_coord == "x":
            # draw x input rect
            self.image.draw_rect(COLORS["highlighted_fill"],
                                        self.x_input_rect.__getattr__("topleft"),
                                        self.input_rect_size)
            # draw y input rect
            self.image.draw_rect(COLORS["not_highlighted_fill"],
                                        self.y_input_rect.__getattr__("topleft"),
                                        self.input_rect_size)
        elif self.highlighted_coord == "y":
            # draw x input rect
            self.image.draw_rect(COLORS["not_highlighted_fill"],
                                        self.x_input_rect.__getattr__("topleft"),
                                        self.input_rect_size)
            # draw y input rect
            self.image.draw_rect(COLORS["highlighted_fill"],
                                        self.y_input_rect.__getattr__("topleft"),
                                        self.input_rect_size)
        # draw submit input rect
        self.image.draw_rect(COLORS["shoot_fill"],
                                    self.submit_input_rect.__getattr__("topleft"),
                                    self.submit_rect_size)

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


    def type_key(self, key):
        if key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            # user entered an int
            if key == "\b":
                # enter has been pressed
                return
            if self.highlighted_coord == "x":
                self.scene.x_input += key
            elif self.highlighted_coord == "y":
                self.scene.y_input += key

class Basketball(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(Basketball, self).__init__(*args, **kwargs)
        
        self.user_has_shot = True
        self.waiting_for_input = True
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        
        self.hoops = get_hoops(self)

        self.points = []
        for i in range(int(NUM_X_POINTS + 1)):
            for j in range(int(NUM_Y_POINTS + 1)):
                self.points.append(Point(self, i, j))

        self.up_ball = Ball(self, 5)
        self.up_ball.pos = (COORD_WIDTH/2 + PAD_LEFT, HEIGHT)
        self.down_ball = Ball(self, 1)
        self.down_ball.image = spyral.Image(filename="basketball_images/basketball_small.png")

        # starts in middle, moved to correct posn later (before it drops)
        self.down_ball.pos = (WIDTH/2, -self.down_ball.image._surf.get_height())

        self.x_input = ""
        self.y_input = ""
        
        # We have to give our camera to the group so it knows where to draw
        self.group = spyral.Group(self.camera)
        # We can add the sprites to the group
        for hoop in self.hoops:
            self.group.add(hoop)
        self.group.add(self.up_ball)
        self.group.add(self.down_ball)

        self.graph = Graph(self)
        self.group.add(self.graph)

        for point in self.points:
            self.group.add(point)

        self.run_num = 1
        self.score = 0
        self.num_shots = 0

        self.scoreboard = Scoreboard(self)
        self.group.add(self.scoreboard)
        
        self.shot_point = ShotPoint(self)
        self.group.add(self.shot_point)

        self.pet = Pet(self)
        self.group.add(self.pet)


    def reset(self):
        for hoop in self.hoops:
            self.group.remove(hoop)

        self.user_has_shot = True

        self.hoops = get_hoops(self)
        for hoop in self.hoops:
            self.group.add(hoop)

        self.up_ball.pos = (COORD_WIDTH/2 + PAD_LEFT, HEIGHT)
        self.down_ball.pos = (WIDTH/2, -self.down_ball.image._surf.get_height())
        self.up_ball.vel_y = 0
        self.down_ball.vel_y = 0

        self.x_input = ""
        self.y_input = ""

        self.run_num = 1

        self.waiting_for_input = True


    def on_enter(self):
        background = spyral.Image(size=(WIDTH, HEIGHT))##filename="basketball_images/background.jpg")#
        background.fill(COLORS["background"])
        self.camera.set_background(background)

        
    def render(self):
        # Simply tell the group to draw
        self.group.draw()


    def hide_hoops(self):
        for hoop in self.hoops:
            if hoop.is_target:
                continue
            self.group.remove(hoop)

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
            if event['type'] == 'MOUSEBUTTONDOWN':
                pos = event['pos']
                self.scoreboard.get_input(pos)
            if event['type'] == 'KEYDOWN':
                if event['key'] == 27:
                    spyral.director.pop()
                self.scoreboard.type_key(event['unicode'])

        if self.waiting_for_input:
            # don't shoot basketball
            return
        
        if self.run_num == 3:
            if self.num_shots == 5:
                print "You made %d out of %d shots!" % (self.score, self.num_shots) # @TODO: print to scoreboard
                time.sleep(4)
                spyral.director.pop()
                return

            self.num_shots+=1
            for hoop in self.hoops:
                if not hoop.is_target:
                    continue
                if int(self.x_input) == hoop.x_coord and int(self.y_input) == hoop.y_coord:
                    print "You got a basket!" # @TODO: print to scoreboard
                    self.score += 1
                else:
                    print "You missed the basket!" # @TODO: print to scoreboard

        elif self.run_num > 3 and self.user_has_shot:
            self.hide_hoops()
            self.up_ball.shoot_up(dt)
            self.user_has_shot = False

        elif self.up_ball.pos[1] < (-1 * self.up_ball.image._surf.get_height()) - self.up_ball.hangtime:
            # @TODO: optimize {
            self.down_ball.shoot_down(dt, int(self.x_input)) # @TODO: only needs to be called once
            for hoop in self.hoops: # @TODO: for loop not necessary for every update
                if not hoop.is_target:
                    continue
                if int(self.x_input) == hoop.x_coord and int(self.y_input) == hoop.y_coord:
                    if (self.down_ball.y > (hoop.y - self.down_ball.ball_slow_range) and
                                self.down_ball.y < (hoop.y + self.down_ball.ball_slow_range)):
                        self.down_ball.vel_y = self.down_ball.ball_speed_slow
                    else:
                        self.down_ball.vel_y = self.down_ball.ball_speed_fast
            # @TODO: }
            if self.down_ball.pos[1] > (HEIGHT + self.down_ball.image._surf.get_height()) - self.down_ball.hangtime:
                self.reset()
        

        self.run_num += 1
