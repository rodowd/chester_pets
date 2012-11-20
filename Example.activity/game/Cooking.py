#!/usr/bin/python
'''
Ryan O'Dowd, Kevin Touhey, and Yifan Hong
CISC 374
Fall 2012
'''

__doc__ = ''' # @TODO: '''

import pygame
import random
import spyral
#import nom_nom

UNIT_CONV = [3,16,2]
UNIT_CONV_2 = [1,3,48,96]

class Fraction:
    def __init__(self,numer,denom):
        self.numer = numer
        self.denom = denom
    def add(self,other):
        return Fraction(self.numer*other.denom+self.denom*other.numer,
                        other.denom*self.denom).simplify()
    def mult(self,num):
        return Fraction(self.numer*num,self.denom).simplify()
    def divide(self,num):
        return Fraction(self.numer,num*self.denom).simplify()
    def simplify(self):
        if self.numer==0:
            return Fraction(0,1)
        x = gcd(self.numer,self.denom)
        return Fraction(self.numer/x,self.denom/x)
    def sameFrac(self,other):
        return self.numer==other.numer and self.denom==other.denom
    def __str__(self):
        if self.denom==1:
            return self.numer.__str__()
        return self.numer.__str__()+"/"+self.denom.__str__()

class Recipe:
    def __init__(self, measurements, ingredients):
        self.measures = measurements
        self.ingredients = ingredients
    def get_frac_tsp(self,measure):
        f = measure.frac
        if measure.tool=="tsp.":
            return f
        if measure.tool=="tbsp.":
            return f.mult(3)
        if measure.tool=="cup":
            return f.mult(48)
        return f.mult(96)
    def add(self, measure, ingred):
        for i in range(len(self.ingredients)):
            if self.ingredients[i]==ingred:
                self.measures[i] = Measurement(self.get_frac_tsp(self.measures[i]).add(self.get_frac_tsp(measure)),"tsp.")
    def sameRecipe(self,other):
        for i in range(len(self.measures)):
            if not(other.get_frac_tsp(other.measures[i]).sameFrac(self.get_frac_tsp(self.measures[i]))):
                print self.ingredients[i],": ",self.measures[i]," vs. ",other.ingredients[i],": ",other.measures[i]
                return False
        return True
    def __str__(self):
        string = ""
        for i in range(len(self.measures)):
            string+=self.measures[i].__str__()+" of "+self.ingredients[i].__str__()+"\n"
        return string

class Ingredient(spyral.Sprite):
    def __init__(self,group,name,filename,x,y):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.name = name
        self.filename = filename
        self.pos = [x,y]
        self.render()
    def render(self):
        self.image = spyral.Image(filename="cooking_images/"+self.filename)
    def __str__(self):
        return self.name

class Measurement:
    def __init__(self,frac,tool):
        self.frac = frac
        self.tool = tool # "tsp.", "tbsp.", "cup", "pint"
    def __str__(self):
        return self.frac.__str__()+" "+self.tool

def gcd(a,b):
    if b<a:
        return gcd(b,a)
    num = 1
    x = 2
    while x<=a:
        if b%x==0 and a%x==0:
            num*=x
            b/=x
            a/=x
        else:
            x+=1
    return num

def random_tool(tool):
    denom = random.randint(2,4)
    if denom>=5:
        denom+=1
    #numer = denom
    numer = random.randint(1,denom-1)
    frac = Fraction(numer,denom)
    return Measurement(frac,tool)

def random_recipe(measures,ingredients):
    meas = []
    for ingred in ingredients:
        toolnum = random.randint(0,1)*2
        numtools1 = random.randint(1,3)
        numtools2 = random.randint(1,2)
        frac = measures[toolnum].frac.mult(numtools1)
        frac = frac.add(measures[toolnum+1].frac.mult(numtools2).mult(UNIT_CONV[toolnum]))
        meas.append(Measurement(frac,measures[toolnum].tool))
    return Recipe(meas,ingredients)

CK_WIDTH = 640
CK_HEIGHT = 480

class CookingMain(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (CK_WIDTH,CK_HEIGHT),layers = ['__default__','tool'])
        self.group = spyral.Group(self.camera)
        self.tools = [random_tool("tsp."),
                      random_tool("tbsp."),
                      random_tool("cup"),
                      random_tool("pint")]
        self.ingredients = [Ingredient(self.group,"flour","FLOUR.png",230,10),
                            Ingredient(self.group,"sugar","SUGAR.png",230,170),
                            Ingredient(self.group,"chocolate","CHOCOLATE.png",230,330),
                            Ingredient(self.group,"water","WATER.png",350,10),
                            Ingredient(self.group,"eggs","EGG.png",350,170),
                            Ingredient(self.group,"butter","BUTTER.png",350,330)]
        recipeSprite = self.addImage("cooking_images/RECIPE_SCROLL.png",112,125)
        self.emptyBG = spyral.Sprite(self.group)
        self.emptyBG.image = spyral.Image(size=[CK_WIDTH,CK_HEIGHT])
        self.group.add(self.emptyBG)
        self.font = pygame.font.SysFont(None,20)
        self.recipe = random_recipe(self.tools,self.ingredients)
        recipelist = self.recipe.__str__().split("\n")
        bigfont = pygame.font.SysFont(None,40)
        recipeTitle = bigfont.render("COOKIES",True,[0,0,0,255]).convert_alpha()
        recipeSprite.image._surf.blit(recipeTitle,[30,10])
        for i in range(len(recipelist)):
            recipe = recipelist[i]
            surf = self.font.render(recipe,True,[0,0,0,255]).convert_alpha()
            recipeSprite.image._surf.blit(surf,[max(max(15,20-5*i),5*i-5),50+25*i])
        self.bowl = Recipe([Measurement(Fraction(0,1),"tsp.") for ingred in self.ingredients],self.ingredients)
        self.tsp = self.addImage("cooking_images/TEA_SPOON.png",65,285,'tool')
        self.tbsp = self.addImage("cooking_images/TBL_SPOON.png",165,285,'tool')
        self.cup = self.addImage("cooking_images/MEASURING_CUP2.png",65,395,'tool')
        self.pint = self.addImage("cooking_images/MEASURING_CUP.png",165,395,'tool')
        self.toolSprites = [self.tsp,self.tbsp,self.cup,self.pint]
        self.addImage("cooking_images/BOWL.png",545,225)
        for i in range(4):
            tool = self.tools[i]
            x = 65+100*(i%2)
            y = 310
            if i>1: y+=130
            self.addText(tool.__str__(),x,y)
        for i in range(6):
            ingred = self.ingredients[i]
            string = ingred.name
            string = string[0].upper()+string[1:]
            x = 280
            if i>2: x+=120
            y = 150*(i%3)+130
            self.addText(string,x,y)
        self.toolSelect = 0
        self.pointer1 = self.addImage("cooking_images/SPOINTER.png",65,330)
        self.ingredSelect = 0
        self.pointer3 = self.addImage("cooking_images/SPOINTER.png",545,320)
        self.group.remove(self.pointer3)
        self.curTool = None
        self.state = 0
    def addText(self,string,x,y):
        surf = self.font.render(string,True,[0,0,0,255]).convert_alpha()
        y = y-surf.get_height()/2
        x = x-surf.get_width()/2
        self.emptyBG.image._surf.blit(surf,[x,y])
    def addImage(self,filename,x,y,layer = "__default__"):
        sprite = spyral.Sprite(self.group)
        sprite._set_layer(layer)
        sprite.image = spyral.Image(filename=filename)
        sprite.pos = [x,y]
        sprite.anchor = 'center'
        self.group.add(sprite)
        return sprite
    def render(self):
        self.group.draw()
    def movePointer(self,key):
        if self.state==0:
            if key<275:
                self.toolSelect = (self.toolSelect+2)%4
            elif self.toolSelect < 2:
                self.toolSelect = 1 - self.toolSelect
            else:
                self.toolSelect = 5 - self.toolSelect
            self.setPointer1()
            return
        if self.state==1:
            num = 275-key
            if key>274:
                self.ingredSelect = (self.ingredSelect+3)%6
            elif self.ingredSelect < 3:
                self.ingredSelect = (self.ingredSelect+num)%3
            else:
                self.ingredSelect = (self.ingredSelect+num)%3+3
            self.setIngredPointer()
            return
    def setPointer1(self):
        self.pointer1.x = 65+100*((self.toolSelect)%2)
        if self.toolSelect<2:
            self.pointer1.y = 330
        else:
            self.pointer1.y = 460
    def setIngredPointer(self):
        self.curTool = self.toolSprites[self.toolSelect]
        self.curTool.x = 280
        if self.ingredSelect>2:
            self.curTool.x = 400
        self.curTool.y = 65+150*((self.ingredSelect)%3)
        
    def accept(self):
        if self.state==0:
            self.state = 1
            self.setIngredPointer()
            return
        if self.state==1:
            self.state = 2
            self.group.add(self.pointer3)
            return
        if self.state==2:
            self.bowl.add(self.tools[self.toolSelect],self.ingredients[self.ingredSelect])
    def cancel(self):
        if self.state==0:
            return
        if self.state==1:
            self.state = 0
            self.curTool.x = 65+100*(self.toolSelect%2)
            self.curTool.y = 285
            if self.toolSelect>1:
                self.curTool.y = 395
            return
        if self.state==2:
            self.state = 1
            self.group.remove(self.pointer3)
    def update(self,dt):
        if self.bowl.sameRecipe(self.recipe):
            print "YOU GOT THE CORRECT RECIPE!!!"
            spyral.director.pop()
            #spyral.director.push(nom_nom.Bake())
            return
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop() # Happens when someone asks the OS to close the program
                return
            if event['type'] == 'KEYDOWN':
                if event['key']==27:
                    spyral.director.pop()
                    #spyral.director.push(nom_nom.Bake())
                    return
                if event['key']>=273 and event['key']<=276:
                    self.movePointer(event['key'])
                if event['key']==13:
                    self.accept()
                if event['key']==8:
                    self.cancel()
    def on_enter(self):
        bg = spyral.Image(size=(CK_WIDTH,CK_HEIGHT))
        bg.fill([255,64,64,255])
        self.camera.set_background(bg)
    
