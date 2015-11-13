from direct.showbase.DirectObject import DirectObject
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

class PropertiesTable(DirectObject):
	def __init__(self, table):
		self.table = table
		
		self.currentSelection = []
		
		self.accept("selected one", self.oneobj)
		self.accept("selected none", self.noneobj)
		
		self.table.cellChanged.connect(self.cellChanged)
	
	def oneobj(self, obj):
		self.clearTable()
		
		#adding properties
		for key, value in obj.getPropertyList().iteritems():
			self.addPropertyRow(key, value)
		
		#storing temporary selection in a cleared list
		self.currentSelection.append(obj)
	
	def manyobj(self, object_list):
		pass
	
	def noneobj(self):
		self.clearTable()
		
	def cellChanged(self, row, column):
		if len(self.currentSelection)>0: #if something is selected, else is bogus
			
			key = self.table.item(row,0).text().__str__()
			value = self.table.item(row,1).text().__str__()
		
			self.currentSelection[0].setProperty(key,value)
		
			#reload everything
			self.oneobj(self.currentSelection[0])
			messenger.send("refresh scenetree")
	
	def addPropertyRow(self, label, value):
		#resizing table size
		self.table.setRowCount(self.table.rowCount()+1)
		self.table.setColumnCount(2)
		
		#creating items
		namelabel = QTableWidgetItem(label)
		valuelabel = QTableWidgetItem(value)
		
		#attaching items to correct position
		self.table.setItem(self.table.rowCount()-1,0, namelabel)
		self.table.setItem(self.table.rowCount()-1,1, valuelabel)
		
	def clearTable(self):
		self.currentSelection = [] #clearing selection list
		self.table.clear()
		
		#clearing rows and columns
		self.table.setRowCount(0)
		self.table.setColumnCount(0)
