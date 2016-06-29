from panda3d.core import LVecBase4f, CardMaker, NodePath
from direct.interval.LerpInterval import LerpColorInterval, LerpColorScaleInterval
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import TextNode

#useful for apicall integration (timed with domethodlater)
class FadingTextManager():
    def __init__(self):
        pass
    
    def spawn(self, text, x=0.55, z=-0.5, scale=0.09, r=1.0, g=1.0, b=1.0):
        FadingText(text, x, z, scale, r, g, b)

class FadingText(DirectObject):
    def __init__(self, text, x, z, scale, r, g, b):
        self.x = x
        self.z = z
        self.scale = scale
        self.r = r
        self.g = g
        self.b = b
        
        textnode = TextNode('fadingtext')
        textnode.setText(text)
        self.node = aspect2d.attachNewNode(textnode)
        self.node.setScale(self.scale)
        
        self.node.setTransparency(TransparencyAttrib.MAlpha)
        self.node.setPos(self.x,-1,self.z)
        self.node.setColorScale(LVecBase4f(self.r,self.g,self.b,0.0))
        self.node.reparentTo(aspect2d)
        
        delay = 3.0
        seq = Sequence(
            self.fadeIn(delay),
            Wait(delay),
            self.fadeOut(delay)
        )
        seq.start()
        
    def fadeIn(self, t):
        return LerpColorScaleInterval(self.node,
                            t,
                            LVecBase4f(self.r,self.g,self.b,1.0),
                            LVecBase4f(self.r,self.g,self.b,0.0))
    
    def fadeOut(self, t):
        return LerpColorScaleInterval(self.node,
                            t,
                            LVecBase4f(self.r,self.g,self.b,0.0),
                            LVecBase4f(self.r,self.g,self.b,1.0))
    
    def remove(self):
        self.node.remove_node()
