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
            self.background.remove_node()
        
        #background
        self.background = OnscreenImage(image = resourceManager.getResource(image), pos = (0, 0, 0), scale = (self.ratio, 1, 1))
        self.background.reparentTo(self.frame)
    
    def clearAll(self):
        self.frame.destroy()
    
    '''
    FIXME: not functional for some reason, inspect
    '''
    def quickstart(self):
        mainMenu.show()
    
    def start(self):
        f = FadeOut()
        
        speed = 1.0

        Sequence(
            Wait(2*speed),
            f.fadeIn(2*speed),
            Wait(2*speed),
            Func(self.showImage, "intro/panda3d.png"),
            f.fadeOut(2*speed),
            Wait(3*speed),
            f.fadeIn(2*speed),
            Wait(2*speed),
            Func(self.showImage, "intro/ramesesb.png"),
            f.fadeOut(2*speed),
            Wait(3*speed),
            f.fadeIn(2*speed),
            Wait(2*speed),
            Func(self.showImage, "intro/miyoki.png"),
            f.fadeOut(2*speed),
            Wait(3*speed),
            f.fadeIn(2*speed),
            Wait(2*speed),
            Func(audioManager.playMusic, "soundtrack/Game2.ogg", 2),
            Func(self.showImage, "intro/simonini.png"),
            f.fadeOut(2*speed),
            Wait(5*speed),
            f.fadeIn(2*speed),
            Wait(2*speed),
            Func(self.showImage, "intro/reavsoft.png"),
            f.fadeOut(2*speed),
            Wait(5*speed),
            f.fadeIn(2*speed),
            Wait(2*speed),
            Func(self.showImage, "intro/presents.png"),
            f.fadeOut(2*speed),
            Wait(5*speed),
            f.fadeIn(2*speed),
            Wait(2),
            Func(self.clearAll),
            Func(mainMenu.show), #change this with a lucrezia apicall
            Wait(0.5),
            f.fadeOut(2),
            Wait(2),
            Func(f.remove)
        ).start()

'''

            f.fadeIn(2),
            Wait(2),
            Func(self.showImage, "misc/truestory.png"),
            f.fadeOut(2),
            Wait(1),
'''
