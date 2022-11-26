from cmu_112_graphics import *
import random
# return distance based on x1,x2,y1,y2
def getDistance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5
# the map that the player is playing on
class Board():
    # takes the tank, IFV, argillery, and obstacles objects in lists
    def __init__(self, tankList,ifvList,artList,obstacles):
        self.tankList=tankList # tanks objects on the map
        self.ifvList=ifvList #IFV objects on the map
        self.artList=artList #artillery objects on the map
        self.obstacles=obstacles #obstacles object on the map
        self.width = 3000 #map width
        self.height = 4000 #map height
        self.backgroundColor="green" # ground color
        self.screen=[[0,1440],[0,763]]  #current viewing range x and y
    # change the viewing range
    def changeScreen(self,moved_x,moved_y):
        self.screen[0][0]+=moved_x
        self.screen[0][1]+=moved_x
        self.screen[1][0]+=moved_y
        self.screen[1][1]+=moved_y
    # get the tank object
    def getTank(self,x,y):
        for tank in self.tankList:
            if abs(x-tank.x)<=30 and abs(y-tank.y)<=30:
                return tank
        return None
    # get the IFV object
    def getIFV(self,x,y):
        for ifv in self.ifvList:
            if abs(x-ifv.x)<=30 and abs(y-ifv.y)<=30:
                return ifv
        return None
    # get the Arrtillery object
    def getART(self,id):
        pass
    # get the obstacle object
    def getObs(self,id):
        pass

class Tank():
    def __init__(self,x,y,coverState,identity,id):
        self.x=x
        self.y=y
        self.health=2000
        self.damage=100
        self.coverState=coverState
        self.speed=15
        self.firingRate=800
        self.range=1200
        self.identity=identity
        self.id=id
    # firing weapons
    def firing(self):
        return self.damage
    # change the current location of the object
    def changeLoc(self,x,y):
        self.x=x
        self.y=y
    # take damage from the enemy
    def takeDamage(self,damage,distance):
        if self.coverState==False:
            # 80% chance of direct hit in open field
            if random.randint(1,10) not in (1,2):
                #if in open field damage decreases as 1/x
                realDamage=1/(distance+(1/damage))
                self.health=self.health-realDamage
            else:
                return None
        else:
            #if the tank is in cover, only 0.3 chance to land a hit
            if random.randint(1,10) in (1,2,3):
                realDamage=(1/(distance+(1/damage)))
                self.health=self.health-realDamage
            else:
                return None
    def __repr__(self):
        return f'Tank{self.id}:{self.x},{self.y}'
    def __hash__(self):
        return hash((self.id,self.identity))

class IFV():
    def __init__(self,x,y,coverState,identity,id):
        self.x=x
        self.y=y
        self.health=1000
        self.damage=50
        self.coverState=coverState
        #is mountState is True, the infantry is mounted on the vehicle
        self.mountState=True
        self.speed=20
        self.firingRate=300
        self.range=1000
        self.identity=identity
        self.id=id
    # change the current location of the object
    def changeLoc(self,x,y):
        self.x=x
        self.y=y
    # take damage from the enemy
    def takeDamage(self,damage,distance):
        # in cover and mounted reduce chance of being hit
        if self.coverState==False and self.mountState==True:
            # 70% chance of direct hit in open field
            if random.randint(1,10) not in (1,2,3):
                #damage decreases as 1/x 
                realDamage=1/(distance+(1/damage))
                self.health=self.health-realDamage
            else:
                return None
        elif self.coverState==False and self.mountState==False:
            # 80% chance of direct hit in open field
            if random.randint(1,10) not in (1,2):
                #damage decreases as 1/x 
                realDamage=1/(distance+(1/damage))
                self.health=self.health-realDamage
            else:
                return None
        else:
            #if the tank is in cover, only 0.2 chance to land a hit
            if random.randint(1,10) in (1,2):
                realDamage=(1/(distance+(1/damage)))
                self.health=self.health-realDamage
            else:
                return None
    # firing weapons
    def firing(self):
        return self.damage
    # mismount or mount the infantry in the IFV
    def changeMountState(self,mountState):
        if mountState==False:
            self.damage=200
            self.firingRate=500
            self.mountState=mountState
            self.speed=10
            self.range=1400
        else:
            self.damage=50
            self.mountState=mountState
            self.speed=25
            self.firingRate=300
            self.range=1000
    def __repr__(self):
        return f'IFV{self.id}:{self.x},{self.y}'
    def __hash__(self):
        return hash((self.id,self.identity))
        
class Artillery():
    def __init__(self,x,y,coverState,identity,id):
        self.x=x
        self.y=y
        self.health=2000
        self.damage=100
        self.damgaeArea=30
        self.coverState=coverState
        self.speed=15
        self.firingRate=500
        self.range=2000
        self.identity=identity
        self.id=id
    # firing weapons
    def firing(self):
        pass
    # change the current location of the object
    def changeLoc(self,x,y):
        self.x=x
        self.y=y
    # take damage from the enemy
    def takeDamage(self,damage,distance):
        if self.coverState==False:
            # 80% chance of direct hit in open field
            if random.randint(1,10) not in (1,2):
                #if in open field damage decreases as 1/x
                realDamage=1/(distance+(1/damage))
                self.health=self.health-realDamage
            else:
                return None
        else:
            #if the artillery is in cover, only 0.3 chance to land a hit
            if random.randint(1,10) in (1,2,3):
                realDamage=(1/(distance+(1/damage)))
                self.health=self.health-realDamage
            else:
                return None
    def __repr__(self):
        return f'Tank{self.id}:{self.x},{self.y}'
    def __hash__(self):
        return hash((self.id,self.identity))

def directVision(x1,y1,x2,y2):
    pass
class Tree():
    def __init__(self,x,y,id):
        self.x=x
        self.y=y
        self.id=id
        # if entity is false, the obstacle will block vision but not stop shells
        self.entity=False
    def inCover(self,x,y,enemyX,enemyY):
        if getDistance(x,y,self.x,self.y)<=40:
            pass
    def __hash__(self):
        return hash(self.id)

class House():
    def __init__(self,x,y,id):
        self.x=x
        self.y=y
        self.id=id
        # if entity is false, the obstacle will block vision but not stop shells
        # if the entity is True, the obstacle will block vision and stop shells
        self.entity=True
    def inCover(self,x,y,enemyX,enemyY):
        if getDistance(x,y,self.x,self.y)<=40:
            pass
    def __hash__(self):
        return hash(self.id)
