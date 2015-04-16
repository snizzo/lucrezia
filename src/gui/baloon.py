from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.task import Task
from direct.interval.LerpInterval import LerpColorInterval
from direct.interval.IntervalGlobal import *

from resourcemanager.resourcemanager import ResourceManager

from utils.fadeout import FadeOut
from utils.misc import Misc

import sys, os

'''
This class represent a single baloon, with text animation
'''
class Baloon(DirectObject):
    def __init__(self, who, message, target, speed):
        #text is in pure normal text
        #owner is in 
        self.pos = target.node.getPos()
        self.who = who
        self.message = list(message[::-1])
        self.textapplied = []
        self.startTime = 0.0
        self.elapsedTime = 0.0
        
        self.show()
    
    def textAnimation(self):
        taskMgr.doMethodLater(0.1, self.addLetter, 'showletters')
        
    def addLetter(self, Task):
        self.textapplied.append(self.message.pop())
        self.text.setText(''.join(self.textapplied))
        if not self.message:
            return Task.done
        else:
            return Task.again
    
    def show(self):
        print self.pos
        #text
        self.text = TextNode('baloontextnode')
        self.text.setTextColor(1, 1, 1, 1)
        self.text.setWordwrap(15.0)
        
        #card as background
        self.text.setFrameColor(0.7, 0.7, 0.7, 0.7)
        self.text.setFrameAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text.setCardColor(0.5, 0.5, 0.5, 1)
        self.text.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        self.text.setCardDecal(True)
        
        textnp = render.attachNewNode(self.text)
        textradius = textnp.getBounds().getRadius()/2
        textnp.setY(-0.5)
        textnp.setScale(0.37)
        textnp.setPos(self.pos.getX(),-1,self.pos.getZ()+2)
        textnp.setLightOff()
        
        self.textAnimation()