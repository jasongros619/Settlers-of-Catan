class Player(object):
    def __init__(self,id,col="white"):
        self.id=id
        self.cards={ "wheat":0,"ore":0,"brick":0,"sheep":0,"wood":0}
        self.used_army=0
        self.dev=[]
        self.vp=0
        self.corn=[]
        self.settlements=[]
        self.color=col
        self.ports={"wheat":False,"ore":False,"brick":False,"wood":False,"sheep":False,"3":False}
