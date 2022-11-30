from cmu_112_graphics import *
from HelperClass import *

# return distance based on x1,x2,y1,y2
def getDistance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5
# initilize all objects and variables===========================================
def appStarted(app):

    app.tank1=Tank(600,400,False,"player",1)
    app.tank2=Tank(700,400,False,"player",2)
    app.tank3=Tank(800,400,False,"player",3)
    app.tank4=Tank(1500,1500,False,"hostile",4)
    app.tank5=Tank(600,1500,False,"hostile",5)

    app.ifv1=IFV(400,300,False,"player",1)
    app.ifv2=IFV(500,300,False,"player",2)
    app.ifv3=IFV(600,300,False,"player",3)
    app.ifv4=IFV(1800,1500,False,"hostile",4)

    app.tree1=Tree(900,600,1)
    app.tree2=Tree(1000,600,2)
    app.tree3=Tree(1700,1400,3)

    app.house1=House(1050,850,120,100,1)
    app.house2=House(650,850,120,100,2)
    app.house3=House(1500,1400,60,60,3)

    app.image1 = app.loadImage('Image1.png')
    app.image3 = app.scaleImage(app.image1, 1/4)
    app.image2 = app.loadImage('Image2.png')
    app.image4 = app.scaleImage(app.image2, 1/4)
    app.image5 = app.loadImage('Image3.png')
    app.image6 = app.scaleImage(app.image5, 240/252)
    app.image7 = app.loadImage('Image4.png')
    app.image8 = app.scaleImage(app.image7, 120/160)
    app.image9 = app.loadImage('Image6.png')
    app.image10 = app.scaleImage(app.image9, 120/1374)
    app.image11 = app.loadImage('Image7.png')
    app.image12 = app.scaleImage(app.image11, 1/4)
    app.image13 = app.loadImage('Image8.png')
    app.image14 = app.scaleImage(app.image13, 1/2.5)
    app.image15 = app.loadImage('Image9.png')
    app.image16 = app.scaleImage(app.image15, 1/2.5)

    # initialize the map
    app.board1=Board([app.tank1,app.tank2,app.tank3,app.tank4,app.tank5],[app.ifv1,app.ifv2,app.ifv3,app.ifv4],[],{app.tree1,app.tree2,app.tree3},{app.house1,app.house2,app.house3})
    # keep track of how much screen should be shifted
    app.moved_x = 0
    app.moved_y = 0
            
    #==============Values regarding the player============================#
    # the location that the player want the unit to move
    app.destination=[]
    # the unit being selected by the player
    app.selected=None
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

    #==============Values regarding the enemy============================#
    # hotile units
    app.hostileUnits=set()
    for tanks in app.board1.tankList:
        if tanks.identity=="hostile":
            app.hostileUnits.add(tanks)
    for IFVs in app.board1.ifvList:
        if IFVs.identity=="hostile":
            app.hostileUnits.add(IFVs)
    
# key press functions=========================================================
def keyPressed(app, event):
    # shift the view down
    if (event.key=="Down"):
        if app.board1.screen[1][1]<=(2500):
            app.moved_y+=30
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    # shift the view up
    elif (event.key=="Up"):
        if app.board1.screen[1][0]>=30:
            app.moved_y-=30
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    # shift the view left
    if (event.key=="Left"):
        if app.board1.screen[0][0]>=30:
            app.moved_x-=30
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    # shift the view right
    elif (event.key=="Right"):
        if app.board1.screen[0][1]<=(2440):
            app.moved_x+=30
            app.board1.changeScreen(app.moved_x,app.moved_y)
            app.moved_x=0
            app.moved_y=0
    if isinstance(app.selected,IFV):
        if event.key=="d":
            app.selected.mountState= not app.selected.mountState
            app.selected.changeMountState(app.selected.mountState)
            
# mouse press functions =========================================================
def mousePressed(app,event):
    # x,y coordinates on the map
    x=app.board1.screen[0][0]+event.x
    y=app.board1.screen[1][0]+event.y
    #selecting unit to move
    selectUnits(app,x,y)

# select unit and select destination
def selectUnits(app,x,y):
    # if clicked unit is a tank
    if app.board1.getTank(x,y)!=None:
        # if unit is friendly
        if app.board1.getTank(x,y) in app.playerUnits:
            # unit being controled is the unit being clicked
            app.selected = app.board1.getTank(x,y)
        # if unit clicked is not friendly
        else:
            enemy = app.board1.getTank(x,y)
            # make sure the unit is in distance
            if enemy in app.sighted:
                app.selected.target=enemy

    # if clicked unit is an IFV
    elif app.board1.getIFV(x,y)!=None:
        # if unit is friendly
        if app.board1.getIFV(x,y) in app.playerUnits:
            # unit being controled is the unit being clicked
            app.selected = app.board1.getIFV(x,y)
        # if unit clicked is not friendly
        else:
            enemy=app.board1.getIFV(x,y)
            # make sure the unit is seen
            if enemy in app.sighted:
                app.selected.target=enemy
    else:
        # if not selecting, then the location clicked is destination
        app.destination = [x,y]


# Timer Fired functions=========================================================

def timerFired(app):
    # clear sight sets every time so previously sighted unit can be recalculated
    app.sighted=set()
    for unit in app.playerUnits:
        unit.sight=set()
    for unit in app.hostileUnits:
        unit.sight=set()
    # clear moved trace since the move information is strored
    app.moved_x=0
    app.moved_y=0
    # game functions
    playerFunctions(app)
    enemyFunctions(app)

def enemyFunctions(app):
    #moveHunits(app)
    for unit in app.hostileUnits:
        countCover(app,unit)
    playerSighted(app)
    fireHostile(app)

def playerFunctions(app):
    moveUnits(app)
    countCover(app,app.selected)
    enemySighted(app)
    firePlayer(app)

# general timerfired functions
# the function to check if the vision on the enemy is blocked by obstacles
def directSight(app,x1,x2,y1,y2):
    if getDistance(x1,x2,y1,y2)<=10:
        return True
    elif app.board1.getHouses(x1,y1)!=None:
        return False
    else:
        if x1<x2:
            return directSight(app,x1+5,x2,y1+((y2-y1)/(x2-x1))*5,y2)
        elif x1>x2:
            return directSight(app,x1-5,x2,y1+((y1-y2)/(x2-x1))*5,y2)
        else:
            if y1>y2:
                return directSight(app,x1,x2,y1-5,y2)
            elif y1<y2:
                return directSight(app,x1,x2,y1+5,y2)
# check if the unit selected is in the location of a house
def notInBounds(app,x,y):
    if app.board1.getHouses(x,y+30) is not None:
        return False
    elif app.board1.getHouses(x,y-30) is not None:
        return False
    else:
        return True
    if app.board1.getHouses(x+30,y) is not None:
        return False
    elif app.board1.getHouses(x-30,y) is not None:
        return False
    else:
        return True
# indicate the coverState of unit object
def countCover(app,unit):
    if unit is not None:
        for house in app.board1.houses:
            if house.inCover(unit.x,unit.y):
                unit.coverState=True
                return None
        for tree in app.board1.trees:
            if tree.inCover(unit.x,unit.y):
                unit.coverState=True
                return None
        unit.coverState=False

# player functions
# calculate the attack of player's units
def firePlayer(app):
    for unit in app.playerUnits:
        if unit.target is not None and unit.target not in unit.sight:
            unit.target=None
        damage=unit.firing()
        if unit.target is not None and damage != 0:
            unit.target.takeDamage(damage,getDistance(unit.target.x,unit.x,unit.target.y,unit.y))
            if unit.target.health<=0:
                app.hostileUnits.remove(unit.target)
# put the enemy units in view in app.sighted set
def enemySighted(app):
    for plu in app.playerUnits:
        for hu in app.hostileUnits:
            if getDistance(plu.x,hu.x,plu.y,hu.y)<=plu.range and directSight(app,plu.x,hu.x,plu.y,hu.y):
                app.sighted.add(hu)
                if len(plu.sight)==0 and plu.target==None:
                    plu.target=hu
                plu.sight.add(hu)          

# move the selected unit, change its x y in timerfired
def moveUnits(app):
    if app.selected !=None and app.destination!=[]:
        if getDistance(app.selected.x,app.destination[0],app.selected.y,app.destination[1])>=20:
            if app.selected.x<app.destination[0]:
                app.selected.x+=app.selected.speed
                # if moved location is in houses, undo the move
                if not notInBounds(app,app.selected.x,app.selected.y):
                    app.selected.x-=app.selected.speed
            else:
                app.selected.x-=app.selected.speed
                if not notInBounds(app,app.selected.x,app.selected.y):
                    app.selected.x+=app.selected.speed
            if app.selected.y<app.destination[1]:
                app.selected.y+=app.selected.speed
                if not notInBounds(app,app.selected.x,app.selected.y):
                    app.selected.y-=app.selected.speed
                    #app.selected.y-=((app.destination[1]-app.selected.y)/(app.destination[0]-app.selected.x))*app.selected.speed
            else:
                app.selected.y-=app.selected.speed
                if not notInBounds(app,app.selected.x,app.selected.y):
                    app.selected.y+=app.selected.speed
                    #app.selected.y-=((app.destination[1]-app.selected.y)/(app.destination[0]-app.selected.x))*app.selected.speed
        else:
            app.destination=[]
# enemy functions
def fireHostile(app):
    for unit in app.hostileUnits:
        if unit.target is not None and unit.target not in unit.sight:
            unit.target=None
        damage=unit.firing()
        if unit.target is not None and damage != 0:
            unit.target.takeDamage(damage,getDistance(unit.target.x,unit.x,unit.target.y,unit.y))
            if unit.target.health<=0:
                app.playerUnits.remove(unit.target)
def playerSighted(app):
    for hu in app.hostileUnits:
        for plu in app.playerUnits:
            if getDistance(plu.x,hu.x,plu.y,hu.y)<=hu.range and directSight(app,plu.x,hu.x,plu.y,hu.y):
                if len(hu.sight)==0 and hu.target==None:
                    hu.target=plu
                hu.sight.add(plu)          

# Draw functions=========================================================

# draw all tree objects on the board
def drawTree(app,canvas,treeSet):
    for trees in treeSet:
        #x location on the screen
        x=trees.x-app.board1.screen[0][0]
        #y location on the screen
        y=trees.y-app.board1.screen[1][0]
        # if the tree on the map
        if app.board1.screen[0][0]<=trees.x<=app.board1.screen[0][1] and\
         app.board1.screen[1][0]<=trees.y<=app.board1.screen[1][1]:
         canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image10))
         #canvas.create_polygon(x,y-60*3**0.5,x-60,y,x+60,y,fill="Green")

# draw all House objects on the board        
def drawHouse(app,canvas,houseSet):
    for houses in houseSet:
        #x location on the screen
        x=houses.x-app.board1.screen[0][0]
        #y location on the screen
        y=houses.y-app.board1.screen[1][0]
        # if the tree on the map
        if app.board1.screen[0][0]<=houses.x<=app.board1.screen[0][1] and\
         app.board1.screen[1][0]<=houses.y<=app.board1.screen[1][1]:
            #canvas.create_rectangle(x-houses.width,y-houses.height,x+houses.width,y+houses.height,fill="Grey")
            if houses == app.house1 or houses==app.house2:
                canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image6))
            elif houses == app.house3:
                canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image8))
         

# draw all Tank objects on the board
def drawTank(app,canvas,tankList):
    for tanks in tankList:
        #x location on the screen
        x=tanks.x-app.board1.screen[0][0]
        #y location on the screen
        y=tanks.y-app.board1.screen[1][0]
        # if the tank is on the map
        if app.board1.screen[0][0]+30<=tanks.x<=app.board1.screen[0][1]-30 and\
         app.board1.screen[1][0]+30<=tanks.y<=app.board1.screen[1][1]-30 and\
            (tanks.identity=="player"or tanks in app.sighted) and tanks.health>=0:
            if tanks in app.playerUnits:
                canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image3))
            elif tanks in app.hostileUnits:
                canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image16))
            #canvas.create_oval(x-30,y-30,x+30,y+30,fill='Red')
            canvas.create_text(x,y,text=f"{tanks}",fill='Black')
            canvas.create_text(x,y-20,text=f"Health: {tanks.health}",fill='Black')
            canvas.create_text(x,y+30,text=f"cover: {tanks.coverState}",fill='Black')
            #canvas.create_text(x,y-15,text=f"firing: {tanks.firestatus}",fill='Black')
            canvas.create_text(x,y-30,text=f"timer: {tanks.timer}",fill='Black')
            canvas.create_text(x,y+20,text=f"target: {tanks.target}",fill='Black')

# draw all IFV objects on the board
def drawIFV(app,canvas,ifvList):
    for IFVs in ifvList:
        #x location on the screen
        x=IFVs.x-app.board1.screen[0][0]
        #y location on the screen
        y=IFVs.y-app.board1.screen[1][0]
        # if the IFV is on the map
        if app.board1.screen[0][0]+30<=IFVs.x<=app.board1.screen[0][1]-30 and\
         app.board1.screen[1][0]+30<=IFVs.y<=app.board1.screen[1][1]-30 and\
        (IFVs.identity=="player"or IFVs in app.sighted) and IFVs.health>=0:
            if IFVs in app.playerUnits:
                if IFVs.mountState==True:
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image4))
                elif IFVs.mountState==False:
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image12))
            elif IFVs in app.hostileUnits:
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.image14))
            #canvas.create_oval(x-30,y-30,x+30,y+30,fill='Blue')
            canvas.create_text(x,y,text=f"{IFVs}",fill='Black')
            canvas.create_text(x,y-20,text=f"Health: {IFVs.health}",fill='Black')
            canvas.create_text(x,y+15,text=f"mount: {IFVs.mountState}",fill='Black')
            #canvas.create_text(x,y-15,text=f"firing: {IFVs.firestatus}",fill='Black')
            canvas.create_text(x,y-30,text=f"timer: {IFVs.timer}",fill='Black')
            canvas.create_text(x,y+30,text=f"cover: {IFVs.coverState}",fill='Black')
            canvas.create_text(x,y+20,text=f"target: {IFVs.target}",fill='Black')

# call every draw functions and information for the player
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,2440,2500,fill="grey")
    drawHouse(app,canvas,app.board1.houses)
    drawTank(app,canvas,app.board1.tankList)
    drawIFV(app,canvas,app.board1.ifvList)
    drawTree(app,canvas,app.board1.trees)
    if app.selected is not None:
        canvas.create_text(app.width/2,app.height/2+20,text=
    f"{app.selected.target}",fill="black")

    if len(app.playerUnits)==0 or len(app.hostileUnits)==0:
        canvas.create_text(app.width/2,app.height/2,text="Game Over",fill="Red")
    else:
        canvas.create_text(app.width/2,app.height/2,text=
    f"Frame {app.moved_x},{app.moved_y}, {app.board1.screen}",fill="black")
        canvas.create_text(app.width/2,app.height/2-30,text=
    f"Selected object{app.selected}",fill="black")
        canvas.create_text(app.width/2,app.height/2-50,text=
    f"{app.sighted}",fill="black")
    
    
# call everything===============================================================
def main():
    runApp(width=1440, height=763)

if __name__ == '__main__':
    main()
