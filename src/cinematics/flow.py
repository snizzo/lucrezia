from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

from direct.showbase.DirectObject import DirectObject

import sys

class Flow(DirectObject):
    
    def __init__(self):
        self.globalLock = False
    
    def wait(self, seconds):
        self.globalLock = True
        script.addOneCustomLock(self)
        
        taskMgr.doMethodLater(seconds, self.release, 'releaseWait')
    
    def release(self, task):
        self.globalLock = False
        return Task.done
