from basic_functions import abxy

class Corner(object):
    def __init__(self,data):
        self.id=data[0]
        self.a=data[1] #a coordinate
        self.b=data[2] #b coordinate
        xy=abxy( (self.a,self.b) )
        self.x=xy[0] #x coordinate
        self.y=xy[1] #

        #list of nearby roads' ids
        self.roads=[]
        for r in data[3:9]:
            if r==-1:
                break
            self.roads.append(r)

        #list of nearby hexes' ids
        self.hexes=[]
        for h in data[9:15]:
            if h==-1:
                break
            self.hexes.append(h)
            
        #list of nearby corners' ids
        self.corners=[]
        for c in data[15:21]:
            if c==-1:
                break
            self.corners.append(c)
        self.owner=None
        self.lvl=0
        self.ports = None

    def drawSettlement(self,turtle,color="red"):
        R=15
        turtle.color("black",color)
        
        turtle.up()
        turtle.goto(self.x+R,self.y-R)
        turtle.down()
        turtle.begin_fill()
        turtle.goto(self.x+R,self.y+R)
        turtle.goto(self.x-R,self.y+R)
        turtle.goto(self.x-R,self.y-R)
        turtle.goto(self.x+R,self.y-R)
        turtle.end_fill()
    #"""

    #bool if player can settle on corner
    def canSettle(self,player,needConnect=True):
        
        #Check if corner is connected to your roads
        if (needConnect and (self.id not in [corn.id for corn in player.corners])):
            print("You do not have a road connected to this point")
            return False

        #check if there is a different settlement on the corner
        if self.owner!=None:
            print("There is already a settlement there.")
            return False

        #check if there are centers nearby
        nearby=False
        for neighbor in self.corners:
            if neighbor.owner!=None:
                nearby = True
                break
        if nearby:
            print("There is a settlement nearby")
            return False

        #there are no restrictions
        return True

    def buildSettlement(self,player,turtle,needConnect=True):
        """
        * set corner's owner/lvl to settlement
        * (adds corner to player if new)
        * add nearby ports, vp, 'settlement' to player
        * draws settlement
        """
        #change Corner object
        self.owner=player
        self.lvl = 1

        #Adjusts player:
        #'.vp', '.settlments', '.ports', '.corners'
        self.owner.vp+=1
        self.owner.settlements.append(self)
        if self.id not in [corn.id for corn in player.corners]:
            self.owner.corners.append(self)

        
        if self.ports != None:
            resource = self.ports[6:]
            self.owner.ports[resource] = True

        #drawit
        self.drawSettlement(turtle,player.color)

#        for Hex in [self.hexes[hex_id] for hex_id in self.hexes]:
#            if Hex.type in ["ports-brick","ports-wheat","ports-wood","ports-sheep","ports-ore","ports-3"]:
#                player.ports[ Hex.type[6:] ]=True


    def drawCity(self,turtle,color="red"):
        R=15
        turtle.color("black",color)
        
        turtle.up()
        turtle.goto(self.x+R,self.y-R)
        turtle.down()
        turtle.begin_fill()
        turtle.goto(self.x+R,self.y+R)
        turtle.goto(self.x,self.y+2*R)
        turtle.goto(self.x-R,self.y+R)
        turtle.goto(self.x-R,self.y-R)
        turtle.goto(self.x+R,self.y-R)
        turtle.end_fill()

    def canCity(self,player):

        #NOT OWNED BY PLAYER
        if self.owner.id != player.id:
            if self.lvl == 0:
                print("There is no settlement there.")
                return False
            if self.lvl == 1:
                print("That is not your settlement.")
                return False
            if self.lvl == 2:
                print("That is not your city.")
                return False
            
        #IS OWNED BY PLAYER
        else:
            #Check if already a city
            if self.lvl == 2:
                print("This is already a city.")
                return False

        return True

    def buildCity(self,player,turtle):
        self.owner.vp+=1
        self.lvl = 2
        self.drawCity(turtle,player.color)
"""
#         id a  b r [               ] [               ] [               ] 
string = "32 4 -2 r 53 50 45 44 49 52 58 65 66 69 70 71 25 28 29 34 35 36".split(" ")
string = [ int(s) if i!=3 else s for i,s in enumerate( string )]

c = Corner(string)
print(c.id)
print(c.a,c.b)
print(c.x,c.y)
print(c.roads)
print(c.hexes)
print(c.corners)
"""
