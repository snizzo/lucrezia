from direct.showbase.DirectObject import DirectObject 
from panda3d.core import *

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

from utilities import *

'''
Object that analyze and build up the scene graph in
the right (upper) window
'''
class SceneGraphAnalyzer(DirectObject):
    def __init__(self,root,tree):
        self.tree = tree
        self.rootNode = root #storing our temporary root node
        self.parent = None
        
        #qt4 event bindings
        self.tree.itemClicked.connect(self.changeSelection)
        
        #panda3d event bindings
        self.accept("refresh scenetree", self.refresh)
    
    def refresh(self):
        #clear up all the scene
        self.eraseAll()
        
        #adding all the others
        self.generate()
        
        self.expandAll(self.tree.topLevelItem(0))
    
    def expandAll(self,item):
        if not Utilities.hasFileExtension(item.text(0).__str__()):
            self.tree.expandItem(item)
            
            childList = []
            
            for childIndex in range(item.childCount()):
                self.expandAll(item.child(childIndex))
    
    def changeSelection(self, item):
        myCamera.st.forceSelection(item.text(0).__str__())
    
    def addItem(self):
        pass
    
    def eraseAll(self):
        pass
    
    def generate(self):
        pass
    
    #
    # recursive function that fills the scene node
    # no more limited at .egg structures
    #
    def browse(self,node):
        pass
