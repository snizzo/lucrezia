
from panda3d.core import NodePath

from grid.Entity import Entity

class GameEntity:
    '''
    In order for a game entity to be valid should be set to a parent (doens't hold for LoadPoint)
    '''
    def __init__(self, parent):
        self.parent = parent
        self.node = None
    
    def getNode(self):
        return self.node
    
    def setNode(self, node: NodePath):
        self.node = node

    '''
    Automatically move the object to the near tile depending
    on the latest movement direction. Works only if target object has
    supports offset movement (horizontal and vertical).
    horizontal < -0.5 -> move left; horizontal > 0.5 move right
    vertical < -0.5 -> move down; vertical > 0.5 move up
    '''
    def updateTilePosition(self):
        needsmove = False
        if hasattr(self, "properties"):
            if "offsethorizontal" in self.properties:
                if self.properties['offsethorizontal'] < -0.5:
                    t = pGrid.getTile(self.parent.getX()-1, self.parent.getY())
                    needsmove = 'left'
                if self.properties['offsethorizontal'] > 0.5:
                    t = pGrid.getTile(self.parent.getX()+1, self.parent.getY())
                    needsmove = 'right'
            if "offsetvertical" in self.properties:
                if self.properties['offsetvertical'] < -0.5:
                    t = pGrid.getTile(self.parent.getX(), self.parent.getY()-1)
                    needsmove = 'down'
                if self.properties['offsetvertical'] > 0.5:
                    t = pGrid.getTile(self.parent.getX(), self.parent.getY()+1)
                    needsmove = 'up'
            
            #calling pGrid method
            if needsmove != False:
                #self.parent parent
                #self se stesso
                #t tile di arrivo
                if t != -1:
                    self.parent.removeObject(self)
                    t.addExistentObject(self)
                    if needsmove == 'left':
                        self.properties['offsethorizontal'] = self.properties['offsethorizontal']+1
                    if needsmove == 'right':
                        self.properties['offsethorizontal'] = 1-self.properties['offsethorizontal']
                    if needsmove == 'down':
                        self.properties['offsetvertical'] = self.properties['offsetvertical']+1
                    if needsmove == 'up':
                        self.properties['offsetvertical'] = 1-self.properties['offsetvertical']
                    self.generateNode()
    '''
    Reparent self to target tile
    @param tile that will become parent of self
    '''
    def reparentTo(self, tile):
        self.node.reparentTo(tile.getNode())
        self.parent = tile
