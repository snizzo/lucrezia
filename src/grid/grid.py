from panda3d.core import NodePath

from utils.toggle import Toggle
from tile import Tile

'''
This class abstracts the 2D grid commoly used in 2D games
to use with panda3d.

INTERNAL TILESET EXAMPLE GRAPH:
       x
  O------------>
  |
y |
  |
  |
  v
'''
class Grid:
	
	'''
	Autogenerates empty tileset at start
	'''
	def __init__(self):
		#variables initialization
		self.tileset = []
		
		self.node = render.attachNewNode("tileset")
		
		#automatic methods
		self.generateEmptyTileset(20,20)
		self.mergeMeshes()
	
	'''
	This method generates an internal tileset.
	Seen with list of lists (multidim array)
	
	The tileset is automatically placed at (0,0,0) and coloured
	chess-style.
	'''
	def generateEmptyTileset(self, x, y):
		colorSwitch = Toggle(False)
		
		for i in range(x):
			l = []
			
			colorSwitch.toggle()
			
			for j in range(y):
				t = Tile()
				
				#color switcher
				if colorSwitch.get():
					t.setBackgroundColor(0.7,0.7,0.7,1)
				else:
					t.setBackgroundColor(0.3,0.3,0.3,1)
				colorSwitch.toggle()
				
				#setting right coordinates
				t.setX(i-(x/2))
				t.setY(j-(y/2))
				#reparenting to grid node
				t.node.reparentTo(self.node)
				
				#appending to list
				l.append(t)
				
				
			self.tileset.append(l)
	
	'''
	Use this function with caution. Can cause artifacts or crash bugs.
	Don't ever use if not strictly needed.
	
	Can solve slowness if big grid is shown. Best use for static images grid.
	'''
	def mergeMeshes(self):
		self.node.flattenStrong()
	
	'''
	Debug method that prints tileset in human-readable form
	'''
	def printTileset(self):
		for i in range(len(self.tileset)):
			print self.tileset[i]
	
	'''
	Debug method used to verify correct memory instantiation
	'''
	def ping(self):
		print "GRID: pong!"
