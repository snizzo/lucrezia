#panda3d
from panda3d.core import NodePath, TextureStage, Texture

#pandamodules
from pandac.PandaModules import CardMaker
from pandac.PandaModules import TransparencyAttrib

#custom python
import random

from grid.GameEntity import GameEntity
from grid.XMLExportable import XMLExportable
from editor.gui.PropertiesTableAbstract import PropertiesTableAbstract

#this class represents a cluster of grass blade for every tile in grid
class Grass(GameEntity, PropertiesTableAbstract, XMLExportable):
    def __init__(self, attributes, baseDimension):
        
        self.baseDimension = baseDimension
        self.node = NodePath('brush')
        self.typeName = "grass"
        self.properties = {
            'minuniform' : '',
            'maxuniform' : '',
            'density' : '',
            'id' : ''
        }
        
        #local override
        if attributes.has_key('minuniform'):
            self.properties['minuniform'] = float(attributes['minuniform'].value)
            self.properties['minuniform'] = 0.35
        else:
            self.properties['minuniform'] = 0.35
        
        #local override
        if attributes.has_key('maxuniform'):
            self.properties['maxuniform'] = float(attributes['maxuniform'].value)
            self.properties['maxuniform'] = 0.5
        else:
            self.properties['maxuniform'] = 0.5
        
        #local override
        if attributes.has_key('density'):
            self.properties['density'] = int(attributes['density'].value)
            self.properties['density'] = 8
        else:
            self.properties['density'] = 8
        
        self.generateNode()
    
    def generateNode(self):
        self.node.remove_node()
        self.node = NodePath('brush')
        
        for i in range(self.properties['density']):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            
            scale = random.uniform(self.properties['minuniform'], self.properties['maxuniform'])
            
            tex = loader.loadTexture(resourceManager.getResource('misc/grass_special.png'))
            tex.setWrapV(Texture.WM_clamp)
            tex.setWrapU(Texture.WM_clamp)
            
            #this is true pixel art
            #change to FTLinear for linear interpolation between pixel colors
            tex.setMagfilter(Texture.FTNearest)
            tex.setMinfilter(Texture.FTNearest)
        
            xscaled = tex.getOrigFileXSize() / self.baseDimension
            yscaled = tex.getOrigFileYSize() / self.baseDimension
            
            cm = CardMaker("tileobject")
            cm.setFrame(-xscaled/2,xscaled/2,0,yscaled)
            
            grassnodenp = NodePath(cm.generate())
            grassnodenp.setTexture(tex)
            grassnodenp.setTransparency(3)
            #grassnodenp.setTransparency(TransparencyAttrib.MMultisample)
            grassnodenp.reparentTo(self.node)
            grassnodenp.setP(-355)
            grassnodenp.setX(x)
            grassnodenp.setZ(y)
            grassnodenp.setScale(scale)
            
    def getNode(self):
        return self.node
    
    '''XMLExportable'''
    def xmlAttributes(self):
        return self.properties
    
    def xmlTypeName(self):
        return self.typeName
    
    '''Editor integration'''
    def getName(self):
        return 'Grass object'
    
    '''
    Sanitize properties data to be of correct type from string
    '''
    def sanitizeProperties(self):
        #sanitizing data
        self.properties['minuniform'] = float(self.properties['minuniform'])
        self.properties['maxuniform'] = float(self.properties['maxuniform'])
        self.properties['density'] = int(self.properties['density'])
    
    #interface needed by PropertiesTable
    # regenerates the node at every change
    def onPropertiesUpdated(self):
        self.sanitizeProperties()
        
        self.generateNode()
    
    def getPropertyList(self):
        return self.properties
    
    def setProperty(self, key, value):
        self.properties[key] = value
    
    def destroy(self):
        self.node.remove_node()
