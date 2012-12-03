import pygame
import spyral
import random
import TownMap

WIDTH = 1200
HEIGHT = 900
UPPER_BOUND = 400
LANE_WIDTH = (HEIGHT - UPPER_BOUND) / 3
LINE_SIZE = [25,5]
LINE_COLOR = [255,255,0,255]
FONT1 = pygame.font.SysFont(None,60)
FONT2 = pygame.font.SysFont(None,36)

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
            if line.x>=WIDTH+LINE_SIZE[0]:
                self.group.remove(line)
        self.list = [line for line in self.list if line.x<=WIDTH+LINE_SIZE[0]]

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
        self.image = spyral.Image(filename="images/racing/cat.png")
    def render2(self,active):
        if active:
            self.image = spyral.Image(filename="images/racing/cat_turbo.png")
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
        self.vy = max(-self.turn,min(self.vy+dy,self.turn))
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        if self.image._surf.get_height()+self.y>=HEIGHT:
            self.y = HEIGHT-self.image._surf.get_height()
            self.vy = 0
        if self.image._surf.get_width()+self.x>=WIDTH:
            self.x = WIDTH-self.image._surf.get_width()
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
        self.turbo = maxTurbo*.5
        self.active = False
        self.changed = False
        self.slow = False
        self.render()
        TurboText(self)
    def render(self):
        self.image = spyral.Image(size = [200,48])
        self.anchor = 'topright'
        self.image.fill([153,153,153,255])
        self.image.draw_rect(self.get_color(),[self.turbo*200/self.maxTurbo-200,0],[200,48])
        self.pos = [WIDTH-10,10]
    def get_color(self):
        ratio = self.turbo/self.maxTurbo
        return [min(255,510-ratio*510),min(255,510*ratio),0,255]
    def toggle(self):
        if self.slow:
            return
        oldact = self.active
        self.active = not(self.active)
        if self.turbo==0:
            self.active = False
        self.changed = oldact==self.active
    def turnOff(self):
        self.active = False
        self.changed = True
        self.slow = True
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
        self.changed = True

class TurboText(spyral.Sprite):
    def __init__(self,turbometer):
        spyral.Sprite.__init__(self,turbometer.group)
        self.group.add(self)
        self._set_layer("hud2")
        self.meter = turbometer
        emptyText = FONT2.render("Empty",True,[128,0,0,255])
        turboText = FONT2.render("TURBO!!!",True,[0,0,255,255])
        maxText = FONT2.render("MAX!",True,[0,0,255,255])
        slowText = FONT2.render("Slow",True,[128,0,0,255])
        readyText = FONT2.render("Ready!",True,[0,0,128,255])
        self.texts = [emptyText,turboText,slowText,maxText,readyText]
        self.state = self.getState()
        self.anchor = turbometer.anchor
        self.pos = turbometer.pos
        self.render()
    def getState(self):
        if self.meter.slow:
            return 2
        if self.meter.turbo==0:
            return 0
        if self.meter.active:
            return 1
        if self.meter.turbo==self.meter.maxTurbo:
            return 3
        return 4
    def render(self):
        self.image = spyral.Image(size = [200,48])
        text = self.texts[self.state]
        self.image._surf.blit(text,[100-text.get_width()*.5,24-text.get_height()*.5])
        if self.state==1:
            self.image.draw_rect([0,255,255,128],[0,0],[199,47],2)
    def update(self,dt):
        state2 = self.getState()
        if not(state2==self.state):
            self.state = state2
            self.render()

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
        self.pos = [WIDTH/2,30]
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
        self.image = spyral.Image(size = [500,60])
        self.anchor = 'center'
        surf = FONT1.render(self.num1.__str__()+" "+self.oper+" "+
                           self.num2.__str__()+" = ?",
                           True,[255,255,255,255])
        self.image._surf.blit(surf,[250-surf.get_width()*.5,
                                    30-surf.get_height()*.5])
    def renderGuess(self,correct):
        right = 0
        if self.oper == "+":
            right = self.num1+self.num2
        if self.oper == "-":
            right = self.num1-self.num2
        self.image = spyral.Image(size = [500,60])
        self.anchor = 'center'
        color = [255,0,0,255]
        if correct:
            color = [0,255,0,255]
        surf = FONT1.render(self.num1.__str__()+" "+self.oper+" "+
                           self.num2.__str__()+" = "+right.__str__(),
                           True,color)
        self.image._surf.blit(surf,[250-surf.get_width()*.5,
                                    30-surf.get_height()*.5])
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
        self.image = spyral.Image(size = [54,36])
        self.image.fill(col1)
        self.anchor = 'midleft'
        surf = FONT2.render(self.num.__str__(),True,col2)
        self.image._surf.blit(surf,[27-surf.get_width()*.5,
                                    18-surf.get_height()*.5])
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
                    self.question.main.turbometer.refill(3)
                else:
                    self.question.main.setSlow(0)
                self.question.renderGuess(self.correct)
                for ans in self.question.answers:
                    self.question.main.group.remove(ans)

class TimerSprite(spyral.Sprite):
    def __init__(self,main):
        spyral.Sprite.__init__(self,main.group)
        self.group.add(self)
        self.main = main
        self.anchor = 'topleft'
        self.time = int(main.timer)
        self.pos = [5,5]
        self.render()


    def render(self):
        self.image = spyral.Image(size = [100,20])
        surf = FONT2.render(self.getTimeString(),True,[255,255,255,255])
        self.image._surf.blit(surf,[0,10-surf.get_height()*.5])


    def getTimeString(self):
        minutes = int(self.time/60)
        seconds = self.time%60
        z = minutes.__str__()+":"
        if minutes<10:
            z = "0"+z
        if seconds<10:
            z+="0"
        return z+seconds.__str__()


    def update(self,dt):
        time2 = int(self.main.timer)
        if not(time2==self.time):
            self.time = time2
            self.render()
    

class RacingMain(spyral.Scene):
    def __init__(self, passed_in_pet):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT),layers = ['__default__','on_road','over_road','hud','hud2'])
        self.group = spyral.Group(self.camera)
        self.normalspeed = 200
        self.accel = 50
        self.speed = self.normalspeed
        self.slow = 1
        self.distance = WIDTH
        self.timer = 0
        self.questionNum = 1
        self.linelist1 = LineList(self,UPPER_BOUND+LANE_WIDTH,100,6)
        self.linelist2 = LineList(self,UPPER_BOUND+LANE_WIDTH*2,100,6.9)
        self.car = Car(self.group,self.normalspeed,300,300)
        self.turbometer = TurboMeter(self.group,10)
        self.question = Question(self,self.distance)
        self.timerSprite = TimerSprite(self)

        self.pet = passed_in_pet


    def setSlow(self,slow):
        self.slow = min(self.slow,slow)
        self.turbometer.turnOff()


    def render(self):
        self.group.draw()


    def toggleTurbo(self):
        self.turbometer.toggle()


    def update(self,dt):
        if self.distance >= 16000: # @TODO: magic
            # game over
            # @TODO: wait
            # @TODO: show end screen
            self.pet.money += (100 - int(self.timer)) # @TODO: 100 is magic
            print self.pet.money
            spyral.director.pop()
            if self.pet.destination == "Touheyville":
                spyral.director.push(TownMap.Touheyville(self.pet))
            elif self.pet.destination == "Hong Kong":
                spyral.director.push(TownMap.HongKong(self.pet))
            else:
                spyral.director.push(TownMap.ODowdShire(self.pet))
            return
        self.timer+=dt
        self.speed = self.normalspeed
        if self.turbometer.active:
            self.speed*=2
        if self.slow<1:
            self.slow = min(1,self.slow+(dt*self.accel)/self.normalspeed)
        else:
            self.turbometer.slow = False
        if self.turbometer.changed:
            self.turbometer.changed = False
            self.car.render2(self.turbometer.active)
        self.speed*=self.slow
        self.distance+=self.speed*dt
        if self.distance>=WIDTH+3000*self.questionNum and self.questionNum<5:
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
            if event['type'] == 'KEYDOWN':
                if event['key']==273:
                    # up arrow
                    self.car.up = True
                if event['key']==274:
                    # down arrow
                    self.car.down = True
                if event['key']==275:
                    # right arrow
                    self.car.right = True
                if event['key']==276:
                    # left arrow
                    self.car.left = True
                if event['key']==32:
                    # spacebar
                    self.toggleTurbo()
            if event['type'] == 'KEYUP':
                if event['key']==273:
                    # up arrow
                    self.car.up = False
                if event['key']==274:
                    # down arrow
                    self.car.down = False
                if event['key']==275:
                    # right arrow
                    self.car.right = False
                if event['key']==276:
                    # left arrow
                    self.car.left = False


    def on_enter(self):
        bg = spyral.Image(size=(WIDTH,HEIGHT))
        bg.fill([0, 0, 0, 255]) # @TODO: magic
        bg.draw_rect([100, 100, 100, 255], [0, UPPER_BOUND], [WIDTH, HEIGHT]) # @TODO: magic
        self.camera.set_background(bg)
