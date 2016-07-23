from math import *
from basic_functions import *
from hexclass import *
from cornerclass import *
from roadclass import *
#uses the 3 .txt files
import turtle
INF=float("inf")

class Board(object):
    #creates objects for each hex, corner, and road
    #reads files which tell objects what they are next to
    def __init__(self):
        self.hex=[]
        self.corn=[]
        self.road=[]
    
        #hexes
        file=open("hexgraphs2.txt",'r')
        for line in file:
            line=line.split()
            for i in range(len(line)):
                if i!=3:
                    line[i]=int(line[i])
            obj=Hex(line)
            self.hex.append(obj)
        file.close()
        
        #corners
        file=open("cornergraphs2.txt",'r')
        for line in file:
            line=line.split()
            for i in range(len(line)):
                line[i]=int(line[i])
            obj=Corner(line)
            self.corn.append(obj)
        file.close()
        
        #roads
        file=open("roadgraphs.txt",'r')
        for line in file:
            line=line.split()
            for i in range(len(line)):
                line[i]=int(line[i])
            obj=Road(line)
            self.road.append(obj)


    #shuffles board
    def shuffle(self):
        nums=([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
        random.shuffle(nums)
        resource=(["wheat"]*4+["ore"]*3+["sheep"]*4+["wood"]*4+["brick"]*3+['desert'])
        ports=(["wheat","ore","sheep","wood","brick"]+["3"]*4)
        random.shuffle(nums)
        random.shuffle(resource)
        random.shuffle(ports)
        n=0
        r=0
        p=0
        for i in range(len(self.hex)):
            t=self.hex[i].type
            if t=="r":
                self.hex[i].type=resource[r]
                r+=1
                if self.hex[i].type!="desert":
                    self.hex[i].num=nums[n]
                    n+=1
            if t=="p":
                self.hex[i].type="ports-"+ports[p]
                p+=1

    #draws map using TURTLE. This should be replaced later
    #with a better graphics program
    def drawmap(self):
        self.hex[8].rob=True #for testing purposes

        
        for h in self.hex:
            if h.type=="s" or h.type[:5]=="ports":
                color="cyan"
            elif h.type=="desert":
                color="orange"
            elif h.type=="sheep":
                color="lime"
            elif h.type=="wood":
                color="green"
            elif h.type=="brick":
                color="brown"
            elif h.type=="ore":
                color="grey"
            elif h.type=="wheat":
                color="yellow"
            else:
                color="black"
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
            if h.rob:
                turtle.goto(h.x,h.y-30)
                turtle.setheading(0)
                turtle.color("black","black")
                turtle.begin_fill()
                turtle.circle(30)
                turtle.end_fill()

######################
#SETTLEMENT FUNCTIONS#
######################

    def drawSettlement(self,cid,color="red"):
        C=self.corn[cid]
        R=15
        turtle.color("black",color)
        
        turtle.up()
        turtle.goto(C.x+R,C.y-R)
        turtle.down()
        turtle.begin_fill()
        turtle.goto(C.x+R,C.y+R)
        turtle.goto(C.x-R,C.y+R)
        turtle.goto(C.x-R,C.y-R)
        turtle.goto(C.x+R,C.y-R)
        turtle.end_fill()
        
        
    #returns the id of the nearest corner
    #or -1 if nothing nearby
    def selectCorn(self,x,y):
        pos=turtle.pos()
        c=self.corn[0]
        bestd=15
        id=-1
        for i in range(len(self.corn)):
            d=dist(x,y,self.corn[i].x,self.corn[i].y)
            if d<bestd:
                bestd=d
                id=self.corn[i].id
        return id

    #returns the id of the 'selected' corner if you can build there
    #-1 if you cannot
    def canSettle(self,x,y,pid,game,needConnect=True):
        id=self.selectCorn(x,y)
        if id==-1: #when you dont click near a corner
            return -1

            
        #check if you DONT have a road connected to the corner
        #when you need to have one (every time except setup)
        if (needConnect and ( id not in game.players[pid].corn )):
            print("You do not have a road connected to this point")
            return -1

        #check if there is a different settlement on the corner
        if self.corn[id].owner!=None:
            print("There is already a settlement there.")
            return -1

        #check if there are centers nearby
        nearby=False
        for c in self.corn[id].corn:
            if self.corn[c].owner!=None:
                nearby=True
                break
        if nearby:
            print("There is a settlement nearby")
            return -1

        #there are no restrictions
        return id

    
    def buildSettlement(self,x,y,pid,game,needConnect=False):
        pos=turtle.pos
        cid=self.canSettle(x,y,pid,game,needConnect)
        if cid==-1:
            return -1
        #at this poind cid = the id of the corner
        
        #add to corners if you are not already connected to corner
        if needConnect==False:
            if cid not in game.players[pid].corn:
                game.players[pid].corn.append(cid)
                
        #change the map so that it knows who now owns the corner
        self.corn[cid].owner=pid

        #add victory points
        game.players[pid].vp+=1

        #add the settlement to the player
        game.players[pid].settlements.append(cid)

        #drawit
        self.drawSettlement(cid, game.players[pid].color)

        #aquire ports
        for H in self.corn[cid].hexes:
            if self.hex[H].type in ["ports-brick","ports-wheat","ports-wood","ports-sheep","ports-ore","ports-3"]:
                game.players[pid].ports[ self.hex[H].type[6:] ]=True
        return cid

################
#ROAD FUNCTIONS#
################

    def drawRoad(self,id,color="white"):
        R=self.road[id]
        p1=abxy( R.c1 )
        p2=abxy( R.c2 )
        turtle.up()
        turtle.goto( p1[0],p1[1] )
        turtle.down()
        turtle.color("black")
        turtle.pensize( 9 )
        turtle.goto( p2[0], p2[1] )
        turtle.pensize(5)
        turtle.color(color)
        turtle.goto( p1[0], p1[1] )
        turtle.pensize( 1 )

    #returns id of closest road
    #-1 if none are close
    def selectRoad(self,x,y):
        id=-1
        best=2 #radians

        #of each set of corners and the selected point, check what
        #forms the smallest triangle by checking which is the most obtuse
        #at the selected point's angle.
        for r in self.road:
            ang=calcAng(x,y,r.c1,r.c2)
            if ang>best:
                best=ang
                id=r.id
        return id

    #returns id of selected road if you can build
    #-1 if you cant
    def canRoad(self,x,y,pid,game,needConnect):
        id=self.selectRoad(x,y)
        if id==-1: #when no road
            return -1

        #check if a road is already there
        if self.road[id].owner!=None:
            print("There is already a road built here")
            return -1

        #check if you are connected to road (assuming you need to be)
        R=self.road[id]
        if needConnect==None:
            needConnect=game.players[pid].corn
        #assume you have a list [x_i , ... , x_n ]
        if not ( R.ci1 in needConnect or R.ci2 in needConnect):
            if game.round==0 or game.round==1:
                print("You must place a road connected to your newest settlement.")
            else:
                print("You do not have a road connected to this point")
            return -1

        #there are no restrictions
        return id

    #build road if possible
    #returns -1 if not possible or the road's id if possible
    def buildRoad(self,x,y,pid,game,needConnect):
        #find the id of the road
        #return -1 if you cant build road
        #set R = the road
        rid=self.canRoad(x,y,pid,game,needConnect)
        if rid==-1:
            return -1
        R=self.road[rid]
        
        #add corners to player
        if R.ci1 not in game.players[pid].corn:
            game.players[pid].corn.append(R.ci1)
        if R.ci2 not in game.players[pid].corn:
            game.players[pid].corn.append(R.ci2)
        # set board's road's owner to player
        self.road[rid].owner=pid
        # draw it
        self.drawRoad(rid, game.players[pid].color)
        return rid
