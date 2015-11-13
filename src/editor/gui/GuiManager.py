from direct.showbase.DirectObject import DirectObject

class GuiManager(DirectObject):
 
	def __init__(self):
		pass
	
	'''
	Simply telling GUI selection has changed and sending pointers to delegates.
	'''
	def noneObjSelected(self):
		messenger.send("selected none")
	
	def oneObjSelected(self, obj):
		messenger.send("selected one", [obj])
		
	def manyObjSelected(self,objlist):
		messenger.send("selected many", objlist)
