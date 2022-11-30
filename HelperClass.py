from cmu_112_graphics import *
import random
# return distance based on x1,x2,y1,y2
def getDistance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5
# the map that the player is playing on
class Board():
    # takes the tank, IFV, argillery, and obstacles objects in lists
    def __init__(self, tankList,ifvList,artList,trees,houses):
        self.tankList=tankList # tanks objects on the map
        self.ifvList=ifvList #IFV objects on the map
        self.artList=artList #artillery objects on the map
        self.trees=trees #Tree object on the map
        self.houses=houses #Tree object on the map
        self.width = 2440 #map width
        self.height = 2500 #map height
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
    def getART(self,x,y):
        pass
    # get the obstacle object
    def getHouses(self,x,y):
        for house in self.houses:
            if house.x-house.width<=x<=house.x+house.width and house.y-house.height<=y<=house.y+house.height:
                return house
        return None

class Tank():
    def __init__(self,x,y,coverState,identity,id):
        self.x=x
        self.y=y
        self.health=2000
        self.damage=400
        self.coverState=coverState
        self.speed=15
        self.firingRate=800
        # sight range
        self.range=1200
        # indicate player or enemy
        self.identity=identity
        # used for hashing
        self.id=id
        # count reload time
        self.timer=0
        # whether the unit is ready to fire
        self.firestatus=False
        # the unit being fired uppon by this unit
        self.target=None
        # the other enemy unit that this unit can see
        self.sight=set()

    # change the current location of the object
    def changeLoc(self,x,y):
        self.x=x
        self.y=y
    # firing weapons
    def firing(self):
        if self.target is not None:
            if self.firestatus==True:
                self.timer=0
                self.firestatus=False
                return self.damage
            elif self.timer>=self.firingRate:
                self.firestatus=True
                return 0
            else:
                self.timer+=10
                return 0       
        elif self.target is None:
            if self.timer<self.firingRate:
                self.timer+=10
                return 0
            elif self.timer==self.firingRate:
                self.firestatus=True
                return 0
    
    # take damage from the enemy
    def takeDamage(self,damage,distance):
        if self.coverState==False:
            # 80% chance of direct hit in open field
            if random.randint(1,10) not in (1,2):
                #if in open field damage decreases as 1/x
                realDamage=damage*(2**(-distance/1000))
                self.health=self.health-realDamage
            else:
                return None
        else:
            #if the tank is in cover, only 0.4 chance to land a hit
            if random.randint(1,10) in (1,2,3,4):
                realDamage=damage*(2**(-distance/1000))
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
        self.firingRate=50
        # sight range
        self.range=1000
        # indicate player or enemy
        self.identity=identity
        # used for hashing
        self.id=id
        # count reload time
        self.timer=0
        # the unit being fired uppon by this unit
        self.target=None
        # whether the unit is ready to fire
        self.firestatus=False
        # the other enemy unit that this unit can see
        self.sight=set()

    # change the current location of the object
    def changeLoc(self,x,y):
        self.x=x
        self.y=y

    # firing weapons
    def firing(self):
        if self.target is not None:
            if self.firestatus==True:
                self.timer=0
                self.firestatus=False
                return self.damage
            elif self.timer>=self.firingRate:
                self.firestatus=True
                return 0
            else:
                self.timer+=10
                return 0       
        elif self.target is None:
            if self.timer<self.firingRate:
                self.timer+=10
                return 0
            elif self.timer==self.firingRate:
                self.firestatus=True
                return 0

    # take damage from the enemy
    def takeDamage(self,damage,distance):
        # in cover and mounted reduce chance of being hit
        if self.coverState==False and self.mountState==True:
            # 70% chance of direct hit in open field
            if random.randint(1,10) not in (1,2,3):
                #damage decreases exponencially  
                realDamage=damage*(2**(-distance/1000))
                self.health=self.health-realDamage
            else:
                return None
        elif self.coverState==False and self.mountState==False:
            # 80% chance of direct hit in open field
            if random.randint(1,10) not in (1,2):
                #damage decreases as 1/x 
                realDamage=damage*(2**(-distance/1000))
                self.health=self.health-realDamage
            else:
                return None
        else:
            #if the tank is in cover, only 0.4 chance to land a hit
            if random.randint(1,10) in (1,2,3,4):
                realDamage=damage*(2**(-distance/1000))
                self.health=self.health-realDamage
            else:
                return None

    # mismount or mount the infantry in the IFV
    def changeMountState(self,mountState):
        if mountState==False:
            self.damage=250
            self.firingRate=250
            self.mountState=mountState
            self.speed=10
            self.range=1400
        else:
            self.damage=50
            self.mountState=mountState
            self.speed=25
            self.firingRate=50
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
        # indicate player or enemy
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


class Tree():
    def __init__(self,x,y,id):
        self.x=x
        self.y=y
        self.id=id
        # if entity is false, the obstacle can be overlapped and doesnot stop shells
        self.entity=False
    def inCover(self,x,y):
        if  self.x-(60+60)<=x<=self.x+(60+60) and \
            self.y-(60+60)<=y<=self.y+(60+60):
            return True
        else: 
            return False
    def __hash__(self):
        return hash(self.id)
    def __repr__(self):
        return f'Tree{self.id}:{self.x},{self.y}'

class House():
    def __init__(self,x,y,width,height,id):
        self.x=x
        self.y=y
        self.id=id
        #half width of the rectangle
        self.width=width
        #half height of the rectangle
        self.height=height
        # if entity is false, the obstacle can be overlapped and doesnot stop shells
        # if the entity is True, the obstacle will block vision and stop shells
        self.entity=True

    def inCover(self,x,y):
        if  self.x-(self.width+60)<=x<=self.x+(self.width+60) and \
            self.y-(self.height+60)<=y<=self.y+(self.height+60):
            return True
        else: 
            return False

    def __hash__(self):
        return hash(self.id)
    def __repr__(self):
        return f'House{self.id}:{self.x},{self.y}'

