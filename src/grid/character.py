from pandac.PandaModules import CardMaker
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import NodePath, TextureStage
from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import BoundingSphere, Point3
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
        self.currentlydown = 0
        
        #public props
        self.node = NodePath("characternode")
        self.node.setTwoSided(True)
        
        self.wtop = loader.loadModel(resourceManager.getResource(name)+'/wtop.egg')
        self.wdown = loader.loadModel(resourceManager.getResource(name)+'/wdown.egg')
        self.wleft = loader.loadModel(resourceManager.getResource(name)+'/wleft.egg')
        self.wright = loader.loadModel(resourceManager.getResource(name)+'/wright.egg')
        self.stop = loader.loadModel(resourceManager.getResource(name)+'/stop.egg')
        self.sdown = loader.loadModel(resourceManager.getResource(name)+'/sdown.egg')
        self.sleft = loader.loadModel(resourceManager.getResource(name)+'/sleft.egg')
        self.sright = loader.loadModel(resourceManager.getResource(name)+'/sright.egg')
        
        self.wtop.reparentTo(self.node)
        self.wdown.reparentTo(self.node)
        self.wleft.reparentTo(self.node)
        self.wright.reparentTo(self.node)
        self.stop.reparentTo(self.node)
        self.sdown.reparentTo(self.node)
        self.sleft.reparentTo(self.node)
        self.sright.reparentTo(self.node)
        
        if playable=="true":
            self.setPlayable(True)
            self.setCollisions(True)
        else:
            self.setPlayable(False)
        
        self.node.setX((-32/2)+0.5)
        self.node.setP(-(360-int(inclination)))
        self.node.setScale(float(scale))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
    
    def setCollisions(self, value):
        if value == True:
            print "setting collisions"
            b = self.node.getBounds().getRadius()
            
            self.cTrav = CollisionTraverser()
            
            self.collisionTube = CollisionSphere(b/2,0,b/2,0.035)
            self.collisionNode = CollisionNode('characterTube')
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNode.setFromCollideMask(BitMask32.bit(0))
            self.collisionNode.setIntoCollideMask(BitMask32.allOff())
            self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
            self.collisionHandler = CollisionHandlerQueue()
            self.cTrav.addCollider(self.collisionNodeNp, self.collisionHandler)

            # Uncomment this line to see the collision rays
            self.collisionNodeNp.show()
        
            # Uncomment this line to show a visual representation of the 
            # collisions occuring
            self.cTrav.showCollisions(render)
    
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
        self.wtop.hide()
        self.wdown.hide()
        self.wleft.hide()
        self.wright.hide()
        self.stop.hide()
        self.sdown.hide()
        self.sleft.hide()
        self.sright.hide()
    
    def setMovement(self, value):
        if value == True:
            if self.movtask == 0:
                self.movtask = taskMgr.add(self.moveCharacter, "moveCharacterTask")
        if value == False:
            if self.movtask != 0:
                if self.currentlydown == 0:
                    taskMgr.remove(self.movtask)
                    self.movtask = 0
    
    def clearMovement(self):
        self.leftdown = False
        self.rightdown = False
        self.topdown = False
        self.downdown = False
        
    
    def arrowLeftDown(self):
        self.clearMovement()
        #track key down
        self.leftdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wleft.show()
        self.currentlydown += 1
    def arrowLeftUp(self):
        self.leftdown = False
        self.setMovement(False)
        #show changes to screen
        if self.currentlydown == 1:
            self.hideAllSubnodes()
            self.sleft.show()
        self.currentlydown -= 1
    
    def arrowRightDown(self):
        self.clearMovement()
        #track key down
        self.rightdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wright.show()
        self.currentlydown += 1
    def arrowRightUp(self):
        self.setMovement(False)
        self.rightdown = False
        #show changes to screen
        if self.currentlydown == 1:
            self.hideAllSubnodes()
            self.sright.show()
        self.currentlydown -= 1
    
    def arrowDownDown(self):
        self.clearMovement()
        #track key down
        self.downdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wdown.show()
        self.currentlydown += 1
    def arrowDownUp(self):
        self.downdown = False
        self.setMovement(False)
        #show changes to screen
        if self.currentlydown == 1:
            self.hideAllSubnodes()
            self.sdown.show()
        self.currentlydown -= 1
    
    def arrowUpDown(self):
        self.clearMovement()
        #track key down
        self.topdown = True
        self.setMovement(True)
        #show changes to screen
        self.hideAllSubnodes()
        self.wtop.show()
        self.currentlydown += 1
    def arrowUpUp(self):
        self.topdown = False
        self.setMovement(False)
        #show changes to screen
        if self.currentlydown == 1:
            self.hideAllSubnodes()
            self.stop.show()
        self.currentlydown -= 1
    
    def moveCharacter(self, task):
        dt = globalClock.getDt()
        if self.leftdown == True:
            self.node.setX(self.node.getX()-1*dt)
        if self.rightdown == True:
            self.node.setX(self.node.getX()+1*dt)
        if self.topdown == True:
            self.node.setZ(self.node.getZ()+1*dt)
        if self.downdown == True:
            self.node.setZ(self.node.getZ()-1*dt)
        
        #check collisions
        self.cTrav.traverse(render)
        
        return Task.cont
    
    def setX(self, x):
        self.node.setX(x)
    
    def setY(self, y):
        self.node.setZ(y)
