'''
Handles multiple grids around the 3D world

Subclass of EntityManager
'''

from grid.EntityManager import EntityManager
from grid.grid import Grid

class GridManager(EntityManager):
    def __init__(self) -> None:
        EntityManager.__init__(self)

    def add(self, file="", name="") -> int:
        newgrid = Grid(file, name)
        newgrid.loadMap()
        newgrid.changedMap()

        self.append(newgrid)

        return self.last()
