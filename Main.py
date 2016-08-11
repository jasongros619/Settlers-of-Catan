from gameclass import *
import cTurtle
""" Setup Turtle """
cTurtle.speed(10)
#cTurtle.title("Settlers of Catan")
cTurtle.hideturtle()
cTurtle.colormode(255)

""" Create a new game """
game=Game(cTurtle)


#Dont let program quit if it is __Main__
cTurtle.listen()
cTurtle.mainloop()
