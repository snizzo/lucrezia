from pandac.PandaModules import CardMaker
from panda3d.core import NodePath, TextureStage
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import UvScrollNode

class Scrollable():
    
    def __init__(self, name, inclination, baseDimension):
        #public props
        self.baseDimension = baseDimension
        
        tex = loader.loadTexture('../res/'+name+'.png')
        
        xscaled = tex.getOrigFileXSize() / self.baseDimension
        yscaled = tex.getOrigFileYSize() / self.baseDimension
        
        cm = CardMaker("unscrollobject")
        cm.setFrame(0,xscaled,0,yscaled)
        
        ts = TextureStage('ts')
        ts.setMode(TextureStage.MDecal)
        
        uvscroll = UvScrollNode("uvscrollnode", 1,0.0,0.0,0.0)
        
        uvscroll.addChild(cm.generate())
        
        self.node = NodePath(uvscroll)
        self.node.setTwoSided(True)
        
        self.node.setX((-xscaled/2)+0.5)
        self.node.setP(-(360-int(inclination)))
        self.node.setTexture(tex)
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        self.node.reparentTo(render)
    
    def setX(self, x):
        self.node.setX(x)
    
    def setY(self, y):
        self.node.setZ(y)
 
