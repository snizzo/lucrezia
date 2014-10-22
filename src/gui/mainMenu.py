from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from pandac.PandaModules import TransparencyAttrib
from direct.task import Task
from direct.fsm import FSM
from panda3d.core import LVecBase4f, CardMaker, NodePath
from direct.interval.LerpInterval import LerpColorInterval
from direct.interval.IntervalGlobal import *
from resourcemanager.resourcemanager import ResourceManager
from direct.showbase.Transitions import Transitions

from utils.fadeout import FadeOut

import sys, os, time

menuPlayable = True

class MainMenu(DirectObject):
    
    def generateWorld(self):
        f = FadeOut()
        
        Sequence(
         f.fadeIn(1),
         Func(self.hideAll),
         f.fadeOut(1)
        ).start()
        
    def __init__(self,lang):
        wp = WindowProperties()
        wp.setTitle("Menu Testing")
        wp.setSize(800, 600)
        
        self.mainFrame = DirectFrame(frameColor=(0, 0, 0, 1),
                      frameSize=(-2, 2, -2, 2),
                      pos=(0, 0, 0))
        
        self.background = OnscreenImage(image = resourceManager.getResource('misc/MenuBackground.png'), pos = (0, 0, 0), scale = (1.34, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.background.reparentTo(self.mainFrame)
        
        self.buttonMaps = loader.loadModel(resourceManager.getResource('misc/button_maps.egg'))

        self.startButton = DirectButton(text = "Premi invio", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_rollover"),
                                                         self.buttonMaps.find("**/button_disabled")), command=self.generateWorld, pos=(-1, 0, 0.6))
        self.startButton.reparentTo(self.mainFrame)
        
        
        if menuPlayable==True:
            self.setKey(True)
        else:
            self.setKey(False)
            
    def setKey(self, value):
        if value==True :
            self.accept("enter", self.enterDown)
        else:
            self.ignoreAll()
        
    def enterDown(self):
        print("ENTER")
        self.generateWorld()
        

    def hideAll(self):
        self.mainFrame.hide()
        self.setKey(False)