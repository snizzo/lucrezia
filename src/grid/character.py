from pandac.PandaModules import CardMaker
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import NodePath, TextureStage, Texture
from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import BoundingSphere, Point3
from panda3d.core import UvScrollNode
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

from direct.showbase.DirectObject import DirectObject

from grid.CharacterEmotions import CharacterEmotions
from grid.XMLExportable import XMLExportable
from grid.GameEntity import GameEntity
from editor.gui.PropertiesTableAbstract import PropertiesTableAbstract
from grid.Pausable import Pausable
from grid.Entity import Entity

import sys

class Character(DirectObject, XMLExportable, PropertiesTableAbstract, GameEntity, Pausable, CharacterEmotions):
    
    def __init__(self, attributes, showCollisions, grid_currentx, grid_currenty, grid_playable_pos, parent):
        GameEntity.__init__(self, parent) #running parent constructor


        self.playable = False #defaulting to false
        self.cinematic = False #defaulting to false
        self.footSound = None
        self.movtask = 0
        self.showCollisions = showCollisions
        self.grid_currentx = grid_currentx
        self.grid_currenty = grid_currenty
        self.grid_playable_pos = grid_playable_pos
        self.attributes = attributes
        self.onPicked = ''
        self.onWalked = ''
        self.typeName = 'character'
        
        self.properties = {
            'url' : '',
            'onWalked' : '',
            'onPicked' : '',
            'id' : '',
            'inclination' : '',
            'scale' : '',
            'hitboxscale' : '',
            'speed' : '',
            'playable' : '',
            'direction' : '',
            'footsteps' : ''
        }
        
        self.propertiesUpdateFactor = {
            'inclination' : 0.2,
            'scale' : 0.1,
            'hitboxscale' : 0.1,
            'speed' : 0.1
        }
        
        if 'url' in attributes:
            self.properties['url'] = attributes['url'].value
        else:
            print("WARNING: url not defined, loading placeholder")
            self.properties['url'] = 'misc/placeholder'
        
        if 'id' in attributes:
            self.properties['id'] = attributes['id'].value
        else:
            self.properties['id'] = 'all'
        
        if 'inclination' in attributes:
            self.properties['inclination'] = float(attributes['inclination'].value)
        else:
            self.properties['inclination'] = 2.0
        
        if 'scale' in attributes:
            self.properties['scale'] = float(attributes['scale'].value)
        else:
            self.properties['scale'] = 1.0
        
        if 'hitboxscale' in attributes:
            self.properties['hitboxscale'] = float(attributes['hitboxscale'].value)
        else:
            self.properties['hitboxscale'] = 1.0
        
        if 'speed' in attributes:
            self.properties['speed'] = float(attributes['speed'].value)
        else:
            self.properties['speed'] = 1.0
        
        #self.isNPC remains true while isPlayable is changable
        if 'playable' in attributes:
            self.playable = playable = attributes['playable'].value
            if self.playable == 'false':                
                self.isNPC = False
                #print("setting ", self.properties['id'], " to ", self.isNPC)
            else:
                self.isNPC = True
                #print("setting ", self.properties['id'], " to ", self.isNPC)
        else:
            self.playable = playable = 'false'
            self.isNPC = True
        self.properties['playable'] = self.playable
        
        
        if 'direction' in attributes:
            self.properties['direction'] = attributes['direction'].value
        else:
            self.properties['direction'] = "down"
        
        if 'footsteps' in attributes:
            self.properties['footsteps'] = attributes['footsteps'].value
        else:
            self.properties['footsteps'] = "sfx/footsteps_default0.ogg"
        
        if 'onWalked' in attributes:
            self.properties['onWalked'] = self.onWalked = attributes['onWalked'].value
        else:
            self.properties['onWalked'] = self.onWalked = ""
        
        if 'onPicked' in attributes:
            self.properties['onPicked'] = self.onPicked = attributes['onPicked'].value
        
        self.generateNode(showCollisions)
        CharacterEmotions.__init__(self)
        
    def generateNode(self, showCollisions):
        self.destroy()
        
        #setting local variable
        attributes = self.attributes
        
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
        
        self.wtop = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/wtop.egg'))
        self.wdown = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/wdown.egg'))
        self.wleft = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/wleft.egg'))
        self.wright = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/wright.egg'))
        self.stop = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/stop.egg'))
        self.sdown = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/sdown.egg'))
        self.sleft = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/sleft.egg'))
        self.sright = self.applyNearestFilter(loader.loadModel(resourceManager.getResource(self.properties['url'])+'/sright.egg'))
        
        #Texture.FTNearest
        
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
        
        if self.playable=="true":
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
        self.node.setP(-(360-int(self.properties['inclination'])))
        self.node.setScale(float(self.properties['scale']))
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        
        self.lastpos = self.node.getPos()
        
        self.showAllSubnodes()
        
        #taskMgr.doMethodLater(4, self.face, 'charload'+self.properties['id'], [self.properties['direction']])
        self.face(self.properties['direction'])
        
        #set unique id
        self.node.setTag("id", self.properties['id'])

        #setting scripting part
        self.node.setTag("onWalked", self.onWalked)
        self.node.setTag("onPicked", self.onPicked)
        
        #storing a pointer of the gamenode
        self.node.setPythonTag("gamenode", self)
        
        self.npc_walk_stack = []
        self.npc_walk_happening = False
        self.globalLock = False
        
        self.setX(self.grid_currentx)
        self.setY(self.grid_currenty)
        
        if self.isNPC!=True:
            print("attempting creation of NPC in ", self.grid_currentx, "-", self.grid_currenty)
        
        if self.properties['footsteps'] != "":
            path = resourceManager.getResource(self.properties['footsteps'])
            self.footSound = base.loader.loadSfx(path)
            self.footSound.setVolume(0.75)
            self.footSound.setLoop(True)
        
        if 'playable' in attributes:
            if self.isNPC!=False:
                if ((self.grid_playable_pos.getX() != 0) and (self.grid_playable_pos.getY() != 0)):
                    #print('GRID: moving player to ' + str(self.grid_playable_pos))
                    self.setX(self.grid_playable_pos.getX())
                    self.setY(self.grid_playable_pos.getY())
        
        #automatic reparenting (and showing) when (re)generating node
        self.node.wrtReparentTo(self.parent.node)
    
    def getName(self):
        return 'Character: '+self.properties['id']
    
    def xmlAttributes(self):
        return self.properties
    
    def xmlTypeName(self):
        return self.typeName
    
    '''
    Sanitize properties data to be of correct type from string
    '''
    def sanitizeProperties(self):
        #sanitizing data
        self.properties['inclination'] = float(self.properties['inclination'])
        self.properties['hitboxscale'] = float(self.properties['hitboxscale'])
        self.properties['speed'] = float(self.properties['speed'])
        self.properties['scale'] = float(self.properties['scale'])
        
        self.updateTilePosition()
    
    #interface needed by PropertiesTable
    # regenerates the node at every change
    def onPropertiesUpdated(self):
        self.sanitizeProperties()
        self.generateNode(self.showCollisions)
        
    
    #interface needed by PropertiesTable
    #TODO: implement as real interface?
    def getPropertyList(self):
        return self.properties
    
    #interface needed by PropertiesTable
    def setProperty(self, key, value):
        self.properties[key] = value
    
    def increaseProperty(self, key, multiplier):
        if key in self.propertiesUpdateFactor:
            self.setProperty(key, self.properties[key]+self.propertiesUpdateFactor[key]*multiplier)
        
    def decreaseProperty(self, key, multiplier):
        if key in self.propertiesUpdateFactor:
            self.setProperty(key, self.properties[key]-self.propertiesUpdateFactor[key]*multiplier)
    
    def copyProperties(self):
        return self.getPropertyList()
    
    def pasteProperties(self, props):
        for key, value in props.items():
            if key in self.properties:
                self.properties[key] = value
        self.onPropertiesUpdated()
    
    def setSpeed(self, s):
        self.properties['speed'] = s
    
    def applyNearestFilter(self, model):
        for tex in model.findAllTextures():
            tex.setMinfilter(Texture.FT_nearest)
            tex.setMagfilter(Texture.FT_nearest)
        return model
    
    def startFootsteps(self):
        if self.footSound != None:
            self.footSound.play()
    
    def stopFootsteps(self):
        if self.footSound != None:
            self.footSound.stop()
    
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
        self.npc_movtask = taskMgr.add(self.npc_walk_task, "npc_moveCharacterTask"+self.properties['id'], uponDeath=self.npc_walk_callback)
        #footsteps call
        self.startFootsteps()
    
    def npc_walk_task(self, task):
        dt = globalClock.getDt()
        
        if(self.npc_direction=='left'):
            self.node.setX(self.node.getX()-1*dt*self.properties['speed'])
            currentx = self.node.getX()
            
            if currentx <= self.npc_targetx:
                return task.done
        if(self.npc_direction=='right'):
            self.node.setX(self.node.getX()+1*dt*self.properties['speed'])
            currentx = self.node.getX()
            
            if currentx >= self.npc_targetx:
                return task.done
        if(self.npc_direction=='up'):
            self.node.setZ(self.node.getZ()+1*dt*self.properties['speed'])
            currenty = self.node.getZ()
            
            if currenty >= self.npc_targety:
                return task.done
        if(self.npc_direction=='down'):
            self.node.setZ(self.node.getZ()-1*dt*self.properties['speed'])
            currenty = self.node.getZ()
            
            if currenty <= self.npc_targety:
                return task.done
        
        return task.cont
    
    def setCinematic(self, value):
        self.cinematic = value
    
    '''
    Resume past state of playable when
    resumeGameplay is catched 
    '''
    def resumeGameplay(self):
        self.setPlayable(True)
    
    
    '''
    Resume past state of playable when
    resumeGameplay is catched 
    '''
    def pauseGameplay(self):
        self.setPlayable(False)
    
    
    def npc_walk_callback(self, task):
        self.face(self.npc_direction)
        
        #unlocking concurrent movement protection
        self.npc_walk_happening = False
        
        #stopping footsteps
        self.stopFootsteps()
        
        if len(self.npc_walk_stack) > 0:
            self.npc_walk_helper()
        else: #character ended walking, unlock
            self.globalLock = False
            
    
    '''
    write destroy function
    '''
    def destroy(self):
        #not accepting events
        self.ignoreAll()
        #destroying everything down
        if self.node != None:
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
            b = self.node.getBounds().getRadius()
            
            self.cTrav = CollisionTraverser()
            
            self.collisionTube = CollisionSphere(b/2,0,b/2,0.035*self.properties['hitboxscale'])
            self.collisionNode = CollisionNode('characterTube')
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
            self.collisionHandler = CollisionHandlerQueue()
            self.cTrav.addCollider(self.collisionNodeNp, self.collisionHandler)
            
            if self.showCollisions == True or main.editormode:
                # Uncomment this line to see the collision rays
                self.collisionNodeNp.show()
                
                # Uncomment this line to show a visual representation of the 
                # collisions occuring
                self.cTrav.showCollisions(render)
        else:
            b = self.node.getBounds().getRadius()
            self.collisionTube = CollisionSphere(b/2,0,b/2,0.035*self.properties['hitboxscale'])
            
            #allowing playables to collide with npcs
            if self.isNPC == True: #TODO: fix because it's completely fucked up
                self.collisionNode = CollisionNode('characterTube')
            else:
                self.collisionNode = CollisionNode('characterNPCTube')
            
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
    
    #set if camera has to effectively follow the character
    #while it moves
    def setFollowedByCamera(self, value):
        #camera follow
        if value:
            if self.currentlyfollowed!=True:
                customCamera.follow(self)
                self.currentlyfollowed = True
        else:
            if self.currentlyfollowed!=False:
                customCamera.dontFollow()
                self.currentlyfollowed = False
    
    def setPickCollisions(self, value):
        if value:
            print("setting pick collisions")
            b = self.node.getBounds().getRadius()
            
            self.pickCTrav = CollisionTraverser()
            
            self.pickCollisionTube = CollisionSphere(b/2,0,b/2,0.035*self.properties['hitboxscale']+0.01)
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
        if self.cinematic == True:
            value = False
        if self.isNPC != False:
            if value == True:
                self.playable = True
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
                self.accept("pauseGameplay", self.pauseGameplay) #can pause play
            else:
                self.playable = False
                self.ignoreAll()
                self.node.setTag("playable", "false")
                self.setFollowedByCamera(False)
                self.resetMovement() #reset every movement happening
                self.accept("resumeGameplay", self.resumeGameplay) #can resume play if not NPC
    
    #estimate loading time 4 seconds... lol... UPDATE: seems fixed in newer panda versions, inspect
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
            self.startFootsteps() #playing footsteps
            if self.movtask == 0:
                self.movtask = taskMgr.add(self.moveCharacter, "moveCharacterTask")
        if value == False:
            self.stopFootsteps() #stopping footsteps
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
                self.node.setX(self.node.getX()-1*dt*self.properties['speed'])
            if self.currentlydown[-1] == 'right':
                self.node.setX(self.node.getX()+1*dt*self.properties['speed'])
            if self.currentlydown[-1] == 'top':
                self.node.setZ(self.node.getZ()+1*dt*self.properties['speed'])
            if self.currentlydown[-1] == 'down':
                self.node.setZ(self.node.getZ()-1*dt*self.properties['speed'])
        
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
            sp = entries[0].getSurfacePoint(self.node) #surface point
            objectNode = entries[0].getIntoNodePath().getParent() #into object node
            groundNode = entries[0].getIntoNodePath() #into object node
            
            if objectNode.hasTag("collideandwalk"):
                if objectNode.getTag("collideandwalk") != "yes":
                    self.node.setPos(self.lastpos)
            else:
                self.node.setPos(self.lastpos)
            
            #if node is a real object (not a wall)
            if objectNode.hasTag("avoidable"):
                if objectNode.getTag("avoidable") == "true": #see if object is intelligently avoidable
                    if objectNode.hasTag("xscaled") and objectNode.hasTag("yscaled"):
                        if len(self.currentlydown) > 0: #at least 1, avoids list index out of range exception
                            if self.currentlydown[-1] == 'left' or self.currentlydown[-1] == 'right': #TODO: fix the shiet, not always working
                                bottomObjPos = objectNode.getZ()-(float(objectNode.getTag("yscaled"))/2)
                                topObjPos = objectNode.getZ()+(float(objectNode.getTag("yscaled"))/2)
                                if self.node.getZ() < bottomObjPos:
                                    self.node.setZ(self.node.getZ()-1*dt*self.properties['speed'])
                                if self.node.getZ() > topObjPos:
                                    self.node.setZ(self.node.getZ()+1*dt*self.properties['speed'])
                                pass
                            if self.currentlydown[-1] == 'top' or self.currentlydown[-1] == 'down':
                                leftObjPos = objectNode.getX()-(float(objectNode.getTag("xscaled"))/2)
                                rightObjPos = objectNode.getX()+(float(objectNode.getTag("xscaled"))/2)
                                
                                if self.node.getX() < leftObjPos:
                                    self.node.setX(self.node.getX()-1*dt*self.properties['speed'])
                                    
                                if self.node.getX() > rightObjPos:
                                    self.node.setX(self.node.getX()+1*dt*self.properties['speed'])
                            self.lastpos = self.node.getPos()
            
        
        for entry in entries:
            objectNode = entry.getIntoNodePath().getParent()
            onWalked = objectNode.getTag("onWalked")
            if len(onWalked)>0:
                eval(onWalked) #oh lol, danger detected here
        
        evaluatedOnce = False
        if self.pickRequest == True:
            for entry in pickentries:
                objectNode = entry.getIntoNodePath().getParent()
                onPicked = objectNode.getTag("onPicked")
                if len(onPicked)>0 and evaluatedOnce == False:
                    eval(onPicked) #oh lol, danger detected again here
                    evaluatedOnce = True
                else:
                    if hasattr(objectNode.getPythonTag('gamenode'), 'name'):
                        print("WARNING: picking on this object is not defined: ", objectNode.getPythonTag('gamenode').name)
                        print("X: ",objectNode.getX())
                        print("Y: ",objectNode.getZ())
            self.pickRequest = False #resetting request
        
        #this is needed for empty pick
        if self.pickRequest == True:
            self.pickRequest = False #resetting request
        
        return Task.cont
    
    def getX(self):
        return self.node.getX()
        
    def getY(self):
        return self.node.getY()
    
    def getZ(self):
        return self.node.getZ()
    
    def getNode(self):
        return self.node
    
    def getWorldPos(self):
        return self.node.getPos(render)
    
    def setX(self, x):
        self.node.setX(x)
        self.lastpos.setX(x)
    
    def setY(self, y):
        self.node.setZ(y)
        self.lastpos.setZ(y)
    
    #here for polymorph
    def getTileX(self):
        return self.parent.getX()
    
    #here for polymorph
    def getTileY(self):
        return self.parent.getY()
