from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import NodePath, TextureStage

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
    def addObject(self, name, inclination):
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        
        xscaled = tex.getOrigFileXSize() / self.baseDimension
        yscaled = tex.getOrigFileYSize() / self.baseDimension
        
        cm = CardMaker("tileobject")
        cm.setFrame(0,xscaled,0,yscaled)
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        self.node.showTightBounds()
        tb = self.node.getTightBounds()
        print tb
        
        self.collisionTube = CollisionSphere(xscaled/2,0,xscaled/2,xscaled/2)
        self.collisionNode = CollisionNode('objectSphere')
        self.collisionNode.addSolid(self.collisionTube)
        self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
        self.collisionNodeNp.setX(-xscaled/4)
        
        geomnode = NodePath(cm.generate())
        geomnode.setX((-xscaled/2)+0.5)
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