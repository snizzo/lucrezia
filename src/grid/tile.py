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
        #public props
        self.walkable = True
        self.resources = []
        
        #inner props
        self.geometry = 0
        self.node = 0
        
        #quads
        self.cm = CardMaker("tilebgcolor")
        self.cm.setFrame(-0.5,0.5,-0.5,0.5) #this make a 1x1 quad
    
    #this oen adds static resource
    def addResource(self, name):
        pass
    
    def setX(self, x):
        if self.node != 0:
            self.node.setX(x)
            
    def setY(self, y):
        if self.node != 0:
            self.node.setZ(y)
    
    def setBackgroundColor(self, r, g, b, a):
        cm.setColor(r, g, b, a)
        
    def setTexture(self, name):
        tex = loader.loadTexture('../res/'+name+'.png')
        self.node.setTexture(tex)
    
    def generate(self):
        self.geometry = self.cm.generate()
        self.node = NodePath(self.geometry)
        self.node.setTwoSided(True)