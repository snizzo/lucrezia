#panda3d
from panda3d.core import NodePath, LPoint2i
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *

#standard python
from xml.dom import minidom
from xml.dom import Node

#internals
from utils.toggle import Toggle
from utils.once import Once
from objects.grass import Grass
from objects.light import Light
from tile import Tile
from character import Character

from utils.fadeout import FadeOut

import os

'''
This class abstracts the 2D grid commoly used in 2D games
to use with panda3d.

INTERNAL TILESET EXAMPLE GRAPH:
       x
  O------------>
  |
y |
  |
  |
  v
'''
class Grid(DirectObject):
    '''
    Autogenerates empty tileset at start
    '''
    def __init__(self):
        #variables initialization
        self.tileset = []
        self.characterset = []
        self.scrollableset = [] #fix this shiet, scollables can't definitely sit here...
        
        #only used in editor as for now, contains just mapname
        self.currentMapName = ''
        self.currentMapPath = ''
        
        #main nodes
        self.node = render.attachNewNode("tileset")
        self.grassnode = self.node.attachNewNode("grassnodes")
        
        #default value, just for fun
        self.tileDimension = 128.0
        self.showCollisions = False
        #automatic methods
        #self.generateEmptyTileset(20,20)
        #self.mergeMeshes()
        self.unloadScript = False
        self.loadScript = False
        
        self.acceptOnce("changeMap", self.changeMap)
    
    def changedMap(self):
        self.acceptOnce("changeMap", self.changeMap)
        self.getPlayable().setPlayable(True)
    
    def disablePlayable(self):
        if self.getPlayable() != None:
            self.getPlayable().setPlayable(False)
    
    #apicall
    def changeMap(self, mapFile, position):
        f = FadeOut()
        
        Sequence(
         Func(self.disablePlayable),
         f.fadeIn(1),
         Func(self.changeMapHelper, mapFile, position),
         Wait(3),
         f.fadeOut(1),
         Func(self.changedMap)
        ).start()
    
    #APICALL
    def getObjectsById(self, search):
        l = self.node.findAllMatches("**/=id="+search)
        s = []
        for e in l:
            s.append(e.getPythonTag("gamenode"))
        return s
    
    #APICALL
    def getObjectById(self, search):
        l = self.node.findAllMatches("**/=id="+search)
        if len(l) > 0:
            s = l[0].getPythonTag("gamenode")
        return s
    
    '''
    return the playable object of the game
    '''
    def getPlayable(self):
        return self.node.find("**/=playable=true").getPythonTag("gamenode")
    
    def changeMapHelper(self, mapFile, position):
        #executing code before killing the map
        if self.unloadScript != False:
            eval(self.unloadScript)
        
        #disabling all lights
        render.setLightOff()
        
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
            print 'ERROR: please define a correct position in .map file, resetting to 0,0'
            x = 0
            y = 0
        
        if not os.path.isfile(mapFile):
            self.loadMap(resourceManager.getResource('Mappe/'+mapFile),LPoint2i(x,y))
        else:
            self.loadMap(mapFile,LPoint2i(x,y))
        
        if main.editormode == False:
            self.getPlayable().setFollowedByCamera(True)
        
        self.currentMapPath = mapFile
        self.currentMapName = mapFile.split('/')[-1].replace('.map', '')
        
        if self.loadScript != False and main.editormode == False:
            eval(self.loadScript)
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
    
    '''
    @return string current map name
    '''
    def getCurrentMapName(self):
        return self.currentMapName
    
    '''
    @return string current map filepath
    '''
    def getCurrentMapPath(self):
        return self.currentMapPath
    
    def loadMap(self,file,playable_pos=LPoint2i(0,0)):
        xmldoc = minidom.parse(file)
        
        data = xmldoc.getElementsByTagName('data')
        for d in data:
            if d.attributes > 0:
                if d.attributes.has_key('tilesize'):
                    self.tileDimension = float(d.attributes['tilesize'].value)
                else:
                    self.tileDimension = 32.0
                if d.attributes.has_key('showcollisions'):
                    if d.attributes['showcollisions'].value == 'false':
                        self.showCollisions = False
                    else:
                        self.showCollisions = True
                else:
                    self.showCollisions = False
                if d.attributes.has_key('camdistance'):
                    customCamera.setDistance(float(d.attributes['camdistance'].value))
                else:
                    customCamera.setDistance(15)
                if d.attributes.has_key('onLoad'):
                    self.loadScript = d.attributes['onLoad'].value
                else:
                    self.loadScript = False
                    
                if d.attributes.has_key('onUnload'):
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
                                t.addCharacter(res.attributes, self.showCollisions, currentx, currenty, playable_pos)
                            
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
    @return Tile instance or -1 if tile is not found
    '''
    def getTile(self, x, y):
        for t in self.tileset:
            if t.getX() == x and t.getY() == y:
                return t
        
        return -1
    '''
    This method generates an internal tileset.
    Seen with list of lists (multidim array)
    
    The tileset is automatically placed at (0,0,0) and coloured
    chess-style.
    '''
    def generateEmptyTileset(self, x, y):
        colorSwitch = Toggle(False)
        
        for i in range(x):
            l = []
            
            for j in range(y):
                t = Tile()
                
                t.generate()
                
                #color switcher
                t.setTexture("misc/grass")
                
                #setting right coordinates
                t.setX(i-(x/2))
                t.setY(j-(y/2))
                #reparenting to grid node
                t.node.reparentTo(self.node)
                
                #appending to list
                l.append(t)
                    
                    
            self.tileset.append(l)
    
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
            print self.tileset[i]
    
    '''
    Debug method used to verify correct memory instantiation
    '''
    def ping(self):
        print "GRID: pong!"
