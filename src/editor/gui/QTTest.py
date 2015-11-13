
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from mainwindow import Ui_MainWindow

from utilities import *

from TerrainPool import TerrainPool

import sys, os, string


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
		
		self.tp = TerrainPool(self.ui.terrainPool, self.ui.createTerrainButton, self.ui.modifyTerrainButton)
		
		self.ui.actionPPL.triggered.connect(myEventHandler.togglePerPixelLighting)
		self.ui.actionAmbientOcclusion.triggered.connect(myEventHandler.toggleAmbientOcclusion)
		self.ui.actionToonShading.triggered.connect(myEventHandler.toggleToonShading)
		
	def setWidgetEvents(self):
		self.ui.eggPool.itemDoubleClicked.connect(self.sendNewModel)
		self.ui.treeWidget.itemDoubleClicked.connect(self.toolTriggered)
	
	'''
	gui requests will be broadcasted
	'''
	def toolTriggered(self, item, column):
		print "broadcasting: ", item.text(0)
		messenger.send(item.text(0).__str__())
	
	def fillPool(self):
		self.ui.eggPool.clear()
		files = Utilities.getFilesIn(resourceManager.get_path())
		for e in files:
			self.ui.eggPool.addItem(e)
	
	def sendNewModel(self,item):
		filepath = str(item.text())  #casting due to compatibility issues
		messenger.send("addobject", [filepath])
