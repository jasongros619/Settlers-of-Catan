from gameclass import *
import cTurtle

""" Setup Turtle """
cTurtle.speed(10)
cTurtle.hideturtle()
cTurtle.colormode(255)

"""Adjust Screen"""
cTurtle.screensize(780,780)
cTurtle.winsize(780,780)

""" Create a new game """
game=Game(cTurtle)
#game.debug = True


game.NewGame()

#Dont let program quit if it is __Main__
cTurtle.listen()
cTurtle.mainloop()
