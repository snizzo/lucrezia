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

'''
class SceneGraphBrowser(QMainWindow):
    
    class SceneGraphBrowserHandler(DirectObject):
        def __init__(self, parent):
            self.parent = parent
        
        def enable(self):
            self.accept("editor_analyzecell", self.parent.loadCellInfo)
        
        def disable(self):
            self.ignoreAll()
    
    def __init__(self): 
        QMainWindow.__init__(self)
        self.ui = Ui_sceneGraphBrowser()
        self.ui.setupUi(self)
        
        self.handler = SceneGraphBrowser.SceneGraphBrowserHandler(self)
        self.handler.enable()
        
        #object delegate to draw an manage what's going on on the object/s properties table
        self.pt = PropertiesTable(self.ui.propertiesTable)
    
    def loadCellInfo(self, x, y):
        tile = pGrid.getTile(x, y)
        
        #tile not found
        if tile==-1:
            self.ui.cellinfo.setText("Current Tile: ("+str(x)+", "+str(y)+") (not exists)")
        else:
            self.ui.cellinfo.setText("Current Tile: ("+str(x)+", "+str(y)+")")
