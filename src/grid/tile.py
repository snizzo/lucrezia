from pandac.PandaModules import CardMaker
from panda3d.core import NodePath

'''
TILE CLASS

Tile class is used to represent a tile in the 2d simulated
world. This will take care of anything from flags to textures to 
geometries attached to it. Please reference to this instead of the
direct geometry in other parts of code.
'''
class Tile:
	
	def __init__(self):
		self.geometry = 0
		self.node = 0
	
	def setX(self, x):
		if self.node != 0:
			self.node.setX(x)
		
	def setY(self, y):
		if self.node != 0:
			self.node.setZ(y)
	
	def setBackgroundColor(self, r, g, b, a):
		cm = CardMaker("tilebgcolor")
		cm.setFrame(-0.5,0.5,-0.5,0.5) #this make a 1x1 quad
		cm.setColor(r, g, b, a)
		
		self.geometry = cm.generate()
		self.node = NodePath(self.geometry)
