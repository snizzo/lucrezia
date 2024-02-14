"""
LoadPoints are used to load the grid in chunks as the player moves around the world.
Created by GridManager and provided to current loaded grids.
"""

from panda3d.core import NodePath, Point3

#lucrezia imports
from geometries.PrimitiveSphere import PrimitiveSphere
from geometries.ColorCodes import ColorCodes

from grid.Placeholder import Placeholder


class LoadPoint:
    def __init__(self, parent = None, name = "unknown", position = Point3(0,0,0), radius = 5) -> None:
        """
        Args:
            name (str, optional): the name of the loadpoint. Defaults to "unknown".
            position (Point3, optional): the position of the loadpoint. Defaults to Point3(0,0,0).
            radius (int, optional): the radius of the loadpoint implemented as a cube, not as a circumference. Defaults to 5.
        """
        self.node = None

        # visible means the point has a visible position model attached to it
        self.visible = False

        #sets also nodepath name
        self.setName(name)
        self.setPosition(position)
        self.setRadius(radius)

        if parent != None:
            self.attachTo(parent)
    
    def setName(self, name) -> None:
        self.name = "loadpoint-" + name

        if self.node == None:
            self.node = NodePath(self.name)
        else:
            self.node.setName(self.name)

    def getName(self) -> str:
        return self.name

    # TODO: duplicate code of attachTo
    #       here for compatibility reason
    def reparentTo(self, parent) -> None:
        self.attachTo(parent)

    def attachTo(self, parent) -> None:
        self.node.reparentTo(parent)
    
    def detach(self) -> None:
        self.node.detachNode()
    
    # function isInRange return boolean
    def isInRange(self, position) -> bool:
        """
        Checks if the given position is in range of the loadpoint.

        Args:
            position (Point3): the position to check
        """
        if position.getX() >= self.node.getX() - self.radius and position.getX() <= self.node.getX() + self.radius:
            if position.getY() >= self.node.getY() - self.radius and position.getY() <= self.node.getY() + self.radius:
                return True
        return False
    
    def getNode(self) -> NodePath:
        '''
        Get a reference to the current nodepath
        '''
        return self.node

    def move(self, position) -> None:
        self.node.setPos(self.node, position)

    def getPosition(self, relativeto=None) -> Point3:
        if relativeto != None:
            return self.node.getPos(relativeto)
        else:
            return self.node.getPos()

    def setPosition(self, position) -> None:
        self.node.setPos(position)
    
    def setRadius(self, radius) -> None:
        #if is float
        if isinstance(radius, float):
            #round to integer
            radius = int(radius)
        self.radius = radius

    # TODO: duplicate code of getPos
    def getPosition(self) -> tuple:
        return self.node.getPos()
    
    # TODO: duplicate code of getPosition
    def getPos(self) -> tuple:
        return self.node.getPos()

    def getRadius(self) -> int:
        return self.radius

    def setVisible(self, visible = False) -> None:
        self.visible = visible
        if visible == True:
            self.placeholder = Placeholder(self.node, 0.2)
    
