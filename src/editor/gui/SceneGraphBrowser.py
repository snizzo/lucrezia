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
    def __init__(self): 
        QMainWindow.__init__(self)
        self.ui = Ui_sceneGraphBrowser()
        self.ui.setupUi(self)
        
        #object delegate to draw an manage what's going on on the object/s properties table
        self.pt = PropertiesTable(self.ui.propertiesTable)
        
        #URGENT REFACTOR, MOVE IN APPROPRIATE CLASSE WITHOUT TOUCHING BASE
        base.accept("editor_analyzecell", self.loadCellInfo)
    
    def loadCellInfo(self, x, y):
        tile = pGrid.getTile(x, y)
        print tile.getNode()
