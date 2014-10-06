from pandac.PandaModules import CardMaker
from panda3d.core import NodePath, TextureStage
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import UvScrollNode
from direct.task import Task

from direct.showbase.DirectObject import DirectObject

class Character(DirectObject):
    
    def __init__(self, name, inclination, scale, playable):
        #movement
        self.state = "still"
        self.direction = "down"
        
        self.leftdown = False
        self.rightdown = False
        self.topdown = False
        self.downdown = False
        
        self.movtask = 0
        
        #public props
        self.node = NodePath("characternode")
        self.node.setTwoSided(True)
        
        self.wtop = loader.loadModel('../res/'+name+'/wtop.egg')
        self.wdown = loader.loadModel('../res/'+name+'/wdown.egg')
        self.wleft = loader.loadModel('../res/'+name+'/wleft.egg')
        self.wright = loader.loadModel('../res/'+name+'/wright.egg')
        self.stop = loader.loadModel('../res/'+name+'/stop.egg')
        self.sdown = loader.loadModel('../res/'+name+'/sdown.egg')
        self.sleft = loader.loadModel('../res/'+name+'/sleft.egg')
        self.sright = loader.loadModel('../res/'+name+'/sright.egg')
        
        self.wtop.reparentTo(self.node)
        self.wdown.reparentTo(self.node)
        self.wleft.reparentTo(self.node)
        self.wright.reparentTo(self.node)
        self.stop.reparentTo(self.node)
        self.sdown.reparentTo(self.node)
        self.sleft.reparentTo(self.node)
        self.sright.reparentTo(self.node)
        
        self.node.setX((-32/2)+0.5)
        self.node.setP(-(360-int(inclination)))
        self.node.setScale(float(scale))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        
        if playable=="true":
            self.setPlayable(True)
        else:
            self.setPlayable(False)
    
    #used to set playability in real time
    #useful when we want to switch context/scripted scenes
    def setPlayable(self, value):
        if value == True:
            #down events
            self.accept("arrow_left", self.arrowLeftDown)
            self.accept("arrow_right", self.arrowRightDown)
            self.accept("arrow_up", self.arrowUpDown)
            self.accept("arrow_down", self.arrowDownDown)
            #up events
            self.accept("arrow_left-up", self.arrowLeftUp)
            self.accept("arrow_right-up", self.arrowRightUp)
            self.accept("arrow_up-up", self.arrowUpUp)
            self.accept("arrow_down-up", self.arrowDownUp)
        else:
            self.ignoreAll()
    
    def hideAllSubnodes(self):
        for n in self.node.getChildren():
            n.hide()
    
    def setMovement(self, value):
        if value == True:
            if self.movtask == 0:
                self.movtask = taskMgr.add(self.moveCharacter, "moveCharacterTask")
        if value == False:
            if self.movtask != 0:
                taskMgr.remove(self.movtask)
                self.movtask = 0
    
    def arrowLeftDown(self):
        #track key down
        self.leftdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wleft.show()
    def arrowLeftUp(self):
        self.leftdown = False
        self.setMovement(False)
        #show changes to screen
        self.hideAllSubnodes()
        self.sleft.show()
    
    def arrowRightDown(self):
        #track key down
        self.rightdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wright.show()
    def arrowRightUp(self):
        self.setMovement(False)
        self.rightdown = False
        #show changes to screen
        self.hideAllSubnodes()
        self.sright.show()
    
    def arrowDownDown(self):
        #track key down
        self.downdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wdown.show()
    def arrowDownUp(self):
        self.downdown = False
        self.setMovement(False)
        #show changes to screen
        self.hideAllSubnodes()
        self.sdown.show()
    
    def arrowUpDown(self):
        #track key down
        self.topdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wtop.show()
    def arrowUpUp(self):
        self.topdown = False
        self.setMovement(False)
        #show changes to screen
        self.hideAllSubnodes()
        self.stop.show()
    
    def moveCharacter(self, task):
        if self.leftdown == True:
            self.node.setX(self.node.getX()-0.01)
        if self.rightdown == True:
            self.node.setX(self.node.getX()+0.01)
        if self.topdown == True:
            self.node.setZ(self.node.getZ()+0.01)
        if self.downdown == True:
            self.node.setZ(self.node.getZ()-0.01)
        return Task.cont
    
    def setX(self, x):
        self.node.setX(x)
    
    def setY(self, y):
        self.node.setZ(y)
