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
            #Choose a random color
            #that isnt similar to existing ones
            while True:
                color1 = random.randint(0,255)
                color2 = random.randint(0,255)
                color3 = random.randint(0,255)

                is_too_similar = False
                for player in self.players:
                    c1 = player.color[0]
                    c2 = player.color[1]
                    c3 = player.color[2]
                    diffSqr = (c1-color1)**2 + (c2-color2)**2 + (c3-color3)**2
                    if diffSqr < 10000: #arbitrary number
                        is_too_similar = True
                        break
                if not is_too_similar:
                    break
            self.players.append( Player(i, (color1,color2,color3)) )

    def __init__(self,turt):
        self.players=[]
        self.addplayers()

        self.turn=0
        self.state="new"
        #set to 'settle' and 'road' during starting rounds
        #set to None, 'robber', 'trade', 'buy',...
        self.round=-1 #-1 for init
        self.lastRoad=-1
        self.lastSettle = -1
        self.board = Board()
        self.turtle = turt #reference to Main's cTurtle
        self.debug = False

        #setup board
#        self.board.shuffle()
#        self.board.drawmap(self.turtle)

        """for debugging
        for r in self.board.corners:
            turtle.up()
            turtle.goto(r.x,r.y)
            turtle.write(r.id)
        #    print(r.id,r.x,r.c2)
        #"""

    def StartGame(self,x,y):
        #Player is happy and wants to play
        print("")
        self.state = "setup_settle"
        self.turtle.onClick(self.setup_settle)
        self.endturn()
        print("Player "+str(self.turn+1)+", click on a corner to place a settlement.")


    def NewGame(self):
        self.board.shuffle()
        self.board.drawmap(self.turtle)
#        print("Click on '?' if you are happy with the board.")
#        print("Otherwise you can click elsewhere to reshuffle the board.")
        print("During the first two rounds, each player places a settlement and a road.")
        print("Click to start game.")

        self.turtle.onClick(self.StartGame)
            


    def setState(self,state):
        if self.debug:
            print("==Changing state from "+self.state+" to "+state)
        self.state = state

    #ends turn by adjusting 'self.turn' and 'self.round'
    def reshuffle_board(self,x,y):
        isHappy = True
        
        if not isHappy: #player wants to reshuffle
            self.turtle.onClick(None)
            self.board.shuffle()
            self.board.drawmap()
            self.turtle.onClick(self.reshuffle_board)

        if isHappy:
            self.setState("setup_settle")
#            print("state set to ",self.state)
            print("============")
            print("Now each player will place a settlement and a road.")
            print("")
            self.endturn()
            print("Player "+str(self.turn+1)+", please click on a corner to place a settlement.")
            self.turtle.onClick(self.setup_settle)



    def setup_settle(self,x,y):
        #printCoordinates
        if self.debug:
            print("Coordinates (x,y) = ",(x,y))
        corn = self.board.selectCorn(x,y)
        if corn == None:
            print("No corner selected")
            return False

        player = self.players[ self.turn ]
        if not corn.canSettle(player,False):
            return False

        self.turtle.onClick(None)
        corn.buildSettlement(player,self.turtle,False) #right?
        self.lastSettle = corn.id
        print("")
        self.setState("setup_road")
        print("Player "+str(self.turn+1)+", click on an edge to place a road.")
#        print("State set to: "+self.state)
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

        if self.round == 1 and self.turn == 0:
            print("")
            self.setState("roll_die")
            self.endturn()
            print("Player "+str(self.turn+1)+", click to roll dice.")
            self.turtle.onClick(self.roll_die)
        else:
            #print("State set to 'setup_settle'")
            print("")
            self.endturn()
            self.setState("setup_settle")
            print("Player "+str(self.turn+1)+", please click on a corner to place a settlement.")
            self.turtle.onClick(self.setup_settle)

    
    
    def endturn(self):
        print("\n\n\n====== New Turn ======")
        if self.round==-1:
            self.turn=0
            self.round=0
        elif self.round==0:
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
            if self.turn==len(self.players):
                self.turn=0
                self.round+=1
    def roll_die(self,x,y):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        both = die1+die2
        print("You rolled: "+str(die1)+" and a "+str(die2)+" for a total of "+str(both))

        #print("Before roll:")
        #for id,player in enumerate(self.players):
        #    print("Player "+str(id+1)+" has ",player.cards)
        self.board.provide(both)
        #print("After roll:")
        #for id,player in enumerate(self.players):
        #    print("Player "+str(id+1)+" has ",player.cards)

        if both == 7:
            print("robber?")
        else:
            print("You recieved : ...")
        print("You now have "+str(self.players[self.turn].cards))

        
        print("")
        self.setState("main_turn")
        self.turtle.onClick(self.main_turn)
        
    def main_turn(self,x,y):
        choice = self.select_corners(x,y)

        #End Turn
        if choice == 0:
            self.setState("roll_die")
            self.endturn()
            print("Player "+str(self.turn+1)+", please click to roll dice.")
            self.turtle.onClick(self.roll_die)

        if choice == 1:
            self.trade_prompts()
        if choice == 2:
            self.buy_prompts()


    def select_corners(self,x,y):
        if self.debug:
            print("==Mouse: "+str((x,y)))

        ans = -1
        if overRect(x,y,-380,260,120,120):
            ans = 0
        elif overRect(x,y,260,260,120,120):
            ans = 1
        if overRect(x,y,-380,-380,120,120):
            ans = 2
        if overRect(x,y,260,-380,120,120):
            ans = 3

        #print what corner is chosen if any
        if self.debug:
            responses = (
                "==You clicked on: 'End Turn'",
                "==You clicked on: 'Trade'",
                "==You clicked on: 'Buy'",
                "==You clicked on: 'Use Dev Card'"
            )
            if ans != -1:
                print(responses[ans])

        return ans

    def trade_prompts(self):
        player1 = self.players[self.turn]
        ans1 = input("Do you wish to trade with players or ports? (players/ports)\n")

        if ans1 == "players":
            #SELECT player2
            for i,player in enumerate(self.players):
                if i!=self.turn:
                    print("Player "+str(i+1)+" has "+str(sum(player.cards.values()))+" cards.")
            pid = input("Who do you wish to trade with? Enter 1, 2, 3 (or 4)\n")
            if pid not in ["1","2","3","4","5","6"][:len(self.players)]:
                print("Unkown player number. Trade aborted")
                return False
            player2 = self.players[int(pid)-1]

            #Ask to provide resources, check if you have them
            dic1 = player1.getDic(True)
            if not player1.canBuy(dic1):
                print("You do not have enough resources. Trade aborted")
            dic2 = player2.getDic(False)
            
            #Check if player 2 agrees (and can afford the trade).
            print("=========")
            print("Player "+str(player2.id+1)+", do you want to trade:")
            print(str(dic2)+" for "+str(dic1)+" with Player "+str(player1.id+1))
            cons = input("(y/n) ")
            while True:
                if cons == "y":
                    if player2.canBuy(dic2):
                        player1.payFor(dic1)
                        player2.payFor(dic2)
                        player1.recieve(dic2)
                        player2.recieve(dic1)
                        return True
                    else:
                        print("Player "+str(player2.id+1)+" cannot afford the trade. Trade aborted.")
                elif cons == "n":
                    print("Player "+str(player2.id+1)+" declined. Trade aborted")
                    return False
                else:
                    cons = input("Invalid response. Please answer 'y' or 'n'. ")
        else:
            print("Unknown response.")

    def buy_prompts(self):
        player = self.players[self.turn]
        items = ["road","settlement","city","dev card"]
        dics = [{"brick":1,"wood":1},
                {"brick":1,"wood":1,"sheep":1,"wheat":1},
                {"ore":3, "wheat":2},
                {"ore":1, "wheat":1, "sheep":1}
        ]

        #Display your items + item costs
        print("The cost of each item is:")
        for i in range(4):
            print("%12s : %12s" % (items[i],str(dics[i])))
        print("You have: "+str(player.cards))
        print("")
        
        #Ask for which resource
        which = input("Which would you like to buy? (or enter q to quit)\n")
        while which not in ["q"]+items:
            which = input("Invalid answer. Which would you like to buy? (or enter q to quit)\n")

        #Quit
        if which == "q":
            print("Trade aborted.\n")
            return False

        #Check if canBuy
        N = items.index(which)
        if not player.canBuy(dics[N]):
            print("You do not have enough resources to buy this card.")
            print("Trade aborted.\n")
            return False

        #SWITCH(){}
        if which == "settlement":
            print("Click on the corner you wish to build a settlement.")
            self.setState("_buy_settle")
            self.turtle.onClick(self._buy_settle)
        elif which == "road":
            print("Click on the edge you wish to build a road.")
            self.setState("_buy_road")
            self.turtle.onClick(self._buy_road)
        elif which == "city":
            print("Click on the corner you wish to build a city.")
            self.setState("_buy_city")
            self.turtle.onClick(self._buy_city)
        else:
            print("Not dealt with this option yet")

    def _buy_settle(self,x,y):
        if self.debug:
            print("Coordinates (x,y) = ",(x,y))


        #Select a corner and quit if None
        corn = self.board.selectCorn(x,y)
        if corn == None:
            print("No corner selected.")
            print("Buying settlement aborted.\n")
            self.setState("main_turn")
            self.turtle.onClick(self.main_turn)
            return False

        #Check that player can place a settlement there
        player = self.players[self.turn]
        if not corn.canSettle(player,True):
            print("Buying settlement aborted.\n")
            self.setState("main_turn")
            self.turtle.onClick(self.main_turn)
            return False

        #Actually build it & revert state
        corn.buildSettlement(player,self.turtle,True)
        player.payFor({"brick":1,"wheat":1,"sheep":1,"wood":1})
        print("You bought a settlement.")
        self.setState("main_turn")
        self.turtle.onClick(self.main_turn)
        return True

    def _buy_road(self,x,y):
        #Select road if possible
        road = self.board.selectRoad(x,y)
        if road == None:
            print("No road selected")
            print("Buying road aborted.\n")
            self.setState("main_turn")
            self.turtle.onClick(self.main_turn)
            return False

        #Check if road is buildable
        player = self.players[ self.turn ]
        if not road.canRoad(player):
            #warning message printed
            print("Buying road aborted.\n")
            self.setState("main_turn")
            self.turtle.onClick(self.main_turn)
            return False

        #Actually build it
        self.turtle.onClick(None)
        print("You bought a road.\n")
        road.buildRoad(player,self.turtle)
        player.payFor({"brick":1,"wood":1})
        self.setState("main_turn")
        self.turtle.onClick(self.main_turn)

    def _buy_city(self,x,y):
        #Select corn if possible
        corn = self.board.selectCorn(x,y)
        if corn == None:
            print("No corner selected.")
            print("Buying city aborted.\n")
            self.setState("main_turn")
            self.turtle.onClick(self.main_turn)
            return False

        #Check if player can build it
        player = self.players[ self.turn ]
        if not corn.canCity(player):
            print("Buying city aborted.\n")
            self.setState("main_turn")
            self.turtle.onClick(self.main_turn)
            return False

        #Actually build it
        self.turtle.onClick(None)
        print("You bought a city.\n")
        corn.buildCity(player,self.turtle)
        player.payFor({"ore":3,"wheat":2})
        self.setState("main_turn")
        self.turtle.onClick(self.main_turn)
        
            
        

    

#a = cTurtle
#game = Game(a)

            
