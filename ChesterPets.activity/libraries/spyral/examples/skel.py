try:
    import _path
except NameError:
    pass
import pygame
import spyral
import sys

SIZE = (640, 480)
BG_COLOR = (0, 0, 0)

class Game(spyral.Scene):
    """
    A Scene represents a distinct state of your game. They could be menus,
    different subgames, or any other things which are mostly distinct.
    
    A Scene should define two methods, update and render.
    """
    def __init__(self):
        """
        The __init__ message for a scene should set up the camera(s) for the
        scene, and setup groups and other structures which are needed for the
        scene.
        """
        spyral.Scene.__init__(self)
        # We cannot draw directly to the root camera, so we always make a child
        # camera for our scene with our requested virtual resolution. In this
        # case we'll use the same as the window size, but this doesn't have to be
        # the case
        self.camera = self.parent_camera.make_child(SIZE)
        self.group = spyral.Group(self.camera)
        self.initialized = False
        
    def on_enter(self):
        # Some things you may wish to do every time you enter the scene
        if self.initialized:
            return
        self.initialized = True
        # Other things you may want to do only once
        bg = spyral.Image(size=SIZE)
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
        # More setup here
                
    def render(self):
        """
        The render function should call .draw() on the scene's group(s).
        Unless your game logic should be bound by framerate,
        logic should go elsewhere.
        """
        self.group.draw()
        
    def update(self, dt):
        """
        The update function should contain or call out to all the logic.
        Here is where group.update() should be called for the groups, where
        event handling should be taken care of, etc.
        """
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.quit()
                sys.exit()
                    
        self.group.update(dt)

if __name__ == "__main__":
    spyral.init() # Always call spyral.init() first
    spyral.director.init(SIZE) # the director is the manager for your scenes
    spyral.director.push(Game()) # push means that this Game() instance is
                                 # on the stack to run
    spyral.director.run() # This will run your game. It will not return.
