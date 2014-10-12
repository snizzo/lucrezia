from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import NodePath, TextureStage
from panda3d.core import Point3, CollisionPolygon, CollisionBox, LPoint3f

from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import CardMaker

'''
TILE CLASS 

Tile class is used to represent a tile in the 2d simulated
world. This will take care of anything from flags to textures to 
geometries attached to it. Please reference to this instead of the
direct geometry in other parts of code.
'''
class Tile:
    
    def __init__(self, baseDimension):
        #public props
        self.walkable = True
        self.resources = []
        
        self.innerX = 0
        self.innerY = 0
        self.innerDimension = 0
        
        self.baseDimension = baseDimension
        
        self.node = NodePath('tilenode')
        self.node.setTwoSided(True)
        
        #generating groundnode
        cm = CardMaker("tiletexture")
        cm.setFrame(0,1,0,1)
        
        self.groundnode = NodePath('groundtilenode')
        self.groundnode.attachNewNode(cm.generate())
        self.groundnode.reparentTo(self.node)
    
    #add a static texture to basic 128x128 tile pixel image
    #use just to paint the world basicly. Use addObject for every object that has to do with collision etc
    def addTexture(self, name):
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        self.groundnode.setTexture(ts, tex)
    
    #used to add objects to game that intersects (or not) walkability
    def addObject(self, attributes):
        #manage attributes directly in object creation,
        #this was many attributes are not mandatory
        if attributes.has_key('url'):
            name = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            name = 'misc/placeholder'
        
        if attributes.has_key('inclination'):
            inclination = float(attributes['inclination'].value)
        else:
            inclination = 30.0
        
        if attributes.has_key('offsetwidth'):
            offsetwidth = float(attributes['offsetwidth'].value)
        else:
            offsetwidth = 0.0
        
        if attributes.has_key('offsetheight'):
            offsetheight = float(attributes['offsetheight'].value)
        else:
            offsetheight = 0.0
        
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        
        xscaled = tex.getOrigFileXSize() / self.baseDimension
        yscaled = tex.getOrigFileYSize() / self.baseDimension
        
        print xscaled
        print yscaled
        
        cm = CardMaker("tileobject")
        cm.setFrame(0,xscaled,0,yscaled)
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        #must handle differently objects which are small and big
        #check directly on xscaled
        if xscaled < 1:
            self.collisionTube = CollisionBox(LPoint3f(0.5 - xscaled/2 - offsetwidth,0,0),LPoint3f(0.5 + xscaled/2 + offsetwidth,0.1,0.3 + offsetheight))
            
        if xscaled >= 1:
            self.collisionTube = CollisionBox(LPoint3f(0 - offsetwidth,0,0),LPoint3f(xscaled + offsetwidth,0.1,0.3 + offsetheight))
        
        self.collisionNode = CollisionNode('objectSphere')
        self.collisionNode.addSolid(self.collisionTube)
        self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
        self.collisionNodeNp.setX(0)
        
        geomnode = NodePath(cm.generate())
        if xscaled >= 1:
            geomnode.setX(0)
        if xscaled < 1:
            geomnode.setX(0.5 - xscaled/2)
        geomnode.setP(-(360-int(inclination)))
        geomnode.setTexture(tex)
        geomnode.setTransparency(TransparencyAttrib.MAlpha)
        geomnode.reparentTo(self.node)
        
        '''
        tex = loader.loadTexture('../res/'+name+'.png')
        
        xscaled = tex.getOrigFileXSize() / 128
        yscaled = tex.getOrigFileYSize() / 128
        
        cm = CardMaker("tileobject")
        cm.setFrame(-xscaled,xscaled,-yscaled,yscaled)
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        objectnode = self.node.attachNewNode('objectnode')
        objectgeomnode = objectnode.attachNewNode(cm.generate())
        objectnode.setP(300)
        objectnode.setTexture(ts, tex)
        objectnode.place()
        '''
    
    def getResDimension(self):
        pass
    
    def setWalkable(self, value):
        self.walkable = value
    
    def getWalkable(self):
        return self.walkable
    
    def setX(self, x):
        if self.node != 0:
            self.node.setX(x)
            self.innerX = x
            
    def setY(self, y):
        if self.node != 0:
            self.node.setZ(y)
            self.innerY = y

    def generate(self):
        pass