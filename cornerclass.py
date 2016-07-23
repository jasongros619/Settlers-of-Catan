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
        self.corn=[]
        for c in data[15:21]:
            if c==-1:
                break
            self.corn.append(c)
        self.owner=None
        self.lvl=0
        
