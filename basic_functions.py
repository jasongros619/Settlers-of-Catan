import random
import math
import turtle
turtle.speed(10)

def answer(prompt,*arg):
    ans=input(prompt+"\n")
    arg=list(arg)
    for i in range(len(arg)):
        arg[i]=str(arg[i])
    while ans not in arg:
        print("Unknown command. Type help for list of all commands.")
        ans=input(prompt+"\n")
        if ans=="help":
            print("Commands : "+', '.join(arg))
    return ans

def nearid(group,pos):
    def dist(x1,y1,x2,y2):
        x=x1-x2
        y=y1-y2
        return (x*x+y*y)**0.5
    bestd=dist( pos[0],pos[1], group[0].x,group[0].y )
    besti=0
    for i in range(1,len(group)):
        d=dist( pos[0],pos[1], group[i].x,group[i].y )
        if d<bestd:
            bestd=d
            besti=i
    return besti

def abxy( ab,r=60,x=0,y=40):
    a=ab[0]
    b=ab[1]

    x=(a+b/2)*r+x
    y=(b*3**0.5/2)*r+y
    return (x,y)

def dist(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5


def drawhex(self,rad=40):
    turtle.up()
    turtle.goto(self.x+self.r,self.y)
    turtle.down()
    for i in range(1,7):
        turtle.goto( self.x+math.cos(math.pi/3*i)*self.r,
                        self.y+math.sin(math.pi/3*i)*self.r)

def calcAng(x,y,c1,c2):
    c1=abxy(c1)
    c2=abxy(c2)
    dx1=x-c1[0]
    dy1=y-c1[1]
    dx2=x-c2[0]
    dy2=y-c2[1]
    d1=(dx1*dx1+dy1*dy1)**0.5
    d2=(dx2*dx2+dy2*dy2)**0.5
    if d1*d2==0:
        return None
    dot=dx1*dx2+dy1*dy2
    cosAng=dot/d1/d2
    return math.acos(cosAng)


def cabAng(c,a,b):
    #given three points c,a,b find the angle ACB. (in radians)
    if a==c or b==c:
        return 0
    A=( c[0]-a[0], c[1]-a[1] )
    B=( c[0]-b[0], c[1]-b[1] )
    dot=A[0]*B[0]+A[1]*B[1]
    lenA=(A[0]*A[0]+A[1]*A[1])**0.5
    lenB=(B[0]*B[0]+B[1]*B[1])**0.5
    cosAng=dot/lenA/lenB
    from math import acos
    from math import pi
    return acos(cosAng)*180/pi

def overRect(mouseX,mouseY,x,y,w,h):
    #
    # (x,y+h)----(x+w,y+h)
    #   |            |
    #   |            |
    # (x,y)------(x+w,y)
    return mouseX>x and mouseY>y and mouseX<x+w and mouseY<y+h
    
def drawRect(x,y,w,h,fillColor="white",lineColor="black"):
    turtle.up()
    
    turtle.goto(x,y)
    turtle.down()
    turtle.color(lineColor,fillColor)
    turtle.begin_fill()
    turtle.goto(x+w,y)
    turtle.goto(x+w,y+h)
    turtle.goto(x,y+h)
    turtle.goto(x,y)
    turtle.end_fill()

#turtle.goto(0,0)
#drawRect(0,0,10,10)
#drawRect(100,100,200,200,"red","black")
