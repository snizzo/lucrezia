from abc import ABC, abstractmethod

class Movable(ABC):
    """
    Defines a Movable interface / class used to give a class the ability to be manually moved across the grid via different devices
    """

    def setMovableNode(self, node):
        self.movableNode = node
    
    def isSetMovableNode(self):
        return hasattr(self, 'movableNode') and self.movableNode != None
    
    def autoSetMovableNode(self):
        """
        Attempt to set automatically the node attribute (if present) as the movable node (if not already set)

        Returns:
            bool: True if the node was set, False otherwise
        """

        if not self.isSetMovableNode():
            if hasattr(self, 'node'):
                if debug:
                    print("Movable: auto setting movable node to be: " + str(self.node) + "...")
                self.setMovableNode(self.node)
                return True

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