class Player(object):
    def __init__(self,id,col="white"):
        self.id=id
        self.cards={ "wheat":0,"ore":0,"brick":0,"sheep":0,"wood":0}
        self.n_cards = 0
        self.used_armies=0
        self.dev_cards=[]
        self.vp = 0
        self.corners=[] #actual objects
        self.settlements=[]
        self.roads=[]
        self.color = col
        self.ports = {"wheat":False,"ore":False,"brick":False,"wood":False,"sheep":False,"3":False}

    #if player can pay for a dictionary of items
    def canBuy(self,dic):
        #    'settlement':{"wheat":1,"brick":1,"wood":1,"sheep":1},
        #    'city':{"wheat":2,"ore":3},
        #    'dev':{"wheat":1,"ore":1,"sheep":1},
        #    'road':{"brick":1,"wood":1}
        for key in dic:
            if self.cards[key] < dic[key]:
                return False
        return True

    #pays for a dictionary of items
    def payFor(self,dic):
        for key in dic:
            self.cards[key] -= dic[key]
        

    #
    def recieve(self,dic):
        for key in dic:
            self.cards[key] += dic[key]



    #If user has more than 7 cards
    #must discard half of your cards (rounding down)
    def robber_discard(self):
        init_cards = self.n_cards

        if init_cards > 7:
            while player.n_cards > (init_cards+1)//2:
                print("You have "+str(player.n_cards)+" cards.")
                extra = player.n_cards - (init_cards+1)//2
                print("You need to discard "+str(extra)+"cards.")
                for key in player.cards:
                    print("You have "+str(player.cards[key])+" "+key)
                disc = input("For each card you wish to discard, enter its first letter and a space inbetween letters.")
                disc = disc.split(" ")
                for ans in disc:
                    if player.n_cards == (init_cards+1)//2:
                        #you have discarded enough cards
                        break
                    if ans=="W" or ans=="w":
                        if player.cards["wheat"]>0:
                            player.cards["wheat"]-=1
                            player.n_cards-=1
                        if ans=="L" or ans=="l":
                            if player.cards["lumber"]>0:
                                player.n_cards-=1
                                player.cards["lumber"]-=1
                        if ans=="B" or ans=="b":
                            if player.cards["brick"]>0:
                                player.n_cards-=1
                                player.cards["brick"]-=1
                        if ans=="S" or ans=="s":
                            if player.cards["sheep"]>0:
                                player.cards["sheep"]-=1
                                player.n_cards-=1

    def getDic(self,isTradingAway):
        print("There are 5 resources: wood, wheat, ore, sheep and brick.")
        #SELECT Resources to send
        good = False
        while not good:
            if isTradingAway:
                response = input("Enter each resource you want to trade away, seperated by a space.\n")
            else:
                response = input("Enter each resource you want to trade for, seperated by a space.\n") 
            dic = {}
            resources=["wheat","ore","brick","sheep","wood"]
            for r in response.split():
                if r in resources:
                    dic[r] = dic.get(r,0)+1
            good = input("You selected "+str(dic)+". Is this what you want? (y/n)\n")
            if good == "n":
                pass
            elif good == "y":
                good = True
            else:
                print("Unknown response, answer interpreted as yes.")

        return dic

        
        



