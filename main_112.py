from cmu_112_graphics import *
from HelperClass import *
# return distance based on x1,x2,y1,y2
def getDistance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

def appStarted(app):
    # This is a Controller
    app.tank1=Tank(500,500,False,"player",1)
    app.tank2=Tank(1500,1500,False,"hostile",2)
    app.ifv1=IFV(400,400,False,"player",1)
    app.ifv2=IFV(1600,1500,False,"hostile",2)
    app.tree1=Tree(900,600,1)
    app.tree2=Tree(1000,600,2)
    app.house1=House(1050,850,1)
    # initialize the map
    app.board1=Board([app.tank1,app.tank2],[app.ifv1,app.ifv2],[],[app.tree1,app.tree2,app.house1])
    # keep track of how much screen should be shifted
    app.moved_x = 0
    app.moved_y = 0
    # the location that the player want the unit to move
    app.destination=[]
    # the unit being selected
    app.selected=None
    app.firingTarget=None
    # object within player's sight
    app.sighted=set()
    # units controled by the player
    app.playerUnits=set()
    for tanks in app.board1.tankList:
        if tanks.identity=="player":
            app.playerUnits.add(tanks)
    for IFVs in app.board1.ifvList:
        if IFVs.identity=="player":
            app.playerUnits.add(IFVs)
    # hotile units
    app.hostileUnits=set()
    for tanks in app.board1.tankList:
        if tanks.identity=="hostile":
            app.hostileUnits.add(tanks)
    for IFVs in app.board1.ifvList:
        if IFVs.identity=="hostile":
            app.hostileUnits.add(IFVs)
    # trees Set
    app.trees=set()
    for objs in app.board1.obstacles:
        if type(objs)==Tree:
            app.trees.add(objs)
    # houses Set
    app.houses=set()
    for objs in app.board1.obstacles:
        if type(objs)==House:
            app.houses.add(objs)

def keyPressed(app, event):
    # shift the view down
    if (event.key=="Down"):
        if app.board1.screen[1][1]<=(3990):
            app.moved_y+=10
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    # shift the view up
    elif (event.key=="Up"):
        if app.board1.screen[1][0]>=10:
            app.moved_y-=10
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    # shift the view left
    if (event.key=="Left"):
        if app.board1.screen[0][0]>=10:
            app.moved_x-=10
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    # shift the view right
    elif (event.key=="Right"):
        if app.board1.screen[0][1]<=(2990):
            app.moved_x+=10
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0

def mousePressed(app,event):
    # x,y coordinates on the map
    x=app.board1.screen[0][0]+event.x
    y=app.board1.screen[1][0]+event.y
    #selecting unit to move
    if app.board1.getTank(x,y)!=None:
        app.selected = app.board1.getTank(x,y)
    elif app.board1.getIFV(x,y)!=None:
        app.selected = app.board1.getIFV(x,y)
    else:
        # if not selecting, then the location clicked is destination
        app.destination = [x,y]

# move the selected unit, change its x y in timerfired
def moveUnits(app):
    if app.selected !=None and app.destination!=[] and\
    getDistance(app.selected.x,app.destination[0],app.selected.y,app.destination[1]):
        if app.selected.x<app.destination[0]:
            app.selected.x+=app.selected.speed
        else:
            app.selected.x-=app.selected.speed
        if app.selected.y<app.destination[1]:
            app.selected.y+=app.selected.speed
        else:
            app.selected.y-=app.selected.speed
# put the enemy units in view in app.sighted set
def enemysighted(app):
    for plu in app.playerUnits:
        for hu in app.hostileUnits:
            if getDistance(plu.x,hu.x,plu.y,hu.y)<=plu.range:
                app.sighted.add(hu)
    
def timerFired(app):
    app.sighted=set()
    app.moved_x=0
    app.moved_y=0
    moveUnits(app)
    enemysighted(app)

def drawTree(app,canvas,treeSet):
    for trees in treeSet:
        #x location on the screen
        x=trees.x-app.board1.screen[0][0]
        #y location on the screen
        y=trees.y-app.board1.screen[1][0]
        # if the tree on the map
        if app.board1.screen[0][0]<=trees.x<=app.board1.screen[0][1] and\
         app.board1.screen[1][0]<=trees.y<=app.board1.screen[1][1]:
         canvas.create_polygon(x,y-120,x-60,y,x+60,y,fill="Green")
         
def drawHouse(app,canvas,houseSet):
    for houses in houseSet:
        #x location on the screen
        x=houses.x-app.board1.screen[0][0]
        #y location on the screen
        y=houses.y-app.board1.screen[1][0]
        # if the tree on the map
        if app.board1.screen[0][0]<=houses.x<=app.board1.screen[0][1] and\
         app.board1.screen[1][0]<=houses.y<=app.board1.screen[1][1]:
         canvas.create_rectangle(x-120,y-100,x+120,y+100,fill="Grey")

def drawTank(app,canvas,tankList):
    for tanks in tankList:
        #x location on the screen
        x=tanks.x-app.board1.screen[0][0]
        #y location on the screen
        y=tanks.y-app.board1.screen[1][0]
        # if the tank is on the map
        if app.board1.screen[0][0]+30<=tanks.x<=app.board1.screen[0][1]-30 and\
         app.board1.screen[1][0]+30<=tanks.y<=app.board1.screen[1][1]-30 and\
            (tanks.identity=="player"or tanks in app.sighted):
            canvas.create_oval(x-30,y-30,x+30,y+30,fill='Red')
            canvas.create_text(x,y,text=f"Health: {tanks.health}",fill='Black')

def drawIFV(app,canvas,ifvList):
    for IFVs in ifvList:
        #x location on the screen
        x=IFVs.x-app.board1.screen[0][0]
        #y location on the screen
        y=IFVs.y-app.board1.screen[1][0]
        # if the IFV is on the map
        if app.board1.screen[0][0]+30<=IFVs.x<=app.board1.screen[0][1]-30 and\
         app.board1.screen[1][0]+30<=IFVs.y<=app.board1.screen[1][1]-30 and\
        (IFVs.identity=="player"or IFVs in app.sighted):
            canvas.create_oval(x-30,y-30,x+30,y+30,fill='Blue')
            canvas.create_text(x,y,text=f"Health: {IFVs.health}",fill='Black')

def redrawAll(app, canvas):
    drawTank(app,canvas,app.board1.tankList)
    drawIFV(app,canvas,app.board1.ifvList)
    drawTree(app,canvas,app.trees)
    drawHouse(app,canvas,app.houses)
    canvas.create_text(app.width/2,app.height/2,text=
    f"Frame {app.moved_x},{app.moved_y}, {app.board1.screen}",fill="black")
    canvas.create_text(app.width/2,app.height/2-30,text=
    f"Selected object{app.selected}",fill="black")
    canvas.create_text(app.width/2,app.height/2-50,text=
    f"{app.sighted}",fill="black")

def main():
    runApp(width=1440, height=763)

if __name__ == '__main__':
    main()
