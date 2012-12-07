import pygame
import spyral
import random

WIDTH = 1200
HEIGHT = 900
BLOCK_SIZE = 38
LETTERFONT = 38
BG_COLOR = (100, 100, 100)
PUZZLE_POS = [120,60]

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
    string = string.replace('\n','').replace('\r','')
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
        self.hint_sort()
    def hint_sort(self):
        hints = self.hints
        self.hints = []
        for hint in hints:
            self.insertHint(hint)
    def insertHint(self,hint):
        for i in range(len(self.hints)):
            if self.comes_before(hint,self.hints[i]):
                self.hints.insert(i,hint)
                return
        self.hints.append(hint)
    def comes_before(self,hint1,hint2):
        if hint1[2]=="Across":
            if hint2[2]=="Down":
                return True
        if hint1[2]=="Down":
            if hint2[2]=="Across":
                return False
        if hint1[1]<hint2[1]:
            return True
        if hint1[1]>hint2[1]:
            return False
        return hint1[0]<hint2[0]
    def create(self,words):
        self.insertFirstWord(words)
        #print "==============================================================="
        while True:
            if len(words)==0:
                return
            done = False
            #print "---------------------------------"
            for x in range(8):
                if not(done):
                    i = random.randint(0,len(words)-1)
                    done = self.addWordDown(words[i])
                    if done:
            #            print "  Down:  ",x,words[i].string
                        words.remove(words[i])
            #        else:
            #            print "  Failed  ",words[i].string
            #if not(done):
            #    print "  Down:  no"
            if len(words)==0:
                return
            done2 = False
            for x in range(8):
                if not(done2):
                    i = random.randint(0,len(words)-1)
                    done2 = self.addWordAcross(words[i])
                    if done2:
            #            print "  Across:",x,words[i].string
                        words.remove(words[i])
            #        else:
            #            print "  Failed  ",words[i].string
            #if not(done2):
            #    print "  Across: no"
            if not(done) and  not(done2):
                return
    def insertFirstWord(self,words):
        bigwords = [word for word in words if len(word.string)>7]
        i = random.randint(0,len(bigwords)-1)
        self.placeFirstWord(bigwords[i])
        words.remove(bigwords[i])
    def placeFirstWord(self,word):
        y = self.size/2
        x = (self.size-len(word.string))/2
        self.setWordAcross(x,y,word)
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

class PuzzleGrid(spyral.Sprite):
    def __init__(self,cross,group):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.gridsize = cross.size
        self.grid = [[not(cross.lettergrid[x][y]=='') for y in range(cross.size)]
                     for x in range(cross.size)]
        self.letters = 0
        self.pos = PUZZLE_POS
        for y in range(cross.size):
            for x in range(cross.size):
                if self.grid[x][y]:
                    self.letters+=1
        self.render()
        self.hint = None
    def setHint(self,hint):
        if self.hint==hint:
            return
        self.render()
        if not(self.hint==None):
            self.paintHint(self.hint,[192,192,255,255])
        self.paintHint(hint,[255,255,128,255])
        self.hint = hint
    def paintHint(self,hint,color):
        x = hint[0]
        y = hint[1]
        dx = 0
        dy = 1
        if hint[2]=="Across":
            dx = 1
            dy = 0
        for i in range(len(hint[3])):
            self.image.draw_rect(color,[(x+i*dx)*BLOCK_SIZE+1,(y+i*dy)*BLOCK_SIZE+1],
                                 [BLOCK_SIZE-1,BLOCK_SIZE-1])
    def render(self):
        self.image = spyral.Image(size=[self.gridsize*BLOCK_SIZE+1,self.gridsize*BLOCK_SIZE+2])
        for y in range(self.gridsize):
            for x in range(self.gridsize):
                if self.grid[x][y]:
                    self.image.draw_rect([0,0,0,255],[x*BLOCK_SIZE,y*BLOCK_SIZE],
                                         [BLOCK_SIZE+1,BLOCK_SIZE+1],1)
                    self.image.draw_rect([192,192,255,255],[x*BLOCK_SIZE+1,y*BLOCK_SIZE+1],
                                         [BLOCK_SIZE-1,BLOCK_SIZE-1])
    def update(self,dt):
        pass

class HintAndAnswer(spyral.Sprite):
    def __init__(self,group,size,hint):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.font = pygame.font.SysFont(None,30)
        self.pos = [60,700]
        self.anchor = 'topleft'
        self.hint = None
        self.setHint(hint)


    def setHint(self,hint):
        if self.hint==hint:
            return
        self.hint = hint
        self.answer = ""
        self.answerIndex = 0
        for i in range(len(hint[3])):
            self.answer += "_ "
        self.render()


    def typeKey(self,letter):
        if self.answerIndex==len(self.answer):
            return
        self.answer = self.answer[0:self.answerIndex]+letter+self.answer[self.answerIndex+2:]
        self.answerIndex+=1
        self.render()


    def deleteKey(self):
        if self.answerIndex==0:
            return
        self.answer = self.answer[0:self.answerIndex-1]+"_ "+self.answer[self.answerIndex:]
        self.answerIndex-=1
        self.render()


    def render(self):
        self.image = spyral.Image(size = [WIDTH,60])
        surf = self.font.render(self.hint[4],True,[0,0,0,255])
        self.image._surf.blit(surf,[2,0])
        surf = self.font.render(self.answer,True,[0,0,0,255])
        self.image._surf.blit(surf,[22,28])

class WordBank(spyral.Sprite):
    def __init__(self,group,hints):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        hintlist = [hint for hint in hints]
        self.words = []
        while len(hintlist)>0:
            n = len(hintlist)
            i = random.randint(0,n-1)
            self.words.append(hintlist[i][3])
            hintlist.remove(hintlist[i])
        self.pos = [790,50]
        self.font = pygame.font.SysFont(None,30)
        self.render()
    def render(self):
        self.image = spyral.Image(size = [300,HEIGHT-100])
        for i in range(len(self.words)):
            surf = self.font.render(self.words[i],True,[0,0,0,255])
            self.image._surf.blit(surf,[150-surf.get_width()/2,30*i+20])
        

class AnswerGrid(spyral.Sprite):
    def __init__(self,group,font,size):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.font = font
        self.gridsize = size
        self.grid = [['' for y in range(size)] for x in range(size)]
        self.letters = 0
        self.pos = PUZZLE_POS
        self.render()
    def setAnswer(self,hint):
        changed = False
        X = hint[0]
        Y = hint[1]
        dx = 0
        dy = 1
        if hint[2]=="Across":
            dx = 1
            dy = 0
        for i in range(len(hint[3])):
            x = X+dx*i
            y = Y+dy*i
            if not(self.grid[x][y]==hint[3][i]):
                changed = True
                self.grid[x][y] = hint[3][i]
                self.letters+=1
        if changed:
            self.render()
    def render(self):
        self.image = spyral.Image(size=[self.gridsize*BLOCK_SIZE,self.gridsize*BLOCK_SIZE])
        for y in range(self.gridsize):
            for x in range(self.gridsize):
                if not(self.grid[x][y]==''):
                    surf = self.font.render(self.grid[x][y],True,[0,0,0,255])
                    self.image._surf.blit(surf,[(x+.5)*BLOCK_SIZE-surf.get_width()/2+.5,
                                                (y+.5)*BLOCK_SIZE-surf.get_height()/2+.5])
        
class CrosswordMain(spyral.Scene):
    """
    this will be the actual scene that the crossword is run on.
    """
    def __init__(self, passed_in_pet):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT),layers = ["__default__","top"])
        self.group = spyral.Group(self.camera)
        words = readWords("wordlist.txt")
        cross = Crossword(15,words)
        self.font = pygame.font.SysFont(None,LETTERFONT)
        self.grid = PuzzleGrid(cross,self.group)
#        for hint in cross.hints:
#            print hint[0],hint[1],hint[2],hint[3],hint[4]
        self.grid.setHint(cross.hints[0])
        self.hintAndAnswer = HintAndAnswer(self.group,cross.size,cross.hints[0])
        self.answergrid = AnswerGrid(self.group,self.font,cross.size)
        self.hintNum = 0
        self.hints = cross.hints
        self.hintDone = [False for hint in self.hints]
        self.answergrid._set_layer("top")
        self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        WordBank(self.group,cross.hints)
        self.pet = passed_in_pet
        self.pet.x = 950
        self.pet.y = 750
        self.group.add(self.pet)

    
    def on_enter(self):
        bg = spyral.Image(filename = "images/crossword_puzzle/background.png")
        font = pygame.font.SysFont(None,30)
        surf = font.render("Arrow Keys/Tab Key: Select a different part of the crossword.",True,[0,0,0,255])
        bg._surf.blit(surf,[60,760])
        surf = font.render("Letter Keys: Type in the answer",True,[0,0,0,255])
        bg._surf.blit(surf,[60,780])
        surf = font.render("Backspace: Delete a letter you typed.",True,[0,0,0,255])
        bg._surf.blit(surf,[60,800])
        surf = font.render("Enter: If you have the right answer, put it into the puzzle.",True,[0,0,0,255])
        bg._surf.blit(surf,[60,820])
        self.camera.set_background(bg)
        
    def render(self):
        self.group.draw()
        
    def currentHint(self):
        return self.hints[self.hintNum]
        
    def update(self,dt):
        self.group.update(dt)
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                self.pet.get_last_posn()
                return
            if event['type'] == 'KEYDOWN':
                if event['key']==274 or event['key']==275 or event['key']==9:
                    self.hintNum = (self.hintNum+1)%len(self.hints)
                    while self.hintDone[self.hintNum]:
                        self.hintNum = (self.hintNum+1)%len(self.hints)
                if event['key']==273 or event['key']==276:
                    self.hintNum = (self.hintNum-1)%len(self.hints)
                    while self.hintDone[self.hintNum]:
                        self.hintNum = (self.hintNum-1)%len(self.hints)
                if event['key']>=97 and event['key']<=122:
                    letter = self.alpha[event['key']-97]
                    self.hintAndAnswer.typeKey(letter)
                if event['key']==8:
                    self.hintAndAnswer.deleteKey()
                if event['key']==13:
                    if self.currentHint()[3]==self.hintAndAnswer.answer:
                        self.answergrid.setAnswer(self.currentHint())
                        self.hintDone[self.hintNum] = True
                        if self.answergrid.letters==self.grid.letters:
                            spyral.director.pop()
                            spyral.director.push(CrosswordVictory(self.pet))
                            return
                self.hintAndAnswer.setHint(self.currentHint())
                self.grid.setHint(self.currentHint())

class CrosswordVictory(spyral.Scene):
    def __init__(self, passed_in_pet):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT),layers = ["__default__","top"])
        self.group = spyral.Group(self.camera)

        self.pet = passed_in_pet
        self.pet.current_clue += 1
        self.pet.money += 100


    def on_enter(self):
        bg = spyral.Image(size=(WIDTH,HEIGHT))
        bg.fill(BG_COLOR)
        font = pygame.font.SysFont(None,80)
        surf = font.render("YOU DID IT!!!",True,[255,255,0,255])
        bg._surf.blit(surf,[(WIDTH-surf.get_width())*.5,(HEIGHT-surf.get_height())*.5-40])
        surf = font.render("You Earned 100 Chester Points!!!",True,[255,255,0,255])
        bg._surf.blit(surf,[(WIDTH-surf.get_width())*.5,(HEIGHT-surf.get_height())*.5+40])
        self.camera.set_background(bg)


    def update(self,dt):
        for event in self.event_handler.get():
            if event['type'] == 'KEYDOWN':
                if event['key'] == 27 or event['key'] == 13:
                    # esc or enter
                    spyral.director.pop()
                    self.pet.get_last_posn()
                    return
