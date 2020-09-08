from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
#from pandac.PandaModules import TransparencyAttrib
from direct.task import Task
#from direct.fsm import FSM
#from panda3d.core import LVecBase4f, CardMaker, NodePath
#Sequence
from direct.interval.LerpInterval import LerpColorInterval
from direct.interval.IntervalGlobal import *

from resourcemanager.resourcemanager import ResourceManager
from gui.baloon import Baloon

from utils.fadeout import FadeOut
from utils.misc import Misc

import sys, os, collections

class BaloonManager(DirectObject):
    def __init__(self):
        #callback
        self.callback = None
        #module
        self.lock = False
        self.globalLock = False #very important for scripting engine
        self.queue = []
        
        #loading font once
        self.font = loader.loadFont(resourceManager.getResource('fonts/gnu-freefont_freesans/FreeSans.ttf'))
        
        self.accept("resumeGameplay", self.unlock)
        taskMgr.add(self.baloonTask, "baloonspawntask")
    
    def getFont(self):
        return self.font
    
    #APICALL
    #sets a function to be called when the message stack
    #reaches emptiness
    def setOnEmptyCallback(self, fun):
        self.callback = fun
    
    def clearCallback(self):
        self.callback = None
    
    #APICALL
    def pushThought(self, who, message, node, speed=0.015):
        targetNodeList = pGrid.getObjectsById(node)
        
        for n in targetNodeList:
            b = Baloon(self, who, message, n, speed, True)
            self.queue.append(b)
            self.globalLock = True
    
    #APICALL
    def push(self, who, message, node, speed=0.015):
        targetNodeList = pGrid.getObjectsById(node)
        
        for n in targetNodeList:
            b = Baloon(self, who, message, n, speed, False)
            self.queue.append(b)
            self.globalLock = True
    
    '''
    Unlocks and broadcast signals across the engine
    '''
    def unlock(self):
        self.lock = False
        
        #unlocking scripting engine
        if len(self.queue) == 0:
            self.globalLock = False
    
    ### DO RUN TASK
    def baloonTask(self, task):
        if self.lock == False and len(self.queue) > 0:
            baloon = self.queue.pop(0)
            self.lock = True
            baloon.show()
            baloon.requestPause()
        #onEmpty event
        if self.lock == False and len(self.queue) == 0:
            if isinstance(self.callback, collections.Callable):
                self.callback()
                self.clearCallback()
                
        return task.cont
    '''
    self.show()
        
    self.requestPause()
    '''
    
    def ping(self):
        print("pong")
