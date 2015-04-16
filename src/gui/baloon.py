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
        self.speed = speed
        
        self.show()
        
        self.requestPause()
    
    def requestPause(self):
        messenger.send("pauseGameplay");
    
    def resumePause(self):
        messenger.send("resumeGameplay");
        self.textnp.remove_node()
        
    def canResumePause(self):
        self.accept("space", self.resumePause);
    
    def textAnimation(self):
        taskMgr.doMethodLater(self.speed, self.addLetter, 'showletters')
        
    def addLetter(self, Task):
        self.textapplied.append(self.message.pop())
        self.text.setText(''.join(self.textapplied))
        if not self.message:
            self.canResumePause()
            print "now pause can be resumed"
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
        
        self.textnp = render.attachNewNode(self.text)
        textradius = self.textnp.getBounds().getRadius()/2
        self.textnp.setY(-0.5)
        self.textnp.setScale(0.37)
        self.textnp.setPos(self.pos.getX(),-1,self.pos.getZ()+2)
        self.textnp.setLightOff()
        
        self.textAnimation()