from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.task import Task
from direct.interval.LerpInterval import LerpColorInterval
from direct.interval.IntervalGlobal import *

from resourcemanager.resourcemanager import ResourceManager

from utils.fadeout import FadeOut
from utils.misc import Misc

import sys, os, math

'''
This class represent a single baloon, with text animation
'''
class Baloon(DirectObject):
    def __init__(self, parent, who, message, target, speed, thought):
        #text is in pure normal text
        #owner is in 
        self.pos = target.getWorldPos()
        self.who = who
        self.message = list(message[::-1])
        self.textapplied = [who,':\n']
        self.speed = speed
        self.isThought = thought
        self.parent = parent
        
        '''
        for i in range(len(self.message)):
            self.textapplied.append(' ')
        '''
        
        #good default?
        self.openCloseSpeed = 0.25 #0.25
    
    def requestPause(self):
        messenger.send("pauseGameplay");
        print(pGrid.getPlayable())
        print("requesting pause...")
    
    def resumePause(self):
        closeInterval = self.textnp.scaleInterval(self.openCloseSpeed, 0.0001, 0.25)
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
    
    #TODO: implement
    def setAutomaticWordwrap(self, minimum):
        i = 0
        j = 0
        previous = 0
        latest = 0
        rmessage = self.message[::-1]
        for letter in rmessage:
            if letter == ' ':
                previous = i
                if j > minimum:
                    if math.fabs(previous - i) < j:
                        rmessage[previous] = '\n'
                    else:
                        rmessage[i] = '\n'
                    j = 0
                
            i += 1
            j += 1
        self.message = rmessage[::-1]
            
    def canResumePause(self):
        self.accept("space", self.resumePause);
    
    def textAnimation(self):
        taskMgr.doMethodLater(self.speed, self.addLetter, 'showletters')
        self.textnp.scaleInterval(self.openCloseSpeed, 0.25, 0.0001).start()
        
    def addLetter(self, Task):
        self.textapplied.append(self.message.pop())
        self.text.setText(''.join(self.textapplied))
        if not self.message:
            self.canResumePause()
            #print("now pause can be resumed")
            return Task.done
        else:
            return Task.again
    
    def show(self):
        self.requestPause()
        
        self.setAutomaticWordwrap(30)
        
        #text
        self.textbg = TextNode('baloontextnodebg')
        self.textbg.setTextColor(0.5, 0.5, 0.5, 0)
        self.textbg.setFont(self.parent.getFont())
        #self.textbg.setWordwrap(13.0)
        self.textbg.setText(''.join([self.who,":\n"]+self.message))
        
        #card as background
        self.textbg.setFrameColor(0.7, 0.7, 0.7, 0.6)
        self.textbg.setFrameAsMargin(0.4, 0.8, 0.4, 0.3)
        if self.isThought:
            self.textbg.setCardColor(0.2, 0.2, 0.2, 0.4)
        else:
            self.textbg.setCardColor(0.5, 0.5, 0.5, 0.75)
        self.textbg.setCardAsMargin(0.4, 0.8, 0.4, 0.3)
        self.textbg.setCardDecal(True)
        self.height = self.textbg.getHeight()
        self.width = self.textbg.getWidth()
        
        print(self.height)
        print(self.width)
        
        #text
        self.text = TextNode('baloontextnode')
        self.text.setFont(self.parent.getFont())
        self.text.setShadow(0.05, 0.05)
        if self.isThought:
            self.text.setTextColor(0.4, 0.4, 0.4, 0.7)
        else:
            self.text.setTextColor(1, 1, 1, 1)
        #self.text.setWordwrap(13.0)
        
        self.textnp = render.attachNewNode(self.text)
        self.textnp.setY(-0.5)
        self.textnp.setScale(0.0001)
        self.textnp.setPos(self.pos.getX()+0.5-self.width/6,-1,self.pos.getZ()+1+self.height/2)
        self.textnp.setLightOff()
        self.textnp.setDepthTest(False)
        self.textbgnode = self.textnp.attachNewNode(self.textbg)
        self.textbgnode.setY(0.1)
        
        self.textAnimation()
