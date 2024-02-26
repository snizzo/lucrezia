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
This class represents a grid that is statically loaded (all at once).

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

LOADING GRID (OLD STATIC METHOD):
changeMap()       -> game engine api call that fades out calls changeMapHelper() and fades in
changeMapHelper() -> destroys every asset in the map and calls loadMap()
loadMap()         -> called to load a map
changedMap()      -> called to attach playable to camera and start gameplay
'''
class StaticGrid(Grid):

    def __init__(self, mapFile = None, currentGridName=""):
        """
        name = ""
        Descriptive name of the map, used within scripting engine

        mapFile = None
        Name of the map file to load
        """

        #making it an Entity
        Entity.__init__(self)
        Grid.__init__(self, mapFile=mapFile, currentGridName=currentGridName)
    
    def changedMap(self):
        # TODO: remove, deprecated
        #self.acceptOnce("changeMap", self.changeMap)
        playable = self.getPlayable()
        if playable != None:
            playable.setPlayable(True)
        else:
            print("WARNING: no playable set!")
    
    #apicall
    def changeMap(self, mapFile, position, face="down", animation='none'):
        f = FadeOut()
        
        callback = Sequence(
            Func(self.changedMap)
        )
        
        change = Sequence(
         Func(self.disablePlayable),
         #f.fadeIn(1),
         Func(self.changeMapHelper, mapFile, position, callback, face)
         #f.fadeOut(1),
        )
        
        if animation=='flyall':
            tiles = self.getAllTiles()
            totSequence = Sequence()
            flyallParallel = Parallel()
            flyallParallel.append(Func(self.disablePlayable))
            delay = 0
            delayFactor = 0.7
            for t in tiles:
                gameObjects = t.getGameObjects()
                for o in gameObjects:
                    node = o.getNode()
                    if o!=self.getPlayable():
                        s = Sequence()
                        nodeint = node.posInterval(2.0,Point3(node.getX(),node.getY()-15,node.getZ()+10),startPos = Point3(node.getX(),node.getY(),node.getZ()), blendType = 'easeIn', bakeInStart=1)
                        s.append(Wait(delay))
                        s.append(nodeint)
                        delay += delayFactor
                        flyallParallel.append(s)
            totSequence.append(flyallParallel)
            totSequence.append(Func(self.changeMapHelper, mapFile, position, callback, face))
            totSequence.start()
        
        if animation=='none':
            change.start()
    
    def changeMapHelper(self, mapFile, position, callback, face="down"):
        """
        Actually destroys the map and loads the new one
        """
        #executing code before killing the map
        #blocking
        if self.unloadScript != False:
            eval(self.unloadScript)
        
        #disabling all lights
        self.node.setLightOff()
        
        #manually removing tiles
        for t in self.tileset[:]:
            t.destroy()
            self.tileset.remove(t)
        
        #manually removing characters
        for c in self.characterset[:]:
            c.destroy()
            self.characterset.remove(c)
        
        #destroying every node
        for n in self.node.getChildren():
            n.removeNode()
        
        tks = position.split(',')
        if len(tks) > 1:
            x = int(tks[0])
            y = int(tks[1])
        else:
            print('ERROR: please define a correct position in .map file, resetting to 0,0')
            x = 0
            y = 0
        
        if not os.path.isfile(mapFile):
            self.loadMap(resourceManager.getResource('Mappe/'+mapFile),LPoint2i(x,y))
        else:
            self.loadMap(mapFile,LPoint2i(x,y))
        
        if main.editormode == False:
            self.getPlayable().setFollowedByCamera(True)
            self.getPlayable().face(face)
        
        self.currentMapPath = mapFile
        self.setCurrentGridNameEditor(mapFile.split('/')[-1].replace('.map', ''))
        
        if self.loadScript != False and main.editormode == False:
            eval(self.loadScript)
        
        callback.start()
    
    '''
    set a background image to be used into the map as borders go away
    '''
    def setBackgroundImage(self, imageurl):
        self.bgImage = imageurl
        imageurl = resourceManager.getResource(imageurl)+'.png'
        self.background = OnscreenImage(parent=render2dp, image=imageurl)
        base.cam2dp.node().getDisplayRegion(0).setSort(-20)

    def loadDataBlock(self, dataBlock):
        pass
    
    def loadMap(self,file="",playable_pos=LPoint2i(0,0)):
        '''
        loads map statically, probably going to be deprecated
        '''

        if self.getDynamicLoading() == True:
            print("WARNING: "+ str(self.getEntityName()) + " is loading map dynamically")
            print("WARNING: dynamic loading is enabled, this will cause some issues")

        if not file:
            file = self.mapFile

        if not os.path.isfile(file):
            print("WARNING: can't find map file, attempting resource parsing: "+file)

            if os.path.isfile(resourceManager.getResource('Mappe/'+file)):
                file = resourceManager.getResource('Mappe/'+file)
            else:
                print("ERROR: can't find map file (resourced): "+file)
                sys.exit()

        xmldoc = minidom.parse(file)
        
        data = xmldoc.getElementsByTagName('data')
        
        for d in data:
            if len(d.attributes) > 0:
                if 'tilesize' in d.attributes:
                    self.tileDimension = float(d.attributes['tilesize'].value)
                else:
                    self.tileDimension = 32.0
                if 'showcollisions' in d.attributes:
                    if d.attributes['showcollisions'].value == 'false':
                        self.showCollisions = False
                    else:
                        self.showCollisions = True
                else:
                    self.showCollisions = False
                if 'camdistance' in d.attributes:
                    customCamera.setDistance(float(d.attributes['camdistance'].value))
                else:
                    customCamera.setDistance(15)
                if 'bgImage' in d.attributes:
                    self.setBackgroundImage(d.attributes['bgImage'].value)
                else:
                    customCamera.setDistance(15)
                if 'onLoad' in d.attributes:
                    self.loadScript = d.attributes['onLoad'].value
                else:
                    self.loadScript = False
                    
                if 'onUnload' in d.attributes:
                    self.unloadScript = d.attributes['onUnload'].value
                else:
                    self.unloadScript = False

        
        rowsdata = xmldoc.getElementsByTagName('row')
        
        currentx = 0
        currenty = 0
        
        for row in rowsdata:                            #for every row
            for tile in row.childNodes:                 #for every tile
                if tile.nodeType == Node.ELEMENT_NODE:  #if child is tile
                    t = Tile(self.tileDimension)
                    t.setX(currentx)
                    t.setY(currenty)
                    
                    #apending lolol
                    self.tileset.append(t)
                    
                    o = Once() #lo switch viene fatto solo in presenza di una texture 'ground'
                    
                    for res in tile.childNodes:
                        if res.nodeType == Node.ELEMENT_NODE: # adding resources to tile
                            if res.nodeName == 'ground':
                                t.addTexture(res.attributes)
                                if o.get():
                                    currentx += 1
                            elif res.nodeName == 'object':
                                t.addObject(res.attributes)
                            elif res.nodeName == 'grass':
                                g = Grass(res.attributes, self.tileDimension) #creating object
                                t.addCustomObject(g) #setting coordinates of tile
                                g.getNode().wrtReparentTo(self.grassnode)
                            elif res.nodeName == 'light':
                                t.addLight(res.attributes)
                            elif res.nodeName == 'scrollable':
                                c = Scrollable(res.attributes['url'].value, res.attributes['inclination'].value, self.tileDimension)
                                c.setX(currentx)
                                c.setY(currenty)
                                self.scrollableset.append(c)
                            elif res.nodeName == 'character':
                                t.addCharacter(res.attributes, self.showCollisions, playable_pos)
                            
                    t.node.reparentTo(self.node)
            currentx = 0
            currenty += 1
        
        self.grassnode.flattenStrong() #pumping performance for dynamic grass (like, 120x)
    
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