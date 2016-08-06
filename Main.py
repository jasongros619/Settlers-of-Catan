#550,400
"""
TO DO:
~build road?
"""
#"hexgraphs" =[id,a,b,[*corners],[*roads]]
#'cornergraphs'=[id,a,b,[*roads],[*hexes]]
#'roadsgraphs'=[id,ab,ab,id1,id2,[*roads],[*hexes]

import turtle
turtle.speed(10)
turtle.title("Settlers of Catan")
turtle.hideturtle()
turtle.colormode(255)
import math
import random


from basic_functions import *
    # answer ( prompt, *arg) -needs an escape option
    # nearid ( group, pos ) <>
    # abxy(pos) <> => (x,y)
    # dist(x1,y1,x2,y2)```````````````````````````````````````````
    # drawhex( ? )  -should use real pictures
    # cabAng(c,a,b) returns ang (in radians)?


from playerclass import *
    # .id .cards .army .dev .vp .corn[] .settlements[]
"Hex class"
    # .r .id .a .b .x .y .type .corners[] .roads[] .hex[] .num .rob
    # .provide()
"Corner class"
    # .id .a .b .x .y .roads[] .hexes[] .corn[]
"Road class"
    # .id .c1(a,b) .ci1 .c2(a,b) .ci2 .x .y .p1(x,y) .p2(x,y) .roads[] .owner=None
from boardclass import *
    # .hex .corn .road
    # .shuffle()
    # .drawmap()
    # .roll
    # .drawSettlement(cid,color='red')
    # .selectCorn(x,y,reach=20)
    # .canSettle(x,y,connect=True)
    # .buildSettlement(x,y,playerID,game,connect)
    # .selectRoad(x,y,?
from gameclass import *
    # .players=[] .turn



#drawRect(550,-400,300,800,"black","black")
#drawRect(-550,-400,-300,800,"black","black")
drawRect(-550,-400,1100,800,(200,200,200),"black")

game=Game()





#game states
#start screen
#each player initial setup
    #choose a settlement
    #choose a road
    #end turn ... 


turtle.listen()       


turtle.onscreenclick( game.setuprounds)
turtle.mainloop()
