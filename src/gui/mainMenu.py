from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from pandac.PandaModules import TransparencyAttrib
from direct.task import Task
from direct.fsm import FSM
import sys, os

from resourcemanager.resourcemanager import ResourceManager

from direct.showbase.Transitions import Transitions

import time

menuPlayable = True

class MainMenu(DirectObject):

    def generateWorld(self):
        
        self.transition = Transitions(self.background)
        self.transition.setFadeColor(0,0,0)
        self.transition.fadeOut(2)
        
        self.mainFrame.hide()
        self.transition.fadeIn(2)
    
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
        
