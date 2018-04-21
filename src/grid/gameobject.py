from panda3d.core import CollisionTraverser,CollisionNode,CollisionTube,BitMask32,CollisionSphere
from panda3d.core import NodePath, TextureStage, Texture
from panda3d.core import Point3, CollisionPolygon, CollisionBox, LPoint3f
from panda3d.core import GeomVertexWriter, GeomVertexReader

from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import CardMaker

from XMLExportable import XMLExportable
from GameEntity import GameEntity
from editor.gui.PropertiesTableAbstract import PropertiesTableAbstract
from geometries.CustomQuad import CustomQuad

import math

'''
@inherit XMLExportable
'''
class GameObject(GameEntity, XMLExportable, PropertiesTableAbstract):
    '''
    used to add objects to game that intersects (or not) walkability
    @param attribues list of xml loaded attributes
    '''
    def __init__(self, attributes, parent, innerX, innerY, innerDimension, baseDimension):
        GameEntity.__init__(self, parent) #running parent constructor
        
        self.onPicked = ''
        
        self.innerX = innerX
        self.innerY = innerY
        self.innerDimension = innerDimension
        self.baseDimension = baseDimension
        self.typeName = 'object'
        
        self.properties = {
            'url' : '',
            'id' : '',
            'scale' : '',
            'name' : '',
            'inclination' : '',
            'elevation' : '',
            'rotation' : '',
            'offsetheight' : '',
            'offsetwidth' : '',
            'offsethorizontal' : '',
            'offsetvertical' : '',
            'offsetcollisionh' : '',
            'offsetcollisionv' : '',
            'collisionmode' : '',
            'walkable' : '',
            'avoidable' : '',
            'onPicked' : '',
            'onWalked' : ''
        }
        
        self.propertiesUpdateFactor = {
            'scale' : 0.1,
            'inclination' : 0.2,
            'elevation' : 0.02,
            'rotation' : 1.0,
            'offsetheight' : 0.02,
            'offsetwidth' : 0.02,
            'offsethorizontal' : 0.02,
            'offsetvertical' : 0.02,
            'offsetcollisionh' : 0.02,
            'offsetcollisionv' : 0.02
        }
        
        self.node = None
        self.collisionNodeNp = None
        #manage attributes directly in object creation,
        #this was many attributes are not mandatory
        if attributes.has_key('url'):
            self.properties['url'] = name = attributes['url'].value
        else:
            print "WARNING: url not defined, loading placeholder"
            self.properties['url'] = name = 'misc/placeholder'
        
        if attributes.has_key('id'):
            self.properties['id'] = self.uid = attributes['id'].value
        else:
            self.properties['id'] = self.uid = 'all'
        
        if attributes.has_key('inclination'):
            self.properties['inclination'] = float(attributes['inclination'].value)
        else:
            self.properties['inclination'] = 30.0
        
        if attributes.has_key('rotation'):
            self.properties['rotation'] = float(attributes['rotation'].value)
        else:
            self.properties['rotation'] = 0.0
        
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
                self.properties['walkable'] = walkable = 'true'
            else:
                self.properties['walkable'] = walkable = 'false'
        else:
            self.properties['walkable'] = walkable = 'false'
        
        if attributes.has_key('avoidable'):
            if attributes['avoidable'].value == "true":
                self.properties['avoidable'] = self.avoidable = True
            else:
                self.properties['avoidable'] = self.avoidable = False
        else:
            self.properties['avoidable'] = self.avoidable = False
        
        self.generateNode()
    
    def generateNode(self):        
        self.destroy()
        
        self.node = NodePath('gameobjectnode')
        self.node.setTwoSided(True)
        self.node.reparentTo(self.parent.node)
        
        if self.properties['avoidable'] == True:
            self.node.setTag("avoidable", 'true')
        else:
            self.node.setTag("avoidable", 'false')
        
        #setting scripting part
        self.node.setTag("onWalked", self.onWalked)
        self.node.setTag("onPicked", self.onPicked)
        #set unique id
        self.node.setTag("id", self.properties['id'])
        
        tex = loader.loadTexture(resourceManager.getResource(self.properties['url'])+'.png')
        tex.setWrapV(Texture.WM_clamp)
        tex.setWrapU(Texture.WM_clamp)
        
        #this is true pixel art
        #change to FTLinear for linear interpolation between pixel colors
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
        if self.properties['walkable'] == 'false':
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
                self.collisionNodeNp.setZ(self.collisionNodeNp.getZ()+self.properties['offsetcollisionv']+0.1)
                if main.editormode:
                    self.collisionNodeNp.show()
                
            elif self.properties['collisionmode'] == "2d":
                #must handle differently objects which are small and big
                if xscaled < 1:
                    self.collisionTube = CollisionBox(LPoint3f(0.5 - xscaled/2 - self.properties['offsetwidth'],0,0),LPoint3f(0.5 + xscaled/2 + self.properties['offsetwidth'],yscaled + self.properties['offsetheight'],0.3))
                    
                if xscaled >= 1:
                    self.collisionTube = CollisionBox(LPoint3f(0 - self.properties['offsetwidth'],0,0),LPoint3f(xscaled + self.properties['offsetwidth'],yscaled + self.properties['offsetheight'],0.3))
                
                self.collisionNode = CollisionNode('objectSphere')
                self.collisionNode.addSolid(self.collisionTube)
                self.collisionNodeNp = self.node.attachNewNode(self.collisionNode)
                self.collisionNodeNp.setP(-(270-int(self.properties['inclination'])))
                self.collisionNodeNp.setX(self.properties['offsethorizontal'])
                self.collisionNodeNp.setZ(self.properties['offsetvertical'])
                self.collisionNodeNp.setX(self.collisionNodeNp.getX()+self.properties['offsetcollisionh'])
                self.collisionNodeNp.setZ(self.collisionNodeNp.getZ()+self.properties['offsetcollisionv']+0.1)
                if main.editormode:
                    self.collisionNodeNp.show()
        
        geomnode = NodePath(cm.generate())
        if geomnode.node().isGeomNode():
            vdata = geomnode.node().modifyGeom(0).modifyVertexData()
            writer = GeomVertexWriter(vdata, 'vertex')
            reader = GeomVertexReader(vdata, 'vertex')
            
            '''
            this part apply rotation flattening to the perspective view
            by modifying directly structure vertices
            '''
            i = 0 #counter
            while not reader.isAtEnd():
                v = reader.getData3f()
                x = v[0]
                y = v[1]
                z = v[2]
                newx = x
                newy = y
                newz = z
                if self.properties['rotation'] == -90.0:
                    if i == 0:
                        newx = math.fabs(math.cos(math.radians(self.properties['inclination']))) * z
                        newz = 0
                        ssen = math.fabs(math.sin(math.radians(self.properties['inclination']))) * z
                        sparsen = math.fabs(math.sin(math.radians(self.properties['inclination']))) * ssen
                        spercos = math.fabs(math.cos(math.radians(self.properties['inclination']))) * ssen
                        newy -= spercos
                        newz += sparsen
                    if i == 2:
                        newx += math.fabs(math.cos(math.radians(self.properties['inclination']))) * z
                        newz = 0
                        ssen = math.fabs(math.sin(math.radians(self.properties['inclination']))) * z
                        sparsen = math.fabs(math.sin(math.radians(self.properties['inclination']))) * ssen
                        spercos = math.fabs(math.cos(math.radians(self.properties['inclination']))) * ssen
                        newy -= spercos
                        newz += sparsen
                    writer.setData3f(newx, newy, newz)
                i += 1 #increase vertex counter
        if xscaled >= 1:
            geomnode.setX(0)
        if xscaled < 1:
            geomnode.setX(0.5 - xscaled/2)
        geomnode.setScale(self.properties['scale'])
        geomnode.setX(geomnode.getX()+self.properties['offsethorizontal'])
        geomnode.setZ(geomnode.getZ()+self.properties['offsetvertical'])
        geomnode.setY(-self.properties['elevation'])
        geomnode.setP(int(self.properties['inclination'])-360)
        geomnode.setTexture(tex)
        geomnode.setTransparency(TransparencyAttrib.MAlpha)
        geomnode.reparentTo(self.node)
        self.node.setR(self.properties['rotation'])
    
    def getName(self):
        return self.properties['url']
    
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
        self.properties['rotation'] = float(self.properties['rotation'])
        self.properties['offsetwidth'] = float(self.properties['offsetwidth'])
        self.properties['offsetheight'] = float(self.properties['offsetheight'])
        self.properties['offsethorizontal'] = float(self.properties['offsethorizontal'])
        self.properties['offsetcollisionh'] = float(self.properties['offsetcollisionh'])
        self.properties['offsetcollisionv'] = float(self.properties['offsetcollisionv'])
        self.properties['offsetvertical'] = float(self.properties['offsetvertical'])
        self.properties['elevation'] = float(self.properties['elevation'])
        self.properties['scale'] = float(self.properties['scale'])
        
        self.updateTilePosition()
    
    #interface needed by PropertiesTable
    # regenerates the node at every change
    def onPropertiesUpdated(self):
        self.sanitizeProperties()
        self.generateNode()
        
    
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
        for key, value in props.iteritems():
            if key in self.properties:
                self.properties[key] = value
        self.onPropertiesUpdated()
    
    #called before destruction
    def destroy(self):
        #clearing old node
        if self.node != None:
            self.node.removeNode()
        
        if self.collisionNodeNp != None:
            self.collisionNodeNp.removeNode()
    
    #here for polymorph
    def getTileX(self):
        return self.parent.getX()
    
    #here for polymorph
    def getTileY(self):
        return self.parent.getY()
    
    def getWorldPos(self):
        return self.node.getPos(render)
