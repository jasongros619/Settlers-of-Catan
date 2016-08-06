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
        self.hexes=[]
        self.corners=[]
        self.roads=[]
    
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
        nums=([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
#        random.shuffle(nums)
        resource=(["wheat"]*4+["ore"]*3+["sheep"]*4+["wood"]*4+["brick"]*3+['desert'])
        ports=(["wheat","ore","sheep","wood","brick"]+["3"]*4)
        random.shuffle(nums)
        random.shuffle(resource)
        random.shuffle(ports)

        dice_ind = 0 #die-roll number index
        res_ind  = 0 #resource index
        port_ind  = 0 #port index

        #hex.type is intially (r)esource, (p)ort or '(s)ea'
        #hex.type is changed
        #from 'r' to 'wheat','ore','wheat','wood','brick','desert'
        #from 'p' to 'wheat'______________________'brick','3'
        for hex in self.hexes:
            #resource
            if hex.type=="r":
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
            if hex.type=="p":
                #set port commodity
                hex.type="ports-"+ports[port_ind]
                port_ind+=1


    #draws map using TURTLE. This should be replaced later
    #with a better graphics program
    def drawmap(self):
#        self.hexes[8].rob=True #for testing purposes

        
        for h in self.hexes:
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
        C=self.corners[cid]
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
        pos=turtle.pos() #turtle.pos()?
        c = self.corners[0]
        best_dist = 15
        id = -1
        for corn in self.corners:
            d=dist(x,y,corn.x,corn.y)
            if d < best_dist:
                best_dist = d
                id=corn.id
        return id

    #returns the id of the 'selected' corner if you can build there
    #-1 if you cannot
    def canSettle(self,x,y,pid,game,needConnect=True):
        id=self.selectCorn(x,y)
        if id==-1: #when you dont click near a corner
            return -1

        #check if you DONT have a road connected to the corner
        #when you need to have one (every time except setup)
        if (needConnect and ( id not in game.players[pid].corners )):
            print("You do not have a road connected to this point")
            return -1

        #check if there is a different settlement on the corner
        if self.corners[id].owner!=None:
            print("There is already a settlement there.")
            return -1

        #check if there are centers nearby
        nearby=False
        for c in self.corners[id].corners:
            if self.corners[c].owner!=None:
                nearby=True
                break
        if nearby:
            print("There is a settlement nearby")
            return -1

        #there are no restrictions
        return id

    
    def buildSettlement(self,x,y,pid,game,needConnect=False):
        pos=turtle.pos() #right function?
        cid=self.canSettle(x,y,pid,game,needConnect)
        if cid==-1:
            return -1
        #at this poind cid = the id of the corner

        player = game.players[pid]
        
        #add to corners if you are not already connected to corner
        if needConnect==False:
            if cid not in player.corners:
                player.corners.append(cid)
                
        #change the map so that it knows who now owns the corner
        self.corners[cid].owner=pid

        #add victory points
        player.vp+=1

        #add the settlement to the player
        player.settlements.append(cid)

        #drawit
        self.drawSettlement(cid, player.color)

        #aquire ports
        for Hex in [self.hexes[hex_id] for hex_id in self.corners[cid].hexes]:
            if Hex.type in ["ports-brick","ports-wheat","ports-wood","ports-sheep","ports-ore","ports-3"]:
                game.players[pid].ports[ Hex.type[6:] ]=True
        return cid

################
#ROAD FUNCTIONS#
################

    def drawRoad(self,id,color="white"):
        R=self.roads[id]
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
        for r in self.roads:
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
        if self.roads[id].owner!=None:
            print("There is already a road built here")
            return -1

        #check if you are connected to road (assuming you need to be)
        R=self.roads[id]
        if needConnect==None:
            needConnect=game.players[pid].corners
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
        R=self.roads[rid]
        player = game.players[pid]
        
        #add corners to player
        if R.ci1 not in player.corners:
            player.corners.append(R.ci1)
        if R.ci2 not in player.corners:
            player.corners.append(R.ci2)
        # set board's road's owner to player
        self.roads[rid].owner = pid
        # draw it
        self.drawRoad(rid, player.color)
        return rid
