from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import NodePath, TextureStage, Texture
from panda3d.core import Point3, CollisionPolygon, CollisionBox, LPoint3f

from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import CardMaker

from objects.light import Light
from gameobject import GameObject
from character import Character
from XMLExportable import XMLExportable
from editor.gui.PropertiesTableAbstract import PropertiesTableAbstract

'''
TILE CLASS 

Tile class is used to represent a tile in the 2d simulated
world. This will take care of anything from flags to textures to 
geometries attached to it. Please reference to this instead of the
direct geometry in other parts of code.
'''
class Tile(XMLExportable, PropertiesTableAbstract):
    
    def __init__(self, baseDimension):
        #public props
        self.walkable = True
        self.resources = []
        self.textures = [] #list that holds every texture in the tile, ordered from bottom to top
        self.objects = [] #list that holds every object in the tile, ordered from bottom to top
        self.lights = [] #list that holds every light in the tile, ordered from bottom to top
        self.typeName = 'tile' #needed by xml
        
        self.tileProperties = {
            'id' : '', #still no used, polymorph
            'url' : '',
            'onWalked' : '',
            'onPicked' : '',
            'walkable' : ''
        }
        
        self.innerX = 0
        self.innerY = 0
        self.innerDimension = 0
        
        self.baseDimension = baseDimension
        
        self.node = NodePath('tilenode')
        self.node.setTwoSided(True)
        self.onPicked = ''
        
        #storing gamenode address, mainly used for node searching
        self.node.setPythonTag("gamenode", self)
        
        #generating groundnode
        cm = CardMaker("tiletexture")
        cm.setFrame(0,1,0,1)
        
        self.groundnode = NodePath('groundtilenode')
        self.groundnode.attachNewNode(cm.generate())
        self.groundnode.reparentTo(self.node)
    
    def xmlAttributes(self):
        return self.tileProperties
    
    def xmlTypeName(self):
        return self.typeName
    
    def onPropertiesUpdated(self):
        print "Tile.onPropertiesUpdated() called! Use this to modify live prop update behaviour!"
    
    def getPropertyList(self):
        return self.tileProperties
    
    def setProperty(self, key, value):
        self.tileProperties[key] = value
    
    def getNode(self):
        return self.node
    
    '''
    return quad ground node
    '''
    def getGroundNode(self):
        return self.groundnode
    
    '''
    add a static texture to basic 128x128 tile pixel image
    use just to paint the world basicly. Use addObject for every object that has to do with collision etc
    '''
    def addTexture(self, attributes):
        self.clearAllTextures()
        if attributes.has_key('url'):
            self.tileProperties['url'] = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            self.tileProperties['url'] = 'misc/placeholder'
        
        if attributes.has_key('onWalked'):
            self.tileProperties['onWalked'] = attributes['onWalked'].value
        else:
            self.tileProperties['onWalked'] = ""
        
        if attributes.has_key('onPicked'):
            if self.tileProperties['onPicked'] == '':
                self.tileProperties['onPicked'] = attributes['onPicked'].value
        
        if attributes.has_key('walkable'):
            if attributes['walkable'].value == "true":
                self.walkable = True
                self.tileProperties['walkable'] = 'true'
            else:
                self.walkable = False
                self.tileProperties['walkable'] = 'false'
                self.groundnode.setTag("collideandwalk", "no")
            if attributes['walkable'].value == "collide":
                self.walkable = False
                self.tileProperties['walkable'] = 'collide'
                self.groundnode.setTag("collideandwalk", "yes")
        else:
            self.tileProperties['walkable'] = 'true'
            self.walkable = True
        
        #setting scripting part
        self.groundnode.setTag("onWalked", self.tileProperties['onWalked'])
        self.groundnode.setTag("onPicked", self.tileProperties['onPicked'])
        
        #setting walkable or not
        self.setWalkable(self.walkable)
        
        #actually loading texture
        tex = loader.loadTexture(resourceManager.getResource(self.tileProperties['url'])+'.png')
        tex.setWrapV(Texture.WM_clamp)
        tex.setWrapU(Texture.WM_clamp)
        
        #this is true pixel art
        #change to FTLinear for linear interpolation between pixel colors
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
        
        self.groundnode.setTexture(tex)
        
        self.textures.append(self.tileProperties['url'])
    
    def getObjectAt(self, i):
        return self.objects[i]
        
    def deleteObjectAt(self, pos):
        self.objects[pos].destroy()
        self.objects.remove(self.objects[pos])
    
    '''
    return the list of objects under the node
    '''
    def getGameObjects(self):
        return self.objects
    
    '''
    return the list of ground textures applied
    '''
    def getTextures(self):
        return self.textures
    
    '''
    clear all ground textures on the node
    '''
    def clearAllTextures(self):
        self.groundnode.clearTexture()
        self.textures = []

    '''
    Set a list of textures.
    Destroy all textures and rebuilds all base on a new list
    @param  tex  list of urls that points to textures
    '''
    def setTextures(self, tex):
        self.textures = tex
        for t in self.textures:
            self.addTexture(t)
    
    '''
    if true automatically create a collider that intersects with walking objects
    same size as the tile (def 128x128 ground pixels)
    @param  value   true or false
    '''
    def setWalkable(self, value):
        if value == False:
            self.collisionTube = CollisionBox(LPoint3f(0,0,0),LPoint3f(1,1,1))
            
            self.collisionNode = CollisionNode('unwalkable')
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNodeNp = self.groundnode.attachNewNode(self.collisionNode)
        
    '''
    remove an object from the tile
    @param target to be removed
    '''
    def removeObject(self, target):
        if target in self.objects:
            self.objects.remove(target)
    
    '''
    Add already existent object into objects children list
    @param target to be appended
    '''
    def addExistentObject(self, target):
        self.objects.append(target)
        target.reparentTo(self)
    
    '''
    used to add objects to game that intersects (or not) walkability
    @param attribues list of xml loaded attributes
    '''
    def addObject(self, attributes):
        gameObject = GameObject(attributes, self, self.innerX, self.innerY, self.innerDimension, self.baseDimension)
        self.objects.append(gameObject)
    
    def addLight(self, attributes):
        lightObject = Light(attributes, self)
        self.objects.append(lightObject)
    
    def addCharacter(self, attributes, showCollisions, currentx, currenty, playablepos):
        characterObject = Character(attributes, showCollisions, currentx, currenty, playablepos, self)
        self.objects.append(characterObject)
    
    '''
    Mostly broken with oop structure. Needed by grass and maybe some other.
    '''
    def addCustomObject(self, o):
        o.getNode().reparentTo(self.node)
    
    def setX(self, x):
        if self.node != 0:
            self.node.setX(x)
            self.innerX = x
            
    def setY(self, y):
        if self.node != 0:
            self.node.setZ(y)
            self.innerY = y
    
    #here for polymorph
    def getTileX(self):
        return self.getX()
    
    #here for polymorph
    def getTileY(self):
        return self.getY()
    
    #real getX
    def getX(self):
        return self.innerX
    
    #real getY
    def getY(self):
        return self.innerY
    
    def destroy(self):
        for o in self.objects[:]:
            o.destroy()
            self.objects.remove(o)
        self.node.removeNode()
