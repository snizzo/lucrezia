
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from mainwindow import Ui_MainWindow

from utilities import *
from MapExporter import MapExporter

import sys, os, string

'''

outgoing:
editor_loadmap [filename]
'''
class QTTest(QMainWindow):
    def __init__(self,pandaCallback): 
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #fills widget with found models on dataset folder
        self.fillPool()
        
        self.setWidgetEvents()
        
        # this basically creates an idle task
        self.timer = QTimer(self)
        self.connect( self.timer, SIGNAL("timeout()"), pandaCallback )
        self.timer.start(0)
        
    def setWidgetEvents(self):
        #self.ui.texturePool.itemDoubleClicked.connect(self.sendNewModel)
        self.ui.texturePool.currentItemChanged.connect(self.showPreview)
        self.ui.texturesFilter.textChanged.connect(self.applyFilter)
        self.ui.treeWidget.itemDoubleClicked.connect(self.toolTriggered)
        self.ui.actionLoad.triggered.connect(self.loadMap)
        self.ui.actionSave_Scene.triggered.connect(self.saveScene)
        self.ui.actionEdit_onLoad.triggered.connect(self.editOnLoad)
        self.ui.actionEdit_onUnload.triggered.connect(self.editOnUnload)
    
    def saveScene(self):
        m = MapExporter()
        m.save()
    
    def loadMap(self):
        filename = QFileDialog.getOpenFileName(self.ui.texturePool, 'Open Map', '', 'PandaRPG (*.map)')
        messenger.send("editor_loadmap", [filename])
    
    '''
    events handled by PropertiesTable
    '''
    def editOnLoad(self):
        messenger.send("open-editor-onLoad")
    
    '''
    events handled by PropertiesTable
    '''
    def editOnUnload(self):
        messenger.send("open-editor-onUnload")
    
    '''
    gui requests will be broadcasted
    '''
    def toolTriggered(self, item, column):
        if self.ui.texturePool.currentItem() != None:
            messenger.send(item.text(0).__str__(), [self.ui.texturePool.currentItem().text()])
            print "broadcasting: ", item.text(0), self.ui.texturePool.currentItem().text()
        else:
            messenger.send(item.text(0).__str__())
            print "broadcasting: ", item.text(0)
    
    def applyFilter(self, filt):
        self.ui.texturePool.clear()
        self.fillPool(filt)
    
    def showPreview(self, image, last):
        filepath = str(resourceManager.getResource(image.text()))
        pixmap = QPixmap(filepath)
        self.ui.label.setPixmap(pixmap.scaled(150,150,Qt.KeepAspectRatio))
    
    def fillPool(self, filt = ""):
        self.ui.texturePool.clear()
        files = Utilities.getSubfilesIn(resourceManager.get_path(), ['.png','.jpg'])
        for e in files:
            e = e.replace('../res/','').replace('.png','').replace('.jpg','')
            if filt == "": #if filtering disabled add all
                self.ui.texturePool.addItem(e)
            else: #if filtering enabled filter
                if e.find(filt) != -1:
                    self.ui.texturePool.addItem(e)
    
    #refactor
    def sendNewModel(self,item):
        filepath = str(item.text())  #casting due to compatibility issues
        messenger.send("addobject", [filepath])
