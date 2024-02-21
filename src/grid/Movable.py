from abc import ABC, abstractmethod
from webbrowser import get

#panda imports
from panda3d.core import NodePath

#lucrezia imports
from grid.GameEntity import GameEntity

class Movable(ABC):
    """
    Defines a Movable interface / class used to give a class the ability to be manually moved across the grid via different devices

    If set to be a GameEntity instance, tries to set to the GameEntity.getNode() node
    """

    def setMovableNode(self, node):
        self.movableNode = node

        if isinstance(self.movableNode, GameEntity):
            if self.autoSetMovableNodePath():
                if debug:
                    print("Movable: auto setting movable node to be: " + str(self.movableNode) + "...")
                return True
    
    def isSetMovableNode(self):
        return hasattr(self, 'movableNode') and self.movableNode != None
    
    def autoSetMovableNode(self):
        """
        Attempt to set automatically the node attribute (if present) as the movable node (if not already set).

        Sets self as the movable path is self is GameEntity and is guaranteed to have getNode(), then tries to set the movable node from the getNode() method. Uses autoSetMovableNodePath as helper.

        Returns:
            bool: True if the node was set, False otherwise
        """

        if not self.isSetMovableNode():
            self.setMovableNode(self)
            
        return False
    
    def autoSetMovableNodePath(self):
        # if type of self.movablenode is not NodePath 
        if not isinstance(self.movableNode, NodePath) and isinstance(self.movableNode, GameEntity):
            if isinstance(self.movableNode.getNode(), NodePath):
                # if debug is True
                if debug:
                    print("Movable: auto setting movable node to be: " + str(self.movableNode) + "...")
                # set self.movableNode to self.node
                self.setMovableNode(self.movableNode.getNode())
                return True
        return False

    @abstractmethod
    def setMovable(self, value, speed = 0.1):
        pass

    @abstractmethod
    def startMoveUp(self):
        pass

    @abstractmethod
    def startMoveDown(self):
        pass

    @abstractmethod
    def startMoveLeft(self):
        pass

    @abstractmethod
    def startMoveRight(self):
        pass
    
    @abstractmethod
    def stopMoveUp(self):
        pass

    @abstractmethod
    def stopMoveDown(self):
        pass

    @abstractmethod
    def stopMoveLeft(self):
        pass

    @abstractmethod
    def stopMoveRight(self):
        pass