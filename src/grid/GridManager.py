'''
Handles multiple grids around the 3D world

Subclass of EntityManager
'''

from grid.EntityManager import EntityManager
from grid.grid import Grid

class GridManager(EntityManager):
    def __init__(self) -> None:
        EntityManager.__init__(self)

        #loadpoints
        self.loadPoints = []

    def add(self, file="", name="", method="static") -> int:
        """
        Args:
            file (str, optional): the file to load the grid from. Defaults to "".
            name (str, optional): the name of the grid. Defaults to "".
            method (str, optional): the method to load the grid. Defaults to "".

            method can be: "static" or "dynamic" where static is the default method used to load the whole grid at once
                            and dynamic is the method used to load the grid in chunks as the player moves around the world
        """
        newgrid = Grid(file, name)

        if method == "dynamic":
            self.loadDynamic(newgrid)
        elif method == "static":
            self.loadStatic(newgrid)
        else:
            print("WARNING: could not load grid with method: " + method + ", using static method")
            self.loadStatic(newgrid)

        self.append(newgrid)

        return self.last()

    def loadStatic(self, newgrid) -> None:
        newgrid.loadMap()
        newgrid.changedMap()
    
    def loadDynamic(self, newgrid) -> None:
        newgrid.setDynamicLoading(True)
        #refresh load points
        self.updateLoadPoints()
    
    def addLoadPoint(self, point):
        """
        Add a new loadpoint to the the pool
        Everytime a new LoadPoint is added, the loadpoints of every grid are updated

        Args:
            point (LoadPoint): the loadpoint to add
        """

        print("GridManager: adding load point to pool...")

        self.loadPoints.append(point)
        #refresh load points
        self.updateLoadPoints()
    
    def updateLoadPoints(self):
        for grid in self.getAllEntities():
            grid.setLoadPoints(self.loadPoints)

