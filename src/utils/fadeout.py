from panda3d.core import LVecBase4f, CardMaker, NodePath
from direct.interval.LerpInterval import LerpColorInterval, LerpColorScaleInterval
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib

class FadeOut(DirectObject):
    def __init__(self):
        self.cm = CardMaker("fadeout")
        self.cm.setFrame(-2,2,-2,2)
        self.cmnode = NodePath(self.cm.generate())
        self.cmnode.setTransparency(TransparencyAttrib.MAlpha)
        self.cmnode.setY(-1)
        self.cmnode.setColorScale(LVecBase4f(0.0,0.0,0.0,0.0))
        self.cmnode.reparentTo(aspect2d)
        
    def fadeIn(self, t):
        return LerpColorScaleInterval(self.cmnode,
                            t,
                            LVecBase4f(0.0,0.0,0.0,1.0),
                            LVecBase4f(0.0,0.0,0.0,0.0))
    
    def fadeOut(self, t):
        return LerpColorScaleInterval(self.cmnode,
                            t,
                            LVecBase4f(0.0,0.0,0.0,0.0),
                            LVecBase4f(0.0,0.0,0.0,1.0))
    
    def remove(self):
        self.cmnode.remove_node()
        