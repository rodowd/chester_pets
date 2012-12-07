#!/usr/bin/python
'''
Ryan O'Dowd, Kevin Touhey, and Yifan Hong
CISC 374
Fall 2012
'''

__doc__ = ''' The cooking minigame '''

import pygame
import random
import spyral
import nom_nom

WIDTH = 1200
HEIGHT = 900
UNIT_CONV = [3, 16, 2]
UNIT_CONV_2 = [1, 3, 48, 96]

class Fraction:
    def __init__(self, numer, denom):
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
        x = greatest_common_denominator(self.numer, self.denom)
        return Fraction(self.numer/x,self.denom/x)
    def sameFrac(self, other):
        return self.numer == other.numer and self.denom == other.denom
    def __str__(self):
        if self.denom == 1:
            return self.numer.__str__()
        return self.numer.__str__() + "/" + self.denom.__str__()


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
    def empty(self,other):
        for i in range(6):
            m = self.measures[i]
            if not(m.frac.sameFrac(other.measures[i].frac)):
                m.frac = Fraction(0,1)
    def add(self, measure, ingred):
        for i in range(len(self.ingredients)):
            if self.ingredients[i]==ingred:
                self.measures[i].frac = self.measures[i].frac.add(measure.convert_frac(self.measures[i].tool))
    def sameRecipe(self,other):
        for i in range(len(self.measures)):
            if not(other.get_frac_tsp(other.measures[i]).sameFrac(self.get_frac_tsp(self.measures[i]))):
                return False
        return True
    def __str__(self):
        string = ""
        for i in range(len(self.measures)):
            string+=self.measures[i].__str__()+" of "+self.ingredients[i].__str__()+"\n"
        return string

class BowlContents(spyral.Sprite):
    def __init__(self,group,recipe,recipe2):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.recipe = recipe
        self.target_fracs = [m.frac for m in recipe2.measures]
        self.font = pygame.font.SysFont(None,30)
        self.render()
    def render(self):
        self.image = spyral.Image(size=[400,400])
        self.pos = [700,100]
        string = self.recipe.__str__()
        strings = string.split("\n")
        for i in range(6):
            col = [0,0,0,255]
            if self.target_fracs[i].sameFrac(self.recipe.measures[i].frac):
                col = [64,255,64,255]
            surf = self.font.render(strings[i],True,col)
            self.image._surf.blit(surf,[0,40*i])
    def update(self,dt):
        pass

class Ingredient(spyral.Sprite):
    def __init__(self,group,name,filename,x,y):
        spyral.Sprite.__init__(self,group)
        self.group.add(self)
        self.name = name
        self.filename = filename
        self.pos = [x,y]
        self.render()
    def render(self):
        self.image = spyral.Image(filename=self.filename)
    def __str__(self):
        return self.name

class Measurement:
    def __init__(self,frac,tool):
        self.frac = frac
        self.tool = tool
    def convert_frac(self,tool):
        tools = ["tsp.", "tbsp.", "cup", "pint"]
        i = tools.index(self.tool)
        i2 = tools.index(tool)
        return self.frac.mult(UNIT_CONV_2[i]).divide(UNIT_CONV_2[i2])
    def __str__(self):
        return self.frac.__str__()+" "+self.tool

def greatest_common_denominator(a,b):
    if b < a:
        return greatest_common_denominator(b, a)
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


class Cooking(spyral.Scene):
    def __init__(self, passed_in_pet):
        spyral.Scene.__init__(self)
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH,HEIGHT),layers = ['__default__','tool'])
        self.group = spyral.Group(self.camera)
        self.tools = [random_tool("tsp."),
                      random_tool("tbsp."),
                      random_tool("cup"),
                      random_tool("pint")]
        self.ingredients = [Ingredient(self.group, "flour", "images/cooking/flour.png", 230, 10),
                            Ingredient(self.group, "sugar", "images/cooking/sugar.png", 230, 170),
                            Ingredient(self.group, "chocolate", "images/cooking/chocolate.png", 230, 330),
                            Ingredient(self.group, "water", "images/cooking/water.png", 350, 10),
                            Ingredient(self.group, "eggs", "images/cooking/eggs.png", 350, 170),
                            Ingredient(self.group, "butter", "images/cooking/butter.png", 350, 330)]
        recipeSprite = self.addImage("images/cooking/recipe_scroll.png", 112, 125)
        self.emptyBG = spyral.Sprite(self.group)
        self.emptyBG.image = spyral.Image(size=[WIDTH,HEIGHT])
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
        for i in range(6):
            self.bowl.measures[i].tool = self.recipe.measures[i].tool
        self.tsp = self.addImage("images/cooking/teaspoon.png", 65, 285, 'tool')
        self.tbsp = self.addImage("images/cooking/tablespoon.png", 165, 285, 'tool')
        self.cup = self.addImage("images/cooking/measuring_cup1.png", 65, 395, 'tool')
        self.pint = self.addImage("images/cooking/measuring_cup2.png", 165, 395, 'tool')
        self.toolSprites = [self.tsp, self.tbsp, self.cup, self.pint]
        self.addImage("images/cooking/bowl.png", 545, 150)
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
        self.pointer1 = self.addImage("images/cooking/pointer.png", 65, 330)
        self.ingredSelect = 0
        self.pointer3 = self.addImage("images/cooking/pointer.png", 545, 250)
        self.group.remove(self.pointer3)
        self.curTool = None
        self.state = 0

        self.pet = passed_in_pet
        self.pet.x = 500
        self.pet.y = 500
        self.group.add(self.pet)
        self.bowlcontents = BowlContents(self.group,self.bowl,self.recipe)

        
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
            self.bowlcontents.render()
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
            self.pet.money += 100
            spyral.director.replace(nom_nom.Bake(self.pet))
            return
        for event in self.event_handler.get():
            if event['type'] == 'KEYDOWN':
                if event['key']>=273 and event['key']<=276:
                    self.movePointer(event['key'])
                if event['key']==13:
                    self.accept()
                if event['key']==8:
                    self.cancel()
                if event['key']==27:
                    self.bowl.empty(self.recipe)
                    self.bowlcontents.render()
    def on_enter(self):
        bg = spyral.Image(size=(WIDTH,HEIGHT))
        bg.fill([255,64,64,255])
        font = pygame.font.SysFont(None,40)
        surf = font.render("Arrow Keys: Move pointer.",True,[0,0,0,255])
        bg._surf.blit(surf,[10,600])
        surf = font.render("Enter Key: Select Tool/Ingredient or add to the bowl.",True,[0,0,0,255])
        bg._surf.blit(surf,[10,650])
        surf = font.render("Backspace: Go back to tool or ingredient selection.",True,[0,0,0,255])
        bg._surf.blit(surf,[10,700])
        surf = font.render("Escape: Remove unfinished ingredients from the bowl.",True,[0,0,0,255])
        bg._surf.blit(surf,[10,750])
        self.camera.set_background(bg)

"""
class CookingVictory(spyral.Scene):
    def __init__(self,passed_in_pet):
        spyral.Scene.__init__(self)
        self.pet = passed_in_pet
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH,HEIGHT),layers = ['__default__','tool'])
        self.group = spyral.Group(self.camera)
        self.pet.current_clue+=1
    
    def on_enter(self):
        bg = spyral.Image(size=(WIDTH,HEIGHT))
        bg.fill([255,64,64,255])
        font = pygame.font.SysFont(None,80)
        surf = font.render("DELICIOUS!!!",True,[255,255,0,255])
        bg._surf.blit(surf,[(WIDTH-surf.get_width())*.5,(HEIGHT-surf.get_height())*.5])
        self.camera.set_background(bg)

    def update(self,dt):
        for event in self.event_handler.get():
            if event['type'] == 'QUIT':
                spyral.director.pop()
                self.pet.get_last_posn()
                return
            if event['type'] == 'KEYDOWN':
                if event['key'] == 27 or event['key'] == 13:
                    # esc or enter
                    spyral.director.pop()
                    self.pet.get_last_posn()
                    return
"""
