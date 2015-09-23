from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import NodePath, TextureStage, Texture
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
        self.onPicked = ''
        
        #storing gamenode address, mainly used for node searching
        self.node.setPythonTag("gamenode", self)
        
        #generating groundnode
        cm = CardMaker("tiletexture")
        cm.setFrame(0,1,0,1)
        
        self.groundnode = NodePath('groundtilenode')
        self.groundnode.attachNewNode(cm.generate())
        self.groundnode.reparentTo(self.node)
    
    #add a static texture to basic 128x128 tile pixel image
    #use just to paint the world basicly. Use addObject for every object that has to do with collision etc
    def addTexture(self, attributes):
        if attributes.has_key('url'):
            self.name = name = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            self.name = name = 'misc/placeholder'
        
        if attributes.has_key('onWalked'):
            self.onWalked = attributes['onWalked'].value
        else:
            self.onWalked = ""
        
        if attributes.has_key('onPicked'):
            if self.onPicked == '':
                self.onPicked = attributes['onPicked'].value
        
        if attributes.has_key('walkable'):
            if attributes['walkable'].value == "true":
                self.walkable = True
            else:
                self.walkable = False
                self.groundnode.setTag("collideandwalk", "no")
            if attributes['walkable'].value == "collide":
                self.walkable = False
                self.groundnode.setTag("collideandwalk", "yes")
        else:
            self.walkable = True
        
        #setting scripting part
        self.groundnode.setTag("onWalked", self.onWalked)
        self.groundnode.setTag("onPicked", self.onPicked)
        
        #setting walkable or not
        self.setWalkable(self.walkable)
        
        #actually loading texture
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        tex.setWrapV(Texture.WM_clamp)
        tex.setWrapU(Texture.WM_clamp)
        
        self.groundnode.setTexture(tex)
    
    def setWalkable(self, value):
        if value == False:
            self.collisionTube = CollisionBox(LPoint3f(0,0,0),LPoint3f(1,1,1))
            
            self.collisionNode = CollisionNode('unwalkable')
            self.collisionNode.addSolid(self.collisionTube)
            self.collisionNodeNp = self.groundnode.attachNewNode(self.collisionNode)
        
    
    #used to add objects to game that intersects (or not) walkability
    def addObject(self, attributes):
        #manage attributes directly in object creation,
        #this was many attributes are not mandatory
        if attributes.has_key('url'):
            self.name = name = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            self.name = name = 'misc/placeholder'
        
        if attributes.has_key('id'):
            self.uid = attributes['id'].value
        else:
            self.uid = 'all'
        
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
        
        if attributes.has_key('offsethorizontal'):
            offsethorizontal = float(attributes['offsethorizontal'].value)
        else:
            offsethorizontal = 0.0
        
        if attributes.has_key('offsetcollisionh'):
            offsetcollisionh = float(attributes['offsetcollisionh'].value)
        else:
            offsetcollisionh = 0.0
        
        if attributes.has_key('offsetcollisionv'):
            offsetcollisionv = float(attributes['offsetcollisionv'].value)
        else:
            offsetcollisionv = 0.0
        
        if attributes.has_key('offsetvertical'):
            offsetvertical = float(attributes['offsetvertical'].value)
        else:
            offsetvertical = 0.0
        
        if attributes.has_key('elevation'):
            elevation = float(attributes['elevation'].value)
        else:
            elevation = 0.0
        
        if attributes.has_key('scale'):
            scale = float(attributes['scale'].value)
        else:
            scale = 1.0
        
        if attributes.has_key('onWalked'):
            self.onWalked = attributes['onWalked'].value
        else:
            self.onWalked = ""
        
        if attributes.has_key('onPicked'):
            if self.onPicked == '':
                self.onPicked = attributes['onPicked'].value
        
        if attributes.has_key('collisionmode'):
            collisionmode = attributes['collisionmode'].value
        else:
            collisionmode = "2d"
        
        if attributes.has_key('walkable'):
            if attributes['walkable'].value == "true":
                walkable = True
            else:
                walkable = False
        else:
            walkable = False
        
        if attributes.has_key('avoidable'):
            self.node.setTag("avoidable", attributes['avoidable'].value) #applying property also to node as tag
            if attributes['avoidable'].value == "true":
                self.avoidable = True
            else:
                self.avoidable = False
        else:
            self.node.setTag("avoidable", "false")
            self.avoidable = False
        
        #setting scripting part
        self.node.setTag("onWalked", self.onWalked)
        self.node.setTag("onPicked", self.onPicked)
        #set unique id
        self.node.setTag("id", self.uid)
        
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        tex.setWrapV(Texture.WM_clamp)
        tex.setWrapU(Texture.WM_clamp)
        
        
        xorig = tex.getOrigFileXSize() / self.baseDimension
        yorig = tex.getOrigFileYSize() / self.baseDimension
        xscaled = (tex.getOrigFileXSize() / self.baseDimension) * scale
        yscaled = (tex.getOrigFileYSize() / self.baseDimension) * scale
        
        self.node.setTag("xscaled", str(xscaled))
        self.node.setTag("yscaled", str(yscaled))
        
        cm = CardMaker("tileobject")
        cm.setFrame(0,xorig,0,yorig)
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        # distinguish between 3d collisions (for objects with an height and sensible inclination)
        # and 2d collisions for plain sprites
        if walkable == False:
            if collisionmode == "3d":
                #must handle differently objects which are small and big
                if xscaled < 1:
                    self.collisionTube = CollisionBox(LPoint3f(0.5 - xscaled/2 - offsetwidth,0,0),LPoint3f(0.5 + xscaled/2 + offsetwidth,0.1,0.3 + offsetheight))
                    
                if xscaled >= 1:
                    self.collisionTube = CollisionBox(LPoint3f(0 - offsetwidth,0,0),LPoint3f(xscaled + offsetwidth,0.1,0.3 + offsetheight))
                
                self.collisionNode = CollisionNode('objectSphere')
                self.collisionNode.addSolid(self.collisionTube)
                self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
                self.collisionNodeNp.setX(offsethorizontal)
                self.collisionNodeNp.setZ(offsetvertical)
                self.collisionNodeNp.setX(self.collisionNodeNp.getX()+offsetcollisionh)
                self.collisionNodeNp.setZ(self.collisionNodeNp.getZ()+offsetcollisionv)
                
            elif collisionmode == "2d":
                #must handle differently objects which are small and big
                if xscaled < 1:
                    self.collisionTube = CollisionBox(LPoint3f(0.5 - xscaled/2,0,0),LPoint3f(0.5 + xscaled/2,yscaled,0.3))
                    
                if xscaled >= 1:
                    self.collisionTube = CollisionBox(LPoint3f(0,0,0),LPoint3f(xscaled,yscaled,0.3))
                
                self.collisionNode = CollisionNode('objectSphere')
                self.collisionNode.addSolid(self.collisionTube)
                self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
                self.collisionNodeNp.setP(-(270-int(inclination)))
                self.collisionNodeNp.setX(offsethorizontal)
                self.collisionNodeNp.setZ(offsetvertical)
                self.collisionNodeNp.setX(self.collisionNodeNp.getX()+offsetcollisionh)
                self.collisionNodeNp.setZ(self.collisionNodeNp.getZ()+offsetcollisionv)
        
        geomnode = NodePath(cm.generate())
        if xscaled >= 1:
            geomnode.setX(0)
        if xscaled < 1:
            geomnode.setX(0.5 - xscaled/2)
        geomnode.setScale(scale)
        geomnode.setX(geomnode.getX()+offsethorizontal)
        geomnode.setZ(geomnode.getZ()+offsetvertical)
        geomnode.setY(-elevation)
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
