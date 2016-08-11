class Player(object):
    def __init__(self,id,col="white"):
        self.id=id
        self.cards={ "wheat":0,"ore":0,"brick":0,"sheep":0,"wood":0}
        self.n_cards = 0
        self.used_armies=0
        self.dev_cards=[]
        self.vp = 0
        self.corners=[]
        self.settlements=[]
        self.roads=[]
        self.color = col
        self.ports = {"wheat":False,"ore":False,"brick":False,"wood":False,"sheep":False,"3":False}

    #
    def canBuy(self,item):
        cards = ()
        num = ()
        if item == "settlement":
            cards = ("wheat","brick","wood","sheep")
            num = (1,1,1,1)
        elif item == "city":
            cards = ("wheat","ore")
            num = (2,3)
        elif item == "road":
            cards = ("brick","wood")
            num = (1,1)
        elif item == "development card":
            cards = ("wheat","ore","sheep")
            num = (1,1,1)
        else:
            print("Unkown item: "+item)
            return False
        for i,card in enumerate(cards):
            if self.cards[card] < num[i]:
                return False
        return True

    #pays for item
    #('settlement','city','road','development card')
    def payFor(self,item):
        cards = ()
        num = ()
        if item == "settlement":
            cards = ("wheat","brick","wood","sheep")
            num = (1,1,1,1)
        elif item == "city":
            cards = ("wheat","ore")
            num = (2,3)
        elif item == "road":
            cards = ("brick","wood")
            num = (1,1)
        elif item == "development card":
            cards = ("wheat","ore","sheep")
            num = (1,1,1)
        else:
            print("Unkown item: "+item)
        for i,card in enumerate(cards):
            self.cards[card] -= num[i]



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


