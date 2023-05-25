'''
Handles multiple grids around the 3D world
'''

from grid.grid import Grid

class GridManager:
    def __init__(self) -> None:
        self.grids = []

    def addGrid(self, file="", name="") -> int:
        newgrid = Grid(file, name)
        newgrid.loadMap()
        newgrid.changedMap()

        self.grids.append(newgrid)

        return len(self.grids) - 1
    
    def getAllLoadedGridsKeys(self) -> list:
        return [grid.getCurrentGridName() for grid in self.grids]

    def getGrid(self, key) -> Grid:
        #if is a string
        if isinstance(key, str):
            for grid in self.grids:
                if grid.getCurrentGridName() == key:
                    return grid
        
        if isinstance(key, int):
            return self.grids[key]
    

