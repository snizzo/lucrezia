from panda3d.core import LVecBase4f, CardMaker, NodePath
from direct.interval.LerpInterval import LerpColorInterval
from direct.showbase.DirectObject import DirectObject

class FadeOut(DirectObject):
    def __init__(self):
        cm = CardMaker("fadeout")
        cm.setFrame(0,1,0,1)
        cmnode = NodePath(cm.generate())
        cmnode.setColor(0.0,0.0,0.0,1.0)
        cmnode.reparentTo(pixel2d)
        cmnode.setY(1)
        
        """ i = LerpColorInterval(cmnode,
                            2,
                            LVecBase4f(0.0,0.0,0.0,1.0),
                            LVecBase4f(0.0,0.0,0.0,0.0))
        i.start()"""