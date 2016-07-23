from basic_functions import abxy
class Road(object):
    def __init__(self,data):
        self.id=data[0]
        self.c1=(data[1],data[2])   #(a,b) of 1st corner
        self.c2=(data[3],data[4])   #(a,b) of 2nd corner
        self.p1=abxy( self.c1 ) #(x,y) of 1st corner
        self.p2=abxy( self.c2 ) #(x,y) of 2nd corner
        self.ci1=data[5]    #corner 1 id
        self.ci2=data[6]    #corner 2 id
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
