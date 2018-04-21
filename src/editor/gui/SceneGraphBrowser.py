from direct.showbase.DirectObject import DirectObject 
from panda3d.core import *

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

#custom imports
from SceneGraphBrowserUi import Ui_sceneGraphBrowser

from PropertiesTable import PropertiesTable
from SceneGraphAnalyzer import SceneGraphAnalyzer

'''
Scene graph window class
ingoing:
editor_analyzecell [x] [y]
add texture to ground [texture]
add Light
'''
class SceneGraphBrowser(QMainWindow):
    
    class SceneGraphBrowserHandler(DirectObject):
        def __init__(self, parent):
            self.parent = parent
        
        def enable(self):
            self.accept("editor_analyzecell", self.parent.loadCellInfo)
            self.accept("add texture to ground", self.parent.addCurrentTexture)
            self.accept("add object with texture in tile", self.parent.addObjectToTile)
            self.accept("add Light", self.parent.addLightToTile)
            self.accept("add character", self.parent.addCharacterToTile)
        
        def disable(self):
            self.ignoreAll()
    
    '''
    used for minidom compatibility injection when creating new object
    '''
    class MiniValue:
        def __init__(self, s):
            self.value = s
    
    def __init__(self): 
        QMainWindow.__init__(self)
        self.currentx = 0
        self.currenty = 0
        
        self.ui = Ui_sceneGraphBrowser()
        self.ui.setupUi(self)
        
        self.handler = SceneGraphBrowser.SceneGraphBrowserHandler(self)
        self.handler.enable()
        
        self.ui.deleteCurrent.clicked.connect(self.onDeleteCurrent)
        self.ui.tileObjects.itemClicked.connect(self.onItemClicked)
        self.ui.onPickedButton.clicked.connect(self.onPickedButtonClicked)
        self.ui.onWalkedButton.clicked.connect(self.onWalkedButtonClicked)
        
        #increase propertis
        self.ui.increaseButton.clicked.connect(self.onIncreaseButtonClicked)
        self.ui.increase2Button.clicked.connect(self.onIncrease2ButtonClicked)
        self.ui.increase3Button.clicked.connect(self.onIncrease3ButtonClicked)
        
        #decrease properties
        self.ui.decreaseButton.clicked.connect(self.onDecreaseButtonClicked)
        self.ui.decrease2Button.clicked.connect(self.onDecrease2ButtonClicked)
        self.ui.decrease3Button.clicked.connect(self.onDecrease3ButtonClicked)
        
        #copy/paste
        self.ui.copyButton.clicked.connect(self.onCopyButtonClicked)
        self.ui.pasteButton.clicked.connect(self.onPasteButtonClicked)
        
        self.ui.colorPickerButton.clicked.connect(self.onColorPickerButtonClicked)
        
        #object delegate to draw and manage what's going on on the object/s properties table
        self.pt = PropertiesTable(self.ui.propertiesTable)
    '''
    All these events will be handled by PropertiesTable!
    '''
    def onCopyButtonClicked(self):
        messenger.send('copyProperties')
    
    def onPasteButtonClicked(self):
        messenger.send('pasteProperties')
    
    def onIncreaseButtonClicked(self):
        messenger.send('increaseProperty', [1])
    
    def onIncrease2ButtonClicked(self):
        messenger.send('increaseProperty', [7])
        
    def onIncrease3ButtonClicked(self):
        messenger.send('increaseProperty', [20])
    
    def onDecreaseButtonClicked(self):
        messenger.send('decreaseProperty', [1])
    
    def onDecrease2ButtonClicked(self):
        messenger.send('decreaseProperty', [7])
    
    def onDecrease3ButtonClicked(self):
        messenger.send('decreaseProperty', [20])
    
    def onColorPickerButtonClicked(self):
        messenger.send('colorPicker')
    
    def onPickedButtonClicked(self):
        messenger.send('open-editor-onPicked')
        
    def onWalkedButtonClicked(self):
        messenger.send('open-editor-onWalked')
    '''
    End of events handled by prop tables
    '''
    
    def onDeleteCurrent(self):
        tile = pGrid.getTile(self.currentx, self.currenty)
        item = self.ui.tileObjects.currentItem()
        position = self.ui.tileObjects.row(item)
        if position == 1:
            self.clearCurrentTextures()
        if position > 2:
            #position is position -2  because we have to delete 2 informative items
            #('ground textures' and 'game objects') from the list
            tile.deleteObjectAt(position-3)
    
    def onItemClicked(self, item):
        tile = pGrid.getTile(self.currentx, self.currenty)
        position = self.ui.tileObjects.row(item)
        if position == 1:
            messenger.send("selected one", [tile])
        if position > 2:
            #position is position -2  because we have to delete 2 informative items
            #('ground textures' and 'game objects') from the list
            messenger.send("selected one", [tile.getObjectAt(position-3)])
    
    def addCurrentTexture(self, t):
        tile = pGrid.getTile(self.currentx, self.currenty)
        
        attributes = { 'url' : SceneGraphBrowser.MiniValue(t.__str__()) }
        tile.addTexture(attributes)
    
    def addObjectToTile(self, t):
        tile = pGrid.getTile(self.currentx, self.currenty)
        
        attributes = { 'url' : SceneGraphBrowser.MiniValue(t.__str__()) }
        tile.addObject(attributes)
        self.loadCellInfo(self.currentx, self.currenty)
    
    def addCharacterToTile(self, t):
        tile = pGrid.getTile(self.currentx, self.currenty)
        
        playablepos = Point3(self.currentx, self.currenty, 0)
        attributes = { 'url' : SceneGraphBrowser.MiniValue(t.__str__()) }
        tile.addCharacter(attributes, True, playablepos)
        self.loadCellInfo(self.currentx, self.currenty)
    
    def addLightToTile(self, dummy_param=None):
        tile = pGrid.getTile(self.currentx, self.currenty)
        
        #on="true" distance="1" color="255,150,10" attenuation="0.02"
        attributes = { 'on' : SceneGraphBrowser.MiniValue('true'),
                        'distance' : SceneGraphBrowser.MiniValue('1'),
                        'color' : SceneGraphBrowser.MiniValue('255,150,10'),
                        'attenuation' : SceneGraphBrowser.MiniValue('0.02')}
        tile.addLight(attributes)
        self.loadCellInfo(self.currentx, self.currenty)
    
    def clearCurrentTextures(self):
        if self.currentx != -1 and self.currenty != -1:
            tile = pGrid.getTile(self.currentx, self.currenty)
            tile.clearAllTextures()
        else:
            print "Warning: attempted deleting textures on non-existent cell"
    
    def loadCellInfo(self, x, y):
        self.ui.tileObjects.clear() #clearing texture list
        
        tile = pGrid.getTile(x, y)
        
        #tile not found
        if tile==-1:
            self.ui.cellinfo.setText("Current Tile: ("+str(x)+", "+str(y)+") (not exists)")
            self.currentx = -1
            self.currenty = -1
        else:
            self.ui.cellinfo.setText("Current Tile: ("+str(x)+", "+str(y)+")")
            self.currentx = x
            self.currenty = y
            
            messenger.send("selected one", [tile])
            
            self.ui.tileObjects.addItem('--Ground Texture--')
            
            for t in tile.getTextures():
                self.ui.tileObjects.addItem(t)
            
            self.ui.tileObjects.addItem('--Game Objects--')

            for o in tile.getGameObjects():
                self.ui.tileObjects.addItem(o.getName())
