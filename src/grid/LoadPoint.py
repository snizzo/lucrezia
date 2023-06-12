"""
LoadPoints are used to load the grid in chunks as the player moves around the world.
Created by GridManager and provided to current loaded grids.
"""

from panda3d.core import NodePath, Point3

class LoadPoint:
    def __init__(self, name = "unknown", position = Point3(0,0,0), radius = 5) -> None:
        """
        Args:
            name (str, optional): the name of the loadpoint. Defaults to "unknown".
            position (Point3, optional): the position of the loadpoint. Defaults to Point3(0,0,0).
            radius (int, optional): the radius of the loadpoint implemented as a cube, not as a circumference. Defaults to 5.
        """
        self.node = None

        #sets also nodepath name
        self.setName(name)
        self.setPosition(position)
        self.setRadius(radius)
    
    def setName(self, name) -> None:
        self.name = "loadpoint-" + name

        if self.node == None:
            self.node = NodePath(self.name)
        else:
            self.node.setName(self.name)

    def getName(self) -> str:
        return self.name

    def attachTo(self, parent) -> None:
        self.node.reparentTo(parent)
    
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

    
    def setPosition(self, position) -> None:
        self.node.setPos(position)
    
    def setRadius(self, radius) -> None:
        #if is float
        if isinstance(radius, float):
            #round to integer
            radius = int(radius)
        self.radius = radius

    def getPosition(self) -> tuple:
        return self.node.getPos()
    
    def getRadius(self) -> int:
        return self.radius
    