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

        #fun
        for r in self.board.corn:
            turtle.up()
            turtle.goto(r.x,r.y)
            turtle.write(r.id)
        #    print(r.id,r.x,r.c2)

        self.state = "settle"

        #turtle.listen()
        #turtle.onscreenclick( self.setuprounds)

        #turtle.mainloop()

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
            #special event where each player w/ over 7 cards discards half
            #and then the roller moves the robber to a space
            #and steals and random resource from the a player with settlement
            #on corner next to hex

            for i in range(len(self.players)):
                player = self.players[i]
                init_cards = player.n_cards
                
                if player.n_cards > 7:
                    print("Player "+str(i+1)+", you have over 7 cards.")
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
                            #if ans
                                
                    
            print("Move robber")
            print("EVENT NEEDED in boardclass\roll")
        else:
            #have each appropriate hex give the appropriate corners'
            #owners their respective resources
            for h in self.board.hex:
                if h.num==x+y and h.rob==False:
                    for c in h.corners:
                        if self.board.corn[c].owner!=None:
                            players[c.owner].cards[ str(h.type) ]+=c.lvl

    #takes mouse input and relates it to regular turn
    def regular_turn(self,x,y):
        input("Press enter to ROLL!")
        
        

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
                    C=self.board.corn[cid]
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
            
