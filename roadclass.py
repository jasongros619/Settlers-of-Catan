
from basic_functions import abxy

class Road(object):
    def __init__(self,data):
        self.id=data[0]
        self.c1=(data[1],data[2])   #(a,b) of 1st corner
        self.c2=(data[3],data[4])   #(a,b) of 2nd corner
        self.p1=abxy( self.c1 )     #(x,y) of 1st corner
        self.p2=abxy( self.c2 )     #(x,y) of 2nd corner
        self.ci1=data[5]            #corner 1 id
        self.ci2=data[6]            #corner 2 id
        self.x=(self.p1[0]+self.p2[0])/2 #x coordinate of midpoint
        self.y=(self.p1[1]+self.p2[1])/2 #y coordinate of midpoint

        #ids of nearby roads
        self.roads=[]
        for r in data[7:13]:
            if r==-1:
                break
            self.roads.append(r)

        #ids of nearby hexes
        self.hexes=[]
        for h in data[13:19]:
            if h==-1:
                break
            self.hexes.append(h)
        self.owner=None

    def drawRoad(self,turtle,color="white"):
        p1=abxy( self.c1 )
        p2=abxy( self.c2 )
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
    
    def canRoad(self,player,corner_id=None):

        #check if a road is already there
        if self.owner!=None:
            print("There is already a road built here.")
            return False

        #regular turn
        if corner_id == None:
            if not(self.ci1.id in player.corners or self.ci2.id in player.corners):
                print("You do not have a road connected to this point.")
                return False
        #setup round
        else:
            if not(self.ci1.id == corner_id or self.ci2.id == corner_id):
                print("You must place a road connected to your newest settlement.")
                return False
        
        return True

    def buildRoad(self,player,turtle):

        # set board's road's owner to player
        self.owner = player
        
        #add corners to player
        if self.ci1 not in self.owner.corners:
            self.owner.corners.append(self.ci1)
        if self.ci2 not in self.owner.corners:
            self.owner.corners.append(self.ci2)

        # draw it
        self.drawRoad(turtle,player.color)    

    
