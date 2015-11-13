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
		self.tree.clear()
	
	def generate(self):
		
		#adding root scene node
		nn = QTreeWidgetItem()
		nn.setText(0,QString("mainScene"))
		self.tree.addTopLevelItem(nn)
		
		self.parent = nn
		self.browse(self.rootNode)
	
	#
	# recursive function that fills the scene node
	# no more limited at .egg structures
	#
	def browse(self,node):
		for child in node.getChildren():
			
			#adding root scene node
			nn = QTreeWidgetItem(self.parent)
			nn.setText(0,QString(child.getName()))
			
			lastParent = self.parent
			
			self.parent = nn
			# 
			# checking file extension in order to go to deeper than egg model structure
			# 
			if Utilities.hasFileExtension(child.getName()) != "egg":
				self.browse(child)
			
			self.parent = lastParent
