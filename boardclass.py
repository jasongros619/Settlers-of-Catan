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

        dice_ind = 0 #die-roll number index
        res_ind  = 0 #resource index
        port_ind  = 0 #port index

        main_resources = ["wheat","ore","wood","brick","sheep"]
        #hex.type is intially (r)esource, (p)ort or '(s)ea'
        #hex.type is changed
        #from 'r' to 'wheat','ore','wheat','wood','brick','desert'
        #from 'p' to 'wheat'______________________'brick','3'        
        for hex in self.hexes:
            #reset if already done:
            
            #resource
            if hex.type in ["r","desert"]+main_resources:
                #set resource type
                hex.type=resource[res_ind]
                res_ind += 1
                #set dice number
                if hex.type!="desert":
                    hex.num=nums[dice_ind]
                    dice_ind+=1
                else:
                    hex.rob = True
            #ports
            if hex.type in ["p","ports-3"] + ["ports-"+res for res in main_resources]:
                #set port commodity
                hex.type="ports-"+ports[port_ind]
                #inform neighbor corners
                for cid in hex.corners:
                    self.corners[cid].ports = hex.type
                
                port_ind+=1

                

                


    #draws map using TURTLE. This should be replaced later
    #with a better graphics program
    def drawmap(self):
        if self.hex_turtles != []:
            for turt in self.hex_turtles:
                turt.shape('blank')
                x,y = abxy((0,0))
                turt.goto(x,y)
        else:
            self.hex_turtles = []
            for i in range(37):
                turt = cTurtle.Turtle()
                turt.shape('blank')
                turt.up()
                turt.speed(0)
                self.hex_turtles.append(turt)
                #for i in range(37)]
        
        for h in self.hexes:
            #Move turtles to positions
            turt = self.hex_turtles[ h.id ]
            filename = None
            if h.type=="s" or h.type[:5]=="ports":
                filename = "MediumWater.gif"
            elif h.type=="desert":
                pass
                #filename = "MediumWater.gif"
            elif h.type=="sheep":
                filename = "MediumPasture.gif"
            elif h.type=="wood":
                filename = "MediumForest.gif"
            elif h.type=="brick":
                filename = "MediumBrick.gif"
            elif h.type=="ore":
                filename = "MediumOre.gif"
            elif h.type=="wheat":
                filename = "MediumWheat.gif"

            if filename != None:
                path = os.path.dirname(__file__)
                filename = os.path.join(path,"Media/"+filename)
                turt.addshape(filename)
                turt.goto(h.x,h.y)
                turt.shape(filename)

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
