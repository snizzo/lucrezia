from direct.showbase.DirectObject import DirectObject

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

from utilities import *

import sys, os, string

class TerrainPool(DirectObject):
	def __init__(self, pool, create, modify):
		#setting initial terrain list
		self.pool = pool
		self.create = create
		self.modify = modify
		
		self.create.clicked.connect(self.createTerrain)
		self.modify.clicked.connect(self.modifyTerrain)
		
		self.pool.itemDoubleClicked.connect(self.loadTerrain)
		
		self.accept("refresh-terrain-pool", self.refreshPool)
		
		self.refreshPool()
	
	def createTerrain(self):
		print "INFO: create terrain triggered"
		#calling third part tools used to edit terrains
		messenger.send("third-party", ["terrain", ""]) #run a third party tool to edit terrain
	
	def modifyTerrain(self):
		item = self.pool.selectedItems()
		if len(item)<1:
			print "ERROR: must select a map to modify"
		else:
			mapName = str(item[0].text())
			messenger.send("third-party", ["terrain", "-m " + mapName]) #run a third party tool to edit terrain
	
	def refreshPool(self):
		self.pool.clear()
		terrains = Utilities.getEverythingIn("external_tools/sleep_source/maps")
		for t in terrains:
			self.pool.addItem(t)
	
	def loadTerrain(self,item):
		filepath = "external_tools/sleep_source/maps/"+str(item.text())  #casting due to compatibility issues
		messenger.send("addterrain", [filepath])
	
