"""
GridData holds .map data into a matrix and feeds the requested data to the Grid that holds it.

Used heavily into dynamic loading of Grids.
"""

#panda3d
import string
from panda3d.core import Point3

#standard python
from xml.dom import minidom
from xml.dom import Node
from utils.once import Once
import os, copy

from grid.GridDataBlock import GridDataBlock
from grid.Placeholder import Placeholder

class GridData:
    def __init__(self, mapFile = None) -> None:
        if debug and mapFile != None:
            print("GridData: loading map file: " + mapFile)
        
        self.attributes = {}     #attributes of the map such as cameraDistance, tilesize etc...
        self.data = []           #tiles, meshes, map data as (GridDataBlock)s

        

        #describing the max size of the grid horizontally and vertically
        self.sizeX = 0
        self.sizeY = 0

        self.loadedMatrix = [] #latest generated load matrix
        self.loadedNodes = [] #latest generated load nodes, used to unload the grid correctly
        self.defaultZeroMatrix = [] #default matrix of zeros
        """
        loadedMatrix uses a different code to describe the map from loadMatrix and unloadMatrix
        """

        if mapFile != None:
            correctFile = GridData.resolvePath(mapFile)
            self.loadData(correctFile)
            self.loadedMatrix = self.generateZeroMatrix()
            self.defaultZeroMatrix = self.generateZeroMatrix()
        else:
            print("WARNING: no map file specified, creating empty GridData")
        

    def getAttributes(self) -> dict:
        return self.attributes
    
    def getSizeX(self) -> int:
        return self.sizeX
    
    def getSizeY(self) -> int:
        return self.sizeY

    def getData(self, position) -> list:

        #if is type Point3
        if isinstance(position, Point3):
            return self.data[int(position.getX())][int(position.getY())]
        #if is type tuple
        elif isinstance(position, tuple):
            return self.data[position[0]][position[1]]
        else:
            print("WARNING: getData() called with wrong type: " + str(type(position)))
            return None

    def printDebugData(self) -> None:
        for row in self.data:
            print("[")
            for datablocklist in row:
                print("\t[")
                for datablock in datablocklist:
                    print("\t\t", datablock.getType(), "[", datablock.getAttributes(), "]")
            print("]")
    
    def generateZeroMatrix(self) -> list:
        newMatrix = [[0] * self.getSizeX() for _ in range(self.getSizeY())]
        return newMatrix

    def generateLoadedMatrix(self, loadPoints: list, mapOffset: Point3 = Point3(0,0,0)) -> list:
        """
        Generates a matrix of 1s and 0s where 1 means that the cell is loaded and 0 means that the cell is not loaded
        mapOffset is used to offset the map from the origin, necessary to calculate correct positions
        """

        print("Generating loaded matrix with offset: ", mapOffset)

        xOffset = int(mapOffset.getX())
        yOffset = int(mapOffset.getY())

        print("xOffset: ", xOffset)
        print("yOffset: ", yOffset)

        newLoadedMatrix = self.generateZeroMatrix() #temporary matrix that will overwrite self.loadMatrix
        GridData.debugPrintMatrix(newLoadedMatrix, "step 1 zeroMatrix")

        # this is the crucial check made between loadpoint and grid positions
        #generate new loaded matrix
        for loadPoint in loadPoints:
            for x in range(0,self.getSizeY()):
                for y in range(0, self.getSizeX()):
                    
                    #trying to normalize the grid check to the absolute position provided by the loadpoint
                    if loadPoint.isInRange(Point3(x+xOffset,y+yOffset,0)):
                        newLoadedMatrix[x][y] = 1

        GridData.debugPrintMatrix(newLoadedMatrix, "step 2 checked")

        #newLoadedMatrix = newLoadedMatrix[::-1] #reverse matrix to match panda3d coords

        GridData.debugPrintMatrix(newLoadedMatrix, "step 3 reversed")

        return newLoadedMatrix

    @staticmethod
    def fromGraphToMatrixCoords(self, x, y):
        return [x , self.getSizeY()-y]

    def generateLoadMatrix(self, oldMatrix, newMatrix) -> list:
        """
        LoadMatrix has 1 where the cell has to be loaded, 0 otherwise

        This is a comparison between the old and the new matrix, therefore there's no need to check for offset position
        """
        loadMatrix = self.generateZeroMatrix()
        for y in range(0,self.getSizeY()):
            for x in range(0, self.getSizeX()):
                if oldMatrix[y][x] == 0 and newMatrix[y][x] == 1:
                    loadMatrix[y][x] = 1
        return loadMatrix
    
    def generateUnloadMatrix(self, oldMatrix, newMatrix) -> list:
        """
        UnloadMatrix has 1 where the cell has to be unloaded, 0 otherwise
        """
        unloadMatrix = self.generateZeroMatrix()
        for y in range(0,self.getSizeY()):
            for x in range(0, self.getSizeX()):
                if oldMatrix[y][x] == 1 and newMatrix[y][x] == 0:
                    unloadMatrix[y][x] = 1
        return unloadMatrix

    def generateChangeMatrixFromLoadPoints(self, loadPoints: list, mapOffset: Point3 = Point3(0,0,0)) -> list:
        """
        Args:
            loadPoints (list): the list of loadpoints to generate the change matrix from
            mapOffset (Point3, optional): the offset of the map from the origin. Defaults to Point3(0,0,0).

        Returns:
            list: [loadMatrix, unloadMatrix]
            
        loadMatrix has 1 where the cell has to be loaded, 0 otherwise
        unloadMatrix has 1 where the cell has to be unloaded, 0 otherwise
        """

        #generate new matrices comparing them to the old ones
        newLoadedMatrix = self.generateLoadedMatrix(loadPoints, mapOffset)
        loadMatrix = self.generateLoadMatrix(self.loadedMatrix, newLoadedMatrix)
        unloadMatrix = self.generateUnloadMatrix(self.loadedMatrix, newLoadedMatrix)

        GridData.debugPrintMatrix(newLoadedMatrix, "newLoadedMatrix")
        GridData.debugPrintMatrix(loadMatrix, "loadMatrix")
        GridData.debugPrintMatrix(unloadMatrix, "unloadMatrix")

        #update newloadedmatrix now becomes loadedmatrix
        #and represents loaded cells
        self.loadedMatrix = newLoadedMatrix

        #GridData.debugPrintMatrix(newLoadedMatrix)

        return [loadMatrix, unloadMatrix]

    @staticmethod
    def debugPrintMatrix(matrix: list, name: string = "unknown") -> None:
        print("Printing matrix: " + name)
        for row in matrix:
            print(row)

    @staticmethod
    def rotateMatrix(matrix):
        # Use zip() with argument unpacking (*) to transpose the matrix
        transposed = list(zip(*matrix))

        # Reverse each row in the transposed matrix to rotate it clockwise
        rotated = [row[::-1] for row in transposed]

        return rotated

    def loadData(self, mapFile) -> None:
        if debug:
            print("GridData: loading map file: " + mapFile)
        
        xmldoc = minidom.parse(mapFile)
        
        data = xmldoc.getElementsByTagName('data')
        for d in data:
            if len(d.attributes) > 0:
                self.attributes = d.attributes
        
        rowsdata = xmldoc.getElementsByTagName('row')
        
        currentx = 0
        currenty = 0
        
        for row in rowsdata:                            #for every row
            self.data.append([])
            for tile in row.childNodes:                 #for every tile
                if tile.nodeType == Node.ELEMENT_NODE:  #if child is tile
                    
                    o = Once() #lo switch viene fatto solo in presenza di una texture 'ground'

                    d = None
                    
                    subdata = []

                    for res in tile.childNodes:
                        if res.nodeType == Node.ELEMENT_NODE: # adding resources to tile
                            if res.nodeName == 'ground':
                                d = GridDataBlock('ground', res.attributes)
                                subdata.append(d)
                                if o.get():
                                    self.data[currenty].append(subdata)
                                    currentx += 1
                            elif res.nodeName == 'object':
                                d = GridDataBlock('object', res.attributes)
                                subdata.append(d)
                            elif res.nodeName == 'grass':
                                d = GridDataBlock('grass', res.attributes)
                                subdata.append(d)
                            elif res.nodeName == 'light':
                                d = GridDataBlock('light', res.attributes)
                                subdata.append(d)
                            elif res.nodeName == 'scrollable':
                                pass #TODO: deprecated?
                            elif res.nodeName == 'character':
                                d = GridDataBlock('character', res.attributes)
                                subdata.append(d)
            self.sizeX = currentx
            currentx = 0
            currenty += 1
            self.sizeY = currenty
        
        #self.data = GridData.rotateMatrix(self.data) #reverse matrix to match panda3d coords

    @staticmethod
    def resolvePath(file):
        if not os.path.isfile(file):
            print("WARNING: can't find map file, attempting resource parsing: "+file)

            if os.path.isfile(resourceManager.getResource('Mappe/'+file)):
                file = resourceManager.getResource('Mappe/'+file)
            else:
                print("ERROR: can't find map file (resourced): "+file)
        
        return file

