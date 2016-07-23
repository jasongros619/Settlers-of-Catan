from basic_functions import abxy

class Hex(object):
    def __init__(self,data):
        self.r=60
        self.id=data[0]
        self.a=data[1]
        self.b=data[2]
        xy=abxy( (self.a,self.b),self.r,0,40)
        self.x=xy[0]
        self.y=xy[1]
        self.type=data[3] #

        #id of nearby corners
        self.corners=[]
        for i in data[4:10]:
            if i==-1:
                break
            self.corners.append(i)

        #id of nearby roads
        self.roads=[]
        for i in data[10:16]:
            if i==-1:
                break
            self.roads.append(i)

        #id of nearby hexes
        self.hex=[]
        for i in data[16:22]:
            if i==-1:
                break
            self.hex.append(i)
        self.num=0
        self.rob=False
