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

'''
This class handles all baloons around the screen
'''
class BaloonManager(DirectObject):
    def __init__(self):
        print "new baloon spawned!"
        
        self.allBaloons = []
    
    def show(self, who, message):
        print "attempt to show a baloon:"
        print who
        print message
        
        #text
        text = TextNode('baloontextnode')
        text.setTextColor(1, 1, 1, 1)
        text.setWordwrap(15.0)
        text.setText(message)
        
        #card as background
        text.setFrameColor(1, 1, 1, 1)
        text.setFrameAsMargin(0.2, 0.2, 0.2, 0.1)
        text.setCardColor(0,0,0,0.6)
        text.setCardAsMargin(0.2, 0.2, 0.2, 0.1)
        text.setCardDecal(True)
        
        textnp = render.attachNewNode(text)
        textradius = textnp.getBounds().getRadius()/2
        textnp.setY(-0.5)
        textnp.setScale(0.27)
        
        '''
        #actually loading texture
        tex = loader.loadTexture(resourceManager.getResource(name)+'.png')
        tex.setWrapV(Texture.WM_clamp)
        tex.setWrapU(Texture.WM_clamp)
        '''
        
        #baloon.setTexture(tex)