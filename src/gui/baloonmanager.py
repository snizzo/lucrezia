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
from gui.baloon import Baloon

from utils.fadeout import FadeOut
from utils.misc import Misc

import sys, os

class BaloonManager(DirectObject):
    def __init__(self):
        pass
    
    def show(self, who, message, node, speed=0.05):
        targetNodeList = pGrid.getObjectsById(node)
        
        for n in targetNodeList:
            b = Baloon(who, message, n, speed)
    
    def ping(self):
        print "pong"