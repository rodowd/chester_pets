"""try:
    import _path
except NameError:
    pass"""
import pygame
import spyral
from spyral.sprite import Sprite
from spyral.scene import Scene
import math
import sys
import random

CW_WIDTH = 640
CW_HEIGHT = 480
BLOCK_SIZE = 20
NUMBERFONT = 0
LETTERFONT = 20
BG_COLOR = (100, 100, 100)

def readWords(filename):
    """
    takes a file name and returns a list of vocabulary words from its data.
    """
    f = open(filename,'r')
    strings = f.readlines()
    words = [getWord(s) for s in strings]
    return words
def getWord(string):
    """
    splits up the line from the file and uses its info to create
    and return a word with its definitions.
    word:definition1;definition2;definition3
    """
    string = string[0:-1]
    s2 = string.split(":")
    s3 = s2[1].split(";")
    return Word(s2[0],s3)

class Word:
    """
    A word has an all uppercase string depending on what the word is,
    and a list of definitions that it will pick randomly to use as a hint.
    The definition might end in something like .jpg for image, but
    this is currently not handled.
    """
    def __init__(self,string,definitions):
        self.string = string.upper()
        self.definitions = definitions
    def __str__(self):
        return self.string
    def getDef(self):
        if len(self.definitions)==0:
            return self.string
        i = random.randint(0,len(self.definitions)-1)
        return self.definitions[i]

class Crossword:
    """
    The crossword will probably not be the actual puzzle, but it definitely
    will be the generator for it. size is a number that represents how
    big a grid the puzzle can be. acrossgrid is a 2d boolean grid representing
    any place where an across word can have a letter. downgrid is the same for
    down. lettergrid is a grid that contains all the correct letters. hints is
    the list of lists containing whether a word is across or down, and its
    definition.
    """
    #MAKE A CHECK TO SEE IF THE PUZZLE IS TOO SMALL
    #MAKE HINTS CLEARER
    def __init__(self,size,words):
        self.size = size
        self.acrossgrid = [[True for y in range(size)] for x in range(size)]
        self.downgrid = [[True for y in range(size)] for x in range(size)]
        self.lettergrid = [['' for y in range(size)] for x in range(size)]
        self.hints = []
        self.create(words)
    def create(self,words):
        self.insertFirstWord(words)
        while True:
            if len(words)==0:
                return
            done = False
            for x in range(15):
                if not(done):
                    i = random.randint(0,len(words)-1)
                    done = self.addWordDown(words[i])
                    if done:
                        words.remove(words[i])
            if len(words)==0:
                return
            done2 = False
            for x in range(15):
                if not(done2):
                    i = random.randint(0,len(words)-1)
                    done2 = self.addWordAcross(words[i])
                    if done2:
                        words.remove(words[i])
            if not(done) and  not(done2):
                return
    def insertFirstWord(self,words):
        """
        i = random.randint(0,len(words)-1)
        if len(words[i].string)<7:
            self.insertFirstWord(words)
            return
        """
        bigwords = [word for word in words if len(word.string)>7]
        i = random.randint(0,len(bigwords)-1)
        self.placeFirstWord(bigwords[i])
        words.remove(bigwords[i])
    def placeFirstWord(self,word):
        y = self.size/2
        x = (self.size-len(word.string))/2
        self.setWordAcross(x,y,word)
#        self.setWordAcross(2,2,word)
    def addWordAcross(self,word,lowest = 2):
        n = 0
        L = []
        for x in range(self.size+1-len(word.string)):
            for y in range(self.size):
                n2 = self.checkWordAcross(x,y,word)
                if n2==n:
                    L.append([x,y])
                elif n2>n:
                    n = n2
                    L = [[x,y]]
        if n<lowest:
            return False
        i = random.randint(0,len(L)-1)
        self.setWordAcross(L[i][0],L[i][1],word)
        return True
    def addWordDown(self,word,lowest = 2):
        n = 0
        L = []
        for x in range(self.size):
            for y in range(self.size+1-len(word.string)):
                n2 = self.checkWordDown(x,y,word)
                if n2==n:
                    L.append([x,y])
                elif n2>n:
                    n = n2
                    L = [[x,y]]
        if n<lowest:
            return False
        i = random.randint(0,len(L)-1)
        self.setWordDown(L[i][0],L[i][1],word)
        return True
    def isEmpty(self,x,y):
        if x<0 or y<0 or x>=self.size or y>=self.size:
            return True
        return self.lettergrid[x][y]==''
    def cancelAcross(self,x,y):
        if x<0 or y<0 or x>=self.size or y>=self.size:
            return
        self.acrossgrid[x][y] = False
    def cancelDown(self,x,y):
        if x<0 or y<0 or x>=self.size or y>=self.size:
            return
        self.downgrid[x][y] = False
    def cancelBoth(self,x,y):
        if x<0 or y<0 or x>=self.size or y>=self.size:
            return
        self.acrossgrid[x][y] = False
        self.downgrid[x][y] = False
    def checkWordAcross(self,x,y,word):
        if x<0 or y<0 or x+len(word.string)>self.size or y>=self.size:
            return False
        if not(self.isEmpty(x-1,y)):
            return False
        if not(self.isEmpty(x+len(word.string),y)):
            return False
        if self.isEmpty(x,y):
            if not(self.isEmpty(x,y-1)):
                return False
            if not(self.isEmpty(x,y+1)):
                return False
        if self.isEmpty(x+len(word.string)-1,y):
            if not(self.isEmpty(x+len(word.string)-1,y-1)):
                return False
            if not(self.isEmpty(x+len(word.string)-1,y+1)):
                return False
        n = 1
        for x2 in range(len(word.string)):
            if not(self.acrossgrid[x+x2][y]):
                return False
            if not(self.lettergrid[x+x2][y]==''):
                if not(self.lettergrid[x+x2][y]==word.string[x2]):
                    return False
                n+=1
        return  n
    def checkWordDown(self,x,y,word):
        if x<0 or y<0 or y+len(word.string)>self.size or x>=self.size:
            return False
        if not(self.isEmpty(x,y-1)):
            return False
        if not(self.isEmpty(x,y+len(word.string))):
            return False
        if self.isEmpty(x,y):
            if not(self.isEmpty(x-1,y)):
                return False
            if not(self.isEmpty(x+1,y)):
                return False
        if self.isEmpty(x,y+len(word.string)-1):
            if not(self.isEmpty(x-1,y+len(word.string)-1)):
                return False
            if not(self.isEmpty(x+1,y+len(word.string)-1)):
                return False
        n = 1
        for y2 in range(len(word.string)):
            if not(self.downgrid[x][y+y2]):
                return False
            if not(self.lettergrid[x][y+y2]==''):
                if not(self.lettergrid[x][y+y2]==word.string[y2]):
                    return False
                n+=1
        return  n
    def setWordAcross(self,x,y,word):
        self.cancelBoth(x-1,y)
        self.cancelBoth(x+len(word.string),y)
        self.cancelAcross(x,y)
        self.cancelAcross(x+len(word.string)-1,y)
        self.lettergrid[x][y] = word.string[0]
        self.lettergrid[x+len(word.string)-1][y] = word.string[-1]
        for x2 in range(1,len(word.string)-1):
            self.cancelAcross(x+x2,y-1)
            self.cancelAcross(x+x2,y)
            self.cancelAcross(x+x2,y+1)
            self.lettergrid[x+x2][y] = word.string[x2]
        self.hints.append([x,y,"Across",word.string,word.getDef()])
    def setWordDown(self,x,y,word):
        self.cancelBoth(x,y-1)
        self.cancelBoth(x,y+len(word.string))
        self.cancelDown(x,y)
        self.cancelDown(x,y+len(word.string)-1)
        self.lettergrid[x][y] = word.string[0]
        self.lettergrid[x][y+len(word.string)-1] = word.string[-1]
        for y2 in range(1,len(word.string)-1):
            self.cancelDown(x-1,y+y2)
            self.cancelDown(x,y+y2)
            self.cancelDown(x+1,y+y2)
            self.lettergrid[x][y+y2] = word.string[y2]
        self.hints.append([x,y,"Down",word.string,word.getDef()])
    def __str__(self):
        z = ""
        for y in range(self.size):
            z+="|"
            for x in range(self.size):
                z+=self.lettergrid[x][y]
                if self.lettergrid[x][y]=='':
                    z+=' '
            z+="|\n"
        z = ".\n"+z+"'"
        for x in range(self.size):
            z ="-"+z+"-"
        return "."+z+"'\n"

class Puzzle(spyral.Sprite):
    def __init__(self,crossword,group):
        spyral.Sprite.__init__(self,group)
        group.add(self)
        self.smallfont = pygame.font.SysFont(None,NUMBERFONT)
        self.bigfont = pygame.font.SysFont(None,LETTERFONT)
        self.answer = crossword.lettergrid
        self.gridsize = crossword.size
        self.grid = [['' for y in range(self.gridsize)] for x in range(self.gridsize)]
        self.setHints(crossword.hints)
        self.setHintGrid()
        self.currentHint = self.downhints[0]
        if self.acrosshints[0][0]==1:
            self.currentHint = self.acrosshints[0]
        self.setGuess()
        self.render()
    def setGuess(self):
        self.guess = ""
        for x in range(len(self.currentHint[2])):
            self.guess+="_ "
        self.guessindex = 0
        self.guesslength = len(self.currentHint[2])
    def setHintGrid(self):
        self.hintgrid = [[[] for y in range(self.gridsize)] for x in range(self.gridsize)]
        for hint in self.acrosshints:
            coords = self.getBoxCoords(hint[0])
            for x in range(len(hint[2])):
                self.hintgrid[coords[0]+x][coords[1]].append(hint)
        for hint in self.downhints:
            coords = self.getBoxCoords(hint[0])
            for y in range(len(hint[2])):
                self.hintgrid[coords[0]][coords[1]+y].append(hint)
    def getBoxCoords(self,num):
        for boxnum in self.boxnumbers:
            if num==boxnum[0]:
                return [boxnum[1],boxnum[2]]
    def setHint(self,x,y):
        xgrid = x/BLOCK_SIZE
        ygrid = y/BLOCK_SIZE
        if xgrid<0 or ygrid<0 or xgrid>=self.gridsize or ygrid>=self.gridsize:
#            print "Out of bounds"
            return
        if self.answer[xgrid][ygrid]=='':
#            print "Not valid box spot"
            return
        hintlist = self.hintgrid[xgrid][ygrid]
        if len(hintlist)==2:
            if hintlist[0]==self.currentHint:
                self.currentHint = hintlist[1]
            else:
                self.currentHint = hintlist[0]
        else:
            self.currentHint = hintlist[0]
        self.setGuess()
    def sameHint(self,x,y,hint):
        hintlist = self.hintgrid[x][y]
        for hint2 in hintlist:
            if hint==hint2:
                return True
        return False
    def render(self):
        self.image = spyral.Image(size=[CW_WIDTH,CW_HEIGHT])
        self.image.pos = [0,0]
        for y in range(self.gridsize):
            for x in range(self.gridsize):
                if not(self.answer[x][y]==''):
                    color = [204,204,255,255]
                    if self.sameHint(x,y,self.currentHint):
                        color = [255,255,153,255]
                    self.image.draw_rect(color,
                                         [x*BLOCK_SIZE,y*BLOCK_SIZE],
                                         [BLOCK_SIZE+1,BLOCK_SIZE+1])
                    self.image.draw_rect([0,0,0,255],
                                         [x*BLOCK_SIZE,y*BLOCK_SIZE],
                                         [BLOCK_SIZE+1,BLOCK_SIZE+1],1)
                if not(self.grid[x][y]==''):
                    surf = self.bigfont.render(self.answer[x][y],True,[0,0,0,255]).convert_alpha()
                    self.image._surf.blit(surf,[BLOCK_SIZE*(x+.5)-surf.get_width()*.5+1,
                                                BLOCK_SIZE*(y+.5)-surf.get_height()*.5+2])
        hintstring = self.currentHint[1]
        if self.currentHint[1]=='':
            hintstring = self.currentHint[2]
        hintprint = self.bigfont.render(hintstring,True,[0,0,0,255]).convert_alpha()
        self.image._surf.blit(hintprint,[5,BLOCK_SIZE*self.gridsize+15])
        for boxnum in self.boxnumbers:
            num = boxnum[0]
            x = boxnum[1]
            y = boxnum[2]
            surf = self.smallfont.render(num.__str__(),True,[0,0,0,255]).convert_alpha()
            self.image._surf.blit(surf,[BLOCK_SIZE*x+2,
                                        BLOCK_SIZE*y+2])
        guessprint = self.bigfont.render(self.guess,True,[0,0,0,255]).convert_alpha()
        self.image._surf.blit(guessprint,[5,BLOCK_SIZE*self.gridsize+35])
    def update(self,dt):
        self.render()
        pass
    def setHints(self,hints):
        self.downhints = []
        self.acrosshints = []
        self.boxnumbers = []
        num = 1
        for y in range(self.gridsize):
            for x in range(self.gridsize):
                L = [hint for hint in hints if hint[0]==x and hint[1]==y]
                if len(L)>0:
                    self.boxnumbers.append([num,x,y])
                    for info in L:
                        if info[2]=="Across":
                            self.acrosshints.append([num,info[4],info[3]])
                        else:
                            self.downhints.append([num,info[4],info[3]])
                    num+=1
    def typekey(self,key):
        key = key.upper()
        alpha = ['Q','W','E','R','T','Y','U','I','O','P',
                 'A','S','D','F','G','H','J','K','L',
                 'Z','X','C','V','B','N','M']
        if key=='\b':
            if self.guessindex==0:
                return
            self.guess = self.guess[0:self.guessindex-1]+"_ "+self.guess[self.guessindex:]
            self.guessindex-=1;
            return
        for letter in alpha:
            if letter==key:
                if self.guessindex==self.guesslength:
                    return
                self.guess = self.guess[0:self.guessindex]+key+self.guess[self.guessindex+2:]
                self.guessindex+=1
                return
    def checkanswer(self):
        if not(self.guess==self.currentHint[2]):
            print "INCORRECT!!!"
            return
        coords = self.getBoxCoords(self.currentHint[0])
        across = False
        for hint in self.acrosshints:
            if hint==self.currentHint:
                across = True
        if across:
            for x in range(len(self.guess)):
                self.grid[coords[0]+x][coords[1]] = self.guess[x]
            return
        for y in range(len(self.guess)):
            self.grid[coords[0]][coords[1]+y] = self.guess[y]
            
    def printHints(self):
        print "ACROSS:"
        for hint in self.acrosshints:
            print " ",hint[0],"\t",hint[2],": ",hint[1]
        print "DOWN:"
        for hint in self.downhints:
            print " ",hint[0],"\t",hint[2],": ",hint[1]
    def cycleHints(self):
        for i in range(len(self.acrosshints)):
            hint = self.acrosshints[i]
            if hint==self.currentHint:
                if i+1==len(self.acrosshints):
                    self.currentHint = self.downhints[0]
                    self.setGuess()
                    return
                self.currentHint = self.acrosshints[i+1]
                self.setGuess()
                return
        for i in range(len(self.downhints)):
            hint = self.downhints[i]
            if hint==self.currentHint:
                if i+1==len(self.downhints):
                    self.currentHint = self.acrosshints[0]
                    self.setGuess()
                    return
                self.currentHint = self.downhints[i+1]
                self.setGuess()
                return
                

class CrosswordMain(spyral.Scene):
    """
    this will be the actual scene that the crossword is run on.
    """
    def __init__(self):#change to (self,head,body,etc.)
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (CW_WIDTH, CW_HEIGHT))
        self.group = spyral.Group(self.camera)
        words = readWords("wordlist.txt")
        cross = Crossword(15,words)
        self.puzzle = Puzzle(cross,self.group)
        self.render()
    
    def on_enter(self):
        bg = spyral.Image(size=(CW_WIDTH,CW_HEIGHT))
        bg.fill(BG_COLOR)
        self.camera.set_background(bg)
        
    def render(self):
        self.group.draw()

    def update(self,dt):
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()  # Happens when someone asks the OS to close the program
                return
            if event['type'] == 'MOUSEBUTTONDOWN':
                pos = event['pos']
                self.puzzle.setHint(pos[0],pos[1])
            if event['type'] == 'KEYDOWN':
                self.puzzle.typekey(event['unicode'])
                if event['key']==13:
                    self.puzzle.checkanswer()
                if event['key']==9:
                    self.puzzle.cycleHints()
            if self.puzzle.answer == self.puzzle.grid:
                print "YOU SOLVED THE PUZZLE!!!"
                spyral.director.pop()  # Happens when someone asks the OS to close the program
                return
                #if event['ascii'] == 'p':
                 #   spyral.director.pop()

## RACING GAME CODE STARTS HERE

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
    def __init__(self,group,handle,accel,turn):
        spyral.Sprite.__init__(self,group)
        self.handle = handle
        self.turn = turn
        self.accel = accel
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
            dx = self.accel*dt
        if self.left:
            dx -= self.accel*dt
        if self.down:
            dy = self.turn*dt
        if self.up:
            dy -= self.turn*dt
        if dx==0:
            if self.vx>0:
                dx = -min(self.vx,self.accel*dt)
            elif self.vx<0:
                dx = min(-self.vx,self.accel*dt)
        if dy==0:
            if self.vy>0:
                dy = -min(self.vy,self.accel*dt)
            elif self.vy<0:
                dy = min(-self.vy,self.accel*dt)
        self.vx = max(-self.handle,min(self.vx+dx,self.handle))
        self.vy = max(-self.handle,min(self.vy+dy,self.handle))
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
        self.turbo = maxTurbo
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
        self.changed = oldact==self.active
        if self.changed:
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



class RacingMain(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (RC_WIDTH, RC_HEIGHT))
        self.group = spyral.Group(self.camera)
        self.speed = 200
        self.distance = 150
        self.linelist1 = LineList(self,UPPER_BOUND+LANE_WIDTH,100,6)
        self.linelist2 = LineList(self,UPPER_BOUND+LANE_WIDTH*2,100,6.9)
        self.car = Car(self.group,200,300,300)
        #(self,group,speed,y,wait)
        self.question = Question(self,self.distance)
        self.turbometer = TurboMeter(self.group,20)
        self.render()
    def render(self):
        self.group.draw()
    def toggleTurbo(self):
        self.turbometer.toggle()
    def update(self,dt):
        if self.turbometer.changed:
            if self.turbometer.active:
                self.speed = 600
            else:
                self.speed = 200
            self.turbometer.changed = False
            self.car.render2(self.turbometer.active)
        self.distance+=self.speed*dt
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
