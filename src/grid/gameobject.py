from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import NodePath, TextureStage, Texture
from panda3d.core import Point3, CollisionPolygon, CollisionBox, LPoint3f

from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import CardMaker

'''
used to add objects to game that intersects (or not) walkability
@param attribues list of xml loaded attributes
'''

class GameObject:
    def __init__(self, attributes, parent, innerX, innerY, innerDimension, baseDimension):
        self.onPicked = ''
        
        self.innerX = innerX
        self.innerY = innerY
        self.innerDimension = innerDimension
        self.baseDimension = baseDimension
        
        self.properties = {
            'url' : '',
            'onWalked' : '',
            'onPicked' : '',
            'walkable' : ''
        }
        
        self.node = NodePath('gameobjectnode')
        self.node.setTwoSided(True)
        self.node.reparentTo(parent.node)
        #manage attributes directly in object creation,
        #this was many attributes are not mandatory
        if attributes.has_key('url'):
            self.properties['name'] = name = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            self.properties['name'] = name = 'misc/placeholder'
        
        if attributes.has_key('id'):
            self.properties['uid'] = self.uid = attributes['id'].value
        else:
            self.properties['uid'] = self.uid = 'all'
        
        if attributes.has_key('inclination'):
            self.properties['inclination'] = float(attributes['inclination'].value)
        else:
            self.properties['inclination'] = 30.0
        
        if attributes.has_key('offsetwidth'):
            self.properties['offsetwidth'] = float(attributes['offsetwidth'].value)
        else:
            self.properties['offsetwidth'] = 0.0
        
        if attributes.has_key('offsetheight'):
            self.properties['offsetheight'] = float(attributes['offsetheight'].value)
        else:
            self.properties['offsetheight'] = 0.0
        
        if attributes.has_key('offsethorizontal'):
            self.properties['offsethorizontal'] = float(attributes['offsethorizontal'].value)
        else:
            self.properties['offsethorizontal'] = 0.0
        
        if attributes.has_key('offsetcollisionh'):
            self.properties['offsetcollisionh'] = float(attributes['offsetcollisionh'].value)
        else:
            self.properties['offsetcollisionh'] = 0.0
        
        if attributes.has_key('offsetcollisionv'):
            self.properties['offsetcollisionv'] = float(attributes['offsetcollisionv'].value)
        else:
            self.properties['offsetcollisionv'] = 0.0
        
        if attributes.has_key('offsetvertical'):
            self.properties['offsetvertical'] = float(attributes['offsetvertical'].value)
        else:
            self.properties['offsetvertical'] = 0.0
        
        if attributes.has_key('elevation'):
            self.properties['elevation'] = float(attributes['elevation'].value)
        else:
            self.properties['elevation'] = 0.0
        
        if attributes.has_key('scale'):
            self.properties['scale'] = float(attributes['scale'].value)
        else:
            self.properties['scale'] = 1.0
        
        if attributes.has_key('onWalked'):
            self.properties['onWalked'] = self.onWalked = attributes['onWalked'].value
        else:
            self.properties['onWalked'] = self.onWalked = ""
        
        if attributes.has_key('onPicked'):
            if self.onPicked == '':
                self.properties['onPicked'] = self.onPicked = attributes['onPicked'].value
        
        if attributes.has_key('collisionmode'):
            self.properties['collisionmode'] = attributes['collisionmode'].value
        else:
            self.properties['collisionmode'] = "2d"
        
        if attributes.has_key('walkable'):
            if attributes['walkable'].value == "true":
                self.properties['walkable'] = walkable = True
            else:
                self.properties['walkable'] = walkable = False
        else:
            self.properties['walkable'] = walkable = False
        
        if attributes.has_key('avoidable'):
            self.node.setTag("avoidable", attributes['avoidable'].value) #applying property also to node as tag
            if attributes['avoidable'].value == "true":
                self.properties['avoidable'] = self.avoidable = True
            else:
                self.properties['avoidable'] = self.avoidable = False
        else:
            self.node.setTag("avoidable", "false")
            self.properties['avoidable'] = self.avoidable = False
        
        #setting scripting part
        self.node.setTag("onWalked", self.onWalked)
        self.node.setTag("onPicked", self.onPicked)
        #set unique id
        self.node.setTag("id", self.uid)
        
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        tex.setWrapV(Texture.WM_clamp)
        tex.setWrapU(Texture.WM_clamp)
        
        #this is true pixel art
        #change to FTLinear for linear interpolatino between pixel colors
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
        
        xorig = tex.getOrigFileXSize() / self.baseDimension
        yorig = tex.getOrigFileYSize() / self.baseDimension
        xscaled = (tex.getOrigFileXSize() / self.baseDimension) * self.properties['scale']
        yscaled = (tex.getOrigFileYSize() / self.baseDimension) * self.properties['scale']
        
        self.node.setTag("xscaled", str(xscaled))
        self.node.setTag("yscaled", str(yscaled))
        
        cm = CardMaker("tileobject")
        cm.setFrame(0,xorig,0,yorig)
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        # distinguish between 3d collisions (for objects with an height and sensible self.properties['inclination'])
        # and 2d collisions for plain sprites
        if walkable == False:
            if self.properties['collisionmode'] == "3d":
                #must handle differently objects which are small and big
                if xscaled < 1:
                    self.collisionTube = CollisionBox(LPoint3f(0.5 - xscaled/2 - self.properties['offsetwidth'],0,0),LPoint3f(0.5 + xscaled/2 + self.properties['offsetwidth'],0.1,0.3 + self.properties['offsetheight']))
                    
                if xscaled >= 1:
                    self.collisionTube = CollisionBox(LPoint3f(0 - self.properties['offsetwidth'],0,0),LPoint3f(xscaled + self.properties['offsetwidth'],0.1,0.3 + self.properties['offsetheight']))
                
                self.collisionNode = CollisionNode('objectSphere')
                self.collisionNode.addSolid(self.collisionTube)
                self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
                self.collisionNodeNp.setX(self.properties['offsethorizontal'])
                self.collisionNodeNp.setZ(self.properties['offsetvertical'])
                self.collisionNodeNp.setX(self.collisionNodeNp.getX()+self.properties['offsetcollisionh'])
                self.collisionNodeNp.setZ(self.collisionNodeNp.getZ()+self.properties['offsetcollisionv'])
                
            elif self.properties['collisionmode'] == "2d":
                #must handle differently objects which are small and big
                if xscaled < 1:
                    self.collisionTube = CollisionBox(LPoint3f(0.5 - xscaled/2,0,0),LPoint3f(0.5 + xscaled/2,yscaled,0.3))
                    
                if xscaled >= 1:
                    self.collisionTube = CollisionBox(LPoint3f(0,0,0),LPoint3f(xscaled,yscaled,0.3))
                
                self.collisionNode = CollisionNode('objectSphere')
                self.collisionNode.addSolid(self.collisionTube)
                self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
                self.collisionNodeNp.setP(-(270-int(self.properties['inclination'])))
                self.collisionNodeNp.setX(self.properties['offsethorizontal'])
                self.collisionNodeNp.setZ(self.properties['offsetvertical'])
                self.collisionNodeNp.setX(self.collisionNodeNp.getX()+self.properties['offsetcollisionh'])
                self.collisionNodeNp.setZ(self.collisionNodeNp.getZ()+self.properties['offsetcollisionv'])
        
        geomnode = NodePath(cm.generate())
        if xscaled >= 1:
            geomnode.setX(0)
        if xscaled < 1:
            geomnode.setX(0.5 - xscaled/2)
        geomnode.setScale(self.properties['scale'])
        geomnode.setX(geomnode.getX()+self.properties['offsethorizontal'])
        geomnode.setZ(geomnode.getZ()+self.properties['offsetvertical'])
        geomnode.setY(-self.properties['elevation'])
        geomnode.setP(-(360-int(self.properties['inclination'])))
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
    
    def getName(self):
        return self.properties['name']
    
    #interface needed by PropertiesTable
    #TODO: implement as real interface?
    def getPropertyList(self):
        return self.properties
    
    #interface needed by PropertiesTable
    def setProperty(self, key, value):
        self.properties[key] = value
