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
        self.pos = target.getWorldPos()
        self.who = who
        self.message = list(message[::-1])
        self.textapplied = [who,':\n']
        self.speed = speed
        
        '''
        for i in range(len(self.message)):
            self.textapplied.append(' ')
        '''
        
        #good default?
        self.openCloseSpeed = 0.2
    
    def requestPause(self):
        messenger.send("pauseGameplay");
    
    def resumePause(self):
        closeInterval = self.textnp.scaleInterval(self.openCloseSpeed, 0.0001, 0.37)
        Sequence(
            closeInterval,
            Func(messenger.send, "resumeGameplay"),
            Func(self.ignoreAll),
            Func(self.textnp.remove_node)
        ).start()
        
        '''
        messenger.send("resumeGameplay");
        self.ignoreAll()
        self.textnp.remove_node()
        '''
        
    def canResumePause(self):
        self.accept("space", self.resumePause);
    
    def textAnimation(self):
        taskMgr.doMethodLater(self.speed, self.addLetter, 'showletters')
        self.textnp.scaleInterval(self.openCloseSpeed, 0.37, 0.0001).start()
        
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
        self.requestPause()
        
        #text
        self.textbg = TextNode('baloontextnodebg')
        self.textbg.setTextColor(0.5, 0.5, 0.5, 0)
        self.textbg.setWordwrap(13.0)
        self.textbg.setText(''.join([self.who,":\n"]+self.message))
        
        #card as background
        self.textbg.setFrameColor(0.7, 0.7, 0.7, 0.6)
        self.textbg.setFrameAsMargin(0.4, 0.4, 0.4, 0.3)
        self.textbg.setCardColor(0.5, 0.5, 0.5, 0.67)
        self.textbg.setCardAsMargin(0.4, 0.4, 0.4, 0.3)
        self.textbg.setCardDecal(True)
        
        #text
        self.text = TextNode('baloontextnode')
        self.text.setTextColor(1, 1, 1, 1)
        self.text.setWordwrap(13.0)
        
        self.textnp = render.attachNewNode(self.text)
        textradius = self.textnp.getBounds().getRadius()/2
        self.textnp.setY(-0.5)
        self.textnp.setScale(0.0001)
        self.textnp.setPos(self.pos.getX()+0.5,-1,self.pos.getZ()+2.25)
        self.textnp.setLightOff()
        self.textbgnode = self.textnp.attachNewNode(self.textbg)
        self.textbgnode.setY(0.1)
        
        self.textAnimation()
