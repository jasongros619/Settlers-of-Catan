from boardclass import *
from playerclass import *

#import cTurtle
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

    def __init__(self,turt):
        self.players=[]
        self.addplayers()

        self.turn=0
        self.state="new"
        #set to 'settle' and 'road' during starting rounds
        #set to None, 'robber', 'trade', 'buy',...
        self.round=0
        self.lastRoad=-1
        self.lastSettle = -1
        self.board = Board()
        self.turtle = turt #reference to Main's cTurtle


        #setup board
        self.board.shuffle()
        self.board.drawmap()

        """for debugging
        for r in self.board.corners:
            turtle.up()
            turtle.goto(r.x,r.y)
            turtle.write(r.id)
        #    print(r.id,r.x,r.c2)
        #"""
        
        self.state = "setup_settle"
        self.turtle.onClick(self.reshuffle_board)

        #turtle.listen()
        #turtle.onscreenclick( self.setuprounds)

        #turtle.mainloop()

    #ends turn by adjusting 'self.turn' and 'self.round'
    def reshuffle_board(self,x,y):
        isHappy = True
        if not isHappy: #player wants to reshuffle
            self.turtle.onClick(None)
            self.board.shuffle()
            self.board.drawmap()
            self.turtle.onClick(self.reshuffle_board)

        if isHappy:
            self.state = "setup_settle"
            print("state set to ",self.state)
            self.turtle.onClick(self.setup_settle)


    def setup_settle(self,x,y):
        corn = self.board.selectCorn(x,y)
        if corn == None:
            print("No corner selected")
            return False

        player = self.players[ self.turn ]
        neighbors = [self.board.corners[cid] for cid in corn.corners]
        if not corn.canSettle(player,neighbors,False):
            return False

        self.turtle.onClick(None)
        corn.buildSettlement(player,self.turtle,False) #right?
        self.lastSettle = corn.id
        self.state = "setup_road"
        print("State set to: "+self.state)
        self.turtle.onClick(self.setup_road)

    def setup_road(self,x,y):
        road = self.board.selectRoad(x,y)
        if road == None:
            print("No road selected")
            return False
        player = self.players[ self.turn ]

        if not road.canRoad(player,self.lastSettle):
            return False

        self.turtle.onClick(None)
        road.buildRoad(player,self.turtle)

        self.endturn()
        if self.round == 2:
            self.state = "roll_die"
            print("State set to 'roll_die'")
            print("Player "+str(self.turn+1)+", click to roll dice.")
            self.turtle.onClick(self.roll_die)
        else:
            print("State set to 'setup_settle'")
            self.state = "setup_settle"
            self.turtle.onClick(self.setup_settle)

    def provide(self,roll):
        for hex in [hex for hex in self.board.hexes if hex.num == roll and hex.robber == False]:
            for corner in [self.board.corners[cid] for cid in hex.corners]:
                if corner.owner != None:
                    player = self.players[corner.owner]
                    player.cards[hex.type] += corner.lvl
    
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
    def roll_die(self,x,y):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        both = die1+die2
        print("You rolled: "+str(die1)+" and a "+str(die2)+" for a total of "+str(both))

        print("Before roll")
        for id,player in enumerate(self.players):
            print("Player "+str(id+1)+" has:")
            print(player.cards)

        print("After roll")
        for id,player in enumerate(self.players):
            print("Player "+str(id+1)+" has:")
            print(player.cards)
        
    def main_turn(x,y):
        pass


        # 0,0 -> 0,1
        # 0,1 -> 0,2
        # 0,2 -> 0,3 -> 1,2
        # 1,2 -> 1,1
        # 1,1 -> 1,0
        # 1,0 -> 1,-1 -> 2,0
        # x,y
        #
    

    def roll(self):
        x = random.randint(1,6)
        y = random.randint(1,6)
        if x+y == 7:
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

#a = cTurtle
#game = Game(a)

            
