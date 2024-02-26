#panda3d
from panda3d.core import NodePath, LPoint2i, Point3
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.LerpInterval import LerpPosInterval
from direct.task import Task

#standard python
from xml.dom import minidom
from xml.dom import Node

#internals
from utils.toggle import Toggle
from utils.once import Once
from objects.grass import Grass
from objects.light import Light
from grid.grid import Grid
from grid.tile import Tile
from grid.character import Character
from grid.Entity import Entity
from grid.GridData import GridData
from grid.Placeholder import Placeholder

from utils.fadeout import FadeOut

import os, sys

'''
This class abstracts the 2D grid commonly used in 2D games
to use with panda3d.

INTERNAL TILESET EXAMPLE GRAPH:
  ^
  |
  |
y |
  |
  |
  O------------>
        x

Grid represents a single map entity composed of tiles, objects and other information regarding weather, load and unload scripting.

LOADING GRID (NEW DYNAMIC METHOD):
setDynamicLoading()      -> used to enable dynamic loading
dynamicLoadMap()         -> asks GridData for load / unload matrices (using loadpoints) and asks dynamicLoadUpdate() to load / unload the map
dynamicLoadUpdate()      -> loads / unloads the map based on the matrices
'''
class DynamicGrid(Grid):
    """
    Entity
      ^
      |
    Grid
      ^
      |
    DynamicGrid
    """

    def __init__(self, mapFile = None, currentGridName=""):
        """
        name = ""
        Descriptive name of the map, used within scripting engine

        mapFile = None
        Name of the map file to load
        """

        #making it an Entity
        Entity.__init__(self)
        Grid.__init__(self, mapFile, currentGridName)

        #uncomment to enable dynamic loading by default
        #self.setDynamicLoading(True)
    
    def setDynamicLoadingDelay(self, value):
        """
        Sets the delay in seconds between loadmatrix refreshes

        Arguments: 
            value: True or False
        """
        self.dynamicLoadingDelay = value
    
    def getDynamicLoadingDelay(self):
        return self.dynamicLoadingDelay
    
    def setDynamicLoading(self, dynamic):
        """
        Arguments:
            dynamic: True to enable dynamic loading, False to disable it
        """


        # works only as a status change, if status is the same, do nothing
        if dynamic == self.getDynamicLoading():
            return

        if self.mapFile == None:
            print("WARNING: map file not set, can't enable dynamic loading")
            return

        print("WARNING: setting dynamic loading to "+str(dynamic)+"...")
        self.dynamicLoading = dynamic

        #loading preloaded attributes from map file
        self.loadAttributes(self.gridData.getAttributes())

        if self.dynamicLoading == True:
            taskMgr.doMethodLater(self.getDynamicLoadingDelay(), self.dynamicLoadMap, str(self.getEntityName())+"-dynamicLoadTask")
            
    
    def getDynamicLoading(self):
        """
        Returns:
            True if dynamic loading is enabled, False otherwise
        """
        return self.dynamicLoading

    def dynamicLoadMap(self, task):
        """
        Load / unload map dynamically based on LoadPoints
        """
        
        if debug:
            print("list of loadpoints:")
            for p in self.loadPoints:
                print(p.getPosition())
        
        updatedMatrixes = self.gridData.generateChangeMatrixFromLoadPoints(self.loadPoints, self.getPos())
        loadMatrix = updatedMatrixes[0]
        unloadMatrix = updatedMatrixes[1]

        # set load / unload matrix from GridData
        self.dynamicLoadUpdate(loadMatrix, unloadMatrix)
        
        return Task.again
    
    def dynamicLoadUpdate(self, loadMatrix, unloadMatrix):
        """
        Update map dynamically based on matrices
        """

        #load new tiles from loadMatrix
        for y in range(0, self.gridData.getSizeY()):
            for x in range(0, self.gridData.getSizeX()):
                if loadMatrix[y][x] == 1:
                    self.loadTile(x, y)
        
        #unload tiles from unloadMatrix
        for y in range(0, self.gridData.getSizeY()):
            for x in range(0, self.gridData.getSizeX()):
                if unloadMatrix[y][x] == 1:
                    self.unloadTile(x, y)
