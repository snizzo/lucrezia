"""
GridData holds .map data into a matrix and feeds the requested data to the Grid that holds it.

Used heavily into dynamic loading of Grids.
"""

#panda3d
from panda3d.core import Point3

#standard python
from xml.dom import minidom
from xml.dom import Node
from utils.once import Once
import os

from grid.GridDataBlock import GridDataBlock

class GridData:
    def __init__(self, mapFile) -> None:
        if debug:
            print("GridData: loading map file: " + mapFile)
        
        self.attributes = {}
        self.data = []

        correctFile = GridData.resolvePath(mapFile)
        self.loadData(correctFile)
        #self.printDebugData()

        print(self.getData(Point3(1,1,0)))

    def getAttributes(self) -> dict:
        return self.attributes
    
    def getData(self, position: Point3) -> list:
        return self.data[int(position.getX())][int(position.getY())]

    def printDebugData(self) -> None:
        for row in self.data:
            print("[")
            for datablocklist in row:
                print("\t[")
                for datablock in datablocklist:
                    print("\t\t", datablock.getType(), "[", datablock.getAttributes(), "]")
            print("]")

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
                            
            currentx = 0
            currenty += 1

    @staticmethod
    def resolvePath(file):
        if not os.path.isfile(file):
            print("WARNING: can't find map file, attempting resource parsing: "+file)

            if os.path.isfile(resourceManager.getResource('Mappe/'+file)):
                file = resourceManager.getResource('Mappe/'+file)
            else:
                print("ERROR: can't find map file (resourced): "+file)
        
        return file

