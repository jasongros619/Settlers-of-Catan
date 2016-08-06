from boardclass import *
from playerclass import *

import random

class Game(object):
    def addplayers(self):
        count = 0
        answer = 3
#        answer = input("How many players?\n")
#        while answer!="3" and answer!="4":
#            answer = input("Invalid answer. How many players?\n")
        for i in range( int(answer) ):
            color1 = random.randint(0,255)
            color2 = random.randint(0,255)
            color3 = random.randint(0,255)
            self.players.append( Player(i, (color1,color2,color3)) )

    def __init__(self):
        self.players=[]
        self.addplayers()

        self.turn=0
        self.state="new"
        #set to 'settle' and 'road' during starting rounds
        #set to None, 'robber', 'trade', 'buy',...
        self.round=0
#        self.lastRoad=-1
        self.lastSettle=-1
        self.board = Board()




        #setup board
        self.board.shuffle()
        self.board.drawmap()

        #for debugging
        for r in self.board.corners:
            turtle.up()
            turtle.goto(r.x,r.y)
            turtle.write(r.id)
        #    print(r.id,r.x,r.c2)

        self.state = "settle"

        #turtle.listen()
        #turtle.onscreenclick( self.setuprounds)

        #turtle.mainloop()

    #ends turn by adjusting 'self.turn' and 'self.round'
    def endturn(self):
        if self.round==0:
            self.turn+=1
            if self.turn==len(self.players):
                self.turn=len(self.players)-1
                self.round=1
        elif self.round==1:
            self.turn-=1
            if self.turn==-1:
                self.round=2
                self.turn=0
        else: #>=2
            self.turn+=1
            if self.turn==len(players):
                self.turn=0
                self.round+=1

        # 0,0 -> 0,1
        # 0,1 -> 0,2
        # 0,2 -> 0,3 -> 1,2
        # 1,2 -> 1,1
        # 1,1 -> 1,0
        # 1,0 -> 1,-1 -> 2,0
        # x,y
        #

    def roll(self):
        x=random.randint(1,6)
        y=random.randint(1,6)
        if x+y==7:
            #Special event

            #have players dicard cards
            for player in self.players:
                player.robber_discard()
                                
            #move robber and steal from nearby players if applicable
            print("Move robber")
            print("EVENT NEEDED in boardclass\roll")
        else:
            #have each appropriate hex give the appropriate corners'
            #owners their respective resources
            for H in self.board.hexes:
                if H.num==x+y and H.rob==False: 
                    for corn in [self.board.corners[c] for c in h.corners]:
                        if corn.owner!=None:
                            players[corn.owner].cards[ str(H.type) ]+=corn.lvl
                            players[corn.owner].n_cards += corn.lvl

    #takes mouse input and relates it to regular turn
    def regular_turn(self,x,y):
        input("Press enter to ROLL!")

        #incomplete
        

    #takes mouse input and relates it to the setup rounds
    def setuprounds(self,x,y):
        #round 0
        if self.round==0:
            if self.state=="settle":
                cid=self.board.buildSettlement(x,y,self.turn,self,False)
                if cid!=-1:
                    self.state="road"
                    self.lastSettle=cid
            elif self.state=="road":
                rid=self.board.buildRoad(x,y,self.turn,self,[self.lastSettle])
                if rid!=-1:
                    self.state="settle"
                    self.endturn()
        #round 1
        elif self.round==1:
            if self.state=="settle":
                cid=self.board.buildSettlement(x,y,self.turn,self,False)
                if cid != -1:
                    self.state="road"
                    C=self.board.corners[cid]
                    for h in C.hexes:
                        try:
                            self.players[self.turn].cards[ board.hex[h].type ]+=1
                        except:
                            pass
                    self.lastSettle=cid
            elif self.state=="road":
                rid=self.board.buildRoad(x,y,self.turn,self,[self.lastSettle])
                if rid != -1:
                    self.state="settle"
                    self.endturn()
            
