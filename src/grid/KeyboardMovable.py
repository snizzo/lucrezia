
# copy paste imports from main.py
#panda imports
from direct.showbase.DirectObject import DirectObject 
from panda3d.core import Point3
from direct.task import Task

#libs imports

#lucrezia imports
from grid.LoadPoint import LoadPoint
from grid.Movable import Movable

#from utils.once import Once
from utils.misc import Misc

class KeyboardMovable(Movable, DirectObject):

    def __init__(self):
        pass
    
    def setMovable(self, value, speed = 0.1):
        """
        Sets the correct input / ignore events of the movable object 
        """
        if not self.isSetMovableNode():
            if not self.autoSetMovableNode():
                if debug:
                    print("ERROR: failed to activate movable object, no node set and auto set node failed.")
                return
            else:
                if debug:
                    print("WARNING: keyboardmovable node has been auto set, can cause problems...")
        
        # set some util variables here, like in a class constructor
        self.movableSpeed = speed

        if value == True:
            self.accept("arrow_up", self.startMoveUp)
            self.accept("arrow_up-up", self.stopMoveUp)
            self.accept("arrow_down", self.startMoveDown)
            self.accept("arrow_down-up", self.stopMoveDown)
            self.accept("arrow_left", self.startMoveLeft)
            self.accept("arrow_left-up", self.stopMoveLeft)
            self.accept("arrow_right", self.startMoveRight)
            self.accept("arrow_right-up", self.stopMoveRight)
        else:
            self.ignore("arrow_up")
            self.ignore("arrow_up-up")
            self.ignore("arrow_down")
            self.ignore("arrow_down-up")
            self.ignore("arrow_left")
            self.ignore("arrow_left-up")
            self.ignore("arrow_right")
            self.ignore("arrow_right-up")

    # TODO: implement continuos movement
    def stopMoveUp(self):
        pass

    def stopMoveDown(self):
        pass
    
    def stopMoveLeft(self):
        pass
    
    def stopMoveRight(self):
        pass   

    # TODO: get rid of duplicate code
    def startMoveUp(self):
        originalX = self.movableNode.getPos().getX()
        originalY = self.movableNode.getPos().getY()
        originalZ = self.movableNode.getPos().getZ()
        self.movableNode.setPos(originalX,originalY,originalZ+self.movableSpeed)

    def startMoveDown(self):
        originalX = self.movableNode.getPos().getX()
        originalY = self.movableNode.getPos().getY()
        originalZ = self.movableNode.getPos().getZ()
        self.movableNode.setPos(originalX,originalY,originalZ-self.movableSpeed)

    def startMoveLeft(self):
        originalX = self.movableNode.getPos().getX()
        originalY = self.movableNode.getPos().getY()
        originalZ = self.movableNode.getPos().getZ()
        self.movableNode.setPos(originalX-self.movableSpeed,originalY,originalZ)

    def startMoveRight(self):
        originalX = self.movableNode.getPos().getX()
        originalY = self.movableNode.getPos().getY()
        originalZ = self.movableNode.getPos().getZ()
        self.movableNode.setPos(originalX+self.movableSpeed,originalY,originalZ)