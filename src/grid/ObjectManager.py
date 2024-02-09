'''
Manages all random objects spawned in the game scene that aren't tied to a Grid

Subclass of EntityManager
'''

from grid.EntityManager import EntityManager
from grid.grid import Grid

class ObjectManager(EntityManager):
    def __init__(self) -> None:
        EntityManager.__init__(self)
    
    def add(self, file="", name=""):
        """
        Name of the resource to load the object from
        """