import random

SHAPES = ["Square","Circle","Triangle1","Triangle2","Triangle3","Triangle4","Diamond"]

class Clue:
    def __init__(self,last_town):
        towns = ["Hong Kong","Touheyville","O'dowd Shire"]
        towns.remove(last_town)
        self.town = towns[random.randint(0,1)]
        self.number = random.randint(30,46)
        if self.town=="O'dowd Shire":
            self.number = random.randint(30,45)
        self.set_number_clue()
        self.shape = SHAPES[random.randint(0,6)]
        self.set_shape_clue()
    def set_number_clue(self):
        clue = random.randint(1,4)
        nums = []
        a = random.randint(2,7)
        b = random.randint(1,a-1)
        if clue==1:
            nums = [a*i for i in range(5)]
        elif clue==2:
            nums = [-a*i for i in range(5)]
        elif clue==3:
            nums = [0,a,a+b,2*a+b,2*a+2*b]
        else:
            nums = [0,a,a-b,2*a-b,2*a-2*b]
        self.find_place(nums)
    def find_place(self,nums):
        place = random.randint(1,3)
        add = self.number-nums[place]
        self.number_clue = ""
        for i in range(5):
            if i==place:
                self.number_clue+="?"
            else:
                self.number_clue+=(nums[i]+add).__str__()
            self.number_clue+=","
        self.number_clue = self.number_clue[0:-1]
    def set_shape_clue(self):
        place = random.randint(0,5)
        shapes = [shape for shape in SHAPES if not(shape==self.shape)]
        shape2 = SHAPES[random.randint(0,6)]
        shape3 = shapes[random.randint(0,5)]
        shapelist = [0,0,0,0,0,0]
        shapelist[place] = "?"
        shapelist[(place+1)%6] = shape2
        shapelist[(place+2)%6] = shape3
        shapelist[(place+3)%6] = self.shape
        shapelist[(place+4)%6] = shape2
        shapelist[(place+5)%6] = shape3
        self.shape_clue = shapelist
    def __str__(self):
        z = self.town+":\n  "+self.number.__str__()+": "+self.number_clue
        z+="\n  "+self.shape+": "
        for shape in self.shape_clue:
            z+=shape+","
        return z

print Clue("Hong Kong")
