"""
LoadPoints are used to load the grid in chunks as the player moves around the world.
Created by GridManager and provided to current loaded grids.
"""

from platform import node
from panda3d.core import NodePath, Point3, LVecBase3f

#lucrezia imports
from geometries.PrimitiveSphere import PrimitiveSphere
from geometries.ColorCodes import ColorCodes
from grid.GameEntity import GameEntity

from grid.Placeholder import Placeholder


class LoadPoint(GameEntity):
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
        # TODO: LoadPoint should have to be tied to grid tile's GameEntity restriction but breaks oop
        #GameEntity.reparentTo(self, parent)


        self.attachTo(parent)

    def attachTo(self, parent) -> None:
        self.node.reparentTo(parent)
    
    def detach(self) -> None:
        self.node.detachNode()
    
    # function isInRange return boolean
    def isInRange(self, position, relativeto = "render") -> bool:
        """
        Checks if the given position is in range of the loadpoint.

        Args:
            position (Point3): the position to check, relative to render
            relativeto (str, optional): specify if has to check position between relative or absolute positions, 
                                        "render" for absolute, "this" for relative.
                                        Defaults to "render".
        """

        if relativeto == "render":
            nodepos = self.node.getPos(render)
        elif relativeto == "this":
            nodepos = self.node.getPos()
        else:
            print("ERROR: LoadPoint::isInRange -> param relativeto is missing, can be \"render\" or \"this\"")
        
        if position.getZ() >= nodepos.getX() - self.radius and position.getZ() <= nodepos.getX() + self.radius:
            if position.getX() >= nodepos.getZ() - self.radius and position.getX() <= nodepos.getZ() + self.radius:
                return True
        return False

    def getNode(self) -> NodePath:
        '''
        Get a reference to the current nodepath
        '''
        return self.node

    def move(self, position) -> None:
        self.node.setPos(self.node, position)
    
    def setPos(self, relativeto, position:LVecBase3f=None) -> None:
        """
        setPos accepts both implicit and explicit relative position value

        Arguments:
            relativeto: can be Point3(), stating an implicit relative position to node's parent or NodePath, explicitely stating relative to
            position  : used to specity explicit relative position when relativeto is used
        
        """
        if isinstance(relativeto, LVecBase3f):
            self.node.setPos(relativeto)
        elif isinstance(relativeto, NodePath) and isinstance(position, LVecBase3f) and position != None:
            self.node.setPos(relativeto, position)

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

    def setVisible(self, visible = False, label=None) -> None:
        self.visible = visible
        if visible == True:
            self.placeholder = Placeholder(self.node, 0.2)
            self.placeholder.setLabel(label)
        else:
            if hasattr(self, 'placeholder') and isinstance(self.placeholder, Placeholder):
                self.placeholder.hide()
                self.placeholder.destroy()
                self.placeholder = None
    
    def isVisible(self) -> bool:
        return self.visible
    
