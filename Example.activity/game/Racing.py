import pygame
import spyral
import random

RC_WIDTH = 640
RC_HEIGHT = 480
UPPER_BOUND = 300
LANE_WIDTH = (RC_HEIGHT-UPPER_BOUND)/3
LINE_SIZE = [25,5]
LINE_COLOR = [255,255,0,255]

class LineList:
    def __init__(self,racingmain,y,between,counterFrac):
        self.main = racingmain
        self.group = racingmain.group
        self.between = between
        self.dist = -counterFrac*between
        self.list = []
        self.y = y
    def update(self,dt):
        while self.dist<=self.main.distance:
            self.list.append(Line(self,self.group,self.main.distance-self.dist,self.dist,self.y))
            self.dist+=self.between
        for line in self.list:
            if line.x>=RC_WIDTH+LINE_SIZE[0]:
                self.group.remove(line)
        self.list = [line for line in self.list if line.x<=RC_WIDTH+LINE_SIZE[0]]

class Line(spyral.Sprite):
    def __init__(self,linelist,group,x,dist,y):
        spyral.Sprite.__init__(self,group)
        self.linelist = linelist
        self.group.add(self)
        self.dist = dist
        self.pos = [x,y]
        self.anchor = 'midright'
        self.render()
    def render(self):
        self.image = spyral.Image(size = LINE_SIZE)
        self.image.fill(LINE_COLOR)
    def update(self,dt):
        self.x = self.linelist.main.distance-self.dist
        

class Car(spyral.Sprite):
    def __init__(self,group,speed,handle,turn):
        spyral.Sprite.__init__(self,group)
        self.handle = handle
        self.speed = speed
        self.turn = turn
        self.vx = 0
        self.vy = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.render()
        self.pos = (400,300)
    def render(self):
        self.image = spyral.Image(filename="racing_images/CatCar.png")
    def render2(self,active):
        if active:
            self.image = spyral.Image(filename="racing_images/CatCarFast.png")
        else:
            self.render()
    def update(self,dt):
        dx = 0
        dy = 0
        if self.right:
            dx = self.handle*dt
        if self.left:
            dx -= self.handle*dt
        if self.down:
            dy = self.turn*dt
        if self.up:
            dy -= self.turn*dt
        if dx==0:
            if self.vx>0:
                dx = -min(self.vx,self.handle*dt)
            elif self.vx<0:
                dx = min(-self.vx,self.handle*dt)
        if dy==0:
            if self.vy>0:
                dy = -min(self.vy,self.turn*dt)
            elif self.vy<0:
                dy = min(-self.vy,self.turn*dt)
        self.vx = max(-self.speed,min(self.vx+dx,self.speed))
        self.vy = max(-self.speed,min(self.vy+dy,self.speed))
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        if self.image._surf.get_height()+self.y>=RC_HEIGHT:
            self.y = RC_HEIGHT-self.image._surf.get_height()
            self.vy = 0
        if self.image._surf.get_width()+self.x>=RC_WIDTH:
            self.x = RC_WIDTH-self.image._surf.get_width()
            self.vx = 0
        if self.x<=0:
            self.x = 0
            self.vx = 0
        if self.y<=UPPER_BOUND:
            self.y = UPPER_BOUND
            self.vy = 0

class TurboMeter(spyral.Sprite):
    def __init__(self,group,maxTurbo):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.maxTurbo = maxTurbo
        self.turbo = maxTurbo/2
        self.active = False
        self.changed = False
        self.render()
    def render(self):
        self.image = spyral.Image(size = [25,80])
        self.anchor = 'topright'
        self.image.fill([255,0,0,255])
        self.image.draw_rect([0,255,0,255],[0,80-self.turbo*80/self.maxTurbo],[25,80])
        self.pos = [RC_WIDTH-10,10]
    def toggle(self):
        oldact = self.active
        self.active = not(self.active)
        if self.turbo==0:
            self.active = False
        self.changed = oldact==self.active
    def update(self,dt):
        oldact = self.active
        if self.active:
            self.turbo = max(0,self.turbo-dt)
        if self.turbo==0:
            self.active = False
        self.changed = oldact==self.active or self.changed
        if self.changed:
            self.render()
    def refill(self,num):
        self.turbo = min(self.turbo+num,self.maxTurbo)

class Question(spyral.Sprite):
    def __init__(self,main,dist):
        spyral.Sprite.__init__(self,main.group)
        self.main = main
        self.group.add(self)
        self.num1 = random.randint(1,49)
        i = random.randint(0,1)
        opers = ["+","-"]
        self.oper = opers[i]
        self.num2 = random.randint(1,49)
        self.pos = [RC_WIDTH/2,30]
        self.dist = dist
        self.done = False
        self.answers = []
        self.generateAnswers()
        self.render()
    def generateAnswers(self):
        right = 0
        wrongs = []
        if self.oper == "+":
            right = self.num1+self.num2
            wrongs = [right+10,right+1,right-1,right-10,right-2*self.num2]
        if self.oper == "-":
            right = self.num1-self.num2
            wrongs = [right+2*self.num2,-right,right-10,right+10]
        wrongs = [ans for ans in wrongs if not(ans==right)]
        i = random.randint(0,len(wrongs)-1)
        i2 = random.randint(0,len(wrongs)-2)
        if i2>=i:
            i2+=1
        answers = [right,wrongs[i],wrongs[i2]]
        inorder = []
        while len(answers)>0:
            i = random.randint(0,len(answers)-1)
            inorder.append(answers[i])
            answers.remove(answers[i])
        self.answers = []
        for i in range(len(inorder)):
            answer = RacingAnswer(self,inorder[i],UPPER_BOUND+(2*i+1)*LANE_WIDTH*.5,
                                  inorder[i]==right,self.dist+random.randint(500,1500))
            self.answers.append(answer)        
    def render(self):
        self.image = spyral.Image(size = [300,30])
        self.anchor = 'center'
        font = pygame.font.SysFont(None,40)
        surf = font.render(self.num1.__str__()+" "+self.oper+" "+
                           self.num2.__str__()+" = ?",
                           True,[255,255,255,255])
        self.image._surf.blit(surf,[150-surf.get_width()*.5,
                                    15-surf.get_height()*.5])
    def renderGuess(self,correct):
        right = 0
        if self.oper == "+":
            right = self.num1+self.num2
        if self.oper == "-":
            right = self.num1-self.num2
        self.image = spyral.Image(size = [300,30])
        self.anchor = 'center'
        font = pygame.font.SysFont(None,40)
        color = [255,0,0,255]
        if correct:
            color = [0,255,0,255]
        surf = font.render(self.num1.__str__()+" "+self.oper+" "+
                           self.num2.__str__()+" = "+right.__str__(),
                           True,color)
        self.image._surf.blit(surf,[150-surf.get_width()*.5,
                                    15-surf.get_height()*.5])
    def update(self,dt):
        pass

class RacingAnswer(spyral.Sprite):
    def __init__(self,question,num,y,correct,dist):
        spyral.Sprite.__init__(self,question.group)
        self.question = question
        self.group.add(self)
        self.num = num
        self.pos = [0,y]
        self.correct = correct
        self.dist = dist
        self.stage = 'far'
        self.render()
    def render(self):
        self.render2([255,0,0,128],[0,0,0,128])
    def render2(self,col1,col2):
        self.image = spyral.Image(size = [32,24])
        self.image.fill(col1)
        self.anchor = 'midleft'
        font = pygame.font.SysFont(None,24)
        surf = font.render(self.num.__str__(),True,col2)
        self.image._surf.blit(surf,[16-surf.get_width()*.5,
                                    12-surf.get_height()*.5])
    def update(self,dt):
        if self.stage=='far':
            if self.question.main.distance>=self.dist-200:
                self.stage = 'close'
                self.render2([255,255,0,128],[0,0,0,128])
        elif self.stage=='close':
            if self.question.main.distance>=self.dist:
                self.stage = 'here'
                self.render2([0,255,0,255],[0,0,0,255])
                self.x = self.question.main.distance-self.dist
        else:
            self.x = self.question.main.distance-self.dist
            if self.question.main.car.get_rect().collide_rect(self.get_rect()):
                if self.correct:
                    self.question.main.turbometer.refill(2)
                else:
                    self.question.main.setSlow(.2)
                self.question.renderGuess(self.correct)
                for ans in self.question.answers:
                    self.question.main.group.remove(ans)

class RacingMain(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (RC_WIDTH, RC_HEIGHT),layers = ['__default__','on_road','over_road'])
        self.group = spyral.Group(self.camera)
        self.normalspeed = 200
        self.accel = 50
        self.speed = self.normalspeed
        self.slow = 1
        self.distance = RC_WIDTH
        self.timer = 0
        self.questionNum = 1
        self.linelist1 = LineList(self,UPPER_BOUND+LANE_WIDTH,100,6)
        self.linelist2 = LineList(self,UPPER_BOUND+LANE_WIDTH*2,100,6.9)
        self.car = Car(self.group,self.normalspeed,300,300)
        self.turbometer = TurboMeter(self.group,10)
        self.question = Question(self,self.distance)
        self.render()
    def setSlow(self,slow):
        self.slow = min(self.slow,slow)
    def render(self):
        self.group.draw()
    def toggleTurbo(self):
        self.turbometer.toggle()
    def update(self,dt):
        self.timer+=dt
        if self.turbometer.changed:            
            self.turbometer.changed = False
            self.car.render2(self.turbometer.active)
        self.speed = self.normalspeed
        if self.turbometer.active:
            self.speed*=2
        if self.slow<1:
            self.slow = min(1,self.slow+(dt*self.accel)/self.normalspeed)
        self.speed*=self.slow
        self.distance+=self.speed*dt
        if self.distance>=RC_WIDTH+2000*self.questionNum:
            for ans in self.question.answers:
                self.group.remove(ans)
            self.group.remove(self.question)
            self.question = Question(self,self.distance)
            self.questionNum+=1
        self.linelist1.update(dt)
        self.linelist2.update(dt)
        self.group.update(dt)
        self.group.remove(self.car)
        self.group.add(self.car)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()  # Happens when someone asks the OS to close the program
                return
            if event['type'] == 'KEYDOWN':
                if event['key'] == 27:
                    spyral.director.pop()
                    return
                if event['key']==273:
                    self.car.up = True
                if event['key']==274:
                    self.car.down = True
                if event['key']==275:
                    self.car.right = True
                if event['key']==276:
                    self.car.left = True
                if event['key']==32:
                    self.toggleTurbo()
            if event['type'] == 'KEYUP':
                if event['key']==273:
                    self.car.up = False
                if event['key']==274:
                    self.car.down = False
                if event['key']==275:
                    self.car.right = False
                if event['key']==276:
                    self.car.left = False
        #print (self.speed-self.car.vx)/20,"m/s"
        #print (self.distance-self.car.x)/20,"meters"
    def on_enter(self):
        bg = spyral.Image(size=(RC_WIDTH,RC_HEIGHT))
        bg.fill([0,0,0,255])
        bg.draw_rect([100,100,100,255],[0,UPPER_BOUND],[RC_WIDTH,RC_HEIGHT])
        self.camera.set_background(bg)
