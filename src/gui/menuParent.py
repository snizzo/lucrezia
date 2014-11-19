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

#menu superclass (virtual)
class Menu(DirectObject):
    def __init__(self,lang,image):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1),
                      frameSize=(-2, 2, -2, 2),
                      pos=(0, 0, 0))
        
        x = float(configManager.getData("XSCREEN"))
        y = float(configManager.getData("YSCREEN"))
        
        self.cursor = 0   # tracks the currently selected button
        self.buttons = [] # list of buttons
        self.ratio = x/y  # used to set correctly quads
        self.currenty = 0 # used to set correctly button vertical position
        self.spacebetweenbuttons = 0.3 # space offset between buttons
        
        #background
        self.background = OnscreenImage(image = resourceManager.getResource(image), pos = (0, 0, 0), scale = (self.ratio, 1, 1))
        self.background.reparentTo(self.frame)
        
        self.buttonMaps = loader.loadModel(resourceManager.getResource('misc/button_maps.egg'))
        self.frame.hide()
        
        #first refresh ever
        self.refreshKeyState()
    
    def disableAll(self):
        for button in self.buttons:
                button['state'] = DGG.DISABLED
    
    def refreshKeyState(self):
        self.disableAll()
        
        if len(self.buttons) > 0 and self.cursor <= len(self.buttons): #avoid crashing in empty menus or cursor overload (no buttons or too many)
            self.buttons[self.cursor]['state'] = DGG.NORMAL #todo change here something
    
    def printButtonState(self):
        for button in self.buttons:
                print button['state']
    
    def setKey(self, value):
        if value == True:
            self.accept("enter", self.onEnter)
            self.accept("arrow_up", self.onArrowUp)
            self.accept("arrow_down", self.onArrowDown)
        else:
            self.ignoreAll()
    
    def onEnter(self):
        self.buttons[self.cursor].getPythonTag("callback")()
    
    def onArrowUp(self):
        if self.cursor == 0:
            self.cursor = len(self.buttons)-1
        else:
            self.cursor -= 1
        self.refreshKeyState()
    
    def onArrowDown(self):
        if self.cursor == len(self.buttons)-1:
            self.cursor = 0
        else:
            self.cursor += 1
        self.refreshKeyState()
    
    '''
    Callback on return pressed when cursor is at correct position
    '''
    def addButton(self, mtext, callback):
        
        #all a line of code lol
        self.btn = DirectButton(text = mtext, text_scale=(0.085, 0.085), relief=None, geom= (Misc.loadImageAsPlane(resourceManager.getResource("misc/button_ready.png")),
        self.buttonMaps.find("**/button_click"),
        Misc.loadImageAsPlane(resourceManager.getResource("misc/button_disabled.png"))), pos=(0, 0, self.currenty))
        
        self.btn.setPythonTag("callback", callback)
        self.btn.reparentTo(self.frame)
        self.buttons.append(self.btn)
        self.currenty -= self.spacebetweenbuttons
        
        self.refreshKeyState() # refreshing :)
        #self.printButtonState()
    
    def getNode(self):
        return self.frame
    
    def setX(self, x):
        for button in self.buttons:
            button.setX(button.getX()+x)
    
    def setY(self, z):
        for button in self.buttons:
            button.setZ(button.getZ()+z)
    
    def setSpaceBetweenButtons(self, v):
        self.spacebetweenbuttons = v
    
    def show(self):
        self.frame.show() #show main frame
        self.setKey(True)
        
    def close(self):
        self.hide()
            
    def hide(self):
        self.frame.hide()

'''
Reference example on how a menu should be
'''
class MainMenu(Menu):
    
    """ Class for the main menu """
    def __init__(self,lang):
        
        #MAIN FRAME
        Menu.__init__(self,lang,'menu/mainmenubg.png')
        self.addButton("New game", self.onNewGame)
        self.addButton("Load game", self.onLoadGame)
        self.addButton("Wake up", self.onWakeUp)
        
        self.setX(-1.0)
        
        self.show()
        
    def onNewGame(self):
        self.close()
        
    def onLoadGame(self):
        print "loadgame triggered"
    
    def onWakeUp(self):
        print "wakeup triggered"
    
    #override
    def close(self):
        Sequence(
            Func(messenger.send, 'changeMap', ['camera.map','5,6']), #using map api to change map
            Wait(1),
            Func(Menu.close, self)
            ).start()