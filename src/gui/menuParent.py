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

import sys, os

menuPlayable=True
index = 0
position = 0

class MenuParent(DirectObject):
    
    def __init__(self,lang):
        wp = WindowProperties()
        wp.setTitle("Menu Testing")
        wp.setSize(800, 600)
        #creating object for every menu
        
        #enter menu
        self.enter = enterMenu(lang)
        #main menu
        self.main = mainMenu(lang) 
        #>>>config menu
        self.config = configMenu(lang)
        
        
        self.menustr = [self.enter, self.main, self.config, 0]
        
        self.menustr[index].show()
        
        if menuPlayable==True:
            self.setKey(True)
        else:
            print("disabled")
            self.setKey(False)
    
    def setKey(self, value):
        if value==True :
            self.accept("enter", self.enterDown)
            """
            self.accept("mouse1", self.ignore)
            """
            
            self.accept("arrow_up", self.arrowUpDown)
            self.accept("arrow_down", self.arrowDownDown)
            
        else:
            self.ignoreAll()
    
    def arrowUpDown(self):
        print("V")
        if (index!=0): 
            self.movecursor(-1)
            print("%d : %d" % (index,position))
        
    def arrowDownDown(self):
        print("A")
        if (index!=0):
            self.movecursor(1)
            print("%d : %d" % (index,position))
            
    def movecursor(self,value):
        print(value)
        self.menustr[index].cursorMove(value)
    
    def enterDown(self):
        print("enter")
        """
        DA SISTEMARE
        """
        self.check = index
        self.menustr[index].event()
        self.change(self.check)
        
    def change(self,check):
        print("change")
        if (check != index):
            if (self.menustr[index] != 0):
                self.menustr[index].show()
            else:
                self.setKey(False)
        
#================================================================================================

class menu:
    """ Class for a generic menu """
    def __init__(self,lang,image):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1),
                      frameSize=(-2, 2, -2, 2),
                      pos=(0, 0, 0))
        
        self.background = OnscreenImage(image = resourceManager.getResource(image), pos = (0, 0, 0), scale = (1.34, 1, 1))
        self.background.setTransparency(TransparencyAttrib.MAlpha)
        self.background.reparentTo(self.frame)
        
        self.buttonMaps = loader.loadModel(resourceManager.getResource('misc/button_maps.egg'))
        self.frame.hide()
    
    def show(self):
        self.frame.show()    
        
    def close(self):
        if ((index == 1)and(position == 0)):
            f = FadeOut()
            Sequence(
             f.fadeIn(1),
             Func(self.hide),
             f.fadeOut(1)
            ).start()
        else:
            self.hide()
            
    def hide(self):
        self.frame.hide()


class enterMenu(menu):
    """ Class for the intro menu """
    def __init__(self,lang):
        #ENTERFRAME
        menu.__init__(self,lang,'misc/MenuBackground.png')
        
        #self.buttonMaps = loader.loadModel(resourceManager.getResource('misc/button_maps.egg'))
                #buttons
        self.startButton = DirectButton(text = "Premi invio", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_disabled")), pos=(0, 0, -0.5))
        self.startButton.reparentTo(self.frame)
        
    def event(self):
        self.close()
        global index
        index += 1

    def show(self):
        menu.show(self)
        
    def close(self):
        menu.close(self)
        
class  mainMenu(menu):
    buttons = []
    
    """ Class for the main menu """
    def __init__(self,lang):
        #MAIN FRAME
        menu.__init__(self,lang,'misc/MenuBackground1.png')
        
        #self.buttonMaps = loader.loadModel(resourceManager.getResource('misc/button_maps.egg'))
                #buttons
        self.startButton = DirectButton(text = "Nuovo Gioco", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_disabled")), pos=(0, 0, 0.7))
        self.startButton.reparentTo(self.frame)
        
        self.loadButton = DirectButton(text = "Carica Partita", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_disabled")), pos=(0, 0, 0.2))
        self.loadButton.reparentTo(self.frame)
        
        self.configButton = DirectButton(text = "Impostazioni", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_disabled")), pos=(0, 0, -0.3))
        self.configButton.reparentTo(self.frame)
          
        self.exitButton = DirectButton(text = "Esci", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_disabled")), pos=(0, 0, -0.8))
        self.exitButton.reparentTo(self.frame)  
   
    def cursorMove(self,value):        
        global buttons
        global position
        
        self.i=position
        if(position + value == len(buttons)):
            position = 0
        elif(position + value == -1):
            position = 3
        else:
            position = position + value
        print("========")
        print(len(buttons))
        print(self.i)
        print(position)
        print("========")

        buttons[self.i]["state"] = DGG.DISABLED
        
        buttons[position]["state"] = DGG.NORMAL

    def event(self):
        global index
        # new game
        if (position==0):
            self.close()
            index += 2    
        # instruction
        elif (position==2):
            self.close()
            index += 1 
        
    def show(self):
        global buttons
        global position
        buttons = [self.startButton,self.loadButton,self.configButton,self.exitButton]
        for button in buttons:
            button["state"] = DGG.DISABLED
        
        buttons[position]["state"] = DGG.NORMAL
        menu.show(self)    
        
    def close(self):
        menu.close(self)


class configMenu(menu):
    
    buttons = []
    
    """ Class for the config menu """
    def __init__(self,lang):
        #MAIN FRAME
        menu.__init__(self,lang,'misc/MenuBackground1.png')
        
        #self.buttonMaps = loader.loadModel(resourceManager.getResource('misc/button_maps.egg'))
                #buttons

        self.exitButton = DirectButton(text = "Esci", text_scale=(0.07, 0.07), relief=None, geom= (self.buttonMaps.find("**/button_ready"),
                                                         self.buttonMaps.find("**/button_click"),
                                                         self.buttonMaps.find("**/button_disabled")), pos=(0.4, 0, -0.8))
        self.exitButton.reparentTo(self.frame)  
    
    
    def cursorMove(self,i):        
        pass
        
    def event(self):
        self.close()
        global index
        global position
        index -= 1
        position = 2
        
        
    def show(self):
        global buttons
        buttons = [self.exitButton]
        for button in buttons:
            button["state"] = DGG.DISABLED
        
        self.exitButton["state"] = DGG.NORMAL
        menu.show(self)    
        
    def close(self):
        menu.close(self)


   