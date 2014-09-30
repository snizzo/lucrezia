from tile import Tile

'''
This class abstracts the 2D grid commoly used in 2D games
to use with panda3d.

INTERNAL TILESET EXAMPLE GRAPH:
       y
  O------------>
  |
x |
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
		
		#automatic methods
		self.generateEmptyTileset(6,4)
		self.printTileset() # TODO: deleteme
	
	'''
	This method generates an internal tileset.
	Seen with list of lists (multidim array)
	'''
	def generateEmptyTileset(self, x, y):
		for i in range(x):
			l = []
			for j in range(y):
				t = Tile()
				l.append(t)
			self.tileset.append(l)
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
