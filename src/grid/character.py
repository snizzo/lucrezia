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
    
    def __init__(self, attributes, showCollisions):
        #name, inclination, scale, playable
        #res.attributes['url'].value, res.attributes['inclination'].value, res.attributes['scale'].value, res.attributes['playable'].value
        if attributes.has_key('url'):
            self.name = name = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            self.name = name = 'misc/placeholder'
        
        if attributes.has_key('inclination'):
            self.inclination = inclination = float(attributes['inclination'].value)
        else:
            self.inclination = inclination = 30.0
        
        if attributes.has_key('scale'):
            self.scale = scale = float(attributes['scale'].value)
        else:
            self.scale = scale = 1.0
        
        if attributes.has_key('hitboxscale'):
            self.hitboxscale = float(attributes['hitboxscale'].value)
        else:
            self.hitboxscale = 1.0
        
        if attributes.has_key('speed'):
            self.speed = float(attributes['speed'].value)
        else:
            self.speed = 1.0
        
        if attributes.has_key('playable'):
            self.playable = playable = attributes['playable'].value
        else:
            self.playable = playable = "false"
        
        if attributes.has_key('direction'):
            self.direction = attributes['direction'].value
        else:
            self.direction = "down"
        
        #movement
        self.state = "still"
        self.showCollisions = showCollisions
        
        self.movtask = 0
        self.currentlydown = []
        self.currentlyfollowed = 0
        
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
            self.setPlayable(False) #seems nonsense, triggered on grid.changeMap event
            self.node.setTag("playable", "true") #setting this to make it recognizable from grid changeMap api
            self.setCollisions(True)
        else:
            self.setPlayable(False)
            self.node.setTag("playable", "false")
        
        #self.node.setX((-32/2)+0.5)
        self.node.setP(-(360-int(inclination)))
        self.node.setScale(float(scale))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        
        self.lastpos = self.node.getPos()
        
        self.face(self.direction)
        
        self.node.setPythonTag("gamenode", self)
        
        
    def face(self, direction):
        if direction == "left":
            self.hideAllSubnodes()
            self.sleft.show()
        if direction == "right":
            self.hideAllSubnodes()
            self.sright.show()
        if direction == "top":
            self.hideAllSubnodes()
            self.stop.show()
        if direction == "down":
            self.hideAllSubnodes()
            self.sdown.show()
    
    def setCollisions(self, value):
        if value == True:
            print "setting collisions"
            b = self.node.getBounds().getRadius()
            
            self.cTrav = CollisionTraverser()
            
            self.collisionTube = CollisionSphere(b/2,0,b/2,0.035*self.hitboxscale)
            self.collisionNode = CollisionNode('characterTube')
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
            self.collisionHandler = CollisionHandlerQueue()
            self.cTrav.addCollider(self.collisionNodeNp, self.collisionHandler)
            
            if self.showCollisions == True:
                # Uncomment this line to see the collision rays
                self.collisionNodeNp.show()
                
                # Uncomment this line to show a visual representation of the 
                # collisions occuring
                self.cTrav.showCollisions(render)
    
    #set if camera has to effectively follow the character
    #while it moves
    def setFollowedByCamera(self, value):
        #camera follow
        if value:
            if self.currentlyfollowed!=True:
                customCamera.follow(self.node)
                self.currentlyfollowed = True
        else:
            if self.currentlyfollowed!=False:
                customCamera.dontFollow()
                self.currentlyfollowed = False
    
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
            self.node.setTag("playable", "true")
            self.setFollowedByCamera(True)
        else:
            self.ignoreAll()
            self.node.setTag("playable", "false")
            self.setFollowedByCamera(False)
    
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
                if len(self.currentlydown) == 0:
                    taskMgr.remove(self.movtask)
                    self.movtask = 0
    
    def setAnim(self):
        self.hideAllSubnodes()
        
        if len(self.currentlydown) > 0:
            if self.currentlydown[-1] == 'left':
                self.wleft.show()
            if self.currentlydown[-1] == 'right':
                self.wright.show()
            if self.currentlydown[-1] == 'top':
                self.wtop.show()
            if self.currentlydown[-1] == 'down':
                self.wdown.show()
        
        
    
    def arrowLeftDown(self):
        #track key down
        self.leftdown = True
        self.setMovement(True)
        #show changes to screen
        self.currentlydown.append("left")
        self.setAnim()
    def arrowLeftUp(self):
        self.leftdown = False
        self.setMovement(False)
        #show changes to screen
        if len(self.currentlydown) == 1:
            self.hideAllSubnodes()
            self.sleft.show()
        if "left" in self.currentlydown:
            self.currentlydown.remove("left")
        
        if len(self.currentlydown) > 0:
            self.setAnim()
    
    def arrowRightDown(self):
        #track key down
        self.rightdown = True
        self.setMovement(True)
        #show changes to screen
        self.currentlydown.append("right")
        self.setAnim()
    def arrowRightUp(self):
        self.setMovement(False)
        self.rightdown = False
        #show changes to screen
        if len(self.currentlydown) == 1:
            self.hideAllSubnodes()
            self.sright.show()
        if "right" in self.currentlydown:
            self.currentlydown.remove("right")
        
        if len(self.currentlydown) > 0:
            self.setAnim()
    
    def arrowDownDown(self):
        #track key down
        self.downdown = True
        self.setMovement(True)
        #show changes to screen
        self.currentlydown.append("down")
        self.setAnim()
    def arrowDownUp(self):
        self.downdown = False
        self.setMovement(False)
        #show changes to screen
        if len(self.currentlydown) == 1:
            self.hideAllSubnodes()
            self.sdown.show()
        if "down" in self.currentlydown:
            self.currentlydown.remove("down")
        
        if len(self.currentlydown) > 0:
            self.setAnim()
    
    def arrowUpDown(self):
        #track key down
        self.topdown = True
        self.setMovement(True)
        #show changes to screen
        self.currentlydown.append("top")
        self.setAnim()
    def arrowUpUp(self):
        self.topdown = False
        self.setMovement(False)
        #show changes to screen
        if len(self.currentlydown) == 1:
            self.hideAllSubnodes()
            self.stop.show()
        if "top" in self.currentlydown:
            self.currentlydown.remove("top")
        if len(self.currentlydown) > 0:
            self.setAnim()
    
    def moveCharacter(self, task):
        
        dt = globalClock.getDt()
        if len(self.currentlydown) > 0:
            if self.currentlydown[-1] == 'left':
                self.node.setX(self.node.getX()-1*dt*self.speed)
            if self.currentlydown[-1] == 'right':
                self.node.setX(self.node.getX()+1*dt*self.speed)
            if self.currentlydown[-1] == 'top':
                self.node.setZ(self.node.getZ()+1*dt*self.speed)
            if self.currentlydown[-1] == 'down':
                self.node.setZ(self.node.getZ()-1*dt*self.speed)
        
        #check collisions
        self.cTrav.traverse(render)
        
        if self.collisionHandler.getNumEntries() == 0:
            self.lastpos = self.node.getPos()
        else:
            self.node.setPos(self.lastpos)
            sp = self.collisionHandler.getEntry(0).getSurfacePoint(self.node) #surface point
            objectNode = self.collisionHandler.getEntry(0).getIntoNodePath().getParent() #into object node
            
            #if node is a real object (not a wall)
            if objectNode.hasTag("xscaled") and objectNode.hasTag("yscaled"):
                if len(self.currentlydown) > 0: #at least 1, avoids list index out of range exception
                    if self.currentlydown[-1] == 'left' or self.currentlydown[-1] == 'right':
                        bottomObjPos = objectNode.getZ()-(float(objectNode.getTag("yscaled"))/2)
                        topObjPos = objectNode.getZ()+(float(objectNode.getTag("yscaled"))/2)
                        if self.node.getZ() < bottomObjPos:
                            print "SHIFTBOTTOM"
                            self.node.setZ(self.node.getZ()-1*dt*self.speed)
                        if self.node.getZ() > topObjPos:
                            print "SHIFTTOP"
                            self.node.setZ(self.node.getZ()+1*dt*self.speed)
                        pass
                    if self.currentlydown[-1] == 'top' or self.currentlydown[-1] == 'down':
                        leftObjPos = objectNode.getX()-(float(objectNode.getTag("xscaled"))/2)
                        rightObjPos = objectNode.getX()+(float(objectNode.getTag("xscaled"))/2)
                        
                        if self.node.getX() < leftObjPos:
                            print "SHIFTLEFT"
                            self.node.setX(self.node.getX()-1*dt*self.speed)
                            
                        if self.node.getX() > rightObjPos:
                            print "SHIFTRIGHT"
                            self.node.setX(self.node.getX()+1*dt*self.speed)
                    self.lastpos = self.node.getPos()
            
        
        for i in range(self.collisionHandler.getNumEntries()):
            entry = self.collisionHandler.getEntry(i)
            objectNode = entry.getIntoNodePath().getParent()
            onWalked = objectNode.getTag("onWalked")
            if len(onWalked)>0:
                eval(onWalked)
        
        return Task.cont
    
    def setX(self, x):
        self.node.setX(x)
    
    def setY(self, y):
        self.node.setZ(y)
