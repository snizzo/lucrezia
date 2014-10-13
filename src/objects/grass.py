#panda3d
from panda3d.core import NodePath, TextureStage, Texture

#pandamodules
from pandac.PandaModules import CardMaker
from pandac.PandaModules import TransparencyAttrib

#custom python
import random

#this class represents a cluster of grass blade for every tile in grid
class Grass():
    def __init__(self, attributes, baseDimension):
        
        self.baseDimension = baseDimension
        self.node = NodePath('brush')
        
        for i in range(40):
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)
            
            scale = random.uniform(0.7, 1.3)
            
            tex = loader.loadTexture(resourceManager.getResource('misc/grass_special.png'))
            tex.setWrapV(Texture.WM_clamp)
            tex.setWrapU(Texture.WM_clamp)
        
            xscaled = tex.getOrigFileXSize() / self.baseDimension
            yscaled = tex.getOrigFileYSize() / self.baseDimension
            
            cm = CardMaker("tileobject")
            cm.setFrame(-xscaled/2,xscaled/2,0,yscaled)
            
            grassnodenp = NodePath(cm.generate())
            grassnodenp.setTexture(tex)
            grassnodenp.setTransparency(TransparencyAttrib.MAlpha)
            grassnodenp.reparentTo(self.node)
            grassnodenp.setP(-330)
            grassnodenp.setX(x)
            grassnodenp.setZ(y)
            grassnodenp.setScale(scale)
            
    def getNode(self):
        return self.node
