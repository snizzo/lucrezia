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
'''
class SceneGraphBrowser(QMainWindow):
    
    class SceneGraphBrowserHandler(DirectObject):
        def __init__(self, parent):
            self.parent = parent
        
        def enable(self):
            self.accept("editor_analyzecell", self.parent.loadCellInfo)
            self.accept("add texture to ground", self.parent.addCurrentTexture)
            self.accept("add object with texture in tile", self.parent.addObjectToTile)
        
        def disable(self):
            self.ignoreAll()
    
    '''
    used for minidom compatibility
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
        
        #object delegate to draw and manage what's going on on the object/s properties table
        self.pt = PropertiesTable(self.ui.propertiesTable)
    
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
