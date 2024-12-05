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

Used as a superclass for StaticGrid and DynamicGrid
'''
class Grid(Entity):

    def __init__(self, mapFile = None, currentGridName=""):
        """
        name = ""
        Descriptive name of the map, used within scripting engine

        mapFile = None
        Name of the map file to load
        """

        #making it an Entity
        Entity.__init__(self)

        #variables initialization
        self.tileset = []
        self.characterset = []
        self.scrollableset = [] #FIXME: scrollables can't definitely sit here...
        
        #only used in editor as for now, contains just mapname
        self.currentGridNameEditor = ''
        self.currentGridName = ''
        self.currentMapPath = ''
        self.mapFile = mapFile

        #main nodes
        self.node = render.attachNewNode("tileset")
        self.grassnode = render.attachNewNode("grassnodes")
        self.bgImage = None
        
        #default value, just for fun
        self.tileDimension = 128.0
        self.showCollisions = False
        self.stashed = False
        #automatic methods
        #self.mergeMeshes()
        self.unloadScript = False
        self.loadScript = False

        #setting default name if map is empty
        if mapFile != None and not currentGridName:
            print("setting grid name to " + mapFile)
            self.setEntityName(mapFile)
        else:
            self.setEntityName(currentGridName)
        
        # TODO: remove, deprecated
        #self.acceptOnce("changeMap", self.changeMap)

        #loading grid data
        # TODO: port static load code to new GridData class?
        if mapFile != None:
            self.gridData = GridData(mapFile)
        else:
            self.gridData = GridData()

        #dynamic loading
        self.dynamicLoading = False  # enables dynamic loading
        self.loadPoints = []         # points where to load the map
        self.dynamicLoadingDelay = 0.5  # wait time between dynamic loading

        self.ph = Placeholder()
        self.ph.setParent(self.node)
    
    def disablePlayable(self):
        if self.getPlayable() != None:
            messenger.send("pauseGameplay")
    
    #APICALL
    def getObjectsById(self, search):
        l = self.node.findAllMatches("**/=id="+search)
        s = []
        for e in l:
            s.append(e.getPythonTag("gamenode"))
        return s
    
    #APICALL
    def getObjectById(self, search):
        s = None
        l = self.node.findAllMatches("**/=id="+search)
        if len(l) > 0:
            s = l[0].getPythonTag("gamenode")
        if s != None:
            return s
        else:
            print("ERROR: getObjecyById("+search+") -- can't find any object with id: "+search)
            sys.exit()
    
    def getPlayable(self):
        '''
        Returns: 
            the playable object of the game if any,
            else None
        '''
        value = self.node.find("**/=playable=true").getPythonTag("gamenode")

        return None if value == None else value
    
    '''
    @return script to be executed when map is loaded
    '''
    def getOnLoad(self):
        if self.loadScript == False:
            return ''
        return self.loadScript
    
    '''
    @param script value of script to be executed when opening map
    '''
    def setOnLoad(self, script):
        self.loadScript = script

    '''
    @return script to be executed when map is unloaded
    '''
    def getOnUnload(self):
        if self.unloadScript == False:
            return ''
        return self.unloadScript
    
    '''
    @param script to be executed when map is unloaded
    '''
    def setOnUnload(self, script):
        self.unloadScript = script
    
    def getCurrentGridNameEditor(self):
        """
        Returns:
            name of the current grid in editor.
            This name has its own internal logic and is binded to editor gui generation and behaviour
        """
        return self.currentGridNameEditor
    
    def setCurrentGridNameEditor(self, name):
        """
        Arguments:
            sets name of the current grid in editor.
            This name has its own internal logic and is binded to editor gui generation and behaviour
        """
        self.currentGridNameEditor = name

    def getBackgroundImage(self):
        return self.bgImage
    
    def getSizeX(self):
        return self.gridData.getSizeX()
    
    def getSizeY(self):
        return self.gridData.getSizeY()
    
    '''
    Real time map modifiers
    TODO: implement this
    '''
    def addRow(self, currentx, currenty):
        pass
    
    def addColumn(self):
        pass
    
    def setHpr(self, vector: Point3, relativeto: NodePath = None):
        """
        Arguments:
            vector: rotation vector
            relativeto: NodePath to get the rotation relative to, if None rotation is relative to itself
        """
        if relativeto == None:
            self.node.setHpr(vector)
        else:
            self.node.setHpr(relativeto, vector)
    
    def getHpr(self, relativeto: NodePath = None):
        """
        Arguments:
            relativeto: NodePath to get the rotation relative to, if None rotation is relative to itself

        Returns:
            node rotation: relative to itself if no argument is passed
        """
        if relativeto == None:
            return self.node.getHpr()
        else:
            return self.node.getHpr(relativeto)

    def setPos(self, vector: Point3, relativeto: NodePath = None):
        """
        #should always be relative to render because usually grid's internal self.node is always a child of render
        #but nothing except implicit code strucutre is enforcing this rule

        #TODO: explicitely enforce render?
        """

        if relativeto == None:
            self.node.setPos(vector)
        else:
            self.node.setPos(relativeto, vector)
    
    def getPos(self):
        """
        Returns:
            position: always relative to render
        """
        return self.node.getPos(render)

    def move(self, vector: Point3):
        self.node.setPos(self.node, vector)

    def getNode(self):
        """
        Returns:
            internal panda NodePath holding all grid subnodes
        """
        return self.node

    def stash(self):
        """
        Remove grid from the scene graph, making it invisible and not checkying for collisions. Will still accept events.
        """
        self.node.stash()
        self.setStashed(True)
    
    def unstash(self):
        """
        Insert grid into the scene graph, making it visible and checking for collisions.
        Have to be called after stash().
        """
        self.node.unstash()
        self.setStashed(False)
    
    def setStashed(self, stashed):
        """
        Arguments:
            stashed: True to stash the grid, False to unstash it
        """
        self.stashed = stashed
    
    def toggleStash(self):
        """
        Toggle grid stashed state
        """
        if self.isStashed():
            self.unstash()
        else:
            self.stash()

    def isStashed(self):
        """
        Returns:
            True if grid is stashed, False otherwise
        """
        return self.stashed

    def loadTile(self, x, y):
        t = Tile(self.tileDimension)
        t.setX(x)
        t.setY(y)
        
        #appending to grid internal tileset
        self.tileset.append(t)
        
        o = Once() #lo switch viene fatto solo in presenza di una texture 'ground'
        
        # load resource from data
        for res in self.gridData.getData((y, x)):
            type = res.getType()
            attributes = res.getAttributes()

            if type == 'ground':
                t.addTexture(attributes)
            elif type == 'object':
                t.addObject(attributes)
            elif type == 'grass':
                g = Grass(attributes, self.tileDimension) #creating object
                t.addCustomObject(g) #setting coordinates of tile
                g.getNode().wrtReparentTo(self.grassnode)
            elif type == 'light':
                t.addLight(attributes)
            elif type == 'scrollable':
                c = Scrollable(attributes['url'].value, attributes['inclination'].value, self.tileDimension)
                c.setX(x)
                c.setY(y)
                self.scrollableset.append(c)
            elif type == 'character':
                t.addCharacter(attributes, self.showCollisions, Point3(x,y,0))
                
        t.node.reparentTo(self.node)
    
    def unloadTile(self, x, y):
        t = self.getTile(x, y)
        t.destroy()
        self.tileset.remove(t)

    def loadAttributes(self, attributes):
        if 'tilesize' in attributes:
            self.tileDimension = float(attributes['tilesize'].value)
        else:
            self.tileDimension = 32.0
        if 'showcollisions' in attributes:
            if attributes['showcollisions'].value == 'false':
                self.showCollisions = False
            else:
                self.showCollisions = True
        else:
            self.showCollisions = False
        if 'onLoad' in attributes:
            self.loadScript = attributes['onLoad'].value
        else:
            self.loadScript = False
            
        if 'onUnload' in attributes:
            self.unloadScript = attributes['onUnload'].value
        else:
            self.unloadScript = False

        # kept here for static loading compatibility
        if self.getDynamicLoading() == False:
            if 'camdistance' in attributes:
                customCamera.setDistance(float(attributes['camdistance'].value))
            else:
                customCamera.setDistance(15)
            if 'bgImage' in attributes:
                self.setBackgroundImage(attributes['bgImage'].value)
            else:
                customCamera.setDistance(15)

    def loadDataBlock(self, dataBlock):
        pass

    '''
    @return string current map filepath
    '''
    def getCurrentMapPath(self):
        return self.currentMapPath
    
    '''
    @return list of all tiles
    '''
    def getAllTiles(self):
        return self.tileset
    
    '''
    Used to get Tile object from coordinates.
    Very slow, linear, improvable.
    Used only in editor mode.

    This may no more be the case.
    TODO: improve this to constant time

    @return Tile instance or -1 if tile is not found
    '''
    def getTile(self, x, y):
        for t in self.tileset:
            if t.getX() == x and t.getY() == y:
                return t
        
        return -1
    
    def setLoadPoints(self, lp):
        self.loadPoints = lp
    
    '''
    Use this function with caution. Can cause artifacts or crash bugs.
    Don't ever use if not strictly needed.
    
    Can solve slowness if big grid is shown. Best use for static images grid.
    '''
    def mergeMeshes(self):
        self.node.flattenStrong()
    
    '''
    Debug method that prints tileset in human-readable form
    '''
    def printTileset(self):
        for i in range(len(self.tileset)):
            print(self.tileset[i])
    
    '''
    Debug method used to verify correct memory instantiation
    '''
    def ping(self):
        print("GRID: pong!")
