from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
#from pandac.PandaModules import TransparencyAttrib
#from direct.task import Task
#from direct.fsm import FSM
#from panda3d.core import LVecBase4f, CardMaker, NodePath
#Sequence
from direct.interval.LerpInterval import LerpColorInterval
from direct.interval.IntervalGlobal import *

from resourcemanager.resourcemanager import ResourceManager

from utils.fadeout import FadeOut
from utils.misc import Misc

import sys, os

#menu superclass (virtual)
class Intro(DirectObject):
    def __init__(self):
        self.background = 0
        x = float(configManager.getData("XSCREEN"))
        y = float(configManager.getData("YSCREEN"))
        self.ratio = x/y
        
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1),
                      frameSize=(-2, 2, -2, 2),
                      pos=(0, 0, 0))
        
        pass #lol
    
    def showImage(self, image):
        if self.background != 0:
            self.background.remove()
        
        #background
        self.background = OnscreenImage(image = resourceManager.getResource(image), pos = (0, 0, 0), scale = (self.ratio, 1, 1))
        self.background.reparentTo(self.frame)
    
    def clearAll(self):
        self.frame.destroy()
    
    def start(self):
        f = FadeOut()
        
        Sequence(
            f.fadeIn(0.05),
            Wait(0.05),
            Func(self.showImage, "misc/reavsoft.png"),
            f.fadeOut(2),
            Wait(8),
            f.fadeIn(2),
            Wait(2),
            Func(self.showImage, "misc/crywolf.png"),
            Wait(0.5),
            f.fadeOut(2),
            Wait(8),
            f.fadeIn(2),
            Wait(2),
            Func(self.clearAll),
            Func(mainMenu.show),
            Wait(0.5),
            f.fadeOut(2),
            Wait(2),
            Func(f.remove)
        ).start()
        