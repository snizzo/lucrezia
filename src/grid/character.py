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
        
        if attributes.has_key('id'):
            self.uid = uid = attributes['id'].value
        else:
            self.uid = uid = 'all'
        
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
        
        #self.isNPC remains true while isPlayable is changable
        if attributes.has_key('playable'):
            self.playable = playable = attributes['playable'].value
            if self.playable == 'false':                
                self.isNPC = False
                print "setting ", self.uid, " to ", self.isNPC
            else:
                self.isNPC = True
                print "setting ", self.uid, " to ", self.isNPC
        else:
            self.playable = playable = 'false'
            self.isNPC = False
        
        if attributes.has_key('direction'):
            self.direction = attributes['direction'].value
        else:
            self.direction = "down"
        
        #defaulted to None
        self.pickCTrav = None
        
        #movement
        self.state = "still"
        self.showCollisions = showCollisions
        
        self.movtask = 0
        self.currentlydown = []
        self.currentlyfollowed = 0
        
        self.pickRequest = False
        
        #public props
        self.node = NodePath("characternode")
        self.node.setTwoSided(True)
        
        self.wtop = loader.loadModel(resourceManager.getResource(name)+'/wtop.bam')
        self.wdown = loader.loadModel(resourceManager.getResource(name)+'/wdown.bam')
        self.wleft = loader.loadModel(resourceManager.getResource(name)+'/wleft.bam')
        self.wright = loader.loadModel(resourceManager.getResource(name)+'/wright.bam')
        self.stop = loader.loadModel(resourceManager.getResource(name)+'/stop.bam')
        self.sdown = loader.loadModel(resourceManager.getResource(name)+'/sdown.bam')
        self.sleft = loader.loadModel(resourceManager.getResource(name)+'/sleft.bam')
        self.sright = loader.loadModel(resourceManager.getResource(name)+'/sright.bam')
        
        self.wtop.reparentTo(self.node)
        self.wdown.reparentTo(self.node)
        self.wleft.reparentTo(self.node)
        self.wright.reparentTo(self.node)
        self.stop.reparentTo(self.node)
        self.sdown.reparentTo(self.node)
        self.sleft.reparentTo(self.node)
        self.sright.reparentTo(self.node)
        
        self.leftdown = False
        self.rightdown = False
        self.downdown = False
        self.topdown = False
        
        if playable=="true":
            self.setPlayable(False) #seems nonsense, triggered on grid.changeMap event
            self.node.setTag("playable", "true") #setting this to make it recognizable from grid changeMap api
            self.setCollisions(True)
            self.setPickCollisions(True)
        else:
            self.setPlayable(False)
            self.node.setTag("playable", "false")
            self.setCollisions(False)
            self.setPickCollisions(False)
        
        #self.node.setX((-32/2)+0.5)
        self.node.setP(-(360-int(inclination)))
        self.node.setScale(float(scale))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        
        self.lastpos = self.node.getPos()
        
        self.showAllSubnodes()
        
        taskMgr.doMethodLater(4, self.face, 'charload'+self.uid, [self.direction])
        #self.face(self.direction)
        
        #set unique id
        self.node.setTag("id", self.uid)
        
        #storing a pointer of the gamenode
        self.node.setPythonTag("gamenode", self)
        
        self.npc_walk_stack = []
        self.npc_walk_happening = False
        self.globalLock = False
    
    '''
    make the npc walk in direction for units
    '''
    def npc_push_walk(self, direction, units):
        #locking script execution
        self.globalLock = True
        script.addOneCustomLock(self)
        
        #start the walking
        self.npc_walk_stack.append([direction, units])
        self.npc_walk_helper()
        
    #apicall
    def npc_walk_helper(self):
        x = self.node.getX()
        y = self.node.getZ()
        
        #concurrent protection
        if self.npc_walk_happening == True:
            return
        
        #returning if no movement has to be performed
        if len(self.npc_walk_stack) < 0:
            return
        
        movement = self.npc_walk_stack.pop(0)
        
        direction = movement[0]
        units = movement[1]
        
        self.npc_targetx = x
        self.npc_targety = y
        self.npc_direction = direction
        
        if(direction=="down"):
            self.npc_targety = self.npc_targety - units
        elif(direction=="up"):
            self.npc_targety = self.npc_targety + units
        elif(direction=="left"):
            self.npc_targetx = self.npc_targetx - units
        elif(direction=="right"):
            self.npc_targetx = self.npc_targetx + units
        
        self.setAnim(direction)
        
        self.npc_walk_happening = True
        self.npc_movtask = taskMgr.add(self.npc_walk_task, "npc_moveCharacterTask"+self.uid, uponDeath=self.npc_walk_callback)
    
    def npc_walk_task(self, task):
        dt = globalClock.getDt()
        
        if(self.npc_direction=='left'):
            self.node.setX(self.node.getX()-1*dt*self.speed)
            currentx = self.node.getX()
            
            if currentx <= self.npc_targetx:
                return task.done
        if(self.npc_direction=='right'):
            self.node.setX(self.node.getX()+1*dt*self.speed)
            currentx = self.node.getX()
            
            if currentx >= self.npc_targetx:
                return task.done
        if(self.npc_direction=='up'):
            self.node.setZ(self.node.getZ()+1*dt*self.speed)
            currenty = self.node.getZ()
            
            if currenty <= self.npc_targety:
                return task.done
        if(self.npc_direction=='down'):
            self.node.setZ(self.node.getZ()-1*dt*self.speed)
            currenty = self.node.getZ()
            
            if currenty <= self.npc_targety:
                return task.done
        
        return task.cont
    
    def npc_walk_callback(self, task):
        self.face(self.npc_direction)
        
        #unlocking concurrent movement protection
        self.npc_walk_happening = False
        
        if len(self.npc_walk_stack) > 0:
            self.npc_walk_helper()
        else: #character ended walking, unlock
            self.globalLock = False
            
    
    '''
    write destroyfunction
    '''
    def destroy(self):
        #not accepting events
        self.ignoreAll()
        #destroying everything down
        self.node.remove_node()
        #removing all tasks
        if self.movtask != 0:
            taskMgr.remove(self.movtask)
            self.movtask = 0
    
    def face(self, direction):
        if direction == "left":
            self.hideAllSubnodes()
            self.sleft.show()
        if direction == "right":
            self.hideAllSubnodes()
            self.sright.show()
        if direction == "top" or direction == "up": #let's keep retrocompatibility
            self.hideAllSubnodes()
            self.stop.show()
        if direction == "down":
            self.hideAllSubnodes()
            self.sdown.show()
    
    def setCollisions(self, value):
        if value == True:
            print "setting collisions"
            b = self.node.getBounds().getRadius()
            
            print "INSTANTIATED"
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
        else:
            b = self.node.getBounds().getRadius()
            self.collisionTube = CollisionSphere(b/2,0,b/2,0.035*self.hitboxscale)
            self.collisionNode = CollisionNode('characterTube')
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
    
    #set if camera has to effectively follow the character
    #while it moves
    def setFollowedByCamera(self, value):
        print "camera"
        print value
        #camera follow
        if value:
            if self.currentlyfollowed!=True:
                customCamera.follow(self.node)
                self.currentlyfollowed = True
        else:
            if self.currentlyfollowed!=False:
                customCamera.dontFollow()
                self.currentlyfollowed = False
    
    def setPickCollisions(self, value):
        if value:
            print "setting pick collisions"
            b = self.node.getBounds().getRadius()
            
            self.pickCTrav = CollisionTraverser()
            
            self.pickCollisionTube = CollisionSphere(b/2,0,b/2,0.035*self.hitboxscale+0.01)
            self.pickCollisionNode = CollisionNode('characterPickTube')
            self.pickCollisionNode.addSolid(self.pickCollisionTube)
            self.pickCollisionNodeNp = NodePath(self.pickCollisionNode)
            self.pickCollisionNodeNp.reparentTo(self.node)
            self.pickCollisionHandler = CollisionHandlerQueue()
            self.pickCTrav.addCollider(self.pickCollisionNodeNp, self.pickCollisionHandler)
            
            
            
            if self.showCollisions == True:
                # Uncomment this line to see the collision rays
                self.pickCollisionNodeNp.show()
                
                # Uncomment this line to show a visual representation of the 
                # collisions occuring
                self.pickCTrav.showCollisions(render)
        else:
            #dereferincing all pick colliders (must be done in order not to collide onto NPCs)
            self.pickCTrav = None
            self.pickCollisionTube = None
            self.pickCollisionNode = None
            self.pickCollisionNodeNp = None
            self.pickCollisionHandler = None
            
    
    #used to set playability in real time
    #useful when we want to switch context/scripted scenes
    def setPlayable(self, value):
        print "SETTING PLAYABLE"
        if self.isNPC != False:
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
                self.accept("space", self.spaceDown)
                self.node.setTag("playable", "true")
                self.setFollowedByCamera(True)
                self.accept("pauseGameplay", self.setPlayable, [False]) #can pause play
            else:
                self.ignoreAll()
                self.node.setTag("playable", "false")
                self.setFollowedByCamera(False)
                self.resetMovement() #reset every movement happening
                self.accept("resumeGameplay", self.setPlayable, [True]) #can resume play if not NPC
    
    #estimate loading time 4 seconds... lol...
    def showAllSubnodes(self):
        self.wtop.show()
        self.wdown.show()
        self.wleft.show()
        self.wright.show()
        self.stop.show()
        self.sdown.show()
        self.sleft.show()
        self.sright.show()
        
    
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
    
    '''
    reset every movement actually happening
    '''
    def resetMovement(self):
        if self.leftdown == True:
            self.face("left")
        if self.rightdown == True:
            self.face("right")
        if self.downdown == True:
            self.face("down")
        if self.topdown == True:
            self.face("top")
        
        self.leftdown = False
        self.rightdown = False
        self.downdown = False
        self.topdown = False
        
        self.currentlydown = []
        
        self.setMovement(False)
    
    def setAnim(self, direction=''):
        self.hideAllSubnodes()
        
        if direction=='':        
            if len(self.currentlydown) > 0:
                if self.currentlydown[-1] == 'left':
                    self.wleft.show()
                if self.currentlydown[-1] == 'right':
                    self.wright.show()
                if self.currentlydown[-1] == 'top':
                    self.wtop.show()
                if self.currentlydown[-1] == 'down':
                    self.wdown.show()
        else:
            if direction=='left':
                self.wleft.show()
            if direction=='right':
                self.wright.show()
            if direction=='up':
                self.wtop.show()
            if direction=='down':
                self.wdown.show()
    
    #pick request function
    def spaceDown(self):
        self.pickRequest = True
        
    #movement related functions
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
        if self.cTrav != None:
            self.cTrav.traverse(render)
        
        if self.pickCTrav != None:
            self.pickCTrav.traverse(render)
        
        #entries python list
        entries = list(self.collisionHandler.getEntries())
        pickentries = list(self.pickCollisionHandler.getEntries())
        
        for e in entries[:]:
            if e.getIntoNodePath().getName() == "characterPickTube":
                entries.remove(e)
        
        for e in pickentries[:]:
            if e.getIntoNodePath().getName() == "characterTube":
                pickentries.remove(e)
        
        if len(entries) == 0:
            self.lastpos = self.node.getPos()
        else:
            self.node.setPos(self.lastpos)
            sp = entries[0].getSurfacePoint(self.node) #surface point
            objectNode = entries[0].getIntoNodePath().getParent() #into object node
            
            #if node is a real object (not a wall)
            if objectNode.hasTag("avoidable"):
                if objectNode.getTag("avoidable") == "true": #see if object is intelligently avoidable
                    if objectNode.hasTag("xscaled") and objectNode.hasTag("yscaled"):
                        if len(self.currentlydown) > 0: #at least 1, avoids list index out of range exception
                            if self.currentlydown[-1] == 'left' or self.currentlydown[-1] == 'right': #TODO: fix the shiet, not always working
                                bottomObjPos = objectNode.getZ()-(float(objectNode.getTag("yscaled"))/2)
                                topObjPos = objectNode.getZ()+(float(objectNode.getTag("yscaled"))/2)
                                if self.node.getZ() < bottomObjPos:
                                    self.node.setZ(self.node.getZ()-1*dt*self.speed)
                                if self.node.getZ() > topObjPos:
                                    self.node.setZ(self.node.getZ()+1*dt*self.speed)
                                pass
                            if self.currentlydown[-1] == 'top' or self.currentlydown[-1] == 'down':
                                leftObjPos = objectNode.getX()-(float(objectNode.getTag("xscaled"))/2)
                                rightObjPos = objectNode.getX()+(float(objectNode.getTag("xscaled"))/2)
                                
                                if self.node.getX() < leftObjPos:
                                    self.node.setX(self.node.getX()-1*dt*self.speed)
                                    
                                if self.node.getX() > rightObjPos:
                                    self.node.setX(self.node.getX()+1*dt*self.speed)
                            self.lastpos = self.node.getPos()
            
        
        for entry in entries:
            objectNode = entry.getIntoNodePath().getParent()
            onWalked = objectNode.getTag("onWalked")
            if len(onWalked)>0:
                eval(onWalked) #oh lol, danger detected here
        
        for entry in pickentries:
            if self.pickRequest == True:
                self.pickRequest = False #resetting request
                objectNode = entry.getIntoNodePath().getParent()
                onPicked = objectNode.getTag("onPicked")
                if len(onPicked)>0:
                    eval(onPicked) #oh lol, danger detected again here
                else:
                    print "WARNING: picking on this object is not defined"
        
        #this is needed for empty pick
        if self.pickRequest == True:
            self.pickRequest = False #resetting request
        
        return Task.cont
    
    def setX(self, x):
        self.node.setX(x)
        self.lastpos.setX(x)
    
    def setY(self, y):
        self.node.setZ(y)
        self.lastpos.setZ(y)
