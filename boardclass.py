from math import *
from basic_functions import *
from hexclass import *
from cornerclass import *
from roadclass import *

#uses the 3 .txt files
import cTurtle
import os
INF=float("inf")

class Board(object):
    #creates objects for each hex, corner, and road
    #reads files which tell objects what they are next to
    def __init__(self):
        self.hexes=[]
        self.corners=[]
        self.roads=[]
        self.hex_turtles=[]
        self.num_turtles=[None]*37
        for i in range(37):
            turt = cTurtle.Turtle('blank')
            turt.speed(10)
            turt.up()
            self.hex_turtles.append(turt)
        for i in range(37):
            turt = cTurtle.Turtle('blank')
            turt.speed(10)
            turt.up()
            self.num_turtles.append(turt)
        
        #hexes
        file=open("hexgraphs2.txt",'r')
        for line in file:
            line=line.split()
            for i in range(len(line)):
                if i!=3:
                    line[i]=int(line[i])
            obj=Hex(line)
            self.hexes.append(obj)
        file.close()
        
        #corners
        file=open("cornergraphs2.txt",'r')
        for line in file:
            line=line.split()
            for i in range(len(line)):
                line[i]=int(line[i])
            obj=Corner(line)
            self.corners.append(obj)
        file.close()
        
        #roads
        file=open("roadgraphs.txt",'r')
        for line in file:
            line=line.split()
            for i in range(len(line)):
                line[i]=int(line[i])
            obj=Road(line)
            self.roads.append(obj)

        #setup objects
        for road in self.roads:
            road.ci1    = self.corners[road.ci1]
            road.ci2    = self.corners[road.ci2]
            road.roads  =[ self.roads[id] for id in road.roads ]
            road.hexes  =[ self.hexes[id] for id in road.hexes ]
        for corn in self.corners:
            corn.roads  =[ self.roads[id] for id in corn.roads ]
            corn.hexes  =[ self.hexes[id] for id in corn.hexes ]
            corn.corners=[ self.corners[id] for id in corn.corners]
        for hex in self.hexes:
            hex.corners =[ self.corners[id] for id in hex.corners]
            hex.roads   =[ self.roads[id] for id in hex.roads]
            hex.hexes   =[ self.hexes[id] for id in hex.hexes]

    #gives players cards for their city/settlement(s)
    #next to hexes with the same number as 'num'
    def provide(self,num):
        for hex in self.hexes:
            if hex.num == num and hex.robber==False:
                for corn in hex.corners:
                    if corn.owner != None:
                        corn.owner.cards[hex.type] += corn.lvl

    #shuffles board
    def shuffle(self):
        for corn in self.corners:
            corn.ports = None
        
        nums=([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
#        random.shuffle(nums)
        resource=(["wheat"]*4+["ore"]*3+["sheep"]*4+["wood"]*4+["brick"]*3+['desert'])
        ports=(["wheat","ore","sheep","wood","brick"]+["3"]*4)
        random.seed()
        random.shuffle(nums)
        random.shuffle(resource)
        random.shuffle(ports)

        dice_ind = 0  #die-roll number index
        res_ind  = 0  #resource index
        port_ind  = 0 #port index

        main_resources = ["wheat","ore","wood","brick","sheep"]
        #hex.type is intially (r)esource, (p)ort or '(s)ea'
        #hex.type is changed
        #from 'r' to 'wheat','ore','wheat','wood','brick','desert'
        #from 'p' to 'wheat'______________________'brick','3'        
        for hex in self.hexes:
            #resource
            if hex.type in ["r","desert"]+main_resources:
                #set resource type
                hex.type=resource[res_ind]
                res_ind += 1
                #set dice number
                if hex.type!="desert":
                    hex.num=nums[dice_ind]
                    #self.num  <= ?
                    dice_ind += 1
                else:
                    hex.num = None
                    hex.rob = True
                
                
            #ports
            if hex.type in ["p","ports-3"] + ["ports-"+res for res in main_resources]:
                #set port commodity
                hex.type="ports-"+ports[port_ind]
                #inform neighbor corners
                for corn in hex.corners:
                    corn.ports = hex.type
                
                port_ind+=1

                

                


    #draws map using TURTLE. This should be replaced later
    #with a better graphics program
    def drawmap(self,turtle):
        # 'ERASE' existing a) Numbers b) Hexes
        for turt in self.num_turtles:
            #print(type(turt))
            if turt is not None:
                turt.shape('blank')
        for turt in self.hex_turtles:
            turt.shape('blank')
        
        
        for h in self.hexes:
            #Move turtles to positions
            turt = self.hex_turtles[ h.id ]
            filename = None
            if h.type=="s" or h.type[:5]=="ports":
                filename = "MediumWater.gif"
            elif h.type=="desert":
                filename = "raw_desert.gif"
                #filename = "MediumWater.gif"
            elif h.type=="sheep":
                filename = "raw_pasture.gif"
            elif h.type=="wood":
                filename = "raw_forest.gif"
            elif h.type=="brick":
                filename = "raw_brick.gif"
            elif h.type=="ore":
                filename = "raw_ore.gif"
            elif h.type=="wheat":
                filename = "raw_wheat.gif"

            if filename != None:
                path = os.path.dirname(__file__)
                filename = os.path.join(path,"Media/"+filename)
                turt.addshape(filename)
                turt.goto(h.x,h.y)
                turt.shape(filename)

            if h.type in ["sheep","wood","brick","ore","wheat"]:
                path = os.path.dirname(__file__)
                num = str(h.num)
                filename = os.path.join(path,"Media/new_"+num+".gif")
                if self.num_turtles[h.id] is None:
                    turt = cTurtle.Turtle('blank')
                    turt.up()
                    turt.speed(10)
                else:
                    turt = self.num_turtles[h.id]
                turt.addshape(filename)
                turt.goto(h.x,h.y)
                turt.shape(filename)
                self.num_turtles[h.id]=turt

        #turtle.up()
        #turtle.speed(10)
        #turtle.color("red")
        #for hex in self.hexes:
        #    if hex.num in [2,3,4,5,6,8,9,10,11,12]:
        #        turtle.goto( hex.x, hex.y-20)
        #        turtle.write(hex.num,False,"center",("Arial",30,"normal"))

        turtle.speed(10)
        drawRect(turtle,-380,260,120,120,"red")
        drawRect(turtle,-380,-380,120,120,"blue")
        drawRect(turtle,260,260,120,120,"green")
        drawRect(turtle,260,-380,120,120,"yellow")

        
        turtle.up()
        turtle.goto(-320,310)
        turtle.write("End Turn",False,"center",("Arial",20,"normal"))
        turtle.goto(320,310)
        turtle.write("Trade\n(No ports)",False,"center",("Arial",20,"normal"))
        turtle.goto(320,-380)
        turtle.write("Use\nDev\nCard\n(Not yet)",False,"center",("Arial",20,"normal"))
        turtle.goto(-320,-330)
        turtle.write("Buy\n(No dev)",False,"center",("Arial",20,"normal"))
        
        
        #add numbers somehow
        """
            turtle.color("black",color)
            turtle.begin_fill()
            drawhex(h)
            turtle.end_fill()
            turtle.up()
            turtle.goto(h.x,h.y-20)
            if h.num in [2,3,4,5,6,8,9,10,11,12]:
                turtle.setheading(0)
                if h.num==6 or h.num==8:
                    turtle.color("red")
                else:
                    turtle.color("black")
                turtle.write(h.num,False,"center",("Arial",30,"normal"))
        #"""
        #add robber
        """
            if h.rob:
                turtle.goto(h.x,h.y-30)
                turtle.setheading(0)
                turtle.color("black","black")
                turtle.begin_fill()
            turtle.circle(30)
            turtle.end_fill()
        #"""

##########################
#SELECT OBJECT FUNCTIONS #
# > Returns object closest to (x,y) input or None if not close
##########################

    #returns nearest corner object or None if none are close.
    def selectCorn(self,x,y):
        best_dist = 15
        id = -1
        for corn in self.corners:
            d=dist(x,y,corn.x,corn.y)
            if d < best_dist:
                best_dist = d
                id=corn.id
        if id == -1:
            return None
        else:
            return self.corners[id]

    #returns Road object of nearest road or None if none nearby
    def selectRoad(self,x,y):
        id=-1
        best=2 #radians

        #of each set of corners and the selected point, check what
        #forms the smallest triangle by checking which is the most obtuse
        #at the selected point's angle.
        for r in self.roads:
            ang=calcAng(x,y,r.c1,r.c2)
            if ang>best:
                best=ang
                id=r.id
        if id == -1:
            return None
        else:
            return self.roads[id]

    #returns nearest Hex object or None if none nearby.
    def selectHex(self,x,y,r=100):
        best_hex = None
        best_dist = r

        for hex in self.hexes:
            d = dist(x,y,hex.x,hex.y)
            if d < best_dist:
                best_dist = d
                best_hex = hex

        return best_hex

#"""

if __name__ == "__main__":
    b = Board()
    print("__init__")
    b.shuffle()
    print("shuffled")
    b.drawmap(cTurtle)
